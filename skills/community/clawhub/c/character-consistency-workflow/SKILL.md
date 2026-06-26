---
name: character-consistency-workflow
description: AI 短剧/短片创作中的角色一致性工作流。解决"人物漂移"（character drift）问题——多镜头生成时同一角色外观漂移、换脸、换装。触发关键词：角色一致性、人物漂移、换脸、定妆照、AI视频、多镜头、一致性Tokens、Seedance、Nano Banana。当需要保持角色跨镜头外观统一、防止AI生成时角色"变脸"时使用此技能。
---

# Character Consistency Workflow
# AI 短剧创作 · 角色一致性工作流

> 解决 AI 生成多镜头时"人物漂移"（Character Drift）的系统方法论。

---

## 🔍 问题诊断：什么是 Character Drift？

**Character Drift（人物漂移）** 是 AI 生成视频序列时，同一角色在不同镜头间的外观变化：

| 漂移类型 | 表现 | 严重程度 |
|---------|------|---------|
| **长相漂移** | 脸型、五官、发色在镜头间变化 | ⭐⭐⭐ 高 |
| **服装漂移** | 衣服颜色、款式、饰品不一致 | ⭐⭐ 中 |
| **表情漂移** | 情绪表情、眼神光变化 | ⭐⭐⭐ 高 |
| **肤色漂移** | 肤色明暗、冷暖色调跳变 | ⭐⭐ 中 |
| **年龄感漂移** | 面部年龄特征不稳定 | ⭐⭐ 中 |

### 三大一致性层级

```
Level 1: Appearance（长相一致性）
  └── 脸型、五官比例、肤色、发型的基准锁定
Level 2: Costume（服装一致性）
  └── 服装颜色、款式、饰品、道具的连续性
Level 3: Emotion（表情一致性）
  └── 情绪状态、眼神、面部肌肉走向
```

### 技术背景

- **Seedance 2.0** 三大核心突破之一：解决 Character Drift（漂移角色）
- **Nano Banana 2**：支持 5 角色 / 14 物体一致性
- 当前主流工具（LibLib、即梦等）均存在不同程度的漂移问题，需要系统性防漂移工作流

---

## 📦 第一阶段：Asset Preparation（资产准备）

### 定妆照拍摄规范

每个角色需要准备以下参考图（详见 `references/asset-preparation.md`）：

1. **正面定妆照** × 1
   - 纯色背景，正面机位，自然光
   - 完整上半身可见

2. **侧面/3/4 侧面照** × 2
   - 与正面照同天拍摄，光源一致
   - 服装、妆容完全相同

3. **表情参考 Sheet** × 1 组
   - 6-8 种基础情绪表情
   - 平静、开心、愤怒、悲伤、惊讶、沉思

4. **服装细节特写** × 3-5 张
   - 领口、袖口、饰品、面料纹理
   - 用于补全镜头细节

### 文件夹组织

```
characters/
├── protagonist/
│   ├── ref_front.jpg      # 正面定妆照
│   ├── ref_side.jpg       # 侧面照
│   ├── ref_3quarter.jpg   # 3/4侧面照
│   ├── expressions/
│   │   ├── neutral.jpg
│   │   ├── happy.jpg
│   │   ├── angry.jpg
│   │   └── ...
│   └── costume_detail/
│       ├── collar.jpg
│       └── accessory.jpg
└── antagonist/
    └── ...
```

---

## 🏷️ 第二阶段：Consistency Tokens（一致性 Tokens）

### Token System 概述

Consistency Tokens 是在每个 prompt 中重复使用的固定描述块，用于锁定角色特征。

**Token 公式：**

```
[BASE_IDENTITY] + [PHYSICAL] + [CLOTHING] + [HAIR] + [DISTINGUISHING_MARKS]
```

### 完整 Token 模板

```
Token: CHARACTER_A

BASE_IDENTITY:
- 姓名/角色名：[角色名]
- 年龄感：青年/中年/少年
- 性别外观：[描述]

PHYSICAL:
- 脸型：[如：鹅蛋脸，颧骨略高]
- 眉型：[如：剑眉，眉峰分明]
- 眼型：[如：杏眼，眼尾微翘]
- 鼻型：[如：直鼻，鼻梁挺拔]
- 唇型：[如：薄唇，唇角微扬]

SKIN:
- 肤色：[如：健康小麦色，质地细腻]
- 特殊：[如：左眼角一颗泪痣]

HAIR:
- 发长：[如：长发及腰]
- 发色：[如：深棕色]
- 发型：[如：中分，发尾微卷]

CLOTHING（按场景固定）:
- 场景A服装：[精确描述，包括颜色、款式、饰品]
- 场景B服装：[精确描述，包括颜色、款式、饰品]

EXPRESSION_PATTERN:
- 常用表情：[如：平静时眉心微蹙]
- 眼神特点：[如：目光沉稳，偶有闪躲]
```

### 多场景 Token 示例

```
# === SCENE 1 TOKENS ===
[Character: LINDA, female, 28, oval face, sharp chin, arched eyebrows, 
almond eyes, high nose bridge, thin lips, fair skin with rosy cheeks, 
long black hair in low ponytail, wearing navy blue blazer, white silk 
blouse, pearl earrings, minimal gold watch on left wrist]

# === SCENE 2 TOKENS (same character, different outfit) ===
[Character: LINDA, female, 28, oval face, sharp chin, arched eyebrows, 
almond eyes, high nose bridge, thin lips, fair skin with rosy cheeks, 
long black hair in low ponytail, wearing red cocktail dress, black stiletto 
heels, diamond drop earrings]
```

> 注意：长相描述（Physical）**不变**，只有服装描述（Clothing）随场景更新。

---

## 🎬 第三阶段：Cross-Shot Consistency（跨镜头一致性）

### Prompt 构建规则

**规则 1：每个 Prompt 包含完整 Token**

即使镜头只拍背影，Token 也必须完整存在，防止特征漂移。

**规则 2：Reference Image 路径写入 Prompt**

```
Style Reference: ./characters/protagonist/ref_front.jpg
Character Identity locked: [Token Block]
```

**规则 3：Negative Token（反向描述）**

```
Negative: [避免的特征，如：different face shape, different hair color, 
different clothing, extra limbs, deformed hands, blurry face]
```

**规则 4：镜头间的渐变规则**

| 镜头切换类型 | Token 处理 |
|------------|-----------|
| 同一场景内切 | 完全一致的 Token |
| 场景跳切 | 服装更新，Physical Token 不变 |
| 时间跳跃 | 重新确认所有 Token，生成前对照定妆照 |
| 情绪特写 | 在 Token 基础上叠加表情描述（emotion overlay） |

### 表情情绪叠加格式

```
# Base Token + Emotion Overlay
[Character: LINDA ...] + Emotion: eyes wide, pupils dilated, 
mouth slightly open, eyebrows raised, expression of shock
```

### 镜头序列示例

```
Shot 1: Medium Shot
[Character: LINDA ... wearing navy blazer...] + neutral expression
Prompt: Medium shot, LINDA standing in office, facing camera, 
natural lighting, cinematic

Shot 2: Close-up (same scene)
[Character: LINDA ... wearing navy blazer...] + slight frown, focused eyes
Prompt: Close-up, LINDA face, eyes looking at document, slight frown, 
cinematic lighting, shallow depth of field

Shot 3: Cutaway to hands
[Character: LINDA ... wearing navy blazer...] + (no face needed)
Prompt: Close-up, LINDA hands typing on keyboard, navy blazer sleeve visible, 
gold watch on wrist, cinematic lighting
```

---

## ✅ 第四阶段：Quality Check（质量检查）

### 一致性检查清单

生成完成后，按以下顺序检查：

```
□ 1. 长相一致性
  □ 脸型是否与定妆照一致？
  □ 眉毛形状、眼睛形状是否漂移？
  □ 发色、发长是否一致？

□ 2. 服装一致性
  □ 服装颜色是否一致？
  □ 饰品位置是否正确？
  □ 面料质感是否一致？

□ 3. 肤色一致性
  □ 肤色明暗是否跳变？
  □ 冷暖色调是否一致？

□ 4. 比例一致性
  □ 头身比是否稳定？
  □ 手部比例是否正常？

□ 5. 光影一致性
  □ 光源方向是否一致？
  □ 光影质感是否统一？
```

### 漂移问题修复对照表

| 问题 | 修复方案 |
|-----|---------|
| 脸型漂移 | 在 Token 中加入更精确的脸型描述，使用 Reference Image |
| 发色漂移 | 明确标注发色 hex 值，如：深棕色 #3B2417 |
| 服装颜色漂移 | 明确标注服装颜色，如：海军蓝 #1B2838 |
| 眼睛形状漂移 | 使用 expression sheet 中的眼部特写作为参考 |
| 手部畸形 | 加入 negative token: deformed hands, extra fingers |
| 饰品消失 | 在 Token 中详细列出所有饰品，加入场景描述 |

### 跨平台一致性策略

| 平台/模型 | 一致性能力 | 建议 |
|---------|----------|-----|
| Seedance 2.0 | ⭐⭐⭐⭐⭐ 最佳 | 主力使用，其 Character Drift 已被解决 |
| Nano Banana 2 | ⭐⭐⭐⭐ 强 | 支持 5 角色/14 物体，适合群戏 |
| LibLib/即梦 | ⭐⭐⭐ 中等 | 需要更严格的 Token + Reference |
| 其他模型 | ⭐⭐ 不稳定 | 建议用 Seedance 处理关键角色镜头 |

---

## 🛠️ 工具与集成

### Reference Image 使用方式

在 prompt 中引用本地文件路径：

```
# 使用本地路径
Reference: ./characters/protagonist/ref_front.jpg
Style Reference: ./characters/protagonist/ref_front.jpg

# 多个参考角度
Primary Ref: ./characters/protagonist/ref_front.jpg
Secondary Ref: ./characters/protagonist/ref_3quarter.jpg
```

### 推荐的 AI 工具

- **Seedance 2.0** — 目前 character consistency 最佳解决方案
- **Nano Banana 2** — 多角色/物体一致性
- **LibLib AI** — 参考图 + Token 组合使用
- **即梦** — 参考图锁定 + 负向描述

---

## 📁 相关文件

- `references/asset-preparation.md` — 定妆照拍摄规范与资产准备详解
- `references/consistency-tokens.md` — Consistency Tokens 完整模板与格式说明
