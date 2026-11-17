# 单店铺数据查询能力参考

> 本文档仅在**单店铺模式**下需要阅读。多店铺模式使用 `get_multi_shop_report` 一条命令完成所有查询。

## 通用说明

### CLI 调用格式

```bash
python3 {baseDir}/cli.py <command> --query_date <YYYY-MM-DD> [--NEWTON_SHOP_LOGIN_ID <login_id>]
```

### 通用参数

| 参数 | 必填 | 说明 |
|------|------|------|
| `--query_date` | 是 | 查询日期，格式 YYYY-MM-DD，数据 T+1 更新，最早为昨天 |
| `--NEWTON_SHOP_LOGIN_ID` | 否 | 目标店铺 loginId，不传则查默认店铺 |

### 通用失败输出

```json
{
  "success": false,
  "markdown": "❌ <错误描述>",
  "data": { "data": {} }
}
```

> 异常处理与使用注意事项见 SKILL.md「异常处理」章节。

---

## get_trade_data — 交易数据

获取指定日期的店铺交易数据，包含 GMV、订单量、客单价、支付转化率、询盘数，以及日环比、周环比对比数据。

### 返回字段

| 字段 | 类型 | 说明 |
|------|------|------|
| gmv | Number | 成交总额（元） |
| orderCount | Number | 订单量（单） |
| avgPrice | Number | 客单价（元） |
| payConversionRate | Number | 支付转化率（%） |
| inquiryCount | Number | 询盘数（个） |
| dayOnDay | Object | 日环比数据 |
| weekOnWeek | Object | 周环比数据 |

### 成功示例

```json
{
  "success": true,
  "markdown": "交易数据查询成功",
  "data": {
    "data": {
      "gmv": 6360,
      "orderCount": 12,
      "avgPrice": 530,
      "payConversionRate": 3.21,
      "inquiryCount": 44,
      "dayOnDay": { "gmv": 68.98, "orderCount": 100, "inquiryCount": 700 },
      "weekOnWeek": { "gmv": -60.59, "orderCount": 0, "inquiryCount": 100 }
    }
  }
}
```

---

## get_traffic_data — 流量数据

获取指定日期的店铺流量数据，包含 PV、UV、UVCTR、跳出率、广告曝光、搜索曝光等。

### 返回字段

| 字段 | 类型 | 说明 |
|------|------|------|
| pv | Number | 页面浏览量（次） |
| uv | Number | 独立访客数（人） |
| uvCtr | Number | 访客点击率（%） |
| bounceRate | Number | 跳出率（%） |
| adExposure | Number | 广告曝光次数 |
| searchExposure | Number | 搜索曝光次数 |

### 成功示例

```json
{
  "success": true,
  "markdown": "流量数据查询成功",
  "data": {
    "data": {
      "pv": 693,
      "uv": 343,
      "uvCtr": 5.83,
      "bounceRate": 62.68,
      "adExposure": 20109,
      "searchExposure": 8530
    }
  }
}
```

---

## get_user_data — 买家数据

获取指定日期的店铺买家数据，包含新买家数、老买家数及对应支付金额。

### 返回字段

| 字段 | 类型 | 说明 |
|------|------|------|
| newBuyerCount | Number | 新买家数（人） |
| oldBuyerCount | Number | 老买家数（人） |
| newBuyerPayAmount | Number | 新买家支付金额（元） |
| oldBuyerPayAmount | Number | 老买家支付金额（元） |

### 成功示例

```json
{
  "success": true,
  "markdown": "买家数据查询成功",
  "data": {
    "data": {
      "newBuyerCount": 5,
      "oldBuyerCount": 7,
      "newBuyerPayAmount": 2650,
      "oldBuyerPayAmount": 3710
    }
  }
}
```

---

## get_ad_report — 广告投放日报

内部自动查询当天 + 前一天数据，计算环比、汇总指标、Top3 计划。

- 多店铺模式下无需单独调用，`get_multi_shop_report` 已自动集成，结果在 `adReport` 字段
- 广告数据为空时返回 `hasData: false`，Agent 应跳过广告板块

### 返回字段

| 字段 | 说明 |
|------|------|
| `hasData` | 是否有广告数据，false 时跳过广告板块 |
| `spend` | 总消耗（元） |
| `exposure` | 曝光量 |
| `clicks` | 点击量 |
| `visitors` | 广告访客数（去重） |
| `inquiries` | 询盘数 |
| `deals` | 成交笔数 |
| `deal_amount` | 成交金额 |
| `favorites` | 收藏商品数 |
| `cart_adds` | 加购数 |
| `plan_count` | 投放计划数 |
| `ctr` | 点击率 CTR（%） |
| `cpc` | 单次点击成本 CPC（元） |
| `roi` | 投入产出比 ROI |
| `changes` | 各指标日环比变化率（%），null 表示前一天为0无法计算；整体为 null 表示前一天无数据 |
| `topPlans` | 消耗 Top3 计划详情（已按计划名称合并同名子计划、过滤零消耗计划后按消耗降序） |

### 成功示例

```json
{
  "success": true,
  "markdown": "广告投放数据查询成功",
  "data": {
    "query_date": "20260629",
    "prev_date": "20260628",
    "hasData": true,
    "today": {
      "spend": 682.15, "exposure": 6247, "clicks": 249, "visitors": 213,
      "inquiries": 7, "deals": 0, "deal_amount": 0.0,
      "favorites": 7, "cart_adds": 33, "plan_count": 5,
      "ctr": 3.99, "cpc": 2.74, "roi": 0.0
    },
    "prevDay": {
      "spend": 482.87, "exposure": 4696, "clicks": 222, "visitors": 187,
      "inquiries": 14, "deals": 12, "deal_amount": 1117.0,
      "ctr": 4.73, "cpc": 2.18, "roi": 2.31
    },
    "changes": {
      "spend": 41.3, "exposure": 33.0, "clicks": 12.2, "visitors": 13.9,
      "inquiries": -50.0, "deals": -100.0, "deal_amount": -100.0
    },
    "topPlans": [
      {"name": "核心商家成长计划", "category": "核心商家成长计划", "spend": 224.5, "clicks": 54, "inquiries": 0, "deals": 0, "roi": 0.0},
      {"name": "服饰配件5月效果保障计划", "category": "全站推店", "spend": 143.0, "clicks": 74, "inquiries": 3, "deals": 0, "roi": 0.0}
    ]
  }
}
```

### 空数据返回

```json
{
  "success": true,
  "data": { "hasData": false, "message": "当天及前一天均无广告投放数据", "today": null, "prevDay": null, "changes": null, "topPlans": [] }
}
```

### 广告板块展示规则

- `hasData=false` 或查询失败时，日报中省略广告板块
- 异常识别：消耗大幅增加但成交/询盘下降 → ⚠️ 风险；ROI 大幅提升 → 📈 机会
- `topPlans` 已在服务端按计划名称聚合（托管类方案的多条同名子计划合并累加后重算 ROI），展示时直接按计划维度呈现，不再拆分
- 行动建议话术限制：**禁止建议暂停/关停低效计划**，一律用预算再分配话术；品牌类计划不得仅因 ROI 低判定效果差（完整规范见 SKILL.md「广告分析规范」）
