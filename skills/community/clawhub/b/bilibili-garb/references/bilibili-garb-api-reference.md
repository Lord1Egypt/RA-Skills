# B站个性装扮 API 参考文档

## 目录

1. [认证与签名](#认证与签名)
2. [公开接口](#公开接口)
3. [认证接口](#认证接口)
4. [数据获取流程](#数据获取流程)
5. [注意事项](#注意事项)

---

## 认证与签名

### 凭证参数

| 参数 | 说明 | 获取方式 |
|------|------|----------|
| `appkey` | 应用密钥ID | B站移动端内置，公开值 `27eb53fc9058f8c3` |
| `appsecret` | 应用密钥 | 需从B站客户端获取 |
| `access_key` | 用户授权令牌 | 从B站移动端HTTP流量抓包获取，会过期 |
| `csrf` (bili_jct) | CSRF令牌 | 从Cookie中获取 |
| `SESSDATA` | 会话凭证 | 从Cookie中获取 |
| `DedeUserID` | 用户UID | 从Cookie中获取 |

### Sign签名算法

用于需要认证的接口（benefit、asset等）。

1. 将所有请求参数（含 `appkey`, `access_key`, `csrf`, `ts`, `mobi_app`, `platform`）按**键名字典序**排序
2. 使用 `urllib.parse.urlencode(sorted_params)` 拼接为查询字符串
3. 追加 `APPSECRET`：`sign_str = query + APPSECRET`
4. 计算 MD5：`sign = md5(sign_str.encode('utf-8')).hexdigest()`
5. 将 `sign` 追加到请求参数中

### 请求示例

```python
import hashlib
import urllib.parse
import time

def calc_sign(params, appkey, access_key, csrf, appsecret):
    ts = str(int(time.time()))
    all_params = dict(params)
    all_params.update({
        "access_key": access_key,
        "appkey": appkey,
        "csrf": csrf,
        "mobi_app": "iphone",
        "platform": "ios",
        "ts": ts,
    })
    sorted_items = sorted(all_params.items())
    query = urllib.parse.urlencode(sorted_items)
    sign_str = query + appsecret
    sign = hashlib.md5(sign_str.encode("utf-8")).hexdigest()
    all_params["sign"] = sign
    return all_params
```

---

## 公开接口

以下接口无需认证（不需要access_key/sign/cookie）。

### 1. 装扮搜索

```
GET https://api.bilibili.com/x/garb/v2/mall/home/search
```

| 参数 | 类型 | 说明 |
|------|------|------|
| `key_word` | string | 搜索关键词（需URL编码） |
| `pn` | int | 页码，默认1 |
| `ps` | int | 每页数量，默认20 |
| `mobi_app` | string | `iphone` |
| `platform` | string | `ios` |
| `appkey` | string | `27eb53fc9058f8c3` |

**返回**：`data.list[]`，每项含：
- `item_id` — 商品ID
- `name` — 名称
- `state` — 状态：`active`/`ended`/`pending`
- `sale_count_desc` — 销量描述
- `properties.dlc_act_id` — 收藏集活动ID（有此项则为收藏集）
- `properties.dlc_lottery_sale_quantity` — 收藏集实际销量
- `properties.image_cover` — 封面图URL
- `properties.sale_quantity` — 套装总量
- `properties.item_stock_surplus` — 套装剩余库存

### 2. 装扮详情

```
GET https://api.bilibili.com/x/garb/v2/mall/suit/detail
```

| 参数 | 类型 | 说明 |
|------|------|------|
| `item_id` | int/string | 套装ID |
| `part` | string | 子项类型：`suit`/`emoji`/`skin`/`pendant`/`space_bg`/`loading`/`play_icon`/`thumbup`/`card_bg` |

**返回**：`data.suit_items` → 各子类型列表

**⚠️ 注意**：绝版（已下架）装扮的 `suit_items` 为空！需用 benefit 接口。

### 3. 收藏集基础信息

```
GET https://api.bilibili.com/x/vas/dlc_act/act/basic
```

| 参数 | 类型 | 说明 |
|------|------|------|
| `act_id` | int | 收藏集活动ID |
| `mobi_app` | string | `iphone` |
| `platform` | string | `ios` |
| `appkey` | string | `27eb53fc9058f8c3` |

**返回**：`data.act_title`（名称）、`data.start_time`/`end_time`、`data.lottery_list[]`、`data.total_buy_cnt`

即使收藏集已下架，此接口通常仍能返回基础信息。

### 4. DLC卡池信息

```
GET https://api.bilibili.com/x/vas/dlc_act/lottery_home_detail
```

| 参数 | 类型 | 说明 |
|------|------|------|
| `act_id` | int | 收藏集活动ID |
| `lottery_id` | int | 抽奖池ID |

**返回**：
- `data.item_list[]` — 卡池配置，每项含 `card_info`（`card_name`, `card_scarcity`）
- `data.collect_list.collect_infos[]` — 收集奖励列表
  - `redeem_item_type==3` → 头像框（`redeem_item_name`, `redeem_item_image`）

**⚠️ 关键**：DLC头像框必须从此接口获取，不能用收藏集自带的 `frame`/`frame_image` 字段。

---

## 认证接口

以下接口需要 sign 签名 + Cookie。

### 5. ⭐ 装扮权益详情（Benefit）

**绝版装扮的唯一数据源。**

```
GET https://api.bilibili.com/x/garb/v2/user/suit/benefit
```

| 参数 | 类型 | 说明 |
|------|------|------|
| `item_id` | int/string | 套装ID（DIY套装必须传biz_id） |
| `part` | string | 推荐固定传 `space_bg`（一次返回全部子项） |
| `is_diy` | string | `0` 或 `1`（DIY套装检测：item_id含横杠或非纯数字） |
| `vmid` | string | 用户UID |
| + 签名参数 | | `appkey`, `access_key`, `csrf`, `ts`, `mobi_app`, `platform`, `sign` |

**Header**：`Cookie: SESSDATA=...; bili_jct=...; DedeUserID=...`

**返回**：`data.suit_items` → 9种子项完整数据：
- `card` (0-2项)、`card_bg` (1项)、`emoji_package` (1项)
- `loading` (1项)、`pendant` (1项)、`play_icon` (1项)
- `skin` (1项)、`space_bg` (1项)、`thumbup` (1项)

每项含：`item_id`, `name`, `properties`（横竖图/视频/粉丝牌/主题色/表情列表等）

**DIY套装关键**：
- 当 `item_id` 格式为 `1775103232001-0`（含横杠）时，API的 `item_id` 参数必须传 `biz_id`（如 `409236701`），否则返回 `code=-400`
- `is_diy` 参数传 `0` 或 `1` 都可以成功（只要 `item_id` 用 `biz_id`）

**part参数优化**：
- `part` 只决定返回数据的"视角"，`suit_items` 始终包含所有9种子项
- 只需 `part=space_bg` 一次调用即可获取全部数据，无需遍历

### 6. 用户资产列表

```
GET https://api.bilibili.com/x/garb/user/asset
```

| 参数 | 类型 | 说明 |
|------|------|------|
| `part` | string | `suit` 或 `emoji_package` |
| `state` | string | `active` |
| `pn` | int | 页码 |
| `ps` | int | 每页数量 |
| + 签名参数 | | 同上 |

### 7. 用户装扮资产详情

```
GET https://api.bilibili.com/x/garb/v2/user/suit/asset
```

| 参数 | 类型 | 说明 |
|------|------|------|
| `item_id` | int | 套装ID |
| `part` | string | `suit` |
| `trial` | string | `0` |
| + 签名参数 | | 同上 |

### 8. 收藏集列表

```
GET https://api.bilibili.com/x/garb/right/collection/list
```

| 参数 | 类型 | 说明 |
|------|------|------|
| `vmid` | string | 用户UID |
| `ps` | int | 每页数量 |
| `source` | string | `collection_all_sort` |
| `order_type` | string | `1` |
| `hidden_filter` | string | `0` |
| + 签名参数 | | `access_key`, `appkey`, `ts`, `mobi_app`, `platform` |

### 9. 用户持有卡片

```
GET https://api.bilibili.com/x/vas/user/dlc/card/list
```

| 参数 | 类型 | 说明 |
|------|------|------|
| `vmid` | string | 用户UID |
| `act_id` | int | 收藏集活动ID |
| `page` | int | 页码 |
| `page_size` | int | 每页数量 |

**Header**：`Cookie: SESSDATA=...`

**返回**：`card_list[]`，每项含 `card_item.card_name`、`card_no`

### 10. 转让记录

```
GET https://api.bilibili.com/x/vas/dlc_act/transfer/listV2
```

| 参数 | 类型 | 说明 |
|------|------|------|
| `scene` | int | `1`=收到的 / `2`=送出的 |
| `transfer_status` | int | `3`=已接收 / `4`=待领取 |
| + 签名参数 | | 同上 |

---

## 数据获取流程

### 已拥有装扮(含绝版)完整信息

```
benefit API (item_id=套装biz_id, part=space_bg)
  → suit_items → 获取9种各子项的 item_id + properties
  → 如需更详细：suit/detail (子项item_id, part=对应类型)
```

### 收藏集卡片信息

```
act/basic (公开) → lottery_id 列表
lottery_home_detail (公开) → 卡池配置、稀缺度、头像框
card/list (Cookie认证) → card_no 编号
```

### 品级判别流程

1. **公开API优先**：`item_list` 的 `scarcity` 字段最可靠
   - `10` = 普通(N)
   - `20` = 稀有(R)
   - `30` = 小隐藏(SR)
   - `40` = 大隐藏(SSR)
2. **NDJSON次之**：从本地数据库的 `scarcity` 字段
3. **保守兜底**：当背包API `scarcity_rate=2` 且 `rate2_count==1` 时，**默认小隐藏(30)**，不自动升大隐藏，需用户确认

---

## 注意事项

1. **Benefit API** 是绝版装扮的唯一数据源，需 sign 签名
2. **access_key 会过期**，需定期从移动端流量抓包刷新
3. **请求间隔** 0.5-1 秒防风控
4. **DIY套装**：benefit API 的 `item_id` 参数必须传 `biz_id`，否则报 `-400`
5. **DLC头像框**：必须从 `lottery_home_detail` 获取，不能用收藏集自身的 `frame`/`frame_image`
6. **part参数**：只需 `space_bg` 一次调用返回全部9种子项，无需遍历
7. 服务器IP可能被B站部分接口封禁，benefit/sign签名接口通常可用
