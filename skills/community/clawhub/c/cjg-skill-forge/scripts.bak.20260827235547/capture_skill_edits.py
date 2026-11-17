"""被动改动捕获：本地哈希基线 diff，记录 Skill 文件被编辑（edit_capture 信号）。

评审：skill2loop-p0-review-2026-08-21.md §8 (F6)
设计（本地优先、零云默认、零 PII）：
  - 只遍历含 references/signals.md 的技能（信号采集型技能）。
  - 维护 <skill_dir>/.skill_edit_baseline.json：{ "_date": "<当日>", "<relpath>": "<sha256 前16位>", ... }
  - 首次运行：仅建基线，不产信号（T-CAP-02）。
  - 后续运行（同一自然日）：对比**当日起始快照** → 增/改/删 → append 一行 edit_capture 信号到 signals-log.jsonl；
    基线不随运行更新（T-CAP-06：同日改后又还原 → 无净变化 → 不产新信号）；跨日自动重建基线。
  - 是否上行云由既有 .cloud_optin 控制（延续双模态；本脚本自身不上云）。

⚠️ 只读红线（T-CAP-01 生死线，发布阻断项）：
  - 绝不写入/修改/删除任何技能内容文件（SKILL.md / references/* / scripts/*）。
  - 唯一允许的写入：<skill_dir>/.skill_edit_baseline.json（运行时产物）+ signals-log.jsonl（append）。
  - P0 阶段只度量、不改动；任何 apply 必须等 P1 回归守卫落地。

用法：
  python capture_skill_edits.py                 # 遍历 ~/.workbuddy/skills
  python capture_skill_edits.py --base <dir>    # 指定技能根目录
  python capture_skill_edits.py --skill <name>  # 只处理单个技能（本地测试用）
  python capture_skill_edits.py --dry-run       # 只 diff 不写信号
"""
import argparse
import hashlib
import json
import os
import re
import sys
import uuid
from datetime import datetime, timezone, timedelta

# 范围白名单：只跟踪这些相对路径模式（跳过 .git/__pycache__/cloud-enhancement/运行时产物）
TRACK_GLOBS = (
    re.compile(r"^SKILL\.md$"),
    re.compile(r"^references/[^/]+\.md$"),
    re.compile(r"^scripts/[^/]+\.py$"),
)
# 运行时产物/无关目录，绝不跟踪
SKIP_DIRS = {".git", "__pycache__", "cloud-enhancement", ".claude-plugin", "node_modules"}
SKIP_FILES = {
    "signals-log.jsonl", ".skill_edit_baseline.json", ".uploaded_ids.txt",
    ".optin", ".cloud_optin", ".anon_id", "cloud_config.json", "config.json",
}
BASELINE_NAME = ".skill_edit_baseline.json"
CST = timezone(timedelta(hours=8))

# 相对路径校验（防 `..` 逃逸：只允许 base 内的相对路径）
_RELPATH_RE = re.compile(r"^(?!\.\.)[A-Za-z0-9_\-./]+$")


def _utcnow_iso():
    return datetime.now(CST).isoformat(timespec="microseconds")


def _sha16(path, chunk=1 << 20):
    """只读文件算 sha256 前 16 位；失败返回 None（不写入 baseline，下次再试）。"""
    h = hashlib.sha256()
    try:
        with open(path, "rb") as f:
            while True:
                block = f.read(chunk)
                if not block:
                    break
                h.update(block)
    except Exception:
        return None
    return h.hexdigest()[:16]


def _read_json(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return None


def _write_json(path, obj):
    try:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(obj, f, ensure_ascii=False, indent=1)
            f.flush()
            os.fsync(f.fileno())
        return True
    except Exception:
        return False


def _append_signal(skill_dir, sig):
    """append 一行信号到 signals-log.jsonl（与 upload_signals 同文件，行格式一致）。"""
    path = os.path.join(skill_dir, "signals-log.jsonl")
    try:
        with open(path, "a", encoding="utf-8") as f:
            f.write(json.dumps(sig, ensure_ascii=False) + "\n")
            f.flush()
            os.fsync(f.fileno())
        return True
    except Exception:
        return False


# ---------- 文件锁（防与 upload_signals 并发写 signals-log.jsonl）----------
try:
    import msvcrt  # Windows

    class _Lock:
        def __init__(self, path):
            self.path = path

        def __enter__(self):
            self.fd = open(self.path, "a+b")
            msvcrt.locking(self.fd.fileno(), msvcrt.LK_LOCK, 1)
            return self

        def __exit__(self, *a):
            try:
                self.fd.seek(0)
                msvcrt.locking(self.fd.fileno(), msvcrt.LK_UNLCK, 1)
            finally:
                self.fd.close()
except ImportError:
    try:
        import fcntl  # POSIX

        class _Lock:
            def __init__(self, path):
                self.path = path

            def __enter__(self):
                self.fd = open(self.path, "a+b")
                fcntl.flock(self.fd.fileno(), fcntl.LOCK_EX)
                return self

            def __exit__(self, *a):
                try:
                    fcntl.flock(self.fd.fileno(), fcntl.LOCK_UN)
                finally:
                    self.fd.close()
    except ImportError:
        class _Lock:  # 无锁平台：退化为空上下文
            def __init__(self, path):
                self.path = path

            def __enter__(self):
                return self

            def __exit__(self, *a):
                return None


def _read_skill_version(skill_dir):
    """从 SKILL.md frontmatter 读 version（失败返回 None）。"""
    try:
        with open(os.path.join(skill_dir, "SKILL.md"), "r", encoding="utf-8") as f:
            head = f.read(2048)
        m = re.search(r"^version:\s*(\S+)", head, re.MULTILINE)
        return m.group(1) if m else None
    except Exception:
        return None


def _read_anon_id(skill_dir):
    try:
        with open(os.path.join(skill_dir, ".anon_id"), "r", encoding="utf-8") as f:
            return f.read().strip() or None
    except Exception:
        return None


def _tracked_files(skill_dir):
    """遍历技能目录，返回受白名单约束的相对路径列表（相对、正斜杠、无 .. 逃逸）。"""
    out = []
    for root, dirs, files in os.walk(skill_dir):
        rel_root = os.path.relpath(root, skill_dir).replace("\\", "/")
        if rel_root == ".":
            rel_root = ""
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
        for fn in files:
            if fn in SKIP_FILES:
                continue
            rel = f"{rel_root}/{fn}" if rel_root else fn
            if not _RELPATH_RE.match(rel):
                continue
            if any(g.match(rel) for g in TRACK_GLOBS):
                out.append(rel)
    return sorted(out)


def _snapshot(skill_dir):
    """只读快照：{relpath: sha16}；文件缺失跳过（可能在删除中）。"""
    snap = {}
    for rel in _tracked_files(skill_dir):
        h = _sha16(os.path.join(skill_dir, rel.replace("/", os.sep)))
        if h is not None:
            snap[rel] = h
    return snap


def _today():
    return datetime.now(CST).strftime("%Y-%m-%d")


def _read_baseline(skill_dir):
    """读取基线；若无 / 损坏 / 跨日 → 返回 None（触发首跑重建，T-CAP-09 / 每日基线）。"""
    b = _read_json(os.path.join(skill_dir, BASELINE_NAME))
    if not isinstance(b, dict):
        return None
    if b.get("_date") != _today():
        return None  # 跨日：按新的一天重建基线（不产信号）
    return {k: v for k, v in b.items() if k != "_date"}


def _write_baseline(skill_dir, snap):
    payload = {"_date": _today()}
    payload.update(snap)
    return _write_json(os.path.join(skill_dir, BASELINE_NAME), payload)


def run_for_skill(skill_dir, dry_run=False):
    """对单个技能跑一轮捕获。返回 (ok, stats) stats={added,modified,deleted,first_run}。

    每日基线语义（T-CAP-06）：同一自然日内，多次运行对比**当日基线**；
    文件改后又还原 → 与当日基线无净变化 → 不产新信号。跨日自动重建基线。
    """
    name = os.path.basename(skill_dir.rstrip("/\\"))
    if not os.path.exists(os.path.join(skill_dir, "references", "signals.md")):
        return False, None  # 非信号技能，跳过

    baseline_path = os.path.join(skill_dir, BASELINE_NAME)
    lock_path = os.path.join(skill_dir, ".capture.lock")
    prev = _read_baseline(skill_dir)
    stats = {"added": 0, "modified": 0, "deleted": 0, "first_run": False}

    if prev is None:
        # 首跑 / baseline 损坏 / 跨日：仅建基线，不产信号（T-CAP-02/09）
        snap = _snapshot(skill_dir)
        if not dry_run:
            _write_baseline(skill_dir, snap)
        stats["first_run"] = True
        print(f"[capture] [{name}] 首跑：仅建基线（{len(snap)} 文件），不产信号")
        return True, stats

    current = _snapshot(skill_dir)
    rel_paths = sorted(set(list(prev.keys()) + list(current.keys())))
    with _Lock(lock_path):
        anon_id = _read_anon_id(skill_dir)
        skill_version = _read_skill_version(skill_dir)
        for rel in rel_paths:
            old = prev.get(rel)
            new = current.get(rel)
            if old is None and new is not None:
                kind = "add"
                stats["added"] += 1
            elif old is not None and new is None:
                kind = "delete"
                stats["deleted"] += 1
            elif old != new:
                kind = "modify"
                stats["modified"] += 1
            else:
                continue
            if dry_run:
                print(f"[capture] [{name}] DRY-RUN {kind}: {rel}")
                continue
            sig = {
                "ts": _utcnow_iso(),
                "signal_id": str(uuid.uuid4()),
                "skill_slug": name,
                "skill_version": skill_version,
                "method_layer": "L2",
                "event": "edit_capture",
                "weight": 1,
                "note": f"{kind}:{rel}",  # 仅相对路径 + kind，零 PII
                "anon_id": anon_id or "",
            }
            # 只 append 信号；绝不触碰技能内容文件本身
            _append_signal(skill_dir, sig)
            print(f"[capture] [{name}] {kind}: {rel}")
        # ⚠️ 基线保持"当日起始快照"不更新（T-CAP-06：同日改后又还原 → 与当日基线无净变化 → 不产新信号）
        #    跨日由 _read_baseline 的 _date 检查自动重建基线。
    total = stats["added"] + stats["modified"] + stats["deleted"]
    print(f"[capture] [{name}] 完成：add={stats['added']} modify={stats['modified']} delete={stats['deleted']} 合计={total}")
    return True, stats


def main():
    ap = argparse.ArgumentParser(description="被动改动捕获（edit_capture，只读红线）")
    ap.add_argument("--base", default=os.path.expanduser("~/.workbuddy/skills"),
                    help="技能根目录（默认 ~/.workbuddy/skills）")
    ap.add_argument("--skill", default=None, help="只处理单个技能目录名（本地测试用）")
    ap.add_argument("--dry-run", action="store_true", help="只 diff 不写信号")
    args = ap.parse_args()

    if args.skill:
        target = os.path.join(args.base, args.skill)
        if not os.path.isdir(target):
            print(f"[capture] 技能目录不存在: {target}", file=sys.stderr)
            sys.exit(1)
        ok, _ = run_for_skill(target, dry_run=args.dry_run)
        sys.exit(0 if ok else 2)

    total_ok = 0
    total_skills = 0
    for name in sorted(os.listdir(args.base)):
        d = os.path.join(args.base, name)
        if not os.path.isdir(d):
            continue
        if not os.path.exists(os.path.join(d, "references", "signals.md")):
            continue
        total_skills += 1
        ok, _ = run_for_skill(d, dry_run=args.dry_run)
        if ok:
            total_ok += 1
    print(f"[capture] 完成 {total_ok}/{total_skills} 个信号技能")
    sys.exit(0 if total_ok == total_skills else 2)


if __name__ == "__main__":
    main()
