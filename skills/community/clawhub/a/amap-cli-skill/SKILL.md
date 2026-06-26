---
name: amap-cli-skill
display_name: Gaode Map CLI - 高德官方命令行工具 Skill
description: >-
  通过 CLI 命令行参数实时操控运行在容器中的高德地图 JSAPI 2.0 实例，
  支持地图状态控制、路径规划、POI 搜索等，所有操作均以结构化 JSON 输出，适合 AI Agent 驱动的地图可视化交互场景。
metadata:
  openclaw:
    primaryEnv: AMAP_KEY
    requiredBinaries:
      - node
      - npm
    requiredPackages:
      - name: "@amap-lbs/amap-gui"
        installCmd: "npm install -g @amap-lbs/amap-gui@latest"
---

# AMap GUI — 地图容器 CLI 命令行参数模式

通过命令行实时操控运行在 Electron 容器中的高德地图 JSAPI 2.0 实例。



## 前置条件

### 读取并导出 API Key（优先执行）

**在任何操作前，必须先确保 `AMAP_KEY` 已在当前 shell 环境中生效。**
OpenClaw 的 skill env 注入不一定对 agent 的 exec 环境生效，因此需要主动读取配置并 export。

执行以下命令，从 OpenClaw 配置中读取 Key 并导出到当前环境：

```bash
# 1. 检查环境变量是否已注入
echo "AMAP_KEY=${AMAP_KEY}"

# 2. 若为空，从 OpenClaw 配置文件读取
if [ -z "$AMAP_KEY" ]; then
  CONFIG_FILE="$HOME/.openclaw/openclaw.json"
  if [ -f "$CONFIG_FILE" ]; then
    AMAP_KEY=$(node -e "
      const c = require('$CONFIG_FILE');
      const env = c?.skills?.entries?.['amap-cli-skill']?.env || {};
      console.log(env.AMAP_KEY || '');
    " 2>/dev/null)
    AMAP_SECURITY_KEY=$(node -e "
      const c = require('$CONFIG_FILE');
      const env = c?.skills?.entries?.['amap-cli-skill']?.env || {};
      console.log(env.AMAP_SECURITY_KEY || '');
    " 2>/dev/null)
    export AMAP_KEY
    export AMAP_SECURITY_KEY
  fi
fi

# 仅输出是否成功，不泄露 Key 内容
if [ -n "$AMAP_KEY" ]; then
  echo "AMAP_KEY: configured"
else
  echo "AMAP_KEY: not set"
fi
```

**判断逻辑**：
- `AMAP_KEY` 读取成功且非空 → 继续后续步骤
- `AMAP_KEY` 仍为空 → 提示用户在 OpenClaw WebGUI 设置页面配置 `AMAP_KEY`（申请地址：https://lbs.amap.com），配置完成后重试
- `AMAP_SECURITY_KEY` 为空 → 不阻断流程，但新版 Key 可能需要它，建议一并配置
- 两个变量 export 后全局生效，所有后续 `amap-gui` 命令**无需再加 `AMAP_KEY=xxx` 前缀**

### 安装 amap-gui

首先确认 `amap-gui` CLI 是否已安装，若未安装则执行安装：

```bash
# 检查是否已安装（跨平台兼容）
amap-gui --version || npm install -g @amap-lbs/amap-gui@latest
```

> 如果 `amap-gui --version` 执行失败（命令不存在），必须先执行 `npm install -g @amap-lbs/amap-gui@latest` 安装后再继续。
> 
> **安全提示**：`@amap-lbs/amap-gui` 是高德地图官方发布的 npm 包（[npm 主页](https://www.npmjs.com/package/@amap-lbs/amap-gui)），安装前建议确认包名无误，避免 typosquatting 攻击。

### 必须先配置高德地图 API Key（两个）

`amap-gui` 需要高德地图开放平台的 Key 才能加载地图。**支持两种配置方式，任选其一。**

| 环境变量 | 是否必须 | 说明 |
|----------|----------|------|
| `AMAP_KEY` | 必须 | Web JS API Key |
| `AMAP_SECURITY_KEY` | 推荐设置 | JS API 安全密钥（部分账号类型必须） |

#### 方式一：通过 OpenClaw WebGUI 页面配置（推荐）

在 OpenClaw 的 WebGUI 设置页面中，直接填写以下环境变量：

- `AMAP_KEY` — 填入你的高德 Web JS API Key
- `AMAP_SECURITY_KEY` — 填入对应的安全密钥（可选但推荐）

配置后无需手动执行 `export`，OpenClaw 会自动将其注入到运行环境中。

#### 方式二：通过终端手动配置

```bash
# 检查是否已设置
# macOS / Linux:
echo $AMAP_KEY
echo $AMAP_SECURITY_KEY
# Windows (PowerShell):
# echo $env:AMAP_KEY
# echo $env:AMAP_SECURITY_KEY

# 若未设置，立即配置（申请地址：https://lbs.amap.com）
# macOS / Linux:
export AMAP_KEY=your_amap_web_js_key
export AMAP_SECURITY_KEY=your_amap_security_key
# Windows (PowerShell):
# $env:AMAP_KEY="your_amap_web_js_key"
# $env:AMAP_SECURITY_KEY="your_amap_security_key"
```

**判断逻辑**：
- `AMAP_KEY` 已设置（任意方式）→ 可继续后续步骤
- `AMAP_KEY` 未设置 → **必须先让用户配置**，否则 GUI 启动后地图无法加载，显示错误
- `AMAP_SECURITY_KEY` 未设置 → 默认为空字符串（老版 Key 可正常使用，新版 Key 需要设置）

> 若用户尚未申请 Key，引导其前往 [lbs.amap.com](https://lbs.amap.com) 创建「Web端(JS API)」类型的 Key，同时在控制台获取对应的安全密钥。

### 前置判断：容器未启动则先主动启动

**在执行任何地图操作之前**，必须先做前置判断：

1. **确认 AMAP_KEY 已设置**（见上方）

2. **检查状态**：
   ```bash
   amap-gui status
   ```

3. **判断逻辑**：
   - 若返回 `status: "not_running"` → 容器未运行
   - 若返回 `status: "running"` 且 `mapReady: true` → 可以执行命令

4. **若未运行，主动执行启动**（不要依赖自动启动，显式执行）：
   ```bash
   amap-gui start
   ```

5. **等待就绪**：`start` 命令会阻塞直到地图就绪（约 3-8 秒），返回 `mapReady: true` 后再继续后续命令。

**注意**：不采用自动/后台静默启动方式，由 Agent 在检测到未运行时显式执行 `amap-gui start`。

## 命令格式

```
amap-gui <command> [--option value ...]
```

**生命周期命令**（无需参数）：

```bash
amap-gui status          # 检查容器状态
amap-gui start           # 启动容器（阻塞至就绪）
amap-gui stop            # 停止容器
```

**status 返回示例**（容器运行中）：

```json
{
  "success": true,
  "data": {
    "status": "running",
    "port": 9800,
    "mapReady": true,
    "uptime": 125
  },
  "error": null
}
```

**status 返回示例**（容器未运行）：

```json
{
  "success": true,
  "data": {
    "status": "not_running"
  },
  "error": null
}
```

**start 返回示例**：

```json
{
  "success": true,
  "data": {
    "status": "running",
    "port": 9800,
    "mapReady": true
  },
  "error": null
}
```

**stop 返回示例**：

```json
{
  "success": true,
  "data": {
    "status": "stopped"
  },
  "error": null
}
```

**交互感知命令**（无需参数）：

```bash
amap-gui getLastEvent    # 获取用户最后一次地图交互事件
```

**地图操作命令**（通过命令行参数传参，返回 `CommandResult<T>` JSON）：

```bash
amap-gui mapState [--option value]     # 地图视图控制
amap-gui route [--option value]        # 路径规划
amap-gui searchPOI [--option value]    # POI 搜索
```

**结果输出原则**：从容器准确获取 JSON 状态/结果，解析后以文字告知用户，不需要截图。

| 命令 | 解析字段 | 告知用户 |
|------|----------|----------|
| `mapState` | center, zoom, style | 当前中心、缩放、样式 |
| `searchPOI` | pois | 名称、地址、距离、类型 |
| `route` | summary.distance, summary.time, summary.steps | 里程、耗时、路线步骤 |

## 核心命令

### 地图状态控制 — mapState

```bash
# 获取当前状态
amap-gui mapState --action get

# 设置视角
amap-gui mapState --action set --center 116.397,39.909 --zoom 15 --style dark
amap-gui mapState --action set --center 121.473,31.230 --zoom 13 --rotation 45 --pitch 60
```

**参数**：

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `--action` | `get` \| `set` | No | 操作类型，默认 `get` |
| `--center` | `lng,lat` | No | 中心点坐标（经度,纬度） |
| `--zoom` | `3-20` | No | 缩放级别 |
| `--rotation` | `0-360` | No | 旋转角度 |
| `--pitch` | `0-83` | No | 俯仰角度 |
| `--style` | `string` | No | 地图样式 |

**可用样式**：`normal` `dark` `light` `whitesmoke` `fresh` `grey` `graffiti` `macaron` `blue` `darkblue` `wine`

> **注意**：命令行模式下 `--center` 仅接受 `lng,lat` 坐标格式，不支持地名。如需使用地名，请使用 `--json` 模式。

**mapState get 返回示例**：

```json
{
  "success": true,
  "data": {
    "center": [116.397428, 39.90923],
    "zoom": 15,
    "rotation": 0,
    "pitch": 0,
    "style": "normal",
    "bounds": {
      "southWest": [116.384258, 39.902195],
      "northEast": [116.410598, 39.916265]
    }
  },
  "error": null
}
```

| 返回字段 | 类型 | 说明 |
|----------|------|------|
| `data.center` | `[lng, lat]` | 当前地图中心点坐标 |
| `data.zoom` | `number` | 当前缩放级别 |
| `data.rotation` | `number` | 当前旋转角度 |
| `data.pitch` | `number` | 当前俯仰角度 |
| `data.style` | `string` | 当前地图样式名称 |
| `data.bounds` | `object` | 当前可视区域边界（西南角、东北角坐标） |

**mapState set 返回示例**：

```json
{
  "success": true,
  "data": {
    "center": [121.473701, 31.230416],
    "zoom": 13,
    "rotation": 45,
    "pitch": 60,
    "style": "dark",
    "bounds": {
      "southWest": [121.420135, 31.192847],
      "northEast": [121.527267, 31.267985]
    }
  },
  "error": null
}
```

> 设置成功后返回的是**设置后的实际地图状态**，可用于确认视角是否已正确应用。

### 路径规划 — route

```bash
# 驾车
amap-gui route --from 北京南站 --to 天安门 --type driving

# 驾车（带途经点）
amap-gui route --from 北京南站 --to 首都机场T3 --type driving --waypoints 天安门,王府井 --policy fastest

# 步行
amap-gui route --from 故宫博物院 --to 景山公园 --type walking

# 骑行
amap-gui route --from 北京大学 --to 清华大学 --type riding

# 公交（city 必填）
amap-gui route --from 北京站 --to 中关村 --type transit --city 北京

# 使用坐标
amap-gui route --from 116.378,39.865 --to 116.397,39.909 --type driving

# 自定义显示名称
amap-gui route --from 116.378,39.865 --from-name 北京南站 --to 116.397,39.909 --to-name 天安门 --type driving
```

**参数**：

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `--from` | `地名` 或 `lng,lat` | Yes | 起点（地名或坐标） |
| `--from-name` | `string` | No | 起点显示名称（配合坐标使用） |
| `--to` | `地名` 或 `lng,lat` | Yes | 终点（地名或坐标） |
| `--to-name` | `string` | No | 终点显示名称（配合坐标使用） |
| `--type` | `string` | Yes | 出行方式：`driving` `walking` `riding` `transit` |
| `--waypoints` | `p1,p2,...` | No | 逗号分隔的途经点（仅 driving，最多 16 个） |
| `--policy` | `string` | No | 驾车策略：`fastest` `least_fee` `shortest` `no_highway` `avoid_jam` |
| `--strategy` | `string` | No | 公交策略：`fastest` `least_cost` `least_walk` `most_comfort` `no_subway` |
| `--city` | `string` | transit 必填 | 城市名（公交模式必须指定） |

**地图效果**：规划完成后自动绘制路线（带描边+方向箭头），标记起点（绿色）、途经点（蓝色）、终点（红色）。

**驾车路线返回示例**：

```bash
amap-gui route --from 北京南站 --to 天安门 --type driving
```

```json
{
  "success": true,
  "data": {
    "type": "driving",
    "from": {
      "name": "北京南站",
      "position": [116.378888, 39.865026]
    },
    "to": {
      "name": "天安门",
      "position": [116.397477, 39.908692]
    },
    "summary": {
      "distance": 8500,
      "time": 1260,
      "tolls": 0,
      "steps": [
        { "instruction": "从北京南站出发，沿开阳路向北行驶500米", "distance": 500, "time": 60 },
        { "instruction": "右转进入马连道南街，行驶1.2公里", "distance": 1200, "time": 180 },
        { "instruction": "左转进入广安门内大街，行驶2.8公里", "distance": 2800, "time": 420 },
        { "instruction": "沿前门西大街行驶1.5公里", "distance": 1500, "time": 240 },
        { "instruction": "到达天安门", "distance": 0, "time": 0 }
      ]
    }
  },
  "error": null
}
```

| 返回字段 | 类型 | 说明 |
|----------|------|------|
| `data.type` | `string` | 出行方式 |
| `data.from` | `object` | 起点信息（名称 + 解析后的坐标） |
| `data.to` | `object` | 终点信息（名称 + 解析后的坐标） |
| `data.summary.distance` | `number` | 总距离（米） |
| `data.summary.time` | `number` | 预计耗时（秒） |
| `data.summary.tolls` | `number` | 过路费（元，仅驾车） |
| `data.summary.steps[]` | `array` | 路线步骤列表 |
| `steps[].instruction` | `string` | 该步骤的文字导航指引 |
| `steps[].distance` | `number` | 该步骤距离（米） |
| `steps[].time` | `number` | 该步骤耗时（秒） |

**步行路线返回示例**：

```bash
amap-gui route --from 故宫博物院 --to 景山公园 --type walking
```

```json
{
  "success": true,
  "data": {
    "type": "walking",
    "from": {
      "name": "故宫博物院",
      "position": [116.397029, 39.917839]
    },
    "to": {
      "name": "景山公园",
      "position": [116.396794, 39.924908]
    },
    "summary": {
      "distance": 850,
      "time": 720,
      "steps": [
        { "instruction": "从故宫博物院北门出发，向北步行200米", "distance": 200, "time": 170 },
        { "instruction": "沿景山前街向北步行400米", "distance": 400, "time": 340 },
        { "instruction": "到达景山公园南门", "distance": 250, "time": 210 }
      ]
    }
  },
  "error": null
}
```

**公交路线返回示例**：

```bash
amap-gui route --from 北京站 --to 中关村 --type transit --city 北京
```

```json
{
  "success": true,
  "data": {
    "type": "transit",
    "from": {
      "name": "北京站",
      "position": [116.427113, 39.903147]
    },
    "to": {
      "name": "中关村",
      "position": [116.310905, 39.981901]
    },
    "summary": {
      "distance": 18200,
      "time": 3360,
      "steps": [
        { "instruction": "步行380米到达北京站地铁站", "distance": 380, "time": 320 },
        { "instruction": "乘坐地铁2号线（外环），经过4站到达西直门站", "distance": 7200, "time": 960 },
        { "instruction": "站内换乘地铁4号线大兴线（安河桥北方向），经过3站到达海淀黄庄站", "distance": 5800, "time": 720 },
        { "instruction": "步行650米到达中关村", "distance": 650, "time": 540 }
      ]
    }
  },
  "error": null
}
```

### POI 搜索 — searchPOI

```bash
# 关键词搜索
amap-gui searchPOI --keyword 星巴克 --city 北京

# 周边搜索（坐标 + 半径）
amap-gui searchPOI --keyword 咖啡 --center 120.15,30.28 --radius 1000

# 分页
amap-gui searchPOI --keyword 酒店 --city 上海 --pageSize 5 --pageIndex 2
```

**参数**：

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `--keyword` | `string` | Yes | 搜索关键词 |
| `--city` | `string` | No | 搜索城市 |
| `--center` | `lng,lat` | No | 周边搜索中心坐标（不传则为关键词搜索） |
| `--radius` | `number` | No | 周边搜索半径（米），默认 3000 |
| `--pageSize` | `number` | No | 每页数量，默认 10 |
| `--pageIndex` | `number` | No | 页码，默认 1 |

> **注意**：命令行模式下 `--center` 仅接受 `lng,lat` 坐标格式，不支持地名。如需使用地名作为搜索中心，请使用 `--json` 模式。

**地图效果**：搜索结果自动标记在地图上（分类图标），点击可查看详情弹窗。

**关键词搜索返回示例**：

```bash
amap-gui searchPOI --keyword 星巴克 --city 北京
```

```json
{
  "success": true,
  "data": {
    "keyword": "星巴克",
    "city": "北京",
    "total": 238,
    "pageSize": 10,
    "pageIndex": 1,
    "pois": [
      {
        "name": "星巴克(王府井大街店)",
        "address": "王府井大街138号新东安广场1层",
        "location": [116.410156, 39.913889],
        "tel": "010-65281368",
        "type": "餐饮服务;咖啡厅;星巴克",
        "id": "B000A83M61"
      },
      {
        "name": "星巴克(国贸商城店)",
        "address": "建国门外大街1号国贸商城B1层",
        "location": [116.460579, 39.908775],
        "tel": "010-65052638",
        "type": "餐饮服务;咖啡厅;星巴克",
        "id": "B000A8WSBP"
      },
      {
        "name": "星巴克(三里屯太古里店)",
        "address": "三里屯路19号三里屯太古里南区1层S1-12b",
        "location": [116.454872, 39.933743],
        "tel": "010-64176658",
        "type": "餐饮服务;咖啡厅;星巴克",
        "id": "B000A7BKQG"
      }
    ]
  },
  "error": null
}
```

**周边搜索返回示例**：

```bash
amap-gui searchPOI --keyword 咖啡 --center 120.15,30.28 --radius 1000
```

```json
{
  "success": true,
  "data": {
    "keyword": "咖啡",
    "center": [120.15, 30.28],
    "radius": 1000,
    "total": 15,
    "pageSize": 10,
    "pageIndex": 1,
    "pois": [
      {
        "name": "Manner Coffee(西湖银泰店)",
        "address": "延安路98号西湖银泰城B1层",
        "location": [120.152836, 30.279412],
        "tel": "0571-87651234",
        "type": "餐饮服务;咖啡厅;咖啡厅",
        "distance": 180,
        "id": "B0FFHW1N50"
      },
      {
        "name": "星巴克(湖滨银泰店)",
        "address": "东坡路7号湖滨银泰in77 B区1层",
        "location": [120.153921, 30.281035],
        "tel": "0571-87068890",
        "type": "餐饮服务;咖啡厅;星巴克",
        "distance": 450,
        "id": "B0FFH8XKQP"
      }
    ]
  },
  "error": null
}
```

| 返回字段 | 类型 | 说明 |
|----------|------|------|
| `data.keyword` | `string` | 搜索关键词 |
| `data.city` | `string` | 搜索城市（关键词搜索时） |
| `data.center` | `[lng, lat]` | 搜索中心坐标（周边搜索时） |
| `data.radius` | `number` | 搜索半径（周边搜索时） |
| `data.total` | `number` | 匹配结果总数 |
| `data.pageSize` | `number` | 每页数量 |
| `data.pageIndex` | `number` | 当前页码 |
| `data.pois[]` | `array` | POI 结果列表 |
| `pois[].name` | `string` | POI 名称 |
| `pois[].address` | `string` | POI 地址 |
| `pois[].location` | `[lng, lat]` | POI 坐标 |
| `pois[].tel` | `string` | 联系电话 |
| `pois[].type` | `string` | POI 类型分类 |
| `pois[].distance` | `number` | 距搜索中心的距离（米，仅周边搜索） |
| `pois[].id` | `string` | POI 唯一标识 |

### getLastEvent — 获取用户最后一次地图交互事件

```bash
amap-gui getLastEvent
```

无需参数，直接调用。返回用户在 GUI 上最后一次交互的事件信息。

**事件类型**：

| `type` | 触发方式 | 返回字段 |
|--------|----------|----------|
| `map_click` | 点击地图空白处 | `position` |
| `poi_click` | 点击地图上的 POI 标记 | `title` + `address` + `position` |
| `poi_select` | 在左侧搜索结果列表中选中 | `title` + `address` + `position` |

**返回字段说明**：

| 字段 | 说明 |
|------|------|
| `lastEvent.hasEvent` | 是否有事件记录（`false` 表示用户尚未操作）|
| `lastEvent.type` | 事件类型（见上表）|
| `lastEvent.title` | POI 名称（`poi_click` / `poi_select` 时有值）|
| `lastEvent.address` | POI 地址（`poi_click` / `poi_select` 时有值）|
| `lastEvent.position` | 坐标 `[lng, lat]`，所有事件类型均有值 |

**返回示例**：

```json
{
  "success": true,
  "data": {
    "lastEvent": {
      "hasEvent": true,
      "type": "poi_select",
      "title": "故宫博物院",
      "address": "景山前街4号",
      "position": [116.397029, 39.917839]
    }
  },
  "error": null
}
```

**典型用法**：用户在地图上点选某地点后，AI 通过 `getLastEvent` 获取位置，再衔接路线规划等操作，无需用户重复说出地名。

```bash
# 用户在 POI 面板点选了一家餐厅
amap-gui getLastEvent
# → type: poi_select, title: "某餐厅", position: [116.488778, 40.002995]

# AI 用获取到的坐标直接规划路线
amap-gui route --from 北京站 --to 116.488778,40.002995 --to-name 某餐厅 --type driving
```

## 命令行参数 vs JSON 模式对比

| 特性 | 命令行参数模式 | JSON 模式 |
|------|---------------|-----------|
| **地名作为坐标** | `--from`/`--to` 支持地名 | `position`/`center` 支持地名 |
| **地名作为搜索中心** | ❌ `--center` 仅支持坐标 | ✅ `center` 支持地名 |
| **地名作为地图中心** | ❌ `--center` 仅支持坐标 | ✅ `center` 支持地名 |
| **途经点** | `--waypoints p1,p2` 逗号分隔 | `waypoints` 数组 |
| **优先级** | 低 | 高（`--json` 会覆盖其他参数） |
| **适用场景** | 简单命令、快速操作 | 复杂参数、精确控制 |

## 关键规则

1. **前置判断** — 操作前先 `amap-gui status`；若未运行则显式执行 `amap-gui start`，确认 `mapReady: true` 后再继续
2. **route 的 `--from`/`--to` 支持地名** — 直接传地名字符串，容器内部自动 geocode
3. **mapState 和 searchPOI 的 `--center` 仅支持坐标** — 格式为 `lng,lat`，如 `116.397,39.909`
4. **坐标格式** — `经度,纬度`（lng,lat），如 `116.397428,39.90923`
5. **transit 必须传 `--city`** — 公交模式必须指定城市
6. **`--waypoints` 仅 driving** — 途经点只有驾车模式支持，多个途经点用逗号分隔
7. **不需要 clear 命令** — 新命令自动清除上一次的路线/标记
8. **`--json` 优先** — 当 `--json` 与其他参数同时使用时，`--json` 的值优先
9. **命令名大小写不敏感** — `searchpoi`、`searchPOI`、`SearchPOI` 均等效，`mapstate` 等同 `mapState`，`getlastevent` 等同 `getLastEvent`
10. **停止容器** — 完成后用 `amap-gui stop` 停止

## 典型工作流

**场景 1：用户想看某地的地图**

```bash
amap-gui status
# → not_running → 先启动
amap-gui start
# → mapReady: true

amap-gui mapState --action set --center 121.491,31.233 --zoom 15 --pitch 45 --style dark
```

**场景 2：用户想从 A 到 B 怎么走**

```bash
amap-gui route --from 北京南站 --to 首都机场T3 --type driving
```

**场景 3：用户想找附近的 XX**

```bash
amap-gui searchPOI --keyword 咖啡 --center 120.155,30.274 --radius 1000
```

**场景 4：连续操作 — 搜索后导航**

```bash
amap-gui searchPOI --keyword 故宫博物院 --city 北京
# 从结果中取坐标
amap-gui route --from 王府井 --to 116.397029,39.917839 --to-name 故宫博物院 --type walking
```

**场景 5：用户点选地图后导航**

```bash
# 用户在地图上点选了目的地
amap-gui getLastEvent
# → position: [116.488778, 40.002995], title: "某餐厅"

# 直接用坐标规划路线
amap-gui route --from 北京站 --to 116.488778,40.002995 --to-name 某餐厅 --type driving
```

**场景 6：完成后停止**

```bash
amap-gui stop
```
