#!/usr/bin/env python3
"""
标准生成脚本 - drawio-generator
所有生成必须通过此脚本调用，禁止直接调用 generator.py！

用法:
    python3 gen.py "图表标题" '{"title":"...","nodes":[...],"edges":[...]}' [flowchart]
"""
import sys
import json
import os
from pathlib import Path

# 路径配置
SCRIPT_DIR = Path(__file__).parent
OUTPUT_DIR = Path(os.environ.get("DRAWIO_OUTPUT_DIR", "/Users/owen/Desktop/drawio-generator"))

def main():
    if len(sys.argv) < 3:
        print("用法: python3 gen.py '图表标题' '{\"title\":\"...\",\"nodes\":[...]}' [类型]")
        sys.exit(1)

    title = sys.argv[1]
    json_str = sys.argv[2]
    chart_type = sys.argv[3] if len(sys.argv) > 3 else "flowchart"

    try:
        structured = json.loads(json_str)
    except json.JSONDecodeError as e:
        print(f"JSON 解析错误: {e}")
        sys.exit(1)

    # 添加 type
    structured["type"] = chart_type
    structured["title"] = title

    # 切换到 agent-harness 目录确保模块导入正确
    os.chdir(SCRIPT_DIR)
    sys.path.insert(0, str(SCRIPT_DIR))

    from generator import generate_drawio_xml

    xml = generate_drawio_xml(structured)

    # 确保输出目录存在
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    # 输出文件
    safe_title = title.replace("/", "_").replace("\\", "_")
    out_path = OUTPUT_DIR / f"{safe_title}.drawio"
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(xml)

    print(f"✅ 生成成功: {out_path}")
    print(f"   XML 长度: {len(xml)} bytes")

if __name__ == "__main__":
    main()
