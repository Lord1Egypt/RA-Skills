# 视频生成 Provider 对比矩阵

## 总览

| Provider | 类型 | 最大时长 | 分辨率 | 成本 | 质量评级 | 适用场景 |
|----------|------|---------|--------|------|---------|---------|
| ComfyUI | 本地 | 无限制* | 自定义 | 免费(电费) | ★★★★ | 完全控制、隐私敏感 |
| LumaAI Dream Machine | 云API | 5s | 1080p | 免费额度/付费 | ★★★★ | 快速高质、自然语言prompt |
| Runway Gen-3/Gen-4 | 云API | 10s | 4K | 免费试用/付费 | ★★★★★ | 最高质量、商业级 |
| Replicate | 云API | 模型依赖 | 模型依赖 | 按用量/免费层 | ★★★ | 灵活、多模型选择 |
| DALL-E + FFmpeg | 混合 | 关键帧拼接 | 1024x1024 | ~$0.04/帧 | ★★★ | 风格一致性、可控性 |
| Kling (可灵) | 云API | 10s | 1080p | 付费 | ★★★★ | 中文优化、国内访问 |

*ComfyUI 受限于 GPU 显存和处理时间

## 详细对比

### ComfyUI (本地部署)

**优势:**
- 完全免费（仅电费）
- 完全离线可用，隐私保护
- 支持自定义模型和 LoRA
- 可视化节点编辑器
- 社区模型丰富

**限制:**
- 需要 NVIDIA GPU (8GB+ VRAM)
- 安装配置复杂
- 生成速度依赖硬件
- 模型下载占用大量磁盘空间 (2-7GB/模型)

**推荐配置:**
- 最低: RTX 3060 12GB
- 推荐: RTX 4070 12GB+
- 理想: RTX 4090 24GB

**适配 Prompt 风格:**
```
positive: masterpiece, best quality, cinematic lighting, (描述)
negative: low quality, blurry, deformed
Steps: 20-30, CFG: 7-8, Sampler: euler_ancestral
```

### LumaAI Dream Machine

**优势:**
- 高质量输出
- 自然语言 prompt 支持
- 快速生成 (约2-5分钟)
- API 简洁易用

**限制:**
- 单次最长 5 秒
- 免费额度有限
- 需要联网

**API 端点:** `https://api.lumalabs.ai/dream-machine/v1/generations`

**适配 Prompt 风格:**
```
Camera slowly pans across a vast cyberpunk cityscape at night,
neon signs reflecting off wet streets, volumetric fog, cinematic
lighting, photorealistic, 4K quality
```

### Runway Gen-3 / Gen-4

**优势:**
- 业界最高质量
- 支持图生视频
- 高级运镜控制
- 支持 4K 输出

**限制:**
- 价格较高
- 需要国际支付
- 免费试用额度少

**API 端点:** `https://api.dev.runwayml.com/v1`

**适配 Prompt 风格:**
```
Subject: Two giant robots engaged in combat
Camera: Low angle tracking shot, slow motion
Style: Photorealistic, volumetric lighting, lens flare
Environment: Destroyed cityscape, smoke and debris
```

### Replicate

**优势:**
- 多模型选择 (SVD, AnimateDiff, etc.)
- 按用量计费，灵活
- 社区模型丰富
- 有免费层

**限制:**
- 质量参差不齐
- 模型选择需要经验
- 部分模型排队等待

**推荐模型:**
- `stability-ai/stable-video-diffusion` — 图生视频
- `lucataco/animate-diff` — 文生视频
- `zsxkib/realistic-voice-cloning` — 语音克隆(配合使用)

### DALL-E + FFmpeg 管线

**优势:**
- 风格一致性高
- 完全可控每一帧
- 价格可预测

**限制:**
- 不是真正的视频生成
- 帧间连贯性差
- 需要后期处理

**工作流:**
1. DALL-E 3 生成关键帧 ($0.04/帧)
2. FFmpeg 拼接帧序列
3. 可选: 使用插值工具补帧

### Kling (可灵)

**优势:**
- 中文 prompt 优化
- 国内网络访问流畅
- 多镜头生成支持
- 质量持续提升

**限制:**
- API 访问需要申请
- 文档以中文为主
- 国际市场知名度低

## 选择决策树

```
用户有 NVIDIA GPU 且 VRAM >= 8GB?
├── 是 → 推荐 ComfyUI (免费)
│   └── 用户需要最高质量?
│       ├── 是 → 建议同时使用 Runway 对比
│       └── 否 → ComfyUI 足够
└── 否 → 检查 API 密钥
    ├── 有 LumaAI Key → 推荐 LumaAI (高性价比)
    ├── 有 Runway Key → 推荐 Runway (最高质量)
    ├── 有 Replicate Token → 推荐 Replicate (灵活)
    ├── 有 OpenAI Key → DALL-E + FFmpeg (兜底方案)
    └── 无任何 Key → 引导用户注册最便宜的方案
```
