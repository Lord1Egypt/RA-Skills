# 硅基流动文生图模型完整列表

## 调用格式统一说明

所有模型均使用同一接口：
```
POST https://api.siliconflow.cn/v1/images/generations
```

---

## FLUX 系列（Black Forest Labs）

### FLUX.1-schnell（推荐首选）
```
model: "black-forest-labs/FLUX.1-schnell"
特点：速度最快（2-4秒），质量优秀，部分规格免费
适合：日常使用，快速出图，原型验证
推荐参数：
  steps: 4-20（schnell专用，步数少效果已很好）
  guidance_scale: 不支持（schnell模型特性）
  image_size: 1024x1024
```

### FLUX.1-dev（最高质量）
```
model: "black-forest-labs/FLUX.1-dev"
特点：最高画质，细节丰富，稍慢（5-15秒）
适合：精品创作，商业使用，高要求场景
推荐参数：
  steps: 20-50
  guidance_scale: 3.5（官方推荐）
  image_size: 1024x1024
```

---

## Kolors 系列（快手可图）

### Kolors（中文场景最强）
```
model: "Kwai-Kolors/Kolors"
特点：中文理解最佳，人像优秀，支持负向提示词
适合：中文prompt，人像写真，国风，小红书配图
推荐参数：
  steps: 20-30
  guidance_scale: 7.5
  negative_prompt: "低质量, 模糊, 变形, 多余肢体"
  image_size: 1024x1024 或 1080x1440（小红书）
```

---

## Stable Diffusion 系列（Stability AI）

### SD3-Medium（文字渲染）
```
model: "stabilityai/stable-diffusion-3-medium"
特点：图中文字渲染准确，20亿参数，写实感强
适合：含文字图片，海报，证件类图片
推荐参数：
  steps: 20-30
  guidance_scale: 7.0
```

### SDXL（经典稳定）
```
model: "stabilityai/stable-diffusion-xl-base-1.0"
特点：经典成熟，社区生态丰富
适合：艺术创作，风格多样化
推荐参数：
  steps: 20-40
  guidance_scale: 7.5
```

---

## 参数说明

```
num_inference_steps（推理步数）：
  4-10   : 极快，质量一般（schnell专用）
  20     : 标准，速度与质量平衡（默认推荐）
  30-50  : 高质量，较慢

guidance_scale（提示词引导强度）：
  1-3    : 自由发挥，创意更强
  3.5    : FLUX-dev官方推荐
  7-8    : 标准，提示词遵循度高（Kolors/SDXL）
  10+    : 强制遵循提示词，可能过饱和

negative_prompt（负向提示词）：
  仅 Kolors、SDXL、SD3 支持
  FLUX系列不支持负向提示词

seed（随机种子）：
  固定seed可复现相同图片
  不设置则随机生成

n（批量生成数量）：
  1-4张，默认1
  多张时价格倍增
```

---

## 尺寸支持

```
通用正方形：1024x1024
横版16:9：  1280x720 / 1920x1080
竖版9:16：  720x1280 / 1080x1920
小红书3:4： 1080x1440
宽幅：      1440x1024
```

---

## 价格速查（参考，以官网为准）

```
模型                           参考价格/张
FLUX.1-schnell 1024x1024      免费或极低
FLUX.1-dev 1024x1024          ~¥0.07
Kolors 1024x1024              ~¥0.03
SD3-Medium 1024x1024          ~¥0.07

新用户免费额度约可生成50-200张（视模型而定）
```
