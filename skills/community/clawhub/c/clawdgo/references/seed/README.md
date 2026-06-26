# ClawdGo 首次唤醒种子文件

首次用户发送 `clawdgo` 时，若检测到 soul.md 锚点和 runtime/clawdgo-profile.json 均不存在，SKILL.md 的 bootstrap 流程会自动注入这两个文件，无需手动操作。

## 文件说明

| 文件 | 触发时写入位置 | 说明 |
|------|--------------|------|
| `soul-init.md` | soul.md 锚点区 | 10 条初始安全公理 |
| `clawdgo-profile-init.json` | runtime/clawdgo-profile.json | 完整初始训练档案 |

## 初始档案概览

- 训练场次：47 场，覆盖全部 3 层 12 维度
- 平均分：81.3（A 段位 · 硬壳龙虾）
- 安全公理：10 条，覆盖提示词注入、内存投毒、供应链、凭证保护、钓鱼、社工、公共 WiFi、数据安全、内部威胁、应急响应
- 弱项：O4（安全上网）/ E3（内部威胁）/ S3（供应链辨识），用户训练后会动态更新

## 触发条件与幂等性

- 触发条件：`runtime/clawdgo-profile.json` 不存在 **且** soul.md 中没有 `<!-- clawdgo-profile-start -->` 锚点
- 幂等：只要其中一个已存在，不再写入，不覆盖用户数据
