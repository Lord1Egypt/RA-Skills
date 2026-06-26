# ComfyUI API 规范

本文档详细说明 ComfyUI 原生 HTTP / WebSocket API 的端点、请求格式和响应格式。

## 目录

- [执行相关](#执行相关)
- [文件相关](#文件相关)
- [发现与能力探测](#发现与能力探测)
- [WebSocket 实时通信](#websocket-实时通信)
- [错误处理](#错误处理)

## 执行相关

### POST /prompt

提交工作流执行任务。

**请求方法**：POST

**请求头**：
```
Content-Type: application/json
Authorization: Bearer <API_KEY>  # 可选，如果启用了鉴权
```

**请求体**：
```json
{
  "prompt": {
    // 工作流 JSON，详见 workflow-format.md
  },
  "client_id": "unique_client_id"  // 可选，用于 WebSocket 消息路由
}
```

**响应**：
```json
{
  "prompt_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
  "number": 1
}
```

**错误响应**：
```json
{
  "error": {
    "type": "invalid_prompt",
    "message": "工作流格式错误"
  }
}
```

### GET /history/{prompt_id}

查询指定任务的执行历史。

**请求方法**：GET

**路径参数**：
- `prompt_id`：任务 ID

**响应**：
```json
{
  "a1b2c3d4-e5f6-7890-abcd-ef1234567890": {
    "prompt": {
      // 原始工作流
    },
    "outputs": {
      "node_id_1": {
        "images": [
          {
            "filename": "output_001.png",
            "subfolder": "",
            "type": "output"
          }
        ]
      },
      "node_id_2": {
        "videos": [
          {
            "filename": "output_video.mp4",
            "subfolder": "",
            "type": "output"
          }
        ]
      },
      "node_id_3": {
        "audio": [
          {
            "filename": "output_audio.wav",
            "subfolder": "",
            "type": "output"
          }
        ]
      },
      "node_id_4": {
        "files": [
          {
            "filename": "model.glb",
            "subfolder": "",
            "type": "output"
          }
        ]
      }
    },
    "status": {
      "status_str": "success",
      "completed": true,
      "messages": []
    }
  }
}
```

**输出类型说明**：
- `images`：图像文件（PNG、JPEG、WebP、GIF 等）
- `videos`：视频文件（MP4、AVI、MOV、WebM 等）
- `audio`：音频文件（MP3、WAV、OGG、FLAC 等）
- `files`：其他文件（3D模型、GIF动画、数据文件等）
```

### GET /queue

查看当前执行队列。

**请求方法**：GET

**响应**：
```json
{
  "queue_running": [
    {
      "prompt_id": "task-id-1",
      "prompt": {}
    }
  ],
  "queue_pending": [
    {
      "prompt_id": "task-id-2",
      "prompt": {}
    }
  ]
}
```

### POST /queue

管理队列（清除队列）。

**请求方法**：POST

**请求体**：
```json
{
  "clear": true
}
```

**响应**：
```json
{
  "success": true
}
```

### POST /interrupt

中断当前正在执行的任务。

**请求方法**：POST

**响应**：
```json
{
  "success": true
}
```

### POST /free

释放内存（卸载模型）。

**请求方法**：POST

**请求体**：
```json
{
  "unload_models": true,    // 是否卸载模型
  "free_memory": 0.5        // 释放内存比例 (0.0-1.0)
}
```

**响应**：
```json
{
  "success": true
}
```

### POST /history

清理执行历史。

**请求方法**：POST

**请求体**：
```json
{
  "clear": true              // 清空所有历史
}
```

或

```json
{
  "delete": ["prompt_id_1", "prompt_id_2"]  // 删除指定历史
}
```

**响应**：
```json
{
  "success": true
}
```

### GET /prompt

获取当前队列状态和执行信息。

**请求方法**：GET

**响应**：
```json
{
  "exec_info": {
    "queue_remaining": 2
  },
  "queue_running": [
    {
      "prompt_id": "task-id-1",
      "prompt": {}
    }
  ],
  "queue_pending": [
    {
      "prompt_id": "task-id-2",
      "prompt": {}
    }
  ]
}
```

## 文件相关

### GET /view

下载输出文件。

**请求方法**：GET

**查询参数**：
- `filename`：文件名（必需）
- `type`：文件类型（可选，默认：output）
- `subfolder`：子文件夹（可选）
- `preview`：预览模式（可选）

**请求示例**：
```
GET /view?filename=output_001.png&type=output&subfolder=
```

**响应**：
- 成功：返回文件二进制数据（Content-Type: image/png）
- 失败：返回错误 JSON

### POST /upload/image

上传文件到 ComfyUI（支持多种文件类型）。

**请求方法**：POST

**请求头**：
```
Content-Type: multipart/form-data
```

**请求体**（multipart/form-data）：
- `image`：文件数据（必需）- 支持图像、视频、音频、模型等多种类型
- `subfolder`：子文件夹路径（可选）
- `overwrite`：是否覆盖（可选，默认：true）
- `type`：文件类型标识（可选，如 'input', 'output', 'temp'）

**支持的文件类型**：
- **图像**：PNG, JPG, JPEG, WebP, GIF, BMP, TIFF, EXR
- **视频**：MP4, AVI, MOV, MKV, WebM, FLV
- **音频**：MP3, WAV, OGG, FLAC, AAC, M4A
- **模型**：OBJ, GLTF, GLB, FBX, STL
- **其他**：JSON, TXT, CSV 等

**响应**：
```json
{
  "name": "uploaded_file.mp4",
  "subfolder": "input",
  "type": "input"
}
```

**注意**：
- 此端点可处理多种文件类型，不仅限于图像
- 大文件上传可能需要较长时间，建议设置足够的超时时间
- 上传的文件可在工作流中通过文件名引用

### POST /upload/mask

上传蒙版文件。

**请求方法**：POST

**请求头**：
```
Content-Type: multipart/form-data
```

**请求体**（multipart/form-data）：
- `mask`：蒙版文件（必需）
- `subfolder`：子文件夹路径（可选）
- `overwrite`：是否覆盖（可选，默认：true）

**响应**：
```json
{
  "name": "uploaded_mask.png",
  "subfolder": "input",
  "type": "input"
}
```

## 发现与能力探测

## 发现与能力探测

### GET /object_info

获取所有节点的定义信息。

**请求方法**：GET

**查询参数**：
- `node_id`：指定节点 ID（可选，不传则返回所有节点）

**响应**：
```json
{
  "KSampler": {
    "input": {
      "required": {
        "model": ["MODEL", {}],
        "seed": ["INT", {"default": 0, "min": 0, "max": 18446744073709552000}],
        "steps": ["INT", {"default": 20, "min": 1, "max": 10000}],
        "cfg": ["FLOAT", {"default": 8.0, "min": 0.0, "max": 100.0}],
        "sampler_name": ["sampler_name", ["euler", "euler_ancestral", ...]],
        "scheduler": ["scheduler", ["normal", "karras", ...]],
        "positive": ["CONDITIONING", {}],
        "negative": ["CONDITIONING", {}],
        "latent_image": ["LATENT", {}]
      }
    },
    "output": ["LATENT"],
    "category": "sampling"
  }
}
```

### GET /object_info/{node_class}

获取单个节点类型的详细信息。

**请求方法**：GET

**路径参数**：
- `node_class`：节点类名（如 KSampler, CheckpointLoaderSimple）

**响应**：同 GET /object_info，但只返回指定节点的信息

### GET /models

获取可用的模型列表。

**请求方法**：GET

**响应**：
```json
{
  "checkpoints": [
    "v1-5-pruned-emaonly.safetensors",
    "sd_xl_base_1.0.safetensors"
  ],
  "loras": [
    "lora_model.safetensors"
  ],
  "vae": [
    "vae-ft-mse-840000.safetensors"
  ],
  "controlnet": [
    "control_v11p_sd15_canny.safetensors"
  ]
}
```

### GET /models/{folder}

获取特定文件夹中的模型列表。

**请求方法**：GET

**路径参数**：
- `folder`：模型文件夹名（如 checkpoints, loras, vae, controlnet）

**响应**：
```json
[
  "model1.safetensors",
  "model2.safetensors"
]
```

### GET /embeddings

获取可用的 embeddings 列表。

**请求方法**：GET

**响应**：
```json
[
  "easynegative",
  "bad_prompt",
  "embedding_name"
]
```

### GET /extensions

获取已安装的扩展列表。

**请求方法**：GET

**响应**：
```json
[
  "ComfyUI-Manager",
  "was-node-suite-comfyui",
  "ComfyUI-Impact-Pack"
]
```

### GET /features

获取服务器功能特性。

**请求方法**：GET

**响应**：
```json
{
  "front_end_version": "1.0.0",
  "feature_x": true,
  "feature_y": false
}
```

### GET /view_metadata/{filename}

获取模型元数据。

**请求方法**：GET

**路径参数**：
- `filename`：模型文件名

**响应**：
```json
{
  "model_name": "sd_xl_base",
  "model_type": "SDXL",
  "architecture": "stable-diffusion-xl-v1-base",
  "format": "safetensors"
}
```

### GET /workflow_templates

获取工作流模板映射。

**请求方法**：GET

**响应**：
```json
{
  "custom_node_module_1": {
    "template_name": "template_workflow.json"
  }
}
```

### GET /system_stats

获取系统资源信息。

**请求方法**：GET

**响应**：
```json
{
  "system": {
    "os": "Linux",
    "python_version": "3.10.12",
    "comfyui_version": "v0.2.0"
  },
  "devices": [
    {
      "name": "NVIDIA GeForce RTX 4090",
      "type": "cuda",
      "vram_total": 25769803776,
      "vram_used": 8589934592
    }
  ]
}
```

## WebSocket 实时通信

### WS /ws

建立 WebSocket 连接以接收实时进度更新。

**连接 URL**：
```
ws://127.0.0.1:8188/ws?clientId=<client_id>
```

**消息类型**：

#### 1. 进度更新
```json
{
  "type": "progress",
  "data": {
    "value": 10,
    "max": 20
  }
}
```

#### 2. 执行开始
```json
{
  "type": "executing",
  "data": {
    "node": "node_id",
    "prompt_id": "task-id"
  }
}
```

#### 3. 执行完成
```json
{
  "type": "executed",
  "data": {
    "node": "node_id",
    "prompt_id": "task-id",
    "output": {
      "images": [...]
    }
  }
}
```

#### 4. 执行状态
```json
{
  "type": "execution_status",
  "data": {
    "status_str": "running",
    "prompt_id": "task-id"
  }
}
```

#### 5. 错误
```json
{
  "type": "execution_error",
  "data": {
    "prompt_id": "task-id",
    "node_id": "node_id",
    "error": "错误信息"
  }
}
```

## 错误处理

### HTTP 状态码

- `200 OK`：请求成功
- `400 Bad Request`：请求格式错误
- `401 Unauthorized`：未授权（需要 API Key）
- `404 Not Found`：资源不存在
- `500 Internal Server Error`：服务器内部错误

### 错误响应格式

```json
{
  "error": {
    "type": "error_type",
    "message": "详细错误信息",
    "details": {}
  }
}
```

### 常见错误类型

1. **invalid_prompt**：工作流 JSON 格式错误
2. **node_not_found**：节点类型不存在
3. **model_not_found**：模型文件不存在
4. **execution_error**：执行过程中出错
5. **out_of_memory**：GPU 内存不足

## 基础 URL 配置

默认情况下，ComfyUI 服务运行在：
- HTTP：`http://127.0.0.1:8188`
- WebSocket：`ws://127.0.0.1:8188`

可以通过环境变量或命令行参数修改：
- 环境变量：`COMFYUI_SERVER_URL`
- 命令行参数：`--server-url`

## API Key 鉴权

ComfyUI 支持可选的 API Key 鉴权机制。

**配置方式**：
1. 在 ComfyUI 启动时设置 API Key
2. 在请求头中添加：`Authorization: Bearer <API_KEY>`

**注意**：
- 默认情况下无需鉴权
- 如果 ComfyUI 启用了鉴权，未提供 API Key 的请求将被拒绝
