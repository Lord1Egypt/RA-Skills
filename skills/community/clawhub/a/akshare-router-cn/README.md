# akshare-router-cn (MVP skeleton)

这是一个 **OpenClaw skill 骨架**：围绕 AKShare 的免费数据源，对「中国期货/期权」高频问题做 **路由 + 最小可用 recipe**。

- 目标：把问题 **快速分流** 到正确的数据源/计算方法，减少“翻 AKShare 文档/函数名”的成本。
- 范围（一期）：
  - 期货：实时盘口/成交、分钟线(1/5/30m)、日线；基础技术指标（MA/EMA/MACD/RSI 等，后处理）。
  - 期权：合约列表、实时价、隐含波动率、Greeks（来源：Sina 的 `option_sse_greeks_sina` 结构化字段）。
  - RR25：基于 Delta 近似（从 greeks 接口取 delta + IV），用“最接近 ±0.25 delta 的合约”近似。

入口文件：`SKILL.md`

> 注意：本目录是 skeleton；能力/字段随上游站点变动。所有不确定处已标记 TODO。
