#!/usr/bin/env python3
"""把通用模型台账写入目标配置文件（与具体客户端无关）。

默认 dry-run 预演；加 --write 才落盘。落盘流程：备份 → 原子写入 → 回读校验。

用法:
  # 同构 JSON（顶层就是模型数组）：只给路径
  python apply_config.py --path /path/to/target.json
  python apply_config.py --path /path/to/target.json --write

  # 数组在对象里
  python apply_config.py --path /path/to/target.json --root models --write

  # 字段名不同（源字段=目标字段）
  python apply_config.py --path /path/to/target.json --root models \
      --map url=base_url,apiKey=api_key,id=model --key model --write

  # YAML（需要 pyyaml）
  python apply_config.py --path /path/to/target.yaml --format yaml --root providers --write

参数:
  --source   通用台账路径（默认 $FREE_MODEL_CONFIG 或 ~/.free-model-config/models.json）
  --path     目标配置文件（必填）
  --format   json（默认）/ yaml
  --root     数组所在的键路径，支持 a.b.c；省略表示顶层
  --map      字段映射，源=目标，逗号分隔
  --key      合并键（目标字段名），默认 id
  --fields   只写入这些目标字段，逗号分隔（可选）
  --mode     merge（默认，按 key 合并、保留未知条目）/ replace
"""

import argparse
import json
import os
import shutil
import sys
import time

if sys.platform == "win32":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8")


def load_ledger(path):
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    if isinstance(data, list):
        return data
    if isinstance(data, dict):
        for k in ("models", "providers", "items"):
            if isinstance(data.get(k), list):
                return data[k]
    raise ValueError(f"台账格式无法识别: {path}")


def read_config(path, fmt):
    if fmt == "yaml":
        try:
            import yaml
        except ImportError:
            print("错误: 需要 pyyaml：pip install pyyaml", file=sys.stderr)
            sys.exit(1)
        with open(path, "r", encoding="utf-8") as f:
            return yaml.safe_load(f)
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def write_config(path, data, fmt):
    tmp = f"{path}.tmp-{os.getpid()}"
    if fmt == "yaml":
        import yaml
        with open(tmp, "w", encoding="utf-8") as f:
            yaml.safe_dump(data, f, allow_unicode=True, sort_keys=False)
    else:
        with open(tmp, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
            f.write("\n")
    os.replace(tmp, path)


def get_container(data, root, create=False):
    """返回数组所在的容器（list 或 dict 的父级）与键名"""
    if not root:
        return None, None
    node = data
    keys = root.split(".")
    for k in keys[:-1]:
        if not isinstance(node, dict):
            raise ValueError(f"root 路径 {root} 与现有结构不匹配")
        if k not in node or not isinstance(node[k], dict):
            if not create:
                return None, None
            node[k] = {}
        node = node[k]
    return node, keys[-1]


def get_list(data, root, create=False):
    if not root:
        if isinstance(data, list):
            return data
        raise ValueError("顶层不是数组，请用 --root 指定数组键")
    parent, key = get_container(data, root, create)
    if parent is None:
        return None
    if key not in parent:
        if not create:
            return None
        parent[key] = []
    if not isinstance(parent[key], list):
        raise ValueError(f"{root} 不是数组")
    return parent[key]


def set_list(data, root, items):
    if not root:
        if not isinstance(data, list):
            raise ValueError("顶层不是数组，请用 --root 指定数组键")
        data[:] = items
        return data
    parent, key = get_container(data, root, create=True)
    parent[key] = items
    return data


def project(model, mapping, fields):
    out = {}
    for k, v in model.items():
        dst = mapping.get(k, k)
        if fields and dst not in fields:
            continue
        out[dst] = v
    return out


def main():
    ap = argparse.ArgumentParser(description="把通用模型台账写入目标配置文件（默认 dry-run）")
    default_src = os.environ.get("FREE_MODEL_CONFIG") or os.path.expanduser(
        "~/.free-model-config/models.json"
    )
    ap.add_argument("--source", default=default_src, help="通用台账路径")
    ap.add_argument("--path", required=True, help="目标配置文件路径")
    ap.add_argument("--format", choices=["json", "yaml"], default="json")
    ap.add_argument("--root", default="", help="数组所在键路径，如 models 或 a.b")
    ap.add_argument("--map", default="", help="字段映射，源=目标，逗号分隔")
    ap.add_argument("--key", default="", help="合并键（目标字段名），默认取映射后的 id")
    ap.add_argument("--fields", default="", help="只写入这些目标字段，逗号分隔")
    ap.add_argument("--mode", choices=["merge", "replace"], default="merge")
    ap.add_argument("--write", action="store_true", help="实际写入（默认只预演）")
    args = ap.parse_args()

    mapping = {}
    for pair in filter(None, (p.strip() for p in args.map.split(","))):
        if "=" not in pair:
            print(f"错误: --map 项需为 源=目标：{pair}", file=sys.stderr)
            sys.exit(1)
        src, dst = pair.split("=", 1)
        mapping[src.strip()] = dst.strip()
    fields = {f.strip() for f in args.fields.split(",") if f.strip()}
    merge_key = args.key or mapping.get("id", "id")

    if not os.path.exists(args.source):
        print(f"错误: 台账不存在: {args.source}", file=sys.stderr)
        sys.exit(1)
    ledger = load_ledger(args.source)
    incoming = [project(m, mapping, fields) for m in ledger]
    incoming = [m for m in incoming if m.get(merge_key)]

    target = {}
    exists = os.path.exists(args.path)
    if exists:
        target = read_config(args.path, args.format)

    existing = get_list(target, args.root) if exists else None
    existing = list(existing or [])

    if args.mode == "replace":
        merged = incoming
        added, updated, kept = len(incoming), 0, 0
    else:
        index = {m.get(merge_key): i for i, m in enumerate(existing) if m.get(merge_key)}
        merged = list(existing)
        added = updated = 0
        for m in incoming:
            k = m[merge_key]
            if k in index:
                # 合并字段而非整条替换，保留目标里已有的未知字段
                merged[index[k]] = {**merged[index[k]], **m}
                updated += 1
            else:
                merged.append(m)
                added += 1
        kept = len(existing) - updated

    print(f"台账: {args.source}（{len(ledger)} 条）")
    print(f"目标: {args.path}（{'已存在' if exists else '将新建'}，{len(existing)} 条）")
    print(f"模式: {args.mode} | 合并键: {merge_key}")
    print(f"预计: 新增 {added} 条，更新 {updated} 条，保留 {kept} 条，写入后共 {len(merged)} 条")

    if not args.write:
        print("预演完成；确认无误后加 --write 落盘。")
        return

    if exists:
        stamp = time.strftime("%Y%m%d-%H%M%S")
        backup = f"{args.path}.bak-{stamp}"
        shutil.copy2(args.path, backup)
        print(f"已备份: {backup}")

    new_data = set_list(target, args.root, merged) if exists else []
    if not exists:
        new_data = merged if not args.root else {}
        if args.root:
            set_list(new_data, args.root, merged)
    write_config(args.path, new_data, args.format)

    # 回读校验
    check = read_config(args.path, args.format)
    count = len(get_list(check, args.root) or [])
    if count != len(merged):
        print(f"错误: 回读条数不一致（期望 {len(merged)}，实际 {count}）", file=sys.stderr)
        sys.exit(1)
    print(f"写入完成并通过回读校验：{args.path}（{count} 条）")


if __name__ == "__main__":
    main()
