---
name: 8917-docx-official
description: 将 Markdown 或其他已有内容转换为符合中国党政机关公文/正式文件格式的 `.docx` 文档；需要时也可输出 PDF。适用于：生成公文、报告、方案、通知、汇报、意见、纪要等正式文档，或用户要求把 Markdown/文本内容排版为公文格式 Word。触发词：公文格式、正式文件、官方格式、转成 docx、公文 Word、按公文排版。
metadata:
  {
    "openclaw": {
      "emoji": "📝",
      "requires": { "bins": ["python3", "gcc", "soffice"] },
      "install": []
    }
  }
---

# 8917-docx-official

## 定位

这是一个 **工具型 / Generator** skill。

它只负责一件事：
- **把已有内容转换为符合公文/正式格式要求的 `.docx` 文档**

它不是内容策划器，不负责采访补全，不负责审批流。

---

## 输入与输出

### 输入
- Markdown 文件
- 或已整理好的文本内容（建议先保存为 `.md`）

### 输出
- `.docx`
- 如用户明确需要，也可输出 `.pdf`

---

## 核心工作流

### Step 1：确认输出格式
如果用户已经明确说了 `.docx` / `.pdf` / 两者都要，直接继续。
如果没说清，先确认：
- 只要 `.docx`
- 只要 `.pdf`
- 两者都要

### Step 2：整理 Markdown
按以下规则准备输入内容：
- 标题不要手写编号（不要写 `## 一、xxx`）
- 用 Markdown 层级控制公文标题层级
- 正文正常书写

### Step 3：必要时读取格式规则
如果需要确认标题层级、公文排版细节或参数，读取：
- `references/official-format-rules.md`

### Step 4：执行转换脚本
调用：
- `scripts/md2docx.py`

常见用法：

```bash
python scripts/md2docx.py input.md -o output.docx
```

输出 PDF：

```bash
python scripts/md2docx.py input.md -o output.pdf --pdf
```

同时输出 docx 和 PDF：

```bash
python scripts/md2docx.py input.md -o output.docx --pdf
```

### Step 5：返回结果
返回：
- 输出文件路径
- 如转换失败，明确报错原因

---

## Markdown 层级映射

| Markdown | 公文层级 | 自动编号示例 |
|----------|---------|------------|
| `#` | 文档标题 | 居中标题 |
| `##` | 一级标题 | 一、主要任务 |
| `###` | 二级标题 | （一）重点工作 |
| `####` | 三级标题 | 1.具体事项 |
| `#####` | 四级标题 | （1）实施步骤 |
| 普通段落 | 正文 | - |

---

## 关键约束

1. 名称固定为 `8917-docx-official`，这是唯一正式入口。
2. 原 `docx-official` 的有效实现应吸收入本 skill。
3. 输出路径必须支持 `-o` 参数，不允许硬编码到其他节点目录。
4. 如果需要查看格式细节，读 references，不要把大段规范塞进 `SKILL.md`。

---

## 一句话原则

**已有内容先整理成 Markdown，再交给 `8917-docx-official` 转成正式格式 docx。**
