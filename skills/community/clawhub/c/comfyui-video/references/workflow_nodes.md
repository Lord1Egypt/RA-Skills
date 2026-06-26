# LTX-2.3 工作流节点参考

## 完整节点 ID 映射

基于 `LTX-2.3_T2V_I2V_Single_Stage_Distilled_Full.json` (44 节点)

### 核心节点

| 节点类型 | ID | 功能 | 关键参数 |
|----------|-----|------|----------|
| LoadImage | 2004 | 输入参考图 (I2V) | `image`: 文件名 |
| CLIPTextEncode | 2483 | 正面提示词 | `text`: prompt |
| CLIPTextEncode | 2612 | 负面提示词 | `text`: negative prompt |
| EmptyLTXVLatentVideo | 3059 | 空 latent | `width`, `height`, `length` |
| LTXVScheduler | 4966 | 采样器 | `steps`, `length`, `base_resolution` |
| LoraLoaderModelOnly | 4922 | LoRA | `lora_name`, `strength_model` |
| SaveVideo | 4823, 4852 | 输出 | `filename_prefix` |
| CreateVideo | 4819, 4849 | 视频创建 | `fps` (默认 24) |

### 模型加载节点

| 节点类型 | ID | 功能 |
|----------|-----|------|
| UNETLoader | - | 加载 LTX-2.3 主模型 |
| CLIPLoader | - | 加载 Gemma 3 文本编码器 |
| VAELoader | - | 加载 Video VAE |
| LoraLoaderModelOnly | 4922, 4968 | 加载 Distilled LoRA |

### 后处理节点

| 节点类型 | ID | 功能 |
|----------|-----|------|
| LTXVAudioVAEDecode | 4818, 4848 | 音频 VAE 解码 |
| VAEDecodeTiled | 4822, 4851 | 瓦片式 VAE 解码 |

## 常用修改点

### 切换 T2V / I2V

- **T2V**: 禁用 LoadImage 节点 (`node.mode = 4`)
- **I2V**: 启用 LoadImage 节点 (`node.mode = 0`)

### 修改输出分辨率

在 `EmptyLTXVLatentVideo` 节点设置：
- `width`: 1024
- `height`: 576
- `length`: 72 (帧数)

### 修改采样参数

在 `LTXVScheduler` 节点设置：
- `steps`: 15 或 25
- `length`: 与 latent 一致

## 工作流文件位置

```
工作流: /workspace/ComfyUI/custom_nodes/ComfyUI-LTXVideo/example_workflows/2.3/
蓝图: /workspace/ComfyUI/blueprints/
```
