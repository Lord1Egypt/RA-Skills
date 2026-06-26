---
name: collab-offer-polisher
description: 把合作邀约、商务私信、品牌合作需求和合作条款草稿，改写成更专业、更容易推进合作的版本。
metadata: {"openclaw":{"emoji":"🤝","requires":{"bins":["node","pbpaste"]}}}
---

# Collab Offer Polisher

这是一个合作邀约与商务沟通优化 skill。

## 主要用途

适用于：
- 品牌合作邀约
- 场地方合作
- 摄影合作
- 达人邀约
- 甲乙方初次接洽
- 商务私信
- 简版合作方案
- 活动合作说明

## 调用方式

当用户说：
- 读取剪贴板并帮我润色合作邀约
- 帮我把这段商务私信改专业一点
- 用更容易成交的方式重写这段合作话术
- 帮我做一个更有礼貌但更清晰的合作文案

你应运行：

```bash
node {baseDir}/scripts/read_clipboard.mjs