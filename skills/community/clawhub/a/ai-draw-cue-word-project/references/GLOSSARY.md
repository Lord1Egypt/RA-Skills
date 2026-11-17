<div align="center">

# 📖 术语表 · Glossary

**AI DRAWING CUE-WORD PROJECT**

*每个词都用一句人话解释 · Every term explained in one plain sentence*

</div>

---

> 英文术语保留原样，方便你对照 README、CSV 表与各模型官方文档。
> The English term is kept as-is so you can match it against the README, the CSV sheets and each model's official docs.

| 术语 Term | 中文 | 一句话人话 · Plain meaning |
|---|---|---|
| **Prompt** | 提示词 | 你写给 AI 绘画模型的那段描述文字。 |
| **Cue-word engineering** | 提示词工程 | 用可复用的词表 + 权重规则，把出图结果控制住，而不是每次都碰运气。 |
| **Prompt syntax family** | 语法家族 | 五大类模型的写法：自然语言流 / 对话式 / Midjourney / Stable Diffusion / 国内 API。 |
| **Hard anchor** | 硬锚点 | 绝对不能变的固定特征（例如左眼下方的痣），权重 ≥ 1.6。 |
| **Core feature** | 核心特征 | 所有场景里都要保留的特征，权重 1.3–1.5。 |
| **Baseline** | 基线描述 | 默认强度的那部分描述，权重 1.0–1.2。 |
| **Weight** | 权重 | 控制某个词影响力的数值——越大，模型越不敢忽略它。 |
| **Negative prompt** | 负面词库 | 你不想要的东西；注意 FLUX.2 与 Gemini 3 Pro 完全不支持，只能正面写。 |
| **Reference image** | 参考图 | 给模型一张图，让它照着某种身份或风格走。 |
| **LoRA** | 小型微调插件 | 一个几十 MB 的「人物 / 风格补丁」，挂到 SD 上就能稳定复现同一个角色。 |
| **`--cref` / `--oref`** | MJ 角色参考参数 | Midjourney 里指定角色参考的参数；版本不同名字不同（v6 用 `--cref`，v7 用 `--oref`）。 |
| **Multi-character scene** | 多角色场景 | 3 个以上角色同框，需要空间关系表来约束层叠、视线链与遮挡。 |
| **Storyboard / panel** | 分镜 / 面板 | 漫画的一格；分镜骨架规定每一格承担什么叙事职能。 |
| **Speech bubble** | 对话气泡 | 台词框；类型、尾巴朝向、图层优先级都有规则。 |
| **Temporal consistency** | 时序一致性 | 前后两张图之间，人物、服装、光线不能变。 |
| **P0 / P1 / P2** | 校验优先级 | P0 出错等于废图、必须重做；P1 影响可用性、先修；P2 记录、下轮改进。 |
| **Iteration log** | 迭代日志 | 每次出图都记一笔；同类型连续失败 3 次，就换模型或换参数路线。 |
| **Aspect-ratio baseline** | 比例基准 | 不同画风的身头比标准（Q 版 2–3、写实 7.5+），容差 ≤ 5%。 |
| **Cloudflare Pages workbench** | 在线工作台 | www.nohnlins.com/ai-draw/ —— 把 CSV 数据标准变成可交互的生成界面。 |

---

## ✦ English Glossary

*Every term explained in one plain sentence.*

| Term | Plain meaning |
|---|---|
| **Prompt** | The description text you write for an AI image model. |
| **Cue-word engineering** | Using reusable word lists plus weighting rules to control the output, instead of hoping each time. |
| **Prompt syntax family** | The five families of model syntax: natural-language flow / conversational / Midjourney / Stable Diffusion / domestic APIs. |
| **Hard anchor** | A fixed feature that must never change (e.g. the mole under the left eye), weight ≥ 1.6. |
| **Core feature** | A feature to keep in every scene, weight 1.3–1.5. |
| **Baseline** | The default-strength part of the description, weight 1.0–1.2. |
| **Weight** | The number controlling a word's influence — the larger it is, the less the model dares ignore it. |
| **Negative prompt** | What you don't want; note that FLUX.2 and Gemini 3 Pro don't support it at all, so you must phrase things positively. |
| **Reference image** | An image you give the model so it follows a certain identity or style. |
| **LoRA** | A tens-of-MB "character / style patch" you attach to SD to reproduce the same character reliably. |
| **`--cref` / `--oref`** | Midjourney's character-reference parameters; the name differs by version (v6 uses `--cref`, v7 uses `--oref`). |
| **Multi-character scene** | Three or more characters in one frame, needing a spatial-relation table to constrain layering, gaze chains and occlusion. |
| **Storyboard / panel** | One frame of a comic; the storyboard skeleton defines what narrative job each frame carries. |
| **Speech bubble** | The dialogue box; type, tail direction and layer priority all follow rules. |
| **Temporal consistency** | Between two consecutive images, character, clothing and lighting must not change. |
| **P0 / P1 / P2** | Check priorities: a P0 error ruins the image and must be redone; P1 hurts usability and is fixed first; P2 is logged and improved next round. |
| **Iteration log** | One entry per generation; three consecutive failures of the same type means switching model or parameter route. |
| **Aspect-ratio baseline** | The head-to-body ratio standard for each style (chibi 2–3, realistic 7.5+), tolerance ≤ 5%. |
| **Cloudflare Pages workbench** | www.nohnlins.com/ai-draw/ — turns the CSV data standard into an interactive generation interface. |

---

<div align="center">

[← 返回 README](./README.md) &nbsp;·&nbsp; [中文说明](./README-zh.md)

<sub>NOHN AI · AI DRAWING CUE-WORD PROJECT</sub>

</div>
