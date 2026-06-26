# 选品搜索参考文档

本文档包含两种选品模式：**关键词选品**和**图搜选品**。根据用户输入自动判断使用哪种模式：
- 用户提供**图片链接或图片文件** → 图搜选品（`same_img_offer_search`）
- 用户提供**文字描述** → 关键词选品（`fx_keyword_search_selection`）

---

## 一、关键词选品

### 自然语言 → retrieveFilters 转换规则

从用户描述中提取筛选条件，组装 `retrieveFilters` 数组，每个条件格式为：
```json
{ "code": "字段key", "value": ["值"], "queryType": "操作符" }
```

### 常用 queryType

- `contains_any`：包含任意一个（用于关键词、STRING 类型多值）
- `equal`：等于（用于 Y/N 类型的 STRING 字段）
- `range`：范围查询（用于 DOUBLE/BIGINT 数值区间，value 格式: [最小值, 最大值]，null 表示不限制）

## 支持的筛选字段

| 用户描述关键词 | 字段 key | 数据类型 | 示例值 |
|---|---|---|---|
| 关键词/标题包含 | `title` | STRING | `["垃圾袋", "加厚"]` |
| 包邮 | `is_free_post` | STRING | `"Y"` |
| 支持一件代发 | `is_yjdf` | STRING | `"Y"` |
| 7天无理由退货 | `is_no_reason_to_return_7d_fx` | STRING | `"Y"` |
| 24小时发货 | `is_24hour_send_fx` | STRING | `"Y"` |
| 48小时发货 | `is_48hour_send_fx` | STRING | `"Y"` |
| 代发价格范围 | `df_price` | DOUBLE | `range: [5.0, 10.0]`（null 表示不限制） |
| 代发邮费范围 | `df_post` | DOUBLE | `range: [null, 5.0]` |
| 近30天分销订单量 | `fx_ord_cnt_30d` | BIGINT | `range: [100, null]` |
| 近30天订单量 | `ord_cnt_30d` | BIGINT | `range: [500, null]` |
| 7天内新品 | `is_7d_create` | STRING | `"Y"` |
| 30天内新品 | `is_30d_create` | STRING | `"Y"` |
| 支持密文面单（抖音/拼多多/淘宝） | `channels` | STRING | 见下方说明 |
| 退款处理快 | `is_rfd_process_fast` | STRING | `"Y"` |
| 24小时揽收率高 | `is_24h_got_rate_high` | STRING | `"Y"` |
| 48小时揽收率高 | `is_48h_got_rate_high` | STRING | `"Y"` |
| 实力工厂 | `is_shili_factory` | STRING | `"Y"` |
| 先采后付 | `is_xchf` | STRING | `"Y"` |
| 一级类目 | `cate_level1_name` | STRING | `["家居"]` |
| 二级类目 | `cate_level2_name` | STRING | `["清洁用品"]` |
| 叶子类目 | `cate_name` | STRING | `["垃圾袋"]` |
| 淘宝商品体验分高 | `is_tb_pxi_score_high` | STRING | `"Y"` |
| 货描相符大于均值 | `is_score_hm_high` | STRING | `"Y"` |
| 响应速度大于均值 | `is_score_xy_high` | STRING | `"Y"` |
| 发货速度大于均值 | `is_score_fh_high` | STRING | `"Y"` |

### channels 字段特殊说明

`channels` 的 `value` 是一个**渠道枚举数组**，枚举值为：
- `dy`：抖音
- `pdd`：拼多多
- `tb`：淘宝
- `jd`：京东
- `xhs`：小红书

与其他 STRING 字段不同，`channels` 使用 `and` 作为 `queryType`，且 `value` 可同时包含多个渠道（表示"支持这些渠道中的任意一个"）。

**示例**：用户说"支持抖音和拼多多密文面单的商品"，对应：
```json
{ "code": "channels", "value": ["dy", "pdd"], "queryType": "and" }
```

### 价格范围查询特殊说明

`df_price`、`df_post` 等数值字段支持 `range` queryType，用于指定价格区间。`value` 格式为 `[最小值, 最大值]`，`null` 表示不限制该方向。

**示例**：
- 代发价格在 5-10 元之间：`{"code": "df_price", "value": [5.0, 10.0], "queryType": "range"}`
- 代发价格不超过 10 元：`{"code": "df_price", "value": [null, 10.0], "queryType": "range"}`
- 代发价格 5 元以上：`{"code": "df_price", "value": [5.0, null], "queryType": "range"}`

## 分页与排序参数

| 参数 | 类型 | 说明 | 默认值 |
|------|------|------|--------|
| `pageNo` | int | 页码，从 1 开始 | 1 |
| `pageSize` | int | 每页数量，最大 50 | 20 |
| `rankType` | string | 排序方向：`ASC` 升序 / `DESC` 降序 | 不传则默认排序 |
| `rankField` | string | 排序字段，如 `df_price`、`fx_ord_cnt_30d`、`cate_id` 等 | 不传则默认排序 |

## 请求示例

用户说"帮我找包邮且支持一件代发的垃圾袋，按代发价格从低到高"：

```
POST /api/fx_keyword_search_selection/1.0.0
Body:
{
  "params": "{\"retrieveFilters\":[{\"code\":\"title\",\"value\":[\"垃圾袋\"],\"queryType\":\"contains_any\"},{\"code\":\"is_free_post\",\"value\":\"Y\",\"queryType\":\"equal\"},{\"code\":\"is_yjdf\",\"value\":\"Y\",\"queryType\":\"equal\"}],\"pageNo\":1,\"pageSize\":20,\"rankType\":\"ASC\",\"rankField\":\"df_price\"}"
}
```

**注意**：`params` 字段是整个 JSON 对象**序列化后的字符串**，不是嵌套对象。

## 返回结构

```json
{
  "success": true,
  "model": {
    "total": 1486,
    "data": [
      {
        "offerId": "894529405810",
        "title": "户外便携式懒人带枕头充气沙发水上沙滩草地公园空气床可折叠睡袋",
        "dfPrice": 22.0,
        "dfPost": 2.53,
        "offerPic": "https://cbu01.alicdn.com/...",
        "fxOrdCnt30d": "120",
        "ordCnt30d": "280",
        "ciphertextInfoList": [
          { "name": "淘宝(菜鸟)", "key": "thyny" },
          { "name": "抖音", "key": "douyin" },
          { "name": "拼多多", "key": "pinduoduo" }
        ],
        "baseServiceInfo": {
          "isFreePost": false,
          "isYjdf": true,
          "isNoReasonToReturn7dFx": true
        }
      }
    ]
  }
}
```

## 注意事项

- 商品数组在 `model.data`，**不是** `result.data`
- `model.total` 是符合条件的商品总数
- `ciphertextInfoList` 是该商品支持的密文面单渠道列表，`key` 值为 `douyin`/`pinduoduo`/`thyny`（淘宝菜鸟）

## 选品后处理规则

1. 从 `model.data` 数组中取前 3-5 个商品作为候选列表
2. **自动触发选品决策分析**（详见下方流程）
3. 综合展示选品数据 + 参谋分析结果给用户
4. 询问用户确认要铺货的商品（可全选或选择部分）
5. 收集确认的商品 `offerId` 列表，进入后续流程

## 选品决策分析流程

选品返回结果后，**自动**对候选商品批量查询分销参谋数据，综合分析后给出推荐理由。

### 步骤

1. 对每个候选商品调用分销参谋接口查询详细数据：
   ```bash
   python3 scripts/capabilities/offer_info/cmd.py --offer-id "{offerId}" --decision
   ```
2. 综合选品数据（价格、销量、渠道）+ 参谋数据（服务保障、揽收率、铺货分销商数等），为每个商品生成推荐分析

### 推荐维度（正面因素）

| 维度 | 数据来源 | 判断标准 |
|------|----------|----------|
| 价格优势 | 选品 `dfPrice` + 参谋 `priceInInfo` | 一件包邮价低、分销专属价有折扣 |
| 包邮支持 | 参谋 `priceInInfo.onePieceFreePostage` | 一件包邮 > 多件包邮 > 不包邮 |
| 渠道匹配 | 参谋 `supportList` | 支持用户目标渠道的密文面单 |
| 高体验分 | 参谋 `downstreamPerformance.highExperienceScoreList` | 在目标渠道有高体验分 |
| 高履约率 | 参谋 `downstreamPerformance.highPerfectLgtRateList` | 在目标渠道有高完美履约率 |
| 服务保障 | 参谋 `protectionInfoList` | 有退换货保障、晚揽必赔等 |
| 代发数据 | 参谋 `adviseList` | 近30天代发量大、揽收率高 |
| 分销品 | 参谋 `alreadyUpgrade` | 已升级为分销品，铺货更顺畅 |

### 风险维度（负面因素）

| 维度 | 数据来源 | 判断标准 |
|------|----------|----------|
| 品牌未授权 | 参谋 `brandInfo.isBrandOffer` + `isAuth` | 品牌商品但未获得授权，铺货可能失败 |
| 运费高 | 参谋 `freightInfo` | 非包邮且运费高，影响利润 |
| 起批量高 | 参谋 `priceInInfo.startNum` | 起批量过高不适合小卖家 |
| 渠道不匹配 | 参谋 `supportList` | 不支持用户目标渠道 |
| 包邮排除区域多 | 参谋 `priceInInfo.excludeAreaList` | 排除区域过多影响覆盖范围 |

### 展示格式

对每个候选商品输出：

```
### 商品 {offerId}：{title}

**主图**：![商品主图]({offerPic}_300x300.jpg)

**商品链接**：[点击查看详情](https://detail.1688.com/offer/{offerId}.html)

**推荐指数**：⭐⭐⭐⭐⭐（5/5）

**选品数据**：
- 代发价 ¥{dfPrice} | 邮费 ¥{dfPost} | 近30天分销订单 {fxOrdCnt30d}

**参谋分析**：
- ✅ 一件包邮，价格有竞争力
- ✅ 支持抖音、拼多多等 6 个渠道密文面单
- ✅ 近30天代发 9000+，48h揽收率 100%
- ✅ 有官方仓退货、晚揽必赔保障

**风险提示**：
- ⚠️ 包邮排除区域：新疆、西藏、海南等偏远地区

**综合建议**：强烈推荐铺货
```

### 商品 ID 超链接规范

**⚠️ 重要：所有商品 ID 和商品标题必须添加超链接！**

在展示商品时，以下位置必须使用 Markdown 超链接格式，链接到 1688 商品详情页：

1. **商品标题**：`[{title}](https://detail.1688.com/offer/{offerId}.html)`
2. **商品 ID**：`[{offerId}](https://detail.1688.com/offer/{offerId}.html)`
3. **对比表格中的商品 ID**：`[{offerId}](https://detail.1688.com/offer/{offerId}.html)`

**示例**：
```markdown
### 商品 1️⃣：[跨境户外便携折叠月亮椅](https://detail.1688.com/offer/891509457275.html)
**商品 ID**：[891509457275](https://detail.1688.com/offer/891509457275.html)

| 维度 | 商品 1 | 商品 2 |
|------|--------|--------|
| 商品 ID | [891509457275](https://detail.1688.com/offer/891509457275.html) | [1015781448056](https://detail.1688.com/offer/1015781448056.html) |
```

**链接格式**：`https://detail.1688.com/offer/{offerId}.html`

### 商品图片尺寸规范

**⚠️ 重要：所有商品主图必须严格使用 300x300 像素尺寸！**

在展示商品主图时，**必须**在图片 URL 后添加 `_300x300.jpg` 后缀，以确保图片尺寸统一和加载性能。

**正确格式**：
```markdown
**主图**：![商品主图]({offerPic}_300x300.jpg)
```

**示例**：
```markdown
![商品主图](https://cbu01.alicdn.com/img/ibank/O1CN01NoWhxy1r9ohPnnrdH_!!2218782155589-0-cib.jpg_300x300.jpg)
```

**错误示例**（禁止使用）：
```markdown
<!-- 错误：使用原图尺寸，加载慢且显示不一致 -->
![商品主图](https://cbu01.alicdn.com/img/ibank/O1CN01NoWhxy1r9ohPnnrdH_!!2218782155589-0-cib.jpg)

<!-- 错误：使用其他尺寸，不符合规范 -->
![商品主图](https://cbu01.alicdn.com/img/ibank/O1CN01NoWhxy1r9ohPnnrdH_!!2218782155589-0-cib.jpg_500x500.jpg)
```

**规范要求**：
- 统一使用 `_300x300.jpg` 后缀
- 不得使用原图或其他尺寸
- 确保所有商品图片大小一致，提升展示效果

## 铺货后续触发逻辑

铺货完成后，如果铺货日志显示部分商品已成功铺货：

1. 检查选品候选列表中是否还有未铺货的商品
2. 如果有，主动询问用户：「还有 N 个商品未铺货，是否继续铺货？」
3. 用户确认后，跳过已铺货的商品，继续铺货剩余商品
4. 重复直到所有商品处理完毕或用户主动停止

---

## 二、图搜选品

### 接口信息

- **工具名**：`same_img_offer_search`
- **用途**：通过图片搜索相似的分销商品
- **请求体**：直接传 JSON 字符串（非 `{"params": "..."}` 包装）

### 调用方式

```bash
# 通过图片 URL 搜索
python3 scripts/capabilities/select_offer/cmd.py --image-url "https://example.com/sample.jpg"

# 通过图片 Base64 搜索
python3 scripts/capabilities/select_offer/cmd.py --image-base64 "/9j/4AAQSkZJRgABAQAA..."

# 图搜 + 辅助关键词
python3 scripts/capabilities/select_offer/cmd.py --image-url "https://example.com/sample.jpg" --keyword "连衣裙"

# 图搜 + 主体圈选
python3 scripts/capabilities/select_offer/cmd.py --image-url "https://example.com/sample.jpg" --region "100,100,300,400"
```

### 图片参数说明

| 参数 | 说明 |
|------|------|
| `imageAddress` | 图片 URL 地址，用户提供图片链接时使用 |
| `imageBase64` | 图片 Base64 编码，用户直接提供图片时使用 |
| `region` | 主体圈选区域坐标（可选），用于指定图片中要搜索的主体 |

> **二选一**：`imageAddress` 和 `imageBase64` 至少传一个。用户给链接就用 `imageAddress`，用户给图片就转 Base64 用 `imageBase64`。

### 请求参数

| 字段 | 类型 | 必填 | 默认值 | 说明 |
|------|------|:----:|:------:|------|
| `searchMode` | String | 是 | - | 固定传 `IMAGE_SEARCH` |
| `sceneCode` | String | 是 | `fxyx` | 场景代码 |
| `imageParam` | Object | 是 | - | 图搜参数（含 imageAddress/imageBase64/region） |
| `pageIndex` | int | 否 | 1 | 页码 |
| `pageSize` | int | 否 | 20 | 每页大小，最大 50 |
| `keyword` | String | 否 | - | 辅助关键词（可选） |
| `filter` | Array | 否 | `[]` | 筛选条件列表（IndicatorModel 格式） |
| `sortModel` | Object | 否 | - | 排序条件：`{"field": "price", "desc": true}` |
| `terminal` | String | 否 | `PC` | 端标识 |

### 筛选条件（IndicatorModel）

| 字段 | 类型 | 说明 |
|------|------|------|
| `field` | String | 指标字段名 |
| `type` | String | 指标类型 |
| `value` | String | 指标值 |
| `invert` | Boolean | 是否取反 |

### 返回结构

```json
{
  "bizSuccess": true,
  "total": 100,
  "pageNum": 1,
  "pageSize": 20,
  "totalPage": 5,
  "data": [
    {
      "offerId": 7890123456,
      "title": "2026新款夏季女装连衣裙",
      "offerPic": "https://cbu01.alicdn.com/img/xxx.jpg",
      "price": 39.9,
      "yjby": true,
      "ciphertextInfoList": [],
      "dfSalesForSort": null
    }
  ],
  "extendInfo": {
    "yoloCropRegion": "0.1,0.2,0.8,0.9"
  }
}
```

### 返回字段说明

| 字段 | 类型 | 说明 |
|------|------|------|
| `offerId` | Long | 商品 ID |
| `title` | String | 商品标题 |
| `offerPic` | String | 商品图片链接 |
| `price` | Double | 商品展示价格（元） |
| `yjby` | Boolean | 是否一件代发包邮（为 true 时 price 为包邮价） |
| `ciphertextInfoList` | Array | 密文面单渠道信息 |
| `dfSalesForSort` | Long | 月代发销量（精确值，用于排序） |

> **图搜特有**：使用主体圈选（`region`）时，`extendInfo` 中会包含 `yoloCropRegion`，表示 YOLO 模型识别的主体裁剪区域。

### 图搜后处理规则

1. 从返回的 `data` 数组中取前 3-5 个商品作为候选列表
2. 展示每个商品的：图片、标题、价格、是否包邮、支持的渠道
3. **自动触发选品决策分析**（同关键词选品流程）
4. 询问用户确认要铺货的商品

### 注意事项

- 图搜返回的 `bizSuccess` 字段（非 `success`），代码层已自动适配
- 图搜超时设置为 60 秒（比关键词选品更长，因为图片识别耗时更久）
- 图搜结果的商品字段（`offerId`、`title`、`price` 等）与关键词选品一致，后续铺货流程完全相同
