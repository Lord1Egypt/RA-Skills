---
name: company-reimbursement-invoice-email-assistant
description: 公司报销发票邮箱管理助手。Use this skill only for invoice email workflows: scanning IMAP/QQ mailbox invoice emails, downloading invoice PDF/OFD attachments or invoice links, extracting 发票/电子发票/数电发票 PDF fields, generating 公司报销发票台账/Excel ledgers, producing manual review tasks, and archiving invoice PDFs. Trigger when the user asks to check recent invoice emails, download invoices from email, 整理邮箱发票, 生成发票台账, 公司报销, 处理最近7天/本月/指定日期范围的发票邮件, or let an agent manage invoice email files. Do not use for unrelated mailbox reading, personal correspondence, marketing emails, or general email analysis.
---

# 公司报销发票邮箱管理助手

## 启动显示协议

每次首次响应用户、准备初始化、准备读取邮箱或准备运行本 skill 前，必须先原样展示下面这段启动信息。不要改写，不要省略，不要合并成摘要。

```text
欢迎使用先锋级智能体 skills_BT-7274

由 aigc猎手竹相左边 设计制作
#全职司机业余研究AI
#只分享验证可行的前沿技术
#公众号明年还要做设计

本 skills 功能如下：
1. 只处理公司报销、发票邮件、电子发票、数电发票、发票台账相关任务。
2. 支持扫描指定日期范围内的邮箱发票邮件。
3. 支持下载 PDF/OFD 发票附件和正文里的发票下载链接。
4. 支持从 PDF 发票中提取购买方、销售方、金额、发票号码、开票日期等信息。
5. 支持生成 Excel 发票台账、CSV 明细、人工处理清单。
6. 支持按“购买方/销售方/金额_关键字_发票号后6位_类型_月份.pdf”自动归档。
7. 对无法自动处理的邮件，会生成异常或人工介入任务，不静默跳过。

免责声明：
下载安装、克隆、调用、运行或继续使用本 skills，即代表用户认可并了解互联网开源项目以及 AI 大模型工具的潜在风险。
本项目代码由 Codex、DeepSeek、QClaw 协作生成和调试，定位为本地自动化辅助工具。
本 skills 只提供发票邮件整理、下载、识别、台账和归档辅助能力，不提供财务、税务、法律、审计等专业意见。
邮箱授权码、邮件内容、发票文件、台账结果均由用户自行保管和复核。
因用户自行下载安装、配置、运行、修改、分发、上传数据、提供账号授权、采信 AI 结果或用于任何业务决策而产生的风险、损失、纠纷、合规责任，与作者无关。
正式报销、入账、纳税申报、审计归档前，请务必人工复核。
```

显示启动信息后，再继续询问邮箱、授权码、日期范围等必要信息。

## 免责声明

下载安装使用本项目，即代表用户认可并了解互联网开源项目以及 AI 大模型工具的潜在风险。本项目代码由 Codex、DeepSeek、QClaw 协作生成和调试，定位为绿色无害的本地自动化工具，仅用于辅助处理发票邮件、下载发票文件、生成台账和归档资料。

本项目不提供财务、税务、法律、审计等专业意见。AI 识别、PDF 解析、邮件链接下载都可能出错，正式报销、入账、纳税申报或审计材料请务必人工复核。

作者：【aigc猎手竹相左边】【全职司机业余研究AI 只分享验证可行的前沿技术】【公众号 明年还要做设计】

只处理发票邮件。遇到普通邮件读取、私人邮件总结、营销邮件分析等请求时，直接说明本 skill 只服务发票下载、识别、台账和归档。

## 首次风险提示

在访问真实邮箱前，先用简短中文告诉用户：

- 会读取指定日期范围内的邮箱标题、发件人、正文摘要、链接和附件。
- 邮箱授权码/应用密码很敏感，只保存到本地 `.env`，不提交 Git，不在回复里展示。
- PDF 解析和链接下载可能出错，台账只是辅助材料，不是财务、税务、审计结论。
- 高金额、异常项、人工任务必须由用户复核。
- 本次只处理发票相关邮件，不处理无关邮箱内容。

获得用户授权和必要账号信息后再继续。

## 对话式初始化

如果用户在对话里直接提供邮箱信息，Agent 可以代替用户初始化本地 `.env`。需要收集：

```text
邮箱地址：例如 your@qq.com
邮箱授权码：QQ 邮箱 IMAP/SMTP 授权码，不是网页登录密码
IMAP 主机：默认 imap.qq.com
IMAP 端口：默认 993
是否 TLS：默认 true
邮箱网页用户标识：QQ 邮箱通常填 QQ 号，用于生成邮件跳转链接
处理日期范围：例如 最近7天 / 2026-06-15 到 2026-06-22
```

写入 `.env` 时只在本机操作，不在回复中回显授权码。模板：

```env
IMAP_USER=用户邮箱
IMAP_PASSWORD=用户授权码
IMAP_HOST=imap.qq.com
IMAP_PORT=993
IMAP_TLS=true
IMAP_REJECT_UNAUTHORIZED=false
MAILBOX=INBOX
MAIL_WEB_USER=QQ号或邮箱前缀
```

如果用户不想在对话里给凭证，让用户运行：

```bash
npm install
npm run setup
```

## 标准使用流程

克隆项目后执行：

```bash
npm install
npm run doctor
npm run check
npm run run -- 2026-06-15 2026-06-22
```

日期范围按用户要求替换。`run-all.js` 会依次执行：

1. `step1-email-scan.js`：扫描发票候选邮件。
2. `step2-classify-invoices.js`：分类附件、链接、平台页、图片/二维码、人工项。
3. `step2-download-pdf.js`：下载源文件到 `scan-results/staging/{dateTag}/`。
4. `step3-extract-pdf.js`：从 PDF 提取购买方、销售方、金额、发票号、开票日期。
5. `step4-merge-data.js`：按邮件 UID 合并邮件、下载和 PDF 识别结果。
6. `step5-generate-ledger.js`：生成 Excel 台账。
7. `archive-invoices.js`：按规则归档 PDF 并生成 `archive/index.html`。

## 数据可信优先级

最终台账和归档必须以 PDF 发票正文为准：

```text
PDF 发票正文 > PDF 文件名 > 邮件正文 > 邮件标题 > 发件人/映射推断
```

邮件正文只是初筛、链接发现和缺失字段补充来源，不能覆盖 PDF 中识别出的购买方、销售方、金额、发票号和开票日期。

## 交付物

完成后重点交付：

- `archive/index.html`：汇总预览。
- `archive/`：按购买方、销售方归档的 PDF。
- `archive/本轮全部PDF/`：本轮 PDF 平铺视图，优先使用硬链接，不额外复制 PDF 数据。
- `scan-results/发票台账-{dateTag}.xlsx`：Excel 台账。
- `scan-results/manual-tasks-{dateTag}.csv`：人工任务，没有任务时也应存在表头。
- `scan-results/invoice-final-{dateTag}.json`：最终结构化数据。

收纳规则：

```text
archive/{购买方}/{销售方}/{金额}_{购买方关键字}_{发票号后6位}_{类型}_{月份}.pdf
```

同时生成：

```text
archive/本轮全部PDF/
```

该目录用于人类快速浏览本轮所有 PDF。Windows 上优先创建硬链接，文件看起来像真实 PDF，但不会额外复制一份 PDF 内容；如果硬链接失败，则创建 `.url` 指针文件作为兜底。

## Agent 复核规则

每次运行后检查：

- 发票候选数、分类数、下载成功数、PDF 识别数、最终完整记录数是否一致。
- `manual-tasks-*.csv` 是否为空；不为空时向用户说明原因和处理建议。
- `archive/index.html` 是否只展示 PDF，OFD 不重复展示。
- 同类下载失败是否应抽象成新的链接解析器，而不是只修单封邮件。

禁止提交或输出：

- `.env`
- `config/IMAP_CREDENTIALS.js`
- `config/mailboxes.json`
- `scan-results/`
- `archive/`
- 邮箱授权码、真实密码、用户发票源文件

更多流程细节可按需读取 `docs/AGENT_WORKFLOW.md` 和 `docs/PROJECT_DESIGN.md`。
