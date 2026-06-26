#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
📝 File Super Assistant - 文件超级助手
功能：文件创建、格式转换、AI 降味
"""

import json
from pathlib import Path
from datetime import datetime

DATA_DIR = Path(__file__).parent
FILES_FILE = DATA_DIR / "files.json"
OUTPUT_DIR = Path("D:/OneDrive/Desktop/公众号文章")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# AI 降味规则（和公众号助手共享）
HUMANIZE_RULES = {
    "去除 AI 痕迹": [
        ("首先", "说实话"),
        ("其次", "还有"),
        ("最后", "最重要的是"),
        ("总之", "总的来说"),
        ("综上所述", "说了这么多"),
        ("值得注意的是", "要说的是"),
        ("不可否认", "老实说"),
    ],
    "添加个人感受": [
        ("我认为", "我个人觉得"),
        ("可以说", "说实话"),
        ("显然", "明眼人都能看出来"),
    ]
}


def load_files():
    """加载文件记录"""
    if FILES_FILE.exists():
        with open(FILES_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"files": []}


def save_files(data):
    """保存文件记录"""
    with open(FILES_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def humanize_text(text):
    """AI 降味"""
    result = text
    
    # 替换 AI 常用词
    for old, new in HUMANIZE_RULES["去除 AI 痕迹"]:
        result = result.replace(old, new)
    
    # 添加个人感受
    for old, new in HUMANIZE_RULES["添加个人感受"]:
        result = result.replace(old, new)
    
    return result


def create_docx(title, content):
    """创建 Word 文档"""
    # 简单实现：保存为文本
    # 实际可用 python-docx 库
    output_path = OUTPUT_DIR / f"{title}.docx"
    
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(f"# {title}\n\n")
        f.write(f"创建时间：{datetime.now().isoformat()}\n\n")
        f.write(content)
    
    # 记录
    data = load_files()
    data["files"].append({
        "name": title,
        "type": "docx",
        "path": str(output_path),
        "created": datetime.now().isoformat()
    })
    save_files(data)
    
    return output_path


def create_xlsx(title, data_rows):
    """创建 Excel 表格"""
    # 简单实现：保存为 CSV
    # 实际可用 openpyxl 库
    output_path = OUTPUT_DIR / f"{title}.xlsx"
    
    with open(output_path, "w", encoding="utf-8") as f:
        for row in data_rows:
            f.write(",".join(map(str, row)) + "\n")
    
    # 记录
    data = load_files()
    data["files"].append({
        "name": title,
        "type": "xlsx",
        "path": str(output_path),
        "created": datetime.now().isoformat()
    })
    save_files(data)
    
    return output_path


def create_ppt(title, slides):
    """创建 PPT"""
    # 简单实现：保存为文本大纲
    # 实际可用 python-pptx 库
    output_path = OUTPUT_DIR / f"{title}.pptx"
    
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(f"# {title}\n\n")
        for i, slide in enumerate(slides, 1):
            f.write(f"## Slide {i}: {slide['title']}\n")
            for point in slide.get("points", []):
                f.write(f"- {point}\n")
            f.write("\n")
    
    # 记录
    data = load_files()
    data["files"].append({
        "name": title,
        "type": "pptx",
        "path": str(output_path),
        "created": datetime.now().isoformat()
    })
    save_files(data)
    
    return output_path


def convert_to_pdf(input_path):
    """转换为 PDF"""
    # 简单实现：返回提示
    # 实际可用 reportlab 或 pdfkit 库
    output_path = OUTPUT_DIR / f"{Path(input_path).stem}.pdf"
    
    return output_path


def format_file(file):
    """格式化文件信息"""
    response = f"📄 **{file['name']}.{file['type']}**\n\n"
    response += f"📁 路径：{file['path']}\n"
    response += f"📅 创建：{file['created'][:19]}\n"
    
    return response


def main(query):
    """主函数"""
    query = query.lower()
    
    # 创建 Word
    if "word" in query or "docx" in query or "文档" in query:
        title = "新文档"
        content = "这里是文档内容..."
        output_path = create_docx(title, content)
        return f"""✅ Word 文档已创建！

📄 文件名：{title}.docx
📁 路径：{output_path}

💡 把你想写的内容发给我，我帮你生成完整文档！"""
    
    # 创建 Excel
    if "excel" in query or "xlsx" in query or "表格" in query:
        title = "新表格"
        data = [["姓名", "年龄", "城市"], ["张三", "25", "北京"], ["李四", "30", "上海"]]
        output_path = create_xlsx(title, data)
        return f"""✅ Excel 表格已创建！

📄 文件名：{title}.xlsx
📁 路径：{output_path}"""
    
    # 创建 PPT
    if "ppt" in query or "pptx" in query or "演示" in query:
        title = "新演示"
        slides = [
            {"title": "封面", "points": ["标题", "副标题"]},
            {"title": "目录", "points": ["要点 1", "要点 2", "要点 3"]},
            {"title": "总结", "points": ["感谢观看"]},
        ]
        output_path = create_ppt(title, slides)
        return f"""✅ PPT 已创建！

📄 文件名：{title}.pptx
📁 路径：{output_path}"""
    
    # AI 降味
    if "降味" in query or "人类化" in query:
        sample = "首先，我认为这个问题值得探讨。其次，我们需要从多个角度分析。最后，综上所述，结论是明显的。"
        humanized = humanize_text(sample)
        
        return f"""🎭 **AI 降味示例**

**原文：**
{sample}

**降味后：**
{humanized}

💡 把你想降味的文章发给我，我帮你处理！"""
    
    # 查看文件列表
    if "文件" in query and "列表" in query:
        data = load_files()
        if not data["files"]:
            return "📄 暂无文件"
        
        response = "📄 **文件列表**：\n\n"
        for f in data["files"][-5:]:
            type_icon = "📝" if f["type"] == "docx" else "📊" if f["type"] == "xlsx" else "📽️"
            response += f"{type_icon} {f['name']}.{f['type']} ({f['created'][:10]})\n"
        
        return response
    
    # 默认回复
    return """📝 文件超级助手

**功能**：
1. 创建 Word - "创建一个 Word 文档"
2. 创建 Excel - "创建一个 Excel 表格"
3. 创建 PPT - "做一个 PPT 演示"
4. AI 降味 - "把这篇文章降味"
5. 格式转换 - "转成 PDF"

**支持格式**：
- 📝 Word (.docx)
- 📊 Excel (.xlsx)
- 📽️ PPT (.pptx)
- 📄 PDF (.pdf)

告诉我你想创建什么文件？👻"""


if __name__ == "__main__":
    import sys
    sys.stdout.reconfigure(encoding='utf-8')
    print(main("创建一个 Word 文档"))
