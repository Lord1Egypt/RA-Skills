#!/usr/bin/env python3
"""confmt — Config file formatter and converter (JSON/TOML). Zero dependencies."""
import json, sys, argparse, os
try:
    import tomllib  # Python 3.11+
    HAS_TOML = True
except ImportError:
    HAS_TOML = False

def flatten_dict(d, prefix="", sep="."):
    items = {}
    for k, v in d.items():
        key = f"{prefix}{sep}{k}" if prefix else k
        if isinstance(v, dict):
            items.update(flatten_dict(v, key, sep))
        elif isinstance(v, list):
            for i, item in enumerate(v):
                if isinstance(item, dict):
                    items.update(flatten_dict(item, f"{key}[{i}]", sep))
                else:
                    items[f"{key}[{i}]"] = item
        else:
            items[key] = v
    return items

def detect_format(path):
    ext = os.path.splitext(path)[1].lower()
    return {".json": "json", ".toml": "toml", ".env": "env", ".ini": "ini"}.get(ext, "json")

def parse_env(text):
    d = {}
    for line in text.strip().split("\n"):
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if "=" in line:
            k, v = line.split("=", 1)
            v = v.strip().strip('"').strip("'")
            d[k.strip()] = v
    return d

def to_env(d):
    flat = flatten_dict(d)
    lines = []
    for k, v in sorted(flat.items()):
        key = k.upper().replace(".", "_").replace("[", "_").replace("]", "")
        lines.append(f'{key}="{v}"')
    return "\n".join(lines)

def cmd_format(args):
    if args.file:
        text = open(args.file).read()
        fmt = args.input_format or detect_format(args.file)
    else:
        text = sys.stdin.read()
        fmt = args.input_format or "json"

    # Parse
    if fmt == "json":
        data = json.loads(text)
    elif fmt == "toml" and HAS_TOML:
        data = tomllib.loads(text)
    elif fmt == "env":
        data = parse_env(text)
    else:
        data = json.loads(text)

    # Output
    out_fmt = args.output_format or fmt
    if out_fmt == "json":
        indent = None if args.compact else (args.indent or 2)
        print(json.dumps(data, indent=indent, sort_keys=args.sort, ensure_ascii=False))
    elif out_fmt == "flat":
        flat = flatten_dict(data)
        for k, v in flat.items():
            print(f"{k} = {json.dumps(v)}")
    elif out_fmt == "env":
        print(to_env(data))
    else:
        print(json.dumps(data, indent=2, sort_keys=args.sort))

def cmd_diff(args):
    def load(path):
        text = open(path).read()
        fmt = detect_format(path)
        if fmt == "json":
            return json.loads(text)
        elif fmt == "toml" and HAS_TOML:
            return tomllib.loads(text)
        elif fmt == "env":
            return parse_env(text)
        return json.loads(text)

    d1 = flatten_dict(load(args.file1))
    d2 = flatten_dict(load(args.file2))
    
    all_keys = sorted(set(d1) | set(d2))
    added = removed = changed = 0
    for k in all_keys:
        if k not in d1:
            print(f"  + {k} = {json.dumps(d2[k])}")
            added += 1
        elif k not in d2:
            print(f"  - {k} = {json.dumps(d1[k])}")
            removed += 1
        elif d1[k] != d2[k]:
            print(f"  ~ {k}: {json.dumps(d1[k])} → {json.dumps(d2[k])}")
            changed += 1
    
    if not (added or removed or changed):
        print("✅ Files are identical")
    else:
        print(f"\n📊 +{added} -{removed} ~{changed}")

def main():
    p = argparse.ArgumentParser(prog="confmt", description="Config file formatter and converter")
    sub = p.add_subparsers(dest="cmd")

    f = sub.add_parser("format", aliases=["fmt"], help="Format/convert config files")
    f.add_argument("file", nargs="?")
    f.add_argument("-i", "--input-format", choices=["json", "toml", "env"])
    f.add_argument("-o", "--output-format", choices=["json", "flat", "env"])
    f.add_argument("--compact", action="store_true")
    f.add_argument("--sort", action="store_true")
    f.add_argument("--indent", type=int)

    d = sub.add_parser("diff", help="Diff two config files")
    d.add_argument("file1")
    d.add_argument("file2")

    args = p.parse_args()
    if args.cmd in ("format", "fmt"):
        cmd_format(args)
    elif args.cmd == "diff":
        cmd_diff(args)
    else:
        p.print_help()

if __name__ == "__main__":
    main()
