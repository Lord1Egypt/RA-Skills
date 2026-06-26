# Merge Rules Reference

## 章节提取

```python
import re

def extract_sections(markdown_text):
    """返回 {part_num: content} 字典"""
    # 匹配 Part 标题行
    pattern = r'^#\s*\*?Part\s*(\d)\s*【'
    
    positions = []
    for m in re.finditer(pattern, markdown_text, re.MULTILINE):
        positions.append((int(m.group(1)), m.start()))
    
    positions.sort(key=lambda x: x[1])
    
    sections = {}
    for i, (num, start) in enumerate(positions):
        end = positions[i+1][1] if i+1 < len(positions) else len(markdown_text)
        sections[num] = markdown_text[start:end]
    
    return sections
```

## 合并 Markdown 构建

```python
def build_merged_doc(documents, names):
    """documents: [(name, sections_dict), ...]"""
    part_names = {
        1: "Part1：【AI优先：本周核心工作复盘总结】",
        2: "Part2：【学习心得：AI 认知迭代与能力进阶】",
        3: "Part3：【本周工作总结】",
        4: "Part4：【下周工作计划】",
        5: "Part5：【关键经营指标】",
    }
    
    lines = [f"**[AIO]-[{'/'.join(names)}]-周报合并**"]
    
    for part_num in [1, 2, 3, 4, 5]:
        lines.append(f"\n# **{part_names[part_num]}**\n\n---\n")
        
        for name, sections in documents:
            if part_num in sections:
                lines.append(f"## 【{name}】\n")
                lines.append(sections[part_num])
                lines.append("\n---\n")
    
    return "\n".join(lines)
```

## 姓名提取

```python
def extract_name_from_title(title):
    """从文档标题提取员工姓名"""
    # 例如：[AIO]-[通信行业中心]-[阿拉法特]-2026-04-06
    import re
    match = re.search(r'-\[([^\]]+)\]-\[([^\]]+)\]-', title)
    if match:
        return match.group(2)  # 阿拉法特
    return None

def extract_name_from_url(url):
    """无法从标题提取时，从 URL 路径段推断"""
    # URL 中无规律时返回 None，由 Agent 决定
    return None
```

## 空章节处理

如果某员工文档缺少某个 Part（如 Part4 无内容），该 Part 下直接跳过该员工，不输出占位符。

## 表格格式保留

`lark-table`、`lark-td`、`lark-tr` 等飞书特有标签**一字不改**，直接写入合并文档。
