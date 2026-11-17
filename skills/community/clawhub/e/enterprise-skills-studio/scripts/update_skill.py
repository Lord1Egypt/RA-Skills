#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
update_skill.py - 企业技能工程台 自更新器（Self-Updater）

从可信 GitHub 仓库拉取最新发布版本，增量更新本技能的本地安装副本。
纯标准库实现（urllib / tarfile / shutil），零外部依赖。

设计要点（贴合本技能"厚技能 + 薄 harness"与治理原则）：
  - 单一可信源：固定的 repo（默认 jiwei1122/enterprise-skills-studio），**钉置到最新发布标签(经人工发布、不可变)**，而非易变分支，规避供应链投毒
  - 版本真相：本地 VERSION 文件 与 远程 VERSION 文件 比较（语义化版本）
  - 增量合并：只覆盖/新增远程有的文件，保留本地额外文件（不删本地独有文件）
  - 安全：只解包 + 复制文件，绝不执行远程下载的任何代码；归档做路径穿越校验
  - 可回滚：--backup 先快照当前目录到临时目录，失败可手动还原
  - git 保护：若技能目录本身是 git 仓库，默认中止以免覆盖工作区（--force 可强制）
  - 完整性：归档内含 SHA256SUMS 时逐文件校验，不匹配即中止（防篡改）
  - 白名单：仅白名单路径(SKILL.md/references/*/scripts/*/assets/*等)被覆盖，越界文件跳过
  - 企业管控：环境变量 ESS_SELF_UPDATE=off 可禁用写盘更新；ESS_ALLOWED_REPOS 限定可拉取仓库

用法：
  python update_skill.py --check                 # 仅检查（默认动作；退出码 0=最新 1=有更新 2=错误）
  python update_skill.py --check --json          # 机器可读输出
  python update_skill.py --apply                 # 交互确认（明确警告将覆盖本地文件）后更新
  python update_skill.py --apply --yes           # 跳过确认直接更新
  python update_skill.py --apply --dry-run       # 仅打印将变更的文件，不写盘
  python update_skill.py --apply --backup        # 更新前先快照备份
  python update_skill.py --gen-sum               # 生成 SHA256SUMS（发布侧，需提交到仓库根）
  python update_skill.py --apply --repo owner/repo --ref v1.2.3   # 私有化/钉置指定版本
"""
import argparse
import hashlib
import json
import os
import re
import shutil
import sys
import tarfile
import tempfile
import urllib.error
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
SKILL_DIR = os.path.dirname(HERE)            # scripts/ 的父目录 = 技能根
VERSION_FILE = os.path.join(SKILL_DIR, "VERSION")

DEFAULT_REPO = "jiwei1122/enterprise-skills-studio"
DEFAULT_BRANCH = "main"
# 钉置策略：默认解析「最新发布标签」(经人工发布、不可变)，而非易变的 main 分支，
# 规避供应链投毒（攻击者向 main 推恶意代码即被自更新拉取）。--ref 可强制钉置到指定标签/提交。
LATEST_RELEASE_API = "https://api.github.com/repos/{repo}/releases/latest"

# 企业管控项
# 1) 禁用自更新开关：设置环境变量 ESS_SELF_UPDATE=off 可彻底关闭写盘更新（检查仍可用）。
# 2) 私有化 repo 白名单：设置环境变量 ESS_ALLOWED_REPOS="a/b,c/d"（逗号分隔），
#    仅允许从这些仓库拉取；未设置则仅允许 DEFAULT_REPO。
DISABLE_ENV = "ESS_SELF_UPDATE"
ALLOWED_REPOS_ENV = "ESS_ALLOWED_REPOS"

# 合并白名单：仅允许这些路径被自更新覆盖/新增，杜绝归档中夹带非常规文件（如 ../../etc/cron）。
# 即便 SHA256SUMS 校验被绕过，越界文件也绝不会被写入。
ALLOWED_PATH_RE = re.compile(
    r"^(SKILL\.md|VERSION|README\.md|LICENSE|CHANGELOG\.md|SECURITY\.md|"
    r"references/.*|scripts/.*|assets/.*)$"
)

SUMS_FILENAME = "SHA256SUMS"


# ---------------------------------------------------------------------------
# 版本解析与比较
# ---------------------------------------------------------------------------
def parse_version(s):
    """'v1.2.3' / '1.2.3' -> (1, 2, 3)；失败返回 None。"""
    if not s:
        return None
    s = s.strip().lstrip("vV")
    parts = []
    for p in s.split("."):
        p = p.strip()
        parts.append(int(p) if p.isdigit() else 0)
    if not parts:
        return None
    while len(parts) < 3:
        parts.append(0)
    return tuple(parts[:3])


def read_local_version():
    try:
        with open(VERSION_FILE, "r", encoding="utf-8") as f:
            return f.read().strip()
    except OSError:
        return ""


def compare_versions(local, remote):
    """返回 'ahead' | 'equal' | 'behind' | 'unknown'。"""
    lv = parse_version(local)
    rv = parse_version(remote)
    if lv is None or rv is None:
        return "unknown"
    if lv < rv:
        return "behind"
    if lv > rv:
        return "ahead"
    return "equal"


# ---------------------------------------------------------------------------
# 网络
# ---------------------------------------------------------------------------
def fetch_remote_text(url, timeout=20):
    req = urllib.request.Request(
        url, headers={"User-Agent": "enterprise-skills-studio-updater"})
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return resp.read().decode("utf-8", "replace")


def get_target(args):
    """解析自更新目标引用（钉置）。

    优先级：--ref > 最新「发布标签」(不可变) > --branch(默认 main，易变)。
    返回 (ref, kind, raw_version_url, archive_url)。kind='tags' 表示已钉置到不可变版本，
    kind='heads' 表示回退到分支（易变，会在日志告警）。
    """
    ref = getattr(args, "ref", None)
    if ref:
        return (ref, "tags",
                f"https://raw.githubusercontent.com/{args.repo}/{ref}/VERSION",
                f"https://github.com/{args.repo}/archive/refs/tags/{ref}.tar.gz")
    # 钉置：优先解析最新发布标签（经人工发布、不可变），规避拉取易变的 main
    try:
        data = json.loads(fetch_remote_text(
            LATEST_RELEASE_API.format(repo=args.repo), timeout=20))
        tag = data.get("tag_name")
        if tag:
            return (tag, "tags",
                    f"https://raw.githubusercontent.com/{args.repo}/{tag}/VERSION",
                    f"https://github.com/{args.repo}/archive/refs/tags/{tag}.tar.gz")
    except Exception:
        pass
    # 回退：仓库未发布 Release 时，回退到分支（易变，仅作兜底）
    branch = args.branch or DEFAULT_BRANCH
    return (branch, "heads",
            f"https://raw.githubusercontent.com/{args.repo}/{branch}/VERSION",
            f"https://github.com/{args.repo}/archive/refs/heads/{branch}.tar.gz")


# ---------------------------------------------------------------------------
# 文件工具
# ---------------------------------------------------------------------------
def walk_files(root):
    """相对路径集合（跳过 .git）。"""
    out = set()
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d != ".git"]
        for fn in filenames:
            full = os.path.join(dirpath, fn)
            rel = os.path.relpath(full, root)
            out.add(rel.replace(os.sep, "/"))
    return out


def files_equal(a, b):
    try:
        with open(a, "rb") as fa, open(b, "rb") as fb:
            return fa.read() == fb.read()
    except OSError:
        return False


def merge_copy(src_root, dst_root, dry_run=False):
    """把 src_root 内容增量合并进 dst_root。返回 (added, updated, removed)。

    仅允许白名单路径（is_allowed_path）被覆盖/新增，越界文件直接跳过，
    杜绝归档中夹带非常规文件（如 ../../etc/cron）被写入技能目录。
    """
    src_files = walk_files(src_root)
    dst_files = walk_files(dst_root)
    added, updated = [], []
    for rel in src_files:
        if not is_allowed_path(rel):
            print(f"⚠️ 跳过白名单外文件（不被自更新覆盖）: {rel}", file=sys.stderr)
            continue
        s = os.path.join(src_root, rel)
        d = os.path.join(dst_root, rel)
        if os.path.exists(d):
            if not files_equal(s, d):
                updated.append(rel)
        else:
            added.append(rel)
        if not dry_run:
            os.makedirs(os.path.dirname(d), exist_ok=True)
            shutil.copy2(s, d)
    removed = sorted(r for r in dst_files if r not in src_files)
    return added, updated, removed


def safe_extract(tf, dest):
    """带路径穿越防护的解包。"""
    dest_abs = os.path.abspath(dest)
    for m in tf.getmembers():
        target = os.path.abspath(os.path.join(dest_abs, m.name))
        if target != dest_abs and not target.startswith(dest_abs + os.sep):
            raise tarfile.TarError(f"非法归档成员路径（疑似穿越）: {m.name}")
    tf.extractall(dest_abs)


def backup_skill(dst_root):
    tmp = tempfile.mkdtemp(prefix="ess_backup_")
    dest = os.path.join(tmp, "enterprise-skills-studio")
    shutil.copytree(dst_root, dest, ignore=shutil.ignore_patterns(".git"))
    return dest


def is_allowed_path(rel):
    """合并白名单：仅允许已知技能文件被覆盖/新增。"""
    return bool(ALLOWED_PATH_RE.match(rel))


def compute_sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def gen_sums(root):
    """为 root 下所有白名单文件生成 SHA256SUMS（发布侧调用，提交到仓库根）。"""
    rows = []
    for rel in sorted(walk_files(root)):
        if not is_allowed_path(rel):
            continue
        full = os.path.join(root, rel)
        rows.append(f"{compute_sha256(full)}  {rel}")
    sums_path = os.path.join(root, SUMS_FILENAME)
    with open(sums_path, "w", encoding="utf-8") as f:
        f.write("\n".join(rows) + "\n")
    return sums_path


def verify_sums(extracted_root):
    """校验解包目录内白名单文件的 sha256 是否匹配 SHA256SUMS。

    返回 (status, detail)。
      ("ok", ...)       全部匹配
      ("missing", ...) 归档内无 SHA256SUMS（发布未生成），交调用方决定
      ("fail", ...)    存在不匹配项（疑似被篡改）
    """
    sums_path = os.path.join(extracted_root, SUMS_FILENAME)
    if not os.path.isfile(sums_path):
        return ("missing", "归档内未提供 SHA256SUMS")
    expected = {}
    with open(sums_path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            h, _, name = line.partition("  ")
            expected[name.strip()] = h.strip()
    for rel, want in expected.items():
        full = os.path.join(extracted_root, rel)
        if not os.path.isfile(full):
            return ("fail", f"SHA256SUMS 列出了缺失文件: {rel}")
        if compute_sha256(full) != want:
            return ("fail", f"文件校验和不匹配（疑似被篡改）: {rel}")
    return ("ok", f"已校验 {len(expected)} 个文件")


def repo_allowed(repo):
    """判断 repo 是否允许拉取（默认仅 DEFAULT_REPO；可经 ESS_ALLOWED_REPOS 扩展）。"""
    if repo == DEFAULT_REPO:
        return True
    allow = os.environ.get(ALLOWED_REPOS_ENV, "").strip()
    if allow:
        return repo in [r.strip() for r in allow.split(",") if r.strip()]
    return False



# ---------------------------------------------------------------------------
# 动作
# ---------------------------------------------------------------------------
def do_check(args):
    ref, kind, raw_url, _ = get_target(args)
    if kind == "heads":
        print(f"⚠️ 未钉置到发布标签，回退至分支 {ref}（建议发布 GitHub Release 以钉置不可变版本）",
              file=sys.stderr)
    local = read_local_version()
    try:
        remote = fetch_remote_text(raw_url).strip()
    except (urllib.error.URLError, urllib.error.HTTPError, OSError) as e:
        msg = f"无法获取远程版本: {e}"
        if args.json:
            print(json.dumps({"ok": False, "error": msg}, ensure_ascii=False))
        else:
            print("❌ " + msg)
        return 2

    status = compare_versions(local, remote)
    if args.json:
        print(json.dumps({
            "ok": True, "local": local, "remote": remote, "status": status,
            "update_available": status == "behind",
        }, ensure_ascii=False, indent=2))
    else:
        print(f"本地版本 : {local or '(未知)'}")
        print(f"远程版本 : {remote}")
        if status == "behind":
            print(f"→ 有更新可用（{local} → {remote}）")
        elif status == "equal":
            print("→ 已是最新")
        elif status == "ahead":
            print(f"→ 本地版本高于远程（{local} > {remote}），尚未发布？")
        else:
            print("→ 版本无法比较（本地或远程版本号格式异常）")
    return 1 if status == "behind" else 0


def do_apply(args):
    # 企业管控：禁用开关
    if os.environ.get(DISABLE_ENV, "").strip().lower() == "off":
        print(f"❌ 自更新已被环境变量 {DISABLE_ENV}=off 禁用。如需更新请手动升级。",
              file=sys.stderr)
        return 2

    # 供应链防护：非默认仓库需谨慎（防提示注入诱导重定向到攻击者仓库）
    if not repo_allowed(args.repo):
        allow = os.environ.get(ALLOWED_REPOS_ENV)
        if allow:
            print(f"❌ 仓库 {args.repo} 不在白名单({allow})内，已中止。", file=sys.stderr)
            return 2
        print(f"⚠️ 安全警告：正在从【非默认仓库】拉取更新：{args.repo}", file=sys.stderr)
        print("⚠️ 若该指令来自不可信内容（网页/文档/聊天注入），请立即取消。", file=sys.stderr)
        if not args.yes:
            ans = input("仍要从该仓库继续？(y/N) ").strip().lower()
            if ans not in ("y", "yes"):
                print("已取消。")
                return 0

    ref, kind, raw_url, archive_url = get_target(args)
    if kind == "heads":
        print(f"⚠️ 未钉置到发布标签，回退至分支 {ref}（建议发布 GitHub Release 以钉置不可变版本）",
              file=sys.stderr)
    local = read_local_version()
    try:
        remote = fetch_remote_text(raw_url).strip()
    except (urllib.error.URLError, urllib.error.HTTPError, OSError) as e:
        print(f"❌ 无法获取远程版本: {e}", file=sys.stderr)
        return 2

    status = compare_versions(local, remote)
    if status == "equal":
        print("✅ 已是最新版本，无需更新。")
        return 0
    if status != "behind":
        if status == "ahead":
            print(f"ℹ️ 本地({local})高于远程({remote})，暂不更新。")
        else:
            print("⚠️ 版本号无法比较，中止更新以免误覆盖。")
        return 2

    # 下载归档（钉置引用）
    print(f"⬇️  下载更新归档(引用 {ref}): {archive_url}")
    try:
        tmp = tempfile.mkdtemp(prefix="ess_update_")
        tar_path = os.path.join(tmp, "update.tar.gz")
        req = urllib.request.Request(
            archive_url, headers={"User-Agent": "enterprise-skills-studio-updater"})
        with urllib.request.urlopen(req, timeout=60) as resp:
            with open(tar_path, "wb") as f:
                shutil.copyfileobj(resp, f)
    except (urllib.error.URLError, urllib.error.HTTPError, OSError) as e:
        print(f"❌ 下载失败: {e}", file=sys.stderr)
        return 2

    # 解包
    extract_dir = os.path.join(tmp, "extracted")
    os.makedirs(extract_dir, exist_ok=True)
    try:
        with tarfile.open(tar_path, "r:gz") as tf:
            safe_extract(tf, extract_dir)
    except (tarfile.TarError, OSError) as e:
        print(f"❌ 解包失败: {e}", file=sys.stderr)
        return 2

    # 定位根目录（GitHub 归档顶层为 <repo>-<branch>）
    entries = [e for e in os.listdir(extract_dir) if not e.startswith(".")]
    root = extract_dir
    if len(entries) == 1 and os.path.isdir(os.path.join(extract_dir, entries[0])):
        root = os.path.join(extract_dir, entries[0])

    # 安全：确认远程根目录含 SKILL.md，避免误用畸形归档
    if not os.path.isfile(os.path.join(root, "SKILL.md")):
        print("❌ 归档内未找到 SKILL.md，中止（防误覆盖）。", file=sys.stderr)
        return 2

    # 完整性校验：核对 SHA256SUMS（若存在且不匹配则视为被篡改，立即中止）
    vstatus, vdetail = verify_sums(root)
    if vstatus == "fail":
        print(f"❌ {vdetail}，中止更新。", file=sys.stderr)
        return 2
    if vstatus == "missing":
        print(f"⚠️ {vdetail}；建议发布时运行 `update_skill.py --gen-sum` 并提交 SHA256SUMS。"
              "本次仍以钉置标签为准继续。", file=sys.stderr)
        # 非默认仓库在无校验和时强制要求 --yes（上方已在 repo 检查处处理）

    # 差异预览
    added, updated, removed = merge_copy(root, SKILL_DIR, dry_run=True)
    print(f"\n将要应用更新 {local} → {remote}")
    print(f"  新增文件 : {len(added)}")
    print(f"  更新文件 : {len(updated)}")
    print(f"  本地独有（保留，不删除）: {len(removed)}")
    if args.verbose:
        for r in sorted(added)[:80]:
            print(f"    + {r}")
        for r in sorted(updated)[:80]:
            print(f"    ~ {r}")

    if args.dry_run:
        print("\n🔍 dry-run 完成，未做任何修改。")
        return 0

    if not args.yes:
        ans = input(
            "\n⚠️ 即将覆盖本技能【本地文件】，可能影响其当前行为。确认应用以上更新？(y/N) "
        ).strip().lower()
        if ans not in ("y", "yes"):
            print("已取消。")
            return 0

    # git 仓库保护
    if os.path.isdir(os.path.join(SKILL_DIR, ".git")) and not args.force:
        print("❌ 检测到本目录是 git 仓库，为避免覆盖工作区，已中止。"
              "若确定要更新请加 --force。", file=sys.stderr)
        return 2

    # 备份
    backup_path = None
    if args.backup:
        backup_path = backup_skill(SKILL_DIR)
        print(f"📦 已备份当前版本至: {backup_path}")

    # 应用
    merge_copy(root, SKILL_DIR, dry_run=False)
    new_local = read_local_version()
    print(f"\n✅ 更新完成：{local} → {new_local}（来自 {args.repo}@{ref}）")
    if backup_path:
        print(f"   如需回滚：将 {backup_path} 内容复制回技能目录即可。")
    return 0


def do_gen_sum(args):
    """生成 SHA256SUMS（发布侧调用）。"""
    path = gen_sums(SKILL_DIR)
    print(f"已生成校验和文件: {path}")
    print("请将其提交到仓库根目录；自更新会据此校验归档完整性。")
    return 0


def main():
    global SKILL_DIR, VERSION_FILE
    ap = argparse.ArgumentParser(description="企业技能工程台 自更新器")
    ap.add_argument("--check", action="store_true", help="仅检查更新（默认动作）")
    ap.add_argument("--apply", action="store_true", help="应用更新（默认需交互确认）")
    ap.add_argument("--dry-run", action="store_true", help="只预览变更，不写盘")
    ap.add_argument("--backup", action="store_true", help="更新前快照备份当前目录")
    ap.add_argument("--yes", action="store_true", help="跳过交互确认")
    ap.add_argument("--force", action="store_true", help="即使目录是 git 仓库也更新")
    ap.add_argument("--json", action="store_true", help="--check 输出 JSON")
    ap.add_argument("--verbose", action="store_true", help="打印变更文件清单")
    ap.add_argument("--gen-sum", action="store_true",
                    help="生成 SHA256SUMS 校验和（发布侧调用，需提交到仓库根）")
    ap.add_argument("--repo", default=DEFAULT_REPO,
                    help=f"GitHub repo（默认 {DEFAULT_REPO}；仅允许的仓库可被拉取）")
    ap.add_argument("--ref", default=None,
                    help="钉置到指定标签/提交（如 v1.0.1）；默认解析最新发布标签(不可变)，避免拉取易变分支")
    ap.add_argument("--branch", default=DEFAULT_BRANCH,
                    help=f"分支（默认 {DEFAULT_BRANCH}）")
    ap.add_argument("--skill-dir", default=SKILL_DIR,
                    help="覆盖技能根目录（默认自动探测）")
    args = ap.parse_args()

    if args.skill_dir:
        SKILL_DIR = os.path.abspath(args.skill_dir)
        VERSION_FILE = os.path.join(SKILL_DIR, "VERSION")

    if args.gen_sum:
        return do_gen_sum(args)
    if args.apply:
        return do_apply(args)
    return do_check(args)


if __name__ == "__main__":
    sys.exit(main())
