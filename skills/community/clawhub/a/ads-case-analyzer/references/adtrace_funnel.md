# 前链路漏斗分析 — adtrace 2.0 使用指南

## 数据源

| 场域 | 类型 | 表名 | TTL | 说明 |
|------|------|------|-----|------|
| 信息流 | ck-checkpoint | `reddw.feed_trace_ads_checkpoints` | 7天 | ck有二次采样，需还原 |
| 信息流 | ck-running info | `reddw.feed_trace_ads_running_info` | 7天 | |
| 信息流 | hive-checkpoint | `hive_prod.redcdm.dwd_ads_adtrace_log_checkpoint_rt` | 30天 | 无二次采样，推荐用于广告主粒度查询 |
| 信息流 | hive-running info | `hive_prod.redcdm.dwd_ads_adtrace_log_runninginfo_rt` | 30天 | |
| 搜索 | ck-checkpoint | `reddw.search_trace_ads_checkpoints` | 7天 | |
| 搜索 | ck-running info | `reddw.search_trace_ads_running_info` | 7天 | |
| 搜索 | hive-checkpoint | `hive_prod.redcdm.dwd_ads_adtrace_log_checkpoint_rt` | 30天 | source='search' 区分 |
| 搜索 | hive-running info | `hive_prod.redcdm.dwd_ads_adtrace_log_runninginfo_rt` | 30天 | |

> hive 表两个场域共用，通过 `source` 字段区分：`source='feed'` / `source='search'`

---

## 重要注意事项

1. **禁止直接 JOIN 两张 ck 表**（checkpoint + running_info），会造成集群崩溃
2. **生产流量必须过滤**：`request_label_bitset = 0`
3. **hive 分区字段**：`dtm`（日期）、`hh`（小时）；时间字段 `action_date`（非分区）
4. **hive 实验组判断**：`array_contains(exp_ids, 实验id)`（召回~粗排阶段 exp_ids 为 null）
5. **ck 表有二次采样**，redbi 中已还原，直接查 ck 时需注意：
   - 召回/海选/粗排阶段：5% ad 采样
   - 精排及之后：100% 采样

---

## 漏斗阶段 & 正埋点

### 信息流漏斗

| stage | 含义 | 正埋点（checkpoint） |
|-------|------|---------------------|
| `recall_ads_step` | 召回 | `fares_recall_triggered`（进入召回）<br>`fares_recall_pass_validation`（通过基础定向/刹车） |
| `pre_ranking_filter_step` | 海选 | `fares_pre_rank_pass` / `feed_pre_ranking_filter_pass`（通过海选/snake merge） |
| `first_ranking_step` | 粗排 | `fares_first_rank_pass`（通过粗排） |
| `final_ranking_step` | 精排 | `feed_final_ranking_pass`（精排打分结束） |
| `post_ranking_filter_step` | 精排后过滤 | `feed_post_ranking_filter_pass` |
| `insertion_auction_step` | 插入广告位/拍卖 | `feed_insertion_auction_pass`（fas最终返回） |
| `mixrank_step` | 混排竞得 | `feed_mixrank_pass`（2.0使用） |
| `final_step` | 最终竞得 | `feed_final_pass`（1.0使用） |

### 搜索漏斗

| stage | 含义 | 正埋点（checkpoint） |
|-------|------|---------------------|
| `recall_ads_step` | 召回 | `sares_recall_triggered`<br>`sares_recall_pass_validation` |
| `pre_ranking_filter_step` | 海选 | `sares_pre_rank_pass` |
| `first_ranking_step` | 粗排 | `sares_first_rank_pass` |
| `final_ranking_step` | 精排 | `search_final_ranking_pass` |
| `post_ranking_filter_step` | 精排后过滤 | `search_post_ranking_filter_pass` |
| `insertion_auction_step` | 插入广告位 | `search_insertion_auction_pass` |
| `final_step` | 竞得 | `search_mixrank_pass` / `search_final_pass` |

---

## 标准 SQL 模板

### F1：漏斗通过数（hive，推荐）

> 按 campaign_id 查各阶段通过数，用于定位卡在哪个阶段

```sql
SELECT
    stage,
    checkpoint,
    COUNT(*) AS pass_cnt
FROM hive_prod.redcdm.dwd_ads_adtrace_log_checkpoint_rt
WHERE dtm = '{date}'            -- 格式 YYYYMMDD
  AND source = 'feed'           -- 信息流；搜索改为 'search'
  AND request_label_bitset = 0  -- 仅生产流量，必须加
  AND CAST(is_pass AS STRING) = 'true'             -- 仅正埋点（通过），注意是 boolean 类型
  AND campaign_id = '{campaign_id}'
GROUP BY stage, checkpoint
ORDER BY pass_cnt DESC
```

> 若只有 advertiser_id：将 `campaign_id = ?` 改为 `advertiser_id = ?`

---

### F2：漏斗通过率（各阶段通过数 + 通过率）

```sql
WITH funnel AS (
    SELECT
        stage,
        COUNT(*) AS pass_cnt
    FROM hive_prod.redcdm.dwd_ads_adtrace_log_checkpoint_rt
    WHERE dtm = '{date}'
      AND source = 'feed'
      AND request_label_bitset = 0
      AND CAST(is_pass AS STRING) = 'true'
      AND campaign_id = '{campaign_id}'
      AND checkpoint IN (
          'fares_recall_pass_validation',
          'fares_pre_rank_pass',
          'fares_first_rank_pass',
          'feed_final_ranking_pass',
          'feed_post_ranking_filter_pass',
          'feed_insertion_auction_pass',
          'feed_mixrank_pass'
      )
    GROUP BY stage
)
SELECT
    stage,
    pass_cnt,
    ROUND(pass_cnt * 100.0 / MAX(pass_cnt) OVER (), 2) AS pass_rate_pct
FROM funnel
ORDER BY pass_cnt DESC
```

---

### F3：各阶段过滤原因分布

> is_pass=0 为负埋点，checkpoint 字段记录具体过滤原因

```sql
SELECT
    stage,
    checkpoint AS filter_reason,
    COUNT(*) AS filter_cnt,
    ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (PARTITION BY stage), 2) AS ratio_in_stage_pct
FROM hive_prod.redcdm.dwd_ads_adtrace_log_checkpoint_rt
WHERE dtm = '{date}'
  AND source = 'feed'
  AND request_label_bitset = 0
  AND CAST(is_pass AS STRING) = 'false'  -- 负埋点（被过滤），注意 Spark bug 必须用 CAST
  AND campaign_id = '{campaign_id}'
  AND stage = '{target_stage}'  -- 如 'pre_ranking_filter_step'（海选）
GROUP BY stage, checkpoint
ORDER BY filter_cnt DESC
LIMIT 20
```

---

### F4：多日漏斗趋势（定位哪天开始恶化）

```sql
SELECT
    dtm,
    checkpoint,
    COUNT(*) AS pass_cnt
FROM hive_prod.redcdm.dwd_ads_adtrace_log_checkpoint_rt
WHERE dtm BETWEEN '{start_date}' AND '{end_date}'
  AND source = 'feed'
  AND request_label_bitset = 0
  AND CAST(is_pass AS STRING) = 'true'
  AND campaign_id = '{campaign_id}'
  AND checkpoint IN (
      'fares_recall_pass_validation',
      'fares_pre_rank_pass',
      'fares_first_rank_pass',
      'feed_final_ranking_pass',
      'feed_mixrank_pass'
  )
GROUP BY dtm, checkpoint
ORDER BY dtm, pass_cnt DESC
```

---

### F5：running_info 精排分析（精排阶段打分分布）

> 不要 JOIN checkpoint 表，单独查 running_info

```sql
SELECT
    AVG(ecpm)     AS avg_ecpm,
    AVG(pcvr)     AS avg_pcvr,
    AVG(pctr)     AS avg_pctr,
    COUNT(*)      AS cnt
FROM hive_prod.redcdm.dwd_ads_adtrace_log_runninginfo_rt
WHERE dtm = '{date}'
  AND source = 'feed'
  AND request_label_bitset = 0
  AND campaign_id = '{campaign_id}'
  AND array_contains(stages, 'final_ranking_step')  -- 送到精排的
```

---

## 漏斗分析解读框架

```
召回（fares_recall_pass_validation）
  → 海选（fares_pre_rank_pass）          -- 海选通过率 = 海选/召回
    → 粗排（fares_first_rank_pass）       -- 粗排通过率 = 粗排/海选
      → 精排（feed_final_ranking_pass）   -- 精排通过率 = 精排/粗排
        → 精排后过滤（feed_post_ranking_filter_pass）
          → 拍卖（feed_insertion_auction_pass）
            → 混排竞得（feed_mixrank_pass）
```

**定位方法：哪个阶段通过数骤降，问题在那一层。**

| 卡在哪层 | 可能原因 | 下一步 |
|---------|---------|--------|
| 召回低 | 定向太窄、刹车触发、素材被过滤、预算不足 | 看 F3 过滤原因（recall_ads_step） |
| 海选低 | 出价太低（prescreen_bid 不够）、频控限制 | 看 F3 过滤原因（pre_ranking_filter_step）+ 出价链路 |
| 粗排低 | 粗排分低、流量竞争被截断 | 看 running_info 中粗排分分布 |
| 精排低 | 精排分低、ecpm 不够、精排后被过滤 | 看 running_info ecpm/pcvr/pctr 分布 |
| 拍卖低 | 竞价出价不足（被竞争对手压价） | 结合出价链路中 cpa_bid × pConsCvr 估算 ecpm |

---

## 与投后数据的联动

前链路漏斗（adtrace）是**采样明细数据**，反映竞价流程。
投后数据（`dws_ad_full_log_trackid_di`）是**全量汇总数据**，反映最终效果。

两者联动分析方式：
- 投后数据发现 `imp_cnt` 下跌 → 用 adtrace 定位是召回/海选/精排哪层卡住
- 投后数据发现 `cpa` 升高 → 用 adtrace running_info 看精排阶段的 pcvr/ecpm 是否高估
- 掉量场景：先看出价链路（bid_ratio/subsidy_ratio），再用 adtrace 看漏斗哪层通过数在同步下降

---

## 注意事项

- **ck 表 TTL 只有 7 天**，超过 7 天的历史分析只能用 hive 表（30天）
- **不要对 ck 两张表做 JOIN**，资源消耗极大
- **实验组查询**建议用 hive（`array_contains(exp_ids, id)`），ck 查实验 id 需全表扫描容易失败
- 召回到粗排阶段 `exp_ids = null`（hive），ck 表此阶段有 5% 二次采样
- 如需更长数据周期（>30天），联系 @余歌(路志远)

## ⚠️ 采样稀疏限制（重要）

adtrace 展示场域 PV 采样率仅 **0.2%**，对于小账户/掉量账户极易出现 0 行结果。

**判断方法**：预期样本数 = `imp_cnt × 0.2%`，若 < 50 则大概率跑不出数据。

| imp_cnt | 预期样本数 | 能否分析 |
|---------|-----------|---------|
| < 10,000 | < 20 | ❌ 基本无数据 |
| 10,000~50,000 | 20~100 | ⚠️ 数据稀疏，仅供参考 |
| > 50,000 | > 100 | ✅ 可分析 |

**解决方案**：
1. **申请 adtrace 白名单**：将 advertiser_id 加入 pv 采样白名单，命中后全量采样（联系 adtrace 负责人）
2. **用 redbi ck 看板**：通过 [redbi 信息流看板](https://redbi.devops.xiaohongshu.com/dashboard/list?dashboardid=39277) 筛选 campaign_id，ck 表性能好且已还原采样
3. **扩大时间范围**：若某天 imp 不足，合并多天数据看趋势

**hive 表查询注意事项**：
- `advertiser_id` / `campaign_id` 无索引，全表扫描慢且易超时
- 必须加 `hh`（小时）分区缩小扫描范围
- 建议用异步提交（`submit`）而非同步执行（`execute`）
- `is_pass` 是 **boolean 类型**，但 `is_pass = true` 与 `advertiser_id` 过滤组合时会触发 Spark 谓词下推 bug 导致结果为空，**必须改用 `CAST(is_pass AS STRING) = 'true'`**
- stage / checkpoint 字段为**全大写**，如 `RECALL_ADS_STEP`、`FARES_RECALL_TRIGGERED`
