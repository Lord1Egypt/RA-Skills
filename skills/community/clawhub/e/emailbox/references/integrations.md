# 文档数据联动 Document Integration

邮件与文档数据处理的一体化工作流。结合其他 Skills 的能力，实现"数据处理 → 格式化 → 邮件发送"的自动化。

---

## 场景总览

| 场景 | 数据来源 | 邮件输出 | 关联 Skill |
|------|----------|----------|-----------|
| Excel 报表发送 | .xlsx/.csv 数据 | HTML 表格 + 附件 | excel-studio |
| 发票识别+邮件 | 图片/PDF 发票 | 结构化摘要 + 附件 | china-doc-ocr |
| 合同审核+邮件 | 合同 PDF | 审核要点 + 附件 | china-doc-ocr, china-legal-analysis |
| PDF 报告发送 | PDF 文件 | 摘要 + 附件 | pdf-studio |
| 简历解析+邮件 | 简历 PDF/Word | 候选人摘要 + 附件 | china-doc-ocr |
| 数据分析+邮件 | 原始数据 | 分析结论 + 图表 | data-analyzer |

---

## 工作流模板

### 流程 1：Excel 数据 → 格式化邮件

```
用户请求："把这个 Excel 的销售数据做成表格发邮件给老板"
↓
Step 1: 读取 Excel 文件
  → 使用 excel-studio 读取数据
  → 或使用 python3 + openpyxl 直接读取
↓
Step 2: 数据处理与格式化
  → 提取关键指标（总计、变化、排名等）
  → 生成 HTML 表格（使用 templates.md 中商务报告模板）
  → 生成纯文本摘要（作为 fallback）
↓
Step 3: 生成邮件内容并保存
  → 将 HTML 保存为 ${OPENCLAW_WORKSPACE}/.emailbox_body.html
  → 将纯文本保存为 ${OPENCLAW_WORKSPACE}/.emailbox_body.txt
↓
Step 4: 发送邮件
  python3 scripts/send_mail.py \
    --to boss@company.com \
    --subject "销售数据周报 - $(date +%Y%m%d)" \
    --body-file "${OPENCLAW_WORKSPACE}/.emailbox_body.txt" \
    --html-file "${OPENCLAW_WORKSPACE}/.emailbox_body.html" \
    --attach /path/to/sales_data.xlsx \
    --provider qq
```

### 流程 2：OCR 识别 → 邮件通知

```
用户请求："识别这张发票，把结果发邮件给财务"
↓
Step 1: OCR 识别
  → 使用 china-doc-ocr 识别发票图片/PDF
  → 提取关键字段：发票号码、金额、日期、购方/销方信息
↓
Step 2: 格式化邮件内容
  → 使用 templates.md 中的发票通知模板
  → 填入识别出的字段数据
  → 生成纯文本摘要
↓
Step 3: 发送邮件
  python3 scripts/send_mail.py \
    --to finance@company.com \
    --subject "发票处理 - ${invoice_number}" \
    --body-file "${OPENCLAW_WORKSPACE}/.emailbox_body.txt" \
    --html-file "${OPENCLAW_WORKSPACE}/.emailbox_body.html" \
    --attach /path/to/invoice.jpg \
    --provider 163
```

### 流程 3：合同审核 → 邮件汇报

```
用户请求："审核这份合同后把要点发邮件给法务"
↓
Step 1: 识别合同
  → 使用 china-doc-ocr 识别合同文本
↓
Step 2: 法律分析
  → 使用 china-legal-analysis 分析合同条款
  → 提取风险点和审核意见
↓
Step 3: 格式化并发送
  python3 scripts/send_mail.py \
    --to legal@company.com \
    --subject "合同审核报告 - ${contract_name}" \
    --body-file "${OPENCLAW_WORKSPACE}/.emailbox_body.txt" \
    --html-file "${OPENCLAW_WORKSPACE}/.emailbox_body.html" \
    --attach /path/to/contract.pdf \
    --importance high \
    --provider qq
```

### 流程 4：简历解析 → 转发 HR

```
用户请求："解析这份简历然后转发给HR"
↓
Step 1: 识别简历
  → 使用 china-doc-ocr 识别简历 PDF/图片
↓
Step 2: 结构化提取
  → 提取姓名、学历、工作经验、技能等
  → 生成候选人摘要卡片
↓
Step 3: 转发邮件
  python3 scripts/send_mail.py \
    --to hr@company.com \
    --subject "候选人推荐 - ${candidate_name} - ${position}" \
    --body-file "${OPENCLAW_WORKSPACE}/.emailbox_body.txt" \
    --html-file "${OPENCLAW_WORKSPACE}/.emailbox_body.html" \
    --attach /path/to/resume.pdf
```

### 流程 5：数据分析 → 邮件报告

```
用户请求："分析这份数据后发邮件给团队"
↓
Step 1: 读取和数据
  → 使用 data-analyzer 或 python3 分析 CSV/Excel
↓
Step 2: 生成分析报告
  → 关键指标、趋势、异常值
  → 生成 HTML 报告格式
↓
Step 3: 发送邮件
  python3 scripts/send_mail.py \
    --to "team1@company.com,team2@company.com" \
    --subject "数据分析报告 - $(date +%Y%m%d)" \
    --body-file "${OPENCLAW_WORKSPACE}/.emailbox_body.txt" \
    --html-file "${OPENCLAW_WORKSPACE}/.emailbox_body.html" \
    --attach /path/to/data.xlsx
```

### 流程 6：定时日报/周报

```
用户请求："每天早上9点自动发日报给老板"
↓
Step 1: 收集日报内容
  → 用户或 AI 生成日报内容
  → 保存为 HTML 文件
↓
Step 2: 设置定时发送
  python3 scripts/schedule_mail.py \
    --schedule \
    --at "2026-04-19 09:00" \
    --to boss@company.com \
    --subject "工作日报 - $(date +%Y-%m-%d)" \
    --body-file "${OPENCLAW_WORKSPACE}/.emailbox_body.txt" \
    --html-file "${OPENCLAW_WORKSPACE}/.emailbox_body.html" \
    --provider qq
↓
Step 3: 管理定时任务
  # 查看已安排的定时邮件
  python3 scripts/schedule_mail.py --list-scheduled

  # 取消定时邮件
  python3 scripts/schedule_mail.py --cancel SCHEDULE_ID

  # 手动处理到期队列
  python3 scripts/schedule_mail.py --process-queue
```

---

## 数据格式转换速查

### 从 Excel 生成 HTML 表格

```python
import json

# 假设从 Excel 读取的数据格式
data = [
    ["指标", "本周", "上周", "变化"],
    ["营收", "¥128万", "¥115万", "↑11.3%"],
    ["用户数", "12,345", "11,890", "↑3.8%"],
    ["转化率", "3.2%", "2.9%", "↑0.3pp"],
]

# 生成 HTML 表格行
table_rows = ""
for i, row in enumerate(data):
    if i == 0:
        continue  # 跳过表头（模板已有）
    color = "#27ae60" if "↑" in row[3] else "#e74c3c"
    table_rows += f'<tr style="border-bottom:1px solid #eee;">'
    for j, cell in enumerate(row):
        align = "text-align:right" if j > 0 else ""
        font = "font-weight:bold" if j == 3 else ""
        row_color = f'color:{color}' if j == 3 else ""
        table_rows += f'<td style="padding:10px 16px;font-size:14px;{align};{font};{row_color};">{cell}</td>'
    table_rows += '</tr>\n'
```

### 从 OCR 结果生成邮件内容

```python
# OCR 识别结果（从 china-doc-ocr 获取）
ocr_result = {
    "invoice_number": "12345678",
    "amount": "¥5,280.00",
    "date": "2026年4月18日",
    "seller": "XX科技有限公司",
    "buyer": "YY集团有限公司",
}

# 生成摘要文本
summary = f"""发票识别结果：
发票号码：{ocr_result['invoice_number']}
开票日期：{ocr_result['date']}
金额：{ocr_result['amount']}
销售方：{ocr_result['seller']}
购买方：{ocr_result['buyer']}
"""
```

---

## 与 Skills 联动清单

| Skill | 联动方式 | 典型场景 |
|-------|----------|----------|
| china-doc-ocr | OCR 识别 → 邮件内容 | 发票、合同、证件识别后邮件发送 |
| excel-studio | 读取 Excel → 表格邮件 | 数据报表、财务报告 |
| pdf-studio | PDF 处理 → 邮件附件 | PDF 报告发送 |
| data-analyzer | 数据分析 → 结论邮件 | 数据洞察通知 |
| china-legal-analysis | 合同审核 → 邮件通知 | 合同风险点邮件通知 |
| interview-pro | 面试反馈 → 邮件通知 | 候选人评估结果邮件 |