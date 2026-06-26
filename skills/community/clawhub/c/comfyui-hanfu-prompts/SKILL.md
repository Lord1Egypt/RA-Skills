---
name: comfyui-hanfu-prompts
description: 14套已验证的 ComfyUI Z-Image 汉服写真/王家卫风格/杂志封面提示词模板，搭配双采样工作流直出高质量图。RTX 5070 12GB+ 可用。
---

# ComfyUI 汉服写真 · 提示词模板包

14 套已验证的双采样提示词模板 + 一键批量出图。

## 触发条件

当用户需要以下任一场景时激活：
- "帮我生成一张汉服写真"
- "生成王家卫风格的图"
- "做一张杂志封面"
- "批量出汉服图"
- "用双采样生成高质量图"

## 前置条件

- ComfyUI 已启动（默认 127.0.0.1:8000）
- Z-Image Turbo + Qwen CLIP + VAE 模型已加载
- `pip install comfy-batch`

## 14 套提示词模板

### 汉服写真 (5套)
| 模板 | 风格 | 调用方式 |
|------|------|---------|
| 唐风仕女 | 红金宫殿、樱花、黄昏光 | `HANFU_TANG` |
| 宋制素雅 | 蓝白、竹林荷塘、晨雾 | `HANFU_SONG` |
| 明制端庄 | 深蓝金绣、凤冠、书房烛光 | `HANFU_MING` |
| 魏晋风骨 | 白衣飘逸、山崖云雾 | `HANFU_WEIJIN` |
| 明艳宫装 | 红金凤冠、故宫大殿 | `HANFU_PALACE` |

### 王家卫电影风格 (3套)
| 模板 | 风格 | 调用方式 |
|------|------|---------|
| 花样年华 | 霓虹、雨窗、烟、颗粒 | `WKW_MOOD` |
| 重庆森林 | 鱼缸蓝光、凌晨4点、潮湿 | `WKW_CHUNGKING` |
| 堕落天使 | 浴室雾镜、荧光红绿 | `WKW_FALLEN` |

### 杂志封面 (4套)
| 模板 | 风格 | 调用方式 |
|------|------|---------|
| VOGUE中国版 | 红色高定、纯白背景 | `MAG_VOGUE` |
| 时尚芭莎 | 黑白雕塑、负空间 | `MAG_BAZAAR` |
| ELLE港版 | 霓虹街头、都市时尚 | `MAG_ELLE` |
| COSMO | 海滩夏日、活力 | `MAG_COSMO` |

## 使用方式

```python
from comfy_batch import ZImage
from prompt_templates import HANFU_TANG, WKW_MOOD, MAG_VOGUE

z = ZImage()
z.generate(HANFU_TANG, double_sample=True)  # 双采样高质量
z.generate(WKW_MOOD, double_sample=True)
```

批量生成：
```python
from prompt_templates import ALL_TEMPLATES
for key, (name, prompt) in ALL_TEMPLATES.items():
    z.generate(prompt, double_sample=True)
```

## 技术细节

- **模型**: Z-Image Turbo (DiT)
- **工作流**: 双采样 (768×1024→1024×1536, 6步结构+4步细节, denoise=0.35)
- **显存**: 12GB+ (RTX 5070 测试通过)
- **出图速度**: 单张 ~45秒（双采样）/ ~25秒（普通）

## 许可

MIT — 可商用。生成的图片归你所有。

## 来源

- 云曦 AI 桌面女友项目出品
- GitHub: https://github.com/lantianbaicai/comfyui-hanfu-prompts
- 配套工具: https://github.com/lantianbaicai/comfy-batch
