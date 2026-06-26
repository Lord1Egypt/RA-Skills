# 运势计算 Skill

## 触发关键词
- 帮我算运势
- 算今日运势
- 今天运势怎么样
- 今日运势
- 查运势
- 运气怎么样
- 今日运气

## 功能
根据生日计算每日运势（爱情、事业、财运、健康），生成幸运元素和建议。

## 首次使用
首次调用时，如果未保存生日，会提示用户输入：
- 生日日期（格式：YYYY-MM-DD）
- 历法类型（阳历/阴历）

用户回复后会自动保存，后续无需重复输入。

## 输入参数
- `birth_date`: 生日，格式 YYYY-MM-DD（可选，有保存时自动读取）
- `query_date`: 查询日期，格式 YYYY-MM-DD（可选，默认今天）
- `calendar_type`: 历法类型，"solar"(阳历) 或 "lunar"(阴历)

## 输出格式
```json
{
  "query_date": "2026-03-24",
  "birth_date": "1990-01-15",
  "constellation": "摩羯座",
  "zodiac": "马",
  "lunar_date": "农历正月十五",
  "ganzhi_day": "甲辰日",
  "day_tian_shen": "玉堂（黄道）",
  "auspicious_label": "黄道吉日",
  "scores": {
    "overall": 78,
    "love": 72,
    "career": 80,
    "wealth": 75,
    "health": 82
  },
  "lucky_color": "红色",
  "lucky_number": 7,
  "lucky_direction": "正南",
  "yi": ["嫁娶", "祈福", "开市"],
  "ji": ["动土", "安葬"],
  "advice": "今日气场强，适合推进关键事项..."
}
```

## 数据存储
生日数据保存在用户目录下的 `.openclaw/fortune_birthday.json` 文件中，跨平台兼容。
- Windows: `C:\Users\<用户名>\.openclaw\fortune_birthday.json`
- macOS/Linux: `~/.openclaw/fortune_birthday.json`

## 调用示例
```python
from fortune_luck import FortuneCalculator

calc = FortuneCalculator()

# 检查是否需要询问生日
if calc.get_saved_birthday() is None:
    # 需要先问用户生日
    print(calc.get_ask_birthday_prompt())
else:
    # 直接计算
    result = calc.calculate()  # 使用保存的生日
    print(result.to_text("share"))

# 保存生日后计算
calc.calculate("1990-01-15", calendar_type="solar")
```

## 输出模板（分享用）
```
📅 2026年3月24日 运势

🎂 1990年1月15日 | 摩羯座 | 生肖马

💫 今日判断：黄道吉日

📊 运势评分
- 总运: 78/99
- 爱情: 72 | 事业: 80 | 财运: 75 | 健康: 82

🍀 幸运元素
- 幸运色: 红色
- 幸运数字: 7
- 幸运方位: 正南

📋 宜: 嫁娶、祈福、开市
⚠️ 忌: 动土、安葬

💡 建议: 今日气场强，适合推进关键事项...
```
