#!/usr/bin/env python3
"""
Apple Notes Writer Markdown转换示例
"""

import sys
sys.path.insert(0, '../scripts')

from apple_notes import AppleNotesWriter, markdown_to_html

# 创建写入器
writer = AppleNotesWriter()

# Markdown内容示例
markdown_content = """
# 项目周报

## 本周进展

### 已完成
- **需求分析**：完成用户调研，收集50+反馈
- **原型设计**：输出高保真原型图
- **技术评审**：确定技术方案

### 进行中
- *前端开发*：完成60%页面开发
- *后端API*：接口联调中

## 下周计划

1. 完成前端开发（优先级：**高**）
2. 进行第一轮测试
3. 准备上线文档

## 风险与问题

- **风险1**：第三方接口不稳定，需准备降级方案
- **风险2**：人手紧张，可能需要调整排期

---

<i>更新时间：2024年3月28日</i>
"""

print("=== Markdown原文 ===")
print(markdown_content)

# 转换为HTML
print("\n=== 转换后的HTML ===")
html_content = markdown_to_html(markdown_content)
print(html_content[:500] + "...")

# 写入Apple Notes
print("\n=== 写入Apple Notes ===")
result = writer.write(
    title="项目周报-2024W13",
    content=html_content,
    folder="Notes",
    update_existing=True
)
print(result)

# 另一个Markdown示例 - 学习笔记
study_note = """
# Python学习笔记

## 装饰器

装饰器是Python的重要特性：

- **语法糖**：使用@符号
- **功能**：在不修改原函数的情况下添加功能
- **应用**：日志记录、权限检查、缓存等

## 示例代码

```python
@timer
def my_function():
    pass
```

## 要点总结

1. 装饰器本质上是一个高阶函数
2. 使用*functools.wraps*保留原函数元信息
3. 可以叠加多个装饰器

<i>学习日期：2024-03-28</i>
"""

print("\n=== 写入学习笔记 ===")
html_study = markdown_to_html(study_note)
result = writer.write(
    title="Python装饰器学习笔记",
    content=html_study,
    folder="Notes"
)
print(result)

print("\n=== 示例完成 ===")
