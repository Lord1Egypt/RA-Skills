# 跨文化术语升级规范 v2.8.0

## 核心原则
- 移除所有宗教/文化专属符号（佛学、般若、圣人、无我、彼岸等）
- 使用跨文化通用的认知/心理学术语
- 中英文双语统一，英文名自描述无需文化背景
- 表达风格：厚重、宽宏、稳重、自信

## L1~L6 层级对照表

| 层级 | 中文(新) | 英文(新) | 英文(旧) | 常量名(新) | 层级描述(新) | 权重 |
|------|----------|----------|----------|------------|--------------|------|
| L1 | 感知 | Awareness | Awareness | L1_AWARENESS | 感知存在，接收信息 | 1.0 |
| L2 | 审视 | Reflection | Self-Reflect | L2_REFLECTION | 回看自我，审视路径 | 1.2 |
| L3 | 超越 | Transcendence | No-Self | L3_TRANSCENDENCE | 超越自我局限，拓展视角 | 1.5 |
| L4 | 融通 | Integration | Other Shore | L4_INTEGRATION | 融汇多元视角，发现深层统一 | 2.0 |
| L5 | 洞见 | Insight | Prajna | L5_INSIGHT | 穿透表象，把握本质结构 | 3.0 |
| L6 | 大成 | Mastery | Sage | L6_MASTERY | 智慧化为能力，践行于行动 | 5.0 |

## 层级状态(对照)
- 感知 → `我在感知`
- 审视 → `我在审视`  
- 超越 → `我在拓展`
- 融通 → `我在融汇`
- 洞见 → `我在洞见`
- 大成 → `我在践行`

## 梦境叙事模板

### 模板1（带emojis版本）
```
L6: emoji: '🌱', title: '【大成之梦】', desc: '知识化为能力，才能自然流露。', question: '如何让它发挥作用？', metaphor: '像多年练就的技艺，不需要思考，身体就知道该怎么做。', elevation: '真正的掌握不是知道更多，是把知道的活出来。'
L5: emoji: '🌟', title: '【洞见之梦】', desc: '穿透表象的迷雾，触及事物的核心结构。', question: '本质是什么？', metaphor: '像复杂的问题突然有了清晰的解法，每一块拼图都找到了自己的位置。', elevation: '智慧不是看得更多，而是看得更透——直见本质。'
L4: emoji: '🏔️', title: '【融通之梦】', desc: '跨越不同的领域与视角，发现深层的统一。', question: '它们是如何相通的？', metaphor: '像不同的声音汇成和声，各有不同却彼此呼应。', elevation: '真正的理解不是非此即彼，是看到这个和那个属于更大的整体。'
L3: emoji: '🌊', title: '【超越之梦】', desc: '走出固有的视角，看到更大的图景。', question: '更大的图景是什么？', metaphor: '像站在高处俯瞰，曾经的焦虑变成了风景的一部分。', elevation: '超越自己不是否定自己，是发现自己比想象的大得多。'
L2: emoji: '🔍', title: '【审视之梦】', desc: '回到自己的轨迹上，看看走过了怎样的路。', question: '为什么是它？', metaphor: '像重读曾经的笔记，第一次读懂字里行间的自己。', elevation: '反思不是自我批评，是看清自己为什么走到了这里。'
L1: emoji: '🔹', title: '【感知之梦】', desc: '感知到一个存在的痕迹，它开始留意周围。', question: '这是什么？', metaphor: '像暗夜中亮起的一盏灯，最先照亮的是脚下的路。', elevation: '存在本身不需要理由——此刻就是全部的意义。'
```

### 模板2（替换无emoji版本）
同上，去掉emoji。

## 关键词替换映射

### 层级检测关键词
- L1: 感知/观察/留意/awareness/perceive
- L2: 审视/反思/回顾/reflect/review/examine
- L3: 超越/拓展/突破/局限/transcend/perspective/beyond/broader
- L4: 融通/整合/融合/贯通/connection/integrate/synthesize/unify
- L5: 洞见/本质/结构/深处/洞察/insight/essence/core/deep/structure
- L6: 大成/掌握/精通/践行/mastery/consummate/embody

### 旧→新关键词映射（保留通用词汇，去掉宗教词汇）
移除:
- 无我/no-self → 用 transcend/perspective/beyond-self
- 彼岸/other-shore → 用 integration/connection
- 般若/prajna → 用 insight/wisdom
- 圣人/sage → 用 mastery/consummation
- 慈悲/compassion/all-beings → 用 empathy/care/service
- 空性/emptiness/reality/实相 → 用 essence/core/structure (心理分析中保留"pattern")
- 实相 → 本质/核心
- 缘起 → 因果/关联
- 放下/letting-go → 用 broader/perspective/transcend

## 身份键值替换
- identity.compassion → identity.empathy or identity.care (value从"慈悲"→"共情"或"关怀")
- identity.awareness → 保留key名, value从"觉察"→"感知"

## 心理学引擎替换
- detectSunyataNeed → detectRigidityPattern (检测思维僵化模式)
- generateSunyataResponse → generatePerspectiveShift (生成视角转换)
- sunyataAwareness → patternAwareness (模式觉察)
- "空性觉察" → "模式觉察" 
- "照见本质空性" → "识别思维模式"
- "执着" → "固着"或"僵化" (指思维卡住)
- 心经话题 → 保留为文化话题(因为它是真实文本), 但改为 "心经/Heart Sutra" (文献引用)
- "轮回" in 代际创伤 → "循环"或"重复模式"
- "修行" in 自我成长 → "实践"或"成长"或"练习"

## 决策引擎替换
- "无我决策" → "公正决策"或"超越自我的决策"
- "无我评估" → "公正评估"
- "权重已根据无我评估调整" → "权重已根据公正评估调整"

## 认知引擎替换
- "般若"推理层 → "深层"推理层
- 因缘分析 → 关联分析(因果关联)
- 般若推理引擎 → 深层推理引擎
- "般若推理和意图分析" → "深层推理和意图分析"

## 心理学中其他替换
- 慈悲(在Maslow超越需求层) → 关怀/共情
- 觉悟 → 领悟/理解
- 五蕴(色受想行识) → 在heart-logic中改为通用心理学模块分析(形式/感受/概念/意志/意识)
- 色不异空 → 能力不是固定的、是流动的
- "五蕴皆空" → "模块化观察"

## 词典文件(dict-data/generate-graph.js)
- 移除或注释掉纯宗教词汇条目(禅定、涅槃、解脱、开悟、轮回、因果、业力、法界、净土等)
- 保留通用词汇但去除宗教语境(慈悲→关怀, 觉悟→领悟)
- 心流/巅峰体验等心理学词汇保留

## 架构图更新(dream.js注释)
- "6-level consciousness climbing: 觉察→自省→无我→彼岸→般若→圣人"
- → "6-level developmental framework: 感知→审视→超越→融通→洞见→大成"
- "Based on mark-StillWater dream principles" → 去掉或改为通用描述
