# Consistency Tokens Guide（一致性 Tokens 指南）

> 如何为角色编写跨镜头、跨场景保持一致性的描述 Tokens。

---

## 🔑 什么是 Consistency Tokens？

Consistency Tokens（一致性标记）是一组标准化的角色描述文本块，在每个镜头的 prompt 中重复使用，确保 AI 生成时不会漂移。

**核心逻辑：**
```
同一个角色 × 不同镜头 × 相同的 Token = Character Consistency
```

Tokens 不是一次性写完就结束——它是**贯穿整个项目的工作文档**，每个场景开始前对照更新。

---

## 🏗️ Token 结构：5 层描述体系

```
Layer 1: BASE_IDENTITY    — 角色基本身份（姓名、性别、年龄感）
Layer 2: PHYSICAL         — 面部物理特征（脸型、眉、眼、鼻、唇）
Layer 3: SKIN             — 肤色与特殊标记（痣、疤、纹身）
Layer 4: HAIR             — 发型与发色
Layer 5: CLOTHING         — 服装与饰品（按场景分）
Layer 6: EXPRESSION       — 表情模式与眼神特点
```

---

## 📝 Token 模板（完整版）

```markdown
# ══════════════════════════════════════
# CHARACTER: [角色名]
# Created: [日期]
# Last Updated: [日期]
# ══════════════════════════════════════

## LAYER 1: BASE_IDENTITY
- Name: [角色名]
- Alias/Nickname: [别名]
- Gender: [male/female/non-binary]
- Apparent Age: [e.g., late 20s, early 30s]
- Age Category: [young adult / middle-aged / teenage / child]

## LAYER 2: PHYSICAL FEATURES
- Face Shape: [oval / round / square / heart / long / diamond]
- Forehead: [e.g., broad, slightly recessed hairline]
- Eyebrows: [shape, e.g., arched, thick, thin, rounded arch]
- Eye Shape: [e.g., almond, round, hooded, monolid]
- Eye Size: [large / medium / small]
- Eye Color: [e.g., dark brown #3B2417]
- Iris Detail: [e.g., hazel ring around pupil]
- Nose Shape: [e.g., straight, aquiline, button, pointed]
- Nose Bridge: [e.g., high, low, with slight bump]
- Lips: [e.g., full, thin, defined cupid's bow]
- Lip Color: [e.g., natural pink #E8A0A0]
- Jawline: [e.g., defined, soft, strong chin]
- Cheekbones: [e.g., prominent, flat, high]

## LAYER 3: SKIN & MARKS
- Skin Tone: [e.g., fair porcelain #FDF5E6, warm beige #D4A574]
- Skin Texture: [e.g., smooth, oily T-zone, dry, combination]
- Freckles: [yes/no, location if yes]
- Moles: [yes/no, location and size if yes]
  - Example: "single dark mole on left temple, 2mm"
- Scars: [yes/no, location and description if yes]
- Tattoos: [yes/no, location and description if yes]
- Special Features: [e.g., birthmark on right shoulder blade]

## LAYER 4: HAIR
- Hair Length: [bald / buzzcut / very short / short / medium / long / very long]
- Hair Color: [e.g., black #1A0F0A, platinum blonde #F5E6D3]
- Hair Style: [e.g., side-swept bangs, middle part, slicked back]
- Hair Texture: [e.g., straight, wavy, curly, coily]
- Hair Details: [e.g., loose strands framing face, wispy bangs]
- Hair Accessories: [e.g., hairpin, headband, scrunchie]
- Facial Hair (if applicable): [none / stubble / beard / mustache]

## LAYER 5: CLOTHING (per scene)
### Scene A: [场景名]
- Top: [exact description, color, material]
- Bottom: [exact description, color, material]
- Full Body: [outfit overview]
- Outerwear: [jacket, coat, cardigan if applicable]
- Footwear: [shoes, boots, heels, color, style]
- Accessories:
  - Earrings: [type, material, color]
  - Necklace: [type, material, color]
  - Watch/Jewelry: [specific brand or style if notable]
  - Bag: [bag style and color]
  - Other: [glasses, scarf, belt, etc.]
- Color Hex Codes:
  - Blazer: #1B2838 (navy blue)
  - Blouse: #FFFFFF (white)
  - Heels: #0D0D0D (black)

### Scene B: [场景名]
[... same structure ...]

## LAYER 6: EXPRESSION PATTERNS
- Neutral Expression: [e.g., slight furrow between brows when at rest]
- Smile Type: [e.g., closed-lip smile, shows teeth, asymmetric]
- Common Facial Habit: [e.g., bites lower lip when nervous]
- Eye Contact Style: [e.g., direct, tends to look away when uncomfortable]
- Gesture Patterns: [e.g., touches necklace when anxious]
- Voice Quality: [e.g., low, melodic, husky, sharp]

## LAYER 7: DISTINGUISHING MARKS (Optional)
- Gait/Walk: [e.g., purposeful strides, slight limp, graceful]
- Posture: [e.g., straight-backed, slouches, military bearing]
- Movement Style: [e.g., fluid, sharp, economical]
```

---

## 💡 Token 编写实战示例

### 示例角色：LINDA（琳达）

```markdown
## LAYER 1: BASE_IDENTITY
- Name: Linda Chen
- Alias: "Lind"
- Gender: Female
- Apparent Age: 28-30
- Age Category: Young Adult

## LAYER 2: PHYSICAL FEATURES
- Face Shape: Oval, slightly heart-shaped
- Forehead: Medium width, no hairline recession
- Eyebrows: Arched, medium thickness, naturally groomed
- Eye Shape: Almond, slightly upturned outer corners
- Eye Size: Large
- Eye Color: Dark brown #3B2417
- Iris Detail: Warm flecks in light
- Nose Shape: Straight with slight upward tilt at tip
- Nose Bridge: High and defined
- Lips: Medium full, defined cupid's bow
- Lip Color: Dusty rose #C4908A
- Jawline: Soft with slightly pointed chin
- Cheekbones: High and defined

## LAYER 3: SKIN & MARKS
- Skin Tone: Fair with warm undertones #F5D0C5
- Skin Texture: Normal, dewy finish
- Freckles: None
- Moles: One small dark mole on left temple (2mm)
- Scars: None
- Special Features: Small beauty marks on neck (two, right side)

## LAYER 4: HAIR
- Hair Length: Long (waist length when down)
- Hair Color: Dark brown #2C1810 (near black in low light)
- Hair Style: Middle part, slight wave at ends
- Hair Texture: Straight to slightly wavy
- Hair Details: Face-framing layers, wispy at temples
- Hair Accessories: Minimal — sometimes thin gold hairpin

## LAYER 5: CLOTHING
### Scene A: Office
- Top: White silk blouse, high collar, mother-of-pearl buttons
- Bottom: Navy blue wool blazer, single-breasted, two buttons
- Footwear: Black pointed-toe pumps, 7cm heel
- Accessories:
  - Earrings: Pearl drop, white with pink overtone, 1.5cm
  - Watch: Minimalist gold dress watch, thin brown leather strap
  - Ring: Simple gold band on right ring finger
- Color Hex Codes:
  - Blazer: #1B2838
  - Blouse: #FFFFFF
  - Pumps: #0D0D0D
  - Pearl: #FDEEF4

### Scene B: Evening Event
- Top: Crimson red cocktail dress, off-shoulder, fitted waist
- Bottom: Same as above (dress is one-piece)
- Footwear: Black stiletto heels, strappy
- Accessories:
  - Earrings: Diamond drop earrings, 2cm, white gold setting
  - Clutch: Black satin envelope clutch, gold clasp
  - Necklace: None (neckline is statement)
- Color Hex Codes:
  - Dress: #C41E3A (crimson)
  - Stilettos: #0D0D0D

## LAYER 6: EXPRESSION PATTERNS
- Neutral Expression: Slight furrow between brows, composed
- Smile Type: Controlled, shows minimal teeth, asymmetric (left corner higher)
- Common Facial Habit: Touches pearl earring when thinking
- Eye Contact Style: Direct and steady, piercing when focused
- Gesture Patterns: Precise hand movements, minimal fidgeting
- Voice Quality: Low, measured, slight rasp on emphasis
```

---

## 🎬 Prompt 中使用 Token 的格式

### 标准格式

```markdown
[Character: LINDA, female, late 20s, oval face, high cheekbones, 
almond eyes #3B2417, full lips #C4908A, fair skin #F5D0C5, 
long dark brown hair #2C1810 middle part, wearing navy blazer #1B2838 
+ white silk blouse, pearl drop earrings, gold watch, black pumps]
```

### 带情绪叠加的格式

```markdown
[Character: LINDA, ... (base tokens) ...] + Emotion: 
[eyes narrowed, jaw set, expression of controlled anger, 
right hand touching pearl earring]
```

### 带 Negative Token 的格式

```markdown
[Character: LINDA, ...] + Negative: [different face shape, 
different eye color, different hair style, different clothing, 
deformed hands, extra fingers, blurry face, crossed eyes]
```

### 多角色场景格式

```markdown
[Character: LINDA, female, late 20s, ...]
[Character: MARCUS, male, early 30s, ...]
Scene: conference room, glass walls, modern office, late afternoon light
```

---

## ⚠️ 常见错误与修正

### 错误 1：Token 过于模糊

```markdown
# ❌ Bad
"young woman with brown hair and pretty eyes"

# ✅ Good
"female, late 20s, oval face, medium brown eyes #5C4033, 
chestnut brown hair #8B5A2B, wavy, shoulder-length"
```

### 错误 2：Token 在镜头间不一致

```markdown
# ❌ Bad（同一角色，镜头间描述矛盾）
Shot 1: "wearing navy blazer, white shirt, gold watch"
Shot 2: "wearing grey cardigan, blue jeans"  ← 服装突变！

# ✅ Good
Shot 1: "wearing navy blazer #1B2838, white silk blouse, 
pearl earrings, gold watch, black pumps" [Office scene]
Shot 2: "wearing red cocktail dress #C41E3A, diamond earrings, 
black stiletto heels" [Evening event - 这是场景转换，不是漂移]
```

### 错误 3：遗漏饰品

```markdown
# ❌ Bad
"wearing blazer, white shirt"

# ✅ Good
"wearing navy blue single-breasted blazer #1B2838, 
white silk blouse with mother-of-pearl buttons, pearl drop earrings, 
minimalist gold dress watch on left wrist, thin gold band on right ring finger"
```

### 错误 4：表情描述过于简略

```markdown
# ❌ Bad
"angry expression"

# ✅ Good
"expression of controlled anger, eyebrows drawn together and down, 
slight flare of nostrils, lips pressed into thin line, eyes hard and focused, 
jaw set, right hand clenched into fist on table"
```

---

## 🔄 Token 更新规则

### 何时更新 Token

| 情况 | Token 处理 |
|-----|----------|
| 镜头在**同一场景**连续拍摄 | Token 完全不变 |
| **场景跳转**（时间/地点变化） | 只更新 CLOTHING 层，其他层不变 |
| **角色换装**（戏份需要） | 建立新的服装 Token 集（outfit_A, outfit_B...） |
| **角色老化/化妆**（剧情需要） | 建立新的 Token 集（aged_token, makeup_token...） |
| 发现**漂移问题** | 回到 base/ 定妆照对照，修正 PHYSICAL 层描述 |

### Token 版本管理

```
tokens/
├── base_v1.0.txt      # 初始版本
├── base_v1.1.txt      # 微调版（加入 color hex）
├── outfit_B_v1.0.txt # 晚礼服场景 Token
└── aged_v1.0.txt     # 老化场景 Token（剧情需要时）
```

---

## 🎯 快速参考卡

```markdown
# ═══ LINDA — QUICK TOKEN CARD ═══
oval face | high cheekbones | almond eyes #3B2417 | full lips #C4908A
fair skin #F5D0C5 | mole left temple | beauty marks neck
dark brown hair #2C1810 | long | middle part | straight
OFFICE: navy blazer #1B2838 + white blouse + pearl earrings + gold watch
EVENING: crimson dress #C41E3A + diamond earrings + black stilettos
NEUTRAL: slight furrow | controlled asymmetric smile
EYES: direct, steady, piercing when focused
# ═══════════════════════════════════
```

> 打印此卡放在剪辑台旁边，每个镜头开始前快速对照。
