---
name: crc-monthly-financial-report
description: "从财务部固定格式月度 Excel 底稿生成月度财务报告正文、Markdown 和 Word 文件。Use when: 用户上传月度财报底稿、要求生成月报正文、需要 Word 下载文件、需要复用 Dify 月度财报智能体的 Excel 处理逻辑。NOT for: 非固定模板 Excel、财务审计判断、补造或修改底稿数据。需要 Python3 + openpyxl；.xls 需要 xlrd。"
metadata: { "openclaw": { "emoji": "📊", "requires": { "bins": ["python3", "pip"] } } }
---

# 月度财报生成

把财务部固定格式月度 Excel 底稿转换为月度财务报告正文，并生成 `.md` 与 `.docx` 文件。该 Skill 来源于 Dify「月度财报智能体-财务内测版」的处理流程，但执行时直接读取 Excel 单元格，不依赖 Dify 文档提取器。

## When to Use

Use this skill when:

- 用户说“根据月度 Excel 底稿生成财务月报”
- 用户上传 `底稿-5月.xlsx` 这类固定格式月度财务数据表
- 用户需要输出财报正文并提供 Word 下载文件
- 用户想把 Dify 月度财报智能体的 Excel 处理逻辑迁移到 OpenClaw / 类 OpenClaw 智能体中
- 财务内测需要可复核、固定口径的月报初稿

Do not use this skill when:

- 输入不是 `.xlsx` / `.xls` 财务月度底稿
- Excel 结构不是“本月、上月、环比、去年同月、同比、累计实际、年初或去年同期、同比、全年预算、预算完成率”
- 用户要求审计判断、经营归因定稿、会计调整或补造数据
- 用户要求修改底稿数字；此类变更应先在 Excel 中确认后重新生成

## Workflow

1. 确认用户已把月度 Excel 底稿放到 workspace。
2. 如首次使用，安装依赖并确认脚本存在。
3. 执行脚本生成 `.md`、`.docx` 和 `.json` 摘要。
4. 成功后只把 Word 下载链接告诉用户，优先使用脚本 JSON 输出中的 `word_download_markdown`。
5. 提醒用户复核底稿数字、占位归因和最终经营判断。

## Commands

### 首次使用

```bash
pip install openpyxl
```

如果需要处理旧版 `.xls` 文件，再安装：

```bash
pip install xlrd
```

### 生成月度财报

```bash
python3 /home/node/agents/skills/crc-monthly-financial-report/scripts/monthly_financial_report.py \
  "/home/node/workspace/底稿-5月.xlsx" \
  --output-dir "/home/node/workspace/月度财报输出"
```

指定报告期间或工作表：

```bash
python3 /home/node/agents/skills/crc-monthly-financial-report/scripts/monthly_financial_report.py \
  "/home/node/workspace/底稿-5月.xlsx" \
  --period "2026年5月" \
  --sheet "5月" \
  --output-dir "/home/node/workspace/月度财报输出"
```

## Outputs

输出目录包含：

```text
月度财报输出/
├── 月度财务报告_2026年5月.md
├── 月度财务报告_2026年5月.docx
└── 月度财务报告_2026年5月.json
```

`.json` 摘要中包含：

- 识别到的工作表名
- 报告期间
- 生成的 Markdown / Word 文件路径
- Word 下载链接字段 `word_download_url` / `word_download_markdown`（当运行环境提供 `CLAWMATE_INSTANCE_ID` 时）
- 提取到的指标名称
- 报告正文

## Report Logic

脚本会自动：

- 从工作表名或标题识别报告期间，例如 `2026年05月主要财务数据`
- 未指定工作表时，自动选择最新的月度数据工作表
- 识别三个分组：`资产负债（亿元）`、`损益（万元）`、`主要财务指标`
- 提取核心经营指标：`营业收入`、`利润总额`、`净利润`
- 提取资产负债指标：`总资产`、`总负债`、`所有者权益`
- 提取比率指标：`资产负债率`、`杠杆率`、`ROE`、`ROA`、`管理费用率`、`关注资产率`、`不良资产率`
- 将损益类万元自动换算为亿元
- 按 Dify 旧流程生成“标题行 + 一、二、三、四”格式报告正文
- 将 `【...】` 归因占位内容在 Word 中标红，提醒财务人员补充或复核

## Quick Responses

用户说“请根据底稿生成月度财务报告并提供 Word 下载”时：

```bash
python3 /home/node/agents/skills/crc-monthly-financial-report/scripts/monthly_financial_report.py \
  "<用户上传的 Excel 路径>" \
  --output-dir "/home/node/workspace/月度财报输出"
```

然后回复：

```text
月度财务报告已生成。

Word 文件：<直接粘贴脚本输出中的 word_download_markdown>

请重点复核：
1. 报告期间和工作表是否正确；
2. 营业收入、利润总额、净利润、资产负债指标是否与底稿一致；
3. 标红的【原因占位】是否需要替换为正式归因；
4. 本报告为系统自动生成初稿，请结合底稿复核。
```

回复规则：

- 只主动展示 Word 下载链接，不主动展示 `.md` 或 `.json` 下载链接。
- 不要要求用户再去文件管理或工作区查找 Word；除非下载链接无法生成，才给出 `/workspace/...docx` 路径作为兜底。
- 如果脚本输出里有 `word_download_markdown`，直接复制该 Markdown 链接。
- 如果脚本输出里没有 `word_download_markdown`，但环境变量里有 `CLAWMATE_INSTANCE_ID`，重新运行脚本或按 `/api/instances/<CLAWMATE_INSTANCE_ID>/files/download?path=<URL 编码后的 /workspace/...docx>` 生成链接。

## Notes

- 该 Skill 只做底稿解析和初稿生成，不替代财务复核。
- 脚本不使用外部模型，不会自行编造数字。
- 如果用户要求“把净利润改成某个值”，应先确认是否要修改 Excel 底稿；脚本不会在不改底稿的情况下重算指标。
- 如果输出为 `未识别`，通常是工作表结构变化、单元格为空、字段名变化或输入不是固定模板。
- Word 生成优先使用 `python-docx`；如果运行环境没有该库，脚本会用内置 OOXML fallback 生成基础 `.docx`。
- 当前开发版已基于财务部提供的 `底稿-5月.xlsx`、跨年多月份参考底稿、非固定模板失败路径和普通用户 Word 下载路径完成验证。
