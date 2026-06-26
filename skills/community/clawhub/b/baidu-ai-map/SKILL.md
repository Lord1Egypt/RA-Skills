---
name: baidu-ai-map
description: 百度地图 Agent Plan ，无需成为百度地图开发者，立即接入百度地图为 Agent 场景原生设计的地图能力，例如 AI 地点检索、AI 路线规划、地理编码与逆地理编码、天气查询、地图展示等开箱即用的工具。
license: MIT
version: 1.0.0
homepage: https://lbs.baidu.com
repository: https://github.com/baidu-maps/map-skills
metadata:
  openclaw:
    requires:
      bins: ["curl"]
      env: BAIDU_MAP_AUTH_TOKEN
    primaryEnv: BAIDU_MAP_AUTH_TOKEN
---

# 百度地图服务 Agent Plan

提供大模型友好调用的地图工具skills/baidu-ai-map/SKILL.md，支持语义化 AI 搜索、语义化 AI 路线规划、地理编码与逆地理编码、天气查询。

## 使用准则

### 准则 1：API 端点

所有能力统一使用：

> **Base URL**: `https://api.map.baidu.com/`

### 准则 2：SK 凭证安全处理

SK（Service Key）是调用所有 API 的必须凭证：

1. 优先读取环境变量 `BAIDU_MAP_AUTH_TOKEN`。
2. 如果为空，提示用户前往 [百度地图 Agent Plan](https://lbs.baidu.com/apiconsole/agentplan) 申请。
3. 设置环境变量：

```bash
export BAIDU_MAP_AUTH_TOKEN="你的SK"
```

### 准则 3：统一鉴权方式（Header 传入）

调用所有 API 时，统一通过 Header 传入：

- `Authorization: Bearer $BAIDU_MAP_AUTH_TOKEN`

示例：

```bash
curl --get "https://api.map.baidu.com/agent_plan/v1/place" \
  -H "Authorization: Bearer $BAIDU_MAP_AUTH_TOKEN" \
  --data-urlencode "user_raw_request=帮我找北京可带宠物的咖啡馆" \
  --data-urlencode "region=北京市"
```

## 全局参数与行为约束

1. `user_raw_request` 必须是完整的用户需求，不可压缩为关键词。
2. `user_raw_request` 出现“我附近”等非明确地点时，可根据上下文为用户推理为具体地点名称，但不可对坐标进行推理。
3. `user_raw_request` 需保留定语/约束词，例如“评分最高”“最近”“最便宜”“3公里内”。
4. 不得编造坐标；`center` / `location` / `refer_pois` 仅可来自用户明确提供或可信来源，当无可靠坐标时，必须先向用户澄清或先调用 `geocoding` / `place` 等工具获取。
5. 统一使用 Header 鉴权：`Authorization: Bearer $BAIDU_MAP_AUTH_TOKEN`。
6. 经纬度至少保留小数点后 6 位。
7. 所有工具返回坐标类型统一为 `gcj02`。
8. 相同参数请求避免重复发起，否则会造成百度地图 Agent Plan 巨额的token消耗。

## 工具详解

### 1. Place（语义化AI地点检索）

#### API

`GET /agent_plan/v1/place`

#### 参数输入（给模型）

Required:
- `user_raw_request`: 用户原始需求，原样完整传入，不可压缩为关键词；保留约束词（如“评分最高”“最近”“3公里内”）
- `region`: 城市或区域限制

Optional:
- `center`: 检索中心点和排序参考点（`lat,lng`，gcj02）
- `sort`: `distance` 或 `relevance`（默认 `relevance`）

Rules:
- `sort=distance` 时，`center` 必传
- `center` 只能来自用户明确提供或可信来源，禁止推测/编造，可通过 `geocoding` / `place` 等工具获取
- 经纬度至少保留小数点后 6 位

#### 鉴权

- GET：Header `Authorization: Bearer $BAIDU_MAP_AUTH_TOKEN`

#### 示例

```bash
# 1) 帮我查一下八达岭长城附近的五星级酒店
curl --get "https://api.map.baidu.com/agent_plan/v1/place" \
  -H "Authorization: Bearer $BAIDU_MAP_AUTH_TOKEN" \
  --data-urlencode "user_raw_request=帮我查一下八达岭长城附近的五星级酒店" \
  --data-urlencode "region=延庆区" \
  --data-urlencode "sort=relevance"

# 2) 离我最近的火锅店（distance 排序）
curl --get "https://api.map.baidu.com/agent_plan/v1/place" \
  -H "Authorization: Bearer $BAIDU_MAP_AUTH_TOKEN" \
  --data-urlencode "user_raw_request=离我最近的火锅店" \
  --data-urlencode "region=北京市" \
  --data-urlencode "center=40.056800,116.308300" \
  --data-urlencode "sort=distance"
```

### 2. Direction（语义化AI路线规划）

#### API

`GET /agent_plan/v1/direction`

#### 参数输入

Required:
- `user_raw_request`: 用户原始需求，包含起点、终点、途经点，支持沿途搜索POI；保留路线约束词，需要推理并改写用户原始的交通方式
- `location`: 用户当前位置坐标（`lat,lng`，gcj02）

Optional:
- `refer_pois`: 地点精确映射，格式 `地点名称:uid,纬度,经度;地点名称:uid,纬度,经度`

Rules:
- 当前仅支持驾车、步行、骑行、公交路线规划。`user_raw_request` 中出现其他交通方式时，需要改写到这四种交通方式
- 该工具根据用户需求返回两类结果：
  - **路线规划结果**：`answer_type="gptmodel_navigate"`，返回完整路线方案
  - **地点澄清列表**：需要用户确认具体地点，包含两种场景：
    - `answer_type="gptmodel_poi_clarify"`：起终点POI澄清（如同名地标、模糊地址）
    - `answer_type="gptmodel_onway_search_clarify"`：沿途搜索POI澄清（如"路上买杯咖啡"无法确定具体店铺）
- **澄清列表消歧流程**（当返回澄清类型 `answer_type` 时）：
  1. 展示候选：向用户展示澄清列表中的POI选项
  2. 引导选择：请用户从候选列表中选择目标POI
  3. 重新规划：携带用户选择的POI信息重新发起路线规划请求，**必须同时满足以下两个条件**：
     - 改写 `user_raw_request`：在请求中明确指定选中的POI名称
       - 示例：`"路上买杯咖啡"` → `"先去星巴克（知春路店）买杯咖啡"`
     - 传入 `refer_pois`：提供选中POI的精确坐标映射
       - 格式：`地点名称:uid,纬度,经度`
  4. 获取路线：正确执行上述步骤后，接口将返回 `answer_type="gptmodel_navigate"` 的路线规划结果
- `location` 当起点有歧义（如同名地标、模糊起点）时，路线规划服务会基于当前位置推理最合理的起点位置
- `refer_pois` 默认不传，用于消歧场景提供精确POI坐标，仅在需要澄清歧义地点时传入
- `refer_pois` / `location` 的经纬度至少保留小数点后 6 位，禁止推测/编造，可通过 `geocoding` / `place` 等工具获取

#### 鉴权

- GET：Header `Authorization: Bearer $BAIDU_MAP_AUTH_TOKEN`

#### 示例

```bash
# 1) 帮我规划从故宫到颐和园的驾车路线
curl --get "https://api.map.baidu.com/agent_plan/v1/direction" \
  -H "Authorization: Bearer $BAIDU_MAP_AUTH_TOKEN" \
  --data-urlencode "user_raw_request=帮我规划从故宫到颐和园的驾车路线" \
  --data-urlencode "location=39.914590,116.403770"

# 2) “我家”别名映射
curl --get "https://api.map.baidu.com/agent_plan/v1/direction" \
  -H "Authorization: Bearer $BAIDU_MAP_AUTH_TOKEN" \
  --data-urlencode "user_raw_request=步行去我家附近最近的中餐厅" \
  --data-urlencode "location=40.056800,116.308300" \
  --data-urlencode "refer_pois=我家:fbc88a21464370106e3e1b52,40.092180,116.345310"

# 3) 交通方式推理改写：从王府井打车去三里屯要多久
curl --get "https://api.map.baidu.com/agent_plan/v1/direction" \
  -H "Authorization: Bearer $BAIDU_MAP_AUTH_TOKEN" \
  --data-urlencode "user_raw_request=从王府井驾车去三里屯要多久" \
  --data-urlencode "location=39.914590,116.403770"

# 4) 沿途搜索：顺路去买杯咖啡
curl --get "https://api.map.baidu.com/agent_plan/v1/direction" \
  -H "Authorization: Bearer $BAIDU_MAP_AUTH_TOKEN" \
  --data-urlencode "user_raw_request=从百度大厦驾车到颐和园，路上顺便买一杯咖啡" \
  --data-urlencode "location=39.914590,116.403770"
```

### 3. Geocoding（地理编码）

#### API

`GET /agent_plan/v1/geocoding`

#### 参数输入

Required:
- `address`: 要解析的完整地址

Optional:
- `region`: 城市/区域提示（减少歧义）

Rules:
- 地址越完整，解析越稳定

#### 鉴权

- GET：Header `Authorization: Bearer $BAIDU_MAP_AUTH_TOKEN`

#### 示例

```bash
curl --get "https://api.map.baidu.com/agent_plan/v1/geocoding" \
  -H "Authorization: Bearer $BAIDU_MAP_AUTH_TOKEN" \
  --data-urlencode "address=北京市海淀区上地十街10号百度大厦" \
  --data-urlencode "region=北京市"
```

### 4. Reverse Geocoding（逆地理编码）

#### API

`GET /agent_plan/v1/reverse_geocoding`

#### 参数输入

Required:
- `location`: `lat,lng` 格式坐标（gcj02）

Rules:
- 经纬度至少保留小数点后 6 位

#### 鉴权

- GET：Header `Authorization: Bearer $BAIDU_MAP_AUTH_TOKEN`

#### 示例

```bash
curl --get "https://api.map.baidu.com/agent_plan/v1/reverse_geocoding" \
  -H "Authorization: Bearer $BAIDU_MAP_AUTH_TOKEN" \
  --data-urlencode "location=40.056800,116.308300"
```

### 5. Weather（天气查询）

#### API

`GET /agent_plan/v1/weather`

#### 参数输入

Optional:
- `region`: 行政区划名称
- `location`: `lat,lng` 格式坐标（gcj02）

Rules:
- `region` 与 `location` 至少传一个
- `location` 传入时，经纬度至少保留小数点后 6 位

#### 鉴权

- GET：Header `Authorization: Bearer $BAIDU_MAP_AUTH_TOKEN`

#### 示例

```bash
# 1) 按坐标查询天气
curl --get "https://api.map.baidu.com/agent_plan/v1/weather" \
  -H "Authorization: Bearer $BAIDU_MAP_AUTH_TOKEN" \
  --data-urlencode "location=38.766230,116.432130"
```

### 6. MapRender（地图展示）

#### 功能说明

在用户明确表达"在地图上查看"等可视化意图时，生成并打开地图展示链接，用于可视化展示 `place` 或 `direction` 接口的查询结果。

#### 使用条件

**触发条件**：用户明确表达以下任意图时使用
- "在地图上显示/标出"
- "打开地图查看"
- "地图里看看"
- "在地图上看"
- "可视化展示"

**不触发场景**：
- 单纯信息查询，如"附近有什么"、"怎么走"、"多久到"
- `direction` 接口返回非路线结果时（ `answer_type="gptmodel_navigate"` 以外的结果 ）不触发
- 用户表达模糊或不明确

#### 参数输入

Required:
- `resource_key`: 地图资源唯一标识，取自上一步 `place` / `direction` 接口响应中的 `resource_key` 字段

Optional:
- `open_browser`: 是否自动打开浏览器，默认 `true`

#### 规则

1. 必须先调用 `place` 或 `direction` 接口获取 `resource_key`，才能使用本工具
2. 地图展示链接格式：`https://lbs.baidu.com/mapstatic/agentui_resource.html?resource_key=<resource_key>`
3. 默认自动打开浏览器：macOS 使用 `open`，Linux 使用 `xdg-open`，Windows 使用 `start`

#### 示例

```bash
# 用户：帮我找北京可带宠物的咖啡馆，在地图上标出来

# 步骤1: 调用 place 获取 POI 列表和 resource_key
curl --get "https://api.map.baidu.com/agent_plan/v1/place" \
  -H "Authorization: Bearer $BAIDU_MAP_AUTH_TOKEN" \
  --data-urlencode "user_raw_request=帮我找北京可带宠物的咖啡馆" \
  --data-urlencode "region=北京市"

# 响应中包含 resource_key，例如: "abc123def456"

# 步骤2: 使用 resource_key 生成并打开地图展示链接
# macOS:
open "https://lbs.baidu.com/mapstatic/agentui_resource.html?resource_key=abc123def456"
# Linux:
xdg-open "https://lbs.baidu.com/mapstatic/agentui_resource.html?resource_key=abc123def456"
# Windows:
start "" "https://lbs.baidu.com/mapstatic/agentui_resource.html?resource_key=abc123def456"
```

## 错误处理

1. 如果缺少 token，提示用户执行：  
   申请地址：https://lbs.baidu.com/apiconsole/agentplan  
   `export BAIDU_MAP_AUTH_TOKEN="<YOUR_BAIDU_MAP_AUTH_TOKEN>"`
2. 如果提示参数错误，重新阅读本Skills查阅如何传参