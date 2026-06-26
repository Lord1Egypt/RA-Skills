# SQL 模板库 — ads-case-analyzer

## 变量说明
- `{start_date}` / `{end_date}`：格式 `YYYYMMDD`（等于分区字段 `dtm` 的格式）
- `{id_filter}`：根据输入替换为以下之一：
  - `advertiser_id = '123456'`
  - `campaign_id IN (111, 222)`
  - `brand_account_id = 'xxx'`（注意：部分表无此字段，需先 join 到 advertiser_id）
- `{optimize_target_filter}`：可选，完整条件，如 `AND optimize_target IN (61, 64)`
- `{optimize_target_list}`：仅值列表，用于 S1-x 场景，如 `61, 64`（无 AND 前缀）

> **分区字段统一说明**：所有模板分区字段均为 `dtm`（格式 `YYYYMMDD`），无 `date_` 或 `dt` 字段。`bidding_pivot_trace_log_*` 和 `bidding_cube_trace_log_hourly` 有独立小时字段 `hh`。

---

## T1：大盘日粒度（分场域 + 分优化目标）

> 默认不拆平台。用户要求拆 iOS/Android 时，在 SELECT 和 GROUP BY 中加入 `platform`。
> **注意**：分区字段为 `dtm`（格式 `YYYYMMDD`），表中无 `date_` 字段。

```sql
SELECT
    dtm,
    placement,
    -- platform,  -- 拆平台时取消注释
    optimize_target,
    constraint_type,
    SUM(imp_cnt)                                                              AS imp_cnt,
    SUM(click_cnt)                                                            AS click_cnt,
    ROUND(SUM(fee) / 100.0, 2)                                               AS fee_yuan,
    ROUND(SUM(advv), 2)                                                       AS advv,
    SUM(app_activate_cnt)                                                     AS activate_cnt,
    SUM(retention_1d_cnt)                                                     AS retention_1d_cnt,
    SUM(app_pay_cnt)                                                          AS pay_cnt,
    ROUND(SUM(app_pay) / 100.0, 2)                                            AS pay_amount,
    SUM(mini_apps_payment_cnt)                                                AS mini_pay_cnt,
    ROUND(SUM(mini_apps_pay_amount) / 100.0, 2)                              AS mini_pay_amount,
    -- 效率指标
    ROUND(SUM(click_cnt) / NULLIF(SUM(imp_cnt), 0) * 100, 4)                AS ctr_pct,
    ROUND(SUM(app_activate_cnt) / NULLIF(SUM(click_cnt), 0) * 100, 4)       AS cvr_pct,
    ROUND(SUM(fee) / NULLIF(SUM(app_activate_cnt), 0) / 100.0, 2)           AS cpa_activate,
    ROUND(SUM(retention_1d_cnt) / NULLIF(SUM(app_activate_cnt), 0) * 100, 2) AS retention_rate_pct,
    ROUND(SUM(advv) / NULLIF(SUM(fee), 0), 4)                               AS roi,
    -- 预估转化率（均值）
    ROUND(AVG(ori_pcvr) * 100, 4)             AS avg_ori_pcvr_pct,
    ROUND(AVG(pcvr) * 100, 4)                 AS avg_pcvr_pct,
    ROUND(AVG(constraint_type_pcvr) * 100, 4) AS avg_constraint_pcvr_pct,
    ROUND(AVG(cali_pcvr) * 100, 4)            AS avg_cali_pcvr_pct
FROM ads_data_common.dws_ad_full_log_trackid_di
WHERE dtm BETWEEN '{start_date}' AND '{end_date}'
  AND {id_filter}
  {optimize_target_filter}
GROUP BY dtm, placement, optimize_target, constraint_type
  -- , platform  -- 拆平台时取消注释
ORDER BY dtm, placement
```

---

## T2：按输入粒度汇总（不主动下钻）

> 规则：输入什么维度就聚合到下一层，有进一步诉求再交互。
> - 输入 `brand_account_id` → GROUP BY `advertiser_id`
> - 输入 `advertiser_id` → GROUP BY `campaign_id`
> - 输入 `campaign_id` → GROUP BY `ad_id`

```sql
-- 示例：输入 advertiser_id，按 campaign_id 汇总
SELECT
    dtm,
    campaign_id,
    placement,
    SUM(imp_cnt)                                                         AS imp_cnt,
    SUM(click_cnt)                                                       AS click_cnt,
    ROUND(SUM(fee) / 100.0, 2)                                          AS fee_yuan,
    SUM(app_activate_cnt)                                                AS activate_cnt,
    ROUND(SUM(fee) / NULLIF(SUM(app_activate_cnt), 0) / 100.0, 2)      AS cpa_activate,
    SUM(retention_1d_cnt)                                                AS retention_1d_cnt,
    ROUND(SUM(retention_1d_cnt) / NULLIF(SUM(app_activate_cnt), 0) * 100, 2) AS retention_rate_pct,
    ROUND(SUM(advv), 2)                                                  AS advv,
    ROUND(SUM(advv) / NULLIF(SUM(fee), 0), 4)                          AS roi
FROM ads_data_common.dws_ad_full_log_trackid_di
WHERE dtm BETWEEN '{start_date}' AND '{end_date}'
  AND {id_filter}
  {optimize_target_filter}
GROUP BY dtm, campaign_id, placement  -- 按需替换为 ad_id 或 advertiser_id
ORDER BY SUM(fee) DESC
LIMIT 100
```

---

## T3：离线出价参数日粒度（bidding_cube_trace_log_hourly）

> **注意**：分区字段为 `dtm`（格式 `YYYYMMDD`），无 `dt` 字段；小时存在 `hh` 字段。`metric` 是 `MAP<STRING, DOUBLE>`，直接用 `metric['key']` 访问，无需 CAST。

```sql
SELECT
    dtm,
    advertiser_id,
    campaign_id,
    COUNT(*)                                                                   AS record_cnt,
    ROUND(AVG(metric['bid_ratio']), 4)                                        AS avg_bid_ratio,
    ROUND(AVG(metric['given_cpa']) / 100.0, 2)                               AS avg_given_cpa,
    ROUND(AVG(metric['cpa_bid']) / 100.0, 2)                                 AS avg_cpa_bid,
    ROUND(AVG(metric['subsidy_ratio']), 4)                                    AS avg_subsidy_ratio,
    ROUND(AVG(metric['prescreen_bid']), 4)                                    AS avg_prescreen_bid,
    -- 有效出价 = given_cpa × bid_ratio（分）
    ROUND(AVG(metric['given_cpa'] * metric['bid_ratio']) / 100.0, 2)         AS avg_effective_cpa_bid
FROM hive_prod.ads_data_common.bidding_cube_trace_log_hourly
WHERE dtm BETWEEN '{start_date}' AND '{end_date}'
  AND context = 'app_ocpx'
  AND bucket = 'default'
  AND {id_filter}
GROUP BY dtm, advertiser_id, campaign_id
ORDER BY dtm, campaign_id
```

---

## T4：在线出价参数日粒度 — 展示场域

> **注意**：无 `ts` 字段，分区字段为 `dtm`（格式 `YYYYMMDD`）+ `hh`（小时）。`bid_param`/`bid_req` 是 `MAP<STRING, DOUBLE>`，用 `['key']` 访问，禁止 `get_json_object`。

```sql
SELECT
    dtm,
    campaign_id,
    COUNT(*)                                                                   AS request_cnt,
    ROUND(AVG(bid_param['cpaBid']) / 100.0, 2)                               AS avg_cpa_bid_online,
    ROUND(AVG(bid_param['cpaBidRatio']), 4)                                   AS avg_bid_ratio_online,
    ROUND(AVG(bid_param['subsidyRatio']), 4)                                  AS avg_subsidy_ratio,
    ROUND(AVG(bid_req['pcvr']) * 100, 4)                                      AS avg_pcvr_pct,
    ROUND(AVG(bid_req['pConsCvr']) * 100, 4)                                  AS avg_pcons_cvr_pct,
    ROUND(AVG(bid_req['pctr']) * 100, 4)                                      AS avg_pctr_pct,
    ROUND(AVG(bid_req['pgmv']), 4)                                            AS avg_pgmv
FROM hive_prod.ads_data_common.bidding_pivot_trace_log_feed
WHERE dtm BETWEEN '{start_date}' AND '{end_date}'
  AND {id_filter}
GROUP BY dtm, campaign_id
ORDER BY dtm
```

---

## T4b：在线出价参数日粒度 — 搜索场域

> 同 T4，表换为 `bidding_pivot_trace_log_search`，字段结构相同。

```sql
SELECT
    dtm,
    campaign_id,
    COUNT(*)                                                                   AS request_cnt,
    ROUND(AVG(bid_param['cpaBid']) / 100.0, 2)                               AS avg_cpa_bid_online,
    ROUND(AVG(bid_param['cpaBidRatio']), 4)                                   AS avg_bid_ratio_online,
    ROUND(AVG(bid_param['subsidyRatio']), 4)                                  AS avg_subsidy_ratio,
    ROUND(AVG(bid_req['pcvr']) * 100, 4)                                      AS avg_pcvr_pct,
    ROUND(AVG(bid_req['pConsCvr']) * 100, 4)                                  AS avg_pcons_cvr_pct,
    ROUND(AVG(bid_req['pctr']) * 100, 4)                                      AS avg_pctr_pct,
    ROUND(AVG(bid_req['pgmv']), 4)                                            AS avg_pgmv
FROM hive_prod.ads_data_common.bidding_pivot_trace_log_search
WHERE dtm BETWEEN '{start_date}' AND '{end_date}'
  AND {id_filter}
GROUP BY dtm, campaign_id
ORDER BY dtm
```

---

## T5：pcvr 偏差专项（ori vs cali vs 实际 cvr）

```sql
SELECT
    dtm,
    placement,
    -- 预估 vs 实际转化率对比
    ROUND(AVG(ori_pcvr) * 100, 4)                                            AS avg_ori_pcvr_pct,
    ROUND(AVG(cali_pcvr) * 100, 4)                                           AS avg_cali_pcvr_pct,
    ROUND(AVG(pcvr) * 100, 4)                                                AS avg_pcvr_pct,
    ROUND(AVG(ori_constraint_type_pcvr) * 100, 4)                           AS avg_ori_cons_pcvr_pct,
    ROUND(AVG(constraint_cali_pcvr) * 100, 4)                               AS avg_cons_cali_pcvr_pct,
    ROUND(AVG(constraint_type_pcvr) * 100, 4)                               AS avg_cons_pcvr_pct,
    -- 实际转化率
    ROUND(SUM(app_activate_cnt) / NULLIF(SUM(click_cnt), 0) * 100, 4)       AS actual_activate_cvr_pct,
    -- 偏差比（预估/实际，>1 表示高估，<1 表示低估）
    ROUND(AVG(pcvr) / NULLIF(SUM(app_activate_cnt) / NULLIF(SUM(click_cnt), 0), 0), 3) AS pcvr_bias_ratio
FROM ads_data_common.dws_ad_full_log_trackid_di
WHERE dtm BETWEEN '{start_date}' AND '{end_date}'
  AND {id_filter}
  {optimize_target_filter}
GROUP BY dtm, placement
ORDER BY dtm, placement
```

---

## T6：次留专项

```sql
SELECT
    dtm,
    placement,
    SUM(app_activate_cnt)                                                         AS activate_cnt,
    SUM(retention_1d_cnt)                                                         AS retention_1d_cnt,
    ROUND(SUM(retention_1d_cnt) / NULLIF(SUM(app_activate_cnt), 0) * 100, 2)    AS retention_rate_pct,
    ROUND(SUM(fee) / NULLIF(SUM(retention_1d_cnt), 0) / 100.0, 2)               AS cpa_retention,
    ROUND(AVG(ori_pcvr) * 100, 4)                                                AS avg_ori_pcvr_pct,
    ROUND(AVG(pcvr) * 100, 4)                                                    AS avg_pcvr_pct
FROM ads_data_common.dws_ad_full_log_trackid_di
WHERE dtm BETWEEN '{start_date}' AND '{end_date}'
  AND {id_filter}
  AND optimize_target IN (61)  -- 次留目标计划
GROUP BY dtm, placement
ORDER BY dtm
```

---

## 场景一：超成本专项

### S1-1：PAOA 日粒度（by constraint_type + placement）

> PAOA = 预估转化 / 实际转化，目标值 = 1
> - placement IN (1,2)：预估转化 = SUM(constraint_type_pcvr × click_cnt)
> - placement = 7（内流）：预估转化 = SUM(constraint_type_pcvr × imp_cnt)
> - 实际转化字段根据 constraint_type 映射（见 constraint_type_mapping.md）

```sql
SELECT
    dtm,
    placement,
    optimize_target,
    constraint_type,
    -- 预估转化（分 placement 计算）
    SUM(CASE
        WHEN placement IN (1, 2) THEN constraint_type_pcvr * click_cnt
        WHEN placement = 7       THEN constraint_type_pcvr * imp_cnt
        ELSE 0
    END)                                                                      AS pred_convert_cnt,
    -- 实际转化（按 constraint_type 选字段，此处以 61=激活为例，实际使用时替换）
    SUM(CASE constraint_type
        WHEN 60 THEN app_download_button_click_cnt
        WHEN 61 THEN app_activate_cnt
        WHEN 62 THEN app_register_cnt
        WHEN 63 THEN app_key_action_cnt
        WHEN 64 THEN app_pay_cnt
        WHEN 65 THEN app_invoke_cnt
        WHEN 67 THEN mini_apps_payment_cnt
        WHEN 69 THEN app_subscribe_button_click_cnt
        WHEN 72 THEN leads_cnt
        WHEN 73 THEN app_invoke_cnt
        WHEN 74 THEN app_activate_cnt
        WHEN 75 THEN app_payment_cnt
        ELSE NULL
    END)                                                                      AS actual_convert_cnt,
    -- PAOA
    ROUND(
        SUM(CASE
            WHEN placement IN (1, 2) THEN constraint_type_pcvr * click_cnt
            WHEN placement = 7       THEN constraint_type_pcvr * imp_cnt
            ELSE 0
        END)
        / NULLIF(SUM(CASE constraint_type
            WHEN 60 THEN app_download_button_click_cnt
            WHEN 61 THEN app_activate_cnt
            WHEN 62 THEN app_register_cnt
            WHEN 63 THEN app_key_action_cnt
            WHEN 64 THEN app_pay_cnt
            WHEN 65 THEN app_invoke_cnt
            WHEN 67 THEN mini_apps_payment_cnt
            WHEN 69 THEN app_subscribe_button_click_cnt
            WHEN 72 THEN leads_cnt
            WHEN 73 THEN app_invoke_cnt
            WHEN 74 THEN app_activate_cnt
            WHEN 75 THEN app_payment_cnt
            ELSE NULL
        END), 0)
    , 4)                                                                      AS paoa,
    -- 辅助指标
    SUM(imp_cnt)                                                              AS imp_cnt,
    SUM(click_cnt)                                                            AS click_cnt,
    ROUND(SUM(fee) / 100.0, 2)                                               AS fee_yuan,
    ROUND(AVG(ori_constraint_type_pcvr) * 100, 4)                           AS avg_ori_cons_pcvr_pct,
    ROUND(AVG(constraint_cali_pcvr) * 100, 4)                               AS avg_cons_cali_pcvr_pct,
    ROUND(AVG(constraint_type_pcvr) * 100, 4)                               AS avg_cons_pcvr_pct
FROM ads_data_common.dws_ad_full_log_trackid_di
WHERE dtm BETWEEN '{start_date}' AND '{end_date}'
  AND {id_filter}
  AND optimize_target IN ({optimize_target_list})  -- 必须同时过滤 optimize_target 防止字段重叠；格式：61, 64
GROUP BY dtm, placement, optimize_target, constraint_type
ORDER BY dtm, placement
```

### S1-2：PAOA 根因拆解 — ori_pcvr vs cali_pcvr vs 实际

> 判断超成本是模型原始预估偏高、校准放大，还是人群/素材质量问题

```sql
SELECT
    dtm,
    placement,
    constraint_type,
    -- 预估转化率三层拆解
    ROUND(AVG(ori_constraint_type_pcvr) * 100, 4)   AS avg_ori_cons_pcvr_pct,    -- 原始模型预估
    ROUND(AVG(constraint_cali_pcvr) * 100, 4)        AS avg_cons_cali_pcvr_pct,   -- 校准后
    ROUND(AVG(constraint_type_pcvr) * 100, 4)        AS avg_final_cons_pcvr_pct,  -- 最终用于出价的
    -- 实际转化率（实际转化 / 点击）
    ROUND(SUM(CASE constraint_type
        WHEN 60 THEN app_download_button_click_cnt
        WHEN 61 THEN app_activate_cnt
        WHEN 62 THEN app_register_cnt
        WHEN 63 THEN app_key_action_cnt
        WHEN 64 THEN app_pay_cnt
        WHEN 65 THEN app_invoke_cnt
        WHEN 67 THEN mini_apps_payment_cnt
        WHEN 69 THEN app_subscribe_button_click_cnt
        WHEN 72 THEN leads_cnt
        WHEN 73 THEN app_invoke_cnt
        WHEN 74 THEN app_activate_cnt
        WHEN 75 THEN app_payment_cnt
        ELSE NULL
    END) / NULLIF(SUM(click_cnt), 0) * 100, 4)      AS actual_cvr_pct,
    -- 校准倍率：cali / ori（>1 表示校准放大了预估）
    ROUND(AVG(constraint_cali_pcvr) / NULLIF(AVG(ori_constraint_type_pcvr), 0), 3) AS cali_multiplier,
    -- 预估偏差：final_pcvr / actual_cvr（>1 表示高估）
    ROUND(AVG(constraint_type_pcvr) / NULLIF(
        SUM(CASE constraint_type
            WHEN 60 THEN app_download_button_click_cnt
            WHEN 61 THEN app_activate_cnt
            WHEN 62 THEN app_register_cnt
            WHEN 63 THEN app_key_action_cnt
            WHEN 64 THEN app_pay_cnt
            WHEN 65 THEN app_invoke_cnt
            WHEN 67 THEN mini_apps_payment_cnt
            WHEN 69 THEN app_subscribe_button_click_cnt
            WHEN 72 THEN leads_cnt
            WHEN 73 THEN app_invoke_cnt
            WHEN 74 THEN app_activate_cnt
            WHEN 75 THEN app_payment_cnt
            ELSE NULL
        END) / NULLIF(SUM(click_cnt), 0)
    , 0), 3)                                          AS pcvr_bias_ratio
FROM ads_data_common.dws_ad_full_log_trackid_di
WHERE dtm BETWEEN '{start_date}' AND '{end_date}'
  AND {id_filter}
  AND optimize_target IN ({optimize_target_list})
GROUP BY dtm, placement, constraint_type
ORDER BY dtm, placement
```

---

## 场景二：掉量专项

### S2-1：出价链路日粒度趋势

> 出价链路：given_cpa × bid_ratio × subsidy_ratio = 系统有效CPA出价
> 掉量时优先看：① bid_ratio 是否下调 ② given_cpa 是否变化 ③ subsidy_ratio 是否缩扣

```sql
SELECT
    dtm,
    campaign_id,
    ROUND(AVG(metric['given_cpa']) / 100.0, 2)                                  AS avg_given_cpa,
    ROUND(AVG(metric['bid_ratio']), 4)                                           AS avg_bid_ratio,
    ROUND(AVG(metric['cpa_bid']) / 100.0, 2)                                    AS avg_cpa_bid,
    ROUND(AVG(metric['subsidy_ratio']), 4)                                       AS avg_subsidy_ratio,
    ROUND(AVG(metric['prescreen_bid']), 4)                                       AS avg_prescreen_bid,
    -- 有效出价 = given_cpa × bid_ratio
    ROUND(AVG(metric['given_cpa'] * metric['bid_ratio']) / 100.0, 2)           AS avg_effective_cpa,
    COUNT(*)                                                                     AS record_cnt
FROM hive_prod.ads_data_common.bidding_cube_trace_log_hourly
WHERE dtm BETWEEN '{start_date}' AND '{end_date}'
  AND context = 'app_ocpx'
  AND bucket = 'default'
  AND {id_filter}
GROUP BY dtm, campaign_id
ORDER BY dtm, campaign_id
```

### S2-2：在线预估分趋势（展示场域）

> 掉量时看 pcvr/pctr 是否下降（影响 ecpm = cpaBid × pConsCvr × pctr）
> subsidyRatio < 1 表示过收缩扣，会压低实际出价
> **注意**：`bid_param`/`bid_req` 是 `MAP<STRING, DOUBLE>`，用 `['key']` 直接访问。

```sql
SELECT
    dtm,
    campaign_id,
    COUNT(*)                                                                      AS request_cnt,
    ROUND(AVG(bid_param['cpaBid']) / 100.0, 2)                                  AS avg_cpa_bid_online,
    ROUND(AVG(bid_param['cpaBidRatio']), 4)                                      AS avg_bid_ratio_online,
    ROUND(AVG(bid_param['subsidyRatio']), 4)                                     AS avg_subsidy_ratio,
    ROUND(AVG(bid_req['pcvr']) * 100, 4)                                         AS avg_pcvr_pct,
    ROUND(AVG(bid_req['pConsCvr']) * 100, 4)                                     AS avg_pcons_cvr_pct,
    ROUND(AVG(bid_req['pctr']) * 100, 4)                                         AS avg_pctr_pct,
    ROUND(AVG(bid_req['pgmv']), 4)                                               AS avg_pgmv,
    -- 估算 ecpm = cpaBid × pConsCvr × pctr × 1000（单位：分 × 1000）
    ROUND(AVG(
        bid_param['cpaBid']
        * bid_req['pConsCvr']
        * bid_req['pctr']
        * 1000
    ), 4)                                                                         AS avg_est_ecpm
FROM hive_prod.ads_data_common.bidding_pivot_trace_log_feed
WHERE dtm BETWEEN '{start_date}' AND '{end_date}'
  AND {id_filter}
GROUP BY dtm, campaign_id
ORDER BY dtm
```

### S2-3：掉量根因判断逻辑

> 不需要 SQL，LLM 推理时按以下优先级判断：

```
1. bid_ratio 下调？
   → avg_bid_ratio 趋势下降 → 校准系数收紧 → 有效出价降低 → 跑量下降
   → 看 subsidy_ratio：若同步 <1，说明平台过收在缩扣，双重压低出价

2. 预估分下降？
   → avg_pcvr / avg_pctr 趋势下降 → ecpm 降低 → 竞争力下降 → 跑量下降
   → 结合大盘 CTR/CVR 实际值判断是否是素材/人群质量问题

3. 出价绝对值不变但跑量仍下降？
   → 可能是竞争加剧（市场 ecpm 抬升）
   → 看 avg_prescreen_bid 趋势（海选价上升 = 竞争加剧）

4. 以上都正常？
   → 检查预算是否耗尽、投放时段/定向是否有变更
```
