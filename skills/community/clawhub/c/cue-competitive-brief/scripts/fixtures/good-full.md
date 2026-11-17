# 证据表（样例）

决策问题：5 人团队要不要从 A 方案换到更开放的 B 方案
来源日期：2026-10-14
工具状态：omni-reader 正常，来源为官方定价页与仓库 README 解析

| 竞品 | 维度 | 主张 | 证据级别 | 来源 | 日期 | 置信度 |
|---|---|---|---|---|---|---|
| A | 定价 | Individual 每席按月订阅，Teams 档另计 | fact | a.example.com/pricing | 2026-10-12 | 高 |
| A | 开源 | 主体闭源 | fact | a.example.com | 2026-10-12 | 高 |
| B | 定价 | 按席位月付，社区版免费 | fact | b.example.com/pricing | 2026-10-12 | 高 |
| B | 开源 | MIT 许可，主体在公开仓库 | fact | github.com/b/example | 2026-10-12 | 高 |
| C | 成熟度 | 首个正式版发布于 2025 下半年 | inference | github.com/c/example release | 2026-10 | 中 |

## 证据覆盖度

- 证据表总行数：5
- fact：4 · inference：1 · opinion：0
- 置信度高 4 · 中 1 · 低 0
- 完全覆盖：定价 · 开源
- 未覆盖：社区生态规模、企业级管控
