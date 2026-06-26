# Dune Query Registry

本文件登记 skill 允许调用的全部 Dune query。**LLM 不得创建新的 Dune query**，只能调用此处登记的固定 URL。

如果分析过程发现需要的 query 类型不在本表中，应在 `next_query_plan` 表中提出请求，由人工在 Dune 上保存后回填。

---

## 用法说明

每条 query 在 Dune 上保存一次后会得到永久 URL `https://dune.com/queries/<编号>`。
通过 Dune Python SDK 调用时只需传 query_id 和参数。
SQL 模板存在本文件中作为参考；实际执行时以 Dune 上的 SQL 为准。

---

## Q1: logs_by_hash

**用途**：根据 tx_hash 列表拉取完整 log 序列，用于 Phase 1 模式发现和 Phase 2 模式验证

**Dune URL**: `https://dune.com/queries/__FILL_ME__`
**Query ID**: `__FILL_ME__`

**参数**：
- `tx_hashes` (Text): 逗号分隔的 tx_hash 列表，例 `0xabc..., 0xdef...`

**SQL**：
```sql
SELECT
    tx_hash, index AS log_index,
    contract_address, topic0, topic1, topic2, topic3,
    data, block_time, block_number
FROM polygon.logs
WHERE tx_hash IN ({{tx_hashes}})
ORDER BY tx_hash, index
```

---

## Q2: address_panorama

**用途**：种子地址的全景统计（slot, contract, topic0 维度）

**Dune URL**: `https://dune.com/queries/__FILL_ME__`
**Query ID**: `__FILL_ME__`

**参数**：
- `address` (Text): 种子地址 `0x...`

**SQL**：略，参考前述 SKILL 之前迭代的 panorama 模板

---

## Q3: pattern_signature_search

**用途**：根据 (contract + topic0) 序列查找匹配该 pattern 的 tx_hash，用于 Phase 2 验证

**Dune URL**: `https://dune.com/queries/__FILL_ME__`
**Query ID**: `__FILL_ME__`

**参数**：
- `contract_addresses` (Text): 逗号分隔的合约地址（pattern 涉及的合约）
- `topic0_list` (Text): 逗号分隔的 topic0 列表
- `block_time_start` (Text): 起始时间 `2023-06-01`

**SQL**（实现方案 A：宽匹配）：
```sql
-- 找出所有同时包含全部 (contract, topic0) 组合的 tx_hash
WITH hits AS (
    SELECT tx_hash, contract_address, topic0
    FROM polygon.logs
    WHERE contract_address IN ({{contract_addresses}})
      AND topic0 IN ({{topic0_list}})
      AND block_time > TIMESTAMP '{{block_time_start}}'
),
agg AS (
    SELECT tx_hash, COUNT(DISTINCT (contract_address, topic0)) AS combo_count
    FROM hits
    GROUP BY tx_hash
)
SELECT tx_hash FROM agg
WHERE combo_count >= {{min_combo_count}}
ORDER BY tx_hash DESC
LIMIT 100
```
注：这里是宽匹配，不验证 step 顺序。Python 端拿到 tx_hash 后用 Q1 拉完整 log 再做严格匹配。

---

## Q4: pairwise_flow

**用途**：已知地址两两之间的 ERC20 转账流量统计，用于 Phase 4 边聚合

**Dune URL**: `https://dune.com/queries/__FILL_ME__`
**Query ID**: `__FILL_ME__`

**参数**：
- `address_list` (Text): 逗号分隔的地址（普通格式 0x...）
- `block_time_start` (Text)

**SQL**：
```sql
WITH known AS (
    SELECT
        from_hex(LOWER(SUBSTR(addr, 3))) AS addr_raw,
        from_hex(LOWER(CONCAT('000000000000000000000000', SUBSTR(addr, 3)))) AS addr_padded
    FROM (
        SELECT UNNEST(SPLIT_BY_STRING('{{address_list}}', ',')) AS addr
    ) t
)
SELECT
    '0x' || SUBSTR(LOWER(TO_HEX(l.topic1)), 25) AS from_addr,
    '0x' || SUBSTR(LOWER(TO_HEX(l.topic2)), 25) AS to_addr,
    l.contract_address AS token_contract,
    COUNT(*) AS transfer_count,
    SUM(bytearray_to_uint256(l.data)) AS total_amount_raw,
    MIN(l.block_time) AS first_seen,
    MAX(l.block_time) AS last_seen,
    MIN(l.tx_hash) AS sample_tx
FROM polygon.logs l
WHERE l.topic0 = 0xddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef  -- Transfer
  AND l.topic1 IN (SELECT addr_padded FROM known)
  AND l.topic2 IN (SELECT addr_padded FROM known)
  AND l.block_time > TIMESTAMP '{{block_time_start}}'
GROUP BY l.topic1, l.topic2, l.contract_address
ORDER BY transfer_count DESC
LIMIT 5000
```

---

## Q5: external_inflow

**用途**：从非已知地址流入已知地址的资金（受害者投入）

**Dune URL**: `https://dune.com/queries/__FILL_ME__`
**Query ID**: `__FILL_ME__`

**参数**：
- `address_list` (Text)
- `block_time_start` (Text)

**SQL**：
```sql
WITH known AS (
    SELECT from_hex(LOWER(CONCAT('000000000000000000000000', SUBSTR(addr, 3)))) AS addr_padded
    FROM (SELECT UNNEST(SPLIT_BY_STRING('{{address_list}}', ',')) AS addr) t
)
SELECT
    '0x' || SUBSTR(LOWER(TO_HEX(l.topic1)), 25) AS from_external,
    '0x' || SUBSTR(LOWER(TO_HEX(l.topic2)), 25) AS to_known,
    l.contract_address AS token_contract,
    COUNT(*) AS transfer_count,
    SUM(bytearray_to_uint256(l.data)) AS total_amount_raw,
    MIN(l.block_time) AS first_seen,
    MAX(l.block_time) AS last_seen
FROM polygon.logs l
WHERE l.topic0 = 0xddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef
  AND l.topic2 IN (SELECT addr_padded FROM known)
  AND l.topic1 NOT IN (SELECT addr_padded FROM known)
  AND l.block_time > TIMESTAMP '{{block_time_start}}'
GROUP BY l.topic1, l.topic2, l.contract_address
ORDER BY transfer_count DESC
LIMIT 5000
```

**重要 token 过滤**：可在 SQL 中加 `AND l.contract_address IN (DAI, USDC, USDT, WMATIC, WBTC, WETH)` 限制只统计稳定币和主流币（这是真实"victim_inflow"的金额来源）。

---

## Q6: external_outflow

**用途**：从已知地址流向非已知地址的资金（用户提取 + 团队提取）

**Dune URL**: `https://dune.com/queries/__FILL_ME__`
**Query ID**: `__FILL_ME__`

**参数**：与 Q5 相同

**SQL**：
```sql
WITH known AS (
    SELECT from_hex(LOWER(CONCAT('000000000000000000000000', SUBSTR(addr, 3)))) AS addr_padded
    FROM (SELECT UNNEST(SPLIT_BY_STRING('{{address_list}}', ',')) AS addr) t
)
SELECT
    '0x' || SUBSTR(LOWER(TO_HEX(l.topic1)), 25) AS from_known,
    '0x' || SUBSTR(LOWER(TO_HEX(l.topic2)), 25) AS to_external,
    l.contract_address AS token_contract,
    COUNT(*) AS transfer_count,
    SUM(bytearray_to_uint256(l.data)) AS total_amount_raw,
    MIN(l.block_time) AS first_seen,
    MAX(l.block_time) AS last_seen
FROM polygon.logs l
WHERE l.topic0 = 0xddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef
  AND l.topic1 IN (SELECT addr_padded FROM known)
  AND l.topic2 NOT IN (SELECT addr_padded FROM known)
  AND l.block_time > TIMESTAMP '{{block_time_start}}'
GROUP BY l.topic1, l.topic2, l.contract_address
ORDER BY transfer_count DESC
LIMIT 5000
```

---

## 调用约定

所有 query 调用通过 Dune Python SDK 进行：
```python
from dune_client.client import DuneClient
from dune_client.query import QueryBase
from dune_client.types import QueryParameter

q = QueryBase(
    query_id=<query_id>,
    params=[QueryParameter.text_type("name", value), ...],
)
result = dune.run_query(q)
```

注意：Dune query 的参数 widget 必须在 Dune 网页上手动建好，**不能在 SQL 文本里直接定义默认值**。否则会报 `'default value' is not a valid TIMESTAMP literal` 之类错误。

---

## Q7: POLY_PANO (Address Panorama with Custom Events)

**用途**：种子地址的全景统计，包含标准 ERC20 + 自定义事件（Staked, EpochBegin, RebaseAmount, Distributed）

**Dune URL**: `https://dune.com/queries/7450354`
**Query ID**: `7450354`

**参数**：
- `start_time` (Text): 起始时间 `2024-09-01`
- `end_time` (Text): 结束时间 `2024-10-01`
- `tx_hashes` (Text): 逗号分隔的 tx_hash 列表（可选，为空时查全时间段）
- `core_assets` (Text): 核心资产地址列表（sLGNS, USDC 等）
- `seed_assets` (Text): 种子地址列表

**输出**：
- slot: topic 位置（topic1_from, topic2_to, emitter 等）
- contract_address: 合约地址
- topic0: 事件签名
- event_name: 事件名称
- event_count: 事件总数
- tx_count: 交易数
- distinct_counterparty: 不同对手方数
- first_seen / last_seen: 时间范围
- sample_tx: 样本交易
- is_undecoded: 是否未解码

---

## Q8: POLY_LOGS (Raw Logs with Amount Extraction)

**用途**：根据 tx_hash 和 topic0 列表拉取原始 log，包含 amount 字段解析

**Dune URL**: `https://dune.com/queries/7450838`
**Query ID**: `7450838`

**参数**：
- `start_time` (Text): 起始时间
- `end_time` (Text): 结束时间
- `tx_hashes` (Text): 逗号分隔的 tx_hash 列表

**输出**：
- tx_hash, log_index, block_time, block_number
- contract_address, topic0, topic1, topic2, topic3
- data (原始 hex)
- amount (从 data 解析的 uint256，仅对 Transfer/Staked/RebaseAmount 有效)
- tx_from, tx_to

---

## 添加新 query 的流程

当 skill 在分析中发现需要新类型的 query：

1. 在 `next_query_plan` 表中输出条目，包含：
   - 计划的 query 名称（Q7, Q8...）
   - 用途说明
   - 期望的 SQL 大纲
   - 期望的参数

2. 用户审核后，把 SQL 贴到 Dune 创建 query

3. 把 query_id 和 URL 回填到本文件对应位置

4. skill 才能调用新 query

**禁止跳过这个流程在运行时动态构造 SQL**。
