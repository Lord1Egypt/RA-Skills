# ⛅ 中国天气查询工具

一个轻量级的中国城市天气查询工具，数据来源于中国天气网 (weather.com.cn)。

## ✨ 功能特性

- **零第三方依赖**：纯原生 urllib 实现，无需 pip install 任何依赖
- **动态城市代码**：优先从本地 citys.txt 读取，找不到自动在线搜索
- **智能参数解析**：支持多种输出格式，参数顺序灵活
- **7天天气预报**：获取未来一周的天气情况
- **生活指数**：提供穿衣、洗车、紫外线等生活建议

## 🚀 快速开始

### 基本用法

```bash
python weather.py [-json] [-today] [-life] <城市名>
```

### 参数说明

| 参数       | 必填 | 说明                                   |
| ---------- | ---- | -------------------------------------- |
| `<城市名>` | ✅   | 要查询的城市名称，如：北京、深圳、铁岭 |
| `-json`    | ❌   | 输出 JSON 格式，适合程序调用           |
| `-today`   | ❌   | 只显示今天的天气                       |
| `-life`    | ❌   | 显示生活指数（穿衣、洗车、紫外线等）   |

### 使用示例

```bash
# 查询南京7天天气
python weather.py 南京

# 查询深圳今天天气，附带生活指数
python weather.py -today -life 深圳

# 查询北京天气，输出 JSON 格式
python weather.py -json 北京

# 组合使用
python weather.py -json -life -today 上海
```

## 📍 关于城市名称

1. 必须使用中文
2. 使用标准地区名称，如"成都"、"上海"而非简写
3. 只需写到地区最后一级，无需带"市"、"区"、"县"等字样

**示例**：

- "北京市" → 使用 "北京"
- "湘西土家族苗族自治州" → 使用 "湘西"
- "北京市海淀区" → 使用 "海淀"

## 📦 数据输出结构

使用 `-json` 参数时，输出结构如下：

```json
{
  "city": "北京",
  "city_code": "101010100",
  "query_time": "2026-03-22 10:30:00",
  "source": "weather.com.cn",
  "forecast": [
    {
      "date": "22日（今天）",
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
      ]
    }
  ]
}
```

## 🔄 备用方案

如果中国天气网不可用，可使用以下备用方案：

```bash
# 使用 wttr.in
curl -s "wttr.in/Beijing?T"

# 使用 open-meteo.com
curl -s "https://api.open-meteo.com/v1/forecast?latitude=39.9042&longitude=116.4074&current_weather=true&daily=temperature_2m_max,temperature_2m_min,weathercode&timezone=Asia%2FShanghai"
```

## ⚠️ 注意事项

1. **数据延迟**：中国天气网数据可能略有延迟
2. **网络依赖**：需要能够访问 www.weather.com.cn
3. **生活指数**：指数为通用建议，仅供参考

## 🙏 致谢

- 本项目实现参考了以下项目：[China Weather](https://clawhub.ai/hoopan007/weather-china)
- 感谢中国天气网 (weather.com.cn) 提供的天气数据。

## 📄 许可证

本项目采用 MIT 许可证，详见 [LICENSE](LICENSE) 文件。
