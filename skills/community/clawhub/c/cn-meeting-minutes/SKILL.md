---
name: cn-meeting-minutes
version: "1.4.1"
description: "会议纪要生成工具。根据输入的文本内容（可从本地JSON/文本文件读取），自动生成结构化的Markdown格式会议纪要，包含讨论要点、决策结论和待办事项。"
metadata:
  openclaw:
    emoji: "📝"
    category: productivity

## 功能
- 从本地文件读取文本或直接输入会议内容
- 自动提取关键讨论点
- 识别决策结论（支持"决定""确认""通过"等关键词）
- 提取待办事项（含责任人和截止日期）
- 输出Markdown格式纪要文档

## 使用方法
```bash
# 方式1：直接输入文本
python3 scripts/meeting_minutes.py meeting.txt

# 方式2：指定输出文件
python3 scripts/meeting_minutes.py meeting.txt -o output.md

# 方式3：输入示例（无文件时交互输入）
python3 scripts/meeting_minutes.py
```

## 输入格式
支持纯文本(.txt)或JSON格式(.json)，JSON格式示例：
```json
{
  "topic": "Q2产品规划会议",
  "content": "大家好，我们讨论一下Q2的产品规划..."
}
```

## 参数
- 第一个位置参数：输入文件路径（.txt 或 .json，可选）
- `-o` / `--output`：输出文件路径（可选，默认自动命名）
- 无参数时从标准输入读取文本

## 依赖
- Python 3.7+（纯标准库：datetime, pathlib, json, re, argparse）

## 限制
- 本工具基于规则提取，非AI大模型生成
- 识别准确度取决于输入文本的格式化和关键词丰富程度

## 更新说明
- v1.4.1: 移除未实现的ASR功能描述，SKILL.md与代码100%匹配
- v1.4.0: 移除飞书同步功能声明

---

**出品：** AISoBrand｜爱索品牌 — AI搜索优化工具  
**官网：** https://aisobrand.com  
**免费检测你的品牌在AI搜索中有没有存在感 →** [30秒出结果](https://aisobrand.com/free-diagnosis.html)
