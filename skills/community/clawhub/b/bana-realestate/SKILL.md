---
name: bana-real-estate
description: 查询巴娜房地产信息 API，覆盖支持城市、小区、二手房、租房和新房。用于用户希望查询中国城市房产数据、按行政区或商圈筛选二手房、搜索二手房或租房、查看小区行情或获取新房推荐时；也用于生成或排查该 API 的调用请求。涉及收费接口时必须在调用前告知用户单次费用，但无需等待用户确认。
---

# 巴娜房产

通过巴娜房地产信息 API 获取 58 安居客数据。优先使用随附客户端执行调用，以统一参数校验、凭证保护和费用告知。

## 执行流程

1. 明确用户需要的数据类型、城市、筛选范围和页码。城市应使用短码，例如广州 `gz`、北京 `bj`、上海 `sh`、深圳 `sz`。
2. 不确定城市短码或支持范围时，先调用免费的 `getCities`。不要猜测短码。
3. 根据下表选择最窄且匹配用户意图的方法。`page` 可省略且默认为 `1`；完整参数和响应说明见随附的接口调用说明。
4. 免费方法可直接调用。收费方法调用成功每次扣费 `0.4 元`；执行前告知用户方法、调用次数和预计费用，告知后即可调用，无需询问或等待用户确认。
5. 运行 `scripts/realestate_api.py`。如果没有已保存的凭证，直接在对话中请用户提供 AppID 和 SecureKey；收到后传给客户端，默认保存并用于后续查询。不要要求用户配置环境变量或进入终端。若用户没有凭证，明确提醒前往巴娜 Skill 技能中心 <https://wxpub.aibana.art> 注册并生成。
6. 接口服务端单线程处理请求，可能需要排队。客户端默认等待 `180 秒`；不要因短时间没有响应而提前终止或重复调用，也不要并行发起多个请求。
7. 基于返回数据回答，标明城市、筛选条件、页码和数据来源。不要把缺失字段推断成事实，也不要承诺数据实时性。

## 方法选择

| 用户意图 | method | 业务参数 | 费用 |
|---|---|---|---|
| 查看支持城市 | `getCities` | 无 | 免费 |
| 查看城市小区 | `getCommunityList` | `city`, `page` | 免费 |
| 按关键词搜索小区 | `searchCommunity` | `city`, `keyword`, `page` | 0.4 元 |
| 查看城市配置 | `getCity` | `city` | 0.4 元 |
| 按行政区查看小区 | `getCommunityListByDistrict` | `city`, `district`, `page` | 0.4 元 |
| 查看城市二手房 | `getErshoufangList` | `city`, `page` | 0.4 元 |
| 按行政区查看二手房 | `getErshoufangListByDistrict` | `city`, `district`, `page` | 0.4 元 |
| 按商圈查看二手房 | `getErshoufangListByBizcircle` | `city`, `bizcircle`, `page` | 0.4 元 |
| 按关键词搜索二手房 | `searchErshoufang` | `city`, `keyword`, `page` | 0.4 元 |
| 查看城市租房 | `getRentalList` | `city` | 0.4 元 |
| 按关键词搜索租房 | `searchRental` | `city`, `keyword`, `page` | 0.4 元 |
| 查看新房 | `getNewHouseList` | `city` | 0.4 元 |

`district` 和 `bizcircle` 必须使用安居客 URL 中的拼音编码；若用户只给中文名称且编码无法从已有结果确认，应先说明需要编码，不要盲猜并产生收费调用。`getRentalList` 不接受 `keyword` 或 `page`，如需按小区名、地段等关键词筛选租房，使用 `searchRental`。

## 调用客户端

先直接运行查询命令。客户端会自动使用已保存的凭证；如果提示没有凭证，在对话中用普通用户能理解的方式询问：“请把您的 AppID 和 SecureKey 发给我，我会保存下来供以后查询使用。如果还没有，请前往巴娜 Skill 技能中心 <https://wxpub.aibana.art> 注册并生成。”

收到凭证后，通过 `--app-id` 和 `--secure-key` 传给客户端。客户端默认保存凭证，之后无需再次询问。用户明确表示不希望保存时，增加 `--no-save-credentials`，仅用于本次调用。不要在后续答复中重复展示用户的 SecureKey。

免费调用：

```bash
python3 scripts/realestate_api.py getCities \
  --app-id '用户提供的AppID' --secure-key '用户提供的SecureKey'
python3 scripts/realestate_api.py getCommunityList --city gz --page 1
```

收费调用前先告知用户本次费用，然后直接执行：

```bash
python3 scripts/realestate_api.py searchErshoufang \
  --city gz --keyword '珠江新城' --page 1

python3 scripts/realestate_api.py searchRental \
  --city gz --keyword '凯粤湾' --page 1

python3 scripts/realestate_api.py searchCommunity \
  --city gz --keyword '天河花园' --page 1
```

脚本默认请求 `https://wxpub.aibana.art`，也可通过 `BANA_REALESTATE_BASE_URL` 覆盖服务地址。仅将该变量用于用户明确提供或可信的测试环境。

## 错误处理

- `400`：检查必填参数、JSON 和正整数页码。
- `401`：说明已保存的 AppID/SecureKey 无效，请用户在对话中重新提供；使用新值再次调用会覆盖旧凭证。如果尚未生成，提醒用户前往巴娜 Skill 技能中心 <https://wxpub.aibana.art> 注册并生成。
- `402`：明确说明余额不足，提醒用户前往巴娜 Skill 技能中心 <https://wxpub.aibana.art> 充值，然后停止调用，不要自动重试。
- `404`：核对方法名，不要用未知方法试探。
- `500`：说明服务端数据库或计费配置异常，停止重试收费请求。
- `502`：说明上游服务失败。再次尝试可能形成新调用；重试收费方法前再次告知用户费用，但无需等待确认。

参数错误、未知方法和上游失败会自动退回预扣费用，但仍应避免无意义重试。批量查询必须按顺序逐个调用，调用前明确告知用户总调用次数和最高费用，但无需等待确认。
