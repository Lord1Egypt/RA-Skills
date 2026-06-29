# Agent 工作流

这个项目不是让用户手动点脚本，而是给 Agent 一组可靠工具。Agent 负责理解用户目标、配置本地环境、运行流水线、检查结果、解释异常。

## 1. 开始前

先向用户说明风险：

- 会读取指定日期范围内的邮箱标题、正文摘要、链接和附件。
- 授权码只保存到本地 `.env`，不提交 Git，不在回复里展示。
- 台账是辅助结果，需要用户复核。
- 只处理发票邮件，不处理无关邮件。

收集信息：

- 邮箱地址
- 邮箱授权码
- 日期范围
- IMAP 主机、端口，默认 `imap.qq.com:993`
- `MAIL_WEB_USER`，QQ 邮箱通常填 QQ 号

## 2. 初始化

如果用户在对话中给了账号信息，直接写入本地 `.env`。不要回显授权码。

如果用户希望自己输入，运行：

```bash
npm install
npm run setup
```

然后检查环境：

```bash
npm run doctor
npm run check
```

## 3. 运行

完整执行：

```bash
npm run run -- 2026-06-15 2026-06-22
```

流水线：

1. 扫描发票候选邮件。
2. 分类附件、链接、平台页、图片/二维码、人工项。
3. 下载源文件到中转目录。
4. 从 PDF 识别发票字段。
5. 按 UID 合并邮件和 PDF 数据。
6. 生成 Excel 台账。
7. 归档 PDF 并生成 HTML 汇总页。

## 4. 检查结果

运行后必须检查：

- 发票候选邮件数量。
- 下载成功数量。
- PDF 识别数量。
- 完整记录数量。
- 人工任务数量。
- `archive/index.html` 是否可打开。

重点文件：

- `archive/index.html`
- `scan-results/发票台账-{dateTag}.xlsx`
- `scan-results/manual-tasks-{dateTag}.csv`
- `scan-results/invoice-final-{dateTag}.json`

## 5. 人工任务

任何无法自动处理的邮件都不能静默跳过，必须进入人工任务或异常项。

常见原因：

- 链接过期。
- 链接需要扫码。
- 平台防盗链。
- PDF 无法解析。
- 缺少购买方、销售方或金额。

向用户汇报时，说明 UID、邮件标题、已知字段、失败原因和建议动作。

## 6. 扩展原则

不要只为某一封邮件写特例。重复出现的失败模式应抽象成新的链接解析类型或字段识别规则。

最终数据可信顺序：

```text
PDF 发票正文 > PDF 文件名 > 邮件正文 > 邮件标题 > 发件人/映射推断
```

提交代码前确认这些内容没有进入 Git：

- `.env`
- `config/IMAP_CREDENTIALS.js`
- `config/mailboxes.json`
- `scan-results/`
- `archive/`
- 邮箱授权码
