---
name: a2f
description: >-
  Archive2Figure (a2f) skill for converting PDF archives into digital character figures.
  Upload PDF → Extract character features → Generate images → Retrieve results.
  Supports Chinese historical characters and realistic figure generation.
metadata:
  version: "1.0.0"
  author: "Wuji API Integration"
  category: "image-generation"
  tags:
    - image-generation
    - character-creation
    - pdf-processing
    - ai-art
    - chinese-history
  capabilities:
    - PDF feature extraction
    - Character image generation
    - Job status polling
    - Batch image generation
    - Feature-based prompting
  dependencies:
    python: ">=3.8"
    httpx: ">=0.24.0"
    pydantic: ">=2.0.0"
  environment:
    A2F_API_BASE: "https://wuji.cyphy.com/api"
  triggers:
    - "generate character from pdf"
    - "create figure from archive"
    - "extract character features"
    - "a2f"
    - "archive to figure"
    - "character generation"
  endpoints:
    - name: "Extract Features"
      method: "POST"
      path: "/archiveData"
      description: "Upload PDF and extract character features"
    - name: "Generate Images"
      method: "POST"
      path: "/a2fgen"
      description: "Generate character images from features"
    - name: "Job Status"
      method: "GET"
      path: "/job_status/{job_id}"
      description: "Check generation job status"
---

# Archive2Figure (A2F) Skill

## Overview

The A2F (Archive2Figure) skill converts PDF documents containing character information into high-quality digital figure images using AI generation. It's particularly optimized for Chinese historical characters and realistic portrait generation.

### Workflow

1. **Extract Features**: Upload PDF → Extract character features and tags
2. **Generate Images**: Use features to generate character images
3. **Check Status**: Poll for job completion and retrieve results

## Table of Contents

- [Quick Start](#quick-start)
- [API Endpoints](#api-endpoints)
- [Complete Workflow](#complete-workflow)
- [Feature Extraction](#feature-extraction)
- [Image Generation](#image-generation)
- [Response Formats](#response-formats)
- [Examples](#examples)
- [Best Practices](#best-practices)
- [Troubleshooting](#troubleshooting)

## Quick Start

### Basic Usage

```python
import httpx

API_BASE = "https://wuji.cyphy.com/api"

# Step 1: Upload PDF and extract features
async def extract_features(pdf_path, role_name):
    async with httpx.AsyncClient(timeout=60.0) as client:
        with open(pdf_path, "rb") as f:
            files = {"files[0]": (pdf_path, f, "application/pdf")}
            data = {
                "role": role_name,
                "loop_count": 2,
                "gen_method": "qwen",
                "openclaw": 1
            }
            response = await client.post(f"{API_BASE}/archiveData", data=data, files=files)
            return response.json()

# Step 2: Generate images
async def generate_images(prompt):
    async with httpx.AsyncClient(timeout=60.0) as client:
        payload = {
            "text": prompt,
            "negative_text": "低质量, 模糊, 变形",
            "gen_method": 5,
            "gen_size": 1,
            "img_num": 4,
            "json": 1,
            "openclaw": 1
        }
        response = await client.post(f"{API_BASE}/a2fgen", json=payload)
        return response.json()

# Step 3: Check job status
async def check_status(job_id):
    async with httpx.AsyncClient(timeout=30.0) as client:
        response = await client.get(f"{API_BASE}/job_status/{job_id}")
        return response.json()
```

## API Endpoints

### 1. Extract Features

**Endpoint:** `POST /api/archiveData`

Upload a PDF file and extract character features and tags.

**Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `files[0]` | File | Yes | PDF file containing character information |
| `role` | string | Yes | Character name (e.g., "李清照") |
| `loop_count` | int | No | Extraction loops (default: 2) |
| `gen_method` | string | No | Generation method (default: "qwen") |
| `openclaw` | int | No | Service flag (default: 1) |

**Request Example:**

```python
import httpx

async with httpx.AsyncClient() as client:
    with open("character.pdf", "rb") as f:
        files = {"files[0]": ("character.pdf", f, "application/pdf")}
        data = {
            "role": "李清照",
            "loop_count": 2,
            "gen_method": "qwen",
            "openclaw": 1
        }
        response = await client.post(
            "https://wuji.cyphy.com/api/archiveData",
            data=data,
            files=files
        )
        result = response.json()
```

**Response Example:**

```json
{
  "李清照诗词中的自我形象研究_侯淑婉.pdf": {
    "role": ["主要人物"],
    "gender": ["女性"],
    "age": ["成人"],
    "ffeatures": ["皮肤白皙", "面容清秀", "表情细腻", "情感丰富"],
    "hairstyle": ["长发", "传统发型"],
    "headdress": [],
    "build": ["苗条"],
    "clothing": ["古代服饰", "轻薄衣衫", "色彩淡雅"],
    "footwear": [],
    "accessories": ["金钗", "玉饰", "首饰"],
    "activity": ["写诗", "游玩", "思念"],
    "background": ["宋代", "江南水乡", "封建社会", "家庭环境"],
    "context": ["诗词创作", "家庭生活", "社会动荡"],
    "vibe": ["婉约", "细腻", "坚韧"],
    "temperament": ["敏感", "多情", "独立"],
    "language": ["文言文", "宋代", "古代汉语", "文雅"],
    "voice": ["柔和", "深情"],
    "cusstyle": ["中国古典水墨画"]
  }
}
```

### 2. Generate Images

**Endpoint:** `POST /api/a2fgen`

Generate character images using extracted features.

**Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `text` | string | Yes | Combined prompt text |
| `negative_text` | string | No | Negative prompts (quality control) |
| `gen_method` | int | No | Generation method (default: 5) |
| `gen_size` | int | No | Generation size (default: 1) |
| `img_num` | int | No | Number of images (1-10, default: 4) |
| `json` | int | No | Response format (default: 1) |
| `openclaw` | int | No | Service flag (default: 1) |

**Default Negative Prompt:**

```
文本, 特写, 裁剪, 出框, 最差质量, 低质量, jpeg 伪影, pgl y, 重复, 病态, 残缺, 额外的手指, 变异的手, 画得不好的手, 画得不好的脸, 突变, 变形, 模糊, 脱水, 不良的解剖结构, 不良的比例, 额外的肢体, 克隆的脸, 毁容, 总体比例, 畸形的四肢, 缺失的手臂, 缺失的腿, 额外的手臂, 多余的腿, 融合的手指, 太多的手指, 长脖子, 水印, 印章
```

**Request Example:**

```python
payload = {
    "text": "李清照, 女性, 成人, 肖像画, 正脸, 全身照, 站立, 看着观众, 皮肤白皙, 面容清秀, 古代服饰, 中国古典水墨画, 写实风格, 真人风格",
    "negative_text": "文本, 特写, 裁剪, 出框, 最差质量, 低质量",
    "gen_method": 5,
    "gen_size": 1,
    "img_num": 4,
    "json": 1,
    "openclaw": 1
}

async with httpx.AsyncClient() as client:
    response = await client.post(
        "https://wuji.cyphy.com/api/a2fgen",
        json=payload
    )
    result = response.json()
```

**Response Example:**

```json
{
  "job_id": "12345",
  "status": "processing",
  "message": "Job created successfully"
}
```

### 3. Check Job Status

**Endpoint:** `GET /api/job_status/{job_id}`

Check the status of an image generation job.

**Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `job_id` | string | Job ID from generate-images response |

**Request Example:**

```python
async with httpx.AsyncClient() as client:
    response = await client.get(
        f"https://wuji.cyphy.com/api/job_status/{job_id}"
    )
    result = response.json()
```

**Response Example (Processing):**

```json
{
  "job_id": "12345",
  "status": "processing",
  "progress": 50
}
```

**Response Example (Completed):**

```json
{
  "job_id": "12345",
  "status": "completed",
  "progress": 100,
  "results": [
    "https://cdn.example.com/result1.png",
    "https://cdn.example.com/result2.png",
    "https://cdn.example.com/result3.png",
    "https://cdn.example.com/result4.png"
  ]
}
```

## Complete Workflow

### Full Example: PDF to Character Images

```python
import httpx
import asyncio

API_BASE = "https://wuji.cyphy.com/api"

async def complete_a2f_workflow(pdf_path, role_name, style="写实风格,真人风格"):
    """Complete A2F workflow: PDF → Features → Images → Results"""

    # Step 1: Extract features
    print("Step 1: Extracting features from PDF...")
    async with httpx.AsyncClient(timeout=60.0) as client:
        with open(pdf_path, "rb") as f:
            files = {"files[0]": (pdf_path, f, "application/pdf")}
            data = {
                "role": role_name,
                "loop_count": 2,
                "gen_method": "qwen",
                "openclaw": 1
            }
            response = await client.post(f"{API_BASE}/archiveData", data=data, files=files)
            features_result = response.json()

    # Extract features from response
    pdf_key = list(features_result.keys())[0]
    features = features_result[pdf_key]
    print(f"Extracted features: {features['role']}, {features['gender']}")

    # Step 2: Build prompt from features
    print("Step 2: Building prompt and generating images...")
    prompt_parts = [
        role_name,
        features.get("gender", [""])[0],
        features.get("age", [""])[0],
        "肖像画, 正脸, 全身照, 站立, 看着观众"
    ]

    # Add detailed features
    for key in ["ffeatures", "clothing", "hairstyle", "accessories"]:
        if key in features and features[key]:
            prompt_parts.extend(features[key])

    # Add style
    prompt_parts.append(style)

    text = ", ".join(filter(None, prompt_parts))

    # Generate images
    async with httpx.AsyncClient(timeout=60.0) as client:
        payload = {
            "text": text,
            "negative_text": "文本, 特写, 裁剪, 出框, 最差质量, 低质量, jpeg 伪影, pgl y, 重复, 病态, 残缺, 额外的手指, 变异的手, 画得不好的手, 画得不好的脸, 突变, 变形, 模糊, 脱水, 不良的解剖结构, 不良的比例, 额外的肢体, 克隆的脸, 毁容, 总体比例, 畸形的四肢, 缺失的手臂, 缺失的腿, 额外的手臂, 多余的腿, 融合的手指, 太多的手指, 长脖子, 水印, 印章",
            "gen_method": 5,
            "gen_size": 1,
            "img_num": 4,
            "json": 1,
            "openclaw": 1
        }
        response = await client.post(f"{API_BASE}/a2fgen", json=payload)
        gen_result = response.json()

    job_id = gen_result.get("job_id") or gen_result.get("id")
    print(f"Generation started. Job ID: {job_id}")

    # Step 3: Poll for completion
    print("Step 3: Waiting for generation to complete...")
    async with httpx.AsyncClient(timeout=30.0) as client:
        while True:
            response = await client.get(f"{API_BASE}/job_status/{job_id}")
            status_result = response.json()

            status = status_result.get("status")
            progress = status_result.get("progress", 0)

            print(f"Status: {status} ({progress}%)")

            if status == "completed":
                print("\nGeneration complete!")
                results = status_result.get("results", [])
                for i, url in enumerate(results, 1):
                    print(f"Image {i}: {url}")
                return results
            elif status == "failed":
                raise Exception(f"Generation failed: {status_result.get('error')}")

            await asyncio.sleep(5)

# Usage
if __name__ == "__main__":
    results = asyncio.run(complete_a2f_workflow(
        "李清照诗词中的自我形象研究_侯淑婉.pdf",
        "李清照"
    ))
```

## Feature Extraction

### Understanding Feature Categories

The feature extraction returns multiple categories:

| Category | Description | Example Values |
|----------|-------------|----------------|
| `role` | Character role type | ["主要人物"] |
| `gender` | Gender | ["女性"] |
| `age` | Age range | ["成人"] |
| `ffeatures` | Facial features | ["皮肤白皙", "面容清秀"] |
| `hairstyle` | Hair style | ["长发", "传统发型"] |
| `headdress` | Head accessories | [] |
| `build` | Body type | ["苗条"] |
| `clothing` | Clothing | ["古代服饰", "轻薄衣衫"] |
| `footwear` | Shoes | [] |
| `accessories` | Accessories | ["金钗", "玉饰"] |
| `activity` | Activities | ["写诗", "游玩"] |
| `background` | Background setting | ["宋代", "江南水乡"] |
| `context` | Context | ["诗词创作"] |
| `vibe` | Atmosphere | ["婉约", "细腻"] |
| `temperament` | Personality | ["敏感", "多情"] |
| `language` | Language style | ["文言文"] |
| `voice` | Voice quality | ["柔和"] |
| `cusstyle` | Custom style | ["中国古典水墨画"] |

### Building Effective Prompts

**Good Prompt Structure:**

```
[角色名], [性别], [年龄], [基础描述], [细节特征], [服装配饰], [风格]
```

**Example:**

```python
# Base
prompt = "李清照, 女性, 成人"

# Pose & framing
prompt += ", 肖像画, 正脸, 全身照, 站立, 看着观众"

# Features
prompt += ", 皮肤白皙, 面容清秀, 表情细腻"

# Clothing & accessories
prompt += ", 古代服饰, 轻薄衣衫, 色彩淡雅, 金钗, 玉饰"

# Style
prompt += ", 写实风格, 真人风格"

# Result:
# "李清照, 女性, 成人, 肖像画, 正脸, 全身照, 站立, 看着观众, 皮肤白皙, 面容清秀, 表情细腻, 古代服饰, 轻薄衣衫, 色彩淡雅, 金钗, 玉饰, 写实风格, 真人风格"
```

## Image Generation

### Generation Parameters

| Parameter | Value Range | Recommended | Effect |
|-----------|-------------|-------------|--------|
| `gen_method` | 1-10 | 5 | Generation algorithm |
| `gen_size` | 1-5 | 1 | Output resolution |
| `img_num` | 1-10 | 4 | Number of images |

### Negative Prompts

Use negative prompts to control quality:

```python
# Basic quality control
basic_negative = "低质量, 模糊, 变形, 水印"

# Detailed quality control
detailed_negative = "文本, 特写, 裁剪, 出框, 最差质量, 低质量, jpeg 伪影, pgl y, 重复, 病态, 残缺, 额外的手指, 变异的手, 画得不好的手, 画得不好的脸, 突变, 变形, 模糊, 脱水, 不良的解剖结构, 不良的比例, 额外的肢体, 克隆的脸, 毁容, 总体比例, 畸形的四肢, 缺失的手臂, 缺失的腿, 额外的手臂, 多余的腿, 融合的手指, 太多的手指, 长脖子, 水印, 印章"
```

## Response Formats

### Feature Extraction Response

```json
{
  "filename.pdf": {
    "role": ["主要人物"],
    "gender": ["女性"],
    "age": ["成人"],
    "ffeatures": ["皮肤白皙", "面容清秀"],
    "hairstyle": ["长发"],
    "clothing": ["古代服饰"],
    "accessories": ["金钗"],
    "activity": ["写诗"],
    "background": ["宋代"],
    "vibe": ["婉约"],
    "temperament": ["敏感"],
    "cusstyle": ["中国古典水墨画"]
  }
}
```

### Generation Response

```json
{
  "job_id": "17171",
  "status": "processing",
  "message": "Job created successfully"
}
```

### Status Response (Processing)

```json
{
  "job_id": "17171",
  "status": "processing",
  "progress": 45,
  "message": "Generating images..."
}
```

### Status Response (Completed)

```json
{
  "job_id": "17171",
  "status": "completed",
  "progress": 100,
  "results": [
    "https://cdn.example.com/image1.png",
    "https://cdn.example.com/image2.png",
    "https://cdn.example.com/image3.png",
    "https://cdn.example.com/image4.png"
  ]
}
```

## Examples

### Example 1: Generate Li Qingzhao Character

```python
import asyncio
import httpx

async def generate_li_qingzhao():
    API_BASE = "https://wuji.cyphy.com/api"

    # Extract features
    async with httpx.AsyncClient() as client:
        with open("李清照.pdf", "rb") as f:
            files = {"files[0]": ("李清照.pdf", f, "application/pdf")}
            data = {"role": "李清照", "loop_count": 2, "gen_method": "qwen", "openclaw": 1}
            response = await client.post(f"{API_BASE}/archiveData", data=data, files=files)
            features = response.json()

    # Generate images
    prompt = "李清照, 女性, 成人, 肖像画, 正脸, 全身照, 站立, 写诗, 古代服饰, 中国古典水墨画, 写实风格"
    payload = {
        "text": prompt,
        "negative_text": "低质量, 模糊",
        "gen_method": 5,
        "img_num": 4,
        "json": 1,
        "openclaw": 1
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(f"{API_BASE}/a2fgen", json=payload)
        job = response.json()

    print(f"Job ID: {job['job_id']}")
    return job['job_id']
```

### Example 2: Batch Character Generation

```python
async def batch_generate_characters(pdf_files):
    """Generate multiple characters from multiple PDFs"""

    jobs = []

    for pdf_file, role_name in pdf_files:
        # Extract features
        async with httpx.AsyncClient() as client:
            with open(pdf_file, "rb") as f:
                files = {"files[0]": (pdf_file, f, "application/pdf")}
                data = {"role": role_name, "loop_count": 2, "gen_method": "qwen", "openclaw": 1}
                response = await client.post("https://wuji.cyphy.com/api/archiveData", data=data, files=files)
                features = response.json()

        # Build prompt and generate
        prompt = f"{role_name}, 写实风格, 真人风格"
        payload = {"text": prompt, "img_num": 4, "json": 1, "openclaw": 1}

        async with httpx.AsyncClient() as client:
            response = await client.post("https://wuji.cyphy.com/api/a2fgen", json=payload)
            job = response.json()
            jobs.append({"role": role_name, "job_id": job["job_id"]})

    return jobs
```

### Example 3: Custom Style Generation

```python
async def generate_with_custom_style(pdf_path, role_name, style):
    """Generate character with custom style"""

    # Extract features
    async with httpx.AsyncClient() as client:
        with open(pdf_path, "rb") as f:
            files = {"files[0]": (pdf_path, f, "application/pdf")}
            data = {"role": role_name, "loop_count": 2, "gen_method": "qwen", "openclaw": 1}
            response = await client.post("https://wuji.cyphy.com/api/archiveData", data=data, files=files)
            features = response.json()

    # Custom style prompts
    style_prompts = {
        "anime": "动漫风格, 二次元, 动画角色",
        "oil_painting": "油画风格, 古典油画, 艺术绘画",
        "watercolor": "水彩风格, 水彩画, 淡雅",
        "3d_render": "3D渲染, CGI, 3D角色, 立体感"
    }

    prompt = f"{role_name}, {style_prompts.get(style, '写实风格')}"
    payload = {"text": prompt, "img_num": 4, "json": 1, "openclaw": 1}

    async with httpx.AsyncClient() as client:
        response = await client.post("https://wuji.cyphy.com/api/a2fgen", json=payload)
        return response.json()
```

## Best Practices

### 1. PDF Preparation

- Use high-quality PDFs with clear character descriptions
- Include detailed physical descriptions
- Provide historical context and setting
- Mention clothing, accessories, and activities

### 2. Prompt Engineering

**DO:**
```python
# Good: Specific and structured
prompt = "李清照, 女性, 成人, 肖像画, 正脸, 全身照, 古代服饰, 写实风格"
```

**DON'T:**
```python
# Bad: Too vague
prompt = "一个女人"
```

### 3. Error Handling

```python
async def safe_generate(pdf_path, role_name):
    try:
        # Extract features
        async with httpx.AsyncClient(timeout=60.0) as client:
            with open(pdf_path, "rb") as f:
                files = {"files[0]": (pdf_path, f, "application/pdf")}
                data = {"role": role_name, "loop_count": 2, "gen_method": "qwen", "openclaw": 1}
                response = await client.post("https://wuji.cyphy.com/api/archiveData", data=data, files=files)
                response.raise_for_status()
                features = response.json()

        # Generate images
        payload = {"text": f"{role_name}, 写实风格", "img_num": 4, "json": 1, "openclaw": 1}
        response = await client.post("https://wuji.cyphy.com/api/a2fgen", json=payload)
        response.raise_for_status()
        return response.json()

    except httpx.HTTPStatusError as e:
        print(f"HTTP error: {e.response.status_code}")
        print(f"Response: {e.response.text}")
    except Exception as e:
        print(f"Error: {str(e)}")
```

### 4. Polling Strategy

```python
async def poll_with_backoff(job_id, max_wait=300):
    """Poll job status with exponential backoff"""

    start_time = time.time()
    wait_time = 2

    while time.time() - start_time < max_wait:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"https://wuji.cyphy.com/api/job_status/{job_id}")
            result = response.json()

            if result["status"] == "completed":
                return result
            elif result["status"] == "failed":
                raise Exception(f"Job failed: {result.get('error')}")

        await asyncio.sleep(wait_time)
        wait_time = min(wait_time * 2, 10)  # Max 10 seconds

    raise TimeoutError("Job timed out")
```

### 5. Feature Selection

Not all features are equally important. Prioritize:

```python
# High priority features
priority_features = [
    "gender",      # Essential for character appearance
    "age",         # Affects overall look
    "ffeatures",   # Facial characteristics
    "clothing",    # Historical accuracy
    "cusstyle"     # Art style
]

# Lower priority features
optional_features = [
    "language",    # Less relevant for visual
    "voice",       # Audio only
    "context"      # Background info
]
```

## Troubleshooting

### Common Issues

**Issue**: Feature extraction returns empty features
- **Solution**: Ensure PDF contains character descriptions. Try a different PDF.

**Issue**: Generated images don't match character
- **Solution**: Add more specific features to prompt. Include clothing, accessories, and physical traits.

**Issue**: Job status stays "processing" too long
- **Solution**: Jobs can take 1-5 minutes. Implement timeout handling (e.g., 5 minutes).

**Issue**: "401 Unauthorized" error
- **Solution**: Check API endpoint and authentication if required.

**Issue**: Low quality images
- **Solution**: Enhance negative prompts, increase gen_method value, or adjust gen_size.

### Debug Mode

```python
import logging

# Enable debug logging
logging.basicConfig(level=logging.DEBUG)
httpx_logger = logging.getLogger("httpx")
httpx_logger.setLevel(logging.DEBUG)
```

### Testing

```python
async def test_a2f_endpoints():
    """Test A2F endpoints"""

    # Test 1: Feature extraction
    print("Testing feature extraction...")
    # Add test code here

    # Test 2: Image generation
    print("Testing image generation...")
    # Add test code here

    # Test 3: Job status
    print("Testing job status...")
    # Add test code here

    print("All tests passed!")
```

## Resources

- **Python Example**: [a2f_example.py](a2f_example.py) - Complete client implementation
- **Quick Start**: [quick_start.py](quick_start.py) - Simple workflow example
- **Batch Generation**: [batch_generation.py](batch_generation.py) - Batch processing
- **Examples Guide**: [README.md](README.md) - Usage examples

## Changelog

### Version 1.0.0 (2026-05-05)
- Initial release
- Feature extraction from PDFs
- Image generation with custom prompts
- Job status polling
- Complete workflow implementation
