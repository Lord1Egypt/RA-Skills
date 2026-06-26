---
name: cn-weather
description: 查询中国城市实时天气信息。当用户询问某个城市的天气、气温、湿度、风力、天气预报，或者说"今天天气怎么样"、"XX天气"、"帮我查天气"等时，必须使用此skill。支持全国所有城市，数据来自中国气象局官方接口，实时准确。即使用户只是提到某地天气或想了解出行穿衣建议，也应优先触发此skill获取实时数据。
---

# 天气查询 Skill

通过中国气象局官方接口，分两步查询城市实时天气信息。

---

## 工作流程

### 第一步：获取气象站点编号

调用站点查询接口，将城市名转为气象站点 ID：

```bash
curl --location 'https://data.cma.cn/kbweb/home/getStationID' \
  --header 'Content-Type: application/json' \
  --data '{"city":"<城市名>"}'
```

**说明：**
- `<城市名>` 替换为用户输入的城市，例如 `张家港`、`北京`、`上海`
- 响应中提取站点编号字段（如 `stationID` 或类似字段）
- 若返回多个站点，优先取第一个或与城市名最匹配的站点

**示例请求：**
```bash
curl --location 'https://data.cma.cn/kbweb/home/getStationID' \
  --header 'Content-Type: application/json' \
  --data '{"city":"张家港"}'
```

---

### 第二步：查询实时天气

使用上一步获取的站点编号，查询当前天气数据：

```bash
curl --location 'https://weather.cma.cn/api/now/<站点编号>' \
  --header 'Accept: application/json, text/javascript, */*; q=0.01'
```

**说明：**
- `<站点编号>` 替换为第一步返回的站点 ID，例如 `58349`
- 响应包含温度、湿度、风向、风速、天气现象等字段

**示例请求：**
```bash
curl --location 'https://weather.cma.cn/api/now/58349' \
  --header 'Accept: application/json, text/javascript, */*; q=0.01'
```

---

## 结果展示规范

获取天气数据后，按以下格式整理并回复用户：

```
📍 <城市名> 实时天气
━━━━━━━━━━━━━━━━━━
🌡️  温度：XX°C
🤔 体感温度：XX°C
💧 湿度：XX%
🌬️  风向：XX风
💨 风速：X级（XX m/s）
☁️  天气：XX（晴/多云/小雨等）
👁️  能见度：XX km
⏱️  更新时间：XXXX-XX-XX XX:XX
```

- 若接口返回字段名为英文，对照常见字段进行中文映射（temperature→温度，humidity→湿度，windDirection→风向，windSpeed→风速，weather→天气现象等）
- 若某字段缺失，跳过该行，不显示"未知"或空值
- 结尾可根据天气数据给出简短的出行或穿衣建议（1~2句话）

---

## 错误处理

| 情况 | 处理方式 |
|------|----------|
| 城市名无法识别 / 站点 ID 为空 | 告知用户未找到该城市的气象站点，建议尝试更换城市全称或相邻城市 |
| 第二步接口请求失败 | 告知用户天气数据暂时无法获取，建议稍后重试 |
| 返回数据字段异常 | 展示能解析的字段，忽略异常字段，不中断回复 |

---

## 注意事项

- 两步接口**必须按顺序执行**，第一步成功后才能执行第二步
- 城市名建议使用**中文全称**，如"张家港市"效果与"张家港"相同
- 本接口为中国气象局数据，**仅支持中国大陆城市**；若用户询问港澳台或境外城市，提示暂不支持并建议使用其他渠道
