# 根因推理 Prompt 模板

以下是 Step 6 LLM 推理时使用的 prompt 框架，将数据填入后进行分析。

---

## Prompt 模板

```
你是小红书广告算法工程师，擅长内容消费行业广告投放 case 排查。
请基于以下数据，完成根因分析并给出优化建议。

## 排查背景
- 广告主/计划：{advertiser_id} / {campaign_id}
- 分析周期：{start_date} ~ {end_date}
- 排查方向：{issue_direction_label}
- 优化目标：{optimize_target_label}（{optimize_target}）
- 约束目标：{constraint_type_label}（{constraint_type}）
- 是否保浅优深：{is_shallow_deep}（constraint_type ≠ optimize_target 时为是）

## 投后数据（日粒度，分场域）
{table_t1_markdown}

## 分计划数据
{table_t2_markdown}

## 离线出价参数（bid_ratio / given_cpa / cpa_bid / subsidy_ratio）
{table_t3_markdown}

## 在线出价参数（展示场域 pcvr / subsidyRatio / cpaBid）
{table_t4_markdown}

## 在线出价参数（搜索场域）
{table_t4b_markdown}

---

## 分析框架

请按以下结构输出：

### 1. 漏斗拆解
逐层分析：曝光 → 点击（CTR）→ 激活（CVR）→ 次留（retention_rate）
- 哪一层指标出现明显下降或异常？
- 下降幅度和时间节点？

### 2. 出价链路分析
出价链路：given_cpa × bid_ratio × subsidy_ratio = 系统实际 CPA 出价
- bid_ratio 是否在分析期内发生显著变化？方向和幅度？
- subsidy_ratio 是否异常（>2 表示强超扣，<0.5 表示强缩扣）？
- 在线 cpaBid 与离线 cpa_bid 是否一致？如有偏差，说明中间有扰动（bid_layer）
- 在线 pcvr / pConsCvr 趋势是否稳定？是否与实际 CVR 匹配？

### 3. 场域差异
- 展示场域 vs 搜索场域，哪个场域是主要问题来源？
- 两个场域的 CTR / CVR / CPA 差异是否合理？

### 4. 根因定位
结合上述分析，列出 1-3 条核心根因，格式：
- 根因1：[现象] → [数据支撑] → [推断机制]
- 根因2：...

### 5. 优化建议
针对每条根因给出具体可操作的建议：
- 出价调整方向（加价/降价/调整 bid_ratio）
- 素材/人群方向
- 校准问题（如需联系算法同学）
- 监控指标建议
```

---

## optimize_target 标签映射

| 值 | 标签 |
|----|------|
| 60 | 下载按钮点击 |
| 61 | 激活 |
| 62 | 注册 |
| 63 | 关键行为 |
| 64 | app付费 |
| 65 | 小程序打开 |
| 67 | 小程序付费 |
| 69 | 预约下载按钮点击 |
| 72 | 预约表单提交 |
| 73 | 微小打开 |
| 74 | 微小激活 |
| 75 | 微小付费 |
| 48 | 下载24hROI |
| 49 | 小程序24hROI |

## issue_direction 标签映射

| 值 | 标签 |
|----|------|
| volume_drop | 跑量/消耗下跌 |
| cpa_high | 激活/转化成本偏高 |
| roi_bad | ROI/advv 恶化 |
| retention_low | 次留率低 |
| bid_weak | 出价竞争力不足 |
| pcvr_gap | 预估转化率与实际偏差大 |
| placement_abnormal | 某场域表现异常 |
| general | 整体健康度排查 |
