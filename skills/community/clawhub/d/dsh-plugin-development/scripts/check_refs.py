#!/usr/bin/env python3
"""校验 skill 内部所有「指向文件」的引用都能在本 skill 内解析。

为什么需要它：skill 是**自包含**发布物（`references/` `assets/` `scripts/` 之外的路径
在用户机器上都不存在）。一旦正文里留下生成期的素材路径（如 `plugin-research/notes/…`）
或本机绝对路径，引用就会指向空气，且**不会报错**——属于本项目的典型「静默失效」。

分类规则（避免把 DSH 上游路径误判为悬空）：
  OK-内   `references/` `assets/` `scripts/` 下且文件真实存在
  OK-外   形如 `packages/…` `apps/…` `docs/…` `vendor/…` `src/…` `.agents/…`
          —— 这些是 **DSH 上游仓库**里的路径，本 skill 只做引用说明，属合法
  ❌ 素材  `plugin-research/…`、`notes/X.md`、裸 `A~J-*.md` —— 生成期调研素材，不在 skill 内
  ❌ 绝对  盘符开头的本机绝对路径（既悬空又泄漏本机路径）
  ❌ 悬空  以 `references/` `assets/` `scripts/` 开头但文件不存在
  ❌ 悬空  **父目录引用**（`../…`）—— 自包含发布物内不可能解析

补充：「`scripts/xxx.ts|tsx|mjs|js`」视为 OK-外（上游/社区仓库的脚本；本 skill 只发布 `.py`/`.sh`）。
**收紧过一次**：此前是「凡不以 `.py`/`.sh` 结尾的 `scripts/*` 都算上游」，于是
`scripts/xxx.json` 这类**本 skill 侧的路径**被静默放行 —— 真实漏报过一次，已修。

用法：python scripts/check_refs.py <skill目录> [日志路径]
      python scripts/check_refs.py --selftest
退出码：0 = 无问题；1 = 存在问题；2 = 前置错误
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

SCAN_SUFFIXES = {".md", ".py", ".sh", ".json", ".yml", ".yaml"}
SKIP_DIRS = {"vendor", "__pycache__", ".git"}

# 以这些前缀开头的路径属于 DSH 上游仓库，不是本 skill 的文件
UPSTREAM_PREFIXES = (
    "packages/", "apps/", "docs/", "vendor/", "src/", ".agents/", "native/", "scripts/gen-",
)

TICKED = re.compile(r"`([^`\n]{2,160})`")
# 盘符绝对路径。两处收紧，都是为了排除「看着像路径、其实是模式/表格」的文本：
#   ① 负向后顾：排除 URL 里的 `s://`（来自 https:）
#   ② 正向前瞻：分隔符后必须紧跟**路径首字符**（字母/数字/_/./$/~/<）
#      —— 否则断言表里的字段分隔符 `g:\-\-dump-config` 会被误判成 G 盘路径
ABS_WIN = re.compile(r"(?<![A-Za-z0-9])[A-Za-z]:[/\\](?=[A-Za-z0-9_.$~<{])[^\s`）)、，,]*")

# 正则/通配片段守卫：含这些元字符的「盘符形状」文本是模式而非路径（如 `d:\s*([^\s#]+`）
REGEX_META = ("*", "[", "]", "(", ")", "+", "?", "|", "^")

# 文档里用于举例的盘符路径：**通用的、与任何人的机器无关**的示例，
# 不视为「本机路径泄漏」。除此之外的任何盘符路径都会被判为 ❌本机。
# （刻意不写作者自己的工作区路径——那既会泄漏，对第三方用户也是错的判据。）
DOC_EXAMPLE_PATHS = (
    "C:\\Windows",
    "C:/Windows",
    "E:\\e\\foo",
    "E:/e/foo",
)
# 占位/示例路径（含尖括号占位符或省略号）——属正常的文档写法，不算缺陷
PLACEHOLDER = re.compile(r"[<{…]|\.\.\.")

# 本 skill 自己只发布 .py / .sh；`scripts/*.ts|*.mjs|*.js` 一律是 DSH 上游或社区仓库的脚本
OWN_SCRIPT_SUFFIX = (".py", ".sh")
# scripts/ 下这些后缀属「上游 / 社区仓库的脚本」，不是本 skill 的文件。
# 注意：**只放行这几种**。早期版本写成「不以 .py/.sh 结尾的一律放行」，
# 结果 `scripts/xxx.json` 这种本 skill 侧的路径被静默当成上游 —— 真实漏报一次。
UPSTREAM_SCRIPT_SUFFIX = (".ts", ".tsx", ".mjs", ".js")


def is_pathish(s: str) -> bool:
    if " " in s.strip() or "\n" in s:
        return False
    if s.startswith(("http://", "https://", "npm:", "github:", "dsh:", "git+")):
        return False
    if "/" not in s and "\\" not in s:
        return False
    return bool(re.search(r"\.(md|py|sh|json|yml|yaml|ts|tsx|mjs|js|txt|png)$", s))


def classify(ref: str, skill: Path) -> tuple[str, str]:
    rel = ref.lstrip("./").replace("\\", "/")
    # ① 占位/模板形态优先：含 <…> {…} … 的一律视为「示例」，不是可解析的路径。
    #    这一条必须排在最前——否则「不要写成 plugin-research/notes/<素材>.md」这类
    #    **规则示例文本**会被当成真实引用而自指误报。
    if PLACEHOLDER.search(ref):
        return "示例", "含占位符，属正常文档写法"
    # 父目录引用（`../…`）：自包含发布物在用户机器上不可能解析到任何东西。
    # 必须用**原始** ref 判断 —— 下面的 rel 会 lstrip("./") 把 `../` 的信息抹掉。
    # 排在 UPSTREAM_PREFIXES 之前：否则 `../packages/x.ts` 会被 lstrip 成
    # `packages/x.ts` 而以「上游路径」的身份蒙混过去。
    raw = ref.strip().replace("\\", "/")
    if raw.startswith("..") or "/../" in raw:
        return "❌悬空", "父目录引用，自包含发布物内不存在"
    if rel.startswith(UPSTREAM_PREFIXES):
        return "OK-外", ""
    if rel.startswith("plugin-research/") or rel.startswith("notes/"):
        return "❌素材", "生成期调研素材，不在 skill 内"
    if re.match(r"^[A-J]-[a-z][a-z-]*\.md$", rel):
        return "❌素材", "生成期调研笔记名，不在 skill 内"
    if re.match(r"^[A-Za-z]:[/\\]", ref):
        return "❌本机", "本机绝对路径（悬空 + 泄漏本机路径）"
    # `scripts/*.ts|*.tsx|*.mjs|*.js` 不是本 skill 的脚本（我们只发布 .py/.sh）
    if rel.startswith("scripts/") and rel.endswith(UPSTREAM_SCRIPT_SUFFIX):
        return "OK-外", ""
    for root in ("references", "assets", "scripts"):
        if rel.startswith(root + "/"):
            return ("OK-内", "") if (skill / rel).exists() else ("❌悬空", f"{rel} 不存在")
    # 裸文件名：只在本 skill 内找同名文件
    if (skill / rel).exists():
        return "OK-内", ""
    return "忽略", ""


def run(skill: Path, log: Path) -> tuple[int, int]:
    """扫描一个 skill 目录并落盘报告。返回 (退出码, 被扫描的文件数)。"""
    skill = skill.resolve()
    if not (skill / "SKILL.md").exists():
        print(f"FATAL: {skill} 下没有 SKILL.md")
        return 2, 0

    # 排除本脚本自身：它必须写下 `notes/X.md`、盘符路径等**模式字面量**作为判据，
    # 那是规则定义而不是资源引用（否则会自指误报）。
    me = Path(__file__).resolve()
    files = [
        p
        for p in skill.rglob("*")
        if p.is_file()
        and p.suffix in SCAN_SUFFIXES
        and not any(d in p.parts for d in SKIP_DIRS)
        and p.resolve() != me
    ]

    buckets: dict[str, list[tuple[str, int, str, str]]] = {}
    for p in sorted(files):
        rel_file = p.relative_to(skill).as_posix()
        for i, line in enumerate(p.read_text(encoding="utf-8", errors="replace").splitlines(), 1):
            for ref in TICKED.findall(line):
                if not is_pathish(ref):
                    continue
                kind, why = classify(ref, skill)
                if kind == "忽略":
                    continue
                buckets.setdefault(kind, []).append((rel_file, i, ref, why))
            for ref in ABS_WIN.findall(line):
                if ref.lstrip("./").startswith(UPSTREAM_PREFIXES):
                    continue
                is_regex = any(m in ref for m in REGEX_META)
                is_example = (
                    is_regex
                    or PLACEHOLDER.search(ref)
                    or any(ref.startswith(p) for p in DOC_EXAMPLE_PATHS)
                )
                kind = "示例" if is_example else "❌本机"
                if is_example:
                    why = "正则片段或占位示例，非路径"
                else:
                    why = "本机绝对路径（悬空 + 泄漏本机路径）"
                buckets.setdefault(kind, []).append((rel_file, i, ref.rstrip("。；;,)'\""), why))

    out: list[str] = []
    out.append("=" * 78)
    out.append(f" skill 资源引用一致性校验   {skill}")
    out.append("=" * 78)
    out.append(f" 扫描文件数：{len(files)}（后缀 {', '.join(sorted(SCAN_SUFFIXES))}）")
    out.append("")

    total_bad = 0
    for kind in ("❌素材", "❌本机", "❌悬空", "示例", "OK-外", "OK-内"):
        rows = buckets.get(kind, [])
        if kind.startswith("❌"):
            total_bad += len(rows)
        out.append(f"─ {kind}  {len(rows)} 处 ─")
        if kind == "OK-内" and rows:
            out.append("  （数量多，只列前 12 条）")
            rows = rows[:12]
        for rel_file, i, ref, why in rows:
            mark = f"   ← {why}" if why and kind.startswith("❌") else ""
            out.append(f"    {rel_file}:{i}  {ref}{mark}")
        if not rows:
            out.append("    （无）")
        out.append("")

    # 缺失文件清单（去重，便于按清单处理）
    missing = sorted({ref for k in ("❌素材", "❌悬空", "❌本机") for _, _, ref, _ in buckets.get(k, [])})
    out.append("─ 缺失引用清单（去重）─")
    if missing:
        for ref in missing:
            out.append(f"    {ref}")
    else:
        out.append("    （无）")
    out.append("")
    out.append(f"结论：{'✅ 全部引用均可在 skill 内解析或指向 DSH 上游' if total_bad == 0 else f'❌ {total_bad} 处问题引用'}")

    log.write_text("\n".join(out) + "\n", encoding="utf-8")
    return (0 if total_bad == 0 else 1), len(files)


# ---------------------------------------------------------------------------
# 自检：证明这个守门器**会失败**。
# 铁律：任何校验器都必须先证明它能失败，否则它的「通过」不可信。
# 夹具写在系统临时目录（不落进 skill 目录，避免污染发布物），finally 清理。
# ---------------------------------------------------------------------------

FIXTURE_DOC = "references/doc.md"


def _fixture(root: Path, quote: str, *, extra_files: bool = True) -> Path:
    """造一个最小 skill：SKILL.md + references/doc.md，doc 里引用了 quote。"""
    skill = root / "skill"
    (skill / "references").mkdir(parents=True, exist_ok=True)
    (skill / "SKILL.md").write_bytes(b"# fixture\n")
    if extra_files:
        (skill / "references" / "good.md").write_bytes(b"# good\n")
        (skill / "scripts").mkdir(exist_ok=True)
        (skill / "scripts" / "dsh-sync.sh").write_bytes(b"#!/bin/sh\n")
    (skill / FIXTURE_DOC).write_bytes(f"引用：`{quote}`\n".encode("utf-8"))
    return skill


def selftest() -> int:
    import tempfile

    cases: list[tuple[str, str, int, bool]] = [
        # (说明, 被引用的字符串, 期望退出码, 是否附带 good 文件)
        ("A 真实存在的 references 文件", "references/good.md", 0, True),
        ("B 不存在的 references 文件", "references/missing.md", 1, True),
        ("C scripts/ 下的非脚本路径（本 skill 侧，不存在）", "scripts/state.json", 1, True),
        ("D 父目录引用", "../scripts/state.json", 1, True),
        ("E 本机绝对路径", "C:\\Users\\someone\\notes.md", 1, True),
        ("F 生成期调研素材", "plugin-research/notes/foo.md", 1, True),
        ("G DSH 上游路径（合法）", "packages/boot/app-boot/src/index.ts", 0, True),
        ("H 上游脚本（scripts/*.ts，合法）", "scripts/gen-version.ts", 0, True),
        ("I 占位/示例写法（合法）", "references/<素材>.md", 0, True),
    ]

    results: list[tuple[bool, str]] = []
    root = Path(tempfile.mkdtemp(prefix="checkrefs_selftest_"))
    try:
        for name, quote, want, extra in cases:
            skill = _fixture(root, quote, extra_files=extra)
            log = root / f"log_{len(results)}.txt"
            got, scanned = run(skill, log)
            ok = got == want
            results.append((ok, f"{name}：期望退出码 {want}，实得 {got}"
                                f"（扫描 {scanned} 文件）"))
            if scanned == 0:
                results.append((False, f"{name}：扫描文件数为 0 —— 语料护栏失败，"
                                        f"「无问题」可能是假通过"))
    finally:
        import shutil
        shutil.rmtree(root, ignore_errors=True)

    print("=" * 70)
    print(" check_refs.py 自检")
    print("=" * 70)
    failed = 0
    for ok, msg in results:
        print(("  ✅ " if ok else "  ❌ ") + msg)
        failed += 0 if ok else 1
    print("=" * 70)
    print(f" {len(results) - failed}/{len(results)} 通过")
    return 0 if failed == 0 else 1


def main() -> int:
    if len(sys.argv) > 1 and sys.argv[1] == "--selftest":
        return selftest()
    if len(sys.argv) < 2:
        print("usage: check_refs.py <skill_dir> [log]  |  check_refs.py --selftest")
        return 2
    log = Path(sys.argv[2]) if len(sys.argv) > 2 else Path.cwd() / "_refs_report.txt"
    return run(Path(sys.argv[1]), log)[0]


if __name__ == "__main__":
    raise SystemExit(main())
