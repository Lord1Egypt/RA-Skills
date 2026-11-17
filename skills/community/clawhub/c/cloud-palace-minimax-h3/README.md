# 云上仙宫提示词生成器（Cloud-Palace-Minimax-H3）

> 双通道东方史诗感提示词生成器：**通道 A · 文生图** + **通道 B · MiniMax H3 视频**。
> 面向 openclaw 的纯提示词技能，无外部依赖，不下载/不调用任何模型；输出可直接喂给 Midjourney / DALL·E / Stable Diffusion 等文生图模型，或 MiniMax H3 视频生成接口。

![skill-banner](https://img.shields.io/badge/openclaw-skill-blue) ![channel](https://img.shields.io/badge/channels-A%20%2B%20B-9b59b6) ![spec](https://img.shields.io/badge/H3-T2VA%20%7C%20I2VA%20%7C%20FL2VA%20%7C%20L2VA%20%7C%20Ref2VA-orange)

---

## 功能（Function）

| 通道 | 适用场景 | 输出 |
|:---|:---|:---|
| **A · 文生图** | 用户要求静态画面 / 出图 / 海报 / 概念图 | 东方建筑 × 巨物美学 × 空间压缩感的**六维结构英文提示词**（比例 / 镜头 / 场景 / 人物 / 光影 / 氛围 / 技术） |
| **B · H3 视频** | 用户要求做成视频 / 动起来 / 短片 | 严格遵循 **MiniMax H3 官方规范** 的三段式英文提示词：`integrated_multimodal_description` + `overall_soundscape` + `non_diegetic_music`，支持 **T2VA / I2VA / FL2VA / L2VA / Ref2VA** 全五种任务 |

**两通道通用铁律：**
- 直接输出提示词本身，不附加任何寒暄、前后缀或解释（失败处理允许的一句假设/默认值说明除外）。
- 画面中**不得**出现文字、logo、水印；除非用户明确要求某块可见文字，否则不创作任何 on-screen text。

---

## 触发时机（Triggers）

满足以下任一条件时自动触发本技能：

- 🏯 关键词命中：**云上仙宫 / 天宫 / 仙界 / 云端仙境 / 凌霄宝殿 / 南天门 / 蟠桃园 / 广寒宫 / 蓬莱 / 昆仑 / 炼丹炉 / 藏经阁 / 练剑台 / 东海龙宫** ……
- 🎬 视频请求：**文生视频 / 图生视频 / 做成视频 / 动起来 / 生成短片 / H3 提示词 / T2VA / I2VA / FL2VA / L2VA / Ref2VA**
- 🖼️ 图像请求：**出图 / 文生图 / 海报 / 概念图 / 东方史诗感 / 巨物美学 / 空间压缩感**
- 🧩 同时要图 + 视频：先输出通道 A，再基于同主题输出通道 B。

---

## 内置主题库（节选）

> 未命中主题时按"同构风格"自建（核心元素 = 东方建筑词汇 + 主题意象）。

| 类别 | 代表主题 |
|:---|:---|
| 天宫体系 | 凌霄宝殿（帝座 / 玉阶 / 九龙盘柱）、南天门（巨型拱门 / 云海阶梯）、天庭朝会、蟠桃园 |
| 修道场所 | 练剑台（无栏杆悬台）、炼丹炉（九转丹炉 / 八卦阵法）、藏经阁（浮空卷轴）、悟道崖、听雨轩 |
| 月宫系列 | 广寒宫（冰晶玉砌 / 桂树 / 银辉铺地）、嫦娥舞袖 |
| 龙宫系列 | 东海龙宫（珊瑚立柱 / 珍珠穹顶 / 水晶王座）、龙女戏珠 |
| 仙山系列 | 蓬莱仙岛（悬岛群 / 仙桥）、昆仑瑶池（西王母 / 凤凰降临）、泰山云海 |
| 战斗试炼 | 渡劫天梯（九霄雷云）、神魔战场（灵气乱流） |
| 时序变化 | 晨曦、黄昏、月夜、雪境 |
| 材质特效 | 琉璃宫殿（prismatic）、白玉仙府（lustrous white jade）、朱砂神阙（imperial red）、青铜古刹（patinated bronze）、水晶幻境 |

光影氛围词库（Tyndall / volumetric / rim / god rays / atmospheric perspective；色调 platinum-white / cyan-blue / gold-and-purple / pale pink）按需取用。

---

## 参数提取指南

从用户输入 `$ARGUMENTS` 中按顺序解析：

| # | 参数 | 必填 | 默认值 | 说明 |
|:--|:---|:--|:---|:---|
| 1 | **主题 Theme** | ✅ | `凌霄宝殿`（追问后仍缺则取此） | 场景核心词，中文 / 英文均可 |
| 2 | **通道** | ❌ | `图`（关键词含「视频/动起来/H3」时切换） | `图` 或 `视频` |
| 3 | **画面比例** | ❌ | `16:9` | 9:16 / 4:3 / 21:9 等；通道 B 可由 H3 任务类型决定 |
| 4 | **时长** | ❌ | `6 秒` | 仅通道 B |
| 5 | **动作 / 镜头** | ❌ | `默认推轨` | `起飞` / `环绕` / `俯冲` / `左移` / `右移` 等 |
| 6 | **首帧 / 尾帧图片** | ❌ | — | 仅 FL2VA / I2VA |
| 7 | **参考视频 / 参考音频 label** | ❌ | — | 仅 Ref2VA |

---

## 执行步骤

### 通道判定（铁律）
- 用户要**图** → 通道 A。
- 用户要**视频** → 通道 B（H3）。
- 同时要两者 → **先 A 后 B**，同一主题。

### 通道 A · 文生图
1. 解析主题 / 比例 / 偏好（天气、色调、人物、时序）。
2. 命中主题库 → 直接取核心元素；未命中 → 按同构风格自建。
3. 套用 **A3 六维结构模板**（比例 → 镜头 → 场景 → 人物 → 光影 → 氛围 → 技术）。
4. 硬性要求：
   - 必须写"人物仅占画面 1%–3%"（尺度标尺）。
   - 建筑必须被画面裁剪（off-screen cutting / extending beyond the frame）。
   - 建筑描述至少含 3 项东方建筑词（dougong / upturned eaves / vermilion lacquered columns …）。

### 通道 B · MiniMax H3 视频
1. **判定 H3 任务类型：**

   | 用户特征 | 任务类型 |
   |:---|:---|
   | 纯文本生成视频 | **T2VA** |
   | 给一张图生成视频 | **I2VA** |
   | 给首帧 + 尾帧 | **FL2VA** |
   | 给一段视频做续写 | **L2VA** |
   | 参考某段视频/音频 | **Ref2VA** |

2. **判定失败时**：默认按 I2VA 处理（最常见），并在提示词外用一句话注明假设。
3. **组装三段式提示词：**
   - `integrated_multimodal_description`：1–N 个 `[Shot N]`，逐 shot 写镜头、动作、光影、风格基线（1–2 句英文建立）、帧锚点 `<Picture 1>`/`<Picture 3>`；生成类任务正文 350–500 英文词。
   - `overall_soundscape`：环境声 / 现场音（不含配乐）。
   - `non_diegetic_music`：纯配乐（弦乐 / 鼓点 / 钢琴 / 国风等）。
4. **引用参考资源**用 `<Subject N>` / `<Video N>` / `<Picture N>` / `<Audio N>` 标签；`retention_analysis` 显式标注 `fully_preserved` / `partially_preserved` / `attribute_transfer` / `weak_reference`。
5. **风格基线统一**：T2VA / I2VA 默认 `Live-action, cinematic, 70mm IMAX film stock aesthetic with anamorphic lens and shallow depth of field`；可被用户覆盖。

---

## 常用调用示例

| 用户输入 | 通道 | 任务类型 | 关键参数 |
|:---|:---|:---|:---|
| `凌霄宝殿` | A | — | 16:9 / 默认推光影 |
| `凌霄宝殿 9:16` | A | — | 9:16 / 竖屏巨物 |
| `广寒宫，黄昏` | A | — | 16:9 / pale pink dusk |
| `凌霄宝殿，做成视频，6秒` | B | T2VA | 默认推轨 |
| `练剑台，角色原地起飞` | B | T2VA | 起飞 + 仰拍跟踪 |
| 基于某张仙宫图生成视频 | B | I2VA | 锚定 `<Picture 1>` |
| 给定首帧 + 主题 + 尾帧 | B | FL2VA | `the shot begins from <Picture 1>` / `ends on <Picture 3>` |
| 续写某段视频 | B | L2VA | `<Video 1>` 续写源 |
| 复用某段古风配乐 | B | Ref2VA | `<Audio 1>` 风格 / 音色 |

---

## 输出规范

- **通道 A**：单段英文提示词，可直接用于 Midjourney（含 `--ar`）、DALL·E、Stable Diffusion。
- **通道 B**：三段式 `integrated_multimodal_description` / `overall_soundscape` / `non_diegetic_music`，可直接喂给 MiniMax H3 模型。

**H3 任务类型对照：**

| 任务 | 典型字段 | 必备引用标签 |
|:---|:---|:---|
| T2VA | 风格基线 + 单/多 shot | — |
| I2VA | 以 `<Picture 1>` 起手 | `<Picture 1>` |
| FL2VA | 首尾帧锚点 | `<Picture 1>`、`<Picture 3>` |
| L2VA | 续写源 | `<Video 1>` |
| Ref2VA | 参考视频/音频 | `<Video 1>` / `<Audio 1>` + `retention_analysis` |

---

## 失败处理

| 场景 | 兜底方案 |
|:---|:---|
| 用户未给主题 | 追问一次；仍缺则用默认 `凌霄宝殿`，并在提示词外用**一句**话注明所采用的默认值 |
| 视频模式判不准（如只给了图未说明首/尾帧） | 按 **I2VA** 处理，并在提示词前**一句**话注明假设 |
| 时长与动作节奏冲突（如 2 秒内多镜头切点） | 压缩为单 shot，并在提示词前**一句**话说明调整 |
| 主题库未命中 | 按"东方建筑 + 主题意象"自建，保留 A3 六维结构与巨物基准 |

---

## 快速上手（30 秒）

1. 在对话里输入：`凌霄宝殿 9:16` → 立即得到一段通道 A 的六维英文提示词。
2. 改成：`凌霄宝殿，做成视频，6秒` → 立即得到通道 B 的 T2VA 三段式提示词。
3. 上传一张仙宫图，输入：`让这张图动起来` → 通道 B 的 I2VA 提示词，`<Picture 1>` 自动锚定原图。

---

## 元信息（Metadata）

| 字段 | 值 |
|:---|:---|
| `name` | `cloud-palace-h3` |
| `description` | 云上仙宫提示词生成器（双通道升级版）：①文生图——东方史诗感、巨物美学、空间压缩感的六维结构提示词；②视频——严格遵循 MiniMax H3 官方规范（T2VA/I2VA/FL2VA/L2VA/Ref2VA）生成电影级动态影像提示词 |
| `argument-hint` | `[主题] [图|视频] [比例/动作/时长可选]` |
| `user-invocable` | ✅ |
| 外部依赖 | ❌（纯提示词生成器） |
| 适用模型 | Midjourney / DALL·E / SDXL 等文生图模型 + **MiniMax H3** 视频生成接口 |
| 适用人群 | 东方美学 / 仙侠题材的概念设计师、短视频创作者、游戏美术 |

---

## 许可与协作

- 内部使用：在 openclaw 中通过 `$cloud-palace-h3 [主题] [参数]` 调用。
- 主题扩展：按 A2 主题库格式补充新条目（中文名 / 英文名 / 核心元素 / 氛围）。
- 反馈：发现 H3 规范更新或主题词不准，直接修改 `SKILL.md` 对应章节即可，无需改动 README。
