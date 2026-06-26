# Sources — akshare-router-cn

本目录用于放“数据源层”的约定：
- 选哪个网站/接口作为主源（Sina/东方财富）
- 返回结构如何做容错（字段可能变动）
- 限制与降级策略

## 一期主源选择

### 期货实时/分钟线：Sina
- 主因：AKShare 接口成熟，且可直接取分钟 period（1/5/15/30/60）
- 接口：`futures_zh_realtime`、`futures_zh_minute_sina`

### 期权 Greeks/IV：Sina
- 主因：`option_sse_greeks_sina` 已包含 IV 与 Greeks（避免自己反推）
- 接口：`option_sse_codes_sina`（拿内码列表）→ `option_sse_greeks_sina`

### 全市场期权报价：东方财富
- 用途：当用户问“全市场/某板块期权整体”时做补充
- 接口：`option_current_em`
- TODO：字段稳定性验证 + 与 Sina 内码的 crosswalk 方案

## 容错原则
1) 任何字段取值先做 `str.strip()`，数值字段 `to_numeric(errors='coerce')`
2) 对 `option_sse_greeks_sina` 的 key-value 表：必须用字典映射（字段中文可能微调）
3) 失败降级：
   - 网络/上游变更：返回“失败原因 + 已尝试接口 + 下一步建议(换源/换合约/换月份)”

> TODO：补充一张“字段中文 → 内部字段名”的映射表（例如 隐含波动率->iv）。
