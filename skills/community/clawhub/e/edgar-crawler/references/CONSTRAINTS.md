# Constraints

## preservation_manifest

```yaml
required_objects:
  business_decisions_count: 92
  fatal_constraints_count: 31
  non_fatal_constraints_count: 139
  use_cases_count: 1
  semantic_locks_count: 12
  preconditions_count: 4
  evidence_quality_rules_count: 2
  traceback_scenarios_count: 5

```

## Domain Constraints Injected (16)

- **`SHARED-DS-RL-001`** <sub>(fatal)</sub>: Rate Limit + 指数退避重试：所有外部数据 API 调用必须实施速率限制控制 和指数退避重试（Exponential Backoff with Jitter）。收到 429/503 响应后 立即重试是反模式，会加剧服务端压力并触发 IP 封禁。 最大重试次数 3-5 次，退避基数 1-2 秒，最大退避 60 秒。
- **`SHARED-DS-RL-002`** <sub>(high)</sub>: 批量 API 调用必须控制并发数（max_workers），不可无限制并行。 免费 API（akshare/tushare 免费版）通常限制为 1-3 并发； 付费 API 也有并发上限（tushare 积分制，不同积分对应不同并发）。 超出并发限制会触发 429 或 IP 封禁。推荐使用 asyncio.Semaphore 或 ThreadPoolExecutor 的 max_workers 参数显式控制。
- **`SHARED-DS-RL-003`** <sub>(high)</sub>: API Token / 凭证安全：数据源 API key（tushare token / akshare 无需 token 但 其他商业数据源需要）不可硬编码在代码中，必须通过环境变量或配置文件读取。 硬编码 token 提交到 Git 会导致 token 泄露和费用损失。
- **`SHARED-DS-RL-004`** <sub>(medium)</sub>: 请求节流（Throttling）：对同一 API 的批量请求应在请求间插入最小间隔 （akshare 部分接口要求 ≥ 0.5s；tushare 免费版每分钟 200 次）。 纯代码 sleep 不如令牌桶（Token Bucket）算法精确，推荐使用 ratelimit 或 slowapi 等成熟库。
- **`SHARED-DS-MISS-001`** <sub>(high)</sub>: 停牌日数据缺失策略：停牌股票在停牌期间无成交数据，数据库中会出现日期缺口。 缺失日期不可使用 forward-fill（会产生虚假成交量）； 应在数据库中以 is_suspended=True 标记，量和成交额填 0，价格保留前一日收盘价。 因子计算时必须过滤 is_suspended=True 的行。
- **`SHARED-DS-MISS-002`** <sub>(medium)</sub>: 新上市股票的历史数据边界：新股上市首日开始在数据库中出现，但其上市前 无历史数据。若因子计算的 lookback 期超过上市天数，会产生所有 NaN 因子值。 采集时应记录每只股票的上市日期（list_date），采集逻辑应以上市日期为起点， 不以固定开始日期。
- **`SHARED-DS-MISS-003`** <sub>(high)</sub>: 退市股票的数据完整性：已退市股票在主流数据源（akshare/tushare）中依然 可以查询历史数据（退市前的历史），但退市日期后无数据。 历史股票池构建时必须包含已退市股票（否则幸存者偏差）， 且采集时需明确处理退市日截止边界。
- **`SHARED-DS-MISS-004`** <sub>(high)</sub>: 多数据源数据对账（Cross-Source Reconciliation）：同一数据（如收盘价） 从不同数据源（akshare/tushare/baostock）获取可能存在细微差异 （不同复权方式/不同节假日处理/除息调整时间不同）。 应在 pipeline 中实施多源对账检查，差异超阈值（如 0.1%）时记录告警并人工确认。
- **`SHARED-DS-TIME-001`** <sub>(high)</sub>: 时间戳精度与类型一致性：数据库中时间戳应使用统一的数据类型 （timestamp 而非 varchar/int）。混用字符串日期（'2024-01-15'）和 Timestamp 对象是比较、索引、merge 出现细微 bug 的常见来源， 应在 pipeline 入口处强制转换。
- **`SHARED-DS-TIME-002`** <sub>(high)</sub>: 交易时间与自然时间的区分：日线数据的"日期"通常对应交易日（T日）， 而新闻/公告数据的"时间"是自然时间。合并两类数据时，必须将自然时间 映射到下一个可用交易日（next available trading day）， 否则会产生"公告在T日，但T日盘中已经可用"的 lookahead 问题。
- **`SHARED-DS-TIME-003`** <sub>(medium)</sub>: 夏令时（DST）处理：采集美股/欧洲股市数据时，夏令时切换日（3月/11月） 会导致同一 HH:MM 时刻对应不同的 UTC 时间，若未处理，当日时序数据 会出现1小时的漂移。应始终以 UTC 存储，展示时按市场本地时区转换。
- **`SHARED-DS-INCR-001`** <sub>(high)</sub>: 增量更新幂等性：数据更新脚本必须是幂等的（多次运行结果相同）。 若脚本因网络中断在中途失败，重新运行时不应产生重复数据或数据缺口。 实现方式：先写入临时表，校验后 UPSERT 到主表，不直接 INSERT/APPEND。
- **`SHARED-DS-INCR-002`** <sub>(high)</sub>: 数据完整性检验（数据校验和/行数检查）：每次数据更新后， 应对关键字段做完整性检验：行数是否在预期范围内、价格是否为正数、 日期是否连续（无缺失交易日）。缺少自动校验的数据管道是"沉默腐烂"的根源。
- **`SHARED-DS-INCR-003`** <sub>(medium)</sub>: 数据版本化：数据管道的输出数据应版本化管理（data versioning）。 当数据源更新了历史数据（如修订调整后的财务数据）， 旧版本数据应保留可追溯，不应静默覆盖，以便对比版本间差异及复现历史回测。
- **`SHARED-DS-INCR-004`** <sub>(medium)</sub>: 数据对齐到交易日历边界：采集完成后，应验证所有股票/资产的数据覆盖 完整性与交易日历的一致性。每只股票在每个交易日都应有一行数据 （停牌标记，不是缺失）。通过 pivot_table 检查 NaN 比例是有效的快速诊断手段。
- **`SHARED-DS-INCR-005`** <sub>(medium)</sub>: 缓存策略（Caching）：频繁读取的静态/低频更新数据（如股票信息、行业分类、 指数成分股）应本地缓存，避免每次运行重复 API 调用。 缓存必须设置过期时间（TTL），防止使用过期的行业分类或已失效的成分股信息。
