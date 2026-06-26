# Atlas Cloud API 详细文档

本文档提供 Atlas Cloud API 的完整参考，包括所有用于"随手拍广告"工作流的 API 端点。

## API 基础信息

### Base URLs

| 用途 | Base URL |
|-----|----------|
| LLM / 对话补全 | `https://api.atlascloud.ai/v1` |
| 图像 / 视频生成 | `https://api.atlascloud.ai/api/v1` |

### 认证

所有 API 请求需要在 Header 中包含 API Key：

```
Authorization: Bearer your-api-key
```

## 1. 媒体文件上传 API

### Endpoint

```
POST https://api.atlascloud.ai/api/v1/model/uploadMedia
```

### 请求格式

使用 `multipart/form-data` 上传文件：

```python
import requests

def upload_media(file_path: str, api_key: str) -> str:
    """
    上传本地文件到 Atlas Cloud 获取临时 URL
    
    Args:
        file_path: 本地文件路径
        api_key: Atlas Cloud API Key
        
    Returns:
        临时文件 URL
    """
    response = requests.post(
        "https://api.atlascloud.ai/api/v1/model/uploadMedia",
        headers={"Authorization": f"Bearer {api_key}"},
        files={"file": open(file_path, "rb")}
    )
    
    if response.status_code != 200:
        raise Exception(f"上传失败: {response.text}")
    
    result = response.json()
    return result.get("url")
```

### 支持的文件格式

| 类型 | 支持格式 |
|-----|---------|
| 图片 | JPEG, PNG, WEBP, GIF |
| 视频 | MP4, MOV, AVI |
| 音频 | MP3, WAV, M4A |

### 返回示例

```json
{
    "url": "https://static.atlascloud.ai/uploads/xxxxx.jpg",
    "size": 1234567,
    "mimeType": "image/jpeg"
}
```

## 2. Nano Banana 2 Edit API（图像编辑/抠图）

### Endpoint

```
POST https://api.atlascloud.ai/api/v1/model/generateImage
```

### 模型信息

- **模型名称**: `google/nano-banana-2/edit`
- **别名**: Gemini 3.1 Flash Image
- **提供商**: Google DeepMind
- **特点**: 
  - 3-5x 快于 Pro 版本（4-8秒标准生成）
  - 近 Pro 级质量（~95%）
  - 支持高达 4K 分辨率
  - 智能背景移除和编辑

### 请求参数

| 参数 | 类型 | 必填 | 说明 |
|-----|------|-----|------|
| model | string | 是 | `google/nano-banana-2/edit` |
| prompt | string | 是 | 编辑指令 |
| image_url | string | 是 | 输入图片的 URL |
| aspect_ratio | string | 否 | 宽高比，默认保持原图 |
| output_format | string | 否 | `jpeg` / `png`（推荐 png 保留透明） |

### 抠图示例代码

```python
import requests
import time

def remove_background_and_white_bg(image_url: str, api_key: str) -> str:
    """
    使用 Nano Banana 2 Edit 去除背景并添加白底
    
    Args:
        image_url: 输入图片 URL
        api_key: Atlas Cloud API Key
        
    Returns:
        处理后的图片 URL
    """
    # 提交生成任务
    response = requests.post(
        "https://api.atlascloud.ai/api/v1/model/generateImage",
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        },
        json={
            "model": "google/nano-banana-2/edit",
            "prompt": """Remove the background completely and precisely. 
Place the product on a pure white (#FFFFFF) background. 
Keep the product crisp and sharp with professional studio lighting. 
Maintain all product details, textures, colors, and proportions perfectly. 
Add subtle soft shadows underneath for depth.""",
            "image_url": image_url,
            "output_format": "png"  # 保留透明度信息
        }
    )
    
    if response.status_code != 200:
        raise Exception(f"请求失败: {response.text}")
    
    prediction_id = response.json().get("predictionId")
    
    # 轮询获取结果
    return poll_for_result(prediction_id, api_key)


def poll_for_result(prediction_id: str, api_key: str, timeout: int = 120) -> str:
    """
    轮询获取生成结果
    
    Args:
        prediction_id: 任务 ID
        api_key: API Key
        timeout: 超时时间（秒）
        
    Returns:
        输出 URL
    """
    start_time = time.time()
    
    while time.time() - start_time < timeout:
        response = requests.get(
            f"https://api.atlascloud.ai/api/v1/model/getResult?predictionId={prediction_id}",
            headers={"Authorization": f"Bearer {api_key}"}
        )
        
        result = response.json()
        status = result.get("status")
        
        if status == "completed":
            return result.get("output")
        elif status == "failed":
            raise Exception(f"生成失败: {result.get('error')}")
        
        # 图像生成通常 4-8 秒
        time.sleep(2)
    
    raise TimeoutError("生成超时")
```

## 3. LLM API（文案生成）

### Endpoint

```
POST https://api.atlascloud.ai/v1/chat/completions
```

### 推荐模型

| 模型 | 用途 | 特点 |
|-----|------|------|
| `zai-org/glm-5-turbo` | 产品分析 + 分镜脚本 | **推荐使用**，支持视觉输入 |
| `deepseek-v3` | 纯文本文案优化 | 高性价比，强推理能力 |
| `qwen-max` | 中文文案 | 优秀的中文表达能力 |

**⚠️ 注意：Atlas Cloud 没有 Gemini 模型，请使用 `zai-org/glm-5-turbo` 替代！**

### 使用 OpenAI SDK

```python
from openai import OpenAI

def analyze_product_and_generate_copy(
    image_url: str,
    api_key: str,
    style: str = "高端奢华风"
) -> dict:
    """
    分析产品图片并生成广告文案
    
    Args:
        image_url: 产品白底图 URL
        api_key: Atlas Cloud API Key
        style: 文案风格
        
    Returns:
        包含 slogan、解说词、视频提示词的字典
    """
    client = OpenAI(
        api_key=api_key,
        base_url="https://api.atlascloud.ai/v1"
    )
    
    system_prompt = f"""你是一位顶级广告创意总监，拥有20年的高端品牌广告经验。
请仔细分析产品图片，理解产品的：
1. 品类和用途
2. 设计特点和工艺细节
3. 目标受众
4. 核心卖点

然后生成以下内容：

1. SLOGAN（不超过10个字）
   - 简短有力，朗朗上口
   - 能触动目标受众的情感

2. 解说词（30-50字，适合8秒视频配音）
   - 节奏感强，适合朗读
   - 突出产品核心价值
   - 引发购买欲望

3. 视频画面描述（英文，用于 Veo 3.1 视频生成提示词）
   - 描述产品如何在画面中展示
   - 包含摄像机运动（pan, tilt, dolly, zoom）
   - 描述灯光、氛围

风格要求：{style}

输出格式（严格按此格式）：
SLOGAN: [你的Slogan]
解说词: [你的解说词]
画面描述: [英文，用于视频生成]"""

    response = client.chat.completions.create(
        model="zai-org/glm-5-turbo",  # 注意：不是 gemini！
        messages=[
            {"role": "system", "content": system_prompt},
            {
                "role": "user",
                "content": [
                    {
                        "type": "image_url",
                        "image_url": {"url": image_url}
                    },
                    {
                        "type": "text",
                        "text": "请分析这个产品并生成高端广告文案"
                    }
                ]
            }
        ],
        max_tokens=1024,
        temperature=0.8  # 稍高温度增加创意性
    )
    
    content = response.choices[0].message.content
    
    # 解析输出
    result = {}
    for line in content.split('\n'):
        if line.startswith('SLOGAN:'):
            result['slogan'] = line.replace('SLOGAN:', '').strip()
        elif line.startswith('解说词:'):
            result['narration'] = line.replace('解说词:', '').strip()
        elif line.startswith('画面描述:'):
            result['video_prompt'] = line.replace('画面描述:', '').strip()
    
    return result
```

## 4. Veo 3.1 视频生成 API

### Endpoint

```
POST https://api.atlascloud.ai/api/v1/model/generateVideo
```

### 模型信息

- **模型名称**: `google/veo3.1/image-to-video`（Image-to-Video）
- **提供商**: Google DeepMind
- **特点**:
  - 电影级画质
  - 支持 720p/1080p
  - 原生音频支持
  - 4/6/8秒时长选择

### 定价

| 模式 | 价格 |
|-----|------|
| 视频 + 音频 | $0.40/秒 |
| 仅视频 | $0.20/秒 |

**8秒视频参考价格**: ~$1.60（仅视频）/ ~$3.20（含音频）

### 请求参数

| 参数 | 类型 | 必填 | 说明 |
|-----|------|-----|------|
| model | string | 是 | `google/veo3.1/image-to-video` |
| prompt | string | 是 | 视频动态描述（英文效果更佳） |
| image_url | string | 是 | 起始帧图片 URL |
| durationSeconds | int | 否 | 时长：4/6/8，默认 8 |
| resolution | string | 否 | `720p` / `1080p`，默认 1080p |
| aspectRatio | string | 否 | `16:9`（横屏）/ `9:16`（竖屏） |
| withAudio | boolean | 否 | 是否生成配套音频 |
| seed | int | 否 | 随机种子（可复现结果） |

### 完整示例代码

```python
import requests
import time

def generate_ad_video(
    image_url: str,
    prompt: str,
    api_key: str,
    duration: int = 8,
    aspect_ratio: str = "16:9",
    with_audio: bool = True
) -> str:
    """
    使用 Veo 3.1 生成广告视频
    
    Args:
        image_url: 产品白底图 URL
        prompt: 视频动态描述（英文）
        api_key: Atlas Cloud API Key
        duration: 视频时长（4/6/8秒）
        aspect_ratio: 宽高比（16:9 横屏 / 9:16 竖屏）
        with_audio: 是否生成配套音频
        
    Returns:
        生成的视频 URL
    """
    # 构建完整的视频提示词
    full_prompt = f"""Cinematic product advertisement video.
{prompt}

Technical requirements:
- Professional studio lighting with soft diffused key light
- Subtle product rotation or camera movement
- Premium advertising aesthetic
- Smooth, elegant motion
- Clean, white or gradient background"""

    # 提交生成任务
    response = requests.post(
        "https://api.atlascloud.ai/api/v1/model/generateVideo",
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        },
        json={
            "model": "google/veo3.1/image-to-video",
            "prompt": full_prompt,
            "image_url": image_url,
            "durationSeconds": duration,
            "resolution": "1080p",
            "aspectRatio": aspect_ratio,
            "withAudio": with_audio
        }
    )
    
    if response.status_code != 200:
        raise Exception(f"请求失败: {response.text}")
    
    prediction_id = response.json().get("predictionId")
    print(f"视频生成中，任务 ID: {prediction_id}")
    print("预计需要 2-3 分钟，请耐心等待...")
    
    # 轮询获取结果（视频生成较慢）
    return poll_for_video_result(prediction_id, api_key)


def poll_for_video_result(prediction_id: str, api_key: str, timeout: int = 300) -> str:
    """
    轮询获取视频生成结果
    
    Args:
        prediction_id: 任务 ID
        api_key: API Key
        timeout: 超时时间（秒），默认 5 分钟
        
    Returns:
        视频 URL
    """
    start_time = time.time()
    poll_interval = 10  # 每 10 秒查询一次
    
    while time.time() - start_time < timeout:
        response = requests.get(
            f"https://api.atlascloud.ai/api/v1/model/getResult?predictionId={prediction_id}",
            headers={"Authorization": f"Bearer {api_key}"}
        )
        
        result = response.json()
        status = result.get("status")
        
        if status == "completed":
            print("视频生成完成！")
            return result.get("output")
        elif status == "failed":
            raise Exception(f"视频生成失败: {result.get('error')}")
        
        elapsed = int(time.time() - start_time)
        print(f"生成中... 已等待 {elapsed} 秒")
        time.sleep(poll_interval)
    
    raise TimeoutError("视频生成超时，请稍后重试")
```

## 5. 获取生成结果 API

### Endpoint

```
GET https://api.atlascloud.ai/api/v1/model/getResult?predictionId={prediction_id}
```

### 返回状态

| 状态 | 说明 |
|-----|------|
| `pending` | 排队中 |
| `processing` | 生成中 |
| `completed` | 完成 |
| `failed` | 失败 |

### 返回示例

```json
{
    "predictionId": "pred_xxxxx",
    "status": "completed",
    "output": "https://static.atlascloud.ai/outputs/xxxxx.mp4",
    "createdAt": "2026-03-24T12:00:00Z",
    "completedAt": "2026-03-24T12:02:30Z"
}
```

## 错误处理

### 常见错误码

| HTTP 状态码 | 错误 | 处理建议 |
|------------|------|---------|
| 401 | 未授权 | 检查 API Key 是否正确 |
| 402 | 余额不足 | 充值账户 |
| 429 | 请求过于频繁 | 降低请求频率，稍后重试 |
| 500 | 服务器错误 | 稍后重试 |

### 错误响应示例

```json
{
    "error": {
        "code": "invalid_api_key",
        "message": "The API key provided is invalid."
    }
}
```

## 最佳实践

### 1. 图片质量
- 使用高清、光线充足的产品照片
- 避免模糊、过曝或欠曝的图片
- 建议分辨率至少 1024x1024
- **品牌 LOGO 必须清晰可见**（如有）

### 2. 性能优化
- 图像生成：轮询间隔 2 秒
- 视频生成：轮询间隔 10 秒
- 合理设置超时时间

### 3. 成本控制
- 开发测试时使用较短视频（4秒）
- 最终产出时再使用 8 秒高质量
- 视频模式选择：不需要音频时选 "仅视频" 模式

### 4. 提示词技巧
- 视频提示词使用英文效果更佳
- 明确描述摄像机运动（pan, dolly, zoom）
- 指定灯光和氛围

---

## 6. 品牌保护增强指南

本章节提供品牌 LOGO 保护和产品一致性保护的技术方案。

### 6.1 品牌信息数据结构

在开始生成流程前，收集并存储品牌信息：

```python
brand_info = {
    # 基础信息
    "has_brand": True,                      # 是否有品牌
    "brand_name": "品牌名称",                # 品牌名称
    
    # LOGO 信息
    "logo_url": "https://...",              # LOGO 图片 URL（可选）
    "logo_position": "产品正面中央",         # LOGO 在产品上的位置
    
    # 品牌视觉
    "brand_colors": ["#FF0000", "#FFFFFF"], # 品牌主色调（可选）
    
    # 保护设置
    "protection_level": "high"              # high/medium/low
}
```

### 6.2 Nano Banana 2 品牌保护抠图

在使用 Nano Banana 2 Edit 抠图时，增加品牌保护指令：

```python
def get_brand_protection_prompt(brand_info: dict) -> str:
    """
    生成包含品牌保护要求的抠图提示词
    """
    base_prompt = """Remove the background COMPLETELY while applying STRICT protection:

PRODUCT INTEGRITY (CRITICAL):
- Maintain EXACT product shape and proportions
- Keep ALL textures and surface details crisp
- Preserve material appearance perfectly
- Colors must remain accurate"""

    if brand_info.get("has_brand"):
        brand_name = brand_info.get("brand_name", "N/A")
        logo_position = brand_info.get("logo_position", "on the product")
        brand_colors = brand_info.get("brand_colors", [])
        
        brand_prompt = f"""

BRAND LOGO PROTECTION (TOP PRIORITY):
- Keep ALL brand logos 100% sharp, legible, and undistorted
- The brand LOGO located at: {logo_position}
- Maintain exact logo colors without ANY shift
- Preserve logo proportions PERFECTLY
- Do NOT blur or obscure any brand text
- Brand name: {brand_name}
- Brand colors to preserve: {', '.join(brand_colors) if brand_colors else 'original'}"""
    else:
        brand_prompt = """

DETAIL PRESERVATION:
- Keep any text or labels readable
- Preserve all product markings"""

    output_prompt = """

OUTPUT REQUIREMENTS:
- Place on pure white (#FFFFFF) background
- Add subtle professional shadow for depth
- Professional studio lighting
- Clean, precise edges"""

    return base_prompt + brand_prompt + output_prompt


# 使用示例
response = requests.post(
    "https://api.atlascloud.ai/api/v1/model/generateImage",
    headers={
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    },
    json={
        "model": "google/nano-banana-2/edit",
        "prompt": get_brand_protection_prompt(brand_info),
        "image_url": image_url,
        "output_format": "png"
    }
)
```

### 6.3 Veo 3.1 视频一致性保护

在视频生成时，增加产品和品牌一致性保护：

```python
def get_video_consistency_prompt(
    base_description: str,
    brand_info: dict,
    camera_style: str = "dolly_in"
) -> str:
    """
    生成包含一致性保护的视频提示词
    """
    # 摄像机运动
    camera_movements = {
        "static": "Camera remains static with subtle product rotation",
        "dolly_in": "Camera slowly dollies in, revealing product details",
        "orbit": "Camera smoothly orbits around the product",
        "zoom": "Gentle zoom emphasizing premium quality"
    }
    camera_desc = camera_movements.get(camera_style, camera_movements["dolly_in"])
    
    # 品牌保护
    brand_section = ""
    if brand_info.get("has_brand"):
        logo_position = brand_info.get("logo_position", "on the product")
        brand_section = f"""

BRAND PROTECTION (CRITICAL):
- Brand LOGO must remain CLEARLY VISIBLE throughout ALL frames
- LOGO must stay sharp and undistorted in every frame
- LOGO position: {logo_position}
- Brand colors must remain CONSISTENT"""

    prompt = f"""Cinematic product advertisement video.

{base_description}

CAMERA: {camera_desc}

MANDATORY CONSISTENCY REQUIREMENTS:

1. PRODUCT SHAPE CONSISTENCY:
   - Product MUST maintain EXACT shape throughout ALL frames
   - Size and proportions MUST NOT change
   - No morphing, warping, or deformation allowed
   - Product silhouette must remain identical start to finish

2. APPEARANCE CONSISTENCY:
   - Colors must remain EXACTLY the same throughout
   - Textures and surface details must stay consistent
   - Material appearance must be uniform
{brand_section}

3. SCENE CONSISTENCY:
   - Lighting must remain uniform throughout
   - Background must stay consistent (pure white)
   - Shadow must be consistent
   - No sudden lighting changes

4. MOTION QUALITY:
   - Movement must be SMOOTH and STEADY
   - No jarring transitions
   - Elegant, professional motion

TECHNICAL: Professional studio lighting, 1080p, 24fps
The product must look IDENTICAL from first to last frame."""

    return prompt


# 使用示例
response = requests.post(
    "https://api.atlascloud.ai/api/v1/model/generateVideo",
    headers={
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    },
    json={
        "model": "google/veo3.1/image-to-video",
        "prompt": get_video_consistency_prompt(
            "The premium product elegantly showcases its design",
            brand_info,
            "dolly_in"
        ),
        "image_url": white_bg_image_url,
        "durationSeconds": 8,
        "resolution": "1080p",
        "aspectRatio": "16:9",
        "withAudio": True
    }
)
```

### 6.4 品牌保护关键词参考

在构建提示词时，可使用以下关键词增强品牌保护效果：

| 英文关键词 | 用途 |
|-----------|------|
| `pixel-perfect` | 像素级完美 |
| `undistorted` | 无变形 |
| `legible` | 可读的 |
| `crisp` | 清晰的 |
| `consistent` | 一致的 |
| `exact match` | 精确匹配 |
| `no morphing` | 禁止变形 |
| `preserve proportions` | 保持比例 |
| `brand integrity` | 品牌完整性 |
| `color accuracy` | 颜色准确度 |
| `throughout all frames` | 贯穿所有帧 |
| `identical` | 完全相同的 |

### 6.5 常见品牌保护问题

| 问题 | 原因 | 解决方案 |
|-----|------|---------|
| LOGO 模糊 | 原图 LOGO 不清晰 | 提供高清原图，明确指定 LOGO 位置 |
| 颜色偏移 | AI 优化导致 | 在 prompt 中指定准确色值 |
| 视频中产品变形 | 摄像机运动复杂 | 使用简单运动（静态或推镜） |
| 多镜头不连贯 | 场景描述不统一 | 强调 "uniform" 和 "consistent" |

---

## 7. 费用预估功能

### 7.1 费用计算公式

```python
def estimate_ad_cost(
    video_duration: int = 8,
    with_audio: bool = True,
    resolution: str = "1080p"
) -> dict:
    """
    精准估算广告生成费用
    
    Args:
        video_duration: 视频时长（4/6/8秒）
        with_audio: 是否生成音频
        resolution: 分辨率
        
    Returns:
        费用明细字典
    """
    costs = {
        "background_removal": {
            "name": "智能抠图",
            "model": "Nano Banana 2 Edit",
            "min": 0.02,
            "max": 0.05
        },
        "copywriting": {
            "name": "文案生成",
            "model": "Gemini 3.1 Pro",
            "min": 0.01,
            "max": 0.02
        },
        "video_generation": {
            "name": "视频生成",
            "model": "Veo 3.1 I2V",
            "min": video_duration * 0.09,
            "max": video_duration * (0.40 if with_audio else 0.20)
        }
    }
    
    total_min = sum(item["min"] for item in costs.values())
    total_max = sum(item["max"] for item in costs.values())
    
    return {
        "breakdown": costs,
        "total_min": round(total_min, 2),
        "total_max": round(total_max, 2),
        "currency": "USD"
    }
```

### 7.2 费用参考表

| 配置 | 4秒 | 6秒 | 8秒 |
|------|-----|-----|-----|
| 仅视频 | $0.83 | $1.23 | $1.63 |
| 含音频 | $1.63 | $2.43 | $3.27 |

*以上费用包含抠图($0.02-0.05)和文案生成($0.01-0.02)*

### 7.3 费用展示模板

```python
def format_cost_estimate(cost_data: dict, params: dict) -> str:
    """格式化费用预估展示"""
    breakdown = cost_data["breakdown"]
    audio_status = "含音频" if params.get("with_audio") else "无音频"
    
    return f"""
📊 **本次广告生成费用预估**

| 步骤 | 模型 | 费用估算 |
|------|------|----------|
| 🖼️ {breakdown['background_removal']['name']} | {breakdown['background_removal']['model']} | ${breakdown['background_removal']['min']:.2f} - ${breakdown['background_removal']['max']:.2f} |
| ✍️ {breakdown['copywriting']['name']} | {breakdown['copywriting']['model']} | ${breakdown['copywriting']['min']:.2f} - ${breakdown['copywriting']['max']:.2f} |
| 🎬 {breakdown['video_generation']['name']} ({params['duration']}秒, {audio_status}) | {breakdown['video_generation']['model']} | ${breakdown['video_generation']['min']:.2f} - ${breakdown['video_generation']['max']:.2f} |
| **💰 预计总费用** | - | **${cost_data['total_min']:.2f} - ${cost_data['total_max']:.2f}** |

⚠️ *实际费用以 Atlas Cloud 账单为准*
"""
```
