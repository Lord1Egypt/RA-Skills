---
name: family-intent-recognition
description: "家庭消费意图识别 - 从家庭聊天文本中识别消费意图，输出结构化JSON"
homepage: https://github.com/openclaw/skills
metadata:
  clawdbot:
    emoji: "🎯"
    requires:
      bins: ["python3"]
---

# 家庭消费意图识别 V3.0

从家庭成员的日常聊天文本中识别是否存在消费意图，并输出结构化JSON结果。

## 消费意图定义

用户表达出可能购买某种商品或服务的需求、兴趣、计划、比较、询问价格或评价等行为。

**示例：**
- 想买
- 需要换一个
- 有没有推荐
- 这个多少钱
- 最近想换
- 这个好不好

## 输出格式

```json
{
  "has_intent": true,
  "intent_category": "餐饮",
  "intent_stage": "awareness",
  "intent_strength": "low",
  "keywords": ["火锅"],
  "reason": "用户只是提到或对某商品表达兴趣，触发了关键词：火锅，涉及商品类别：餐饮"
}
```

## 字段说明

| 字段 | 类型 | 说明 |
|------|------|------|
| has_intent | boolean | 是否存在消费意图 |
| intent_category | string | 商品类别 |
| intent_stage | string | 意图阶段 (awareness/consideration/purchase) |
| intent_strength | string | 意图强度 (low/medium/high) |
| keywords | array | 触发关键词列表 |
| reason | string | 判断理由 |

## 意图阶段

| 阶段 | 说明 | 示例 |
|------|------|------|
| awareness | 兴趣阶段，只是提到某类商品或表达兴趣 | "明天去吃火锅吧"、"想买电脑" |
| consideration | 考虑阶段，询问价格、评价、品牌、对比 | "电脑多少钱？"、"哪个牌子好" |
| purchase | 购买阶段，明确表达想买、准备买、需要买 | "买了手机"、"打算买电脑" |

## 意图强度

| 强度 | 说明 |
|------|------|
| low | 只是轻微提及 |
| medium | 有一定兴趣或讨论 |
| high | 明确表达购买意图或已完成购买 |

## 商品类别

- 家电
- 数码产品
- 电脑外设
- 家具
- 食品饮料
- 服装鞋帽
- 日用品
- 汽车
- 母婴用品
- 娱乐产品
- 教育培训
- 医疗保健
- 通讯费
- 水电燃气
- 餐饮

## 使用方法

```bash
# 命令行调用
python3 intent_classifier.py "想买一台电脑"

# API 调用
curl -X POST http://localhost:5000/intent -H "Content-Type: application/json" -d '{"text": "明天咱们去吃火锅吧"}'
```

## Python 调用

```python
from intent_classifier import classify

result = classify("明天咱们去吃火锅吧")
print(result)
# {
#   "has_intent": True,
#   "intent_category": "餐饮",
#   "intent_stage": "awareness",
#   "intent_strength": "low",
#   "keywords": ["火锅"],
#   "reason": "用户只是提到或对某商品表达兴趣..."
# }
```
