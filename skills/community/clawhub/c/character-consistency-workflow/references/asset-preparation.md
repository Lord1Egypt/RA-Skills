# Asset Preparation Guide（资产准备指南）

> 定妆照、表情参考、角度参考的完整拍摄与整理规范。

---

## 📋 概述

AI 生成角色一致性的根基在于 Reference Assets（参考资产）的质量。再好的 Token 系统，如果定妆照本身光线不一致、表情不标准，也会导致漂移。

**核心原则：**
- 同一天拍摄所有定妆照
- 固定光源、背景、妆容
- 建立清晰的文件夹命名规范

---

## 🎬 定妆照拍摄规范

### 最小要求：3 个基准角度

| 角度 | 用途 | 拍摄要求 |
|-----|------|---------|
| **正面照** | 主参考，锁定面部基准 | 纯色背景（推荐灰/白），正面机位，自然光或标准影视光 |
| **侧面照** | 侧脸特征锁定 | 同背景，光源与正面照一致，90° 侧脸 |
| **3/4 侧面照** | 中间角度过渡 | 同背景，光源与正面照一致，45°-60° 侧脸 |

### 推荐扩展：6 个角度（高质量工作流）

```
正面 → 正面偏左 15° → 正面偏右 15° → 侧面左 → 侧面右 → 背面
```

### 拍摄要求

**光线标准：**
- 推荐：3-point lighting（三点布光），主光在相机左侧 45°
- 避免：单一顶光（会在眼窝产生阴影）
- 一致性：所有角度使用完全相同的光源设置

**背景标准：**
- 纯色无纹理背景（灰色 #808080 或白色 #FFFFFF）
- 背景与角色之间保持 1.5m 以上距离（避免轮廓染色）

**服装标准：**
- 定妆照拍摄时穿正式出场服装（场景A主打服装）
- 如有多个主要造型，每个造型单独拍摄一套定妆照

**妆容标准：**
- 最终上镜妆容（避免淡妆导致 AI 自行"补全"浓妆）
- 眉色与发色协调

---

## 😊 表情参考 Sheet（Expression Sheet）

### 标准 8 表情组合

每个角色需要建立一套表情参考，建议排列在一张 2×4 或 4×2 的网格图中：

```
┌─────────┬─────────┬─────────┬─────────┐
│ Neutral │  Happy  │  Angry  │  Sad    │
│  平静   │  开心   │  愤怒   │  悲伤   │
├─────────┼─────────┼─────────┼─────────┤
│ Surprise│ Disgust │  Fear  │ Pensive │
│  惊讶   │  厌恶   │  恐惧   │  沉思   │
└─────────┴─────────┴─────────┴─────────┘
```

### 拍摄规范

- 表情之间间隔 3-5 秒（让表情完全松弛后再拍下一个）
- 眼睛直视镜头（用于 eye contact 参考）
- 嘴角、眉毛完全放松后再进入下一个表情
- 分辨率要求：至少 1024×1024px

### 情绪表情细化

| 情绪 | 关键面部特征 |
|-----|------------|
| **愤怒 (Angry)** | 眉毛内聚，眉心皱纹，嘴唇收紧，下颌突出 |
| **开心 (Happy)** | 眼轮匝肌收缩（卧蚕），嘴角上扬，露出上齿 |
| **悲伤 (Sad)** | 眉毛内角上抬，嘴角下垂，眼眶略红 |
| **惊讶 (Surprise)** | 眉毛抬高，瞪眼，嘴唇微张 |
| **恐惧 (Fear)** | 眉毛抬高并聚拢，眼睛睁大，嘴唇后拉 |
| **厌恶 (Disgust)** | 眉毛下沉，鼻子上皱，上唇抬高 |
| **沉思 (Pensive)** | 眼神向斜上看，轻微侧头，手指接触嘴唇 |

---

## 👔 服装细节特写（Costume Detail）

### 必须拍摄的细节

| 部位 | 说明 | 数量 |
|-----|------|-----|
| **领口** | 领型（圆领/V领/立领）、材质（蕾丝/棉/丝绸） | ×1 |
| **袖口** | 袖型（长袖/短袖/喇叭袖）、袖口处理 | ×1 |
| **腰部** | 腰带/收腰方式/腰线位置 | ×1 |
| **饰品** | 项链/耳环/手表的近距离特写 | ×2-3 |
| **面料** | 特殊面料（丝绸/皮革/针织）的纹理 | ×1 |
| **鞋子** | 完整鞋子 + 鞋面特写 | ×1 |

### 拍摄要求

- 使用微距或近摄模式
- 光线：与定妆照一致的光源方向
- 背景：可使用中性灰背景

---

## 📁 文件夹组织规范

### 完整目录结构

```
project/
└── characters/
    └── [character_name]/
        ├── meta.json              # 元数据（角色描述、年龄、性别）
        │
        ├── base/                  # 基准定妆照
        │   ├── ref_front.jpg      # 正面照（主参考）
        │   ├── ref_side_L.jpg     # 左侧侧面照
        │   ├── ref_side_R.jpg     # 右侧侧面照
        │   ├── ref_3quarter_L.jpg  # 左 3/4 侧面
        │   ├── ref_3quarter_R.jpg # 右 3/4 侧面
        │   └── ref_back.jpg       # 背面照（可选）
        │
        ├── expressions/           # 表情参考
        │   ├── neutral.jpg
        │   ├── happy.jpg
        │   ├── angry.jpg
        │   ├── sad.jpg
        │   ├── surprise.jpg
        │   ├── disgust.jpg
        │   ├── fear.jpg
        │   ├── pensive.jpg
        │   └── expression_sheet.jpg  # 合成网格图
        │
        ├── costume/               # 服装参考
        │   ├── outfit_A/          # 场景A服装
        │   │   ├── full.jpg       # 全身图
        │   │   ├── collar.jpg     # 领口特写
        │   │   ├── sleeve.jpg     # 袖口特写
        │   │   └── accessory.jpg  # 饰品特写
        │   └── outfit_B/          # 场景B服装
        │       └── ...
        │
        ├── lighting/              # 光线参考（可选）
        │   ├── main_light.jpg     # 主光参考
        │   └── rim_light.jpg      # 轮廓光参考
        │
        └── tokens/                # Token 笔记
            └── base_tokens.txt    # 该角色的基础 Token 描述
```

### meta.json 示例

```json
{
  "name": "LINDA",
  "chinese_name": "琳达",
  "age_appearance": "28-30",
  "gender": "female",
  "face_shape": "oval",
  "skin_tone": "#F5D0C5",
  "hair_color": "#2C1810",
  "hair_length": "long",
  "eye_color": "#4A3728",
  "build": "slim, 168cm",
  "personality_traits": "reserved, sharp-tongued",
  "distinguishing_marks": [
    "left temple small mole",
    "two beauty marks on neck"
  ],
  "wardrobes": {
    "outfit_A": {
      "name": "Office Look",
      "description": "Navy blue blazer, white silk blouse, pearl earrings, gold watch"
    },
    "outfit_B": {
      "name": "Evening Dress",
      "description": "Red cocktail dress, black stiletto heels, diamond earrings"
    }
  }
}
```

---

## ⚠️ 常见错误与避免方法

| 错误 | 后果 | 避免方法 |
|-----|------|---------|
| 不同天拍摄定妆照 | 光线色温不同，一致性下降 | 集中在同一天、同一个地点拍摄 |
| 背景有纹理 | AI 学习到背景纹理，导致穿帮 | 使用纯色无纹理背景 |
| 表情用力过猛 | 与实际生成的表情差距大 | 表情保持自然，只有关键肌肉动 |
| 饰品遗漏 | 镜头间饰品随机消失 | 在 Token 中列出所有饰品 |
| 服装不完整 | AI 自行补全导致换装 | 定妆照穿全套正式出场服装 |
| 分辨率过低 | 细节丢失，参考价值低 | 定妆照至少 1024×1024px |

---

## 🔗 与 Token 系统的衔接

完成 Asset Preparation 后，将关键信息填入 `consistency-tokens.md` 中的 Token 模板：

```
[Character: LINDA]
Face: oval, sharp chin
Skin: #F5D0C5, rosy cheeks
Hair: long, #2C1810, low ponytail
Eyes: #4A3728, almond shaped
Outfit A: navy blazer + white silk blouse + pearl earrings
Outfit B: red cocktail dress + diamond earrings
Reference: ./characters/LINDA/base/ref_front.jpg
```

> 资产质量 × Token 精确度 = 最终一致性
