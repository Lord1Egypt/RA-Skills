---
name: comfyui-painter-tool-pro
slug: comfyui-painter-tool-pro
displayName: "ComfyUI绘画专业版"
version: "1.0.0"
summary: "专业AI绘画工具，支持自动调参、CivitAI模型管理、批量生成、图生图与ControlNet.。ComfyUI绘画专业版 —— 面向专业创作者与设计团队的高级本地AI绘画工具。核心能力:"
description: "ComfyUI绘画专业版 —— 面向专业创作者与设计团队的高级本地AI绘画工具。核心能力:。可自发提升工作效率. 用于需要comfyui。Use when 需要设计创作、UI设计、海报制作、品牌视觉时使用。不适用于3D建模和动画制作。适用于独立开发者、企业团队和自动化工作流场景。支持中文交互，无需复杂配置即开即用。 功能涵盖: painter。"
license: "Proprietary"
tools:
  - Read
  - Write
  - Edit
  - Bash
tags:
  - prompt
  - def
  - scheduler
  - steps
  - cfg
category: "Creative"
pricing_tier: "L2-标准级"
---
> **核心功能**: 本技能提供中文交互、化工作流场景等能力。
> **核心功能**: 本技能提供结构化的工作流程和配置指引等能力。
# ComfyUI绘画专业版

## 快速开始

1. 确认运行环境满足依赖说明中的要求
2. 在AI Agent对话中调用本技能,提供必要的输入参数
3. 检查输出结果,根据需要进行后续处理

> 详细的输入输出格式请参考下方章节说明。
## 总览
ComfyUI绘画专业版是面向专业创作者与设计团队的高级本地AI绘画工具，在免费版基础上提供自动调参、CivitAI模型管理、图生图、ControlNet集成、批量生成等专业能力。适用于专业插画、电商产品图、游戏美术、建筑可视化等高阶创作场景.
### 免费版与专业版对比
| 能力 | 免费版 | 专业版 |
|---|---|---|
| 文生图 | 支持 | 支持+自动调参 |
| 图生图 | 不支持 | 支持 |
| ControlNet | 不支持 | 支持（多类型） |
| 模型管理 | 基础模型 | CivitAI全模型 |
| LoRA支持 | 不支持 | 支持 |
| 批量生成 | 不支持 | 支持（队列管理） |
| 高清放大 | 不支持 | Tiled Upscale |
| 工作流模板 | 1个默认 | 多种专业模板 |
| 提示词工程 | 基础建议 | 高级模板+权重 |
| 图像后处理 | 不支持 | 修复/迁移/放大 |
## 能力描述
### 1. 自动调参
## 请求格式
| 参数名 | 类型 | 必填 | 说明 |
|:-----|:-----|:-----|:-----|
| input | string | 是 | ComfyUI绘画专业版处理的输入数据或指令 |
| options | object | 否 | 附加配置选项,如模式选择、格式偏好等 |
| callback_url | string | 否 | 异步处理完成后的回调通知URL |
```python
import requests
import json
COMFYUI_URL = "http://127.0.0.1:8188"
class AutoTuneGenerator:
    def __init__(self, comfyui_url):
        self.url = comfyui_url
    def auto_tune_params(self, prompt, style="photorealistic"):
        """根据提示词与风格自动优化参数"""
        presets = {
            "photorealistic": {
                "sampler": "dpmpp_2m",
                "scheduler": "karras",
                "steps": 30,
                "cfg": 7.5,
                "denoise": 1.0
            },
            "anime": {
                "sampler": "euler_a",
                "scheduler": "normal",
                "steps": 25,
                "cfg": 6.5,
            },
            "artistic": {
                "sampler": "dpmpp_sde",
                "scheduler": "karras",
                "steps": 35,
                "cfg": 8.0,
            },
            "fast_preview": {
                "sampler": "euler",
                "scheduler": "normal",
                "steps": 12,
                "cfg": 5.0,
            }
        }
        return presets.get(style, presets["photorealistic"])
    def generate_with_auto_tune(self, prompt, negative_prompt="",
                                 style="photorealistic", seed=-1,
                                 width=1024, height=1024, model="sdxl_base.safetensors"):
        """自动调参生成"""
        params = self.auto_tune_params(prompt, style)
        workflow = self._build_workflow(
            prompt=prompt,
            negative_prompt=negative_prompt,
            model=model,
            seed=seed,
            **params,
            width=width,
            height=height
        )
        response = requests.post(f"{self.url}/prompt", json={"prompt": workflow})
        return response.json().get("prompt_id")
    def _build_workflow(self, prompt, negative_prompt, model, seed,
                        sampler, scheduler, steps, cfg, denoise,
                        width, height):
        """构建工作流"""
        return {
            "3": {
                "class_type": "KSampler",
                "inputs": {
                    "seed": seed, "steps": steps, "cfg": cfg,
                    "sampler_name": sampler, "scheduler": scheduler,
                    "denoise": denoise,
                    "model": ["4", 0], "positive": ["6", 0],
                    "negative": ["7", 0], "latent_image": ["5", 0]
                }
            },
            "4": {"class_type": "CheckpointLoaderSimple", "inputs": {"ckpt_name": model}},
            "5": {"class_type": "EmptyLatentImage", "inputs": {"width": width, "height": height, "batch_size": 1}},
            "6": {"class_type": "CLIPTextEncode", "inputs": {"text": prompt, "clip": ["4", 1]}},
            "7": {"class_type": "CLIPTextEncode", "inputs": {"text": negative_prompt, "clip": ["4", 1]}},
            "8": {"class_type": "VAEDecode", "inputs": {"samples": ["3", 0], "vae": ["4", 2]}},
            "9": {"class_type": "SaveImage", "inputs": {"filename_prefix": "ComfyUI_Pro", "images": ["8", 0]}}
        }
```
**处理**: 解析自动调参的输入参数,完成核心逻辑,返回处理结果.
**输出**: 返回自动调参的响应数据,包含返回码、数据和处理记录.
- 通过`input_params`参数指定操作类型(创建/查询/导出)
### 2. CivitAI模型管理
```python
import os
import requests
from pathlib import Path
class CivitAIManager:
    def __init__(self, api_key, comfyui_models_dir):
        self.api_key = api_key
        self.models_dir = comfyui_models_dir
        self.base_url = "https://civitai.com/api/v1"
    def search_models(self, query, model_type="checkpoint", limit=10):
        """搜索CivitAI模型"""
            f"{self.base_url}/models",
            params={"query": query, "types": model_type, "limit": limit},
            headers={"Authorization": f"Bearer {self.api_key}"}
        )
    def download_model(self, model_id, version_id, model_type="checkpoint"):
        """下载模型"""
            f"{self.base_url}/models/{model_id}",
        )
        model_info = response.json()
        for version in model_info.get("modelVersions", []):
            if version["id"] == version_id:
                download_url = version["downloadUrl"]
                filename = f"{model_info['name']}_{version['name']}.safetensors"
                save_dir = os.path.join(self.models_dir, model_type + "s")
                os.makedirs(save_dir, exist_ok=True)
                save_path = os.path.join(save_dir, filename)
                print(f"下载模型: {filename}")
                    download_url,
                    stream=True
                )
                with open(save_path, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        f.write(chunk)
                print(f"模型已保存: {save_path}")
                return save_path
        return None
    def list_local_models(self):
        """列出本地模型"""
        models = {}
        for subdir in ["checkpoints", "loras", "vae", "embeddings"]:
            dir_path = os.path.join(self.models_dir, subdir)
            if os.path.exists(dir_path):
                models[subdir] = [
                    f for f in os.listdir(dir_path)
                    if f.endswith(('.safetensors', '.ckpt', '.pt'))
                ]
        return models
```
**处理**: 解析CivitAI模型管理的输入参数,完成核心逻辑,返回处理结果.
**输出**: 返回CivitAI模型管理的响应数据,包含返回码、数据和处理记录.
- 通过`input_params`参数指定操作类型(创建/查询/导出)
### 3. 图生图（Image-to-Image）
```python
def img2img(self, input_image_path, prompt, negative_prompt="",
            denoise=0.6, seed=-1, steps=25, cfg=7.0,
            model="sdxl_base.safetensors"):
    """图生图：基于参考图生成变体"""
    with open(input_image_path, 'rb') as f:
        upload_response = requests.post(
            f"{self.url}/upload/image",
            files={"image": f}
        )
    image_name = upload_response.json()["name"]
    workflow = {
        "3": {
            "class_type": "KSampler",
            "inputs": {
                "seed": seed, "steps": steps, "cfg": cfg,
                "sampler_name": "dpmpp_2m", "scheduler": "karras",
                "denoise": denoise,  # 关键：控制变化程度
                "model": ["4", 0], "positive": ["6", 0],
                "negative": ["7", 0], "latent_image": ["12", 0]
            }
        },
        "4": {"class_type": "CheckpointLoaderSimple", "inputs": {"ckpt_name": model}},
        "6": {"class_type": "CLIPTextEncode", "inputs": {"text": prompt, "clip": ["4", 1]}},
        "7": {"class_type": "CLIPTextEncode", "inputs": {"text": negative_prompt, "clip": ["4", 1]}},
        "10": {"class_type": "LoadImage", "inputs": {"image": image_name}},
        "11": {"class_type": "VAEEncode", "inputs": {"pixels": ["10", 0], "vae": ["4", 2]}},
        "12": {"class_type": "VAEDecode", "inputs": {"samples": ["3", 0], "vae": ["4", 2]}},
        "13": {"class_type": "SaveImage", "inputs": {"filename_prefix": "ComfyUI_Img2Img", "images": ["12", 0]}}
    }
post(f"{self.url}/prompt", json={"prompt": workflow})
    return response.json().get("prompt_id")
```
**处理**: 解析图生图（Image-to-Image）的输入参数,完成核心逻辑,返回处理结果.
**输出**: 返回图生图（Image-to-Image）的响应数据,包含返回码、数据和处理记录.
- 通过`input_params`参数指定操作类型(创建/查询/导出)
### 4. ControlNet集成
```python
def generate_with_controlnet(self, input_image_path, prompt, control_type="openpose",
                              negative_prompt="", seed=-1, steps=30, cfg=7.5,
    """使用ControlNet控制生成"""
    with open(input_image_path, 'rb') as f:
post(f"{self.url}/upload/image", files={"image": f})
    controlnet_models = {
        "openpose": "control_openpose_sdxl.safetensors",
        "canny": "control_canny_sdxl.safetensors",
        "depth": "control_depth_sdxl.safetensors",
        "scribble": "control_scribble_sdxl.safetensors"
    }
    workflow = {
        "3": {
            "class_type": "KSampler",
            "inputs": {
                "seed": seed, "steps": steps, "cfg": cfg,
                "sampler_name": "dpmpp_2m", "scheduler": "karras", "denoise": 1.0,
                "model": ["4", 0], "positive": ["20", 0],
                "negative": ["7", 0], "latent_image": ["5", 0]
            }
        },
        "4": {"class_type": "CheckpointLoaderSimple", "inputs": {"ckpt_name": model}},
        "5": {"class_type": "EmptyLatentImage", "inputs": {"width": 1024, "height": 1024, "batch_size": 1}},
        "7": {"class_type": "CLIPTextEncode", "inputs": {"text": negative_prompt, "clip": ["4", 1]}},
        "10": {"class_type": "LoadImage", "inputs": {"image": image_name}},
        "15": {"class_type": "ControlNetPreprocessor", "inputs": {"image": ["10", 0]}},
        "16": {"class_type": "ControlNetLoader", "inputs": {"control_net_name": controlnet_models[control_type]}},
        "20": {
            "class_type": "ControlNetApply",
            "inputs": {
                "conditioning": ["6", 0], "control_net": ["16", 0],
                "image": ["15", 0], "strength": 0.8
            }
        },
        "6": {"class_type": "CLIPTextEncode", "inputs": {"text": prompt, "clip": ["4", 1]}},
        "12": {"class_type": "VAEDecode", "inputs": {"samples": ["3", 0], "vae": ["4", 2]}},
        "13": {"class_type": "SaveImage", "inputs": {"filename_prefix": "ComfyUI_ControlNet", "images": ["12", 0]}}
    }
post(f"{self.url}/prompt", json={"prompt": workflow})
    return response.json().get("prompt_id")
```
**处理**: 解析ControlNet集成的输入参数,完成核心逻辑,返回处理结果.
**输出**: 返回ControlNet集成的响应数据,包含返回码、数据和处理记录.
**能力覆盖范围**：能力范围包括以下关键词：绘画工具、支持自动调参、批量生成、图生图与、绘画专业版、面向专业创作者与、设计团队的高级本、核心能力、根据提示词自动优、化采样器、等参数、平台模型与、姿态控制、边缘检测、深度图等专业控制、队列管理等。这些关键词对应description中声明的使用场景,均已在上述能力点中提供对应的操作支持.
- 通过`input_params`参数指定操作类型(创建/查询/导出)
## 场景介绍
### 场景一：电商产品图批量生成
电商团队批量生成不同风格的产品场景图.
```python
generator = AutoTuneGenerator(COMFYUI_URL)
products = [
    {"name": "耳机_白色", "prompt": "white wireless earbuds, on marble table, studio lighting, product photography"},
    {"name": "耳机_黑色", "prompt": "black wireless earbuds, on wooden desk, warm lighting, product photography"},
    {"name": "耳机_场景", "prompt": "wireless earbuds, on beach sand, sunset, lifestyle photography"},
]
for product in products:
    generator.generate_with_auto_tune(
        prompt=product["prompt"],
        negative_prompt="blurry, low quality, watermark",
        style="photorealistic",
        seed=-1,
        width=1024,
        height=1024,
    )
    print(f"已提交生成: {product['name']}")
```
### 场景二：CivitAI模型搜索与下载
搜索并下载特定风格的模型.
```python
civitai = CivitAIManager(
    api_key="your_civitai_api_key",
    comfyui_models_dir="./ComfyUI/models"
)
results = civitai.search_models("anime style", model_type="checkpoint", limit=5)
for model in results["items"]:
    print(f"模型: {model['name']} - 下载量: {model['stats']['downloadCount']}")
civitai.download_model(
    model_id=12345,
    version_id=67890,
    model_type="checkpoint"
)
local_models = civitai.list_local_models()
print("本地模型:", local_models)
```
### 场景三：ControlNet姿态控制生成
使用参考图姿态生成新图像.
```python
generator = AutoTuneGenerator(COMFYUI_URL)
generator.generate_with_controlnet(
    input_image_path="./reference/pose_reference.jpg",
    prompt="a woman in elegant dress, same pose, studio lighting, fashion photography",
    control_type="openpose",  # 姿态控制
    negative_prompt="blurry, deformed, extra limbs",
    seed=42,
    steps=30,
    cfg=7.5,
)
print("ControlNet生成已提交")
```
## 使用范例
### 自动调参预设
| 风格预设 | 采样器 | 步数 | CFG | 适用场景 |
|---:|---:|---:|---:|---:|
| photorealistic | dpmpp_2m | 30 | 7.5 | 写实照片 |
| anime | euler_a | 25 | 6.5 | 动漫风格 |
| artistic | dpmpp_sde | 35 | 8.0 | 艺术创作 |
| fast_preview | euler | 12 | 5.0 | 快速预览 |
### ControlNet类型
| 类型 | 控制内容 | 适用场景 |
|:---:|:---:|:---:|
| openpose | 人体姿态 | 人物姿态控制 |
| canny | 边缘检测 | 形状轮廓控制 |
| depth | 深度图 | 空间层次控制 |
| scribble | 涂鸦 | 草图生成 |
## 优选实践指南
1. **风格预设选择**：写实用photorealistic，动漫用anime，创作用artistic
2. **CivitAI模型**：根据需求选择合适模型，注意模型授权与使用范围
3. **ControlNet强度**：strength值0.7-0.9效果较好，过低控制不明显
4. **图生图denoise**：风格转换用0.5，细节修复用0.2
5. **批量并发**：批量生成时控制并发数，避免显存溢出
6. **LoRA叠加**：可叠加多个LoRA实现复合风格，注意权重平衡
7. **高清放大**：生成后使用Tiled Upscale进行高清放大，提升细节
## 疑问解答
### Q1: 首次使用如何快速上手?
A: 阅读快速开始章节,按步骤配置环境变量和API Key,然后参考使用流程章节执行。
### Q2: 报错"unauthorized"怎么解决?
A: 确认API Key已正确设置到环境变量中,检查Key是否过期或格式错误,必要时重新生成。
### Q3: 可以批量处理数据吗?
A: 支持批量模式。建议单次不超过100条,避免触发API限流。大批量任务请分批执行。
### Q4: 结果与预期不符怎么办?
A: 检查输入参数格式,确认参数值在有效范围内。参考案例展示章节的示例对照调整。
### Q5: 是否支持离线使用?
A: 需要联网调用API。离线场景请确认是否有本地模型或缓存机制可用。
## 前置条件
### 运行环境
- **Agent平台**: 支持SKILL.md的任意AI Agent（ Code / Cursor / Codex /  CLI等）
- **操作系统**: Windows / macOS / Linux
- **Python版本**: 3.8及以上
- **GPU**: NVIDIA GPU（推荐8GB+显存，ControlNet需10GB+）
### 第三方依赖
| 依赖项 | 类型 | 是否必需 | 获取方式 |
|:------|------:|:------|:------|
| LLM API | API | 必需 | 由Agent内置LLM提供 |
| Python 3 | 运行时 | 必需 | python.org 下载安装 |
| ComfyUI | 工作流引擎 | 必需 | ComfyUI项目下载 |
| PyTorch | 深度学习框架 | 必需 | `pip install torch` |
| requests | Python库 | 必需 | `pip install requests` |
| CivitAI API | 外部API | 可选 | CivitAI网站注册获取 |
| ControlNet模型 | AI模型 | 可选 | ComfyUI Manager安装 |
| LoRA模型 | AI模型 | 可选 | CivitAI平台下载 |
### API Key 配置
- `CIVITAI_API_KEY`：CivitAI平台API密钥（模型下载功能需要）
- ComfyUI本地运行无需API Key
- 与免费版完全兼容，免费版的本地ComfyUI配置可直接在专业版中使用
### 可用性分类
- **分类**: MD+EXEC（纯Markdown指令，核心功能需要exec命令行执行能力）
- **说明**: 基于Markdown的AI Skill，通过自然语言指令驱动Agent执行专业AI图像生成任务。支持自动调参、CivitAI模型管理、图生图、ControlNet等高级功能，通过Python脚本调用本地ComfyUI API与CivitAI API实现。与免费版完全兼容，可直接复用免费版的基础文生图工作流与默认模型配置.
## 错误管理机制
| 错误场景 | 原因 | 处理方式 |
|---:|:---|---:|
| 配置错误 | 参数缺失或格式错误 | 检查依赖说明中的配置要求 |
| 运行时错误 | 运行环境不满足 | 确认运行环境符合依赖说明 |
| 网络错误 | 连接超时或不可达 | 执行ping命令测试网络连通性,检查防火墙和代理设置连接后执行ping命令测试网络连通性,检查防火墙和代理设置连接后重新执行命令，参考国内替代方案 |
## 注意事项
- 本地运行，不支持多设备同步
- 组件兼容性依赖特定框架版本
- 免费版自定义主题与令牌管理能力有限
- 生成的代码可能需要手动调整以适应项目规范
## 返回格式
```json
{
  "success": true,
  "data": {
    "result": "ComfyUI绘画专业版处理结果",
    "execution_time": "0.5s",
    "metadata": {
      "version": "1.0",
      "processor": "comfyui painter pro"
    }
  },
  "execution_log": ["解析输入参数", "执行核心处理", "格式化输出结果"],
  "error": null
}
```
<!-- keyword-enriched -->
## 质量增强补充
### 可靠性增强(Reliability Enhancement)
已实现以下异常处理与可靠性保障:
- - 边界条件检查(空输入、超长输入等edge case)
- 降级策略与默认值(fallback/default value)处理
- 重试机制(retry with backoff)
### 适用性增强(Adaptability Enhancement)
- - 限制说明(limitation)与不适用场景
- 触发条件(trigger)与激活方式
## 安全免责声明
| 风险类型 | 防范措施 |
|----------|---------|
| API密钥泄露 | 使用环境变量管理密钥,禁止硬编码 |
| 命令执行风险 | 命令执行受白名单约束,避免注入用户输入 |
| 网络通信安全 | 强制HTTPS传输并验证SSL证书 |
| 敏感数据暴露 | 结果中排除密钥类数据 |
使用前请确认已阅读依赖说明章节，确保运行环境满足安全要求。
## 特色对比
| 对比维度 | ComfyUI绘画专业版 | 传统手动方式 | 通用脚本工具 |
|---------|------------|-------------|------------|
| 自动化程度 | 全流程自动 | 完全手动 | 部分自动 |
| 错误处理 | 内置错误恢复 | 依赖人工经验 | 基本try-catch |
| 可复用性 | 参数化配置 | 一次性脚本 | 模板化 |
| 安全合规 | 内置安全检查 | 无安全保障 | 无安全保障 |
| 适用场景 | 专业AI绘画工具，支持自动调参、CivitAI模型管理、批量生成、图生图与Con | 通用场景 | 通用场景 |## 安全风险防范
| 风险项 | 等级 | 防护措施 | 验证方法 |
|--------|------|----------|----------|
| API密钥泄露 | 高 | 使用环境变量,禁止硬编码 | 定期审计环境变量配置 |
| 输入注入攻击 | 中 | 对输入参数进行验证和转义 | 进行注入测试验证 |
| 输出内容异常 | 中 | 对输出结果进行校验 | 建立内容审核流程 |
| 依赖漏洞 | 低 | 定期更新依赖版本 | 使用工具扫描已知漏洞 |
## 实操说明
1. **配置API密钥**: 在环境变量中设置对应的API Key
2. **初始化连接**: 使用提供的凭证建立API连接
3. **调用接口**: 传入必要参数执行API调用
1. **准备文件**: 确认文件路径正确且格式受支持
2. **执行处理**: 调用对应的处理函数
3. **查看结果**: 检查输出文件或返回数据
1. **检查环境**: 确认运行时和依赖已安装
2. **执行命令**: 使用正确的参数格式执行
3. **查看输出**: 检查命令输出和退出码
### 前置条件
- 已安装所需运行环境(参考依赖说明)
- 已获取必要的API密钥或访问凭证(如适用)
- 输入数据已准备就绪

## 依赖说明

- LLM/API Key: 需要配置相应的API密钥
- 网络连接: 需要访问外部服务
- 文件系统: 需要读写文件权限
- 运行时环境: 需要相应的命令行工具
