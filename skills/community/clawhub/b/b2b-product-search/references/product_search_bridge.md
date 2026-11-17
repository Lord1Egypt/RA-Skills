# product_search 接口契约

商品检索 Skill 的唯一取数接口。本文件独立可读，SKILL.md 不重复接口细节。

## 优先用脚本

日常调用走 `scripts/search.sh`（见 SKILL.md），它已封装地址、来源标识、JSON 转义与错误处理。本文件是底层契约，供脚本不可用时手动调、或需要核对字段口径时查阅。

## 端点

```
POST https://gwgp-zmtc8kkxxzw.i.bdcloudapi.com/skill_api/product_search
Content-Type: application/json
```

- 当前无需凭证，直接调用即可；地址已内置，用户无需配置环境变量。
- 若返回 401，说明服务端启用了凭证校验，应提示用户更新 skill 版本，而不是猜测凭证重试。

## 入参

- `query`（string，必填）：**只含商品词、用途、规格型号**，如 `"工业冷水机 注塑冷却 5HP"`。不要把预算金额、地域词写进来（"1万以内""上海的"会让站内召回归零），这些用下面的结构化参数传。
- `category_id`（string，可选）：品类 ID / 品类关键词。仅对站内商品生效（全网商品无品类字段，不因此被剔除）。
- `price_min`（float，可选）：最低价（元），`0` 表示不限。
- `price_max`（float，可选）：最高价（元）。
- `location`（string，可选）：发货地偏好，如 `"河北唐山"`。匹配时忽略“省/市/区/县”，双向包含即命中（`河北` 命中 `河北唐山`）。
- `output_format`（string，可选）：`text` / `markdown` / `html`，默认 `markdown`。非法值回落 `markdown`。
- `page_size`（int，可选）：返回条数，默认 10，最大 20。

## 出参

```json
{
  "code": 0,
  "message": "success",
  "data": {
    "total": 128,
    "items": [
      {
        "fullName": "工业冷水机 5匹 注塑冷却 风冷式",
        "picUrl": "https://…",
        "jumpUrl": "https://…",
        "price": "7800",
        "pCurrency": "元",
        "unit": "台",
        "minValue": 1,
        "allowPurchase": true,
        "fullProviderName": "北京某某设备",
        "location": "河北唐山",
        "shopScoreV3": 4.6,
        "isOtherSource": false,
        "sourcePlatform": "爱采购",
        "sourcePlatformLogo": "https://…"
      }
    ],
    "content": "…已按 output_format 渲染好的候选清单…"
  }
}
```

- `total`：过滤后的候选总数；`items`：本次返回的那一页（≤ `page_size`）。
- `content`：可直接呈现给用户的清单文本，已包含“以上为平台展示价，实际成交价以供应商确认为准。”以及命中的兜底提示（来源未接通 / 超出条数上限 / 结果为空）。
- `items` 字段固定为上表 14 个，字段值可能为空字符串（表示该项未取到），键不会缺失。
- `jumpUrl` 是商品详情页直链，爱采购站内的链接会带一个渠道参数（`from=aibotskill_...`）用于统计来源。**原样输出，不要改写、截短、去参数或换成短链**，否则来源统计会断。

不出参的字段（按 MRD【附录】“对外披露=❌”）：`id`、`xzhid`、`sv_cr`、`isMapMember`、`cellNumber`、`contact_info`、`solution`、`select_param`、`category`、`attrs`。联系方式一律不直出，用户点 `jumpUrl` 到详情页查看。`correlationInfo`（推荐匹配度）属采购需求匹配 Skill，本接口不返回。

## 返回码

- `0`：成功（含 `total=0` 的空结果，`data.content` 已带“结果为空”话术）。
- `400`：`query` 为空。`data.content` 为“需求太含糊”话术。
- `401`：凭证缺失、校验失败，或服务端未配置凭证。
- `503`：两路数据源都没接通。`data.content` 为“××来源本次未接通”话术，不返回任何商品。

## 服务端行为（便于解释结果）

- 取数来源：爱采购站内在售商品 ∥ 全网商品（1688 / 京东 / 米思米 / 西域），两路并发；任一路失败或超时只降级为空集，并在 `data.content` 里如实说明。来源通过 `sourcePlatform` 字段随每条结果返回，非爱采购站内且未授权具名的渠道统一标记为「合作站点」。
- 站内商品会补 `minValue`（起订量）、`allowPurchase`（是否支持在线交易）、`location`（发货地/店铺注册地）、`shopScoreV3`（店铺分）；全网商品这些字段多为空，缺失即留空并由调用方标注「该项未取到」。
- 排序：站内在前、全网在后；传了预算时同渠道内按价格升序（预算贴合度），未传预算时保留各渠道的相关度顺序。
- 过滤：
  - 传了 `price_min`/`price_max` → 价格解析不出数值的商品被剔除（无法证明落在预算内）；`3.2万` 这类写法按 32000 处理，`100-200` 取下界 100。
  - 传了 `location` → 商品有发货地且不命中的被剔除；发货地为空的不剔除（无据可判，但会在清单里标 `该项未取到`）。
  - `fullName` 或 `jumpUrl` 为空的条目一律丢弃。
- 全链路无 LLM 调用，结果对同一入参稳定可复现。单次请求通常耗时数秒（多路检索并发取数），调用方超时建议设 20s 以上。

## 联调示例

```bash
curl -s -X POST "https://gwgp-zmtc8kkxxzw.i.bdcloudapi.com/skill_api/product_search" \
  -H "Content-Type: application/json" \
  -H "X-App-Source: workbuddy" \
  -d '{"query":"工业冷水机 注塑冷却","price_max":10000,"location":"河北","output_format":"markdown","page_size":10}'
```
