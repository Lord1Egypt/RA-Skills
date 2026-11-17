"""提取模板的样式定义：字体、字号、对齐等，供格式校验与渲染时参照。"""

import argparse
import json
import sys
from pathlib import Path

from docx import Document


def extract_styles(template_path: str) -> dict:
    """提取 docx 中所有样式定义。

    输出:
        styles: [{name, type, font, size, bold, italic, color, alignment}]
        default_font: 文档默认字体
        default_size: 文档默认字号
    """
    doc = Document(template_path)
    styles_data = []

    for style in doc.styles:
        try:
            font = style.font
            style_info = {
                "name": style.name,
                "type": str(style.type).replace("ENUM_STYLE_TYPE.", "").lower(),
                "font": font.name,
                "size": font.size.pt if font.size else None,
                "bold": font.bold,
                "italic": font.italic,
                "color": font.color.rgb if font.color and font.color.rgb else None,
                "alignment": (
                    str(style.paragraph_format.alignment).replace(
                        "WD_ALIGN_PARAGRAPH.", ""
                    ).lower()
                    if style.paragraph_format and style.paragraph_format.alignment
                    else None
                ),
            }
            styles_data.append(style_info)
        except Exception:
            continue

    default_font = None
    default_size = None
    try:
        normal = doc.styles["Normal"]
        if normal.font.name:
            default_font = normal.font.name
        if normal.font.size:
            default_size = normal.font.size.pt
    except KeyError:
        pass

    return {
        "template_path": str(template_path),
        "styles": styles_data,
        "default_font": default_font,
        "default_size": default_size,
    }


def main():
    parser = argparse.ArgumentParser(description="提取 docx 模板样式定义")
    parser.add_argument("--template", required=True, help="模板文件路径")
    parser.add_argument("--output", required=True, help="输出 JSON 路径")
    args = parser.parse_args()

    if not Path(args.template).exists():
        print(json.dumps({"error": f"模板不存在: {args.template}"}, ensure_ascii=False))
        sys.exit(1)

    try:
        result = extract_styles(args.template)
        Path(args.output).write_text(
            json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8"
        )
        print(json.dumps({
            "success": True,
            "output": args.output,
            "styles_count": len(result["styles"]),
            "default_font": result["default_font"],
            "default_size": result["default_size"],
        }, ensure_ascii=False, indent=2))
    except Exception as e:
        print(json.dumps({"success": False, "error": str(e)}, ensure_ascii=False))
        sys.exit(1)


if __name__ == "__main__":
    main()
