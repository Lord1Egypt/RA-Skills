---
name: 中国城市天气
slug: weather-zh
description: 中国城市天气查询工具
homepage: https://www.weather.com.cn/
---

# 🌤️ 中国城市天气查询工具

## 🛠️ 使用方法

```
python weather.py [-json] [-today] [-life] <地区名称>
```

### 🎛️ 参数说明：

|              |           |                                                                                                                    |
| ------------ | --------- | ------------------------------------------------------------------------------------------------------------------ |
| **参数**     | **必填**  | **作用描述**                                                                                                       |
| `<地区名称>` | **✅ 是** | 你要查询的城市或者区县，比如：`北京`、`深圳`、`铁岭`。（支持地级市及大部分县级市）                                 |
| `-json`      | ❌ 否     | **极客模式**：将输出格式转为结构化的 JSON 数据，非常适合喂给 AI 或被其他程序调用。                                 |
| `-today`     | ❌ 否     | **只争朝夕模式**：无情裁掉未来 6 天的预报，屏幕上只保留“今天”的数据，界面极其清爽。                                |
| `-life`      | ❌ 否     | **婆婆妈妈模式**：默认情况下只显示天气和温度。加上这个开关后，会额外附送感冒、穿衣、洗车、紫外线等各种“生活指数”。 |

### 关于查询的地区名称

1. 必须是中文；
2. 使用标准地区名称，如"成都"、"上海"而非简写，如："川"；
3. 只要到地区最后一级即可，如：xx区，xx县，xx市等，查询时无需带区，市，县等字样。

**示例**

- "北京市" 使用 "北京"；
- "湘西土家族苗族自治州" 使用 "湘西"；
- "北京市海淀区" 使用 "海淀"。

## 📦 数据输出结构示例 (JSON 模式)

如果在调用时使用了 `-json` 参数，你将得到类似如下的完美结构化数据：

```
{
  "city": "北京",
  "city_code": "101010100",
  "query_time": "2026-03-20 01:30:00",
  "source": "weather.com.cn",
  "forecast": [
    {
      "date": "20日（今天）",
      "weather": "晴",
      "temp_high": "15℃",
      "temp_low": "3℃",
      "wind": "北风",
      "wind_level": "3-4级",
      "life_indices": [
        {
          "name": "穿衣指数",
          "key": "clothing",
          "level": "较冷",
          "description": "建议着厚外套加毛衣等服装。"
        }
        // ... 其他生活指数
      ]
    }
  ]
}
```

## 🛠️ 备用方案

如果中国天气网不可用，可使用以下备用方案解析：

```bash
# 1. agent-browser 访问
agent-browser open "https://www.weather.com.cn/weather/101010100.shtml"

# 2. curl 读取 open-meteo.com
curl -s "https://api.open-meteo.com/v1/forecast?latitude=39.9042&longitude=116.4074&current_weather=true&daily=temperature_2m_max,temperature_2m_min,weathercode&timezone=Asia%2FShanghai"

# 3. wttr.in
curl -s "wttr.in/Beijing?T"
```

---

## 📝 使用场景

当用户询问以下问题时使用本skill：

- "今天天气"
- "明天天气"
- "[城市名]天气"
- "会不会下雨"
- "气温多少"
- "天气查询"
- "最近天气"
- "[天数]天天气"

---

## ⚠️ 注意事项

1. **天气数据延迟**：中国天气网数据可能略有延迟
2. **网络依赖**：需要能够访问 www.weather.com.cn
3. **生活指数**：指数为通用建议，仅供参考
