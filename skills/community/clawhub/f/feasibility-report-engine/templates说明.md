# 模板文件说明

本包 `templates/` 提供两份**文本模板**（.md），写作前先填、交付前先查：

| 文件 | 何时用 |
|------|--------|
| `report-plan.md` | 动笔前：每章填「要说什么｜凭什么说｜从哪来」三列，**证据列留白的章节退回补料，不许带着空证据开写** |
| `review-checklist.md` | 交付前：质量三关（反思/审查/修正）逐条打勾，并记录修正处 |

> .docx / .xlsx 成品模板请用 `scripts/` 内脚本一键生成（本平台不随包分发二进制模板）：
> - 报告骨架：`python3 scripts/gen_report_docx.py "项目名称" "" 输出.docx`
> - 测算套表：`python3 scripts/gen_model_xlsx_v2.py 输出.xlsx "项目名" 总投资万元 达产收入万元 建设期 运营期`
> - 编制说明：`python3 scripts/gen_shuoming.py 输出.docx "项目名称" "约XX亿元"`
