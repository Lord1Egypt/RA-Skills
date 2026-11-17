---
name: cloud-palace-minimax-h3
description: '云上仙宫提示词生成器（双通道升级版）：①文生图——东方史诗感、巨物美学、空间压缩感的六维结构提示词；②视频——严格遵循 MiniMax H3 官方规范（T2VA/I2VA/FL2VA/L2VA/Ref2VA）生成电影级动态影像提示词。当用户要求云上仙宫、天宫、仙界、云端仙境风格的图片或视频提示词时触发。'
metadata:
  argument-hint: '[主题] [图|视频] [比例/动作/时长可选]'
---

# 云上仙宫提示词生成工程（图 + H3 视频 双通道）

本技能输出两类提示词。先判定通道，再执行对应管线；$ARGUMENTS 为用户输入（主题、图/视频、比例、动作、时长等）。

## 0. 通道判定与铁律

- **图像请求**（文生图 / "出图" / 要静态画面）→ 通道 A。
- **视频请求**（文生视频 / 图生视频 / "做成视频" / "动起来" / "生成短片"）→ 通道 B（H3）。
- 同时要求两者 → 先输出通道 A，再基于同主题输出通道 B。
- 铁律（两通道通用）：
  - **直接输出提示词本身，不附加任何解释、寒暄、前后缀**（失败处理中允许的一句假设/默认值说明除外）。
  - 画面中不得出现文字、logo、水印；除非用户明确要求某块可见文字，否则不创作任何 on-screen text。

---

## 通道 A：巨构美学文生图

### A1. 输入解析

| 模块 | 说明 | 示例 |
|:---|:---|:---|
| 主题 Theme | 必填，场景核心 | 观星台、炼丹炉、藏书阁、凌霄宝殿 |
| 画面比例 | 选填，默认 16:9 | 9:16、4:3、21:9 |
| 其他偏好 | 选填 | 天气、色调、人物动作、时间 |

### A2. 内置主题库（未命中时按同构风格自建，核心元素=东方建筑词汇+主题意象）

| 类别 | 主题（英文 / 核心元素 / 氛围） |
|:---|:---|
| 天宫体系 | 凌霄宝殿 Lingxiao Hall（帝座、玉阶、九龙盘柱）；南天门 Southern Heaven Gate（巨型拱门、天门守卫、云海阶梯）；天庭朝会 Heavenly Court Ceremony（众仙列队、祥云阵列）；蟠桃园 Peach Garden（千年蟠桃树、灵光闪烁） |
| 修道场所 | 练剑台 Sword Practice Platform（无栏杆悬台、剑痕刻石、孤峰）；炼丹炉 Elixir Furnace Tower（九转丹炉、灵火升腾、八卦阵法）；藏经阁 Celestial Archive Pavilion（浮空卷轴、玉简流光）；悟道崖 Enlightenment Cliff（临渊观星、星河倒挂）；听雨轩 Rain-Listening Pavilion（飞檐滴水、竹影婆娑） |
| 月宫系列 | 广寒宫 Palace of the Moon Goddess（冰晶玉砌、桂树、银辉铺地）；嫦娥舞袖 Chang'e's Silk Dance（飘带凌空、月华如水） |
| 龙宫系列 | 东海龙宫 Eastern Dragon Palace（珊瑚立柱、珍珠穹顶、水晶王座）；龙女戏珠 Dragon Maiden with Pearl |
| 仙山系列 | 蓬莱仙岛 Penglai Floating Isles（悬岛群、仙桥）；昆仑瑶池 Kunlun Jade Pool（西王母殿堂、凤凰降临）；泰山云海 Mount Tai Sea of Clouds（日观峰日出） |
| 特殊场景 | 天河渡船 Milky Way Ferry（星舟渡客、银河波光）；轮回镜台 Reincarnation Mirror（三生石、迷雾幻境）；封神台 Apotheosis Altar（金光洗礼、凡人飞升） |
| 园林仙境 | 仙鹤回廊 Crane-Flight Corridor；琴台听风 Zither Terrace；棋局观星 Star-Gazing Chess Pavilion |
| 战斗试炼 | 渡劫天梯 Tribulation Ascension Ladder（九霄雷云）；神魔战场 Divine-Demonic Battlefield（断壁残垣、灵气乱流） |
| 时序变化 | 晨曦 First Light at Dawn；黄昏 Dusk Afterglow；月夜 Silver Night；雪境 Snow-Clad Celestial Palace |
| 材质特效 | 琉璃宫殿（prismatic refraction）；白玉仙府（lustrous white jade）；朱砂神阙（imperial red）；青铜古刹（patinated bronze）；水晶幻境（crystalline illusion） |

光影氛围词库按需取用：Tyndall effect / volumetric lighting / rim lighting / god rays / atmospheric perspective；色调：platinum-white ethereal / cyan-blue cool tone / gold-and-purple divine / pale pink dusk。

### A3. 结构模板（六个模块必须全部出现，顺序固定）

```
[画面比例] --ar [比例]
[镜头] 长焦压缩 + 透视 + off-screen cutting
[场景] 史诗感东方建筑主体（主题元素 + 建筑词库）
[人物] 1-3% 画面占比的渺小人物（尺度标尺）
[光影] 冷暖对比 + 丁达尔效应 + 体积光
[氛围] 疏可走马留白 + 空灵缥缈
[技术] PBR/胶片质感 + 8K + film grain + negative space
```

### A4. 系统执行规则（硬性）

1. **比例响应**：用户指定比例（如 9:16）则严格执行；未指定则 `--ar 16:9`。
2. **巨物基准**：必须写"人物仅占画面 1%-3%"；建筑结构必须被画面裁剪（off-screen cutting / extending beyond the frame）体现无限延展。
3. **视觉语言库**：建筑描述至少含 3 项：dougong interlocking brackets（斗拱）、upturned eaves / sweeping roof corners（飞檐）、white jade marble（汉白玉）、vermilion lacquered wooden structure（朱红木构）、railing-less long bridge（无栏杆长桥）、floating courtyard（浮空庭院）、colored glaze tile roof（琉璃瓦顶）、surrounded by auspicious clouds（祥云环绕）。
4. **氛围基准**：必须保持"疏可走马"留白（massive negative space / wide breathing space）；禁止构图拥挤、元素堆砌。

### A5. 输出格式（严格，无解释）

```
[画面比例] --ar [比例]
[镜头] ...
[场景] ...
[人物] ...
[光影] ...
[氛围] ...
[技术] ...

【负面提示词】
low quality, blurry, watermark, text, signature, ugly, deformed, distorted, bad anatomy, poorly drawn, realistic photo, mundane, modern buildings, power lines, cars, contemporary elements, cluttered composition, overcrowded, flat lighting, low contrast

【参数建议】
尺寸：[比例] | 采样步数：30-40 | CFG Scale：7-9 | 模型：SDXL/Flux 推荐
```

### A6. 示例

输入：`练剑台，9:16比例，清晨，有仙鹤` → 输出：

```
[画面比例] --ar 9:16
[镜头] 35mm telephoto lens, extreme compression, cinematic low-angle shot, off-screen cutting
[场景] A vast ancient sword-practice platform floating above an endless sea of clouds. Massive vermilion lacquered pillars with intricate dragon carvings extend beyond the frame, railing-less white jade marble steps, upturned eaves disappearing into celestial mist, dougong interlocking brackets on every eave
[人物] A lone immortal cultivator (2% of frame) standing upright on a luminous flying sword, tiny and ethereal against the colossal architecture; a white crane gliding through the misty background
[光影] Misty morning, soft golden sunlight penetrating cloud gaps, strong cold-warm contrast between blue jade shadows and warm golden light on the eaves, Tyndall effect, volumetric god rays
[氛围] Serene, majestic, 疏可走马 vast negative space, quiet emptiness
[技术] PBR materials, epic Oriental fantasy concept art, hyper-detailed textures, 8K, cinematic film grain, masterpiece, best quality

【负面提示词】
low quality, blurry, watermark, text, signature, ugly, deformed, distorted, bad anatomy, poorly drawn, realistic photo, mundane, modern buildings, power lines, cars, contemporary elements, cluttered composition, overcrowded, flat lighting, low contrast

【参数建议】
尺寸：9:16 | 采样步数：30-40 | CFG Scale：7-9 | 模型：SDXL/Flux 推荐
```

---

## 通道 B：H3 电影级视频（MiniMax H3 官方规范）

本通道输出的视频提示词**必须**遵循 MiniMax H3 官方提示词规范：保留字段名、段落顺序、标签与时序记法原样；重写段落全部用英文；对白/歌词/场景可见文字保留原文；每个 shot 写清构图、主体、环境、动作、镜头运动、声音、参考内容出现的精确位置；禁止剧情摘要式空话、悬空 reference 标签、与时长不匹配的时序。

### B1. 模式判定

| 用户输入 | 模式 |
|:---|:---|
| 纯文字（主题 + 可选动作/时长） | T2VA |
| 给了首帧图（"基于这张图"） | I2VA |
| 给了首帧 + 尾帧 | FL2VA |
| 只给了尾帧 | L2VA |
| 完整参考素材（图/视频/音频混合，需定义 reference labels） | Ref2VA |

### B2. 对齐指令（首行，逐字保留；之后空一行再写核心字段）

- **T2VA**：无对齐指令，直接以 `integrated_multimodal_description:` 开头。
- **I2VA** 首行：
  `For the target video, at 0.00 seconds into the target video, <Picture 1> (from [Shot 1]) is fully referenced.`
- **FL2VA** 首行（S.SS=有效时长，精确两位小数）：
  `How the reference pictures align with the target video — Picture 1 (from Shot 1) aligns with the 0.00-second mark of the target video; Picture 2 (from Shot N) aligns with the S.SS-second mark of the target video.`
- **L2VA** 首行（N=最后一个 shot 的序号，图属于该 shot）：
  `How the reference pictures align with the target video — <Picture 1> (from [Shot N]) aligns with the S.SS-second mark of the target video.`

### B3. 基础模式字段顺序（固定）

```
integrated_multimodal_description: [Shot 1] ...

overall_soundscape: ...

non_diegetic_music: ...
```

- `integrated_multimodal_description`：沿时间线描述画面、动作、镜头、说话人、对白、diegetic 声音。`[Shot 1]` 开头先陈述整体风格与初始构图（本场景风格用 B4 基准），不加时间戳。
- 后续 shot：`[Shot 2] At MM:SS.mmm, the camera cuts to ...`，切点严格递增且落在视频时长内；普通剪辑用 `the camera cuts to / transitions to / changes to / switches to`，仅用户明确要求时才用 cross-dissolve/fade/wipe。
- `overall_soundscape`：1-4 句英文段落，概括全片环境声、物理动作声、非语言人声；对白/diegetic 声音不重复。用户明确要求全静才写 `N/A`。
- `non_diegetic_music`：1-3 句，只写乐器/速度/节奏/动态变化，禁止抽象情绪词；无音乐写 `N/A`。
- 默认单 shot；FL2VA 一般单镜头做首尾插值；L2VA 由合理前态逐步收敛到尾帧；用户明确要多镜头才分镜。

### B4. 云上仙宫风格基准（嵌入 `[Shot 1]` 风格与初始构图）

风格开句（可按主题微调建筑细节，句法与关键词保持不变）：

> Live-action, cinematic, 70mm IMAX film stock aesthetic with anamorphic lens and shallow depth of field. An extreme wide low-angle shot frames a colossal [主题] suspended above an endless sea of clouds: vermilion lacquered columns wrapped in dragon carvings extend beyond the frame, dougong interlocking brackets line every upturned eave, white jade marble terraces recede into the mist, and the upper structure vanishes into the celestial haze. A tiny figure (2% of the frame) stands [动作前状态].

贯穿每 shot 的氛围层：intricate volumetric fog, atmospheric depth layers, Tyndall light shafts through cloud gaps, realistic light reflection on architecture, raw organic film grain.

防伪收尾句：photorealistic, hyper-detailed environment, natural motion, looks like captured footage from a big-budget epic, zero AI-generated artifacts.

人物尺度规则：渺小人物（1-3% 画面）作标尺；建筑 off-screen cutting；留白优先，不堆元素。

### B5. 镜头语法（H3：运动类型 + 幅度 + 速度，写成自然英文动词句，不堆标签）

幅度仅 small / large（medium 省略）；速度仅 slow / fast（正常速度省略）。可用运动类型：Zoom In/Out、Push In/Pull Out、Pan Left/Right、Truck Left/Right、Tilt Up/Down、Pedestal Up/Down、Arc Shot、Tracking Shot、Static Shot、Shake Slightly/Strongly、POV、Roll Clockwise/Counterclockwise。

写法范例：
- `The camera pushes in with small amplitude at slow speed toward the central staircase.`
- `The camera pans right with large amplitude at fast speed, revealing the open doorway.`
- `The camera holds a static shot as the runner exits the frame.`

### B6. 动作 → 镜头映射表（用户指定动作时，动作逻辑强制绑定摄像机跟随）

| 用户意图 | 画面动作 | H3 镜头语法 |
|:---|:---|:---|
| 无动作（默认） | 静态宏大场景 | The camera pushes in with small amplitude at slow speed, capturing the grand scale of the palace (constant dolly, subtle organic handheld shake). |
| 原地起飞/上升 | The character initiates a natural, gravity-defying ascent into the clouds. | The camera tilts up and tracks the upward trajectory with small amplitude at slow speed, maintaining subject framing. |
| 人物转身 | The character turns around gracefully with fluid movement. | The camera executes an arc shot around the subject at medium speed, depth of field shifting dynamically. |
| 疾行/御剑 | The character moves forward rapidly on a flying sword with swift, controlled motion. | The camera tracks the subject at fast speed with subtle motion blur. |
| 环视/俯瞰 | The character gazes at the vast celestial scenery. | The camera tilts up / pedestals up with large amplitude at slow speed, revealing the majestic scale of the architecture. |

### B7. 对白与 speaker（默认不用）

云上仙宫场景默认无对白 → 不分配 `(S1)`、不出现 `<d>`。仅当用户给出台词：首次出场用视觉+声音信息建立身份并给稳定 ID，台词原样保留原文与标点 `<d>[语言] 原文</d>`；画外音必须用 `says in an off-screen voiceover` 且紧接说明嘴唇闭合；跨切点台词用 `<scenetrans>`，结尾截断用 `<cutoff>`。

### B8. Ref2VA 六段格式（全参考模式）

段落顺序固定：`subject_definitions` → `summary` → `retention_analysis` → `detailed_description` → `overall_soundscape` → `non_diegetic_music`。

- **labels**：`<Subject N>`（可复用可见内容：人物/场景/服装/特效/风格动作）、`<Picture N>`（作为具体帧锚点/构图锚点的图）、`<Video N>`（整片关系：剪辑源/续写源/结构参考）、`<Audio N>`（音频：复制/风格/音色/对白参考）。同一 label 全段含义一致；仅用于定义其他条目的图不单独成行，写进对应 `<Subject N>` 定义内。
- **summary**：一段短文，以方括号任务类型前缀开头（`[reference generation]` / `[keyframe completion]` / `[video editing]` / `[video continuation]` / `[audio reuse]` / `[audio reference]`，可 ` + ` 组合，不重复）。剪辑任务须以 `The target video is an edited version of <Video 1>.` 开头。只用已定义 label，不引入新 label。
- **retention_analysis**：每个 label 一行。视觉关系标记：`fully_preserved` / `partially_preserved` / `attribute_transfer` / `weak_reference`；音频标记：`fully_copy` / `partially_copy` / `reference` / `weak_reference`。格式如：`<Subject 1> (appears in [Shot 1], [Shot 3]): fully_preserved - ...`。
- **detailed_description**：风格在 `[Shot 1]` 前用 1-2 句英文建立；逐 shot 按播放顺序写；生成类任务正文 350-500 英文词；说话主体写作 `<Subject N> (Sx)`；帧锚点用自然句式（`the shot begins from <Picture 1>` / `the shot ends on <Picture 3>`）。
- 两个声音段落的定义同 B3；引用参考音频时按可听层归属（环境声→overall_soundscape，纯配乐→non_diegetic_music）。

### B9. 示例

**T2VA · 默认推轨**（输入：`凌霄宝殿，做成视频，6秒`）：

```
integrated_multimodal_description: [Shot 1] Live-action, cinematic, 70mm IMAX film stock aesthetic with anamorphic lens and shallow depth of field. An extreme wide low-angle shot frames a colossal Lingxiao Hall suspended above an endless sea of clouds: vermilion lacquered columns wrapped in dragon carvings extend beyond the frame, dougong interlocking brackets line every upturned eave, white jade marble terraces recede into the mist, and the hall's upper structure vanishes into the celestial haze. A tiny immortal figure (2% of the frame) stands motionless on the central staircase. The camera pushes in with small amplitude at slow speed, holding constant forward dolly movement with subtle organic handheld shake. Intricate volumetric fog drifts between the columns, Tyndall light shafts cut through the cloud gaps, and realistic light reflects off the glazed roof tiles. The look remains photorealistic and hyper-detailed, like captured footage from a big-budget epic, with zero AI-generated artifacts.

overall_soundscape: A high wind sweeps steadily across the open cloud terraces with the low hush of a vast sea of clouds beneath. Distant stone creaks and the soft whisper of silk robes drift in underneath.

non_diegetic_music: Sustained low strings at a slow tempo, joined by sparse piano tones and a gradual swell that eases toward the final second.
```

**T2VA · 起飞**（输入：`练剑台，角色原地起飞`）：

```
integrated_multimodal_description: [Shot 1] Live-action, cinematic, 70mm IMAX film stock aesthetic with anamorphic lens and shallow depth of field. An extreme wide low-angle shot frames a vast sword-practice platform floating above an endless sea of clouds, its railing-less edge and vermilion lacquered pillars extending beyond the frame. A lone cultivator in white robes (2% of the frame) at the platform's center initiates a natural, gravity-defying ascent, gracefully lifting off and soaring upward into the clouds as her robes trail behind. The camera tilts up and tracks the subject's upward trajectory with small amplitude at slow speed, maintaining her framing against the colossal architecture. Intricate volumetric fog, Tyndall light shafts through cloud gaps, and realistic light reflection on jade surfaces persist throughout. Photorealistic, hyper-detailed, zero AI-generated artifacts.

overall_soundscape: High wind sweeps the open platform while the sea of clouds hushes below. Silk fabric whistles softly as the figure ascends, with a low resonant stone hum underneath.

non_diegetic_music: Sustained low strings at a slow tempo with a gradually rising dynamic, punctuated by sparse piano notes near the top of the ascent.
```

**I2VA**（输入：基于某张云上仙宫图生成视频）：首行照抄 B2 的 I2VA 指令；`[Shot 1]` 以 `<Picture 1>` 的构图/人物/服装/空间关系为锚点（"the young woman shown in <Picture 1> remains..., preserving her appearance, clothing, and the scene layout"），按 B4 风格 + B6 默认推轨向前发展，人物与场景保持帧间一致。

---

## 失败处理

- 用户未给主题：追问一次；仍缺则用默认主题"凌霄宝殿"，并在提示词外仅用一句话注明所采用的默认值。
- 视频模式判不准（如只给了图未说明首帧/尾帧）：按 I2VA 处理，并在提示词前一句话注明假设。
- 用户要求的时长与动作节奏冲突（如 2 秒内多镜头切点超时长）：压缩为单 shot 并在提示词前一句话说明调整。
