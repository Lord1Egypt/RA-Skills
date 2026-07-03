---
name: 敏感词筛查-CMT-1.0
description: >
  This skill should be used when the user wants to check files (PDF, Word,
  Excel) for sensitive/prohibited words from a word library, and highlight them
  in yellow. The skill has a built-in word library (65 words, 9 categories) and
  also supports external word files.
agent_created: true
version: "3.0"
disable: false
---

# Sensitive Word Checker Skill v3（内置词库版）

## Purpose

检查文件（PDF、Word、Excel）中的敏感/禁用词，**仅对匹配的敏感词本身标黄**（非整段/整句标黄），输出标注后的文件。

## When to Use

- 用户要求对文件进行敏感词筛查/审核
- 合同审核或文档合规检查
- 触发关键词：敏感词、禁用词、检查、审核、标注、标黄

## Workflow

### Step 1: 收集信息

从用户处获取：
1. **待检测文件**：PDF、Word（.docx）或 Excel（.xlsx/.xls）
2. **敏感词库**（可选）：默认使用内置词库（9类65个词条）；也可指定外部 .docx 词库文件
3. **输出位置**：默认桌面

### Step 2: 运行检测脚本

**使用内置词库（推荐，无需额外文件）：**
```bash
python sensitive_word_checker.py --input <待检文件> --output <输出目录>
```

**使用外部词库文件：**
```bash
python sensitive_word_checker.py --words <敏感词库.docx> --input <待检文件> --output <输出目录>
```

**参数说明：**
| 参数 | 说明 | 是否必填 |
|------|------|----------|
| `--input` | 待检测文件路径 | **必填** |
| `--words` | 敏感词库文件路径（.docx） | 可选，不填则用内置词库 |
| `--output` | 输出目录（默认桌面） | 可选 |

### Step 3: 输出结果

- Word文件：`.docx` — **仅敏感词文字本身**标黄（黄色底色+黄色字体高亮）
- Excel文件：`.xlsx` — 含敏感词的单元格标黄
- PDF文件：`.pdf` — 敏感词区域添加黄色高亮注释

## 内置敏感词库（9类65词）

| 类别 | 敏感词 |
|------|--------|
| 高规格名号 | 中国、中华、国家、全国、国际、世界、全球、环球、亚洲、中外、海外、中西、自贸港、峰会、高端、高峰、巅峰、多双边机制 |
| 会议名称 | 分论坛、卫星会、论坛、讲座、讲坛、大会、年会、报告会、研讨会、培训班、上市会、推介会、研讨班 |
| 评奖活动 | 评比、评选、赛、大赛、海选、奖励、奖、示范、表彰、标杆、比拼、达标、植入、学分、案例 |
| 企业专题 | 企业专题会 |
| 名称包含 | 产品名、商品名 |
| 报社文本 | 讲者幻灯 |
| 茶歇宴会 | 茶歇、宴会、宴请 |
| 收费合同 | 软文、报道、硬广、采访、新闻、稿件、文章、字数、记者、驻地记者 |
| 其他 | 授牌、飞检 |

## 核心改进（v1 → v2 → v3）

| 项目 | v1（旧版） | v2（精确标黄） | v3（内置词库） |
|------|-----------|-------------|-------------|
| **标黄精度** | 整个run/段落标黄 | **仅敏感词文字本身标黄** | 同v2 |
| **词库来源** | 需外部文件 | 需外部文件 | **内置65词，开箱即用** |
| **词库格式** | 仅支持简单列表 | 支持【严禁】分类格式 + 表格 | 内置 + 仍支持外部文件 |
| **--words参数** | 必填 | 必填 | **可选** |

## Python Script Location

脚本位于当前 skill 目录下的 `scripts/sensitive_word_checker.py`。

运行前先确保已安装依赖：
```bash
pip install python-docx openpyxl pypdf2 pymupdf
```


## Notes

- 匹配不区分大小写
- 支持部分匹配（如"广告"可命中"广告投放"）
- 长词优先匹配（避免短词误吞长词的一部分）
- 自动合并重叠匹配区间
- 保持原文档格式不变
