---
name: dlazy-image-guide
version: 1.0.0
description: Pick the right dLazy image model and get it right on the first call. Covers all 22 image tools with their prompt caps, size formats, reference-image support, and credit costs, plus editing and post-processing chains.
metadata: {"clawdbot":{"emoji":"🎨","requires":{"bins":["npm","npx"],"env.optional":["DLAZY_API_KEY"]},"install":"npm install -g @dlazy/cli@1.2.3","installAlternative":"npx @dlazy/cli@1.2.3","homepage":"https://dlazy.com","configLocation":"~/.dlazy/config.json","apiEndpoints":["api.dlazy.com","files.dlazy.com"]},"openclaw":{"systemPrompt":"When invoking this skill, run `dlazy <model> -h` to confirm the current flags before building a command."}}
---

# dLazy 生图选型指南

dLazy 有 22 个图像工具。它们的提示词上限差 5 倍、尺寸参数有 6 种互不兼容的写法、默认值里藏着竖屏陷阱，而参数写错的代价是整次调用被拒——积分不退。

这个 skill 解决的是**选哪个、怎么一次调对**，不是教你 dLazy 怎么装。

## 何时使用

- 用户要生成图片，但没指定模型（"帮我画一张…"）
- 用户指定了模型，但参数组合可能无效（尺寸、比例、清晰度）
- 需要按场景挑模型：中文海报、产品图、矢量 logo、写实人像、批量出图
- 需要编辑已有图片：换元素、加文字、抠图、放大、转矢量
- 生成失败了，需要判断是模型选错还是参数写错

不适用于：视频生成、语音、纯文本任务。

## 三条硬规则

**1. 先查上限，再写提示词。** 提示词上限按模型差异极大，超出会让整次请求返回 400，不是截断：

| 上限 | 模型 |
|---|---|
| 500 | seedream 全系、jimeng-t2i、viduq2-t2i |
| 1300 | qwen-image-2-pro |
| 2000 | gpt-image-2、banana 系、recraft 全系、mj-imagine |
| 2500 | kling-image-o1 |

**500 是最容易踩的**。一段带风格、构图、配色、氛围的中文描述轻松过 500 字。要么精简，要么换 2000 档的模型。图片提示词无法像旁白那样分段——半段描述只会画出半张图。

**2. 尺寸参数不通用。** 六种写法，照抄别的模型的参数必然报错。详见 `models.md`，速记：

- `gpt-image-2` → `--size 2048x1152`（像素，用 `x`，固定枚举）
- `jimeng-t2i` / `qwen-image-2-pro` → `--size 2048*2048`（像素，用 `*`）
- seedream 系 / vidu → `--size 16:9` + `--resolution 2k`
- banana 系 → `--aspectRatio 16:9` + `--imageSize 2K`
- recraft 系 / mj → 只有 `--aspect_ratio`
- kling → `--aspect_ratio` + `--clarity`

**3. 不确定就先 `--dry-run`。** 它打印将要发送的参数和积分估算，不消耗积分也不产图：

```bash
dlazy banana-pro --prompt "..." --imageSize 4K --dry-run
```

参数拿不准、要给用户报价、或要批量出图之前，先跑这个。

## 选型决策树

从上往下匹配第一个命中的条件：

1. **要矢量图 / SVG / logo** → `recraft-v4-vector`（11 积分）；质量优先用 `recraft-v4-pro-vector`（22）
2. **图里要有准确的中文文字**（海报、封面、幻灯片）→ `gpt-image-2`（16 积分起）或 `qwen-image-2-pro`（20）
3. **要改一张已有的图**（换元素、改文字、合成）→ `gpt-image-2 --images`，唯一能稳定按指令局部改的
4. **要极致性价比、批量铺量** → `seedream-5.0-lite` 或 `mj-imagine`（都是 5 积分）
5. **要 4K 大图** → `banana-pro --imageSize 4K`（30）或 `seedream-5.0 --resolution 4k`（8，更便宜）
6. **要艺术性 / 风格化构图** → `mj-imagine`（5）
7. **摸不准** → `seedream-5.0`（5 积分，2K，综合素质均衡）

完整对照见 `choosing.md`。

## 默认值陷阱

不写尺寸参数时，这几个模型的默认值可能不是你要的：

- `viduq2-t2i` 默认 **9:16 竖屏**
- `jimeng-t2i` 默认 **1440*2560 竖屏**
- `banana2` 默认 **512**（很低清，出图会糊）
- `gpt-image-2` 默认输出 **jpeg**，需要透明或无损时要显式 `--format png`

做横屏内容时，务必显式写尺寸。

## Reference Map

| 文件 | 内容 |
|---|---|
| `models.md` | 22 个工具的完整参数速查：上限、尺寸写法、参考图支持、积分 |
| `choosing.md` | 按场景选型：中文海报、产品图、矢量、写实、批量、4K |
| `prompting.md` | 提示词写法，含 500 字上限下的压缩技巧 |
| `editing.md` | 参考图、局部编辑、抠图/放大/矢量化的后处理链 |
| `troubleshooting.md` | 报错对照表与省积分策略 |

## 认证

```bash
dlazy login          # 设备码流程，自动保存 key
dlazy auth set KEY   # 已有 key 时直接写入
```

Key 从 https://dlazy.com/dashboard/organization/api-key 获取，保存在 `~/.dlazy/config.json`。也可用 `DLAZY_API_KEY` 环境变量按次传入。

积分不足会返回 `insufficient_balance`，充值入口：https://dlazy.com/dashboard/organization/settings?tab=credits
