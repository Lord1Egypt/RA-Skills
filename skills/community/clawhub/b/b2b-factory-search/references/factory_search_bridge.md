# factory_search 接口契约

厂家检索 Skill 的唯一取数接口。本文件独立可读，SKILL.md 不重复接口细节。

## 优先用脚本

日常调用走 `scripts/search.sh`（见 SKILL.md），它已封装地址、来源标识、JSON 转义与错误处理。本文件是底层契约，供脚本不可用时手动调、或需要核对字段口径时查阅。

## 端点

```
POST https://gwgp-zmtc8kkxxzw.i.bdcloudapi.com/skill_api/factory_search
Content-Type: application/json
```

- 当前无需凭证，直接调用即可；地址已内置，用户无需配置环境变量。
- 若返回 401，说明服务端启用了凭证校验，应提示用户更新 skill 版本，而不是猜测凭证重试。
- 也支持 `GET`（参数走 query string），仅用于联调。

## 入参

- `query`（string，必填）：**只含主营产品词与加工能力**，如 `"铝合金压铸件 定制加工"`。区域不要写进来，用 `location`。
- `location`（string，可选）：厂家所在地/产能区域，如 `"江苏苏州"`。**这一项是硬过滤**，匹配时忽略"省/市/区/县"。
- `capability`（string，可选）：加工/合作方式，如 `"OEM代工"`、`"来图定制"`、`"小批量打样"`。
- `certification`（string，可选）：资质认证，多个以逗号分隔，如 `"SC认证,ISO9001"`。
- `business_type`（string，可选）：`factory`（生产厂家）/ `trader`（贸易商）。
- `with_products`（int/bool，可选）：是否查店内在售商品，**默认 `0`**（关闭）。传 `1` 会对前 3 家各发一次店内检索，多花几秒。
- `output_format`（string，可选）：`text` / `markdown` / `html`，默认 `markdown`。
- `page_size`（int，可选）：返回家数，默认 10，最大 50。**完整工商档案只对前 10 家取数**，更靠后的只带召回侧信息（`fullname`/`mainProduct`/`location`/`shopScoreV3`），其余字段为空——这样 `page_size=50` 与 `page_size=10` 耗时相当。

**重要**：`capability`、`certification`、`business_type` 这三项**只并入检索词参与相关性排序，不做服务端硬过滤**（站内商家检索不支持按这些条件筛选）。命中时 `data.content` 里会带一句说明，转述时必须如实带上，不能说成"已按 SC 认证筛过"。

## 出参

```json
{
  "code": 0,
  "message": "success",
  "data": {
    "total": 12,
    "factories": [
      {
        "fullname": "苏州某某精密压铸有限公司",
        "homePage": "https://…（带渠道参数）",
        "logo": "https://…",
        "shopScoreV3": 4.7,
        "mainProduct": "铝合金压铸件,精密压铸模具",
        "location": "江苏苏州",
        "establishDate": "2011-05-18",
        "regCapital": "1000万元",
        "status": "存续",
        "industry": "金属制品业",
        "personNum": "100-499人",
        "equipmentNum": 32,
        "bpArea": "8000㎡",
        "patentNum": 12,
        "platform_num": 3,
        "brandList": ["某某精密"],
        "oem_brand": "某某车灯",
        "winningBidsNum": 5,
        "prodNum": 386,
        "industry_imgs": ["https://…"],
        "shopLicense": "https://…",
        "vr3d": ["https://…"],
        "profileInfo": [{ "name": "登记机关", "value": "苏州市市场监督管理局" }],
        "prodList": [
          {
            "fullName": "铝合金压铸件 来图定制",
            "jumpUrl": "https://…（带渠道参数）",
            "picUrl": "https://…",
            "price": "12.5",
            "pCurrency": "元",
            "unit": "件"
          }
        ],
        "platform": "爱采购"
      }
    ],
    "content": "…已按 output_format 渲染好的候选厂家清单…"
  }
}
```

- `total`：过滤后的候选总数；`factories`：本次返回的那一页（≤ `page_size`）。
- `content`：可直接呈现给用户的清单。`markdown` 形态是「概览表 + 各家档案明细」两段式，厂家名与"入口"列指向店铺页；已包含免责说明与命中的兜底话术。
- 字段值可能为空（表示该项未取到），键不会缺失。`content` 里已回填 `该项未取到`。
- `homePage`、`prodList[].jumpUrl` 带渠道参数（`from=aibotskill_...`）用于统计来源。**原样输出，不要改写、截短或去参数。**

不出参的字段（按字段口径表"对外披露=❌"）：`xzhid`、`cpaMember`、`cpaDuration`、`seniorRealType`、`isMapMember`、`isAceMember`、`is_consumption_factory`、`contact_info`、`solution`、`prodList[].id`。联系方式一律不直出，用户点 `homePage` 到店铺页查看。

## 返回码

- `0`：成功（含 `total=0` 的空结果，`data.content` 已带"没查到"话术与覆盖范围说明）。
- `400`：`query` 为空，`data.content` 为"诉求太含糊"话术。
- `401`：服务端启用了凭证校验而请求未带对。
- `503`：厂家档案数据源没接通，不返回任何厂家。

## 服务端行为（便于解释结果）

- 取数来源：爱采购站内商家档案（工商信息、能力标签、店内在售商品）。**只覆盖站内商家**，站外工厂无数据。
- 流程：商家检索召回（最多 50 家）→ 相关性过滤 → `location` 过滤 → **截断到 `page_size`** → **前 10 家**逐家并发拉工商档案（每家两路数据源，整体 8s 超时）→ 归一化。
- 分级取数：第 11 家往后不发档案请求，只用召回时已有的字段；档案超时的厂家同样降级而不是丢弃。`data.content` 里会说明有几家是简版。
- `location` 过滤后一家不剩时会降级为不过滤（档案地址字段不齐，省级地名常筛空），`data.content` 里会明确说明"地域条件没能筛住"。
- 工商档案取数有 6s 整体超时。超时或取不到的厂家不丢弃，降级为只带召回侧信息（名称/主营产品/所在地），档案字段留空，`data.content` 里会说明有几家降级了。
- 店内在售商品默认不查（`with_products=0`）；开启后只查前 3 家，其余 `prodList` 为空数组。
- 排序：按召回相关性，不做实力评级、不按规模重排。
- 全链路无 LLM 调用，结果对同一入参稳定可复现。单次请求约 5-8 秒（与 `page_size` 关系不大，因为只对前 10 家拉档案；开 `with_products` 再加几秒），调用方超时建议设 30s 以上。

## 联调示例

```bash
curl -s -X POST "https://gwgp-zmtc8kkxxzw.i.bdcloudapi.com/skill_api/factory_search" \
  -H "Content-Type: application/json" \
  -H "X-App-Source: workbuddy" \
  -d '{"query":"铝合金压铸件 定制加工","location":"江苏苏州","page_size":10}'
```
