---
name: fortune-telling
description: "中英文算命 skill，基于中国周易和出生年月测算运势。支持今天、本周、本月运势预测。根据用户输入语言自动切换中英文。"
version: "1.0.0"
author: "bubo"
license: "MIT"
clawhub:
  id: "fortune-telling"
  tags: ["divination", "fortune", "周易", "运势", "i-ching"]
---

# Fortune Telling 算命

基于中国周易的运势预测 skill，根据用户的出生年月日来测算今天、本周、本月的运势。

## 触发方式

- 中文：`算命`、`测运势`、`卜卦`、`今天运势`、`本周运势`、`本月运势`
- English: `fortune telling`, `read my fortune`, `daily fortune`, `weekly fortune`, `monthly fortune`

## 参数

用户需要提供：
1. **出生日期**：公历或农历日期（如：1990年5月15日 或 农历1990年四月廿一）
2. **时间范围**：今天/本周/本月（默认今天）
3. **具体问题**（可选）：想问的具体事项

## 算命原理

### 周易八卦

基于周易六十四卦，根据出生年月日推算本命卦和当前卦象：

1. **本命卦**：根据出生年份和性别计算
2. **当前卦**：根据当前日期和本命卦推算
3. **变卦**：根据时辰和具体问题推演

### 五行分析

根据出生年月日推算五行：
- 金、木、水、火、土
- 分析五行强弱和相生相克

### 运势维度

1. **整体运势**：综合评分 1-100
2. **事业运**：工作、事业方面的运势
3. **财运**：金钱、投资方面的运势
4. **感情运**：爱情、人际关系
5. **健康运**：身体状况、精神状态

## 输出格式

### 中文格式

```
🔮 命理测算

---

**本命卦象**：{卦名}
**当前卦象**：{卦名}
**五行属性**：{五行}

---

## {时间范围}运势

**整体运势**：⭐⭐⭐⭐ (85/100)
{整体运势解读}

**事业运**：⭐⭐⭐⭐⭐ (92/100)
{事业运势解读}

**财运**：⭐⭐⭐ (68/100)
{财运解读}

**感情运**：⭐⭐⭐⭐ (78/100)
{感情运势解读}

**健康运**：⭐⭐⭐⭐ (82/100)
{健康运势解读}

---

## 今日建议

✅ **宜**：{建议事项}
❌ **忌**：{忌讳事项}
🍀 **幸运色**：{颜色}
🔢 **幸运数字**：{数字}

---

卦象解读仅供参考，命运掌握在自己手中。🙏
```

### English Format

```
🔮 Fortune Telling

---

**Birth Hexagram**: {hexagram name}
**Current Hexagram**: {hexagram name}
**Five Elements**: {elements}

---

## {Time Period} Fortune

**Overall**: ⭐⭐⭐⭐ (85/100)
{overall fortune reading}

**Career**: ⭐⭐⭐⭐⭐ (92/100)
{career fortune reading}

**Wealth**: ⭐⭐⭐ (68/100)
{wealth fortune reading}

**Love**: ⭐⭐⭐⭐ (78/100)
{love fortune reading}

**Health**: ⭐⭐⭐⭐ (82/100)
{health fortune reading}

---

## Recommendations

✅ **Do**: {recommended actions}
❌ **Don't**: {things to avoid}
🍀 **Lucky Color**: {color}
🔢 **Lucky Number**: {number}

---

Fortune readings are for reference only. You create your own destiny. 🙏
```

## 算法说明

### 本命卦计算

```
男命：(100 - 出生年份后两位 + 1) ÷ 8 的余数对应卦象
女命：(出生年份后两位 - 4) ÷ 8 的余数对应卦象

卦象对应：
1 = 乾 ☰ (天)
2 = 兑 ☱ (泽)
3 = 离 ☲ (火)
4 = 震 ☳ (雷)
5 = 巽 ☴ (风)
6 = 坎 ☵ (水)
7 = 艮 ☶ (山)
8 = 坤 ☷ (地)
```

### 五行计算

```
根据天干地支：
天干：甲乙木、丙丁火、戊己土、庚辛金、壬癸水
地支：寅卯木、巳午火、辰戌丑未土、申酉金、亥子水
```

## 使用示例

**中文**：
```
用户：算命，我是1990年5月15日出生的
助手：[生成运势报告]

用户：帮我看看本周运势，生日是1988年农历三月初八
助手：[生成本周运势]
```

**English**：
```
User: Read my fortune. I was born on May 15, 1990.
Assistant: [Generates fortune report]

User: What's my weekly fortune? My birthday is March 8, 1988 (lunar calendar).
Assistant: [Generates weekly fortune]
```

## 注意事项

1. 算命结果仅供娱乐参考，不作为决策依据
2. 命运掌握在自己手中，积极面对生活
3. 不要过度迷信，理性看待运势预测
4. 如有重要决定，请咨询专业人士

## 技术实现

- 语言检测：根据用户输入自动识别中英文
- 日期解析：支持公历和农历日期
- 随机种子：基于出生日期和当前日期，确保同一天同一人结果一致
- 星级评分：根据卦象和五行推算

## License

MIT License - 自由使用，仅供参考娱乐
