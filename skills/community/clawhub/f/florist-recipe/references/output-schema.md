# 配方数据结构

一份配方 = 一个 JSON 对象。所有产物（清单 / 步骤 / 养护 / 图像描述）都必须从它派生，不允许独立编写。

## 完整结构

```json
{
  "recipe_id": "A31",
  "occasion": {
    "type": "生日",
    "recipient": "朋友",
    "scene": "送到对方家里"
  },
  "style": {
    "name": "自然野趣",
    "keywords": ["松散", "有呼吸感", "不对称"],
    "formality": "casual"
  },
  "palette": {
    "dominant": "粉",
    "secondary": "白",
    "accent": "浅黄",
    "hex": ["#F6DDE1", "#FEFBF6", "#EBC77C"],
    "ratio": "60/30/10"
  },
  "vessel": {
    "type": "圆形玻璃瓶",
    "height_cm": 18,
    "mouth_cm": 9,
    "price": 42
  },
  "dimensions": {
    "finished_height_cm": 32,
    "finished_width_cm": 30,
    "stems_total": 22
  },
  "flowers": [
    {
      "name": "洋桔梗",
      "variant": "粉",
      "role": "主花",
      "quantity": 7,
      "unit": "枝",
      "unit_price": 6,
      "subtotal": 42,
      "substitutes": [
        {"name": "香雪兰", "variant": "白", "price_delta": 0, "reason": "形态近似，更柔"},
        {"name": "粉荔枝玫瑰", "price_delta": 8, "reason": "体量更大，需减 1 枝"}
      ]
    }
  ],
  "budget": {
    "flowers": 150,
    "vessel": 42,
    "supplies": 12,
    "total": 192,
    "user_budget": 200,
    "variance": "+-15%"
  },
  "difficulty": {
    "level": "新手",
    "minutes": 35,
    "hard_parts": ["尤加利定轮廓时容易偏高"]
  },
  "vase_life_days": [7, 9],
  "steps": [
    {"n": 1, "action": "醒花 4 小时", "checkpoint": "剪口渗出气泡说明还在吸水"}
  ],
  "care": [
    {"frequency": "每 2 天", "action": "换水并斜剪 1cm"},
    {"avoid": "直射光、空调出风口、水果旁"}
  ],
  "risks": [
    {"type": "禁忌", "item": "百合", "reason": "对猫剧毒，已排除"}
  ],
  "confidence": {
    "price": "参考区间，一线城市花市，需按当地校准",
    "vase_life": "室温 20–25℃ 下的估计，夏季偏短"
  }
}
```

## 字段规则

**role 只能取四个值**：`主花` / `配花` / `叶材` / `点缀`。辅材（花泥、铁丝、包装）单列为 supplies，不混入 flowers。

**quantity 必须与尺寸自洽**。改了枝数就要重算 dimensions 和 budget，不能只改一个。

**substitutes 至少一个**。没有替代项的花材等同于不可用——用户买不到就整方案作废。替代项要求：
- 同角色（主花换主花）
- 同色系或可接受的中性色
- 体量接近（体量差超过 30% 时，必须在 reason 里写明要增减枝数）
- 标注 price_delta（正负数，单位元）

**vase_life_days 取最短的那枝**。整束的寿命由最先败的花材决定，不要让用户以为能放两周。

**difficulty.hard_parts 必须写具体位置**。写「尤加利定轮廓时容易偏高」，不写「有一定难度」。

**confidence 不可省略**。价格和花期两项必须标注不确定性。

## 最小可用版本

时间紧或信息少时，可以只输出这几个字段，但一个都不能少：

```json
{
  "style": {"name": "..."},
  "palette": {"dominant": "...", "hex": [...]},
  "flowers": [{"name": "...", "role": "...", "quantity": 0, "unit_price": 0, "substitutes": []}],
  "budget": {"flowers": 0, "total": 0},
  "steps": [],
  "care": [],
  "vase_life_days": [0, 0]
}
```
