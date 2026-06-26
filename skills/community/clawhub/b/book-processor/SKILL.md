---
name: book-processor
description: 自动化处理 EPUB 电子书，提取全文、封面、概要和框架解读，支持案例库、每日清单、5-Why 分析、思维模型速查卡、流程图和 FAQ 等多种资产生成。
homepage: https://github.com/your-repo/book-processor
metadata:
  openclaw:
    emoji: "📚"
    category: productivity
  clawdbot:
    requires:
      bins: ["jq", "python3", "unzip"]
---

# Book Processor Skill

## 功能概览
本技能自动化处理 EPUB 电子书，将书籍转化为结构化内容与实用工具。

### 核心输出文件
| 文件 | 说明 |
|------|------|
| `cover.jpeg` | 从 EPUB 提取的封面图片 |
| `full_text.txt` | 全书纯文本（若 EPUB 以图片为主，该文件内容可能极少） |
| `summary.txt` | 书籍简要概要（若文字不足需手动补充） |
| `framework_article.txt` | 将书中核心方法映射为“认知‑对抗‑重塑‑持久”四阶段框架的解读文章 |
| `examples.md` | 精选案例库（可根据书中实际人物/案例修改） |
| `daily_combat_checklist.md` | 每日对抗清单模板（适用于需要每日练习的书籍） |
| `5why_sheet.md` | 5‑Why 根因分析工作表 |
| `thinking_models_summary.md` | 思维模型速查卡（通用列表） |
| `framework_flow.mmd` | Mermaid 流程图（可视化四阶段关系） |
| `faq.md` | 常见问题与答案 |
| `process_config.json` | 本次处理所使用的配置（若未提供则使用默认值） |

---

## 触发条件
当用户发送 `.epub` 文件时自动触发。

---

## 工作流程
1. **接收 EPUB**：从用户消息中提取 EPUB 文件
2. **创建书籍文件夹**：在 `~/workspace/books/` 下创建以书名命名的文件夹
3. **保存文件**：将 EPUB 放入对应文件夹
4. **读取配置**：如果文件夹中存在 `process_config.json`，则使用它；否则使用默认配置
5. **执行处理**：运行 `scripts/process_book.sh <book_folder>`（相对于技能目录）
6. **返回结果**：向用户报告生成的文件列表和简要概览

---

## 配置选项
在书籍文件夹中创建 `process_config.json` 来控制生成的资产：

```json
{
  "generate_examples": true,
  "generate_daily_checklist": false,
  "generate_5why": false,
  "generate_thinking_models": true,
  "generate_flowchart": true,
  "generate_faq": true
}
```

**说明**：
- `true` 表示生成对应文件
- `false` 或省略表示跳过
- 默认配置：仅生成 `cover.jpeg`、`full_text.txt`、`summary.txt`、`framework_article.txt` 四个必需文件

---

## 安装与依赖

### 必需工具
| 工具 | 用途 | 安装命令 |
|------|------|----------|
| `jq` | JSON 配置解析 | `sudo apt-get install -y jq` |
| `python3` | 文本提取 | `sudo apt-get install -y python3` |
| `unzip` | EPUB 解压 | `sudo apt-get install -y unzip` |

### 验证安装
```bash
jq --version
python3 --version
unzip -v
```

---

## 使用方法

### 方式 1：自动触发（推荐）
直接将 EPUB 文件发送给福德，技能会自动处理。

### 方式 2：手动执行
```bash
# 处理指定书籍文件夹
/home/haifeng/workspace/scripts/process_book.sh /home/haifeng/workspace/books/《书名》
```

---

## 目录结构示例
```
books/
├── 一生之敌/
│   ├── 一生之敌.epub
│   ├── cover.jpeg
│   ├── full_text.txt
│   ├── summary.txt
│   ├── framework_article.txt
│   ├── examples.md
│   ├── daily_combat_checklist.md
│   ├── 5why_sheet.md
│   ├── thinking_models_summary.md
│   ├── framework_flow.mmd
│   ├── faq.md
│   └── process_config.json
└── 人本教练/
    └── ...
```

---

## 注意事项

1. **EPUB 文件命名**：建议使用简化的文件名（如 `《书名》.epub`），避免特殊字符
2. **图片为主的书**：如果 EPUB 内容主要为图片，`full_text.txt` 可能非常少，需要手动补充 `summary.txt` 和 `framework_article.txt`
3. **重复处理**：重新运行脚本时，会覆盖已有文件（除原始 EPUB 外）
4. **编码**：所有输出文件使用 UTF‑8 编码

---

## 故障排查

| 问题 | 原因 | 解决 |
|------|------|------|
| `jq 未安装` | 缺少依赖 | `sudo apt-get install -y jq` |
| `unzip: command not found` | 缺少解压工具 | `sudo apt-get install -y unzip` |
| `未找到 epub 文件` | 文件夹内无 `.epub` 文件 | 确保 EPUB 文件已放入书籍文件夹 |
| 生成文件为空 | EPUB 为图片格式 | 手动补充 `summary.txt` 和 `framework_article.txt` |

---

## 扩展开发

如需自定义生成内容，可以修改 `.skills/book-processor/scripts/process_book.sh` 脚本。

**自动化集成**：  
该技能已被集成到 OpenClaw 的自动化流程中，当检测到 `.epub` 文件时会自动触发。

---

*最后更新：2026‑03‑14*