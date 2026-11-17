#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
writer_bridge.py — 调用 hekouwang-writer-skill 的检查脚本，把结果折算成内容门禁的检查项。

本 skill 运行时依赖 hekouwang-writer-skill（>= 1.1.0）。查找顺序：
  1. 显式传入的目录（content_gate.py --writer-dir）
  2. 环境变量 HEKOUWANG_WRITER_SKILL_DIR
  3. 与本 skill 同级的 hekouwang-writer-skill/（ClawHub、SkillHub、~/.claude/skills 等安装方式都是同级）
  4. ~/.claude/skills、~/.codex/skills、~/.agents/skills、~/.cursor/skills 下的 hekouwang-writer-skill/

找不到或版本过低时，门禁直接 block，并给出安装命令。

折算规则（level=block 拦截，level=warn 只提醒）：
  写作规范·锯末词      sawdust_scan 判定超密度 → block；有命中但未超 → warn
  写作规范·必拆长句    sentence_load 有超必拆线且无放行理由的句子 → block
  写作规范·长句告警    告警线句子 → warn
  写作规范·分句堆叠    句内逗号/分号 ≥5 → warn
  写作规范·敏感信息    doc_lint 发现完整身份证号或手机号 → block
  写作规范·分号        doc_lint 分号密度超线 → warn
  写作规范·结构        doc_lint 硬错误（表格列数、标题层级）→ block
  写作规范·算术对账    check_fidelity 发现等式或合计对不上 → block
"""
import json
import os
import subprocess
import sys
from pathlib import Path

WRITER_SLUG = "hekouwang-writer-skill"
MIN_VERSION = (1, 1, 0)
ENV_KEY = "HEKOUWANG_WRITER_SKILL_DIR"
REQUIRED = ("sawdust_scan.py", "sentence_load.py", "doc_lint.py", "check_fidelity.py")
INSTALL_HINT = (f"先安装 {WRITER_SLUG}：clawhub install {WRITER_SLUG}，"
                f"或 git clone https://github.com/huiyonghkw/{WRITER_SLUG} 到本 skill 同级目录，"
                f"或设置环境变量 {ENV_KEY}")
TIMEOUT = 30


def _candidates(explicit=None):
    if explicit:
        yield Path(explicit).expanduser()
    if os.environ.get(ENV_KEY):
        yield Path(os.environ[ENV_KEY]).expanduser()
    yield Path(__file__).resolve().parents[1].parent / WRITER_SLUG
    home = Path.home()
    for base in (".claude/skills", ".codex/skills", ".agents/skills", ".cursor/skills"):
        yield home / base / WRITER_SLUG


def _is_writer(d: Path) -> bool:
    return all((d / "scripts" / name).is_file() for name in REQUIRED)


def find_writer_dir(explicit=None):
    for d in _candidates(explicit):
        if _is_writer(d):
            return d
    return None


def _parse_version(s: str):
    parts = []
    for p in str(s).split(".")[:3]:
        digits = "".join(ch for ch in p if ch.isdigit())
        parts.append(int(digits) if digits else 0)
    return tuple(parts + [0] * (3 - len(parts)))


def writer_version(d: Path):
    meta = d / "_meta.json"
    if meta.is_file():
        try:
            return json.loads(meta.read_text(encoding="utf-8")).get("version")
        except (OSError, ValueError):
            return None
    return None


def _run(d: Path, script: str, text: str) -> dict:
    proc = subprocess.run([sys.executable, str(d / "scripts" / script), "--json"],
                          input=text, capture_output=True, text=True, timeout=TIMEOUT)
    if not proc.stdout.strip():
        raise RuntimeError(f"{script} 无输出：{proc.stderr.strip()[-200:]}")
    return json.loads(proc.stdout)


def _short(s: str, n: int = 24) -> str:
    s = s.strip()
    return s if len(s) <= n else s[:n] + "…"


def writer_checks(text: str, writer_dir=None) -> list:
    """返回 [{"check","pass","detail","level"}]，与 content_gate.check 的结果项同构。"""
    out = []

    def add(name, passed, detail, level="block"):
        out.append({"check": name, "pass": bool(passed), "detail": detail, "level": level})

    d = find_writer_dir(writer_dir)
    if d is None:
        add("写作规范依赖", False, f"找不到 {WRITER_SLUG}。{INSTALL_HINT}")
        return out
    ver = writer_version(d)
    if ver is None or _parse_version(ver) < MIN_VERSION:
        need = ".".join(map(str, MIN_VERSION))
        add("写作规范依赖", False,
            f"{d} 的版本是 {ver or '未知'}，需要 >= {need}。clawhub update {WRITER_SLUG} 或 git pull")
        return out

    try:
        saw = _run(d, "sawdust_scan.py", text)
        load = _run(d, "sentence_load.py", text)
        lint = _run(d, "doc_lint.py", text)
        fid = _run(d, "check_fidelity.py", text)
    except (OSError, ValueError, RuntimeError, subprocess.TimeoutExpired) as e:
        add("写作规范依赖", False, f"调用 {WRITER_SLUG} 失败：{e}")
        return out
    add("写作规范依赖", True, f"{WRITER_SLUG} {ver}（{d}）")

    words = [f"{w}×{n}" for group in saw.get("findings", {}).values() for w, n in group.items()]
    if saw.get("over"):
        add("写作规范·锯末词", False,
            f"命中 {words}，密度 {saw.get('density')} 处/千字（上限 {saw.get('threshold')}）。删掉或换成数字")
    else:
        add("写作规范·锯末词", not words, f"命中 {words}" if words else "无", level="block" if not words else "warn")

    hard = [e for e in load.get("over", []) if not e.get("release")]
    add("写作规范·必拆长句", not hard,
        f"{len(hard)} 句 ≥{load.get('split')} 字：" + "；".join(f"「{_short(e['sentence'])}」{e['len']}字" for e in hard)
        if hard else "无")
    warn_items = load.get("warn_items", [])
    add("写作规范·长句告警", not warn_items,
        "；".join(f"「{_short(e['sentence'])}」{e['len']}字" for e in warn_items) if warn_items else "无",
        level="warn")
    stacked = load.get("stacked", [])
    add("写作规范·分句堆叠", not stacked,
        "；".join(f"「{_short(e['sentence'])}」" for e in stacked) + "（拆句或改列表）" if stacked else "无",
        level="warn")

    warnings = lint.get("warnings", [])
    sensitive = [w for w in warnings if "身份证" in w or "手机号" in w]
    add("写作规范·敏感信息", not sensitive, "；".join(sensitive) if sensitive else "无")
    semi = [w for w in warnings if w.startswith("分号密度")]
    add("写作规范·分号", not semi, semi[0] + "（一句一事，分号拆成句号）" if semi else "无", level="warn")
    hard_errors = lint.get("hard_errors", [])
    add("写作规范·结构", not hard_errors, "；".join(hard_errors) if hard_errors else "无")

    fid_errors = fid.get("errors", [])
    add("写作规范·算术对账", not fid_errors,
        "；".join(str(e) for e in fid_errors) if fid_errors else "无")
    return out


if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser(description="用 hekouwang-writer-skill 检查一段点评文案")
    ap.add_argument("text", nargs="?", help="待检查文本；省略时读 stdin")
    ap.add_argument("--writer-dir")
    args = ap.parse_args()
    res = writer_checks(args.text if args.text is not None else sys.stdin.read(), args.writer_dir)
    print(json.dumps(res, ensure_ascii=False, indent=2))
    sys.exit(0 if all(r["pass"] for r in res if r["level"] == "block") else 1)
