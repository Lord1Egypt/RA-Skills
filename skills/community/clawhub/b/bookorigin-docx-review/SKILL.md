---
slug: bookorigin-docx-review
displayName: BookOrigin DOCX Review
version: 1.0.0
description: 在本机对授权 DOCX 做安全 ZIP/结构预检与有限教材判据检查；复核哈希绑定的人工审阅案例并导出仅建议性审阅包。
---

# BookOrigin DOCX Review

Node.js 20 或更高版本即可运行；没有 npm 依赖，不联网、不调用模型、不上传文件、不生成、修改或覆盖 DOCX。调用者须确认对输入文件拥有处理授权。

## 无界面动作

```powershell
node cli.mjs book-docx-safe-preflight --input 'D:\safe\教材.docx'
node cli.mjs book-docx-safe-preflight --input 'D:\safe\教材.docx' > preflight.json
node cli.mjs book-review-package --case-json preflight.json --source 'D:\safe\教材.docx' --decisions decisions.json
```

标准输出恰好一行 JSON，不含绝对路径、原文、DOCX 字节或密钥。动作 schema、稳定错误码和案例格式见 `action-contract.json`。退出码：`0` 成功；`2` 输入/已知失败；`3` 完整性或审阅绑定拒绝；`4` 意外运行时错误。

`book-docx-safe-preflight` 只读输入：先检查 ZIP 目录、压缩限制、路径、加密、宏和 DOCX 必需结构，再从 `word/document.xml` 做只读文本投影，输出明确有限的教材结构判据结果。

预检结果内含不带原文的 `review_case_template`。`book-review-package` 接收该预检 JSON、同一份源 DOCX，以及独立的 `decisions.json`（必须为每个 candidate_id 恰好提供一个 `acknowledged`、`deferred` 或 `rejected` 选择），再复算源 SHA-256、递归规范化的事件哈希链与逐项决定绑定，输出 **advisory-only** 审阅包。它从不将“已阅”解释为接受、审批、签名或身份验证，也不产生修改后的文档。

## 明确边界

- ZIP/DOCX 预检不是病毒扫描、Office 渲染验证或排版/印刷验收。
- 教材判据仅检查此包列出的标题/项目结构信号，不能判断事实正确性、版权、教学质量或交付资格。
- 完整性验证只证明相对记录案例的自洽，不能替代签名、保管链或对恶意持有人防篡改。

## 验证

```powershell
node selfcheck.mjs
```

自检只在临时目录构造合成 DOCX/案例，覆盖成功、坏输入、审阅成功、错误案例和链篡改。
