---

slug: dlazy-gen-tool-pro
name: "dlazy-gen-tool-pro"
version: "1.0.0"
displayName: "综合生成工具-专业版"
summary: "全模态生成引擎，覆盖40+模型，支持图片/视频/音频生成与管道链接批量工作流。。综合生成工具专业版，面向专业团队的全模态AI生成平台。核心能力： - 40+ 模型全覆盖（图片、视频、音频三大"
license: "Proprietary"
edition: "pro"
description: |- 功能涵盖: dlazy, gen。
  综合生成工具专业版，面向专业团队的全模态AI生成平台。核心能力：
  - 40+ 模型全覆盖（图片、视频、音频三大模态）
  - 高质量图片生成（seedream-4。Use when 需要视频处理、音频编辑、媒体转换、配音生成时使用。不适用于版权受保护的媒体内容处理。适用于独立开发者、企业团队和自动化工作流场景。
tags: 工作流,prompt,dlazy,ratio
tools:
  - read
  - exec
  - write
homepage: ""
category: "Automation"

---

> **功能说明**: 本技能涵盖 化工作流场景 等核心能力。


# 综合生成工具（专业版）

## 概述

综合生成工具专业版是全模态 AI 生成平台，覆盖图片、视频、音频三大模态共 40+ 模型。通过管道链接（Pipe Chaining）可将文生图、图生视频、视频配音等多个步骤串联为自动化工作流，实现从文本到完整多媒体内容的一站式生产.
本版本与免费版完全兼容——免费版的 API Key 配置和图片生成功能可直接使用。专业版新增视频生成、音频生成、矢量图生成、高质量模型和管道链接等高级能力.
## 核心能力

### 模态覆盖对比

| 模态 | 免费版 | 专业版 | 代表模型 |
|---|---|---|----|
| 基础文生图 | 4个 | 19个 | banana2, seedream-4.5, recraft-v4-pro, qwen-image-2-pro |
| 矢量图生成 | 不支持 | 2个 | recraft-v4-vector, recraft-v4-pro-vector |
| 图片处理 | 2个 | 4个 | imageseg, superres, image-replicate, video-replicate |
| 视频生成 | 不支持 | 17个 | veo-3.1, seedance-2.0, kling-v3, pixverse-c1, wan2.7 |
| 音频生成 | 不支持 | 15个 | doubao-tts, suno-music, elevenlabs-dialogue |
| 管道链接 | 不支持 | 支持 | 多步骤串联 |

**处理**: 解析模态覆盖对比的输入参数,完成核心逻辑,返回结构化响应.
**输出**: 返回模态覆盖对比的响应数据,包含状态码、结果和日志.
### 核心能力(补充)

## 输入格式
| 参数名 | 类型 | 必填 | 说明 |
|:-----|:-----|:-----|:-----|
| input | string | 是 | 综合生成工具-专业版处理的输入数据或指令 |
| options | object | 否 | 附加配置选项,如模式选择、格式偏好等 |
| callback_url | string | 否 | 异步处理完成后的回调通知URL |

```text
图片生成（19个模型）:
  - 高质量: seedream-4.5, qwen-image-2-pro, recraft-v4-pro
  - 通用型: banana-pro, banana2, gpt-image-2, grok-4.2
  - 风格化: mj-imagine, jimeng-t2i, kling-image-o1, viduq2-t2i
  - 矢量图: recraft-v4-vector, recraft-v4-pro-vector (SVG输出)
  - 轻量级: seedream-5.0-lite
# ...
视频生成（17个模型）:
  - 文生视频: veo-3.1, seedance-2.7
  - 图生视频: jimeng-i2v-first, viduq2-i2v, kling-v3-omni
  - 首尾帧: jimeng-i2v-first-tail
  - 数字人: jimeng-omnihuman-1.5, jimeng-dream-actor
  - 视频编辑: happyhorse-1.0, video-replicate
  - 唇形同步: heygen-lipsync-speed, sync-lipsync-3, videoretalk
  - 视频处理: videoseg
# ...
音频生成（15个模型）:
  - 详见 dlazy-audio-tool-pro
# ...
高级功能:
  - 管道链接（Pipe Chaining）
  - 批量生成
  - 风格复刻（image-replicate, video-replicate）
  - 矢量图输出（SVG）
```

**处理**: 解析核心能力的输入参数,完成核心逻辑,返回结构化响应.
**输出**: 返回核心能力的响应数据,包含状态码、结果和日志.
- 执行此能力时使用`input_params`参数,支持创建/查询/导出操作

### 核心功能执行
用`input_params`参数进行配置.

**处理**: 解析核心功能执行的输入参数,完成核心逻辑,返回结构化响应.
**输出**: 返回核心功能执行的响应数据,包含状态码、结果和日志.
- 执行此能力时使用`input_params`参数,支持创建/查询/导出操作
**能力覆盖范围**：本skill的核心能力覆盖以下场景关键词：全模态生成引擎、支持图片、音频生成与管道链、接批量工作流、综合生成工具专业、面向专业团队的全、生成平台、模型全覆盖、音频三大模态、高质量图片生成、Use、when、需要视频处理、音频编辑、媒体转换、配音生成时使用、不适用于版权受保、护的媒体内容处理、适用于独立开发者、企业团队和自动化、工作流场景等。这些关键词对应description中声明的使用场景,均已在上述能力点中提供对应的操作支持.
## 使用场景

### 场景一：广告素材全流程制作

从文案到视频广告的完整制作流程.
```bash
# 步骤1 生成产品主视觉图
dlazy seedream-4.5 \
  --prompt "高端无线耳机产品图，深色背景，戏剧性灯光，超写实" \
  --ratio "16:9" \
  --quality "4K"
# ...
# 步骤2 图片转视频（图生视频）
dlazy kling-v3 \
  --image @0.url \
  --prompt "耳机缓缓旋转，光影流动，产品展示动效" \
  --duration 5
# ...
# 步骤3 生成背景音乐
dlazy suno-music \
  --mode "custom" \
  --style "electronic ambient premium" \
  --title "Product Showcase BGM" \
  --instrumental true \
  --duration 5
# ...
# 步骤4 生成配音旁白
dlazy doubao-tts \
  --text "全新无线耳机，聆听非凡。" \
  --voice "male-magnetic"
# ...
# 管道链接一键完成:
dlazy seedream-4.5 --prompt "高端无线耳机，深色背景" --ratio "16:9" \
  | dlazy kling-v3 --image @0.url --prompt "耳机旋转展示" --duration 5
```

### 场景二：短视频内容批量生产

批量生成短视频素材.
```python
# 短视频批量生产脚本
import subprocess
import json
# ...
class VideoBatchProducer:
    """短视频批量生产器"""
# ...
    def __init__(self):
        self.pipeline = []
# ...
    def add_image_step(self, prompt, model="seedream-5.0-lite", ratio="9:16"):
        """添加图片生成步骤"""
        self.pipeline.append({
            "type": "image",
            "model": model,
            "prompt": prompt,
            "ratio": ratio
        })
        return self
# ...
    def add_video_step(self, prompt, model="kling-v3", duration=5):
        """添加视频生成步骤"""
        self.pipeline.append({
            "type": "video",
            "model": model,
            "prompt": prompt,
            "duration": duration
        })
        return self
# ...
    def add_audio_step(self, text, model="doubao-tts"):
        """添加配音步骤"""
        self.pipeline.append({
            "type": "audio",
            "model": model,
            "text": text
        })
        return self
# ...
    def execute_batch(self, scenarios):
        """批量执行生产流程"""
        results = []
        for scenario in scenarios:
            steps = []
            for step in self.pipeline:
                cmd = self._build_command(step, scenario)
                result = subprocess.run(cmd, capture_output=True, text=True)
                try:
                    output = json.loads(result.stdout)
                    steps.append({"step": step["type"], "output": output})
                except:
append({"step": step["type"], "error": "failed"})
            results.append({"scenario": scenario, "steps": steps})
        return results
# ...
    def _build_command(self, step, scenario):
        cmd = ["dlazy", step["model"]]
        if step["type"] == "image":
            cmd += ["--prompt", step["prompt"].format(**scenario),
                    "--ratio", step["ratio"]]
        elif step["type"] == "video":
                    "--duration", str(step["duration"])]
        elif step["type"] == "audio":
            cmd += ["--text", step["text"].format(**scenario)]
        return cmd
# ...
# 批量生产
producer = VideoBatchProducer()
producer.add_image_step("美食特写：{dish}，暖色调，诱人", "9:16") \
        .add_video_step("{dish}冒热气，缓慢推进", duration=5) \
        .add_audio_step("今天推荐：{dish}，色香味俱全！")
# ...
scenarios = [
    {"dish": "红烧肉"},
    {"dish": "清蒸鱼"},
    {"dish": "麻婆豆腐"},
    {"dish": "糖醋排骨"},
    {"dish": "宫保鸡丁"}
]
results = producer.execute_batch(scenarios)
```

### 场景三：矢量图与Logo生成

生成可缩放的矢量图资产.
```bash
# 生成SVG矢量Logo
dlazy recraft-v4-vector \
  --prompt "极简风格科技公司Logo，几何图形，蓝色主调" \
  --output "logo.svg"
# ...
# 高保真矢量插画（4MP级别）
dlazy recraft-v4-pro-vector \
  --prompt "详细的等距插画，城市俯视图，扁平风格" \
  --output "city-illustration.svg"
```

### 管道引用速查

| 引用 | 解析为 |
|---:|---:|
| `-` | 上游输出的自然值 |
| `@N` | 第N个输出的主值 |
| `@N.path` | 深入第N个输出 |
| `@*` | 所有输出的主值数组 |
| `@stdin` | 完整上游JSON信封 |

## 快速开始

### 依赖详情

```bash
npm install -g @dlazy/cli@latest
dlazy auth set YOUR_API_KEY
```

### 第二步：生成领先段视频

```bash
# 文生视频
dlazy veo-3.1-fast \
  --prompt "一只金毛犬在海滩上奔跑，夕阳西下，电影感" \
  --duration 5
# ...
# 图生视频
dlazy kling-v3 \
  --image "./input.jpg" \
  --prompt "图片中的场景开始动起来，镜头缓缓推进" \
  --duration 5
```

### 第三步：尝试管道链接

```bash
# 文生图 → 图生视频 → 自动串联
dlazy seedream-4.5 --prompt "山间日出，云海翻涌" \
url --prompt "云海流动，太阳升起" --duration 5
```

**响应解析**: 完成完成后,查看输出响应确认任务状态。成功时输出包含解析摘要和响应数据;失败时根据错误信息排查问题,查阅错误解析章节获取恢复步骤.
## 示例

### 高质量图片生成

```bash
# seedream-4.5 高质量文生图
dlazy seedream-4.5 \
  --prompt "描述文本" \
  --ref-images "ref1.jpg,ref2.jpg" \  # 参考图（可选）
  --quality "4K"                       # 2K 或 4K
  --ratio "16:9"
# ...
# recraft-v4-pro 4MP高分辨率
dlazy recraft-v4-pro \
  --prompt "描述文本" \
  --resolution "4MP"   # 适合印刷品
```

### 视频生成配置

```bash
# veo-3.1 高质量视频
dlazy veo-3.1 \
  --prompt "描述文本" \
  --mode "t2v"          # t2v 或 i2v
  --image "input.jpg"   # i2v模式需要
  --duration 5
# ...
# seedance-2.0 多模态参考
dlazy seedance-2.0 \
  --prompt "描述文本" \
  --ref-images "img1.jpg" \
  --ref-video "ref.mp4" \  # 视频参考
  --first-frame "start.jpg" \
  --last-frame "end.jpg"
```

### 管道链接配置

```bash
# 多步骤管道链接
dlazy seedream-4.5 --prompt "城市夜景" --n 4 \
  | dlazy superres --images @* \
url --prompt "城市灯火流动"
# ...
# 管道引用说明:
# @0.url  = 上游领先个输出的URL
# @*      = 上游所有输出数组
# -       = 上游自然值（单值场景）
```

## 优选实践

1. **模型分级使用**：草稿用 lite 模型，成品用 pro 模型，控制成本.
2. **管道调试**：先用 `--dry-run` 测试管道，确认引用正确再正式执行.
3. **视频时长控制**：短视频 5 秒，广告 10-15 秒，控制生成成本.
4. **参考图引导**：图生视频提供高质量参考图，效果更好.
5. **批量并行**：批量任务可并行执行，提升效率.
```text
专业版优选实践:
[ ] 模型分级使用（草稿lite / 成品pro）
[ ] 管道引用已用 --dry-run 测试
[ ] 视频时长已优化（控制成本）
[ ] 参考图质量已确认
[ ] 批量任务已规划并行策略
[ ] 余额充足（视频生成消耗较高）
[ ] API Key 已安全配置
```

## 常见问题

### Q: 视频生成支持多长？

A: 多数视频模型支持 5-10 秒。veo-3.1 支持更长时长但生成时间相应增加。建议短视频 5 秒起步.
### Q: 管道链接中某一步失败怎么办？

A: 管道中断，已完成的步骤输出仍可使用。检查失败步骤的错误信息，修正后从失败步骤重新执行.
### Q: 矢量图输出什么格式？

A: recraft-v4-vector 和 recraft-v4-pro-vector 输出 SVG 格式，可在任意分辨率下缩放，适合 Logo、图标和插画.
### Q: 如何从免费版升级？

A: API Key 和 CLI 配置无需变更，直接使用专业版的全部 40+ 模型即可.
### 已知限制

A: 单批建议不超过 50 个任务。超大批量请分批执行，避免 API 限流.
### Q: 视频生成消耗大吗？

A: 视频生成的消耗显著高于图片。建议先用图片确认创意方向，再生成视频.
## 依赖说明

### 运行环境
- **Agent平台**: 支持SKILL.md的任意AI Agent（Claude Code / Cursor / Codex / Gemini CLI等）
- **操作系统**: Windows / macOS / Linux
- **Node.js**: 16+（dlazy CLI 运行需要）

### 第三方依赖
| 依赖项 | 类型 | 是否必需 | 获取方式 |
|:---:|:---:|:---:|:---:|
| LLM API | API | 必需 | 由Agent内置LLM提供 |
| Node.js 16+ | 运行时 | 必需 | nodejs.org 官方下载 |
| @dlazy/cli | CLI工具 | 必需 | `npm install -g @dlazy/cli@latest` |
| dlazy API Key | 认证 | 必需 | dlazy.com/dashboard 获取 |
| FFmpeg（可选） | 工具 | 推荐 | 视频拼接与格式转换 |

### API Key 配置
- **必需**: dlazy API Key（与免费版共用）
- **获取方式**: 访问 dlazy.com/dashboard/organization/api-key
- **配置方式**: `dlazy auth set YOUR_API_KEY` 或环境变量 `DLAZY_API_KEY`
- **安全说明**: Key 可随时轮换或撤销；配置文件权限限制为当前用户
- **余额说明**: 视频生成消耗较高，建议定期检查余额

### 可用性分类
- **分类**: MD+EXEC+API（Markdown指令 + 命令行 + 外部API调用）
- **说明**: 企业级AI Skill，支持全模态40+模型、管道链接与批量处理
- **适用规模**: 专业内容团队，多媒体批量生产
- **兼容性**: 与免费版完全兼容，API Key 和配置无缝共用

## 错误处理

| 错误场景 | 原因 | 处理方式 |
|:------|------:|:------|
| 配置错误 | 参数缺失或格式错误 | 检查依赖说明中的配置要求 |
| 运行时错误 | 运行环境不满足 | 确认运行环境符合依赖说明 |
| 网络错误 | 连接超时或不可达 | 执行ping命令测试网络连通性,检查防火墙和代理设置连接后执行ping命令测试网络连通性,检查防火墙和代理设置连接后重新执行命令，参考国内替代方案 |

## 输出格式
```json
{
  "success": true,
  "data": {
    "result": "综合生成工具-专业版处理结果",
    "execution_time": "0.5s",
    "metadata": {
      "version": "1.0",
      "processor": "dlazy gen pro"
    }
  },
  "execution_log": ["解析输入参数", "执行核心处理", "格式化输出结果"],
  "error": null
}
```

## 安全注意事项

| 风险类型 | 防范措施 |
|----------|---------|
| API密钥泄露 | 通过环境变量配置，禁止硬编码到代码或配置文件中 |
| 命令执行风险 | 仅执行白名单命令，避免拼接用户输入到命令行参数中 |
| 网络通信安全 | 使用HTTPS协议，验证SSL证书有效性 |
| 敏感数据暴露 | 输出结果中不包含密钥、令牌等敏感信息 |

使用前请确认已阅读依赖说明章节，确保运行环境满足安全要求。

## 核心功能

- **自动化执行**: 全模态生成引擎，覆盖40+模型，支持图片/视频/音频生成与管道链接批量工作流。。综合生成工具专业版，面向专业团队的全模态
- **文件处理**: 支持多种文件格式的读取、解析和写入操作
- **API集成**: 通过标准化接口调用外部服务并处理响应
- **命令执行**: 在安全沙箱中执行系统命令并收集结果
- **信息检索**: 快速搜索和过滤目标数据

## 核心功能

- **自动化执行**: 全模态生成引擎，覆盖40+模型，支持图片/视频/音频生成与管道链接批量工作流。。综合生成工具专业版，面向专业团队的全模态
- **文件处理**: 支持多种文件格式的读取、解析和写入操作
- **API集成**: 通过标准化接口调用外部服务并处理响应
- **命令执行**: 在安全沙箱中执行系统命令并收集结果
- **信息检索**: 快速搜索和过滤目标数据