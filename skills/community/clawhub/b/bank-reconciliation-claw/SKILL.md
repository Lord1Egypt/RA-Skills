---
name: bank-reconciliation-claw
description: |
  银行流水对账虾 — 自动核对银行流水、发票台账与系统订单，实现财务三方数据闭环。

  **当以下情况时使用此 Skill**：
  (1) 用户上传银行流水文件（Excel/CSV），要求与订单或发票进行核对
  (2) 需要识别未匹配条目、金额差异、重复流水、日期偏差等异常
  (3) 需要生成对账报告（匹配明细 + 异常清单），可选写入飞书多维表格
  (4) 需要对历史数据进行补对账或多账户汇总对账
  (5) 用户提到"对账"、"流水核对"、"发票匹配"、"银行流水"、"三方核验"、"差异报告"、"未匹配"、"重复入账"、"漏单"、"账单比对"
---

# 银行流水对账虾

自动核对银行流水、系统订单、发票台账，秒级定位差异，对账时间从半天压缩到分钟级。全程本地处理，财务数据不外传。

## 工作流程

1. **数据接收** — 接收用户上传的 Excel/CSV 文件（流水、订单、发票）
2. **字段标准化** — 统一日期格式（YYYY-MM-DD）、金额格式（两位小数）、编号格式
3. **智能匹配** — 精确匹配 + 模糊匹配 + 多对一匹配（见 `references/reconciliation-rules.md`）
4. **差异识别** — 标记四类异常：🔴未匹配 / 🟡金额差异 / 🟠重复条目 / 🔵日期偏差
5. **输出报告** — 生成匹配汇总、明细表、异常清单；可选写入飞书多维表格

## 使用方式

### 快速对账（两表）

用户说："帮我核对这份银行流水和订单表"，然后提供文件路径或上传文件。

调用核心脚本：

```bash
python3 scripts/reconcile.py reconcile \
  --bank <bank_file.xlsx> \
  --orders <orders_file.csv> \
  --output report.xlsx
```

### 三表全核

```bash
python3 scripts/reconcile.py reconcile \
  --bank <bank_file.xlsx> \
  --orders <orders_file.csv> \
  --invoices <invoices_file.xlsx> \
  --date-tolerance 3 \
  --output report.xlsx
```

### 预览数据解析

```bash
python3 scripts/reconcile.py preview --file <any_file.xlsx>
```

### 写入飞书多维表格

```bash
python3 scripts/reconcile.py export \
  --report report.xlsx \
  --bitable-url <飞书多维表格URL>
```

## 输入要求

| 文件类型 | 必填字段 | 说明 |
|---------|---------|------|
| 银行流水 | 交易日期、金额、流水号 | 支持主流银行格式，见 field-mapping.md |
| 系统订单 | 支付时间、金额、订单号 | 支持金蝶/用友/SAP 导出格式 |
| 发票台账 | 开票日期、开票金额、发票号 | 增值税发票标准格式 |

- 文件编码建议 UTF-8
- 金额列不含货币符号（脚本会自动清理 ¥ $ ,）
- 单文件建议不超过 50MB（约 10 万行）

## 参考资料

- `references/reconciliation-rules.md` — 匹配规则、容差配置、异常分级
- `references/field-mapping.md` — 各银行/ERP/开票平台字段映射
- `references/desensitization-rules.md` — 脱敏规则（账号、姓名等）

## 依赖

```
Python 3.8+
pandas
openpyxl
```

安装：`pip install pandas openpyxl`

## 与其他虾的协作

- **cross-platform-messenger-claw** — 对账完成后推送报告摘要到财务群
- **auto-data-analysis-claw** — 对对账结果做趋势分析、异常归因
- **feishu-bitable** — 将对账报告写入飞书多维表格供团队协作处理
