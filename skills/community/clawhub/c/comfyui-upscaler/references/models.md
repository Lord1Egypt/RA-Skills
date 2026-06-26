# 推荐模型

## 放大模型（Upscale Models）

### 通用推荐

| 模型 | 倍数 | 特点 | 适用 |
|------|------|------|------|
| 4x-UltraSharp | 4x | 锐利、清晰、细节好 | 通用，推荐首选 |
| 4x_Nickelback | 4x | 温和、保留纹理 | 人像、风景 |
| RealESRGAN_x4plus | 4x | 平衡、稳定 | 通用 |
| R-ESRGAN_4x_De Bayer | 4x | 适合处理伪影 | 动漫、AI生成图 |

### 人像专用

| 模型 | 倍数 | 特点 |
|------|------|------|
| 4x_Reloaded_UltraSharp | 4x | 皮肤光滑、细节丰富 |
| 4x_Faces_Sharp | 4x | 面部特化 |

### 动漫专用

| 模型 | 倍数 | 特点 |
|------|------|------|
| 4x-UltraSharp | 4x | 动漫也很适用 |
| 1x_Un自然的RCDeBayer | 4x | 动漫线条优化 |
| ultrapunch | 4x | 动漫/插画 |

---

## 基础模型（Base Models）

### SDXL（推荐）

| 模型 | VRAM | 特点 |
|------|------|------|
| sd_xl_base_1.0 | 8GB+ | 细节丰富、构图好 |
| sd_xl_refiner_1.0 | 8GB+ | 可配合 refiner 使用 |

### SD1.5

| 模型 | VRAM | 特点 |
|------|------|------|
| v1-5-pruned-emaonly | 4GB+ | 轻量、兼容性最好 |
| anything-v5 | 4GB+ | 动漫风格 |

### Pony

| 模型 | VRAM | 特点 |
|------|------|------|
| ponyDiffusionV6XL | 8GB+ | 多种风格、标签友好 |
| cyberrealistic_v6 | 8GB+ | 写实风格 |

---

## 模型下载

### 自动下载（通过 ComfyUI Manager）

1. 打开 ComfyUI → Manager
2. 搜索模型名
3. 点击 Install

### 手动下载

**放大模型放置位置：**
```
ComfyUI/models/upscale_models/
```

**基础模型放置位置：**
```
ComfyUI/models/checkpoints/
```

**推荐下载源：**
- HuggingFace: https://huggingface.co/FacehugmanIII/4x_faces_Sharp_Better_higher_quality
- CivitAI: https://civitai.com/models
- OpenModelDB: https://openmodeldb.info/

---

## 模型组合建议

### 写实人像
- 底模: cyberrealistic_v6 / RealisticVision
- 放大: 4x-UltraSharp 或 4x_Nickelback

### 动漫/插画
- 底模: anything-v5 / ponyDiffusionV6XL
- 放大: 4x-UltraSharp 或 R-ESRGAN_4x_De Bayer

### UI/海报
- 底模: sd_xl_base_1.0
- 放大: 4x-UltraSharp
