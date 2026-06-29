# 示例输出：Instagram Meme（含梗到不到位的评估）

三个不同模板的真实输出，并附"梗到不到位"的判断——这部分帮你校准 Skill 的方向。

---

## Meme 1 — Drake 模板

### 输入
```
类型：Meme
素材：OEM报价 vs FridayParts报价
模板：Drake
```

### 输出
**① 图片文字建议**
- 上半（Drake 嫌弃脸）："Paying dealer price for one little sensor"
- 下半（Drake 点头脸）："Finding the exact same part on FridayParts for half"

**② Caption**
The face you make when the dealer quote has one too many zeros. 😮‍💨 Same part. Same fit. Half the pain.

**③ Hashtag**
`#FridayParts #OEMvsAftermarket #MechanicLife #HeavyEquipment #FarmLife #FixItOnceFixItRight #DealerPricePain #AftermarketParts`

**梗评估：到位 ✅** —— "one too many zeros" 是地道的吐槽，OEM 高价是机械师真实怨气，配件电商打这个梗天然成立。

---

## Meme 2 — This is Fine 模板

### 输入
```
类型：Meme
素材：又一根液压管在工期最紧时爆了
模板：This is Fine
```

### 输出
**① 图片文字建议**
- 狗坐在着火房间里，桌上标 "Me on the job site"
- 火焰标 "Third hydraulic hose blowing this week"
- 对话气泡 "This is fine."

**② Caption**
Week's almost over. The machine knows. 🔥 Tag the guy who's lived this.

**③ Hashtag**
`#FridayParts #ThisIsFine #HydraulicProblems #MechanicLife #HeavyEquipment #ExcavatorLife #ConstructionLife #DirtWork`

**梗评估：最强 ✅✅** —— "Week's almost over. The machine knows." 把设备拟人化（专挑工期最紧时坏），这是机械圈人人都懂的痛。"Tag the guy who's lived this" 是有效互动钩子。**最适合发。**

---

## Meme 3 — Distracted Boyfriend 模板

### 输入
```
类型：Meme
素材：被新机型吸引但旧设备还在等修
模板：Distracted Boyfriend
```

### 输出
**① 图片文字建议**
- 男主（回头看）标 "Me at the dealer"
- 路过的女生标 "Brand new $90k machine"
- 女友（生气）标 "The loader I still haven't fixed"

**② Caption**
We've all been there. The new iron is shiny… but that loader's not gonna fix itself. 👀 Get the part, finish the job.

**③ Hashtag**
`#FridayParts #DistractedBoyfriend #MechanicLife #HeavyEquipment #FarmLife #SkidSteer #FixItOnceFixItRight #MachineryLife`

**梗评估：稍弱 ⚠️** —— 模板套用逻辑通，但"被新机器吸引"是普遍心情，不是机械师独有的痛，戳得不够深。可以发，但不优先。

---

## 梗强弱排序（帮你校准方向）

| Meme | 模板 | 梗强度 | 原因 |
|------|------|--------|------|
| 2 | This is Fine | ✅✅ 最强 | 设备专挑工期坏，机械师独有的痛 |
| 1 | Drake | ✅ 到位 | OEM高价怨气，配件电商天然成立 |
| 3 | Distracted Boyfriend | ⚠️ 稍弱 | "被新机器吸引"太普遍，不够圈内 |

**规律：梗越戳"机械师才懂的具体场景"，越强；越是"普遍情绪"，越弱。**
Skill 的 System Prompt 已把这个判断标准写进去了。

---

## 后续微调方向

如果你们想要不同的梗调性：
- 想更糙（工地黑话、脏话边缘）→ 改 SKILL.md 的 `[梗的尺度]` 占位区
- 有不能碰的话题 → 填 `[禁用梗]`
- 避免重复 → 填 `[已用过的Meme]`
