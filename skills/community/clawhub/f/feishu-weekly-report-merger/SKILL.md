---
name: feishu-weekly-report-merger
description: 飞书周报文档合并工具。当用户提供若干飞书文档链接（或通过多维表格权限检查后发现的有权限文档），读取每个文档内容，按固定五个章节（Part1~Part5）维度将原文顺序拼接，不修改、不总结、保留原文格式，最终生成一个新的飞书云文档。触发词：合并周报、合并文档、拼接文档、文档合并、周报拼接。
---

# Feishu Weekly Report Merger

将多份飞书周报文档按章节合并为一份新文档。

## 核心原则

**原文一字不改，合并完全由脚本执行，AI 无法干预内容。**

## 工作流程

### Step 1：读取所有源文档

对每个文档 URL，调用 `feishu_fetch_doc` 获取完整 Markdown 内容：

```
feishu_fetch_doc(doc_id="<doc_id>")
```

- doc_id 从 URL 路径段提取（docx 或 wiki token 均可）
- 需要记录每个文档的归属人姓名（从标题或 URL 中识别）

### Step 2：保存原文到临时文件

将每份文档的 `markdown` 字段原始内容写入独立临时文件：

```
/tmp/merge_doc_0.md   ← 文档1原文
/tmp/merge_doc_1.md   ← 文档2原文
/tmp/merge_doc_2.md   ← 文档3原文
...
```

**重要：写入时不做任何修改、不压缩、不总结，原文是什么就写什么。**

### Step 3：调用合并脚本

使用 `exec` 工具运行 Python 脚本：

```bash
python3 ~/workspace/agent/skills/feishu-weekly-report-merger/scripts/merge.py \
  "姓名1/姓名2/姓名3" \
  "姓名1" /tmp/merge_doc_0.md \
  "姓名2" /tmp/merge_doc_1.md \
  "姓名3" /tmp/merge_doc_2.md
```

脚本路径：`~/workspace/agent/skills/feishu-weekly-report-merger/scripts/merge.py`

### Step 4：创建新文档

调用 `feishu_create_doc`，将脚本 stdout 输出作为 markdown 传入：

```
feishu_create_doc(
  markdown="<脚本stdout输出>",
  title="[AIO]-[姓名列表]-周报合并-YYYY-MM"
)
```

标题格式：`[AIO]-[姓名1/姓名2/姓名3]-周报合并-YYYY-MM`，日期取当前月份。

## 脚本工作原理

`merge.py` 按以下规则拼接：

1. **章节识别**：用正则 `^#\s*\*?Part\s*([1-5])\s*【` 匹配 Part1~Part5 标题行
2. **按 Part 切分**：每个文档切分为 5 个 Part 原始文本块
3. **原地拼接**：每个 Part 下，按参数顺序依次放入各文档该 Part 的原文，**不做任何修改**
4. **格式完整保留**：`lark-table`、`lark-td`、`lark-tr` 等飞书标签，以及所有 Markdown 语法全部保留

## 权限与安全

- 只处理 owner 有权限读取的文档
- 合并后的文档创建到 owner 的飞书云空间
- 不在群聊中暴露文档内容

## 常见问题

| 场景 | 处理方式 |
|------|---------|
| 某文档某 Part 缺失 | 该 Part 下只展示有内容的员工，缺失 Part 直接跳过 |
| `feishu_fetch_doc` 返回 forBidden | 跳过该文档，继续处理其他文档 |
| `feishu_fetch_doc` 触发频率限制 | 等 3 秒重试一次；失败超过 2 次则跳过该文档 |
| 文档内容为空 | 跳过该文档 |
| Wiki vs Docx | 两者 token 格式相同，`feishu_fetch_doc` 均支持，直接提取路径段作为 doc_id |

## 合并顺序

严格按照用户在消息中列出的文档顺序（URL 出现顺序）依次拼接，不做字母序或部门排序。
