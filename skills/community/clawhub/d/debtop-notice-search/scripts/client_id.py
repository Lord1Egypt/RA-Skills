#!/usr/bin/env python3
"""客户端标识（skill_id / 链接 source）生成规则 v1 —— 唯一实现。

规则全文见 references/client-source-ids.md「生成规则」。三级优先：

1. **表优先**：客户端产品名命中 `references/client-source-ids.md` → 用表内约定值。
   中文产品名必须走这条（算法只产出 ASCII，中文会被归一化成空 → `mcp`）。
2. **表外按算法生成**：NFKC → strip → lower → 非 ``[a-z0-9]`` 连续段折成单个 ``-``
   → 合并/去首尾 ``-`` → 截断 32 字符并去尾部 ``-`` → 空则 ``mcp``。
3. **拿不到产品名** → ``mcp``。

用法::

    python3 client_id.py --name "千问办公"      # → qwen-office   (表命中)
    python3 client_id.py --name "Foo Bar"       # → foo-bar       (算法)
    python3 client_id.py --name "未知中文客户端"  # → mcp           (兜底)
    python3 client_id.py --name "Foo Bar" --json
    python3 client_id.py --check            # 自检向量（含表命中项），全通过退出 0

设计约束（why）：
- **纯函数**：同一输入永远同一输出，不带时间/随机/外部噪声 —— 否则归属会分裂；
- **不用哈希**：标识要人能读、能在报表里对账；表外客户端靠"是否登记"治理，不靠哈希；
- **长度 32**：服务端正则上限 64，脚本留余量（防止后续拼后缀时越界）。
"""
from __future__ import annotations

import argparse
import json
import pathlib
import re
import sys
import unicodedata

MAX_LEN = 32
FALLBACK = "mcp"
DEFAULT_TABLE = pathlib.Path(__file__).resolve().parent.parent / "references" / "client-source-ids.md"

# 表行: | 客户端 / 平台 | `标识` |（表头与分隔行由内容校验排除）
_ROW = re.compile(r"^\|\s*(?P<name>[^|]+?)\s*\|\s*`(?P<id>[a-z0-9._-]+)`\s*\|\s*$")
_SKIP_NAMES = {"客户端 / 平台", "---"}


def _norm_key(name: str) -> str:
    """查表用的宽松键：NFKC + 去首尾空白 + 小写（保留中文，便于中文名命中）。"""
    return unicodedata.normalize("NFKC", name or "").strip().lower()


def _aliases(name: str) -> list[str]:
    """一个表名可被哪些写法命中：原名、去括号、去所有非字母数字。"""
    base = _norm_key(name)
    if not base:
        return []
    keys = [base]
    no_paren = re.sub(r"[（(].*?[)）]", "", base).strip()
    if no_paren and no_paren != base:
        keys.append(no_paren)
    compact = re.sub(r"[^0-9a-z\u4e00-\u9fff]+", "", base)
    if compact and compact not in keys:
        keys.append(compact)
    return keys


def load_table(path: pathlib.Path | str | None) -> dict[str, str]:
    """解析标识表 → {键: 标识}；文件不存在返回空表（算法兜底仍可用）。"""
    table: dict[str, str] = {}
    if not path:
        return table
    p = pathlib.Path(path)
    if not p.is_file():
        return table
    for line in p.read_text(encoding="utf-8").splitlines():
        m = _ROW.match(line.strip())
        if not m:
            continue
        name, cid = m.group("name").strip(), m.group("id").strip()
        if name in _SKIP_NAMES:
            continue
        for key in _aliases(name):
            table.setdefault(key, cid)
        # 标识自身也认（客户端直接报 workbuddy 也能命中同一值）
        table.setdefault(_norm_key(cid), cid)
    return table


def derive(name: str) -> str:
    """表外算法：纯归一化，不含表查询。空/纯非 ASCII → mcp。"""
    text = unicodedata.normalize("NFKC", name or "").strip().lower()
    out: list[str] = []
    prev_dash = False
    for ch in text:
        if ch.isascii() and ch.isalnum():
            out.append(ch)
            prev_dash = False
        elif not prev_dash:
            out.append("-")
            prev_dash = True
    slug = "".join(out).strip("-")[:MAX_LEN].strip("-")
    return slug or FALLBACK


def resolve(name: str | None, table: dict[str, str] | None = None) -> tuple[str, str]:
    """返回 ``(标识, 来源)``；来源取值 ``table`` / ``derived`` / ``fallback``。"""
    raw = (name or "").strip()
    if table:
        for key in _aliases(raw):
            hit = table.get(key)
            if hit:
                return hit, "table"
    if not raw:
        return FALLBACK, "fallback"
    slug = derive(raw)
    return (slug, "derived") if slug != FALLBACK else (FALLBACK, "fallback")


# 自检向量：第一条不依赖表（算法），后两条依赖表（中文名无法由算法产出）
VECTORS_ALGO = [
    ("WorkBuddy", "workbuddy"),
    ("  Cursor  ", "cursor"),
    ("Foo Bar", "foo-bar"),
    ("qwen_office", "qwen-office"),
    ("Qoder.app", "qoder-app"),
    ("123Client", "123client"),
    ("Very Long Name With Many Words And More", "very-long-name-with-many-words-a"),
    ("---", "mcp"),
    ("", "mcp"),
    ("未知中文客户端", "mcp"),
]
VECTORS_TABLE = [
    ("千问办公", "qwen-office"),
    ("Kimi（月之暗面）", "kimi"),
    ("GitHub Copilot", "github-copilot"),
]


def run_checks(table_path: pathlib.Path | str | None) -> int:
    table = load_table(table_path)
    failures: list[str] = []
    for name, expected in VECTORS_ALGO:
        got = derive(name)
        if got != expected:
            failures.append(f"算法 {name!r}: 期望 {expected!r} 得到 {got!r}")
    print(f"[OK] 算法向量 {len(VECTORS_ALGO)} 项")
    if not table:
        print(f"[!!] 标识表不可用（{table_path}）→ 跳过表向量", file=sys.stderr)
        return 1
    for name, expected in VECTORS_TABLE:
        got, source = resolve(name, table)
        if got != expected or source != "table":
            failures.append(f"表 {name!r}: 期望 {expected!r}(table) 得到 {got!r}({source})")
    print(f"[OK] 表向量 {len(VECTORS_TABLE)} 项（表内 {len(table)} 个键）")
    for line in failures:
        print(f"[!!] {line}", file=sys.stderr)
    print("RESULT: " + ("PASS" if not failures else "FAIL"))
    return 1 if failures else 0


def main() -> int:
    parser = argparse.ArgumentParser(description="客户端标识(skill_id)生成规则 v1")
    parser.add_argument("--name", default="", help="客户端产品名（如 WorkBuddy / 千问办公）")
    # 位置参数等价于 --name（方便直接 `client_id.py "Foo Bar"`）;
    # 以 `-` 开头的值（如 `---`）用 `--name=---` 或 `-- ---` 传入 —— argparse 会把它当选项
    parser.add_argument("positional_name", nargs="?", default="", help=argparse.SUPPRESS)
    parser.add_argument("--table", default=str(DEFAULT_TABLE), help="标识表路径（默认包内 references/）")
    parser.add_argument("--json", action="store_true", help="输出 JSON（含来源）")
    parser.add_argument("--check", action="store_true", help="运行自检向量")
    args = parser.parse_args()

    if args.check:
        return run_checks(args.table)

    table = load_table(args.table)
    raw_name = args.name or args.positional_name
    cid, source = resolve(raw_name, table)
    if args.json:
        print(json.dumps({"name": raw_name, "id": cid, "source": source}, ensure_ascii=False))
    else:
        print(cid)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
