---
AIGC:
    ContentProducer: Minimax Agent AI
    ContentPropagator: Minimax Agent AI
    Label: AIGC
    ProduceID: 6a67c14c2852222b0b7a34e74bd8bcbd
    PropagateID: 6a67c14c2852222b0b7a34e74bd8bcbd
    ReservedCode1: 3044022013c2f6dc72f2acadc50b2625eaafa287dde34ae48617a50386545dad5b8116170220643a821218ef525727b7f8c4022ce662a3b2ee41640740b63e83b8464e58e28c
    ReservedCode2: 304602210090433f12363718a8833b9c9d782c9328554694f84915060c71ec84c68f811294022100ba8cdda85c6eed92e12381129f3bb1acbedb8e21d22463e69407a81aa26f20f8
description: 高德地图全功能工具 - 集成POI搜索、路径规划、天气查询、公交查询、实时路况等。/Gaode Map All-in-One - POI search, route planning, weather, bus, traffic.
icon: "\U0001F5FA️"
name: amap-search
version: 2.0.0
---

# 🗺️ 高德地图全功能工具 (amap-search)

调用高德地图 Web 服务 API，提供完整的位置服务功能。

## ✨ 功能一览

| 命令 | 功能 | 说明 |
|------|------|------|
| `ip` | IP定位 | 自动获取用户当前位置（精确到城市） |
| `geo` | 地理编码 | 地址 → 经纬度坐标 |
| `regeo` | 逆地理编码 | 经纬度坐标 → 地址 |
| `poi` | POI搜索 | 关键字搜索、周边搜索、城市搜索 |
| `route` | 路径规划 | 驾车、步行、公交路线规划 |
| `weather` | 天气查询 | 当前天气 + 未来预报 |
| `traffic` | 实时路况 | 城市/道路拥堵情况 |
| `tips` | 输入提示 | 智能自动补全建议 |

## 📋 快速开始 / Quick Start

### 第一步：申请高德 API Key

1. 访问 **高德开放平台**：https://lbs.amap.com/
2. 点击「注册/登录」→ 使用账号登录
3. 进入「控制台」→ 「应用管理」→ 「创建应用」
4. 应用名称：`高德地图工具`（任意名称）
5. 点击「添加 Key」→ 填写 Key 名称
6. **服务平台**：勾选 **「Web服务」**
7. 点击「提交」，获取 Key

> 💡 **免费额度**：每个 Key 每天 2000 次调用，个人使用足够

### 第二步：配置 API Key（推荐使用环境变量）

**方式一：设置环境变量（推荐）**
```bash
# 在终端中设置环境变量
export AMAP_API_KEY="你的API_KEY"

# 或在 ~/.bashrc 中永久添加
echo 'export AMAP_API_KEY="你的API_KEY"' >> ~/.bashrc
source ~/.bashrc
```

**方式二：命令行参数**
```bash
python3 gaode_map.py <命令> --key 你的API_KEY [参数]
```

> ⚠️ **优先级**：环境变量 > 命令行参数。建议使用环境变量，避免每次输入。

---

## 📖 详细使用说明

### 1️⃣ IP定位 (ip)

获取用户当前所在城市。

```bash
python3 gaode_map.py ip --key 你的KEY
```

**输出示例**：
```
Your location: 四川省 成都市
City code: 510100
```

---

### 2️⃣ 地理编码 (geo)

将地址转换为经纬度坐标。

```bash
# 基本用法
python3 gaode_map.py geo --key 你的KEY --address "成都市天府广场"

# 指定城市（更精确）
python3 gaode_map.py geo --key 你的KEY --address "春熙路" --city 成都
```

**输出示例**：
```
Address: 四川省成都市锦江区春熙路
Location: 104.085329,30.658137
```

---

### 3️⃣ 逆地理编码 (regeo)

将经纬度坐标转换为地址。

```bash
python3 gaode_map.py regeo --key 你的KEY --location "104.085329,30.658137"
```

---

### 4️⃣ POI 搜索 (poi)

搜索附近的商家、服务设施。

#### 按城市关键字搜索
```bash
python3 gaode_map.py poi --key 你的KEY --city 成都 --keyword "火锅"
```

#### 周边搜索（指定位置附近）
```bash
python3 gaode_map.py poi --key 你的KEY --location "104.085,30.658" --radius 3000 --keyword "餐厅"
```

**输出示例**：
```
Found 21 results:

1. 蜀九香火锅(春熙路店)
   Address: 锦江区春熙路南段8号
   Location: 104.085123,30.657891
   Phone: 028-86612345
```

#### 周边搜索（带距离）
```bash
# 搜索附近POI并显示每个结果到起点的实际驾驶距离
python3 gaode_map.py poi --location "104.069,30.229" --radius 2000 --keyword "酒店" --with-distance
```

**输出示例**：
```
Found 10 results:

1. 乐游酒店 | 地址：视高街道xxx | 距离：313米
2. 橙苇公寓 | 地址：xxx | 距离：853米
...
```

---

### 5️⃣ 路径规划 (route)

规划出行路线。

#### 驾车路线
```bash
python3 gaode_map.py route --key 你的KEY \
  --origin "104.065,30.657" \
  --destination "104.085,30.675" \
  --mode driving
```

#### 步行路线
```bash
python3 gaode_map.py route --key 你的KEY \
  --origin "104.065,30.657" \
  --destination "104.085,30.675" \
  --mode walking
```

#### 公交/地铁路线
```bash
python3 gaode_map.py route --key 你的KEY \
  --origin "104.065,30.657" \
  --destination "104.085,30.675" \
  --mode transit \
  --city 成都
```

**输出示例**：
```
Distance: 3418 meters
Duration: 828 seconds (约14分钟)
Steps (12):
  1. 向南行驶23米右转
  2. 向西行驶46米左转
  ...
```

---

### 6️⃣ 天气查询 (weather)

查询天气信息。

#### 当前天气
```bash
python3 gaode_map.py weather --key 你的KEY --city 成都
```

#### 天气预报（包含未来几天）
```bash
python3 gaode_map.py weather --key 你的KEY --city 成都 --forecast
```

**输出示例**：
```
City: 成都市
Weather: 阴
Temperature: 15°C
Wind: 北风 ≤3级
Humidity: 79%

Forecast:
  2026-03-12: 阴/多云, 12°C ~ 18°C
  2026-03-13: 小雨/阴, 10°C ~ 15°C
```

---

### 7️⃣ 实时路况 (traffic)

查询道路交通状况。

#### 城市整体路况
```bash
python3 gaode_map.py traffic --key 你的KEY --city 成都
```

#### 特定道路路况
```bash
python3 gaode_map.py traffic --key 你的KEY --city 成都 --road "天府大道"
```

---

### 8️⃣ 输入提示 (tips)

智能自动补全，输入关键词时给出建议。

```bash
python3 gaode_map.py tips --key 你的KEY --keyword "春熙" --city 成都
```

---

## 📊 JSON 输出

所有命令都支持 `--json` 参数，输出 JSON 格式，方便程序处理：

```bash
python3 gaode_map.py weather --key 你的KEY --city 成都 --json
```

---

## ⚠️ 注意事项

1. **API Key 必需**：每个用户需要自己申请高德 API Key
2. **调用限制**：免费版每天 2000 次，大部分场景足够
3. **坐标格式**：经度在前，纬度在后（如 `104.065,30.657`，不是 `30.657,104.065`）
4. **城市参数**：部分 API 需要城市名称或城市代码

---

## 🔧 常见问题

**Q: 为什么提示 "SERVICE_NOT_AVAILABLE"？**
A: 部分 API（如输入提示）可能需要企业认证，个人免费版可能无法使用。

**Q: 如何获取经纬度？**
A: 使用 `geo` 命令，将地址转换为坐标。

**Q: 路径规划支持哪些方式？**
A: 驾车(driving)、步行(walking)、公交(transit)三种方式。

---

## 📝 更新日志

- **v2.1.0**: 新增 `--with-distance` 参数，POI搜索时显示每个结果的距离
- **v2.0.0**: 新增路径规划、天气查询、实时路况、输入提示功能
- **v1.0.0**: 初始版本，包含 IP定位、地理编码、POI搜索

---

## 📞 支持

- 高德开放平台：https://lbs.amap.com/
- OpenClaw 社区：https://clawd.org.cn/

---

## ⚠️ 免责声明

**本技能仅供学习交流使用，免费提供，不收取任何费用。**

1. **数据准确性**：本工具依赖高德开放平台 API，返回的数据由高德提供，我们不对数据的准确性、完整性、及时性做任何保证。

2. **使用风险**：因使用本技能导致的任何直接或间接损失（包括但不限于商业损失、数据丢失、时间损失），我们不承担任何责任。

3. **API 稳定性**：高德 API 可能存在服务不稳定、调用限制、接口变更等情况，可能导致功能不可用。

4. **用户责任**：用户需自行确保 API Key 的安全妥善使用，遵守高德开放平台的服务条款。

5. **无担保**：本技能按「原样」提供，不提供任何明示或暗示的担保。

**使用本技能即表示您理解并同意上述免责声明。**
