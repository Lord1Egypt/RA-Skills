#!/usr/bin/env python3
"""DataCleaner — 数据清洗与格式化"""

import argparse
import csv
import io
import json
import re
import sys


def clean_text(data: list, rules: dict = None) -> dict:
    """文本数据清洗"""
    if rules is None:
        rules = {}
    strip = rules.get("strip", True)
    remove_html = rules.get("remove_html", True)
    remove_emoji = rules.get("remove_emoji", False)
    remove_duplicates = rules.get("remove_duplicates", True)
    remove_empty = rules.get("remove_empty", True)
    lowercase = rules.get("lowercase", False)
    normalize_whitespace = rules.get("normalize_whitespace", True)

    if not isinstance(data, list):
        return {"error": "输入数据必须是列表格式"}

    original_count = len(data)
    cleaned = []

    for item in data:
        if isinstance(item, str):
            text = item
        elif isinstance(item, dict):
            # 对dict的值进行清洗
            cleaned_item = {}
            for k, v in item.items():
                if isinstance(v, str):
                    cleaned_item[k] = _apply_text_rules(v, strip, remove_html, remove_emoji,
                                                         lowercase, normalize_whitespace)
                else:
                    cleaned_item[k] = v
            cleaned.append(cleaned_item)
            continue
        else:
            text = str(item)

        text = _apply_text_rules(text, strip, remove_html, remove_emoji,
                                 lowercase, normalize_whitespace)
        if remove_empty and not text:
            continue
        cleaned.append(text)

    if remove_duplicates:
        if cleaned and isinstance(cleaned[0], dict):
            seen = set()
            unique = []
            for item in cleaned:
                key = json.dumps(item, sort_keys=True, ensure_ascii=False)
                if key not in seen:
                    seen.add(key)
                    unique.append(item)
            cleaned = unique
        else:
            cleaned = list(dict.fromkeys(cleaned))

    stats = {
        "original_count": original_count,
        "cleaned_count": len(cleaned),
        "removed_count": original_count - len(cleaned),
        "rules_applied": {
            "strip": strip,
            "remove_html": remove_html,
            "remove_emoji": remove_emoji,
            "remove_duplicates": remove_duplicates,
            "remove_empty": remove_empty,
            "lowercase": lowercase,
            "normalize_whitespace": normalize_whitespace,
        },
    }

    return {"stats": stats, "data": cleaned}


def _apply_text_rules(text: str, strip: bool, remove_html: bool, remove_emoji: bool,
                      lowercase: bool, normalize_ws: bool) -> str:
    """应用文本清洗规则"""
    if strip:
        text = text.strip()
    if remove_html:
        text = re.sub(r'<[^>]+>', '', text)
        text = re.sub(r'&[a-zA-Z]+;', ' ', text)
        text = re.sub(r'&#\d+;', ' ', text)
    if remove_emoji:
        text = re.sub(r'[\U0001F600-\U0001F64F\U0001F300-\U0001F5FF\U0001F680-\U0001F6FF\U0001F1E0-\U0001F1FF\U00002702-\U000027B0\U000024C2-\U0001F251]+', '', text)
    if normalize_ws:
        text = re.sub(r'\s+', ' ', text).strip()
    if lowercase:
        text = text.lower()
    return text


def normalize_types(data: list, schema: dict = None) -> dict:
    """数据类型标准化"""
    if not isinstance(data, list):
        return {"error": "输入数据必须是列表格式"}

    if not schema:
        # 自动推断类型
        schema = _infer_schema(data[:20])

    normalized = []
    type_issues = []
    for i, item in enumerate(data):
        if not isinstance(item, dict):
            normalized.append(item)
            continue
        norm_item = {}
        for key, expected_type in schema.items():
            if key not in item:
                norm_item[key] = None
                continue
            val = item[key]
            try:
                if expected_type == "number":
                    val = float(re.sub(r'[^\d.-]', '', str(val))) if val else 0.0
                elif expected_type == "integer":
                    val = int(float(re.sub(r'[^\d.-]', '', str(val)))) if val else 0
                elif expected_type == "string":
                    val = str(val).strip() if val else ""
                elif expected_type == "boolean":
                    if isinstance(val, str):
                        val = val.lower() in ("true", "1", "yes", "是")
                    else:
                        val = bool(val)
                norm_item[key] = val
            except (ValueError, TypeError) as e:
                type_issues.append({"row": i, "field": key, "value": str(val)[:50], "error": str(e)})
                norm_item[key] = None
        normalized.append(norm_item)

    return {
        "schema": schema,
        "normalized_count": len(normalized),
        "type_issues_count": len(type_issues),
        "type_issues_sample": type_issues[:10],
        "data": normalized,
    }


def _infer_schema(sample: list) -> dict:
    """从样本推断数据类型"""
    if not sample or not isinstance(sample[0], dict):
        return {}
    schema = {}
    for key in sample[0].keys():
        values = [item.get(key) for item in sample if key in item and item[key] is not None]
        if not values:
            schema[key] = "string"
            continue
        int_count = sum(1 for v in values if isinstance(v, int) or (isinstance(v, str) and re.match(r'^-?\d+$', v.strip())))
        float_count = sum(1 for v in values if isinstance(v, float) or (isinstance(v, str) and re.match(r'^-?\d+\.\d+$', v.strip())))
        bool_count = sum(1 for v in values if isinstance(v, bool) or (isinstance(v, str) and v.lower() in ("true", "false", "yes", "no")))
        total = len(values)
        if int_count / total > 0.8:
            schema[key] = "integer"
        elif (int_count + float_count) / total > 0.8:
            schema[key] = "number"
        elif bool_count / total > 0.8:
            schema[key] = "boolean"
        else:
            schema[key] = "string"
    return schema


def format_output(data: list, output_format: str = "json", fields: list = None) -> dict:
    """格式化输出"""
    if fields and data and isinstance(data[0], dict):
        data = [{k: item.get(k) for k in fields if k in item} for item in data]

    if output_format == "json":
        formatted = json.dumps(data, ensure_ascii=False, indent=2)
    elif output_format == "csv":
        if not data or not isinstance(data[0], dict):
            return {"error": "CSV输出需要字典列表输入"}
        output = io.StringIO()
        writer = csv.DictWriter(output, fieldnames=data[0].keys())
        writer.writeheader()
        writer.writerows(data)
        formatted = output.getvalue()
    elif output_format == "jsonl":
        lines = [json.dumps(item, ensure_ascii=False) for item in data]
        formatted = "\n".join(lines)
    else:
        return {"error": f"不支持的格式: {output_format}"}

    return {
        "format": output_format,
        "record_count": len(data),
        "output_size_chars": len(formatted),
        "output": formatted,
    }


def main():
    parser = argparse.ArgumentParser(description="DataCleaner - 数据清洗与格式化")
    sub = parser.add_subparsers(dest="command")

    p_clean = sub.add_parser("clean", help="文本数据清洗")
    p_clean.add_argument("--input", type=str, required=True, help="输入JSON数据或文件路径")
    p_clean.add_argument("--strip", type=bool, default=True)
    p_clean.add_argument("--remove-html", type=bool, default=True)
    p_clean.add_argument("--remove-emoji", type=bool, default=False)
    p_clean.add_argument("--remove-duplicates", type=bool, default=True)
    p_clean.add_argument("--remove-empty", type=bool, default=True)
    p_clean.add_argument("--lowercase", type=bool, default=False)

    p_norm = sub.add_parser("normalize", help="数据类型标准化")
    p_norm.add_argument("--input", type=str, required=True, help="输入JSON数据或文件路径")
    p_norm.add_argument("--schema", type=str, default="", help="类型schema (JSON格式)")

    p_fmt = sub.add_parser("format", help="格式化输出")
    p_fmt.add_argument("--input", type=str, required=True, help="输入JSON数据或文件路径")
    p_fmt.add_argument("--format", type=str, default="json", choices=["json", "csv", "jsonl"])
    p_fmt.add_argument("--fields", type=str, nargs="*", help="输出字段列表")

    args = parser.parse_args()
    if not args.command:
        parser.print_help()
        sys.exit(1)

    # 读取输入
    input_data = args.input
    for cmd_name in ["clean", "normalize", "format"]:
        if args.command == cmd_name:
            raw = getattr(args, "input", "")
            if raw.endswith(".json"):
                try:
                    with open(raw, "r", encoding="utf-8") as f:
                        input_data = json.load(f)
                except Exception:
                    input_data = json.loads(raw)
            else:
                input_data = json.loads(raw)
            break

    result = {}
    if args.command == "clean":
        result = clean_text(input_data, {
            "strip": args.strip, "remove_html": args.remove_html,
            "remove_emoji": args.remove_emoji, "remove_duplicates": args.remove_duplicates,
            "remove_empty": args.remove_empty, "lowercase": args.lowercase,
        })
    elif args.command == "normalize":
        schema = json.loads(args.schema) if args.schema else None
        result = normalize_types(input_data, schema)
    elif args.command == "format":
        result = format_output(input_data, args.format, args.fields)

    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
