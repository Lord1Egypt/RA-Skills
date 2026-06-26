---
name: chat-summary
description: 聊天话题汇总技能（支持多语言）。用于整理和总结聊天记录/对话历史，按主题聚类生成结构化摘要。使用场景：(1) 每日讨论汇总，(2) 会议记录整理，(3) 长对话要点提取，(4) 多话题聊天归档。支持语言：中文、英文、繁体中文、日文、韩文等
---

# Chat Summary

## 核心功能

将聊天记录按话题聚类，生成结构化摘要，支持输出到 Notion/Markdown/纯文本。

## 工作流程

### 1. 读取会话历史
```bash
# 使用 OpenClaw sessions 命令
openclaw sessions --json
openclaw sessions_history --session-key <key> --limit <n>
```

### 2. 话题聚类
按以下维度识别话题边界：
- 用户明确切换主题
- 时间间隔 >5 分钟
- 关键词/上下文变化

### 3. 生成摘要
每个话题包含：
- **标题**：简短描述（<20 字）
- **摘要**：核心内容（<200 字）
- **关键数据**：数字/结论/决定
- **相关链接**：URL/文件/引用

### 4. 输出格式

**Notion 页面**（推荐）：
```
标题：YYYY-MM-DD - 讨论摘要
父页面：DRAFTS
内容：话题标题 (Heading 2) + 摘要段落
```

**Markdown**：
```markdown
# YYYY-MM-DD 讨论摘要

## 话题 1: [名称]
摘要内容...

## 话题 2: [名称]
摘要内容...
```

## 话题数量控制

| 场景 | 话题上限 | 摘要长度 |
|------|----------|----------|
| 每日汇总 | 10 个 | 200 字/话题 |
| 会议记录 | 5 个 | 300 字/话题 |
| 快速回顾 | 3 个 | 100 字/话题 |

## 输出目标

### Notion
- API Key: 从 `skills.entries.notion` 读取
- 父页面 ID: 配置中指定（如 DRAFTS）
- 页面命名：`YYYY-MM-DD - [描述]`

### 本地文件
- 路径：`~/Documents/chat-summaries/`
- 格式：Markdown
- 命名：`YYYY-MM-DD-summary.md`

## 示例请求

用户说：
- "总结今天的讨论"
- "把刚才的聊天整理一下"
- "生成会议记录"
- "汇总这个话题的要点"

## 资源配置

### scripts/
- `summarize_session.py` - 会话摘要生成脚本
- `cluster_topics.py` - 话题聚类算法
- `export_notion.py` - Notion API 导出

### references/
- `notion-api.md` - Notion API 使用说明
- `clustering-rules.md` - 话题聚类规则
- `output-templates.md` - 输出模板示例

---

## 多语言支持

### 支持语言
| 语言 | 代码 | 自动检测 |
|------|------|----------|
| 简体中文 | zh-CN | ✅ |
| 繁体中文 | zh-TW | ✅ |
| 英文 | en | ✅ |
| 日文 | ja | ✅ |
| 韩文 | ko | ✅ |

### 语言检测
```python
from langdetect import detect

def detect_language(text: str) -> str:
    """检测文本语言"""
    return detect(text)  # 返回 ISO 639-1 代码
```

### 多语言摘要生成
- **输入语言检测**：自动识别消息语言
- **混合语言处理**：按消息级别检测，支持中英混合
- **输出语言**：默认跟随主要语言，可显式指定

### 用户指定输出语言
```bash
# 命令行参数
summarize_session.py <session_key> --lang zh-CN
summarize_session.py <session_key> --lang en
summarize_session.py <session_key> --lang auto  # 自动检测（默认）

# 自然语言请求
"用英文总结今天的讨论"
"Summarize today's chat in Chinese"
"日本語で要約して"
```

### 翻译集成（可选）
如需跨语言汇总（如中文聊天→英文摘要）：
- 使用 DeepL API / Google Translate / OpenAI 翻译
- 见 `references/translation.md`

---

## 注意事项

1. **隐私**：不汇总敏感/私人对话
2. **准确性**：保留原始数据/结论，不臆造
3. **简洁**：摘要控制在 200 字以内
4. **可追溯**：重要结论标注消息来源
5. **多语言**：优先保持原文语言，除非用户指定翻译
