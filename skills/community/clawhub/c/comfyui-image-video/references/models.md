# ComfyUI + Flux 模型参考

## 模型文件

| 文件 | 位置 | 大小 | 用途 |
|------|------|------|------|
| flux1-schnell.safetensors | models/unet/ | 23.8GB | UNet 扩散模型主体 |
| ae.safetensors | models/vae/ | 335MB | VAE 解码器 |
| clip_l.safetensors | models/clip/ | 250MB | CLIP-L 文本编码器 |
| t5xxl_fp16.safetensors | models/clip/ | 9.8GB | T5-XXL 文本编码器 |

## 模型来源

- ModelScope（魔搭）国内源下载，无需翻墙
- UNet + VAE: `AI-ModelScope/FLUX.1-schnell`
- CLIP 编码器: `comfyanonymous/flux_text_encoders`

## Flux 模型变体

| 变体 | 步数 | 质量 | 显存 |
|------|------|------|------|
| schnell | 4步 | 高 | 16GB够用(fp8) |
| dev | ~20步 | 更高 | 16GB紧(需量化) |

## Schnell 参数推荐

- steps: 4 (最佳值，不要改)
- cfg: 1.0
- sampler: euler
- scheduler: simple
- 分辨率: 1024×1024 (也支持 512×512, 768×1344 等非正方形)

## API 端点

- `POST /prompt` - 提交工作流
- `GET /history/{prompt_id}` - 查询结果
- `GET /system_stats` - 服务器状态
- `GET /view?filename=xxx&subfolder=yyy` - 获取图片
