---
name: ecommerce-product-info-generator
description: 产品卖点基础信息生成器（国际化电商视频管线 Skill1）。接收产品图片和商品信息，自动识别产品类别、凝练结构化卖点、推断适用人群和场景，生成产品白底图（product_layer.png）和结构化卖点数据（selling_points.json）。当用户上传产品图片、要求"分析这个产品""提取卖点""生成产品信息"时触发。
version: 1.2.0
license: MIT
compatibility: opencode
metadata:
  category: e-commerce-video
  workflow: content-generation
  openclaw:
    requires:
      env:
        - AIGC_APP_KEY
        - AIGC_APP_SECRET
        - SUDOCODE_API_KEY
      bins:
        - python3
---

# 国际化电商视频生成 — Skill1：产品卖点基础信息生成

## 整体管线定位

```
                         AI爆款电商视频生成管线
   ═══════════════════════════════════════════════════════════

   整体输入:
     product_catalog  →  产品图册（白底图/主图/详情图/产品信息）
     target_country   →  目标国家（默认: 中国）
     target_platform  →  目标平台（非必填, 默认按市场推荐）
     video_type       →  视频类型（8选1）
     hook_points      →  吸睛点（非必填, 如"限时折扣3折/效果立竿见影"）
     duration         →  视频时长（秒）

                         │
                         ▼
   ┌─────────────────────────────────────────────────────────┐
   │  Skill 1: 基图生成器 (base-image-generator)              │
   │  输入: 整体输入参数                                       │
   │  输出:                                                   │
   │   · 凝练后的结构化卖点（多语言） —————→ 传给 Skill 2        │
    │   · 基图设计方案（两层图片+背景文本） ———→ 传给 Skill 2 + 3  │
   │   · 市场文化配置信息          —————→ 传给 Skill 2 + 3    │
   └─────────────────────┬───────────────────────────────────┘
                         │
                         ▼
   ┌─────────────────────────────────────────────────────────┐
   │  Skill 2: 分镜脚本生成器 (video-script-generator)         │
   │  输入: Skill1 输出 + 整体输入参数中的 duration/platform    │
   │  输出: 完整分镜脚本（含三元素引用标记） —→ 传给 Skill 3    │
   └─────────────────────┬───────────────────────────────────┘
                         │
                         ▼
   ┌─────────────────────────────────────────────────────────┐
   │  Skill 3: AI视频生成器 (ai-video-generator)              │
    │  输入: Skill1 的基图（两层图片+背景文本）+ Skill2 的分镜脚本│
   │  输出: 最终爆款AI视频（含质量检测报告）                    │
   └─────────────────────┬───────────────────────────────────┘
                         │
                         ▼
                   最终爆款AI视频 🎬
```

这是管线的 **Skill 1 — 入口层**。接收用户的原始产品和营销诉求，输出管线下游需要的结构化卖点和基图素材。

---

## 核心概念：一层基图 + 两层文本描述

本 Skill 只生成 **产品图**（`product_layer.png`），人物和背景均为 **文本描述**（不生成图片），
由下游 Skill3 在视频生成时根据文本描述自动渲染，并维护全片场景一致性：

```
输出文件：
───────────────────────────────────────────
① product_layer.png       ← 产品白底/多角度图（保留全部产品细节）
② background_layer        ← 背景环境描述文本（不生成图片）
③ people_layer            ← 人物描述文本（不生成图片）
```

**输出逻辑：** 仅产品层输出图片文件。背景层和人物层仅输出结构化文本描述，
由 Skill3 的 AI 视频模型根据描述自动渲染，并通过 prompt 约束保持全片场景一致。
这样既减少 API 调用次数，又让视频生成 AI 有更大的创作自由度来自适应不同镜头需求。

## 使用场景
本 Skill 是 **AI爆款电商视频管线** 的入口。当用户需要为电商产品制作面向特定国家/市场的爆款视频时触发。
用户提供产品图册和营销诉求，本 Skill 输出凝练后的结构化卖点 + 符合目标市场文化审美的基图设计方案（三层分解）+ 多语言文案 + 多平台版本，供下游 Skill2/3 消费。

## 输出目录规则

- **默认路径**：桌面 `AI视频脚本` 文件夹（自动创建）
- **自定义路径**：通过 `--output` 参数指定
- **聊天环境**：同时输出 Markdown 结果到聊天窗口 + 保存文件到输出目录

## 图片输入方式

本 Skill 支持三种图片输入方式：

### 方式一：ArkClaw/OpenClaw 聊天界面上传（推荐）
用户直接在聊天框拖拽或粘贴图片，系统自动处理：

**单张图片：**
```
用户: [上传产品图.jpg] "帮我分析这个产品，做泰国市场"
→ 系统提供临时路径: {image_path}
→ 执行: python {baseDir}/scripts/generate_base_image.py --product "{image_path}" --country "泰国" --video-type "痛点解决"
```

**多张图片：**
```
用户: [上传3张产品图] "分析这些图，做美妆护肤类"
→ 系统提供路径列表
→ 执行: python {baseDir}/scripts/generate_base_image.py --product "{image_path_1}" --detail-images "{image_path_2},{image_path_3}" --country "中国"
```

### 方式二：本地文件夹路径
```bash
python {baseDir}/scripts/generate_base_image.py --folder "./产品图片" --country "泰国"
```

### 方式三：单张图片路径
```bash
python {baseDir}/scripts/generate_base_image.py --product "./白底图.png" --name "产品名" --country "泰国"
```

> **路径变量说明：**
> - `{image_path}` — ArkClaw 自动注入的单张上传图片临时路径
> - `{image_paths}` — 多张上传图片的路径列表（逗号分隔）
> - `{baseDir}` — 本 Skill 所在目录的绝对路径
> - 默认输出到桌面 `AI视频脚本` 文件夹；可通过 `--output 自定义路径` 指定

---

## 品类维度（5大品类模板）

除 `video_type`（8种视频类型）外，产品所属 **品类** 是影响基图设计的重要维度。不同品类的展示重点和构图逻辑不同：

| 品类 | 产品展示重点 | 背景环境倾向 | 人物互动方式 | 三层输出特征 |
|------|------------|-------------|-------------|-------------|
| **美妆护肤** | 包装质感+质地+使用效果 | 浴室/化妆台/梳妆镜 | 手指涂抹/刷具上妆/脸部展示 | 层①产品多角度 + 层②浴室/梳妆台 + 层③手持产品/上妆姿态 |
| **食品零食** | 包装+内容物+食用状态 | 厨房/餐桌/户外野餐 | 手部取食/咀嚼/满足表情 | 层①包装+内容物 + 层②厨房/餐桌 + 层③手部取食姿态 |
| **家居日用** | 功能性+使用场景+收纳 | 客厅/卧室/厨房/卫生间 | 双手操作/场景化使用 | 层①产品功能特写 + 层②使用环境 + 层③双手操作姿态 |
| **服饰鞋包** | 上身效果+面料质感+搭配 | 衣帽间/街头/咖啡厅 | 全身穿着/转身/手拎展示 | 层①产品细节特写 + 层②搭配场景 + 层③全身穿着展示 |
| **数码3C** | 外观设计+屏幕显示+接口细节 | 桌面/科技背景/极简空间 | 手持操作/手指点击/摆放 | 层①产品主体70% + 层②极简背景 + 层③手持操作姿态 |

> **映射规则:** 若用户未填 `product_catalog.info.category`，AI 根据产品图片自动识别品类。品类决定背景场景倾向和人物互动方式，和 `video_type` 共同作为基图设计的两个维度。

---

## 整体管线输入参数（用户第一入口 — 简洁版）

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| `product_catalog` | object | 是 | — | **产品图册** — 包含图片和商品信息 |
| ├─ `images` | object | 是 | — | 产品图片集合 |
| │  ├─ `white_bg` | string | 否 | — | 白底图URL（最佳输入） |
| │  ├─ `main` | string | 否 | — | 主图URL（无白底图时用于抠图） |
| │  └─ `detail` | array | 否 | [] | 详情图URL列表（辅助产品识别） |
| ├─ `info` | object | 是 | — | 产品信息 |
| │  ├─ `name` | string | 是 | — | 产品名称 |
| │  ├─ `category` | string | 否 | 自动识别 | 产品类目 |
| │  ├─ `selling_points` | string | 否 | 自动提取 | 商品卖点（原始, 需凝练） |
| │  ├─ `target_audience` | string | 否 | 自动推断 | 目标人群 |
| │  ├─ `usage_scenario` | string | 否 | 自动推断 | 适用场景 |
| │  └─ `usage_instructions` | string | 否 | — | **产品使用说明**（可选，用户填写后严格参考，纳入卖点并传给Skill2） |
| └─ `price` | string/number | 否 | — | 福利价格, 如"39.9元"（含货币单位） |
| `target_country` | string | 否 | `"中国"` | **目标国家** — 精确国家名, 如"日本""泰国""美国" |
| `target_platform` | string | 否 | 按市场推荐 | **目标平台** — 如"抖音/TikTok/Instagram"等 |
| `video_type` | string | 是 | — | **视频类型** — 8选1: UGC种草/带货短剧/产品口播/产品演示/开箱种草/痛点解决/反应展示/TVC广告 |
| `hook_points` | string | 否 | 自动提取 | **吸睛点** — 用户期望的视频核心吸引力, 如"3折限时折扣""效果立竿见影""明星同款""限量发售"等 |
| `duration` | number | 是 | — | **视频时长**（秒） |

> 该统一输入将在此 Skill 内部展开为详细的执行参数（见下方"输入参数"表）。下游 Skill2/3 将继承此输入结构。

---

## 输入参数（展开版 — Skill1 内部使用）

> **映射自统一输入:** `product_catalog.images` → `product_layer` / `product_catalog.info` → `product_info` / `target_country` → `target_market` / `target_platform` → `platform` / `video_type` 直接继承 / `hook_points` → 注入卖点凝练和基图设计 / `duration` → 传给 Skill2

| 参数 | 类型 | 必填 | 说明 | 映射来源 |
|------|------|------|------|---------|
| product_layer | object | 是 | **① 产品白底图层** — 产品纯净形态 | `product_catalog.images` |
| ├─ white_bg | string | 否 | 白底图URL（最佳输入） | `images.white_bg` |
| ├─ main | string | 否 | 主图URL（无白底图时用于抠图） | `images.main` |
| └─ detail | array | 否 | 详情图URL列表（辅助产品识别） | `images.detail` |
| background_layer | object | 是 | **② 背景环境层** — 场景描述 | 由AI根据 `target_country` + `video_type` 自动生成 |
| ├─ scene_type | string | 是 | 场景类型（室内/户外/影棚） | AI推断 |
| ├─ style | string | 是 | 风格描述（如原木风/科技感/热带） | AI推断 |
| └─ reference_images | array | 否 | 场景参考图URL列表（可选） | 用户追加 |
| people_layer | object | 否 | **③ 人物层** — 人物设定 | 由AI根据 `target_country` 主流人种自动生成 |
| ├─ presence | string | 是 | 是否含人物（必须/可选/无人） | AI推断 |
| ├─ features | string | 是 | 人物特征（人种/年龄/妆容） | AI根据目标国家生成 |
| ├─ action | string | 是 | 动作姿态（手持/展示/使用） | 根据 `video_type` 匹配 |
| └─ reference_images | array | 否 | 人物参考图URL列表（可选） | 用户追加 |
| product_info | object | 是 | 商品信息 | `product_catalog.info` |
| ├─ name | string | 是 | 产品名称（中文或英文） | `info.name` |
| ├─ category | string | 否 | 产品类目（未填自动识别） | `info.category` 或 AI识别 |
| ├─ selling_points | string | 否 | 商品卖点（未填自动提取） | `info.selling_points` 或 AI提取 |
| ├─ target_audience | string | 否 | 目标人群 | `info.target_audience` 或 AI推断 |
| └─ usage_scenario | string | 否 | 适用场景 | `info.usage_scenario` 或 AI推断 |
| composition | object | 否 | 三层组合参数（各层独立的构图/角度/尺寸） | AI根据 `video_type` + `hook_points` 生成 |
| ├─ product_scale | string | 否 | 产品占比（大/中/小） | 按视频类型匹配 |
| ├─ background_blur | string | 否 | 背景虚化程度（无/轻/重） | 按市场审美生成 |
| └─ people_position | string | 否 | 人物位置（左/中/右/产品后） | 按构图模板生成 |
| video_type | string | 是 | 视频类型（8选1） | 直接继承 |
| hook_points | string | 否 | 吸睛点（注入卖点凝练和基图设计） | 直接继承 |
| target_market | string | 是 | 目标市场（由 `target_country` 自动映射） | `target_country` 映射 |
| platform | array | 是 | 目标平台（多选） | `target_platform` 或市场默认 |
| price | string/number | 否 | 福利价格（可选，需标注货币单位） | `product_catalog.price` |
| usage_instructions | string | 否 | **产品使用说明** — 用户填写的使用方式/场景说明。若有则严格参考，提炼后纳入 `selling_points.json` 的独立字段 `usage_instructions`，传递给 Skill2。 | 用户额外提供 |

> **注意:** `background_layer` 和 `people_layer` 由AI根据 `target_country` 和 `video_type` 自动推断生成, 无需用户手动填写。用户可以通过 `hook_points` 提示系统需要强调的吸引力方向。
>
> **额外说明字段:** `usage_instructions`（产品使用说明）为可选填字段。用户填写时必须严格参考其内容，提炼后写入 `selling_points.json` 的 `usage_instructions` 字段，供 Skill2 消费。Skill3 不涉及此字段。

## 目标市场定义与语言规则

### 市场层级与语言判定

```
IF target_market 精确到国家（如"美国""日本""德国"）:
  → 背景风格 = 该国具体文化元素
  → 语言文字 = 该国官方语言
  → 人物特征 = 该国主流人种特征
  → 审美偏好 = 该国主流审美

ELSE IF target_market 为区域（如"北美""欧洲""东南亚"）:
  → 背景风格 = 该区域通用文化元素
  → 语言文字 = 区域通用语言（见下表）
  → 人物特征 = 区域代表性人种
  → 审美偏好 = 区域主流审美

  区域语言规则：
  - 中国 → 中文汉语
  - 北美/欧洲/东南亚/巴西 → 英语英文
  - 日本 → 日语日文
  - 韩国 → 韩语韩文
```

### 七大市场文化适配规范

| 市场 | 精确国家示例 | 语言 | 人物特征 | 审美风格 | 色彩偏好 | 文化禁忌 |
|------|------------|------|---------|---------|---------|---------|
| **中国** | 中国/中国大陆 | 中文 | 东亚面孔 | 精致/白瘦幼/高级感 | 红金喜庆、莫兰迪高级 | 避免政治敏感、宗教 |
| **北美** | 美国/加拿大 | 英文 | 多元人种（白/黑/拉丁/亚裔） | 真实/多元/自信 | 高饱和、撞色、大胆 | 避免种族刻板印象 |
| **欧洲** | 英国/德国/法国/意大利 | 英文（通用） | 白人为主，南欧偏深 | 极简/质感/艺术感 | 低饱和、黑白灰、大地色 | 避免过度营销感 |
| **日本** | 日本 | 日文 | 东亚面孔，偏柔和 | 治愈/萌系/极简/细节控 | 马卡龙、原木白、低饱和粉 | 避免夸张表情、直接推销 |
| **韩国** | 韩国 | 韩文 | 东亚面孔，偏精致 | 时尚/水光肌/氛围感 | 奶油色、淡紫、薄荷绿 | 避免素颜感、要精致 |
| **东南亚** | 泰国/越南/印尼/菲律宾 | 英文（通用） | 东南亚面孔，偏健康肤色 | 热情/活力/家庭感 | 热带色、亮黄、亮绿、橙 | 避免宗教冲突元素 |
| **巴西** | 巴西 | 英文（通用） | 拉丁裔，偏健康肤色 | 热情/桑巴/活力/户外 | 高饱和、绿黄蓝（国旗色） | 避免刻板印象（足球/雨林） |

---

## 执行流程（严格按顺序执行）

### Step 1: 市场解析与语言判定

**1.1 解析 target_market**

```
输入格式识别：
- "中国" / "中国大陆" / "CN" → 中国市场，中文
- "美国" / "USA" / "United States" → 美国市场，英文
- "日本" / "Japan" / "JP" → 日本市场，日文
- "北美" / "North America" → 北美区域，英文
- "欧洲" / "Europe" → 欧洲区域，英文
- "东南亚" / "SEA" / "Southeast Asia" → 东南亚区域，英文
- "韩国" / "Korea" / "KR" → 韩国市场，韩文
- "巴西" / "Brazil" / "BR" → 巴西市场，英文
```

**1.2 输出市场配置**

```
market_config = {
  "market": "{解析后的市场}",
  "is_country": true/false,
  "language": "{语言代码}",
  "script_type": "{中文/英文/日文/韩文}",
  "people_features": "{人物特征描述}",
  "aesthetic": "{审美风格}",
  "color_preference": "{色彩偏好}",
  "cultural_taboos": ["{禁忌1}", "{禁忌2}"]
}
```

---

### Step 2: 产品识别与卖点凝练（多语言）

**2.1 图像分析**
- 分析主图：识别产品类别、外观特征、核心功能
- 分析详情图：提取使用场景、效果展示、成分/参数
- 分析白底图：获取产品纯净形态，用于抠图

**2.2 OCR文字提取**
- 从详情图中提取所有文字信息
- 识别：产品名、卖点词、成分表、功效宣称、价格信息

**2.3 卖点结构化（仅中文输出）**

> **注意：** 本阶段仅输出中文。多语言翻译（英/日/韩等）在 Skill3 的语音合成和字幕生成步骤完成。

统一输出中文格式：

```
1、商品名称：[中文产品名]
2、核心卖点：
主卖点：[最具差异化的1个核心卖点，不超过15字]
次卖点：
- [支撑主卖点的具体功效/成分/设计，3-5个]
3、适用人群：[精准描述，含年龄/性别/痛点/需求]
4、适用场景：[具体使用时机和场景，2-3个]
```

**凝练原则（各市场通用）：**
- 主卖点必须是用户最关心的、与竞品最差异化的点
- 次卖点必须能支撑主卖点，有具体数字/成分/证据
- 适用人群必须精准，拒绝"所有人"
- 适用场景必须具体，拒绝"日常使用"

---

### Step 3: 视频类型匹配与风格定位

根据 video_type 调用对应基图风格模板：

| 视频类型 | 基图核心识别特征 | 画面公式 | 情绪钩子 |
|---------|---------------|---------|---------|
| UGC种草 | 素颜真人+生活场景+手持产品 | [真人半身/大头]+[手持产品怼镜头]+[生活背景]+[手写体"真实测评"] | 真诚、朋友推荐感 |
| 带货短剧 | 多人剧情+场景叙事+动作定格 | [双人/多人场景]+[动作定格]+[场景纵深]+[剧名式标题] | 悬念、好奇、冲突 |
| 产品口播 | 专家半身+专业背景+直视镜头 | [人物半身]+[专业背景]+[直视镜头]+[权威头衔大字] | 信任、权威、专业 |
| 产品演示 | 产品主体60%+极简背景+侧逆光 | [产品主体60%+]+[极简背景]+[侧逆光轮廓]+[大字参数] | 高级、科技感、精致 |
| 开箱种草 | 半开包装+手部动作+桌面杂物 | [半开快递盒]+[手部动作]+[桌面杂物]+[期待感文字] | 期待、好奇、仪式感 |
| 痛点解决 | Before/After对比+明暗对比 | [痛点场景60%]+[产品小图]+[对比文字]+[左暗右亮] | 焦虑→希望、对比冲击 |
| 反应展示 | 惊讶表情特写+产品在手边 | [人物惊讶表情特写]+[产品在手边]+[感叹文字]+[抓拍感] | 惊喜、不可置信、真实 |
| TVC广告 | 电影场景+品牌融入+大量留白 | [电影感场景]+[产品自然融入]+[品牌slogan]+[大量留白] | 向往、高级、情感共鸣 |

**3.1 广告场景分类维度（新增）**

除 `video_type`（8种视频类型）外，根据产品属性+目标+hook_points 将广告分为5大场景，每个场景影响基图的整体风格定位：

| 广告场景 | 适用 video_type | 基图风格 | 视觉公式 |
|---------|----------------|---------|---------|
| **投流素材（效果广告）** | UGC种草/产品口播/痛点解决 | 高对比、大字价格、强CTR导向 | [产品70%]+[大字数字]+[对比色背景]+[紧迫感文字] |
| **种草产品** | 开箱种草/产品演示/反应展示 | 真实生活感、柔和、朋友推荐感 | [真人手持]+[生活场景]+[产品突出]+[真实口碑文字] |
| **品牌片/TVC** | TVC广告 | 电影级光影、留白、品牌符号突出 | [电影感构图]+[品牌色为主]+[大量留白]+[Slogan] |
| **互动内容** | 带货短剧/反应展示 | 剧情抓拍感、动态构图、评论引导 | [动作定格]+[悬念标题]+[竖屏]+[评论区引导文字] |
| **出海带货** | 全部类型（跨市场） | 多面孔、多语言、本地化元素 | [本地人种]+[本地场景]+[多语言标题]+[文化符号] |

> **映射规则**: `hook_points` 含"限时/折扣/促销" → 投流素材；含"品牌/质感/故事" → TVC；含"新品/真实/测评" → 种草；含"剧情/搞笑/反转" → 互动；`target_country` 非母语→出海。

**3.2 卖点演绎维度（视觉化方法论）**

基图设计不仅要展示产品，更要 **演绎卖点**。将文字卖点转化为视觉编码：

```
文字卖点 → 视觉演绎方案
─────────────────────────────────
"持久"       → 产品在时间推移中的状态不变（如妆容8小时不脱）
"轻薄"       → 质地滴落/延展/透光效果（如精华液从指缝滑落）
"强效"       → 视觉冲击/力量感（如泡沫爆炸/清洁力视觉化）
"天然"       → 自然元素环绕（植物/水滴/阳光穿透）
"精准"       → 精密细节/刻度/数字显示
"大容量"     → 产品与参照物对比（如与手掌对比展示尺寸）
```

基图的卖点演绎方向决定：
- 产品摆放角度（正视图展示容量 vs 侧视图展示轻薄）
- 背景互动方式（产品被自然元素环绕 vs 科技感光效）
- 人物互动方式（手部动作展示使用过程 vs 对比展示效果）

**3.3 黄金3秒开场策略（注入基图首帧设计）**

视频前3秒决定用户是否停留。基图的 **首帧画面** 需按以下策略强化吸引力：

```
黄金3秒开场策略 ← 从 hook_points（吸睛点） 自动匹配或用户指定：

① 视觉冲击法 — "第一眼就震撼"
   适用: 食品内容物/化妆品质地/产品特写
   基图：产品+汁液飞溅/质地滴落/爆炸图

② 悬念提问法 — "这是什么？"
   适用: 新品/陌生品类/功效型产品
   基图：产品遮罩/局部特写/不打全貌

③ 反差对比法 — "Before/After"
   适用: 功效证明类/清洁/护肤/收纳
   基图：左暗右亮/分屏对比

④ 利益承诺法 — "直接给答案"
   适用: 价格驱动/限时促销/痛点明确
   基图：产品+大字价格/效果数字

⑤ 情感共鸣法 — "你也有这个问题吗？"
   适用: 痛点型/生活方式型产品
   基图：人物+产品+场景情绪氛围
```

**匹配规则:**
- `hook_points` 含"折扣""限时""优惠" → ④利益承诺法
- `hook_points` 含"效果""对比""变化" → ③反差对比法
- `hook_points` 含"新品""首发""没见过" → ②悬念提问法
- `hook_points` 为空 → 根据 `video_type` 匹配默认策略

---

### Step 4: 市场文化适配构图设计 — 一层基图 + 两层文本描述

**4.1 独立输出布局**

输出为 **① product_layer.png（图片） + ② background_layer（文本） + ③ people_layer（文本）**。人物和背景均不生成图片，以结构化文本描述传递给下游 Skill3：

```
输出文件：
───────────────────────────────────────────
① product_layer.png        ← 产品白底/多角度图（唯一图片文件）
  尺寸：产品占画面60-80%，白底/透明底，保留全部细节
  角度：正面图为主，可选多角度（正/侧/俯/45°）

② background_layer（文本） ← 背景环境结构化描述（不生成图片）
  内容：场景类型 + 风格 + 色调 + 光影 + 风格预设
  由下游 Skill3 在视频生成时自动渲染，保证全片场景一致

③ people_layer（文本）     ← 人物描述文本（不生成图片）
  内容：人物特征 + 动作 + 表情 + 着妆风格
  由下游 Skill3 在视频生成时根据描述自动生成人物
```

**各层各自独立调节的参数：**

| 层级 | 控制参数 | 说明 |
|------|---------|------|
| ① product_layer.png | product_preservation_level, angle, scale | 产品保真度、展示角度、大小 |
| ② background_layer（文本） | scene_type, style, color_palette, lighting, style_preset | 场景风格、色调、光影、AI生成风格预设 |
| ③ people_layer（文本） | people_feature, action, expression | 人物特征、动作、表情 |

> **注意：** 仅产品层输出图片文件。人物层和背景层均为文本描述，由 Skill3 在视频生成时自动渲染 + 场景一致性约束。

**4.2 各市场人物/场景适配**

| 市场 | 人物特征 | 场景元素 | 表情风格 | 肢体语言 |
|------|---------|---------|---------|---------|
| 中国 | 东亚面孔，精致妆容/素颜感 | 现代都市/温馨家居/国风元素 | 含蓄微笑/真诚 | 含蓄，手势小 |
| 北美 | 多元人种，自然妆容/健康肤色 | 开放式厨房/loft/户外草坪 | 大笑/自信/夸张 | 开放，手势大 |
| 欧洲 | 白人为主，极简妆容/自然感 | 北欧风公寓/咖啡馆/艺术空间 | 淡然/知性/微笑 | 克制，优雅 |
| 日本 | 东亚面孔，柔和妆容/治愈感 | 和室/原木风/狭小精致空间 | 温柔/惊讶捂嘴/可爱 | 含蓄，小动作 |
| 韩国 | 东亚面孔，水光肌/精致妆容 | ins风房间/咖啡馆/街头 | 精致微笑/比心/可爱 | 时尚，流行手势 |
| 东南亚 | 东南亚面孔，健康肤色/活力 | 热带植物/彩色街道/家庭聚餐 | 大笑/热情/家庭感 | 热情，亲密 |
| 巴西 | 拉丁裔，健康肤色/活力 | 海滩/彩色建筑/户外派对 | 热情大笑/舞蹈感 | 极度开放，热情 |

**4.3 各平台安全区（按市场调整）**

| 平台 | 中国市场 | 海外市场（北美/欧洲/东南亚/巴西） | 日本市场 | 韩国市场 |
|------|---------|-------------------------------|---------|---------|
| 抖音/TikTok | 底部20% | 底部20% | 底部20% | 底部20% |
| 小红书 | 底部10% | - | - | - |
| Instagram Reels | - | 底部15% | 底部15% | 底部15% |
| YouTube Shorts | - | 底部15% | 底部15% | 底部15% |
| LINE VOOM | - | - | 底部15% | - |
| Kakao TV | - | - | - | 底部15% |

---

### Step 5: 市场配色方案

根据 **产品类别 + 视频类型 + 目标市场** 三维确定配色：

| 产品类别 | 中国市场 | 北美市场 | 日本市场 | 韩国市场 | 东南亚市场 | 欧洲市场 | 巴西市场 |
|---------|---------|---------|---------|---------|-----------|---------|---------|
| 美妆护肤 | 裸粉+玫瑰金+荧光粉 | 裸色+金棕+亮粉 | 樱花粉+白+薄荷绿 | 水光粉+淡紫+白 | 珊瑚粉+金+亮橙 | 裸粉+灰+玫瑰金 | 亮粉+金+绿 |
| 食品零食 | 暖黄+奶油白+荧光橙 | 橙红+白+牛仔蓝 | 原木+白+抹茶绿 | 奶油黄+淡粉+白 | 亮黄+绿+热带橙 | 大地色+白+橄榄绿 | 亮黄+绿+蓝 |
| 服装鞋包 | 高级灰+黑+品牌色 | 牛仔蓝+白+黑 | 黑+白+灰极简 | 奶油色+淡紫+白 | 亮黄+热带绿+白 | 黑白灰+驼色 | 亮绿+黄+蓝 |
| 家居家电 | 纯白+浅灰+薄荷绿 | 白+海军蓝+木色 | 白+原木+灰 | 白+灰+淡蓝 | 白+亮绿+木色 | 白+灰+黑极简 | 白+绿+黄 |
| 3C数码 | 黑+霓虹紫+电光蓝 | 黑+银+蓝 | 白+银+深蓝 | 黑+银+淡紫 | 黑+亮蓝+银 | 深空灰+银 | 黑+绿+蓝 |
| 母婴用品 | 奶白+淡粉+暖黄 | pastel彩虹+白 | 白+薄荷绿+淡黄 | 奶油白+淡粉+黄 | 亮黄+粉+绿 | 白+淡蓝+灰 | 亮黄+绿+蓝 |

**配色原则（各市场差异）：**
- 中国：喜庆红金可用，但高级感需莫兰迪
- 北美：大胆撞色，高饱和，多元包容色
- 日本：低饱和，原木白，治愈感，拒绝荧光
- 韩国：奶油色系，水光感，精致 pastel
- 东南亚：热带高饱和，明亮活力，绿黄橙
- 欧洲：极简黑白灰，大地色，艺术感
- 巴西：国旗色（绿黄蓝），桑巴活力，高饱和

---

### Step 6: 文案设计（仅中文）

> **注意：** 本阶段仅输出中文文案。多语言翻译（英/日/韩等）和价格格式转换在 Skill3 完成。

**6.1 标题文案公式**

| 视频类型 | 中文公式 |
|---------|---------|
| UGC种草 | [身份]+[时长]+[真实感受] |
| 带货短剧 | [冲突场景]+[悬念] |
| 产品口播 | [身份]+[揭秘]+[产品] |
| 产品演示 | [产品]+[核心参数] |
| 开箱种草 | [动作]+[期待] |
| 痛点解决 | [痛点]+[转折] |
| 反应展示 | [感叹]+[效果质疑] |
| TVC广告 | [品牌slogan] |

**6.2 中文价格标签设计（¥格式）**

```
原价：~~199~~（灰色删除线）
现价：¥89（红色大字）
标签：限时福利/今日专属
```

> 价格文案的货币单位转换和多语言翻译在 Skill3 按目标市场处理。

**6.3 CTA文案（中文）**

| 平台风格 | CTA文案 | 说明 |
|---------|---------|------|
| 紧迫型 | 点击左下角/戳链接/手慢无 | 抢购文化 |
| 邀请型 | 下方链接直达/赶紧去看看 | 温柔引导 |

---
---

### Step 8: 一层基图生成 + 两层文本描述

根据前7步输出的设计方案，采用 **一层基图生成 + 两层文本描述** 策略。
**仅产品层调用图生图**，人物层和背景层**均只输出结构化文本描述**（不调用图片 API），
由下游 Skill3 在视频生成时根据文本描述自动渲染人物和背景。

**8.1 生成策略**

| 输出 | 输入 | 模式 | 文件格式 | 说明 |
|------|------|------|---------|------|
| **product_layer.png** | 产品白底图 + 多角度描述 | 图生图(产品保真high) | PNG (透明底) | 唯一图片输出，去除原背景，保持产品高保真 |
| **background_layer（文本）** | 场景描述参数 | 文本输出 | base_layers.json | 场景类型+风格+色调+光影+风格预设，不生成图片 |
| **people_layer（文本）** | 人物描述参数 | 文本输出 | base_layers.json | 人物特征+动作+表情+着妆风格，不生成图片 |

**8.2 各层独立输出内容**

**层① — 产品白底图层（图生图）：**

```
endpoint: POST /jeecg-boot/openapi/call/generation/image/submit
headers: { X-Tenant-Id, appkey, signature, timestamp }
{
  "model": "{model_id}",
  "prompt": "产品白底图处理，{product_name}，{product_category}，
             纯净形态，保留全部产品细节，透明背景，无背景元素",
  "negative_prompt": "背景杂物、光影阴影、文字、水印",
  "image": "{white_bg图base64}",
  "image_resolution": "1080x1920",
  "n": 1,
  "size": "1080x1920",
  "response_format": "b64_json",
  "parameters": {
    "product_preservation_level": "high",
  }
}
```

**层② — 背景环境描述（文本，不调API）：**

```
# 背景不调用图片API，输出结构化文本描述给下游
background_layer = {
  "scene_type": "室内/客厅",
  "style": "tropical-vibrant",
  "lighting": "自然暖光",
  "color_palette": "白+亮绿+木色",
  "description": "电商产品展示背景，东南亚市场风格，热情活力审美，
                  白+亮绿+木色色调，客厅场景，自然暖光光影，
                  柔化背景，模糊景深，无产品，无人物，干净底板",
  "style_preset": "tropical-vibrant",
  "market": "southeast-asia",
}
```

**层③ — 人物描述（文本，不调API）：**

```
# 人物不调用图片API，输出结构化文本描述给下游
people_layer = {
  "features": "{market}人物特征，{age}，{makeup}",
  "action": "手持产品展示/使用产品",
  "expression": "{expression}",
  "description": "{people_features}，{action}姿态，{expression}表情，
                  {market}风格着妆，自然手势，半身构图",
}
```

**各市场style_preset推荐值（用于下游背景生成）：**
- 中国: "chinese-aesthetic"
- 北美: "north-american-real"
- 欧洲: "european-minimal"
- 日本: "japanese-healing"
- 韩国: "korean-glossy"
- 东南亚: "tropical-vibrant"
- 巴西: "brazilian-warm"

**8.3 输出文件与描述保存**

```
输出文件规格：
─────────────────────────────────────────
① product_layer.png
   格式：PNG（透明底，RGBA）
   内容：产品高保真主体，无背景、无人物
   用途：作为Skill3的 @product_ref 参考图输入

② background_layer（base_layers.json 内嵌）
   格式：结构化JSON字段（非图片文件）
   内容：场景类型 + 风格 + 色调 + 光影 + 文本描述 + 风格预设
   用途：作为Skill3的 @background_ref 文本参考，由AI自动渲染

③ people_layer（文本，base_layers.json 内嵌）
    格式：结构化JSON字段（非图片文件）
    内容：人物特征 + 动作 + 表情 + 着妆风格
    用途：作为Skill3的 @people_ref 文本参考，由AI自动生成人物
```

**8.4 各市场负面提示词附加项（人物层使用）**

| 市场 | market_specific_negative |
|------|------------------------|
| 中国 | 过度磨皮、网红脸 |
| 北美 | 单一肤色、刻板印象 |
| 日本 | 夸张表情、荧光色 |
| 韩国 | 素颜、粗糙皮肤 |
| 东南亚 | 冷淡、高级感过重 |
| 欧洲 | 花哨、繁杂元素 |
| 巴西 | 冷淡、过暗色调 |

**8.5 基图引用 ID（供 Skill3 多模态引用）**

```
@product_ref  → product_layer.png（产品白底图PNG，唯一图片）
@people_ref   → people_layer.description（人物文本描述，不生成图片）
                由 Skill3 根据描述自动生成人物 + 场景一致约束
@background_ref → background_layer.description（背景文本描述，不生成图片）
                  由 Skill3 根据描述自动生成背景 + 场景一致约束
```
---

### 输出格式（必须严格按此格式输出 — 供下游 Skill2/3 消费）

> **管线对接说明:** 本输出将直接传递给 Skill2（分镜脚本生成器）作为 `base_image_layers` 和 `refined_selling_points` 输入; 同时三层图片文件独立保存（不合成）, 供 Skill3（AI视频生成器）按需引用各层作为 `@图片` 参考。

```
═══════════════════════════════════════════════════════
        【{product_name}】{market}市场 基图设计方案
        视频类型：{video_type} | 语言：{language}
═══════════════════════════════════════════════════════

【一、市场配置】
目标市场：{market}
精确国家：{country_or_region}
语言：{language}
文字方向：{horizontal/vertical}（日文/韩文可能竖排）
人物特征：{people_features}
审美风格：{aesthetic}
色彩偏好：{color_preference}
文化禁忌：{cultural_taboos}

【二、凝练卖点（{language}）】
1、商品名称：{product_name_translated}
2、核心卖点：
主卖点：{main_selling_point_translated}
次卖点：
- {secondary_1_translated}
- {secondary_2_translated}
- {secondary_3_translated}
3、适用人群：{target_audience_translated}
4、适用场景：{usage_scenario_translated}

【三、类型匹配】
视频类型：{video_type}
基图风格：{style_description}
情绪钩子：{emotion_hook}

【四、构图设计】
布局：{layout_description}
主体位置：{product_position}，占比{percentage}%
标题位置：{title_position}
安全区：已避让{platform}底部{safe_zone}%

【五、配色方案】
主色：{main_color}（{color_meaning}）
辅色：{sub_color}
强调色：{accent_color}（用于{usage}）

【六、文案方案（{language}）】
主标题：{main_title_translated}
副标题：{sub_title_translated}
价格标签：{price_tag_translated}
CTA文案：{cta_translated}

【七、平台适配（{market}）】
{platform_1}版：
- 尺寸：{size}
- 安全区：顶部{top}%，底部{bottom}%
- 文字位置：{text_position}
- 特殊要求：{special}

{platform_2}版：
- 尺寸：{size}
- 安全区：顶部{top}%，底部{bottom}%
- 文字位置：{text_position}
- 特殊要求：{special}

【八、两层基图 + 背景文本描述方案】
**① product_layer.png**
□ 输入源：{product_white_bg_source}（产品白底图）
□ 处理模式：图生图，product_preservation_level=high
□ 多角度：{product_angles}（正/侧/俯/45°等）
□ 输出文件：`product_layer.png`（透明底PNG）
□ 引用ID：`@product_ref`（供Skill3使用）

**② background_layer（文本描述，不生成图片）**
□ 场景类型：{scene_type}
□ 生成模式：文本输出（不调API），{market}市场风格
□ 色调：{color_preference}，光影：{lighting_style}
□ 风格预设：{style_preset}（供下游AI渲染参考）
□ 输出：`base_layers.json` 内嵌描述字段
□ 引用：`@background_ref → description`（由Skill3根据文本自动生成背景）

**③ people_layer（文本）**
□ 人物特征：{people_features}，动作：{people_action}
□ 表情风格：{expression_style}
□ 生成模式：文本输出（不调API），{market}市场风格
□ 输出：`base_layers.json` 内嵌描述字段
□ 引用：`@people_ref → description`（由Skill3根据文本自动生成人物）

【九、文化合规检查】
□ 人物特征符合{market}主流审美
□ 场景元素无{cultural_taboos}
□ 色彩偏好符合{market}文化
□ 文案语气符合{market}沟通习惯
□ 价格货币单位正确
═══════════════════════════════════════════════════════
```

---

### 真实感红线（各市场通用+差异）

**通用：**
1. 拒绝过度修图：保留皮肤毛孔、包装褶皱、桌面杂物
2. 拒绝广告腔：文字用手写体/马克笔风格，非印刷体
3. 拒绝悬浮产品：产品必须有支撑/手持/摆放，非悬空
4. 拒绝均匀顶光：必须有明暗层次，侧逆光打出轮廓
5. 拒绝完美场景：背景有真实生活痕迹，非样板间

**各市场差异：**
- 中国：可适度精致，但拒绝过度网红脸
- 北美：必须多元包容，拒绝单一审美
- 日本：必须治愈自然，拒绝夸张推销感
- 韩国：必须精致时尚，拒绝素颜邋遢感
- 东南亚：必须热情活力，拒绝冷淡高级
- 欧洲：必须极简质感，拒绝花哨堆砌
- 巴西：必须热情奔放，拒绝冷淡克制

---

### ArkClaw 聊天界面输出格式

当通过 ArkClaw/OpenClaw 执行时，建议使用 `--output-format markdown` 参数，
脚本执行完成后会在终端输出结构化的 Markdown 结果，由聊天界面直接展示：

```
📦 **产品分析完成** — 【{product_name}】{market}市场

**【一、图片分析摘要】**
- 识别产品: {product_name}
- 推测品类: {category}
- 白底图: {已识别/使用原图}

**【二、凝练卖点】**
1. **商品名称**：{product_name}
2. **核心卖点**：
   - **主卖点**：{main_selling_point}
   - {次卖点列表}

**【三、基图设计方案】**
- 视频类型：{video_type}
- 目标市场：{market}
- 背景描述：{background_description}

**【四、输出文件】**
📁 输出目录: `{output_dir}`
   - product_layer.png — 产品透明底图
   - base_layers.json — 基图分层数据
   - selling_points.json — 结构化卖点

✅ **基图已生成**，可继续执行下游管线
```

---

## 模型与脚本引用

### API 认证

本管线统一使用 **aigc.hkttok.com JeecgBoot OpenAPI**。认证方式为 MD5 签名：

```
签名算法: MD5(appKey + appSecret + timestamp(13位毫秒)).hexdigest() 小写
```

请求头：
```http
X-Tenant-Id: 1000
appkey: {your_app_key}
signature: {computed_md5_signature}
timestamp: {current_timestamp_ms}
Content-Type: application/json
```

所有 API 通过 `/jeecg-boot/openapi/call/{path}` 网关转发。

### 脚本文件

| 脚本 | 路径 | 用途 |
|------|------|------|
| `jeecg_auth.py` | `scripts/jeecg_auth.py` | 共享签名认证工具（三个 Skill 共用） |
| `generate_base_image.py` | `scripts/generate_base_image.py` | 调用 aigc 图生图 API 生成基图图片 |

### 环境变量

| 变量 | 说明 | 默认值 |
|------|------|--------|
| `AIGC_API_BASE` | API 基础地址 | `https://aigc.hkttok.com` |
| `AIGC_APP_KEY` | 应用 Key（必填） | — |
| `AIGC_APP_SECRET` | 应用 Secret（必填） | — |
| `AIGC_TENANT_ID` | 租户 ID | `1000` |
| `AIGC_IMAGE_MODEL` | 图片生成模型 ID | `2049087333668446209`（Seedream 5.0 Lite） |

### 输入方式

**方式 A: 手动指定产品白底图（推荐当你知道哪张是白底图时）**
```bash
python scripts/generate_base_image.py \
  --product E:\产品图\白底图.png \
  --name "产品名" --country 泰国 --video-type "痛点解决" --output ./output
```

**方式 B: 传入图片文件夹（自动分析 + 提取产品信息）** ← 推荐
```bash
python scripts/generate_base_image.py \
  --folder E:\产品图文件夹 \
  --country 泰国 --video-type "痛点解决" --output ./output
```

### 自动图片分析能力

传入 `--folder` 时，脚本会自动执行完整的 OpenCV 视觉分析管线：

| 功能 | 方法 | 依赖 |
|------|------|------|
| **白底图识别** | 文件名匹配（`white*`/`白底*`/`product*`）+ OpenCV 像素级背景分析（白色/透明/场景/深色分类） | opencv-python |
| **图片分类** | OpenCV 评分系统：`_score_white_bg_cv2()` 计算白底可信度，`_score_detail_cv2()` 计算详情可信度，综合判定 white_bg/main/detail | opencv-python |
| **背景类型分析** | OpenCV 边缘区域采样 + 灰度均值/方差，自动识别 white/transparent/dark/scene 四种背景 | opencv-python |
| **边缘密度** | Canny 边缘检测，量化图片复杂度（低 → 白底图，高 → 详情图） | opencv-python |
| **轮廓分析** | OTSU 二值化 + findContours，统计物体轮廓数量 | opencv-python |
| **文字区域检测** | MSER 算法检测详情图中文字区域，辅助判定是否为详情图 | opencv-python |
| **主色调提取** | K-Means 聚类（k=5），提取前 5 种主色调及占比 | opencv-python + numpy |
| **产品名称提取** | OCR 识别详情图文字 → 取品牌/产品名 → 降级为文件夹名/文件名 | 需安装 pytesseract |
| **产品类别推断** | 将 OCR 文本匹配 5 大品类关键词（美妆护肤/食品零食/家居日用/服饰鞋包/数码3C） | 需 OCR 检出文字 |
| **卖点提取** | 从详情图文字中提取含 `%`/`倍`/`效`/功效词 的卖点语句 | 需 OCR 检出文字 |
| **分析报告** | 输出 `image_analysis.json`，含完整元数据、分类结果和可信度评分 | 始终执行 |

> **依赖安装：**
> ```bash
> pip install opencv-python numpy
> ```
> OCR 可选（如需自动提取产品名称/类别/卖点）：
> ```bash
> winget install TesseractOCR.Tesseract
> pip install pytesseract
> ```
> 未安装 OpenCV 时自动降级为 PIL 回退模式；未安装 pytesseract 时自动降级为文件名/文件夹名推测。识别结果以 `image_analysis.json` 中 `confidence` 字段标注可信度。

### 图片分析输出

每次运行会在输出目录生成 `image_analysis.json`，包含：

```json
{
  "product_name": "自动识别的产品名",
  "category": "美妆护肤/食品零食/...",
  "selling_points": "5%烟酰胺；28天提亮；敏感肌可用",
  "white_bg_image": "白底图路径",
  "detail_images": ["详情图1", "详情图2", "..."],
  "ocr_texts": ["从详情图提取的文字"],
  "confidence": 0.85
}
```

如果 `confidence < 0.6`，建议手动补充 `--name` 和 `--selling-points` 参数。

**使用方式：**
```bash
# 设置认证凭据（.env 文件或环境变量）
set AIGC_APP_KEY=your_app_key
set AIGC_APP_SECRET=your_app_secret

# ═══════════════════════════════════════════
# 【推荐】统一管线入口 — 从整体输入一键执行
# ═══════════════════════════════════════════
python scripts/generate_base_image.py \
  --folder E:\产品图文件夹 \             # 产品图片文件夹（自动识别白底图）
  --country "目标国家" \                # target_country（默认中国）
  --video-type "视频类型" \             # 视频类型（8选1）
  --hook-points "吸睛点" \             # 吸睛点（非必填）
  --duration 30 \                      # 视频时长（秒）
  --price "福利价格+货币单位" \          # 福利价格（非必填）
  --output ./output

# 或手动指定白底图和名称：
python scripts/generate_base_image.py \
  --product product_white.png \        # 产品白底图
  --name "产品名称" \                   # 产品名称
  --selling-points "原始卖点,分号分隔" \  # 原始卖点
  --country "目标国家" \
  --video-type "视频类型" \
  --hook-points "吸睛点" \
  --duration 30 \
  --price "福利价格+货币单位" \
  --output ./output

# ═══════════════════════════════════════════
# 【进阶】精细控制（背景描述自定义）
# ═══════════════════════════════════════════
python scripts/generate_base_image.py \
  --product product_white.png \
  --output ./output \
  --market "目标市场" \
  --aesthetic "审美风格" \             # 背景审美风格
  --color "色调描述" \                 # 背景色调
  --scene "场景描述" \                 # 场景
  --lighting "光影风格" \              # 光影

# ═══════════════════════════════════════════
# 完整管线示例（三个 Skill 串联）
# ═══════════════════════════════════════════
:: Skill1: 生成基图 + 卖点
python scripts/generate_base_image.py \
  --product product_white.png --name "产品名称" \
  --country "目标国家" --video-type "视频类型" --duration 30 \
  --hook-points "吸睛点" --price "福利价格+货币单位" --output ./output

:: Skill2: 生成分镜脚本（消费Skill1输出）
python ../video-script-generator/scripts/generate_storyboard.py \
  --config ./output/selling_points.json \
  --base-layers ./output/base_layers.json \
  --duration 30 --platform TikTok --output ./output

:: Skill3: 生成最终视频（消费Skill1+Skill2输出）
:: 人物和背景由 Skill3 根据 base_layers.json 中的描述自动生成
python ../ai-video-generator/scripts/generate_video.py \
  --script ./output/storyboard.json \
  --product ./output/product_layer.png \
  --base-layers ./output/base_layers.json \
  --market "目标市场" --output ./output

---
## 管线串联（重要 — AI 执行流程）

本 Skill 是国际化电商视频生成管线的 **第一环节**。执行完成后必须按以下流程操作：

### 执行完成后

1. **告知用户结果**：输出目录、生成文件列表、卖点摘要
2. **询问是否继续**：
   > "产品信息已生成，是否继续执行 Skill2（视频脚本生成）？"

### 如果用户选择继续 Skill2

将本 Skill 的输出作为 Skill2 的输入：

```bash
python {baseDir}/../ecommerce-video-script-generator/scripts/generate_storyboard.py \
  --product-img "{output_dir}/product_layer.png" \
  --config "{output_dir}/selling_points.json" \
  --video-type "{video_type}" \
  --category "{category}" \
  --market "{market}" \
  --duration {duration}
```

> 关键：`--config` 指向本技能输出的 `selling_points.json`（含 `usage_instructions` 字段），`--product-img` 指向 `product_layer.png`

### 上下游说明

| 方向 | 技能 | 仓库 |
|------|------|------|
| ⬆ 上游 | 无（本技能是入口） | — |
| ⬇ 下游 | `ecommerce-video-script-generator` | `https://github.com/BStory28/ecommerce-video-script-generator` |
