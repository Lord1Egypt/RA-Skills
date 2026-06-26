---
name: "seedream-image"
description: "调用火山引擎 Seedream 图片生成 API。当用户需要生成图片时使用此 skill。"
version: "1.0.1"
required_env_vars:
  - VOLCENGINE_API_KEY
---

# Seedream 图片生成 API 调用

此 skill 用于调用火山引擎 Seedream 图片生成 API，支持文生图功能。

**使用方式：** 用户只需提供图片描述，我直接调用 API 生成图片并返回本地文件。

## 支持的模型

代码中使用简短别名调用，完整 Model ID 如下：

| 名称 | 别名 | Model ID | 说明 |
|------|------|----------|------|
| 5.0 | `5.0` | `doubao-seedream-5-0-260128` | 默认使用，支持文生图/图生图/联网搜索 |
| 4.5 | `4.5` | `doubao-seedream-4-5-251128` | 支持文生图/图生图 |
| 4.0 | `4.0` | `doubao-seedream-4-0-250828` | 支持文生图/图生图 |
| 3.0-t2i | `3.0-t2i` | `doubao-seedream-3-0-t2i-250415` | 仅文生图 |
| 3.0-i2i | `3.0-i2i` | `doubao-seededit-3-0-i2i-250415` | 仅图生图 |

## 直接调用

用户说"生成一张xxx图片"时，直接运行：

```bash
python seedream_api.py "一只可爱的橘猫"
```

指定模型：
```bash
python seedream_api.py "一只可爱的橘猫" -m 4.5
```

图片会自动下载到 `output` 目录。

## 命令行参数

| 参数 | 说明 |
|------|------|
| `prompt` | 图片描述（位置参数） |
| `-m, --model` | 模型版本 |
| `-s, --size` | 图片尺寸，默认 2048x2048 |
| `-o, --output-dir` | 输出目录，默认 output |
| `--steps` | 推理步数 1-50，默认 50 |
| `--guidance` | 引导系数 1-20，默认 7.5 |
| `--seed` | 随机种子（可复现结果） |
| `--negative` | 负向提示词 |
| `-i, --image` | 单张参考图片路径或URL（图生图） |
| `--images` | 多张参考图片路径或URL（多图生图/组图） |
| `--group` | 启用组图模式 |
| `--tools` | 工具列表，如 web_search（启用联网搜索） |

或导入使用：

```python
from seedream_api import generate_image

result = generate_image("一只可爱的橘猫坐在窗台上")
for path in result["local_paths"]:
    print(path)  # 本地文件路径
```

## API 端点

```
POST https://ark.cn-beijing.volces.com/api/v3/images/generations
```

## 鉴权方式

使用 API Key 进行鉴权，需要在请求头中添加：
```
Authorization: Bearer <your-api-key>
Content-Type: application/json
```

## 请求参数

### 必选参数

- **model** (string): 模型名称
  - 使用代码中的别名：`5.0`、`4.5`、`4.0`、`3.0-t2i`
  - 或直接使用完整 Model ID

- **prompt** (string): 文本提示词
  - 建议不超过 300 个汉字或 600 个英文单词
  - 字数过多可能导致模型忽略细节

### 可选参数

- **size** (string): 生成图像的尺寸
  - 方式 1：指定分辨率（2K、4K）
  - 方式 2：指定宽高像素值（如 "2048x2048"）
  - 总像素范围：[3686400, 16777216]
  - 宽高比范围：[1/16, 16]
  - 默认值：2048x2048

  推荐尺寸：
  - 2K 1:1: 2048x2048
  - 2K 16:9: 2848x1600
  - 2K 9:16: 1600x2848
  - 4K 1:1: 4096x4096
  - 4K 16:9: 5504x3040
  - 4K 9:16: 3040x5504

- **num_inference_steps** (integer): 推理步数
  - 范围：1-50
  - 默认值：50

- **guidance_scale** (number): 引导系数
  - 范围：1-20
  - 默认值：7.5

- **seed** (integer): 随机种子
  - 用于生成可复现的图片

- **negative_prompt** (string): 负向提示词
  - 描述不希望在图片中出现的内容

- **image** (string/array): 参考图片信息
  - 支持文件路径、URL 或 Base64 编码
  - 单图：传入字符串
  - 多图：传入字符串数组（最多 14 张）
  - Base64 格式：`data:image/<格式>;base64,<编码>`，格式需小写
  - 支持格式：jpeg、png、webp、bmp、tiff、gif
  - 宽高比范围：[1/16, 16]
  - 宽高长度 > 14px
  - 大小：不超过 10MB
  - 总像素：不超过 6000x6000=36000000 px

- **sequential_image_generation** (string): 组图模式
  - `auto`：启用组图模式，生成一组内容关联的图片
  - `disabled`：禁用组图模式，生成单张图片（默认）
  - 组图数量限制：最多 15 张（含参考图）

- **tools** (array): 工具列表
  - 支持的工具类型：`web_search`（联网搜索）
  - 示例：`[{"type": "web_search"}]`
  - 用于增强提示词理解，模型可联网搜索相关信息
  - **仅支持 `5.0` 模型**（doubao-seedream-5-0-260128）

## 使用场景

### 1. 文生图（生成单张图片）

```json
{
  "model": "doubao-seedream-5-0-260128",
  "prompt": "一只可爱的橘猫坐在窗台上，阳光洒在它的毛发上",
  "size": "2048x2048"
}
```

### 2. 单图生图（图生图）

```json
{
  "model": "doubao-seedream-5-0-260128",
  "prompt": "将图片转换成卡通风格",
  "image": "data:image/jpeg;base64,/9j/4AAQSkZJRg...",
  "size": "2048x2048"
}
```

### 3. 多图生图

```json
{
  "model": "doubao-seedream-5-0-260128",
  "prompt": "结合这两张图片的风格",
  "image": [
    "data:image/jpeg;base64,/9j/4AAQSkZJRg...",
    "data:image/jpeg;base64,/9j/4AAQSkZJRg..."
  ],
  "size": "2048x2048"
}
```

### 4. 组图生成

```json
{
  "model": "doubao-seedream-5-0-260128",
  "prompt": "一组不同姿势的橘猫",
  "sequential_image_generation": "auto",
  "size": "2048x2048"
}
```

### 5. 多图生组图

```json
{
  "model": "doubao-seedream-5-0-260128",
  "prompt": "基于参考图片生成一组相关图片",
  "image": [
    "data:image/jpeg;base64,/9j/4AAQSkZJRg...",
    "data:image/jpeg;base64,/9j/4AAQSkZJRg..."
  ],
  "sequential_image_generation": "auto",
  "size": "2048x2048"
}
```

## 响应格式

成功响应：

```json
{
  "created": 1710000000,
  "data": [
    {
      "url": "https://example.com/generated_image1.jpg"
    },
    {
      "url": "https://example.com/generated_image2.jpg"
    }
  ]
}
```

错误响应：

```json
{
  "error": {
    "message": "错误信息",
    "type": "错误类型",
    "param": null,
    "code": null
  }
}
```

## 注意事项

1. **API Key 安全**：不要在代码中硬编码 API Key，建议使用环境变量
2. **图片 URL 可访问性**：确保提供的图片 URL 可以被公开访问
3. **提示词优化**：简洁明确的提示词效果更好
4. **尺寸限制**：注意总像素和宽高比的双重限制
5. **图片数量限制**：最多支持 14 张参考图
6. **格式要求**：Base64 编码时注意格式正确，图片格式需小写
7. **网络请求**：代码会发起外部请求（API 请求和下载生成的图片），需确保网络畅通

## Python 调用示例

```python
import requests
import os

API_KEY = os.getenv("VOLCENGINE_API_KEY")
API_URL = "https://ark.cn-beijing.volces.com/api/v3/images/generations"

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

data = {
    "model": "doubao-seedream-5-0-260128",
    "prompt": "一只可爱的橘猫坐在窗台上，阳光洒在它的毛发上",
    "size": "2048x2048"
}

response = requests.post(API_URL, headers=headers, json=data)
result = response.json()

if "data" in result:
    for image in result["data"]:
        print(f"生成的图片 URL: {image['url']}")
else:
    print(f"错误: {result.get('error', {}).get('message', '未知错误')}")
```

## 使用此 Skill

当用户需要以下功能时，使用此 skill：
- 生成图片（文生图）
- 图生图（使用参考图片）
- 多图生图（多张参考图片）
- 组图生成
- 使用 Seedream 相关模型进行图片生成

### Python 调用示例

#### 文生图
```python
from seedream_api import generate_image

result = generate_image("一只可爱的橘猫坐在窗台上")
for path in result["local_paths"]:
    print(path)  # 本地文件路径
```

#### 图生图（使用文件路径）
```python
from seedream_api import generate_image

result = generate_image(
    prompt="将图片转换成卡通风格",
    image="path/to/input.jpg"
)
for path in result["local_paths"]:
    print(path)
```

#### 图生图（使用 URL）
```python
from seedream_api import generate_image

result = generate_image(
    prompt="将图片转换成卡通风格",
    image="https://example.com/image.jpg"
)
```

#### 多图生图
```python
from seedream_api import generate_image

result = generate_image(
    prompt="结合这两张图片的风格",
    image=["path/to/image1.jpg", "path/to/image2.jpg"]
)
```

#### 组图生成
```python
from seedream_api import generate_image

result = generate_image(
    prompt="一组不同姿势的橘猫",
    sequential_image_generation="auto"
)
for path in result["local_paths"]:
    print(path)
```

#### 使用联网搜索工具
```python
from seedream_api import generate_image

result = generate_image(
    prompt="埃隆·马斯克最新的SpaceX火箭发射场景",
    tools=[{"type": "web_search"}]
)
for path in result["local_paths"]:
    print(path)
```
```

在调用前，确保：
1. 已获取火山引擎 API Key (环境变量: VOLCENGINE_API_KEY)
2. 已开通 Seedream 模型服务
3. 了解所需的使用场景和参数配置
