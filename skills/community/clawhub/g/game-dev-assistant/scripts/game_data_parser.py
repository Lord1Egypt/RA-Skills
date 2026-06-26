#!/usr/bin/env python3
"""游戏数据解析器 - JSON/YAML/Excel 配置文件读取"""
import argparse
import json
import csv
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    yaml = None


def parse_json_game_data(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data


def parse_yaml_game_data(file_path):
    if yaml is None:
        print("[ERROR] 需要 pyyaml: pip install pyyaml")
        return None
    with open(file_path, 'r', encoding='utf-8') as f:
        data = yaml.safe_load(f)
    return data


def parse_csv_game_data(file_path):
    rows = []
    with open(file_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            rows.append(dict(row))
    return rows


def flatten_dict(d, parent_key='', sep='.'):
    items = []
    for k, v in d.items():
        new_key = f"{parent_key}{sep}{k}" if parent_key else k
        if isinstance(v, dict):
            items.extend(flatten_dict(v, new_key, sep=sep).items())
        else:
            items.append((new_key, v))
    return dict(items)


def analyze_game_data(data, path=''):
    """分析游戏数据结构"""
    result = {
        'type': type(data).__name__,
        'keys': [],
        'summary': {}
    }
    if isinstance(data, dict):
        result['keys'] = list(data.keys())
        for k, v in list(data.items())[:10]:
            if isinstance(v, (str, int, float, bool)):
                result['summary'][k] = v
            elif isinstance(v, list):
                result['summary'][k] = f"list[{len(v)}]"
            elif isinstance(v, dict):
                result['summary'][k] = "dict"
    elif isinstance(data, list):
        result['length'] = len(data)
        if data:
            result['item_type'] = type(data[0]).__name__
            if isinstance(data[0], dict):
                result['fields'] = list(data[0].keys())
    return result


def extract_game_constants(data, path=''):
    """提取游戏常量配置"""
    constants = {}
    if isinstance(data, dict):
        for k, v in data.items():
            if isinstance(v, (str, int, float, bool)) and not isinstance(v, bool):
                constants[k] = v
            elif isinstance(v, dict):
                sub = extract_game_constants(v, f"{path}.{k}" if path else k)
                constants.update(sub)
    elif isinstance(data, list) and data and isinstance(data[0], dict):
        # 查找配置表
        for item in data[:5]:
            if 'ID' in item or 'id' in item or 'Name' in item:
                constants[f"表_{len(data)}"] = item
                break
    return constants


def export_to_csv(data, output_path):
    if not isinstance(data, list) or not data:
        print("[ERROR] 数据不是列表格式，无法导出 CSV")
        return
    with open(output_path, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=data[0].keys())
        writer.writeheader()
        writer.writerows(data)
    print(f"[OK] CSV 已导出: {output_path}")


def diff_two_files(path1, path2):
    """对比两个游戏数据文件差异"""
    ext1 = Path(path1).suffix.lower()
    ext2 = Path(path2).suffix.lower()
    if ext1 == '.json':
        d1 = parse_json_game_data(path1)
    elif ext1 in ['.yaml', '.yml']:
        d1 = parse_yaml_game_data(path1)
    else:
        d1 = None

    if ext2 == '.json':
        d2 = parse_json_game_data(path2)
    elif ext2 in ['.yaml', '.yml']:
        d2 = parse_yaml_game_data(path2)
    else:
        d2 = None

    if d1 is None or d2 is None:
        print("[ERROR] 不支持的文件格式")
        return

    diff = []
    all_keys = set()
    if isinstance(d1, dict) and isinstance(d2, dict):
        all_keys = set(d1.keys()) | set(d2.keys())
        for k in all_keys:
            if d1.get(k) != d2.get(k):
                diff.append({'key': k, 'old': d1.get(k), 'new': d2.get(k)})
    print(f"发现 {len(diff)} 处差异:")
    for d in diff[:20]:
        print(f"  {d['key']}: {d['old']} → {d['new']}")
    return diff


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='游戏数据解析')
    sub = parser.add_subparsers(dest='cmd')
    p = sub.add_parser('analyze', help='分析数据结构')
    p.add_argument('file')
    p.add_argument('--flatten', '-f', action='store_true', help='展开嵌套字典')
    p.add_argument('--constants', '-c', action='store_true', help='提取常量')
    p = sub.add_parser('diff', help='对比两个文件')
    p.add_argument('file1')
    p.add_argument('file2')
    p = sub.add_parser('export', help='导出为 CSV')
    p.add_argument('file')
    p.add_argument('--output', '-o', required=True)
    args = parser.parse_args()
    if args.cmd == 'analyze':
        ext = Path(args.file).suffix.lower()
        if ext == '.json':
            data = parse_json_game_data(args.file)
        elif ext in ['.yaml', '.yml']:
            data = parse_yaml_game_data(args.file)
        elif ext == '.csv':
            data = parse_csv_game_data(args.file)
        else:
            print("[ERROR] 不支持格式")
            sys.exit(1)
        result = analyze_game_data(data)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        if args.flatten:
            flat = flatten_dict(data)
            print(f"\n展开后 {len(flat)} 个字段")
        if args.constants:
            consts = extract_game_constants(data)
            print(f"\n常量配置: {json.dumps(consts, ensure_ascii=False, indent=2)}")
    elif args.cmd == 'diff':
        diff_two_files(args.file1, args.file2)
    elif args.cmd == 'export':
        ext = Path(args.file).suffix.lower()
        if ext == '.json':
            data = parse_json_game_data(args.file)
        elif ext in ['.yaml', '.yml']:
            data = parse_yaml_game_data(args.file)
        elif ext == '.csv':
            data = parse_csv_game_data(args.file)
        export_to_csv(data, args.output)
