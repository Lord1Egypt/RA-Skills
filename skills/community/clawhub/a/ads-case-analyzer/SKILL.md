---
name: ads-case-analyzer
description: 内容消费行业广告投放 Case 排查助手。输入 campaign_id/advertiser_id/brand_account_id、数据分析周期和排查方向，自动拉取投后数据、出价数据，完成漏斗分析、出价链路拆解、根因推断，产出结构化 Redoc 分析文档。当用户说「帮我排查这个客户的投放」「分析一下这个计划为什么跑不起来」「这个账户消耗下跌是什么原因」时触发。
metadata: { "openclaw": { "emoji": "🔍", "requires": { "bins": ["curl", "jq", "python3"] } } }
---

# ads-case-analyzer — 内容消费广告投放 Case 排查

## 能力概述

根据输入的广告主/计划标识、分析周期、排查方向，执行以下流程：
1. 拉取投后数据（日粒度大盘 + 分场域 + 分计划）
2. 拉取出价链路数据（离线出价参数 + 在线出价参数）
3. LLM 推理根因，定位问题层（跑量/出价/转化/竞争）
4. 产出结构化 Redoc 分析文档

## 输入参数

| 参数 | 说明 | 是否必填 |
|------|------|----------|
| `advertiser_id` | 广告主 ID | 三选一 |
| `campaign_id` | 计划 ID（可多个，逗号分隔） | 三选一 |
| `brand_account_id` | 品牌账号 ID | 三选一 |
| `start_date` | 分析开始日期，格式 `YYYYMMDD` | 必填 |
| `end_date` | 分析结束日期，格式 `YYYYMMDD` | 必填 |
| `issue_direction` | 排查方向（见下方枚举） | 必填 |
| `optimize_target` | 优化目标（数字，可不填，脚本自动从数据中推断） | 选填 |
| `constraint_type` | 约束目标（数字，可不填，脚本自动推断） | 选填 |

### 排查方向枚举（issue_direction）

| 值 | 含义 |
|----|------|
| `volume_drop` | 跑量/消耗下跌 |
| `cpa_high` | 激活/转化成本偏高 |
| `roi_bad` | 计费比异常（advv/fee 偏低，平台超收）|
| `retention_low` | 次留率低 |
| `bid_weak` | 出价竞争力不足（跑不出量）|
| `pcvr_gap` | 预估转化率与实际偏差大（calibration 问题）|
| `placement_abnormal` | 某场域表现异常 |
| `general` | 整体健康度排查（无明确方向）|

### optimize_target 枚举

| 值 | 含义 |
|----|------|
| 60 | 下载按钮点击 |
| 61 | 激活 |
| 62 | 注册 |
| 63 | 关键行为 |
| 64 | app 付费 |
| 65 | 小程序打开 |
| 67 | 小程序付费 |
| 69 | 预约下载按钮点击 |
| 72 | 预约表单提交 |
| 73 | 微小打开 |
| 74 | 微小激活 |
| 75 | 微小付费 |
| 48 | 下载24hROI |
| 49 | 小程序24hROI |

---

## 数据源说明

### 1. 投后数据：`ads_data_common.dws_ad_full_log_trackid_di`

核心字段：
- **维度**：`advertiser_id`, `campaign_id`, `ad_id`, `placement`（场域：1=信息流,2=搜索）, `platform`（设备平台）, `marketing_target`, `optimize_target`, `constraint_type`
- **曝光/点击**：`imp_cnt`, `click_cnt`
- **消耗**：`fee`（单位：分）
- **advv**：`advv`
- **转化**：`app_activate_cnt`, `app_register_cnt`, `app_pay_cnt`, `app_pay`, `app_key_action_cnt`, `retention_1d_cnt`, `mini_apps_payment_cnt`, `mini_apps_pay_amount`, `app_subscribe_leads_cnt`
- **预估/校准转化率**：`ori_pcvr`, `cali_pcvr`, `pcvr`, `ori_constraint_type_pcvr`, `constraint_cali_pcvr`, `constraint_type_pcvr`
- **分区**：`dtm`（格式 `YYYYMMDD`，无 `date_` 字段）

### 2. 离线出价：`hive_prod.ads_data_common.bidding_cube_trace_log_hourly`

过滤条件：`context = 'app_ocpx'` AND `bucket = 'default'`

`metric` 字段（map 类型）关键 key：
- `bid_ratio`：出价系数（离线校准系数）
- `given_cpa`：广告主出价（单位：分）
- `cpa_bid`：系统计算的 CPA 出价（分）
- `subsidy_ratio`：补贴系数
- `prescreen_bid`：海选价

**注意**：该表为小时粒度，分析时聚合到日，join key 为 `advertiser_id`/`campaign_id`

### 3. 在线出价（信息流场域）：`hive_prod.ads_data_common.bidding_pivot_trace_log_feed`

关键字段（`MAP<STRING, DOUBLE>` 类型，直接用 `['key']` 访问，禁止 `get_json_object`）：
- `bid_param.cpaBid`：在线 CPA 出价
- `bid_param.cpaBidRatio`：离线出价系数透传值
- `bid_param.subsidyRatio`：排序计费分离系数（>1 表示欠收超扣，<1 表示过收缩扣）
- `bid_req.pgmv`：GMV 预估值
- `bid_req.pConsCvr`：约束目标 CVR 预估
- `bid_req.pcvr`：优化目标 CVR 预估
- `bid_req.pctr`：CTR 预估
- `bid_layer`：生效出价扰动策略，`new_bid` 为扰动后的 CPC bid

### 4. 在线出价（搜索场域）：`hive_prod.ads_data_common.bidding_pivot_trace_log_search`

字段结构同 feed 表。

---

## 执行流程

### Step 1：解析输入，确定过滤条件

根据输入的 `advertiser_id`/`campaign_id`/`brand_account_id` 确定 WHERE 条件。
若只有 `brand_account_id`，先查一下关联的 `advertiser_id`：

```sql
-- 通过 brand_account_id 找 advertiser_id（如有此映射表）
SELECT DISTINCT advertiser_id
FROM ads_data_common.dws_ad_full_log_trackid_di
WHERE dtm BETWEEN '{start_date}' AND '{end_date}'
  AND brand_account_id = '{brand_account_id}'
LIMIT 10
```

### Step 2：投后数据 — 日粒度大盘

默认分组维度：`dtm` + `placement` + `optimize_target` + `constraint_type`。
若用户明确要求拆平台，加 `platform` 到 GROUP BY。

```sql
SELECT
    dtm,
    placement,
    -- platform,  -- 用户要求拆 iOS/Android 时取消注释
    optimize_target,
    constraint_type,
    SUM(imp_cnt)              AS imp_cnt,
    SUM(click_cnt)            AS click_cnt,
    SUM(fee) / 100.0          AS fee_yuan,
    SUM(advv)                 AS advv,
    SUM(app_activate_cnt)     AS activate_cnt,
    SUM(retention_1d_cnt)     AS retention_1d_cnt,
    SUM(app_pay_cnt)          AS pay_cnt,
    SUM(app_pay) / 100.0      AS pay_amount,
    SUM(mini_apps_payment_cnt) AS mini_pay_cnt,
    SUM(mini_apps_pay_amount) / 100.0 AS mini_pay_amount,
    -- 核心效率指标
    SUM(click_cnt) / NULLIF(SUM(imp_cnt), 0)         AS ctr,
    SUM(app_activate_cnt) / NULLIF(SUM(click_cnt), 0) AS cvr,
    SUM(fee) / NULLIF(SUM(app_activate_cnt), 0) / 100.0 AS cpa_activate,
    SUM(retention_1d_cnt) / NULLIF(SUM(app_activate_cnt), 0) AS retention_rate,
    AVG(ori_pcvr)             AS avg_ori_pcvr,
    AVG(pcvr)                 AS avg_pcvr,
    AVG(constraint_type_pcvr) AS avg_constraint_pcvr
FROM ads_data_common.dws_ad_full_log_trackid_di
WHERE dtm BETWEEN '{start_date}' AND '{end_date}'
  AND {id_filter}
  -- AND optimize_target IN (61, 64, ...)  -- 按需过滤
GROUP BY dtm, placement, optimize_target, constraint_type
  -- , platform  -- 拆平台时取消注释
ORDER BY dtm, placement
```

### Step 3：投后数据 — 按输入粒度汇总

**规则：输入什么维度就看什么维度，不主动下钻。**
- 输入 `brand_account_id` → 按 `advertiser_id` 汇总
- 输入 `advertiser_id` → 按 `campaign_id` 汇总
- 输入 `campaign_id`（单个或多个）→ 按 `ad_id` 汇总

若用户有进一步下钻诉求，交互确认后再执行更细粒度的查询。

```sql
-- 示例：输入 advertiser_id，按 campaign_id 汇总
SELECT
    dtm,
    campaign_id,
    placement,
    SUM(imp_cnt)          AS imp_cnt,
    SUM(fee) / 100.0      AS fee_yuan,
    SUM(app_activate_cnt) AS activate_cnt,
    SUM(fee) / NULLIF(SUM(app_activate_cnt), 0) / 100.0 AS cpa_activate,
    SUM(advv)             AS advv,
    SUM(advv) / NULLIF(SUM(fee), 0) AS billing_ratio
FROM ads_data_common.dws_ad_full_log_trackid_di
WHERE dtm BETWEEN '{start_date}' AND '{end_date}'
  AND {id_filter}
GROUP BY dtm, campaign_id, placement
ORDER BY SUM(fee) DESC
LIMIT 50
```

### Step 3b：前链路漏斗分析（掉量场景必做，超成本可选）

> 数据来源：adtrace 2.0（详见 `references/adtrace_funnel.md`）
> **注意：ck 表 TTL=7天；超过 7 天用 hive 表（30天）**

**执行时机：**
- `issue_direction = volume_drop`：必做，定位掉量在漏斗哪层
- `issue_direction = cpa_high`：可选，看精排 ecpm/pcvr 是否高估
- 其他场景：用户有明确诉求时再做

**漏斗阶段（信息流）：**
```
召回 → 海选 → 粗排 → 精排 → 精排后过滤 → 拍卖 → 混排竞得
```

**标准执行步骤：**

1. 先查各阶段通过数（SQL F1/F2），定位哪层骤降
2. 对骤降的阶段查过滤原因（SQL F3），找具体过滤 checkpoint
3. 如需多日趋势对比，用 SQL F4

**表名：**
- hive 信息流：`hive_prod.redcdm.dwd_ads_adtrace_log_checkpoint_rt`（`source='feed'`）
- hive 搜索：同表，`source='search'`
- **必须加**：`request_label_bitset = 0`（生产流量）、`is_pass = 1`（正埋点）

**过滤原因定位逻辑：**

| 卡在哪层 | 常见原因 | 对应动作 |
|---------|---------|---------|
| 召回低 | 定向太窄/刹车/预算不足/素材被过滤 | 查 recall_ads_step 过滤原因 |
| 海选低 | 出价太低（prescreen_bid不够）/频控 | 查 pre_ranking_filter_step 过滤原因 + 出价链路 |
| 粗排低 | 粗排分低/竞争截断 | 查 running_info 粗排分分布 |
| 精排/拍卖低 | ecpm 不足/竞价出价低 | 结合出价链路 cpa_bid × pConsCvr 估算 ecpm |

### Step 3c：同笔记品牌内部竞争分析（掉量场景，有 brand_account_id 时执行）

> **分析目的**：判断同品牌账号下其他 advertiser 是否在使用相同笔记素材抢量，导致目标 adv 出价竞争力相对不足而掉量。

**执行时机：**
- `issue_direction = volume_drop` 且有 `brand_account_id`，必做
- 无 `brand_account_id` 时，可先查 `brand_account_id`：

```sql
-- 先查 brand_account_id
SELECT DISTINCT brand_account_id
FROM ads_data_common.dws_ad_full_log_trackid_di
WHERE dtm BETWEEN '{start_date}' AND '{end_date}'
  AND advertiser_id = '{advertiser_id}'
LIMIT 5
```

**标准 SQL：**

```sql
-- 取目标 adv 投放的所有笔记，查同品牌下各 adv 在这批笔记上的消耗分布
WITH adv_notes AS (
    SELECT DISTINCT note_id
    FROM ads_data_common.dws_ad_full_log_trackid_di
    WHERE dtm BETWEEN '{start_date}' AND '{end_date}'
      AND advertiser_id = '{advertiser_id}'
      AND note_id IS NOT NULL
      AND note_id != ''
)
SELECT
    t.dtm,
    t.advertiser_id,
    CASE WHEN t.advertiser_id = '{advertiser_id}' THEN '目标adv' ELSE '品牌其他adv' END AS adv_type,
    COUNT(DISTINCT t.note_id)       AS note_cnt,
    ROUND(SUM(t.fee) / 100.0, 2)   AS fee_yuan,
    SUM(t.imp_cnt)                  AS imp_cnt,
    SUM(t.click_cnt)                AS click_cnt
FROM ads_data_common.dws_ad_full_log_trackid_di t
INNER JOIN adv_notes n ON t.note_id = n.note_id
WHERE t.dtm BETWEEN '{start_date}' AND '{end_date}'
  AND t.brand_account_id = '{brand_account_id}'
GROUP BY t.dtm, t.advertiser_id
ORDER BY t.dtm, fee_yuan DESC
```

**解读逻辑：**

| 现象 | 判断 |
|------|------|
| 目标 adv 掉量，其他 adv 同批笔记消耗不变或上升 | ✅ 内部竞争抢量，需对比出价差异 |
| 目标 adv 掉量，其他 adv 同步下降 | ❌ 非内部竞争，根因在其他层（流量/出价/回传） |
| 目标 adv 掉量，单个 adv 突然大幅放量 | 🔴 强烈抢量信号，重点排查该 adv 出价变化 |

**结论写法：**
- 计算每天「目标 adv 消耗 / 同笔记品牌总消耗」占比，观察掉量日是否显著下降
- 点名放量的竞争 adv，建议排查其 bid_ratio 或 given_cpa 是否在掉量日有提升

---

### Step 4：离线出价参数

> **⚠️ 升维投放说明**：部分账户使用「升维投放」模式，不经过离线出价系统（`bidding_cube_trace_log_hourly` 返回 0 行），这是**正常现象**，不代表出价异常。升维投放的出价逻辑由在线系统直接决定，此时跳过 Step 4，直接看 Step 5 在线出价参数。
>
> **判断方法**：执行下方 SQL 后若返回 0 行，说明该账户走升维投放，记录在报告中并跳过。

```sql
SELECT
    dtm,
    advertiser_id,
    campaign_id,
    ROUND(AVG(metric['bid_ratio']), 4)          AS avg_bid_ratio,
    ROUND(AVG(metric['given_cpa']) / 100.0, 2)  AS avg_given_cpa,
    ROUND(AVG(metric['cpa_bid']) / 100.0, 2)    AS avg_cpa_bid,
    ROUND(AVG(metric['subsidy_ratio']), 4)      AS avg_subsidy_ratio,
    ROUND(AVG(metric['prescreen_bid']), 4)      AS avg_prescreen_bid
FROM hive_prod.ads_data_common.bidding_cube_trace_log_hourly
WHERE dtm BETWEEN '{start_date}' AND '{end_date}'
  AND context = 'app_ocpx'
  AND bucket = 'default'
  AND {id_filter}
GROUP BY dtm, advertiser_id, campaign_id
ORDER BY dtm
```

### Step 5：在线出价参数（信息流场域）

```sql
SELECT
    dtm,
    campaign_id,
    ROUND(AVG(bid_param['cpaBid']) / 100.0, 2)    AS avg_cpa_bid_online,
    ROUND(AVG(bid_param['cpaBidRatio']), 4)         AS avg_bid_ratio_online,
    ROUND(AVG(bid_param['subsidyRatio']), 4)        AS avg_subsidy_ratio,
    ROUND(AVG(bid_req['pcvr']) * 100, 4)           AS avg_pcvr,
    ROUND(AVG(bid_req['pConsCvr']) * 100, 4)       AS avg_pcons_cvr,
    ROUND(AVG(bid_req['pctr']) * 100, 4)           AS avg_pctr,
    ROUND(AVG(bid_req['pgmv']), 4)                 AS avg_pgmv,
    COUNT(*)                                        AS request_cnt
FROM hive_prod.ads_data_common.bidding_pivot_trace_log_feed
WHERE dtm BETWEEN '{start_date}' AND '{end_date}'
  AND {id_filter}
GROUP BY dtm, campaign_id
ORDER BY dtm
```

Step 5b（搜索场域）：同上，表换为 `bidding_pivot_trace_log_search`。

---

### Step 6：LLM 根因推理

收集上述所有 SQL 结果后，结合 `issue_direction` 进行推理。两个最核心场景有专项分析逻辑：

---

#### 场景一：超成本（`issue_direction = cpa_high`）

**额外执行 SQL：** S1-1（PAOA 日粒度）+ S1-2（ori_pcvr vs cali_pcvr vs 实际 CVR）

**PAOA 计算口径：**
- `placement IN (1, 2)`：预估转化 = `SUM(constraint_type_pcvr × click_cnt)`
- `placement = 7`（内流）：预估转化 = `SUM(constraint_type_pcvr × imp_cnt)`
- 实际转化字段：按 `constraint_type` 映射（见 `references/constraint_type_mapping.md`）
- **必须同时过滤 `optimize_target`**，防止 `app_invoke_cnt`/`app_activate_cnt` 等重叠字段混入

**分析链路：**
```
PAOA > 1（高估）→ 模型预估偏高 → 超成本
  ↓
拆解：ori_pcvr vs cali_pcvr vs 实际 CVR
  - ori_pcvr 已偏高 → 原始模型问题（特征/样本）
  - ori 正常但 cali 偏高（cali_multiplier 大）→ 校准放大了偏差
  - 预估都正常但实际 CVR 低 → 素材/落地页/人群质量问题
```

**constraint_type → 实际转化字段映射（快查）：**

| constraint_type | 实际转化字段 |
|----------------|------------|
| 60 | `app_download_button_click_cnt` |
| 61 | `app_activate_cnt` |
| 62 | `app_register_cnt` |
| 63 | `app_key_action_cnt` |
| 64 | `app_pay_cnt` |
| 65 | `app_invoke_cnt` |
| 67 | `mini_apps_payment_cnt` |
| 69 | `app_subscribe_button_click_cnt` |
| 72 | `leads_cnt` |
| 73 | `app_invoke_cnt` |
| 74 | `app_activate_cnt` |
| 75 | `app_payment_cnt` |
| 48/49 | TBD |

---

#### 场景二：掉量（`issue_direction = volume_drop`）

**额外执行 SQL：** S2-1（出价链路趋势）+ S2-2（在线预估分趋势）

**出价链路：**
```
given_cpa × bid_ratio × subsidy_ratio = 系统有效 CPA 出价
  × pConsCvr（约束目标 CVR 预估）
  × pctr（CTR 预估）
  × expoOptBoostScore（bid_layer 扰动系数）
  = CPC bid（最终竞价出价）→ 影响 ecpm → 影响跑量
```

**根因判断优先级：**
1. `bid_ratio` 下调 → 有效出价降低 → 跑量下降（最常见）
2. `avg_pcvr` / `avg_pctr` 下降 → ecpm 降低 → 竞争力不足
3. `subsidy_ratio < 1`（过收缩扣）→ 实际出价被压低
4. 以上正常 → 看 `avg_prescreen_bid` 是否上升（竞争加剧）
5. 以上都正常 → 确认预算/投放设置是否有变更

---

#### 通用根因框架

**漏斗拆解：**
```
曝光 → 点击（CTR）→ 激活/转化（CVR）→ 次留/深层
```
哪层下降最明显，问题就在哪层。

**其他场景根因参考：**

| 排查方向 | 主要看的信号 | 可能根因 |
|---------|------------|---------|
| `roi_bad` | billing_ratio(advv/fee)趋势、pgmv 预估 | advv 预估偏低、GMV 预估不准、平台超收 |
| `retention_low` | retention/activate 比、pcvr 分布 | 次留模型预估偏高、落地页体验差 |
| `pcvr_gap` | ori vs cali vs constraint_type_pcvr | 校准系数异常、样本稀疏 |
| `placement_abnormal` | 分 placement 指标对比 | 场域流量结构变化、出价策略差异 |

---

### Step 7：生成 Redoc 文档

调用 `/app/skills/hi-redoc-curd/scripts/hi-redoc-curd.sh -p {report_path}` 生成文档。

**文档命名规则：**
- 完整报告：`{end_date} {品牌名}-{advertiser_id}账户{issue_type}分析（完整报告）`
- 简报：`{end_date} {品牌名}-{advertiser_id}账户{issue_type}分析`
- `issue_type` 映射：`volume_drop`→掉量，`cpa_high`→超成本，`roi_bad`→计费比异常，`general`→投放分析
- `end_date` 格式：`YYYYMMDD`（8位），如 `20260331`
- 品牌名从 `brand_account_id` 关联的品牌名称获取；若无则用 `advertiser_id` 替代
- 示例：`20260331 杖剑传说-7540400账户掉量分析（完整报告）`

文档结构：

```markdown
# {end_date} {品牌名}-{advertiser_id}账户{issue_type}分析（完整报告）

## ⚡ 核心结论（TL;DR）

> **一句话描述核心异动：{消耗/曝光} 从 X 骤降至 Y（-Z%），根因如下：**

| 优先级 | 根因 | 关键数据 |
|--------|------|---------|
| 🔴 核心 | ... | ... |
| 🟡 重要 | ... | ... |
| 🟢 参考 | ... | ... |

**最紧急的行动项：**
1. 🔴 ...
2. 🔴 ...

---

## 一、基本信息
- 广告主/计划：...
- 分析周期：...
- 排查方向：...
- 优化目标/约束目标：...

## 二、整体大盘趋势
[日粒度核心指标表格：消耗/曝光/点击/激活/次留/计费比(billing_ratio=advv/fee)]
[趋势描述：哪天开始异常，幅度多大]

## 三、分场域拆解
[信息流 vs 搜索对比表]
[哪个场域是主要问题来源]

## 四、分计划拆解
[Top 计划表现，出价/消耗/CPA 对比]

## 五、出价链路分析
[离线出价参数趋势：bid_ratio / given_cpa / cpa_bid / subsidy_ratio]
[在线出价参数：pcvr / pConsCvr / pctr / pgmv 趋势]
[出价链路是否正常：given_cpa × bid_ratio × subsidy_ratio = 实际竞价]

## 六、根因定位
[漏斗断层：哪一层转化率明显下降]
[出价链路：系数变化导致的出价变化估算]
[核心根因：1-3条，明确]

## 七、结论与建议
[问题摘要]
[优化动作建议：出价调整/素材更新/人群策略/calibration修复等]
```

---

## 调用示例

用户说：「帮我排查一下 advertiser_id=123456，3月25日到31日，消耗一直在下跌，看看是什么原因」

执行步骤：
1. 解析：`advertiser_id=123456`, `start_date=20260325`, `end_date=20260331`, `issue_direction=volume_drop`
2. 执行 Step 2–5 的 SQL（展示 DOR 执行前先给用户看 SQL，确认后执行）
3. 整理数据，执行 Step 6 根因推理
4. 生成 Redoc 文档，返回链接

---

## 注意事项

- **SQL 执行规则**：遵循 DOR skill 规范，执行前必须展示 SQL，用户确认后再跑。大表（bidding_pivot）加时间分区过滤，必要时加 `LIMIT`。
- **出价表数据量**：`bidding_pivot_trace_log_feed/search` 数据量较大，分析时优先用 `bidding_cube_trace_log_hourly`（已聚合），只在需要定位具体请求时才查 pivot 表。
- **metric 字段解析**：`bidding_cube_trace_log_hourly` 的 `metric` 是 Hive map 类型，直接用 `metric['key']` 访问。
- **保浅优深计划**：`constraint_type ≠ optimize_target`，出价锚定 `constraint_type`，深层目标为 `optimize_target`，分析时要分清两层指标。
- **fee 单位**：`dws_ad_full_log_trackid_di` 中 `fee`、`given_cpa`、`cpa_bid` 单位均为**分**，展示时除以 100。
- **subsidy_ratio 解读**：>1 表示当前欠收正在超扣（平台补贴广告主），<1 表示过收缩扣，=1 正常。
- **升维投放**：`bidding_cube_trace_log_hourly` 返回 0 行时属正常，记录说明并跳过，直接看在线出价参数。

---

## 排查经验库（来自历史 case）

### 掉量场景常见根因（优先排查顺序）

1. **客户主动操作**：降价/降预算/缩窄定向/暂停/账户余额不足——**最先排查**，可查操作记录表
2. **账户/计划预算撞线**：日预算用完后自动停投，次日才恢复
3. **同物料账户内抢量**：相同笔记在账户内多计划/多 adv 投放，内部去重过滤导致竞得量下降
4. **素材质量问题**：笔记活动声明过期、差评过多导致 CTR/CVR 持续下滑
5. **ecpm 竞争力下降**：pctr/pcvr/出价三者之一下滑，导致海选/粗排截断
6. **lambda/调价策略波动**：转化时序偶然因素导致调价系数重置（整桶调控计划尤其注意）
7. **大促节点后流量回落**：大促期间流量竞争加剧，节后自然回落，属周期性波动

### 超成本场景常见根因

1. **PAOA > 1**：模型高估，拆解 ori_pcvr vs cali_pcvr vs 实际 CVR
2. **竞争环境变化**：竞争加剧导致低出价拿不到量，被迫提价后 CVR 低的流量进来
3. **素材质量下滑**：CTR 正常但 CVR 下降，用户点进来后不转化


### 工具资源（内部平台）

| 工具 | 用途 | 链接 |
|------|------|------|
| 计划投放效果分析工具 | 场域拆分/PAOA/操作记录/竞争力/参竞漏斗/同物料抢量 | redbi dashboard 3120 |
| 投放排查工具（聚光） | 计划竞争力、竞争力拆解（出价/CTR/CVR 三维水位） | ad.xiaohongshu.com/aurora/ad/tools/monitoring_tool |
| 创意粒度漏斗排查 | 详细参竞漏斗，创意粒度 | 内部自助分析工具 |
| hera 平台 | 附身登录查创意审核状态 | hera.xiaohongshu.com |
| red-gravity | 出价因子 lambda 变化趋势 | gravity.devops.xiaohongshu.com |

### 掉量排查 checklist（快速核查）

```
□ 1. 客户操作记录：近 7 天是否有降价/降预算/暂停？
□ 2. 账户预算：是否有某天撞线？
□ 3. 同物料抢量：账户内其他计划是否用了相同笔记？重复消耗占比？
□ 4. 素材状态：活动声明是否过期？CTR/CVR 是否持续下滑？
□ 5. adtrace 漏斗：哪层断层（海选/粗排/竞得）？
□ 6. 品牌内竞争（有 brand_account_id）：同笔记其他 adv 是否放量？
□ 7. 出价链路：bid_ratio/pcvr/pctr 是否有下滑？lambda 是否重置？
□ 8. 大盘环境：是否节点/大促节后自然回落？
```
