#!/usr/bin/env python3
"""从 DSH 源码提取权威 UI 插槽名清单，并与本 skill 声明的清单做差异比对。

用途：核实「40 个官方插槽名全清单」这个说法是否成立。
取证方式（两种互补）：
  A. `declare module '@deepseek-ai/dsh-client-ui-slots'` 块内 `interface SlotMap` 的键
     —— 这是**声明侧**的权威来源（未声明的 slot 注册会失败）。
  B. `ctx.slots.register({ name: '...'` 与 `ctx.slots.inject('...'` 的实参
     —— 这是**调用侧**来源，用于发现 A 漏掉的动态键。

🔴 不要用「非贪婪正则 + 到第一个 2 空格缩进的 `}`」去截 `SlotMap` 正文：一旦出现嵌套的
  `children: { … }`，正则就会**提前截断**，把嵌套对象之后的键**整段丢掉**（2026-09-23 实测：
  96 个声明侧键里漏了 6 个，`settings.models.sign-in` / `conversation.chat.assistant-actions`
  正是这么丢的）→ 已改为**花括号配平**截取，并开始扫描 `.tsx`。

  A2. `packages/extensions/cordis-client-runner/src/client/slot-catalog.ts`
     —— 上游把**客户端半侧插槽契约**编译成了随仓库提交的生成产物（由
     `pnpm run gen-client-catalog` 生成、`verify-client-catalog` 守新鲜度，served to the model
     为 `cordis_inspect what:"client"`）。它是**客户端插槽的权威来源**，比任何正则都可靠 ——
     本脚本用它反查自己的漏抽量（A2 段的 `!` 行）。

用法：
  python scripts/extract_slots.py <DSH仓库路径> <本skill目录> [日志路径]
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

# 🔴 键的字符类必须允许 `-`：`settings.models.sign-in` / `conversation.plan-review.actions` /
# `conversation.chat.assistant-actions` / `settings.models.provider-card` 四个**真实插槽**
# 就因为旧字符类不含连字符而**整类**抽不到（2026-09-23 靠 A2 交叉核对暴露）。
SLOT_KEY = r"[a-z][a-zA-Z0-9]*(?:[-.][a-zA-Z0-9]+)*"

RE_SLOTMAP_HEAD = re.compile(r"interface\s+SlotMap\s*\{")
RE_SLOTMAP_KEY = re.compile(rf"['\"]({SLOT_KEY})['\"]\s*:\s*\{{")
RE_REGISTER = re.compile(rf"slots\.register\(\s*\{{\s*name:\s*['\"]({SLOT_KEY})['\"]")
RE_INJECT = re.compile(rf"slots\.inject\(\s*['\"]({SLOT_KEY})['\"]")
RE_MD_TABLE = re.compile(rf"^\|\s*`({SLOT_KEY})`\s*\|", re.MULTILINE)

# 上游生成产物（客户端半侧权威）—— 见模块 docstring 的 A2。
CATALOG_REL = "packages/extensions/cordis-client-runner/src/client/slot-catalog.ts"
RE_CATALOG_ENTRY = re.compile(r"^    key: '([^']+)',\n    kind: '([a-z-]+)'", re.MULTILINE)


def brace_body(text: str, open_idx: int) -> str:
    """从位于 open_idx 的 `{` 之后起，按花括号配平截取正文。

    只做配平，**不识别字符串/注释里的花括号** —— 作为启发式足够；残留漏抽由 A2 的
    catalog 交叉核对兜底并显式报出，不会静默。
    """
    depth = 0
    i = open_idx
    while i < len(text):
        ch = text[i]
        if ch == "{":
            depth += 1
        elif ch == "}":
            depth -= 1
            if depth == 0:
                return text[open_idx + 1 : i]
        i += 1
    return text[open_idx + 1 :]


def read_catalog(root: Path) -> tuple[bool, dict[str, str]]:
    """读上游生成产物里的客户端插槽清单。

    返回 `(文件是否存在, key → kind)` —— **两者必须分开**：返回空 dict 既可能是「文件不在」
    也可能是「条目正则没匹配到（上游改了产物格式）」，混在一起报「未找到」会把**判据过期**
    伪装成**文件缺失**（本项目已知的静默失效模式）。
    """
    path = root / CATALOG_REL
    if not path.exists():
        return False, {}
    text = path.read_text(encoding="utf-8")
    return True, {m.group(1): m.group(2) for m in RE_CATALOG_ENTRY.finditer(text)}


def scan(root: Path):
    decl: dict[str, str] = {}
    call: dict[str, str] = {}
    files = 0
    for path in root.rglob("*"):
        if path.suffix not in (".ts", ".tsx"):
            continue
        if "/node_modules/" in path.as_posix() or "/dist/" in path.as_posix():
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue
        if "ui-slots" not in text and "slots.register" not in text and "slots.inject" not in text:
            continue
        files += 1
        rel = path.relative_to(root).as_posix()
        for m in RE_SLOTMAP_HEAD.finditer(text):
            for key in RE_SLOTMAP_KEY.findall(brace_body(text, m.end() - 1)):
                decl.setdefault(key, rel)
        for key in RE_REGISTER.findall(text):
            call.setdefault(key, rel)
        for key in RE_INJECT.findall(text):
            call.setdefault(key, rel)
    return decl, call, files


def main() -> int:
    if len(sys.argv) < 3:
        print("usage: extract_slots.py <dsh_repo> <skill_dir> [log]")
        return 2
    repo = Path(sys.argv[1]).resolve()
    skill = Path(sys.argv[2]).resolve()
    # 默认写到**当前工作目录**，不写进 skill 目录（skill 目录可能只读，且不应被运行时产物污染）
    log = Path(sys.argv[3]) if len(sys.argv) > 3 else Path.cwd() / "_slots_report.txt"

    out: list[str] = []
    decl, call, files = scan(repo)
    out.append(f"repo  = {repo}")
    out.append(f"扫描含插槽相关标识的 .ts/.tsx 文件数 = {files}")
    out.append("")

    out.append(f"--- A. 声明侧 SlotMap 键（正则抽取）= {len(decl)} 个 ---")
    for k in sorted(decl):
        out.append(f"  {k:<52} {decl[k]}")
    out.append("")

    # A2：用上游生成产物反查自己的漏抽 —— 这一段的 `!` 行就是本脚本的漏抽量。
    has_cat, catalog = read_catalog(repo)
    if catalog:
        absent = sorted(set(catalog) - set(decl))
        extra = sorted(set(decl) - set(catalog))
        out.append(f"--- A2. 上游生成产物 CLIENT_SLOT_API（客户端半侧**权威**）= {len(catalog)} 个 ---")
        out.append(f"  catalog 有、A 段未抽到的键 = {len(absent)}   ← 本脚本的漏抽量（应为 0；非 0 即判据缺陷）")
        for k in absent:
            out.append(f"    ! {k}  ({catalog[k]})")
        out.append(f"  A 段有、catalog 无的键 = {len(extra)}   ← 应在宿主侧/其他平面（不是客户端插槽）")
    elif has_cat:
        out.append("--- A2. ⚠️ catalog 文件存在，但条目正则**一条都没匹配到** ---")
        out.append("  → 判据已过期（上游改了产物格式），不是文件缺失。请更新 RE_CATALOG_ENTRY。")
    else:
        out.append("--- A2. 上游生成产物 CLIENT_SLOT_API = ⚠️ 未找到（无法交叉核对）---")
        out.append(f"  预期路径：{CATALOG_REL}")
    out.append("")

    out.append(f"--- B. 调用侧 register/inject 实参 = {len(call)} 个 ---")
    for k in sorted(call):
        out.append(f"  {k:<52} {call[k]}")
    out.append("")

    union = sorted(set(decl) | set(call))

    # 测试专用键：出现在 tests/ 目录里，或键名本身是测试脚手架（test.* / t.* / dynamic.* /
    # surface.* / resources.* 且只被测试声明）。这些不是可用的公开插槽。
    def is_test_key(key: str) -> bool:
        where = decl.get(key) or call.get(key) or ""
        if "/tests/" in where or where.endswith(".spec.ts"):
            return True
        return key.split(".")[0] in {"test", "t", "dynamic", "surface"}

    public = [k for k in union if not is_test_key(k)]
    test_only = [k for k in union if is_test_key(k)]

    out.append(f"--- 并集 = {len(union)} 个（公开可用约 {len(public)}，测试专用 {len(test_only)}）---")
    out.append(f"  测试专用键: {', '.join(test_only) if test_only else '(无)'}")
    out.append("")

    # 与本 skill 声明过的清单比对
    claimed: dict[str, str] = {}
    for p in sorted((skill / "references").glob("*.md")):
        try:
            text = p.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue
        for key in RE_MD_TABLE.findall(text):
            claimed.setdefault(key, p.name)
    for p in [skill / "SKILL.md"]:
        if p.exists():
            for key in RE_MD_TABLE.findall(p.read_text(encoding="utf-8")):
                claimed.setdefault(key, p.name)

    out.append(f"--- C. 本 skill 文档中出现的插槽名候选 = {len(claimed)} 个 ---")
    for k in sorted(claimed):
        out.append(f"  {k:<52} {claimed[k]}")
    out.append("")

    real = set(union)
    stated = set(claimed) - {"id", "name", "order", "kind", "scope", "owner", "component"}
    missing = sorted(real - stated)
    invented = sorted(stated - real)

    out.append(f"--- D. 差分 ---")
    out.append(f"  源码有、本 skill 未提及（可能是不全清单的证据）= {len(missing)}")
    for k in missing:
        out.append(f"    + {k}")
    out.append(f"  本 skill 提及、源码未见（可能是编造名）= {len(invented)}")
    for k in invented:
        out.append(f"    - {k}")
    out.append("")

    # 专门核查 studio 用到的几个名字
    out.append("--- E. studio 配方用到的插槽名是否真实存在 ---")
    for name in ["root", "status", "settings", "workspace", "main", "rightbar"]:
        verdict = "存在" if name in real else "❌ 源码中未找到"
        where = decl.get(name) or call.get(name) or "-"
        out.append(f"  {name:<12} {verdict:<18} {where}")
    out.append("")

    log.write_text("\n".join(out) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
