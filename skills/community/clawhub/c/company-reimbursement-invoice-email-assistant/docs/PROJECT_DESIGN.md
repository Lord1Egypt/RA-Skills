# 项目设计

## 目标

让 Agent 用轻量 Node.js 工具管理邮箱里的发票邮件：

- 扫描发票候选邮件。
- 判断发票来源类型。
- 下载 PDF/OFD/图片等源文件。
- 从 PDF 提取真实发票字段。
- 生成 Excel 台账。
- 按购买方、销售方归档 PDF。
- 把不能自动处理的邮件交给人工。

## 数据流

```text
邮箱
  -> step1-email-scan.js
  -> scan-results/emails/emails-{dateTag}.json
  -> step2-classify-invoices.js
  -> scan-results/classified/classified-{dateTag}.json
  -> step2-download-pdf.js
  -> scan-results/staging/{dateTag}/
  -> step3-extract-pdf.js
  -> scan-results/pdf-text-{dateTag}.json
  -> step4-merge-data.js
  -> scan-results/invoice-final-{dateTag}.json
  -> step5-generate-ledger.js
  -> scan-results/发票台账-{dateTag}.xlsx
  -> archive-invoices.js
  -> archive/
```

## 核心设计

### UID 是主键

全流程使用 IMAP UID 串联邮件、附件、下载记录、PDF 识别结果和最终台账。

### 中转目录

所有下载源文件先进入：

```text
scan-results/staging/{dateTag}/
  pdfs/
  ofds/
  images/
  failed/
```

`archive/` 只放最终交付文件，不作为处理工作区。

### 分类先于下载

`step2-classify-invoices.js` 把每封候选邮件分成明确类型：

- `attachment_pdf`
- `attachment_pdf_ofd`
- `attachment_ofd`
- `attachment_image`
- `link_direct_pdf`
- `link_direct_ofd`
- `link_platform_page`
- `link_qrcode_image`
- `link_unknown_page`
- `manual_body`
- `scan_error`

Agent 可以先检查分类结果，再决定是否需要改进解析器。

### PDF 字段最高优先级

购买方、销售方、金额、发票号、开票日期必须优先使用 PDF 发票正文。

```text
PDF 发票正文 > PDF 文件名 > 邮件正文 > 邮件标题 > 发件人/映射推断
```

邮件正文用于初筛、链接发现和缺失字段兜底，不能覆盖 PDF 的真实发票数据。

### 归档只展示 PDF

最终归档规则：

```text
archive/{购买方}/{销售方}/{金额}_{购买方关键字}_{发票号后6位}_{类型}_{月份}.pdf
```

OFD 保留在中转目录用于追溯，但不进入 HTML 汇总，避免和 PDF 重复。

### 人工任务不是失败

无法自动处理的邮件必须进入 `manual-tasks-*.csv` 或 HTML 异常页。

人工任务至少包含：

- UID
- 邮件标题
- 邮件日期
- 已知购买方、销售方、金额
- 原始链接或附件线索
- 失败原因
- 建议动作

## 安全边界

项目只处理发票邮件，不处理普通邮箱内容。

不得提交：

- `.env`
- `config/IMAP_CREDENTIALS.js`
- `config/mailboxes.json`
- `scan-results/`
- `archive/`
- 任何邮箱授权码或用户发票源文件
