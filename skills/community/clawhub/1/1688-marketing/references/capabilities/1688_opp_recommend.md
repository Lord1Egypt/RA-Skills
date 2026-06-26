# 商机推荐查询指南

## 功能说明

通过 CLI 调用 1688 接口，查询商机推荐列表，帮助商家发现市场商机。支持按关键词搜索和按类目筛选。

## 前置条件

- 已配置 AK（未配置时会提示运行 `cli.py configure YOUR_AK`）

## CLI 调用

```bash
python3 {baseDir}/cli.py 1688_opp_recommend [--pageNo 页码] [--pageSize 每页条数] [--keyword 关键词] [--categoryId 类目ID或名称]
```

### 参数说明

| 参数 | 缩写 | 是否必填 | 默认值 | 说明 |
|------|------|----------|--------|------|
| `--pageNo` | `-p` | ❌ 否 | `1` | 页码，从1开始 |
| `--pageSize` | `-s` | ❌ 否 | `20` | 每页条数 |
| `--keyword` | `-k` | ❌ 否 | — | 按商机标题搜索的关键词 |
| `--categoryId` | `-c` | ❌ 否 | — | 一级类目 ID 或中文名称（如 `1038378` 或 `鞋`） |

### 调用示例

```bash
# 查询默认推荐（无筛选）
python3 {baseDir}/cli.py 1688_opp_recommend

# 按关键词搜索
python3 {baseDir}/cli.py 1688_opp_recommend -k "连衣裙"

# 按类目筛选（支持中文名称）
python3 {baseDir}/cli.py 1688_opp_recommend -c "鞋"

# 按类目筛选（支持类目ID）
python3 {baseDir}/cli.py 1688_opp_recommend -c "1038378"

# 组合筛选 + 分页
python3 {baseDir}/cli.py 1688_opp_recommend -k "运动鞋" -c "鞋" -p 2 -s 10
```

---

## 接口信息

- **接口类**：`com.alibaba.cbu.insight.service.opportunityportrait.impl.OpportunityPortraitHandleServiceImpl`
- **方法签名**：`ResultModel<Map<String, Object>> queryOpportunitiesNew(Long userId, Map<String, Object> params)`
- **返回值类型**：`ResultModel<Map<String, Object>>`

### 入参说明

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `userId` | Long | 是 | 用户ID |
| `params` | Map<String, Object> | 是 | 查询参数，包含分页、类目、筛选条件等 |

#### params 内部结构

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `sceneCode` | String | 是 | 场景编码，固定值 `realOpportunityPortraitViewNew` |
| `sceneType` | String | 是 | 场景类型，固定值 `offer_portrait` |
| `pageNo` | int | 是 | 页码，从1开始 |
| `pageSize` | int | 是 | 每页条数，默认20 |
| `conditions` | Object[] | 是 | 筛选条件数组 |

### 筛选条件（conditions）

每个条件对象结构为：

```json
{
  "nodeName": "条件中文名",
  "nodeCode": "条件编码",
  "value": ["值1", "值2"]
}
```

#### 按商机标题检索

```json
{
  "nodeCode": "title",
  "nodeName": "商机标题",
  "value": ["关键词"]
}
```

#### 按类目筛选

```json
{
  "nodeCode": "category_id_path",
  "nodeName": "商机类目",
  "value": ["一级类目ID"]
}
```

> 以上固定条件（`opp_type`、`is_test`、`tag_info`、`status`、`delivery_channel`、`sort_field`）由代码自动注入，调用方无需关心。

### 请求示例

#### 初始化请求（无筛选）

```json
{
  "userId": 2214452629780,
  "params": {
    "sceneCode": "realOpportunityPortraitViewNew",
    "sceneType": "offer_portrait",
    "pageNo": 1,
    "pageSize": 20,
    "mainCategorys": ["1031910", "127372010", "10166", "1045520", "1813"],
    "cate_param_empty": true,
    "conditions": [
      { "nodeName": "画像类型", "nodeCode": "opp_type", "value": ["item"] },
      { "nodeName": "是否测试画像", "nodeCode": "is_test", "value": ["N"] },
      { "nodeName": "商机标签", "nodeCode": "tag_info", "value": ["xinpin_maijiaxuqiu", "xinpin_ifashion", "xinpin_xiaoheihe", "xinpin_xinpinqudong", "xinpin_fuzhuangteshu", "xinpin_chaoliuxinpin", "xinpin_taobao_new_tag", "real_new_cu", "xinpin_trend_hot", "nontb_263531_xinpin", "nontb_263531_aoxia"] },
      { "nodeName": "画像状态", "nodeCode": "status", "value": ["ONLINE"] },
      { "nodeName": "商机状态", "nodeCode": "delivery_channel", "value": ["supply"] },
      { "nodeName": "排序方式", "nodeCode": "sort_field", "value": ["item_rank#desc#tpp"] }
    ]
  }
}
```

> 上述所有字段均为默认值，由代码自动填充，调用方只需提供 `userId`。

#### 按标题关键词检索

```json
{
  "userId": 2214452629780,
  "params": {
    "sceneCode": "realOpportunityPortraitViewNew",
    "sceneType": "offer_portrait",
    "pageNo": 1,
    "pageSize": 20,
    "mainCategorys": ["1031910", "127372010", "10166", "1045520", "1813"],
    "cate_param_empty": true,
    "conditions": [
      { "nodeName": "商机标题", "nodeCode": "title", "value": ["连衣裙"] }
    ]
  }
}
```

> **关键参数**：`conditions` 中新增 `nodeCode: "title"` 条件，`value` 为搜索关键词数组。其余均为默认值。

#### 按类目筛选

```json
{
  "userId": 2214452629780,
  "params": {
    "sceneCode": "realOpportunityPortraitViewNew",
    "sceneType": "offer_portrait",
    "pageNo": 1,
    "pageSize": 20,
    "mainCategorys": ["1031910", "127372010", "10166", "1045520", "1813"],
    "cate_param_empty": true,
    "conditions": [
      { "nodeName": "商机类目", "nodeCode": "category_id_path", "value": ["1038378"] }
    ]
  }
}
```

> **关键参数**：`conditions` 中新增 `nodeCode: "category_id_path"` 条件，`value` 为一级类目ID数组（如 `1038378` 代表鞋）。其余均为默认值。

---

## 出参模型

### ResultModel

```java
package com.alibaba.cbu.insight.service.opportunityportrait.models;

public class ResultModel<T> implements Serializable {
    private T model;                              // 数据主体
    private String msg;                           // 消息
    private ResultCode code = ResultCode.SUCCESS;  // 状态码
    private boolean success = Boolean.TRUE;        // 是否成功
}
```

### 响应结构

```json
{
  "code": "SUCCESS",
  "success": true,
  "model": {
    "oppIds": [133509664, 133510495],
    "totalCnt": "2000",
    "pageNo": 1,
    "pageSize": 20,
    "scmId": "opensearch",
    "data": [ ... ]
  }
}
```

### model 字段说明

| 字段 | 类型 | 说明 |
|------|------|------|
| `oppIds` | Long[] | 商机ID列表 |
| `totalCnt` | String | 总条数 |
| `pageNo` | int | 当前页码 |
| `pageSize` | int | 每页条数 |
| `scmId` | String | 搜索引擎标识 |
| `data` | Object[] | 商机详情数组 |

### data 单条商机字段说明

| 字段 | 类型 | 说明 |
|------|------|------|
| `id` | String | 商机ID |
| `title` | String | 商机标题 |
| `pictUrlList` | String[] | 商品图片列表（OSS key） |
| `pictUrls` | String | 主图（OSS key） |
| `oppItemId` | String | 对应商品ID |
| `cateLevel1Id` | String | 一级类目ID |
| `cateLevel1Name` | String | 一级类目名称 |
| `cateLevel2Id` | String | 二级类目ID |
| `cateLevel3Id` | String | 三级类目ID |
| `categoryId` | String | 类目ID |
| `categoryIdPath` | String | 类目路径（tab分隔） |
| `status` | String | 商机状态（`ONLINE`） |
| `source` | String | 来源（`tb`=淘宝） |
| `deliveryChannel` | String | 投放渠道（`supply`=供给侧） |
| `businessCodes` | String | 业务编码 |
| `opportunityType` | String | 商机类型（`growth`=增长） |
| `opportunityLevel` | int | 商机等级 |
| `buyerDemandSignal` | String | 买家需求信号（`low`/`medium`/`high`） |
| `supplyJudgmentSignal` | String | 供给判断信号 |
| `transactionSignal` | String | 交易信号 |
| `chooseMode` | String | 选品模式（`算法`） |
| `matchType` | String | 匹配类型（`normal`） |
| `tagInfo` | String | 标签信息（tab分隔） |
| `startDate` | long | 开始时间（毫秒时间戳） |
| `endDate` | long | 结束时间（毫秒时间戳） |
| `gmtCreate` | long | 创建时间（毫秒时间戳） |
| `gmtModified` | long | 修改时间（毫秒时间戳） |
| `creator` | String | 创建人 |
| `modifier` | String | 修改人 |
| `owner` | String | 负责人 |
| `isAutoApply` | String | 是否自动应用（`Y`/`N`） |
| `uniqueClusterId` | String | 唯一聚类ID |
| `extendInfo` | String | **扩展信息（JSON字符串，见下方）** |
| `trackInfo` | Object | 追踪信息 |

### extendInfo 关键字段（JSON字符串，需解析）

| 字段 | 类型 | 说明 |
|------|------|------|
| `item_title` | String | 商品标题 |
| `item_url` | String | 商品链接 |
| `item_picts` | String | 商品图片URL（逗号分隔） |
| `brand_name` | String | 品牌名称 |
| `cate_path_name` | String | 类目路径名称（如 `童装>童裤`） |
| `cate_lv1_name` | String | 一级类目名称 |
| `cpv_mapping` | String | 属性映射（分号分隔） |
| **`average_final_price`** | **Number** | **下游高成交价格** |
| **`expose_sum_30`** | **String** | **求购数目（近30天曝光量）** |
| `click_sum_30` | String | 近30天点击量 |
| `pay_amt_30` | String | 近30天成交金额（指数化） |
| `pay_amt_7` | Number | 近7天成交金额 |
| `pay_amt_1` | Number | 近1天成交金额 |
| `quantity_30` | String | 近30天成交件数 |
| `quantity_7` | String | 近7天成交件数 |
| `ord_count_30` | String | 近30天订单数 |
| `ord_count_7` | String | 近7天订单数 |
| `ord_count_1` | String | 近1天订单数 |
| `require_index` | Number | 需求指数 |
| `supply_index` | Number | 供给指数 |
| `require_supply_rate` | Number | 需供比（越大代表供不应求） |
| `cluster_1688_itm_cnt` | String | 1688同款商品数量 |
| `cluster_byr_cnt_1m` | String | 近1月买家数 |
| `cluster_se_ipv_1m` | String | 近1月搜索IPV |
| `growth_score` | String | 增长分数 |
| `ppdx_score` | String | 品牌度分数 |
| `opp_sell_points` | String | 商机卖点（如 `下游趋势新品`） |
| `serviceRequestInfoMap` | String | 服务要求（如 `72小时发货 / 1件起批包邮`） |
| `priceRequestInfoMap` | String | 价格要求（如 `≤57.67元`） |
| `is_spid_new` | String | 是否新品（`Y`/`N`） |
| `is_brand_itm` | String | 是否品牌商品（`Y`/`N`） |
| `sku_info` | String | SKU信息（JSON字符串） |
| `opp_statistics` | String | 商机统计数据（JSON字符串） |

---

## 输出格式

### Skill 提取字段

Skill 层只提取以下关键字段返回给用户：

| 提取字段 | 来源 | 说明 |
|----------|------|------|
| `title` | `data[].title` | 商机标题 |
| `pictUrlList` | `data[].pictUrlList` | 商品图片列表 |
| `demandCount` | `extendInfo.expose_sum_30` | 求购数目（近30天） |
| `averagePrice` | `extendInfo.average_final_price` | 下游高成交价格 |
| `categoryName` | `data[].cateLevel1Name` | 一级类目名称 |
| `oppItemId` | `data[].oppItemId` | 商品ID（可拼接商品链接） |

### 成功

```json
{
  "success": true,
  "markdown": "",
  "data": {
    "totalCnt": "2000",
    "pageNo": 1,
    "pageSize": 20,
    "data": [
      {
        "title": "商机标题",
        "pictUrlList": ["图片URL1", "图片URL2"],
        "demandCount": "1234",
        "averagePrice": "5767",
        "categoryName": "女装",
        "oppItemId": 1032857514520
      }
    ]
  }
}
```

### 失败 — AK 未配置

```json
{
  "success": false,
  "markdown": "❌ AK 未配置，无法查询商机推荐。",
  "data": {}
}
```

### 失败 — 其他异常

```json
{
  "success": false,
  "markdown": "❌ 错误描述信息",
  "data": {}
}
```

---

## Agent 处理流程

```
1. 用户表达查看商机/市场机会的意图
2. 从用户消息中提取筛选条件：关键词、类目（可选）
3. 如果用户提供了类目中文名称，代码会自动转换为类目 ID
4. 执行 python3 {baseDir}/cli.py 1688_opp_recommend [--keyword <关键词>] [--categoryId <类目>] [--pageNo <页码>] [--pageSize <条数>]
5. 检查输出：
   - success=true → 将商机列表以易读格式展示给用户（标题、类目、求购数、参考价格等）
   - success=false → 原样输出错误信息
6. 如有更多结果，提示用户可翻页查看
```

---

## 支持的一级类目

只支持一级类目筛选，支持输入类目中文名称（自动转换为ID）或直接输入类目ID。

| 类目ID | 类目名称 |
|--------|----------|
| `67` | 办公、文化 |
| `1038378` | 鞋 |
| `311` | 童装 |
| `312` | 内衣 |
| `54` | 服饰配件、饰品 |
| `1813` | 玩具 |
| `10166` | 女装 |
| `2` | 食品酒水 |
| `122916001` | 宠物及园艺 |
| `122916002` | 汽车用品 |
| `58` | 灯饰照明 |
| `10165` | 男装 |
| `57` | 电子元器件 |
| `53` | 传媒、广电 |
| `70` | 安全、防护 |
| `68` | 包装 |
| `7` | 数码、电脑 |
| `5` | 电工电气 |
| `4` | 纺织、皮革 |
| `1042954` | 箱包皮具 |
| `65` | 机械及行业设备 |
| `59` | 五金、工具 |
| `8` | 化工 |
| `55` | 橡塑 |
| `201346017` | 建材 |
| `64` | 环保 |
| `10208` | 仪器仪表 |
| `15` | 居家日用品 |
| `201547801` | 日用餐厨饮具 |
| `201547901` | 收纳清洁用具 |
| `96` | 家纺家饰 |
| `97` | 美容护肤/彩妆 |
| `6` | 家用电器 |
| `13` | 家装建材 |
| `12` | 交通运输 |
| `10` | 能源 |
| `1` | 农业 |
| `71` | 汽摩及配件 |
| `509` | 通信产品 |
| `9` | 冶金矿产 |
| `66` | 医药、保养 |
| `72` | 印刷 |
| `18` | 运动户外 |
| `1426` | 机床 |
| `69` | 商务服务 |
| `2829` | 二手设备转让 |
| `2805` | 加工 |
| `130822220` | 个护/家清 |
| `130823000` | 成人用品 |
| `130822002` | 餐饮生鲜 |
| `123614001` | 钢铁 |
| `202052814` | 新能源 |

---

## 异常处理

| 场景 | Agent 应对 |
|------|-----------|
| AK 未配置 | 引导用户执行 `cli.py configure YOUR_AK` 配置 AK |
| 类目无法识别 | 提示用户输入正确的类目 ID 或中文名称 |
| 无搜索结果 | 提示用户尝试更换关键词或类目 |
| 接口返回格式异常 | 提示"格式异常，请稍后重试" |
| 其他运行时异常 | 原样输出错误信息 |

通用 HTTP 异常（400/401/429/500）处理见 `references/common/error-handling.md`。
