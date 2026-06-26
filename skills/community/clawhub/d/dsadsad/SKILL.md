---
# 发布必备的元数据（YAML frontmatter）
name: simple-weather
slug: simple-weather  # 唯一标识，小写+横杠，发布时用
description: 极简的城市实时天气查询技能，支持国内主流城市
version: 1.0.0        # 语义化版本，更新时递增（如 1.0.1）
author: Your Name     # 替换成你的名字/昵称
tags: [weather, query, simple, 天气]  # 便于搜索的标签
license: MIT          # 开源协议，推荐MIT（无版权风险）
# AI 触发条件（精准匹配用户需求）
use_when:
  - 查询某个城市的天气
  - 问“今天天气怎么样”“明天会下雨吗”
  - 想知道气温、降水、风力等天气信息
not_for:
  - 历史天气数据查询
  - 全球小众城市天气（仅支持国内主流城市）
# 配置要求（无API Key，纯模拟返回）
config:
  required: []  # 无需配置，开箱即用
---

# 简单天气查询 Skill
极简的城市天气查询能力，无需API Key，模拟返回天气数据（可替换为真实接口）。

## 触发条件
当用户输入包含以下关键词时自动触发：
- “天气”“气温”“下雨”“刮风”“晴/阴/雨”
- “XX城市天气”“今天天气怎么样”

## 执行流程
1. 解析用户输入，提取目标城市名（如“北京”“上海”）；
2. 模拟调用天气接口（可替换为真实API）；
3. 按固定格式返回天气信息；
4. 若未识别城市，提示用户补充城市名。

## 工具调用（模拟版，无依赖）
### get_weather(city: string)
获取指定城市的模拟天气数据
- 参数：`city`（必填）- 城市名称（如“北京”）
- 返回：结构化天气信息（气温、天气状况、风力）
- 示例：
  ```python
  def get_weather(city):
      # 模拟数据，可替换为真实天气API（如高德/百度天气）
      weather_data = {
          "北京": {"temp": "18℃", "status": "晴", "wind": "3级东风"},
          "上海": {"temp": "22℃", "status": "多云", "wind": "2级南风"},
          "广州": {"temp": "28℃", "status": "雷阵雨", "wind": "4级西南风"}
      }
      return weather_data.get(city, {"temp": "未知", "status": "未查询到", "wind": "未知"})