#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DocPilot Skill - OpenClaw
文档解析、信息抽取、文档分类技能
Base URL: https://docpilot.token-ai.com.cn (生产环境)
"""

import os
import sys
import json
import requests
from pathlib import Path

DEFAULT_BASE_URL = "https://docpilot.token-ai.com.cn"
API_PATHS = {
    "parse": "/v1/skills/parse-document",
    "extract": "/v1/skills/extract-fields",
    "classify": "/v1/skills/classify-document"
}
CONFIG_FILE = Path(__file__).parent / "config.json"

def get_config():
    config = {
        "base_url": os.environ.get("DOCPilot_BASE_URL", DEFAULT_BASE_URL),
        "api_key": os.environ.get("DOCPilot_API_KEY", "")
    }
    if CONFIG_FILE.exists():
        try:
            with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                file_config = json.load(f)
                config.update(file_config)
        except Exception as e:
            print(f"[WARN] 配置文件读取失败：{e}", file=sys.stderr)
    return config

def get_headers(api_key):
    headers = {}
    if api_key:
        headers["Authorization"] = f"Bearer {api_key}"
    return headers

def parse_document(file_path, output_format="structured", include_bbox=False,
                   page_range=None, dpi=None, layout_analysis=True,
                   table_recognition=True, seal_reco_en=False,
                   md_return_image=False, md_image_format="url",
                   normalize_pages=True):
    config = get_config()
    base_url = config["base_url"].rstrip("/")
    api_url = f"{base_url}{API_PATHS['parse']}"
    headers = get_headers(config.get("api_key", ""))

    if not Path(file_path).exists():
        return {"error": f"文件不存在：{file_path}"}

    try:
        with open(file_path, "rb") as f:
            files = {"file": (Path(file_path).name, f)}
            data = {
                "output_format": output_format,
                "include_bbox": str(include_bbox).lower(),
                "layout_analysis": str(layout_analysis).lower(),
                "table_recognition": str(table_recognition).lower(),
                "seal_reco_en": str(seal_reco_en).lower(),
                "md_return_image": str(md_return_image).lower(),
                "normalize_pages": str(normalize_pages).lower(),
            }
            if page_range:
                data["page_range"] = page_range
            if dpi:
                data["dpi"] = str(dpi)
            if md_return_image:
                data["md_image_format"] = md_image_format

            response = requests.post(api_url, headers=headers, files=files, data=data, timeout=120)

            if response.status_code == 200:
                result = response.json()
                if result.get("code") == 10000:
                    return {"success": True, "data": result.get("data", result)}
                else:
                    return {"error": f"API 错误：{result.get('message', '未知错误')}", "code": result.get("code"), "detail": result.get("detail")}
            else:
                return {"error": f"HTTP 错误：{response.status_code}", "response": response.text}
    except requests.exceptions.RequestException as e:
        return {"error": f"请求失败：{str(e)}"}
    except Exception as e:
        return {"error": f"解析失败：{str(e)}"}

def extract_fields(file_path, field_schema, prompt=None, schema_ref=None, options=None):
    config = get_config()
    base_url = config["base_url"].rstrip("/")
    api_url = f"{base_url}{API_PATHS['extract']}"
    headers = get_headers(config.get("api_key", ""))

    if not Path(file_path).exists():
        return {"error": f"文件不存在：{file_path}"}

    if not field_schema:
        return {"error": "field_schema 为必填参数"}

    try:
        with open(file_path, "rb") as f:
            files = {"file": (Path(file_path).name, f)}
            data = {
                "field_schema": json.dumps(field_schema) if isinstance(field_schema, dict) else field_schema
            }
            if prompt:
                data["prompt"] = json.dumps(prompt) if isinstance(prompt, dict) else prompt
            if schema_ref:
                data["schema_ref"] = schema_ref
            if options:
                data["options"] = json.dumps(options) if isinstance(options, dict) else options

            response = requests.post(api_url, headers=headers, files=files, data=data, timeout=120)

            if response.status_code == 200:
                result = response.json()
                if result.get("code") == 10000:
                    return {"success": True, "data": result.get("data", result)}
                else:
                    return {"error": f"API 错误：{result.get('message', '未知错误')}", "code": result.get("code"), "detail": result.get("detail")}
            else:
                return {"error": f"HTTP 错误：{response.status_code}", "response": response.text}
    except requests.exceptions.RequestException as e:
        return {"error": f"请求失败：{str(e)}"}
    except Exception as e:
        return {"error": f"抽取失败：{str(e)}"}

def classify_document(file_path, mode="classify_only", category_schema=None):
    config = get_config()
    base_url = config["base_url"].rstrip("/")
    api_url = f"{base_url}{API_PATHS['classify']}"
    headers = get_headers(config.get("api_key", ""))

    if not Path(file_path).exists():
        return {"error": f"文件不存在：{file_path}"}

    try:
        with open(file_path, "rb") as f:
            files = {"file": (Path(file_path).name, f)}
            data = {"mode": mode}
            if category_schema:
                data["category_schema"] = json.dumps(category_schema) if isinstance(category_schema, dict) else category_schema

            response = requests.post(api_url, headers=headers, files=files, data=data, timeout=120)

            if response.status_code == 200:
                result = response.json()
                if result.get("code") == 10000:
                    return {"success": True, "data": result.get("data", result)}
                else:
                    return {"error": f"API 错误：{result.get('message', '未知错误')}", "code": result.get("code"), "detail": result.get("detail")}
            else:
                return {"error": f"HTTP 错误：{response.status_code}", "response": response.text}
    except requests.exceptions.RequestException as e:
        return {"error": f"请求失败：{str(e)}"}
    except Exception as e:
        return {"error": f"分类失败：{str(e)}"}

def main():
    if len(sys.argv) < 2:
        print("用法：DocPilot <command> [args]")
        print("命令:")
        print("  parse <文件路径> [选项]       - 解析文档")
        print("  extract <文件路径> --schema <JSON> - 信息抽取")
        print("  classify <文件路径> [选项]    - 文档分类")
        print("\n选项:")
        print("  [parse] --output     输出格式 (structured/markdown/text)")
        print("  [parse] --layout     启用版面分析")
        print("  [parse] --table      启用表格识别")
        print("  [parse] --seal       启用印章识别")
        print("  [parse] --dpi        DPI (72/144/200/216)")
        print("  [parse] --pages      页码范围")
        print("  [parse] --bbox       包含边界框坐标")
        print("  [parse] --normalize  返回格式化解析数据 (默认开启)")
        print("  [parse] --include-image  markdown 中包含图片")
        print("  [parse] --image-format   图片格式 (url/base64)")
        print("  [extract] --schema   字段 schema (JSON)")
        print("  [classify] --mode    模式 (classify_only/classify_and_split)")
        print("  [classify] --categories 分类 schema (JSON)")
        sys.exit(1)

    command = sys.argv[1]

    if command == "parse":
        if len(sys.argv) < 3:
            print("[ERROR] 请提供文件路径")
            sys.exit(1)

        file_path = sys.argv[2]
        output = "structured"
        layout = True
        table = True
        seal = False
        dpi = None
        pages = None
        include_bbox = False
        md_return_image = False
        md_image_format = "url"
        normalize_pages = True

        i = 3
        while i < len(sys.argv):
            arg = sys.argv[i]
            if arg == "--output" and i + 1 < len(sys.argv):
                output = sys.argv[i + 1]
                i += 2
            elif arg == "--layout":
                layout = True
                i += 1
            elif arg == "--table":
                table = True
                i += 1
            elif arg == "--seal":
                seal = True
                i += 1
            elif arg == "--dpi" and i + 1 < len(sys.argv):
                dpi = int(sys.argv[i + 1])
                i += 2
            elif arg == "--pages" and i + 1 < len(sys.argv):
                pages = sys.argv[i + 1]
                i += 2
            elif arg == "--bbox":
                include_bbox = True
                i += 1
            elif arg == "--include-image":
                md_return_image = True
                i += 1
            elif arg == "--image-format" and i + 1 < len(sys.argv):
                md_image_format = sys.argv[i + 1]
                i += 2
            elif arg == "--raw":
                normalize_pages = False
                i += 1
            else:
                i += 1

        print(f"[DOC] 解析文档：{file_path}")
        result = parse_document(file_path, output_format=output, include_bbox=include_bbox,
                                page_range=pages, dpi=dpi, layout_analysis=layout,
                                table_recognition=table, seal_reco_en=seal,
                                md_return_image=md_return_image, md_image_format=md_image_format,
                                normalize_pages=normalize_pages)

        if result.get("success"):
            print("[OK] 解析成功!")
            output_file = Path(file_path).stem + "_parsed.json"
            with open(output_file, "w", encoding="utf-8") as f:
                json.dump(result["data"], f, ensure_ascii=False, indent=2)
            print(f"[INFO] 结果已保存到：{output_file}")
            data = result["data"]
            if "page_count" in data:
                print(f"[INFO] 页数：{data.get('page_count')}")
            if "sheet_count" in data:
                print(f"[INFO] 工作表数：{data.get('sheet_count')}")
            print(f"[INFO] 文件类型：{data.get('file_type')}")
        else:
            print(f"[ERROR] {result.get('error', '未知错误')}")
            sys.exit(1)

    elif command == "extract":
        if len(sys.argv) < 3:
            print("[ERROR] 请提供文件路径")
            sys.exit(1)

        file_path = sys.argv[2]
        schema = None
        prompt = None
        schema_ref = None
        options = None

        i = 3
        while i < len(sys.argv):
            arg = sys.argv[i]
            if arg == "--schema" and i + 1 < len(sys.argv):
                try:
                    schema = json.loads(sys.argv[i + 1])
                except json.JSONDecodeError:
                    if Path(sys.argv[i + 1]).exists():
                        with open(sys.argv[i + 1], "r", encoding="utf-8") as f:
                            schema = json.load(f)
                    else:
                        print(f"[ERROR] 无效的 JSON: {sys.argv[i + 1]}")
                        sys.exit(1)
                i += 2
            elif arg == "--prompt" and i + 1 < len(sys.argv):
                try:
                    prompt = json.loads(sys.argv[i + 1])
                except json.JSONDecodeError:
                    prompt = sys.argv[i + 1]
                i += 2
            elif arg == "--schema-ref" and i + 1 < len(sys.argv):
                schema_ref = sys.argv[i + 1]
                i += 2
            elif arg == "--options" and i + 1 < len(sys.argv):
                try:
                    options = json.loads(sys.argv[i + 1])
                except json.JSONDecodeError:
                    options = sys.argv[i + 1]
                i += 2
            else:
                i += 1

        if not schema:
            print("[ERROR] 请提供 --schema 参数")
            sys.exit(1)

        print(f"[EXTRACT] 抽取信息：{file_path}")
        result = extract_fields(file_path, schema, prompt=prompt, schema_ref=schema_ref, options=options)

        if result.get("success"):
            print("[OK] 抽取成功!")
            output_file = Path(file_path).stem + "_extracted.json"
            with open(output_file, "w", encoding="utf-8") as f:
                json.dump(result["data"], f, ensure_ascii=False, indent=2)
            print(f"[INFO] 结果已保存到：{output_file}")
            data = result["data"]
            fields = data.get("fields", [])
            unfound = data.get("unfound_fields", [])
            print(f"[INFO] 找到字段：{len(fields)}")
            if unfound:
                print(f"[WARN] 未找到字段：{len(unfound)}")
            for field in fields:
                print(f"  - {field.get('key')}: {field.get('value')}")
        else:
            print(f"[ERROR] {result.get('error', '未知错误')}")
            sys.exit(1)

    elif command == "classify":
        if len(sys.argv) < 3:
            print("[ERROR] 请提供文件路径")
            sys.exit(1)

        file_path = sys.argv[2]
        mode = "classify_only"
        categories = None

        i = 3
        while i < len(sys.argv):
            arg = sys.argv[i]
            if arg == "--mode" and i + 1 < len(sys.argv):
                mode = sys.argv[i + 1]
                i += 2
            elif arg == "--categories" and i + 1 < len(sys.argv):
                try:
                    categories = json.loads(sys.argv[i + 1])
                except json.JSONDecodeError:
                    if Path(sys.argv[i + 1]).exists():
                        with open(sys.argv[i + 1], "r", encoding="utf-8") as f:
                            categories = json.load(f)
                    else:
                        print(f"[ERROR] 无效的 JSON: {sys.argv[i + 1]}")
                        sys.exit(1)
                i += 2
            else:
                i += 1

        category_schema = None
        if categories:
            category_schema = {"categories": categories} if isinstance(categories, list) else categories

        print(f"[CLASSIFY] 分类文档：{file_path}")
        result = classify_document(file_path, mode=mode, category_schema=category_schema)

        if result.get("success"):
            print("[OK] 分类成功!")
            output_file = Path(file_path).stem + "_classified.json"
            with open(output_file, "w", encoding="utf-8") as f:
                json.dump(result["data"], f, ensure_ascii=False, indent=2)
            print(f"[INFO] 结果已保存到：{output_file}")
            data = result["data"]
            if data.get("mode") == "classify_only":
                cls = data.get("classification", {})
                print(f"[INFO] 类型：{cls.get('category')}")
                print(f"[INFO] 置信度：{cls.get('confidence')}")
                print(f"[INFO] 理由：{cls.get('reasoning', '')[:100]}...")
            else:
                segments = data.get("segments", [])
                print(f"[INFO] 片段数：{len(segments)}")
                for seg in segments:
                    print(f"  - [{seg.get('category')}] {seg.get('title', '')} (页码: {seg.get('page_range')})")
        else:
            print(f"[ERROR] {result.get('error', '未知错误')}")
            sys.exit(1)

    else:
        print(f"[ERROR] 未知命令：{command}")
        sys.exit(1)

if __name__ == "__main__":
    main()
