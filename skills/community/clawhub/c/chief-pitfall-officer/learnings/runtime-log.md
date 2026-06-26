# 运行时日志 (Runtime Log)

每次 Skill 执行后自动追加记录。这是自进化闭环的原始数据入口（L7 Monitor）。

---

## 日志格式

每条记录包含以下字段：

| 字段 | 说明 | 示例 |
| :--- | :--- | :--- |
| `timestamp` | 执行时间 | 2026-06-12 |
| `industry` | 识别的行业 | 餐饮/直播/城市更新/... |
| `scenario` | 场景摘要 | 200㎡火锅店装修防坑 |
| `modules_used` | 实际加载的参考文件 | pricing-database, catering |
| `risk_hits` | 命中的风险预警数 | 5 |
| `risk_misses` | 用户反馈的遗漏风险 | "没提到消防通道宽度要求" |
| `user_feedback` | 用户显式反馈（如有） | "方案很实用" / "报价审计太粗糙" |
| `price_accuracy` | 报价建议与实际偏差 | ±10% / 偏高 / 偏低 / 未知 |
| `regulation_changes` | 用户提及的法规变化 | "2026年新食品安全标准" |

---

## 日志记录

<!-- 以下为示例种子，实际使用时由 Skill 在每次执行结束后自动追加 -->

| timestamp | industry | scenario | modules_used | risk_hits | risk_misses | user_feedback | price_accuracy | regulation_changes |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 2026-06-14 | 餐饮 | 200㎡火锅店装修，预算50万 | pricing-database, catering, acceptance-standards, legal-financial-audit | 7 | 消防通道宽度要求未覆盖 | "实际装修价格 1800 元/㎡，和你说的 1200-1500 不一样"；"乙方用了新套路：先低价中标再通过增项加价" | 偏低（实际偏高20%） | — |
| 2026-06-12 | 餐饮 | 200㎡火锅店装修，预算50万 | pricing-database, catering | 5 | — | — | — | — |
| 2026-06-12 | 直播 | 品牌直播间搭建，预算30万 | pricing-database, livestream, participant-risk-map | 4 | — | — | — | — |
