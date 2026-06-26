---
name: claim-risk-auditor
description: 检查文案、论文、宣传稿或产品说明中的高风险断言，标出证据缺口并给出更稳妥的改写。
metadata: {"openclaw":{"emoji":"🛡️","requires":{"bins":["node","pbpaste"]}}}
---

# Claim Risk Auditor

这是一个“断言风险审计” skill。

## 主要用途

适合检查：
- 产品宣传文案
- 品牌介绍
- 招商文案
- 推广脚本
- 学术写作中的绝对化表达
- 论文讨论部分中的过度结论
- 培训课文案
- 直播口播文案

## 调用方式

当用户说：
- 读取剪贴板并检查风险表达
- 帮我找出容易翻车的断言
- 看看哪些话没有证据支撑
- 帮我改得更稳一点

你应运行：

```bash
node {baseDir}/scripts/read_clipboard.mjs