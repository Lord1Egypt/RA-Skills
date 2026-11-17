# 图像生成 Playbook

> 解决「选什么模型、怎么写提示词、怎么调参数、怎么批量出图」的完整决策链路，子技能 `image-generation` / `image-editing` 的落地方法论。
> 增量信息：模型选择矩阵 + prompt 结构模板 + 参数速查 + 踩坑表 + 交付清单（不复制子技能内容）。

## 1. 模型选择决策树

```
要生成什么图？
├─ 写实人像/产品图 → 优先 FLUX.1-dev（细节强）或 SDXL（生态最全）
├─ 二次元/插画 → SDXL 系二次元微调模型（animagine 等）
├─ 极简/图标/UI 素材 → SDXL 或 FLUX-schnell（快）
├─ 需要严格遵循文字/logo → FLUX（文字渲染能力明显强于 SDXL）
├─ 高速低成本原型 → SDXL-Turbo / LCM（4-8 步）
└─ 老照片修复/放大 → 专用 ControlNet + tile 模型，不走文生图
```

| 模型系 | 显存/内存要求 | 步数 | 强项 | 弱项 |
|--------|--------------|------|------|------|
| SD1.5 | 低（4G 可跑） | 20-30 | 生态最大、老硬件可跑 | 细节/文字弱 |
| SDXL | 中（8G） | 20-35 | 细节与构图平衡，生态第二大 | 文字仍一般 |
| FLUX.1-dev | 高（16G+，量化可降） | 20-30 | 文字/细节/遵循度顶尖 | 重、慢、需配套 T5 编码器 |
| FLUX.1-schnell | 高 | 1-4 | 极快 | 质量略逊 dev |
| SDXL-Turbo/LCM | 中 | 4-8 | 实时预览级速度 | 细节让步 |

**选型原则**：个人/小团队默认 **SDXL 起步**（生态、显存、速度平衡），有文字渲染或高细节需求再上 FLUX；不要一上来追最新模型——部署成本与收益不成正比。

## 2. Prompt 结构模板（SDXL/FLUX 通用）

正面 prompt 按「主体 → 细节 → 环境 → 风格 → 质量词」五段拼：

```
[主体与构图] a cyberpunk street vendor, full body, center composition
[细节] detailed mechanical arm, glowing neon signs, wet asphalt reflections
[环境] rainy night market, dense crowd, shallow depth of field
[风格] cinematic lighting, photorealistic, 8k detail
[质量锚] masterpiece, best quality, highly detailed
```

负面 prompt 三件套（不同模型可微调）：

```
worst quality, low quality, blurry, deformed, distorted, extra fingers,
bad anatomy, watermark, text, logo, jpeg artifacts
```

**踩坑 1**：负面词不是越长越好——SDXL 对负面词敏感度低于 SD1.5，堆 30+ 词只会稀释权重。保留上面 15 个核心词即可，具体坏图特征按需追加。
**踩坑 2**：中英混杂 prompt 会导致模型理解漂移。稳定做法：**正文用英文**（模型训练语料），中文只用于你的笔记/注释。

## 3. 参数速查（SDXL 参考基线）

| 参数 | 默认 | 调整方向 |
|------|------|----------|
| steps | 25-30 | 步数多 ≠ 更好，30 后边际收益趋零 |
| CFG | 5-7 | 低（3-5）自由度高；高（>10）过曝/伪影 |
| sampler | euler / dpmpp_2m | 一般不动；想稳定出图用 euler + 固定 seed |
| seed | -1（随机） | 复现/微调时固定，微调用「同一 seed 改 prompt」 |
| 分辨率 | 1024×1024（SDXL） | 非训练尺寸会出重复纹理；放大走 hires fix 而非直接拉大 |
| 批量 | 1 | 确定风格后再批量，避免浪费 |

**hires fix 正确姿势**：先在 1024×1024 出基础图 → `UpscaleModelLoader` + `LatentUpscale` + 二次采样（denoise 0.3-0.5）→ 放大到目标尺寸。直接 2048×2048 生成会出双头/重复纹理。

## 4. 批量出图纪律（用脚本，不手搓）

- 固定 `seed` 列表 + 逐张记录 → 可复现、可回溯（用 [scripts/media_batch.py](../scripts/media_batch.py) 或工作流内 seed 队列）
- 一批只动一个变量（换 prompt / 换模型 / 换参数），否则无法归因
- 出图后统一走校验：分辨率、格式、是否纯黑/纯白（均值方差检测）
- 交付图统一命名：`{date}-{subject}-{seed}.png`

## 5. 常见踩坑表

| 现象 | 根因 | 处置 |
|------|------|------|
| 双头/重复纹理 | 直接生成超训练分辨率 | 1024 基础图 + hires fix |
| 手指/牙齿崩坏 | 模型能力边界 | 用负面词压制；或修图（img2img + inpaint） |
| 文字乱码 | SDXL 文字渲染弱 | 换 FLUX；或图后处理重排文字 |
| 风格不稳定 | seed 随机 + 参数漂移 | 固定 seed、固定 sampler/CFG |
| 出图偏灰/雾 | CFG 过高或 VAE 不匹配 | CFG 降到 6 以下；检查 VAE |

## 6. 交付清单

- [ ] 模型选型有依据（不是随机试）且资源可承受
- [ ] prompt 五段结构完整、全英文、无堆砌负面词
- [ ] 分辨率在训练尺寸附近；放大走 hires fix
- [ ] 批量任务 seed 记录可复现
- [ ] 输出图片人工抽查无黑/灰/伪影/双头
- [ ] 交付命名规范、格式统一（PNG 保质量，Web 用 JPG/WebP）

## 7. 相关子技能与层次边界（L2→L3）

本篇是 **方法论层（L2）**：负责「模型选哪个、prompt 怎么搭、参数给多少、批量怎么不失控」的
判断依据。具体操作步骤与调用方式在下列 L3 子技能，不在本篇重复：

| 落地能力 | 子技能 | 本篇为它提供什么 |
|----------|--------|------------------|
| 文生图 / 图生图 / 批量出图 | [skills/image-generation/SKILL.md](../skills/image-generation/SKILL.md) | 第 1 节模型决策树、第 2 节 prompt 五段结构、第 3 节参数基线 |
| 局部重绘 / 扩图 / 抠图换背景 | [skills/image-editing/SKILL.md](../skills/image-editing/SKILL.md) | 第 3 节参数基线（denoise/CFG 同源）、第 5 节伪影排查 |

**边界声明**：本篇不讲 ComfyUI 怎么装、节点怎么接（见 [references/comfyui-workflow-playbook.md](comfyui-workflow-playbook.md)），
不讲视频路线（见 [references/video-generation-playbook.md](video-generation-playbook.md)）；批量落地用
[scripts/media_batch.py](../scripts/media_batch.py)，审美拍板由人做。
