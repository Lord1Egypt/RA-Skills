# 提取 PDF 内容并整理向量数据库信息
import pdfplumber
import json
from pathlib import Path
import sys

# 设置 UTF-8 编码
sys.stdout.reconfigure(encoding='utf-8')

pdf_path = r"D:\大模型相关\2026\第四章向量数据库基础理论与实践\第四章 向量数据库基础理论与实践.pdf"
output_path = r"D:\DocsAutoWrter\chatpublice\01-向量数据库技术深度解析.md"

print("[PDF 提取] 开始提取 PDF 内容...")
print(f"PDF 路径：{pdf_path}")

# 提取文本
full_text = []
with pdfplumber.open(pdf_path) as pdf:
    print(f"PDF 页数：{len(pdf.pages)}")
    for i, page in enumerate(pdf.pages):
        text = page.extract_text()
        if text:
            full_text.append(f"--- 第 {i+1} 页 ---\n{text}")
            print(f"  第 {i+1} 页：{len(text)} 字符")

# 保存提取的内容
extracted_path = Path(pdf_path).parent / "extracted_text.txt"
with open(extracted_path, 'w', encoding='utf-8') as f:
    f.write('\n\n'.join(full_text))

print(f"\n[完成] 提取完成！内容已保存到：{extracted_path}")
print(f"总字符数：{sum(len(t) for t in full_text)}")

# 显示前 5000 字符预览
print("\n=== 内容预览 (前 5000 字符) ===")
preview = '\n\n'.join(full_text)
print(preview[:5000] if preview else "无内容")
