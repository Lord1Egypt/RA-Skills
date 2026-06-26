# 工作流详解

## 三重放大原理

### 第一步：潜空间放大（Latent Space Upscale）

**原理：** 将图像通过 VAE 编码器压入潜空间，在潜空间进行放大操作，然后加噪声重采样，最后解码回像素空间。

**节点：**
- `LatentScaleByFactor` - 按系数缩放潜空间图像
- `KSampler` - 重采样

**参数建议：**
| 参数 | 建议值 | 说明 |
|------|--------|------|
| scale_by | 2.0 | 放大倍数 |
| denoise | 0.35 | 去噪强度，越高细节越多但可能失真 |
| steps | 20 | 采样步数 |
| cfg | 7-8 | 提示词引导强度 |

**技巧：**
- denoise 0.3-0.4 最常用
- 低于0.2几乎没有新细节
- 高于0.5可能产生过多噪声或失真

---

### 第二步：分区放大（Tile/Block Upscale）

**原理：** 将图像切成小块，分别用放大模型处理，再拼合。可以有效解决大图显存问题。

**节点：**
- `SDUpscale` - 整合了分块、放大、拼接的复合节点

**参数建议：**
| 参数 | 建议值 | 说明 |
|------|--------|------|
| tile_width/height | 1024 | 分块大小，SDXL建议1024+ |
| mask_blur | 8 | 边缘模糊，防止接缝 |
| tile_padding | 256 | 分块重叠区域 |
| seam_fix_width | 64 | 接缝修复宽度 |
| seam_fix_denoise | 0.35 | 接缝修复去噪 |
| denoise | 0.35 | 整体去噪 |

**显存计算：**
- 1024×1024 分块 ≈ 4GB 显存
- 512×512 分块 ≈ 1GB 显存

---

### 第三步：模型放大（Model Upscale）

**原理：** 使用专门的超分辨率模型（如ESRGAN）对整个图像进行锐化和细节增强。

**节点：**
- `ImageUpscaleWithModel` - 使用放大模型处理像素空间图像

**特点：**
- 不添加新细节
- 只增强现有细节的锐度和清晰度
- 作为最后一步"抛光"

---

## 节点连接顺序

```
[CheckpointLoader]
       |
       v
[CLIPTextEncode] ---positive---> [KSampler(latent)]
[CLIPTextEncode] ---negative--->        |
       ^                                 |
       |                            [LatentScale]
       |                                 |
       |                            [KSampler(latent)]
       |                                 |
       +----[VAEDecode] <--- [latent]----+
                |
                v
          [SDUpscale]  <-- [model/upscale_model]
                |
                v
      [ImageUpscaleWithModel]
                |
                v
           [SaveImage]
```

## 故障排除

### 显存不足 (CUDA OOM)
- 减小 tile_size（从1024降到512或768）
- 减小 batch_size
- 使用更低分辨率的底模

### 接缝明显
- 增加 mask_blur（8→16）
- 增加 tile_padding（256→384）
- 增加 seam_fix_width

### 细节丢失
- 增加第一步的 denoise（0.35→0.45）
- 使用更轻量的底模

### 图像失真
- 降低 denoise
- 减少放大倍数
- 换用更稳定的采样器（如 euler_a）
