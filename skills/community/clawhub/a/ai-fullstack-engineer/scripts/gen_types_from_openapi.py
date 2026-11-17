#!/usr/bin/env python3
"""gen_types_from_openapi.py — 从 OpenAPI 规范生成 TS 接口，保证前后端类型安全。

用法:
    python3 scripts/gen_types_from_openapi.py --spec openapi.json --out src/api/types.ts

支持: components.schemas 中的 object/string/integer/number/boolean/array/$ref，
      以及嵌套 object 与数组元素 $ref。生成 camelCase 属性名用原名保留。
仅用标准库。
"""
import argparse
import json
from pathlib import Path

TYPE_MAP = {
    "string": "string",
    "integer": "number",
    "number": "number",
    "boolean": "boolean",
    "null": "null",
}


def ref_name(ref: str) -> str:
    return ref.split("/")[-1]


def ts_type(schema: dict, visited: set) -> str:
    if "$ref" in schema:
        return ref_name(schema["$ref"])
    t = schema.get("type")
    if t == "array":
        items = schema.get("items", {})
        return f"{ts_type(items, visited)}[]"
    if t == "object" or "properties" in schema:
        props = schema.get("properties", {})
        if not props:
            return "Record<string, unknown>"
        lines = []
        required = set(schema.get("required", []))
        for name, ps in props.items():
            opt = "" if name in required else "?"
            lines.append(f"  {name}{opt}: {ts_type(ps, visited)};")
        return "{\n" + "\n".join(lines) + "\n}"
    if t in TYPE_MAP:
        return TYPE_MAP[t]
    if t == "file":
        return "File"
    return "unknown"


def main():
    ap = argparse.ArgumentParser(description="从 OpenAPI 生成 TS 类型")
    ap.add_argument("--spec", required=True, help="OpenAPI JSON 路径")
    ap.add_argument("--out", required=True, help="输出 .ts 路径")
    args = ap.parse_args()

    spec = json.loads(Path(args.spec).read_text(encoding="utf-8"))
    schemas = (spec.get("components", {}) or {}).get("schemas", {}) or {}
    if not schemas:
        raise SystemExit("未在 components.schemas 找到任何定义")

    blocks = ["// 由 gen_types_from_openapi.py 自动生成，请勿手改。\n"]
    for name, schema in schemas.items():
        blocks.append(f"export interface {name} {ts_type(schema, set())}\n")

    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text("\n".join(blocks) + "\n", encoding="utf-8")
    print(f"✓ 已生成 {len(schemas)} 个接口 -> {out}")


if __name__ == "__main__":
    main()
