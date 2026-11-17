---
name: cosplay-photo-set
slug: cosplay-photo-set
displayName: 真人 cosplay 套图（ComfyUI 本地出图）
version: 2.1.0
summary: 两条入口（文字点名角色 / 上传一张二次元角色图）在「角色情报 → 角色卡」之后完全合并：先出真人基准图并由用户确认，再结合性格、身份设定与标志道具设计动作表情机位，出多张成片；角色卡含 SKIN 段锁全身肤色，成片再用 P7b 身体化妆统一腿脚肤色（加法曝光 + 局部偏色压缩 + 轮廓淡出 + 纹身保护，不磨皮、不出光晕），最后去油光、导出 1–2MB 竖版 JPEG 并附发布文案包。
license: MIT-0
tags:
  - comfyui
  - image-generation
  - cosplay
  - portrait
  - z-image-turbo
description: "通用模板：用本机 ComfyUI（z-image-turbo）把任意二次元角色做成「真人 cosplay 套图」，含腿脚肤色统一（SKIN 段 + P7b 身体化妆）。入口 A 用文字点名角色（检索官方设定与实拍），入口 B 直接上传一张二次元角色图（读图逐件拆解服装配饰，图是唯一设计依据）。两条入口都汇聚到同一张「角色卡」→ 1152 基准图 → 用户确认（硬闸门）→ 按角色性格/身份/元素力/道具设计 4–6 个「情境+表情+动作+手+机位+道具」镜头 → 1440 成片 → 质检返工 → 去油光 → 唯美纯色渐变影棚背景（按角色配色，无实景、无亮斑、无摄影灯）→ 导出 1–2MB 竖版 JPEG → 附标题、正文、标签。适用于任何角色与平台（视频号/小红书/抖音/公众号/图集）。"
---

# 真人 cosplay 套图流水线 v2（通用模板 · ComfyUI / z-image-turbo）

## 总览：一条主线，两个入口，两个确认闸门

```
P0 入口判定
   ├─ A 文字点名角色 ─┐
   ├─ B 上传角色图  ─┼─→ P1 角色情报（取证方式不同，产物相同）
   └─ C 都没有 → 热门提案 → 用户选定 → 回到 A
                              ↓
                        P2 角色卡（九段固定句）
                              ↓
                        P3 基准图（1152×2048，1–2 张候选）
                              ↓
                        ★ G1 用户确认基准图（硬闸门）
                              ↓
                        P4 表演脚本（4–6 镜，性格/设定/道具驱动）
                              ↓
                        ★ G2 用户确认脚本（文字，一行一镜）
                              ↓
                        P5 成片（1440×2560，只换 POSE 行）
                              ↓
                        P6 质检与返工 → P7 去油光 → P8 导出 → P9 交付（含文案包）
```

**三条硬规则（全流程只在这三处说，别在别处再改口径）**

1. **基准图未经用户确认，不得生成任何成片。** 用户上传图也一视同仁。
2. **成片只换 `POSE:` 行**；OPENING / BACKDROP / AGE / HEAD AND HAIR / FACE / COSTUME / HANDS / LIGHTING 逐字复用基准卡。
3. **两条入口在 P2 之后完全合并**：A/B 只影响 P1 怎么取证，不影响后面任何一步。

---

## P0 入口判定（先判断走哪条）

| 入口 | 触发 | 走法 |
|---|---|---|
| **A 点名角色** | 「做长离」「做芙莉莲」 | P1-A：检索官方设定与实拍，交叉验证 |
| **B 上传角色图** | 立绘、动画截图、官方渲染、同人图，说"做成真人" | P1-B：读图拆特征 + 补检索性格设定 |
| **C 无信息** | 只说"做个 cosplay 套图" | 先出 2–3 个近年热门候选，用户选定后按 A 走 |

**通用参数（缺哪条补哪条，别替用户决定）**

- **服装/皮肤**：角色有多套造型时问一句；不回答就取辨识度最高的一套并说明。
- **张数**：默认 4，可 5–6。**比例**：默认 9:16 竖屏。**平台**：视频号/小红书/抖音/公众号/图集。
- **文件大小**：默认 1–2MB。**分辨率**：默认 1440×2560。
- **年龄**：一律 18 岁左右（见「附 C·年龄」）。原作是神明/精灵/千年老妖也不改。
- **背景**：固定「纯色/渐变无缝纸影棚」，按角色标志色配色。**不提供实景方案**——实景偏差大、易显假；用户坚持要实景时说明代价，默认仍走纯色。
- **道具**：默认 1–2 张带标志性小道具，不是每张都拿。

---

## P1 角色情报（A/B 都要做，取证方式不同，产物相同）

### P1-A 点名角色

1. 检索官方立绘/角色页/真人 cos 实拍，**至少两个独立来源交叉**；只看到文字描述时，交付里注明"按官方文字还原"并邀请用户发参考图。
2. 同时收集：**性格**（2–3 个词）、**身份/职业**、**元素力/能力/武器**、**口头禅或名台词**、**剧情关系与近期新皮肤/新剧情**。
3. 参考图存进项目 `refs\`，命名 `角色_类型_序号.jpg`，后面每一版都对着看。

### P1-B 上传角色图

1. **这张图是唯一设计依据**：图中出现的元素优先于任何文字资料。同人图/二创会改设计 → 交付时说明「按你给的这张图还原」。
2. **逐项填特征表**（看不出的写「图中不可见」，不要猜）：

| 项 | 写到什么粒度 |
|---|---|
| 发色/挑染 | 主色 + 挑染位置与宽度 + 渐变方向（"只有发梢最后十几厘米染紫"级） |
| 发型 | 长度、层次、刘海形状（是否遮眼）、束发/编发、呆毛 |
| 发饰 | 形状、材质、位置、数量（左右是否对称） |
| 瞳色 | 具体色相；是否异色瞳；哪只眼被遮 |
| 上装 | 款式、领型、袖型、长度、主色 |
| 胸/腰结构 | 绑带走向、纽扣、腰带、挂饰 |
| 手部 | 手套长度与颜色、臂环、指甲 |
| 下装 | 裙/裤长度、开衩、内衬颜色、前短后长 |
| 腿部 | 袜长、袜色、纹样、肤色/纹身/符文 |
| 鞋 | 款式、跟高、绑带 |
| 外层 | 披风/外套/飘带，正反两色 |
| 纹样/徽记 | 位置与图形 |
| 标志色 | 2 个（浅/深，用于背景渐变） |
| 道具 | 是否必需、大小、是否单手可持 |
| 性格（从表情姿态读） | 2–3 个词 |

3. **同名角色可以也应该检索**——但只用来补三件事：**性格、身份设定、标志道具/能力、名台词与剧情**。**不要用检索结果去改图里已有的设计**（发色、服装、配饰一律以图为准）。
4. 图中没拍到的部件（常见是下装、袜、鞋、背面）按官方设定补，交付时逐件标注「参考图未给，按官方设定补」。
5. 强特征要单独记：**单眼被刘海遮住、异色瞳、兽耳/角、面部纹样、手套**——这些在文生图里最容易漂，必须在基准图和每张成片逐张核验。

### P1 产物：角色情报卡（后续所有步骤都从这张卡取信息）

```
角色 / 作品 / 性别 / 18 岁外貌
性格三词：
身份与职业：
元素力 / 能力 / 武器：
标志动作（看名字就能想到的动作）：
标志道具（1–2 件，能单手拿的小物）：
标志色（浅 / 深）：
强特征（遮眼、异色瞳、纹样、发饰左右对称…）：
她此刻在想什么（一句情境，P4 用）：
```

### 资料冲突时的裁决顺序（避免两份资料打架）

**图中元素 ＞ 官方立绘/实拍 ＞ 官方文字设定 ＞ 攻略站/维基 ＞ 你的记忆**
性格与设定类信息，以「多个来源一致」为准；只有一个来源时，标注"待确认"。

---

## P2 角色卡（九段固定句，之后逐字复用）

用**英文**写（中文容易在额头生成深色斑块），固定分节，只留 `POSE:` 一处占位：

```
Photorealistic live-action cosplay photograph of a real 18-year-old East Asian {{GENDER_WORD}} cosplaying {{CHARACTER}} from {{SERIES}}, {{FRAMING_SENTENCE}}

BACKDROP: {{BACKDROP_SENTENCE}}

AGE: eighteen years old, young adult, fresh youthful face, adolescent-to-young-adult proportions, no mature adult styling, no heavy grown-up makeup.

HEAD AND HAIR: {{HAIR_STYLE_AND_COLOR}}, {{BANGS_RULE}}, {{EYE_COVER_RULE}}, the forehead kept smooth and clear, no dark patches, no markings. {{BRAID_RULE}} The crown smooth and flat against the head, the hair hanging down in clean smooth locks close to the body, built from very fine thin individual strands, softly separated with soft light between them, matte with no plastic sheen, no greasy clumps, no wet-look shine.

FACE: young East Asian bone structure of an eighteen-year-old, {{FACE}}, {{EYE_COLOR}} eyes of natural size (not oversized, not doll eyes), thin natural eyeliner, soft coral lips. Realistic skin with visible fine pores, one clean natural warm skin tone, dry powder-matte finish on the face, shoulders, arms and back, skin looks freshly powdered like a real cosplayer at a shoot. No beauty retouching, no airbrushing.

SKIN: one even warm light beige skin tone with a soft peach undertone from her face all the way down to her feet, the neck, shoulders, arms, thighs, knees, shins, ankles and the tops of her feet all the same healthy tone, softly powdered and evenly toned like a sheer body foundation, gentle natural shading kept along the calves and knees, smooth clear skin with fine real texture, the legs warm and softly lit, the same tone as her face, like a cosplayer who has applied body makeup before the shoot.

COSTUME: {{COSTUME_ITEM_BY_ITEM}}

POSE: {{POSE}}

HANDS: exactly five fingers on each hand, fingers clearly separated, natural knuckles, no extra or fused fingers.

LIGHTING AND CAMERA: soft key light from camera left slightly above eye level, soft fill from the right, gentle falloff, even exposure with natural skin tone, highlights are soft and controlled. Sony A7R IV, 85mm f/1.8, ISO 800, shallow depth of field, fine film grain. The face and eyes are tack-sharp and in critical focus, no motion blur on the subject, the backdrop stays a smooth even gradient top to bottom. Ultra photorealistic, looks like a real person photographed at a cosplay shoot, not anime, not illustration, not 3D render, no plastic waxy skin. Vertical 9:16 composition.
```

**写卡规则**

- `{{FRAMING_SENTENCE}}` 全身固定用这一句（实测只有它能保证脚不被裁）：
  `full-length portrait on a clean seamless paper backdrop, framed from a distance of a few steps so the whole figure fits inside the frame, the body occupying about two thirds of the frame height, with a generous strip of empty backdrop above her head and a wide strip of empty floor below her shoes.`
- `{{BANGS_RULE}}`：有刘海 → `fine feathery bangs lifted slightly off the forehead`；无刘海 → `center-parted and swept back off the face`。
- `{{EYE_COVER_RULE}}`：**角色有一只眼被遮住时必写**，例：`a long soft fringe swept low across her right brow and falling straight over her right eye, that one eye hidden behind the fringe, the rest of her face clear and her left eye open.`；不遮眼就整句留空。
- `{{BRAID_RULE}}`：有细辫 → `one slim braid falling in front of her right shoulder.`；没有就留空（空着比写 `no braid` 安全）。
- `SKIN` 段（腿脚肤色的治本项）：默认整段复用上面模板，只按角色改 `warm light beige` 的冷暖（冷白皮 → `cool fair porcelain`，小麦色 → `warm honey beige`）。**"从脸到脚同一色调"和"body makeup/body foundation"这两句不要删**——实测它们是腿脚不再偏暗、发灰、长褐斑的关键。不要写 `no dark patches on the legs`、`no grey shadow` 这类负向句，会被当成正向画出来。
- `{{COSTUME_ITEM_BY_ITEM}}`：逐件写，颜色用叠词锁死（`dark navy almost black`）；先写整体轮廓（`a short flared white mini skirt` + `a long dark navy panel falling to her ankles behind`），再写层次与配饰。**白色上衣＋白裙会被模型合并成一件长上衣**（实测），必要时用"两段式"写法：先定裙长与后摆，再补胸衣结构。
- 背景句**只有一句**，全流程逐字不变：

```
BACKDROP: a flat seamless paper backdrop with an extremely smooth vertical gradient from {{COLOR_A}} at the top to {{COLOR_B}} at the bottom, colors taken from the character's signature palette, perfectly smooth, evenly lit and completely empty, the shot contains only the person against the empty backdrop.
```

  配色按角色标志色取一浅一深（甘雨 pale ice blue / soft periwinkle；胡桃 warm ivory / muted terracotta；雷电将军 pale lilac / deep indigo violet；芙宁娜 pearl white / pale aqua…）。
  **背景句与灯光句里禁止出现**：`softbox`、`light stand`、`strobe`、`reflector`、`wide`、`wide-angle`、`studio`、`spotlight`、`vignette`、`no blown highlights`、`灯架`、`柔光箱`、`反光板`。负向词会被当成正向画进画面（实测：写了 `no softbox` 真的画出柔光箱）；要高光收敛就正面写 `highlights are soft and controlled`。

---

## P3 基准图（1152×2048，1–2 张候选）

- 尺寸用 **1152×2048**（约 75s/张）；成片才上 1440×2560（约 230s/张）。
- 一次出 **1–2 张同卡不同种子**的候选，让用户挑脸/发型/服装形态；差别只在种子，卡一个字都不改。
- 基准图只验证六件事：**脸、年龄感、发型与遮眼、服装形态、背景配色、构图（脚有没有被裁）**。
- **必须把图发给用户**，并附一句话说明这版相对参考图改了/没改什么。

### ★ G1 基准图确认（硬闸门）

- **用户没确认，不许出任何成片。** 包括"我先把图跑起来"这种自以为是的并行。
- 用户说「用 V11 版」「就这张」= 确认；只说"再调一下"= 未确认。
- **反馈分两类处理**，别乱动整张卡：
  - **设计错了**（服装/发色/配饰/遮眼方式不对）→ 回 P1 改特征表，再改卡里对应那句。
  - **画技错了**（手指糊、发丝成绺、油光、裁脚）→ 只改质感/手势/构图那一句，别动 FACE、COSTUME。
- **改卡之后必须重出基准图并再次确认**；不许在成片批次里偷偷改卡（改一个字脸就换人）。
- 确认清单（逐条问用户，或自己先对一遍）：①脸像不像 ②18 岁左右吗 ③发型/发色/遮眼对不对 ④服装逐件对不对 ⑤背景配色对不对 ⑥脚完整、头顶有留白吗 ⑦整体像不像这个角色。

---

## P4 表演脚本（本 skill 的核心：不是摆姿势，是让角色演一段）

### 4.1 四源设计法（每个镜头都从这四个来源里长出来）

| 来源 | 拿它定什么 | 例子 |
|---|---|---|
| **性格三词** | 表情基调、眼神方向 | 清冷 → 垂眼/视线越过镜头；元气 → 露齿笑、眼睛发亮 |
| **身份与设定** | 她此刻在做什么（情境） | 神社巫女 → 刚收工、握着扫帚回头；将军 → 检阅时停步 |
| **元素力/武器/职业** | 标志动作 | 水元素 → 掌心托一颗水珠；剑士 → 手按刀镡 |
| **标志道具** | 1–2 张拿小物，其余空手 | 折扇、提灯、书、酒杯、护符 |

**每个镜头写六项**：`情境一句话 / 表情 / 动作 / 手 / 机位 / 道具`。缺一项就会退化成"摆姿势"。

### 4.2 镜头类型必须覆盖（4 张最低配，5–6 张更好）

- **A 情绪特写向**：看镜头，情绪最明确（笑/冷/挑衅/委屈），半身或 3/4。
- **B 氛围不看镜头**：视线离开镜头，垂眼、侧脸、背影回望，靠光和静止说话。
- **C 动态抓拍**：走、转身、甩发、跳、拔刀，裙摆/披风/长发带起来。
- **D 标志动作 + 道具**：一眼就认得是她的动作（托水珠、持杖、结印、举杯）。
- **E 极端机位**：低机位仰拍 / 高机位俯拍，打破"四张都平视全身"。
- **F 坐/蹲/卧**：坐台阶、蹲坐抱膝、侧卧，打破"四张都站着"。

**差异化检查（开跑前对一遍，四条都要满足）**：表情不重样 / 至少一张不看镜头 / 机位至少两种 / 手不在同一个位置。

### 4.3 反面清单（出现任意一条就重写脚本）

- 四张都是「回眸 / 半蹲 / 正面 / 走姿」——这是最低配，按性格重写。
- 四张都站直、都看镜头、都空手、都同一个笑。
- 表情与性格打架（高冷角色傻笑、元气角色面瘫）。
- 动作与该角色的身份无关（巫女拿枪、法师徒手格斗），除非设定如此。
- 每张都拿道具（像在摆拍，不像在生活）。

### 4.4 手与道具（手指是本机最大的翻车点）

- **宁少勿多**：最稳 `arms relaxed at her sides, hands open and empty`；次稳单手轻握道具。
- **双手交叠、比 V、指人、托腮、抱膝**都容易糊手指：一套里最多留一张，且必须放大检查。
- 道具**单手轻握**，写进 `POSE:` 行（不进 COSTUME，否则四张全被绑上同一件道具）；大件（长枪、大弓、翅膀、坐骑）默认不带。
- 要"没有道具"写 `hands empty, arms relaxed at her sides`，**不要写 `no props`**（会被画成一堆道具）。
- 拿在手里、托在掌心、悬浮在掌上——三种写法结果不同：要"托住"就写 `resting in her open palm`，只写 holding 容易变成悬浮。

### 4.5 示例（沃雅妮沙 · 2026-11 实测，4 镜）

| # | 情境 | 表情 | 动作/手 | 机位 | 道具 |
|---|---|---|---|---|---|
| 01 | 正式开拍，站定面对镜头 | 浅笑、下巴微抬 | 双臂垂放 | 平视全身 | 无 |
| 02 | 听见有人叫她，低头侧身 | 垂眼、嘴角平 | 双臂垂放、视线离开 | 平视全身、侧 3/4 | 无 |
| 03 | 风起，长发被带起来 | 自信半笑、视线掠过镜头 | 一手在身后、一手垂放 | 平视全身 | 无 |
| 04 | 掌心聚起一小颗水珠 | 冷静、视线略偏 | 单手托球、另一手垂放 | 平视全身 | 水珠 |

### ★ G2 脚本确认（文字，不烧图）

- 用**一行一镜**的表格/清单发给用户：`# / 情境 / 表情 / 动作 / 手 / 机位 / 道具`。
- 确认后才开跑 1440；用户说"先看看样子"，就只出**1 张 1152 单张试稿**，不要整套跑。
- 用户改某一镜，只改那一行，其余不动。

---

## P5 成片（1440×2560）

- 角色卡（除 POSE 外全部段落）**逐字不变**，每个镜头一个 `prompt_0X.txt`，脚本读卡替换 `^POSE:` 行。
- 复杂姿态（坐、跳、大幅转身、双手道具）**先出 1 张 1152 单张验证**，通过再上 1440；常规站姿直接 1440。
- **不要用"替换取景句"的方式做半身/特写**：实测改 `{{FRAMING_SENTENCE}}` 会出全身并裁脚。半身/特写一律**先用全身构图出图，再裁**（裁在人中、胸前或腰线，不要裁在关节上）。
- 每张独立种子；不要在卡里写"第 2 张"之类序号。
- 失败单张单独重跑，不要整套重来；每张打印耗时。
- 4 张 1440 约 15–16 分钟，**用后台任务跑**，不要在前台干等。

---

## P6 质检（逐张看，不合格就重出或后处理）

**背景与构图（先看这三条，不合格直接重出）**
1. 背景干净：无亮斑、白色光块、灯架、柔光箱、地面杂物、墙角/门框。
2. 渐变方向与色相一致，四边无脏边、无抹布纹理。
3. 全身入画：头顶有留白、鞋子完整、鞋下有地面留白。

**年龄与表演**
4. 18 岁左右：不显 30 岁、不显 12 岁、不化浓妆。
5. 表情落在角色性格上，且四张有变化。
6. 视线、机位、手位不是四张一个样。
7. 道具拿得自然、比例对、没有多出第二件。

**干净度与清晰度**
8. 额头/脸颊干净，无斑块、纹身状污渍；**遮挡眼的那缕头发位置对**（不是糊住半张脸）。
9. 脸部不油腻；头发根根分明、不成绺、不反光成塑料假发。
10. 皮肤哑光、有真实肤质；脸与眼睛锐利，模糊只出现在背景。
11. 放大到 100%：没有水彩糊块、重影、AI 涂抹感。

**还原与一致**
12. 手指 5 根、脚趾数对（戴手套也要数）；道具在正确侧。
13. 服装要素逐项对得上特征表（款式、内搭、领口、腰带、下装长度、鞋袜）。
14. 各张之间发型/发色/服装/妆容一致（缩到 300px 并排看一眼），只有表情/动作/机位不同。
15. **强特征逐张核验**：遮眼、异色瞳、纹样、发饰左右；遮眼方式在四张里必须一致。
16. 头发没有"漂浮发圈/呆毛"，没有成块发片贴在额头。
17. **腿脚肤色**：把腿、脚与脸/手臂并排看——腿脚不应比脸/手臂暗一截，不能有灰褐斑块、暗环、脏感、青灰色调；有问题先跑 P7b 身体化妆，压不下去再重出。

---

## P7 去油光/去反光（可选）

用户说"不要油腻/不要反光"时做。高光 = 高亮度 + 低饱和的小块（额头、颧骨、鼻梁、发顶）。
numpy 算亮度 `L` 与饱和度 `S` → 脸/头发区域画柔边椭圆遮罩 → 对 `L > 0.80 && S < 0.45` 的像素把亮度压到 ~0.72（强度 0.6）→ 遮罩大半径高斯羽化后混合。只压高光，不磨皮、不改结构；头发可单独再跑一遍。

---

## P7b 身体化妆（腿脚肤色统一，建议默认做）

对照 P6 第 17 条，腿脚只要比脸/手臂暗、带褐灰斑就处理。提示词 `SKIN:` 段是治本，但随机种子仍会翻车，成片统一兜一遍。

脚本：本技能目录下 `scripts/skin_makeup.py`（Windows 绝对路径 `D:\DSH\skills\cosplay-photo-set\scripts\skin_makeup.py`；纯 numpy + Pillow，无需 scipy/cv2）

```
python <技能目录>\scripts\skin_makeup.py final_01.png deliver\01_xxx.jpg
```

- 默认 `--strength 0.35`（上身/脸几乎不动，只兜底）+ `--leg-strength 0.85`（腿脚）。
- 原理：皮肤遮罩（RGB + Lab 双规则，逐行取左右边缘中位色排背景，粉/红背景不会被当皮肤；低彩度金属排除）→ 参考色取**上胸/手臂**皮肤中位 L*a*b*（比取脸部高光稳）→ 曝光用「皮肤自身低频亮度」与目标的差做**加法平移**（乘法提亮会把褐斑衬得更脏）→ 色度先在皮肤局部均值上压掉小尺度偏黄/偏红，再整体拉向参考色；纹身/贴布按色相距离保护 → 修正只作用在 y 0.32 以下，脸和手臂不动。
- 轮廓：权重在离皮肤边缘 1–6px 内淡出，贴边像素保持原样，**不会出现贴背景的亮边/光晕**。
- 安全区：`--leg-strength 0.60–0.95`；>1.0 开始像磨皮。腿只是略暗用 0.60，正常 0.85。**不要**对同一张图重复跑。
- 跑完放大看：膝盖/脚踝阴影是否还在、腿与手臂交界有没有色阶断层、纹身/贴布形状是否完整；`--debug mask.png` 导出遮罩，确认没吃到背景、白裙、银色鞋带。
- 银鞋带/浅色金属可能被轻微柔化（遮罩已按低彩度排除），小件优先整张重出，不要为它反复调参。
- 旧图里 2–4px 的顽固褐点只能淡化；别为了抹它把强度拉满，会把皮肤做假。

---

## P8 导出

- PNG（约 3MB）→ JPEG：从 q100 往下找第一个 ≤1.95MB 的档位，`subsampling=0, optimize, progressive`；1440×2560 实测落在 1.0–1.9MB。
- 命名：`01_动作名.jpg`…`06_动作名.jpg`（动作名写情绪/情境，不要写"姿势1"），另存 `00_基准角色_<角色>.jpg`、`00_全套预览.jpg`（2×2 拼图，单格 720×1280）。
- 项目结构：`D:\DSH\workspace\cosplay_<角色拼音>\`：`refs\`（参考图）、`prompt_*.txt`、`final_*.png`、`character_card.txt`、`deliver\`（成片 JPEG + 预览）。

---

## P9 交付（每次都要给全，别让用户再问）

1. **成片**：`present` 发布，正文内嵌预览图，附文件名与路径。
2. **标题 3 条**（≤20 字，有情绪钩子，不做标题党）。
3. **正文 2–3 句**：第一人称，写具体细节（光、动作、服装还原点、角色性格）。
4. **标签 8–12 个**：`#角色名` `#作品名` `#cosplay` `#真人cos` `#二次元` + 场景/情绪向。
5. **平台差异**：视频号偏"画面质感 + 一句话故事"；小红书偏"过程感 + 可抄作业"；抖音偏"强钩子 + 短句节奏"；公众号偏"图文引言 + 拍摄记录"。用户点名哪些平台就写哪些。
6. **如实说明**（硬性）：
   - 入口 B 写「按你给的这张图还原」，并逐件列出「参考图未给、按官方设定补」的部件（下装/鞋袜/背面）。
   - 写清楚这版**没做到什么**（裙型被简化、腿色偏冷、手指偏僵、脸有漂移…），不要用"无 LoRA 就这样"当挡箭牌，也不要假装是同一张脸。

---

## 附 A · 本机技术参数（z-image-turbo / 8GB）

- 端点：shim `http://127.0.0.1:8200`（OpenAI 兼容，`/v1/images/generations`、`/v1/images/edits`）→ ComfyUI `127.0.0.1:8188`；查询 `http://127.0.0.1:8188/queue` 判断健康。
- 采样：steps 6 / cfg 2 / shift 3 / res_multistep + simple。**不要**提到 cfg 3、steps 12：更"动漫塑料"，负向词也救不回来。
- 尺寸与耗时：`1152x2048` ≈ 73–80s；`1440x2560` ≈ 220–235s；4K 竖图在 8GB 上必 OOM。
- 图生图（`/v1/images/edits`）denoise 固定 0.85：**改姿势/表情不可行**，动作差异只能靠文生图重画。
- 请求体：
  ```json
  {"model":"z-image-turbo","prompt":"...","size":"1152x2048","quality":"low","n":1,"response_format":"b64_json"}
  ```
  返回 `data[0].b64_json`；seed 由 shim 随机（没有可控 seed）。
- 偶发 502：上游短暂忙/显存未释放，等几秒重试同一请求即可；连续失败再查 ComfyUI 进程。

**Windows 本机踩坑**
- ComfyUI 的 `SaveImage` 默认写 `ComfyUI\output`，沙箱下会 `Permission denied` → 启动加 `--output-directory <项目目录>`。
- `Start-Process` 起的服务会随父 shell 退出被杀 → 用常驻后台进程/后台任务跑 ComfyUI 与 shim。
- `& file.ps1` 会被执行策略拦 → `$code = Get-Content -Raw -Encoding UTF8 file.ps1; Invoke-Expression $code`，或 `powershell -ExecutionPolicy Bypass -File`。
- `Set-Content -Encoding UTF8` 带 BOM，Python 读卡要用 `utf-8-sig`。
- 中文提示词用 `[System.Text.Encoding]::UTF8.GetBytes($json)` 作为 body。
- 下载参考图：`Invoke-WebRequest`/`curl.exe` 常因 schannel TLS 报 `SEC_E_NO_CREDENTIALS` → 改用 node 的 `https` 模块。
- 看图：`modlens_read_image` 没配 vision provider 时不可用 → 直接对本地文件用 `read_image`。

---

## 附 B · 翻车对照表（遇症状先查这里）

| 症状 | 触发原因 | 解法 |
|---|---|---|
| 柔光箱/灯架/白色亮块入画 | 写了 `softbox / light stand / wide`，或写了 `no softbox` | 全删；灯光只写光质与方向 |
| 背景有抹布纹理/光斑/墙角 | 背景句写了 `studio`、`spotlight`、`vignette`，或种子偶发搭出墙角 | 用固定背景句；墙角是种子问题，换种子重出 |
| 额头深色斑块 | 写了"刘海垂下来盖住额头" | 改 `fine feathery bangs lifted slightly off the forehead` |
| 腿脚比脸/手臂暗一截、发灰发褐 | 卡里没有全身肤色约束；FACE 写了 `slight uneven tone`；下半身没补光 | 加 `SKIN:` 段（见 P2）+ 灯光句加 `soft warm bounce from the front`；成片跑 P7b |
| P7b 后腿脚发白、发平像塑料 | `--leg-strength` 过高（>1.0）或重复跑 | 降到 `--leg-strength 0.6–0.85`，每张只跑一次；P7b 只平移曝光与偏色，不会磨皮 |
| 皮肤油光 | 写了 `natural shine / dewy / glossy / 自然光泽` | 全删，改 `matte skin, dry powder-matte finish`（不要用负向写 shine） |
| 头发像抹了发油 | 只描述发型没描述质感 | 加 `clean and dry, individually readable strands, no greasy clumps` |
| 头顶冒出漂浮发圈/呆毛 | 写了 `flyaway wisps`、`wispy tapered ends`，或反复描述编发 | 删掉，改 `the crown smooth and flat against the head` |
| 画成双马尾/两个环 | 写了 `no pigtails` | 删负向，改正向 `one continuous fall of hair, completely loose` |
| 眼睛过大像娃娃 | 只写颜色没写大小 | 加 `eyes of natural size (not oversized, not doll eyes)` |
| 显老（像 30 岁） | 写了 `mature / refined / sharp jawline` | 删掉；只留 `eighteen years old, youthful face` + `soft jawline` |
| 显小（像 12 岁） | 写了 `childlike / petite` | 加 `young adult proportions, adult height and body` |
| 鞋子/脚被裁 | 竖构图没写全身留白；或改了取景句做半身 | 用固定 FULL 取景句；半身改后裁 |
| 半身却画到膝盖 | 只改 POSE 里的 `medium shot` | 不要改取景句，直接全身出图后裁 |
| 白色上衣＋白裙变一件长上衣/短裤 | 白色上下装被模型合并 | 先写裙长与后摆，再补胸衣；实在不行接受近似并如实说明 |
| 道具悬浮而不是托住 | 只写 `holding` | 写 `resting in her open palm` |
| 手指糊成一团/多指 | 双手交叠、比 V、指人、握拳 | 改双臂垂放或单手轻握；一套最多一张手势 |
| 遮挡眼的那缕头发糊住半张脸 | 写"头发盖住脸" | 写 `falling straight over her right eye, the rest of her face clear` |
| 单眼遮挡在四张里不一致 | 只写在 HEAD 段，POSE 没重申 | 每张 POSE 行再写一次 `her right eye hidden behind the fringe` |
| 发色渐变方向反了 | 只说"渐变" | 写 `only the last few centimeters of the tips dyed ...` |
| 银白挑染变成两大块 | 没限宽度 | 写 `a few narrow pale silver-white streaks through the front locks` |
| 服装整体画错 | 凭记忆写提示词，没看图 | 回 P1 重拆；最贵的一类返工 |
| 四张脸不像同一个人 | 卡不够具体 / 只靠换种子 | 按附 C 补 FACE 段锚点，重出基准图再确认 |

---

## 附 C · 一致性锁定与年龄

**一致性**
1. 固定段存文件（`character_card.txt`），每张从文件读、只替换 `^POSE:` 行；手打必然改字，改字就漂。
2. 想改细节：改那一句里的一个短语 → **重出基准图 → 重新确认**，不要在成片批次里偷偷改。
3. FACE 段锚点顺序：脸型（`soft oval face, soft jawline`）→ 瞳色 → 眼型（`outer corner slightly upturned`）→ 唇（`soft coral lips, lower lip slightly fuller`）→ 眉。只写"漂亮"没用。
4. 服装拆「必现件 / 可选件」：必现件 3 条（主色 + 主裙型 + 标志配饰），每张都要对；可选件允许漂移，交付时说明。
5. 一致性验收：四张缩到 300px 并排，一眼不像同一个人就先补 FACE 段重出；补完仍差，就老实说"这批里 X 号脸偏了"。
6. 没有可控 seed：能控的是句子与构图，不是运气。

**年龄（硬约束）**
- 一律 18 岁左右：女性 → `a real 18-year-old East Asian woman`；男性 → `a real 18-year-old East Asian man`。
- 三处年龄锚点同时写：开头人物句、`AGE:` 段、`FACE:` 段的 `bone structure of an eighteen-year-old`。只写一处会滑到 22–28 岁。
- 优先正向描述（`fresh youthful face`、`soft jawline`、`subtle real-person makeup`）；负向词（`not a doll face`、`no mature makeup`）会被当正向。
- G1 确认时直接问一句"这个年龄感对吗"。

---

## 附 D · 沟通纪律

- **需要确认的节点必须给真实产物**：G1 给图；G2 给文字脚本（用户要图就先出 1 张 1152 单张试）。禁止只发提示词/参数让用户脑补。
- 改稿给「上一版 → 这一版」对照 + 一句话说明改了什么、为什么；不要只说"已优化"。
- 用户说"哪里不对"时先分类：**设计错**回 P1/P2；**画技错**改质感/手势/构图那一句。
- P4 脚本没确认前不跑 1440；G1 没确认前不跑任何成片。
- 明确模型边界：无 LoRA 时人脸靠提示词而非像素级一致；写实天花板有限，遮眼/异色瞳/细配件/复杂道具都会漂，交付时如实说。
