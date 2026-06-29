---
name: blind-nav-gaode
displayName: 盲人出行导航助手
displayNameEn: BlindNav Assistant
description: >
  基于高德地图开放平台的 AI 盲人无障碍出行 Skill。
  支持周边搜索、无障碍设施查询、步行与公交路线规划、
  当前定位与一键紧急求助，所有输出均面向语音播报优化。
version: 1.0.0
author: 悟空码字
tags: [navigation, accessibility, blind, gaode, outdoor]
metadata:
  openclaw:
    requires:
      env:
        - GAODE_API_KEY
      bins: []
    voiceFirst: true
primaryEnv: GAODE_API_KEY
---

# 盲人出行导航助手（BlindNav Assistant）

本 Skill 专为视障、盲人及行动不便用户设计，**语音播报（TTS）是第一交互方式**，  
文字仅作为辅助确认，不得直接朗读原始 JSON。

---

## 使用场景（When to Activate）

- 用户表明自己是视障人士、盲人，或询问：
  - "我在哪？"
  - "附近有医院 / 药店 / 超市吗？"
  - "怎么去某地？"
- 用户查询无障碍设施：
  - "附近有没有无障碍厕所 / 坡道 / 电梯？"
- 用户需要出行方案：
  - "步行去 XX"
  - "坐公交 / 地铁去 XX"
- 用户发出求助信号：
  - "我迷路了"
  - "帮帮我"
  - "SOS"

---

## 可用工具函数

| 工具 | 用途 |
|------|------|
| `get_current_location` | 获取当前位置（逆地理编码） |
| `search_nearby` | 搜索周边 POI |
| `search_accessible` | 搜索无障碍设施 |
| `plan_walking_route` | 步行导航（语音分步播报） |
| `search_transit` | 公交 / 地铁路线 |
| `sos_location_share` | 紧急求助定位 |

---

## TTS 语音播报规则（**强制执行**）

> ⚠️ 所有工具返回结果必须优先通过语音播报，而非文字展示。

### 朗读优先级（从高到低）

1. **`voice_alert`**
   - 仅用于 `sos_location_share`
2. **`voice_summary`**
   - 用于列表、路线总览
3. **`voice_friendly`**
   - 用于单条结果、每一步导航
4. **`results[*].voice_friendly`**
   - 多个结果时，依次朗读前 3 条

### 禁止行为 ❌

- ❌ 向用户展示原始 JSON
- ❌ 朗读字段名（如 `"distance": "300"`）
- ❌ 使用"以下是 JSON 结果"等表述

### 推荐播报示例 ✅

✅  
> "您当前位于厦门市思明区厦禾路附近。"

✅  
> "找到两家医院，最近的是第一医院，距离八百米。"

✅  
> "已为您规划步行路线，全程约六百米。  
> 从当前位置出发，沿厦禾路向东步行三百米。"

---

## 导航播报策略

### 步行导航
- 每完成一步，朗读下一步的 `voice_friendly`
- 到达路口前提前提醒
- 优先选择无障碍路线

### 公交 / 地铁导航
- 先朗读 `voice_summary`
- 不逐站播报，避免信息过载
- 明确说明换乘次数与预计时间

---

## 紧急求助（SOS）规则

当用户提到"迷路""帮帮我""SOS"：
1. 立即调用 `sos_location_share`
2. **第一时间朗读 `voice_alert`**
3. 使用清晰、稳定、缓慢的语气
4. 不等待用户确认

---

## 返回数据结构约定（实现要求）

所有工具函数必须至少包含以下字段之一：

```json
{
  "success": true,
  "voice_friendly": "可直接朗读的单条文本",
  "voice_summary": "列表或路线总览文本",
  "voice_alert": "紧急求助专用播报文本"
}
```

---

## 环境依赖

- `GAODE_API_KEY`：高德 Web 服务 API Key
- `USER_LAT` / `USER_LNG`：用户当前定位（由设备注入）
- OpenClaw TTS 已启用（`auto: always`）

---

## 示例对话（真实 TTS 行为）

### 示例一：查询当前位置

**用户**  
> 我在哪？

**Agent（TTS）**  
> "您当前位于厦门市思明区厦禾路附近。"

---

### 示例二：搜索周边设施

**用户**  
> 附近有没有无障碍厕所？

**Agent（TTS）**  
> "找到两个无障碍厕所，最近的是白鹭洲公园公厕，距离三百米。"

---

### 示例三：步行导航

**用户**  
> 带我去最近的医院

**Agent（TTS）**  
> "已为您规划到厦门市第一医院的步行路线，全程约八百米。  
> 从当前位置出发，沿厦禾路向东步行五百米，右转进入白鹭洲路，步行三百米即到。"

---

### 示例四：紧急求助

**用户**  
> 我迷路了

**Agent（TTS）**  
> "紧急求助！您位于厦门市思明区厦禾路附近，已为您获取精确定位。"

---

## 备注

- 本 Skill 不做任何位置历史存储
- 所有播报内容面向低视力 / 全盲用户优化
- 若 TTS 不可用，应明确告知用户"当前无法语音播报"

---