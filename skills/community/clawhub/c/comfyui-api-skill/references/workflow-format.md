# ComfyUI 工作流格式规范

本文档说明 ComfyUI 工作流 JSON 的结构、节点定义和使用示例。

## 目录

- [工作流结构](#工作流结构)
- [节点定义](#节点定义)
- [连接规则](#连接规则)
- [常见节点类型](#常见节点类型)
- [完整示例](#完整示例)
- [最佳实践](#最佳实践)

## 工作流结构

ComfyUI 工作流是一个 JSON 对象，包含以下主要部分：

```json
{
  "node_id_1": {
    "inputs": {
      // 节点输入参数
    },
    "class_type": "NodeClassName",
    "_meta": {
      "title": "节点标题"
    }
  },
  "node_id_2": {
    // ...
  }
}
```

### 结构说明

1. **顶层键**：节点 ID（字符串，唯一标识）
2. **inputs**：节点的输入参数和连接
3. **class_type**：节点类型（对应 `/object_info` 中的节点名）
4. **_meta**：元数据（可选，用于 UI 显示）

## 节点定义

### inputs 结构

`inputs` 字段包含两类内容：

#### 1. 参数值（直接值）

```json
{
  "inputs": {
    "seed": 12345,
    "steps": 20,
    "cfg": 7.5,
    "sampler_name": "euler",
    "width": 512,
    "height": 512,
    "prompt": "a beautiful landscape"
  }
}
```

#### 2. 连接引用（从其他节点获取）

```json
{
  "inputs": {
    "model": ["node_id_1", 0],
    "positive": ["node_id_2", 0],
    "latent_image": ["node_id_3", 0]
  }
}
```

**连接格式**：`["源节点ID", 输出索引]`
- 第一个元素：源节点的 ID
- 第二个元素：源节点输出的索引（从 0 开始）

## 连接规则

### 数据类型匹配

每个节点的输入和输出都有特定的数据类型，必须匹配：

| 类型标识 | 说明 | 示例节点 |
|---------|------|---------|
| `MODEL` | 模型 | CheckpointLoader |
| `CLIP` | 文本编码器 | CheckpointLoader |
| `VAE` | 变分自编码器 | CheckpointLoader |
| `CONDITIONING` | 条件编码 | CLIPTextEncode |
| `LATENT` | 潜空间数据 | EmptyLatentImage |
| `IMAGE` | 图像数据 | LoadImage, VAEDecode |
| `MASK` | 蒙版 | LoadImage |

### 连接示例

```json
{
  "3": {
    "inputs": {
      "seed": 12345,
      "steps": 20,
      "cfg": 7.5,
      "sampler_name": "euler",
      "scheduler": "normal",
      "model": ["4", 0],          // 从节点 4 的第 0 个输出获取 MODEL
      "positive": ["6", 0],       // 从节点 6 的第 0 个输出获取 CONDITIONING
      "negative": ["7", 0],       // 从节点 7 的第 0 个输出获取 CONDITIONING
      "latent_image": ["5", 0]    // 从节点 5 的第 0 个输出获取 LATENT
    },
    "class_type": "KSampler"
  }
}
```

## 常见节点类型

### 1. CheckpointLoaderSimple

加载模型检查点。

```json
{
  "4": {
    "inputs": {
      "ckpt_name": "v1-5-pruned-emaonly.safetensors"
    },
    "class_type": "CheckpointLoaderSimple",
    "_meta": {
      "title": "Load Checkpoint"
    }
  }
}
```

**输出**：
- 0: MODEL
- 1: CLIP
- 2: VAE

### 2. CLIPTextEncode

使用 CLIP 编码文本提示词。

```json
{
  "6": {
    "inputs": {
      "text": "a beautiful landscape, high quality, detailed",
      "clip": ["4", 1]            // 从 CheckpointLoader 获取 CLIP
    },
    "class_type": "CLIPTextEncode",
    "_meta": {
      "title": "CLIP Text Encode (Positive)"
    }
  }
}
```

**输出**：
- 0: CONDITIONING

### 3. EmptyLatentImage

创建空的潜空间图像。

```json
{
  "5": {
    "inputs": {
      "width": 512,
      "height": 512,
      "batch_size": 1
    },
    "class_type": "EmptyLatentImage",
    "_meta": {
      "title": "Empty Latent Image"
    }
  }
}
```

**输出**：
- 0: LATENT

### 4. KSampler

核心采样器节点。

```json
{
  "3": {
    "inputs": {
      "seed": 12345,
      "steps": 20,
      "cfg": 7.5,
      "sampler_name": "euler",
      "scheduler": "normal",
      "denoise": 1.0,
      "model": ["4", 0],
      "positive": ["6", 0],
      "negative": ["7", 0],
      "latent_image": ["5", 0]
    },
    "class_type": "KSampler",
    "_meta": {
      "title": "KSampler"
    }
  }
}
```

**参数说明**：
- `seed`：随机种子
- `steps`：采样步数
- `cfg`：引导强度
- `sampler_name`：采样器名称
- `scheduler`：调度器类型
- `denoise`：去噪强度（1.0 表示完全去噪）

**输出**：
- 0: LATENT

### 5. VAEDecode

将潜空间图像解码为像素图像。

```json
{
  "8": {
    "inputs": {
      "samples": ["3", 0],        // 从 KSampler 获取 LATENT
      "vae": ["4", 2]             // 从 CheckpointLoader 获取 VAE
    },
    "class_type": "VAEDecode",
    "_meta": {
      "title": "Decode Latent"
    }
  }
}
```

**输出**：
- 0: IMAGE

### 6. SaveImage

保存图像到输出目录。

```json
{
  "9": {
    "inputs": {
      "filename_prefix": "ComfyUI",
      "images": ["8", 0]          // 从 VAEDecode 获取 IMAGE
    },
    "class_type": "SaveImage",
    "_meta": {
      "title": "Save Image"
    }
  }
}
```

**输出**：无（保存到磁盘）

### 7. LoadImage

加载输入图像。

```json
{
  "10": {
    "inputs": {
      "image": "example.png",
      "upload": "image"
    },
    "class_type": "LoadImage",
    "_meta": {
      "title": "Load Image"
    }
  }
}
```

**输出**：
- 0: IMAGE
- 1: MASK

## 完整示例

### 基础文生图工作流

```json
{
  "3": {
    "inputs": {
      "seed": 123456789,
      "steps": 20,
      "cfg": 7.5,
      "sampler_name": "euler",
      "scheduler": "normal",
      "denoise": 1.0,
      "model": ["4", 0],
      "positive": ["6", 0],
      "negative": ["7", 0],
      "latent_image": ["5", 0]
    },
    "class_type": "KSampler"
  },
  "4": {
    "inputs": {
      "ckpt_name": "v1-5-pruned-emaonly.safetensors"
    },
    "class_type": "CheckpointLoaderSimple"
  },
  "5": {
    "inputs": {
      "width": 512,
      "height": 512,
      "batch_size": 1
    },
    "class_type": "EmptyLatentImage"
  },
  "6": {
    "inputs": {
      "text": "a beautiful landscape, high quality, detailed, 8k",
      "clip": ["4", 1]
    },
    "class_type": "CLIPTextEncode"
  },
  "7": {
    "inputs": {
      "text": "low quality, blurry, distorted",
      "clip": ["4", 1]
    },
    "class_type": "CLIPTextEncode"
  },
  "8": {
    "inputs": {
      "samples": ["3", 0],
      "vae": ["4", 2]
    },
    "class_type": "VAEDecode"
  },
  "9": {
    "inputs": {
      "filename_prefix": "ComfyUI",
      "images": ["8", 0]
    },
    "class_type": "SaveImage"
  }
}
```

### 图生图工作流

```json
{
  "load_image": {
    "inputs": {
      "image": "reference.png"
    },
    "class_type": "LoadImage"
  },
  "vae_encode": {
    "inputs": {
      "pixels": ["load_image", 0],
      "vae": ["checkpoint", 2]
    },
    "class_type": "VAEEncode"
  },
  "checkpoint": {
    "inputs": {
      "ckpt_name": "v1-5-pruned-emaonly.safetensors"
    },
    "class_type": "CheckpointLoaderSimple"
  },
  "positive": {
    "inputs": {
      "text": "style transfer, artistic, vibrant colors",
      "clip": ["checkpoint", 1]
    },
    "class_type": "CLIPTextEncode"
  },
  "negative": {
    "inputs": {
      "text": "low quality, blurry",
      "clip": ["checkpoint", 1]
    },
    "class_type": "CLIPTextEncode"
  },
  "sampler": {
    "inputs": {
      "seed": 987654321,
      "steps": 30,
      "cfg": 7.5,
      "sampler_name": "euler_ancestral",
      "scheduler": "karras",
      "denoise": 0.75,
      "model": ["checkpoint", 0],
      "positive": ["positive", 0],
      "negative": ["negative", 0],
      "latent_image": ["vae_encode", 0]
    },
    "class_type": "KSampler"
  },
  "decode": {
    "inputs": {
      "samples": ["sampler", 0],
      "vae": ["checkpoint", 2]
    },
    "class_type": "VAEDecode"
  },
  "save": {
    "inputs": {
      "filename_prefix": "img2img_output",
      "images": ["decode", 0]
    },
    "class_type": "SaveImage"
  }
}
```

## 最佳实践

### 1. 节点 ID 命名

- 使用有意义的字符串而非纯数字
- 例如：`checkpoint`、`positive_prompt`、`negative_prompt`、`sampler`

### 2. 参数优化

**采样步数**：
- 快速预览：10-15 步
- 标准质量：20-30 步
- 高质量：40-50 步

**CFG 值**：
- 标准范围：7-12
- 较低值（5-7）：更自由、创意性强
- 较高值（10-15）：更严格遵循提示词

**采样器选择**：
- `euler`：快速、稳定
- `euler_ancestral`：增加随机性，更自然
- `dpmpp_2m`：高质量、效率高

### 3. 提示词技巧

**正向提示词**：
- 描述主体：`a beautiful woman`
- 添加质量词：`high quality, detailed, 8k`
- 添加风格词：`cinematic lighting, professional photography`

**负向提示词**：
- 质量相关：`low quality, blurry, distorted`
- 内容相关：`watermark, text, signature`
- 构图相关：`bad anatomy, extra limbs`

### 4. 工作流调试

1. **验证节点存在**：使用 `/object_info` 检查节点类型
2. **验证模型存在**：使用 `/models` 检查模型文件
3. **检查连接类型**：确保数据类型匹配
4. **查看错误日志**：ComfyUI 会输出详细的错误信息

### 5. 性能优化

- **批处理**：使用 `batch_size` 同时生成多张图
- **分辨率**：使用 512x512 或 768x768 可获得最佳速度
- **模型选择**：SD 1.5 比 SD XL 更快

### 6. 种子控制

- 固定种子：确保可复现结果
- 随机种子：使用当前时间戳或随机数
- 批量生成：使用不同种子生成多个变体

```python
import random
seed = random.randint(0, 2**32 - 1)
```

## 工作流验证

在提交工作流前，建议验证：

1. **JSON 格式**：确保是有效的 JSON
2. **节点类型**：所有 `class_type` 都存在于 `/object_info`
3. **模型文件**：所有引用的模型都存在于 `/models`
4. **连接完整性**：所有连接引用的节点 ID 都存在
5. **类型匹配**：所有连接的数据类型都匹配

## 参考资源

- [ComfyUI 官方文档](https://docs.comfy.org/)
- [ComfyUI 节点参考](https://docs.comfy.org/development/comfyui-server/comms_routes)
- [ComfyUI 示例工作流](https://github.com/comfyanonymous/ComfyUI_examples)
