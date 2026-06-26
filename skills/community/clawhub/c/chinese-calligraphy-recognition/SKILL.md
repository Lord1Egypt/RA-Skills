---
AIGC:
    ContentProducer: Minimax Agent AI
    ContentPropagator: Minimax Agent AI
    Label: AIGC
    ProduceID: "00000000000000000000000000000000"
    PropagateID: "00000000000000000000000000000000"
    ReservedCode1: 3046022100d61658ffc6f5bdbf4ebb1716d5aa7dca050f66263bf32e213943418ffb16c55e0221009c2d3c375e8dec9ad5ed853b5a5a4362d57952f6e99e4e4f90c085f47204f159
    ReservedCode2: 3045022010f2180d5d9d279369f3095ce2c44b7239bd3cdd2bcac43073b1d6e2caf25ae8022100c578ab0227680f8486e4611e114f91c031192271e6475de8a9da186806f3179a
description: |-
    汉字书法字体识别技能。用于识别书法图片中的字体类型，包括楷书、行书、草书、篆书、隶书等。
    当用户上传书法图片并要求识别字体时触发此技能。
    适用于书法作品鉴赏、古籍研究、书法学习、文物鉴定等场景。
    模型地址: https://huggingface.co/spaces/jfxia/shufa
name: shufa-recognition
---

# 汉字书法字体识别技能

## 功能概述

本技能调用 HuggingFace Spaces 上的书法识别模型（jfxia/shufa）来识别书法图片中的字体类型。

## 支持的字体类型

根据书法识别模型，支持以下字体识别：

| 字体类型 | 说明 |
|----------|------|
| 楷书 | 标准楷体，如欧阳询、颜真卿、柳公权字体 |
| 行书 | 行云流水，如王羲之、米芾字体 |
| 草书 | 狂放不羁，如怀素、张旭字体 |
| 篆书 | 大篆、小篆 |
| 隶书 | 汉隶风格 |
| 魏碑 | 魏碑体 |

## 使用方法

### 1. 图像输入

支持以下输入方式：

- **直接上传图片**：用户上传书法图片文件（PNG、JPG、JPEG、BMP 等格式）
- **图片URL**：提供图片的网络链接

### 2. API 调用

使用 HuggingFace Inference API 进行预测：

```python
import requests

# 方法一：使用 HuggingFace Inference API
API_URL = "https://api-inference.huggingface.co/models/xiajingfeng/shufa"
headers = {"Authorization": "Bearer YOUR_API_TOKEN"}

def query(filename):
    with open(filename, "rb") as f:
        data = f.read()
    response = requests.post(API_URL, headers=headers, data=data)
    return response.json()

# 方法二：使用 HuggingFace Space (Gradio UI)
# 直接通过 HTTP 请求调用 Space 的 API
SPACE_URL = "https://xiajingfeng-shufa.hf.space"
```

### 3. 返回结果

模型返回识别结果，包括：

```json
{
  "label": "行书",
  "confidence": 0.85,
  "scores": [
    {"label": "行书", "score": 0.85},
    {"label": "楷书", "score": 0.10},
    {"label": "草书", "score": 0.03},
    {"label": "篆书", "score": 0.01},
    {"label": "隶书", "score": 0.01}
  ]
}
```

## 识别流程

```
用户上传书法图片
    │
    ▼
图片预处理
    │
    ├── 格式转换
    ├── 尺寸调整
    └── 质量检查
    │
    ▼
调用识别模型
    │
    ├── API 请求
    ├── 模型推理
    └── 结果解析
    │
    ▼
返回识别结果
    │
    ├── 字体类型
    ├── 置信度
    └── 备选字体
```

## 使用示例

### 示例 1：识别上传的图片

**用户输入**：
> 请识别这张书法图片是什么字体？

（上传书法图片）

**处理流程**：
1. 接收用户上传的图片
2. 进行图片预处理
3. 调用书法识别 API
4. 返回识别结果

**返回结果**：
> 识别结果：**行书**（置信度 85%）
> 
> 备选字体：楷书（10%）、草书（3%）

### 示例 2：识别图片URL

**用户输入**：
> 识别这个链接中的书法字体：https://example.com/calligraphy.jpg

**处理流程**：
1. 下载图片
2. 调用识别 API
3. 返回结果

## 注意事项

1. **图片质量**：识别效果与图片质量密切相关，建议使用清晰、完整的书法图片
2. **图片内容**：图片中应包含完整的汉字，避免只识别单个笔画
3. **混合字体**：如果图片中包含多种字体，模型会返回主要字体
4. **API 限制**：注意 HuggingFace API 的调用频率限制

## 错误处理

| 错误类型 | 说明 | 处理方式 |
|----------|------|----------|
| 图片格式不支持 | 上传了不支持的图片格式 | 提示用户使用支持的格式 |
| 图片过大 | 图片超过 API 限制 | 自动压缩或提示用户 |
| API 调用失败 | 网络问题或 API 不可用 | 重试或提示稍后重试 |
| 识别失败 | 模型无法识别 | 返回"无法识别"并说明原因 |

## 相关工具

本技能可能需要使用以下工具：

- `images_understand` - 图片理解分析
- `extract_content_from_websites` - 从网页提取图片
- `images_search_and_download` - 搜索并下载图片
- `image_synthesize` - 图片合成（生成书法风格图片）

## 扩展功能

除了基本的字体识别，还可以扩展以下功能：

1. **字体风格分析**：分析书法的具体风格特点
2. **作者推断**：根据风格推断可能的书法家
3. **年代鉴定**：估计书法作品的大致年代
4. **临摹建议**：提供临摹建议和学习路径
