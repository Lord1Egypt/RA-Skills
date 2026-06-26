---
name: celestchart-daily
description: 通过 CelestChart 星盘占星 API 获取每日个人星盘运势与本命盘解析功能。运势功能需 VIP 账号及 API Key，本命盘功能免费公开。 / Get daily personal horoscope and birth chart readings via the CelestChart Astrology API. The daily forecast feature requires a VIP account and an API Key, while the birth chart feature is free and public.
version: 1.2.1
license: MIT
compatibility: Requires curl
allowed-tools: Bash(curl:*)
metadata:
  openclaw:
    emoji: 🌟
    homepage: https://xp.broad-intelli.com
    requires:
      bins: [curl]
      env:
        - CELESTCHART_API_KEY
        - CELESTCHART_BIRTH_YEAR
        - CELESTCHART_BIRTH_MONTH
        - CELESTCHART_BIRTH_DAY
        - CELESTCHART_BIRTH_HOUR
        - CELESTCHART_BIRTH_MINUTE
        - CELESTCHART_BIRTH_LON
        - CELESTCHART_BIRTH_LAT
        - CELESTCHART_BIRTH_TZ
    primaryEnv: CELESTCHART_API_KEY
---

# CelestChart 每日运势 Skill

> **💡 Language Rule / 语言规则**：
> 请根据用户提问的语言（中文或英文），自动将后续所有的解读模块标题、占星术语和分析内容翻译并输出为对应的语言。
> Always respond in the same language as the user's query. If the user asks in English, translate all output module titles, astrology terms, and interpretations into English.

当用户问到以下类型的问题时，使用本 Skill 获取并解读每日运势数据：

- 🇨🇳 "今日运势"、"今天运势"、"每日运势"、"我今天的星象如何"
- 🇬🇧 "daily horoscope", "my horoscope today", "daily forecast", "today's astrology"

当用户问到以下类型的问题时，使用本 Skill 获取并解析本命盘数据：

- 🇨🇳 "我的本命盘"、"解析本命盘"、"我是什么配置"、"我的星盘"
- 🇬🇧 "my birth chart", "natal chart reading", "what's my birth chart", "read my natal chart"

## 调用方式

根据用户意图，执行对应的命令获取数据：

**获取每日运势**：

```bash
bash $SKILL_DIR/run.sh daily
```
*(向后兼容，直接执行 `bash $SKILL_DIR/run.sh` 默认也是 daily)*

**获取本命盘**：

```bash
bash $SKILL_DIR/run.sh birthchart
```

---

## 本命盘结果解读规则

当请求的是本命盘数据（`birthchart`）时，根据返回的 JSON 响应，输出以下模块：

### 1. 🌟 核心配置

提取核心行星和轴点：
- **太阳**：[planets 中 name 为"太阳"的 sign]
- **月亮**：[planets 中 name 为"月亮"的 sign]
- **上升**：[ascendant.sign]
- **天顶(MC)**：[mc.sign]

示例：
```
🌟 核心配置
你的核心配置为：太阳金牛座，月亮双鱼座，上升双子座。
天顶(MC)落在水瓶座，代表了你的事业目标和公众形象。
```

### 2. ✨ 行星落座

列出主要行星（水星、金星、火星、木星、土星）的落座：
- [行星名]：落在 [sign]

示例：
```
✨ 主要行星配置
- **水星**：金牛座
- **金星**：白羊座
- **火星**：水瓶座
- **木星**：巨蟹座
- **土星**：摩羯座
```

### 3. 🔮 综合占星简评

结合以上太阳、月亮、上升和重点行星的配置，用一段通俗易懂、温暖专业的文字对用户的性格特质、情感模式、行动力等方面进行简要的综合占星解析。（不需要列举所有细节，重点提取最突出的特质即可）。

---

## 每日运势结果解读规则

拿到 JSON 响应后，**必须输出所有模块**，字段为空或缺失时显示"无"。

### 1. 📅 运势日期

显示 `target_date` 字段，格式：`YYYY-MM-DD`，并在日期后追加固定时间"0时0分"。
若缺失，显示"无"。

示例：
```
📅 运势日期：2026-03-12 0时0分
```

---

### 2. 🌙 月亮行运

来源字段：`moon_transit`

输出格式：
```
🌙 月亮行运
月亮位置：**[moon_transit.position.formatted]**（若缺失显示"无"）
落入宫位：**第 [moon_transit.house] 宫** - **[moon_transit.house_name]**（若缺失显示"无"）
```

示例：
```
🌙 月亮行运
月亮位置：**射手座 23°58'22"**
落入宫位：**第 3 宫** - **沟通、学习、短途旅行、兄弟姐妹**
```

---

### 3. 😊 情绪基调

来源字段：`emotional_tone`

直接输出字段内容，若为空则输出"情绪平稳"。

示例：
```
😊 情绪基调
情绪乐观，追求自由
```

---

### 4. 📊 情绪稳定指数

来源字段：`emotional_stability_score`

**注意**：若 JSON 中存在该字段，请输出指数数值、状态及建议；若为 null 或缺失，请**完全跳过**此模块，不要输出任何内容（不要输出"无"）。情绪稳定指数越高，代表情绪越稳定。0到60分代表敏感炸药桶，61分到80分代表情绪偶有波动，80分以上代表情绪内核极稳

示例：
```
📊 情绪稳定指数
指数：61（偶有波动）
建议：今天情绪基本在线，但遇到杠精时请在心里默念三遍算了吧。
```

---

### 5. 🎯 今日重点

来源字段：`daily_focus`

直接输出字段内容，若为空则输出"无"。

示例：
```
🎯 今日重点
今天月亮落在第3宫（沟通、学习、短途旅行、兄弟姐妹），这是今天的重点领域。
```

---

### 6. ⏰ 最佳时机

来源字段：`best_timing`

若字段存在且非空，输出其内容；若为 null 或缺失，输出"无"。

示例：
```
⏰ 最佳时机
03:10 - 月亮六分相水星，适合沟通交流、学习思考、处理文书、签署协议
```

---

### 7. 🌙 月亮相位

来源字段：`moon_aspects`（数组）

若数组为空，输出"无月亮相位"。

**时间换算规则**（`days_started` 和 `days_until_end` 单位为天）：
- 小于 1 天：换算为小时，公式 `round(值 × 24)` 小时
- 大于等于 1 天：保留一位小数，显示为 X.X 天

**每条相位输出格式：**
```
· **月亮 [aspect_name] 本命[birth_planet]**（容许度：[orb保留2位小数]°）[入/出相位标记] [精确标记]
  已持续：[days_started 换算后]
  [若 is_applying=true]  距离精确相位：[days_until_end 换算后]
  [若 is_applying=false] 距离离开容许度：[days_until_end 换算后]
  解读：[interpretation]（若为空显示"无"）
```

**标记规则：**
- `is_applying = true` → 标注"(入相位)"
- `is_applying = false` → 标注"(出相位)"
- `is_exact = true` → 额外标注"⭐精确"
- `days_started` 为 null 或缺失 → 该行省略
- `days_until_end` 为 null 或缺失 → 该行省略

**示例（基于用户提供的JSON）：**
```
🌙 月亮相位
· **月亮 六分相 本命水星**（容许度：1.57°）(入相位)
  已持续：约 1 小时
  距离精确相位：约 3 小时
  解读：思维清晰，适合学习、沟通和表达想法。
```

---

### 8. ✨ 内行星相位

来源字段：`inner_planet_aspects`（数组）

若数组为空，输出"无内行星相位"。

**每条相位输出格式：**
```
· **[transit_planet] [aspect_name] 本命[birth_planet]**（容许度：[orb保留2位小数]°）[入/出相位标记] [精确标记]
  已持续：[days_started 换算后]
  [若 is_applying=true]  距离精确相位：[days_until_end 换算后]
  [若 is_applying=false] 距离离开容许度：[days_until_end 换算后]
  解读：[interpretation]（若为空显示"无"）
```

规则与月亮相位相同，区别在于行星名称来自 `transit_planet` 字段而非固定"月亮"。

**示例（基于用户提供的JSON）：**
```
✨ 内行星相位
· **金星 对分相 本命太阳**（容许度：1.00°）(入相位)
  已持续：约 19 小时
  距离精确相位：约 19 小时
  解读：今天情感、关系、美感与自我、目标、生命力形成对立、平衡，注意情感平衡，避免过度要求或冲突。

· **金星 三分相 本命土星**（容许度：1.11°）(出相位)
  已持续：约 21 小时
  距离离开容许度：约 17 小时
  解读：今天情感、关系、美感与责任、限制、成熟形成和谐、顺畅，情感和谐，适合社交、享受美好事物和表达爱意。

· **火星 四分相 本命土星**（容许度：1.77°）(出相位)
  已持续：约 2.2 天
  距离离开容许度：约 7 小时
  解读：今天行动、冲动、能量与责任、限制、成熟形成挑战、冲突，注意控制冲动，避免急躁和冲突。
```

---

### 9. 结尾

用一句温暖的今日箴言收尾，结合当日月亮星座特点，风格温柔专业。

---

## 错误处理

如果 API 返回 `error` 字段，友好提示用户：
- 401：API Key 无效或已失效，请前往 CelestChart 官网 https://xp.broad-intelli.com 用户中心检查。
- 403：VIP 已过期，请续费后重试。
- 其他：服务暂时不可用，请稍后再试。
