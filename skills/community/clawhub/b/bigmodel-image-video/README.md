# 图片与视频生成技能

使用智谱 AI 的 BigModel API (CogView/CogVideoX) 生成高质量图片和视频。

## 目录结构

```
image-video-generation/
├── SKILL.md              # 技能文档（主要文档）
├── README.md             # 本文件
├── lib/                  # 核心库
│   └── image_video.py    # Python 模块
└── examples/             # 示例代码
    ├── simple_image.py   # 简单图片生成
    ├── batch_images.py   # 批量图片生成
    └── video_generation.py  # 视频生成
```

## 快速开始

### 1. 环境准备

设置 API Key（必需）：
```bash
export BIGMODEL_API_KEY=your_api_key_here
```

或添加到 shell 配置文件（~/.zshrc 或 ~/.bashrc）：
```bash
echo 'export BIGMODEL_API_KEY=your_api_key_here' >> ~/.zshrc
source ~/.zshrc
```

### 2. 安装依赖

```bash
pip install requests
```

或使用 uv：
```bash
uv add requests
```

### 3. 运行示例

```bash
# 简单图片生成
python examples/simple_image.py

# 批量图片生成
python examples/batch_images.py

# 视频生成
python examples/video_generation.py
```

## 核心功能

### 图片生成

```python
from lib.image_video import generate_image

result = generate_image(
    prompt="一只可爱的橘猫",
    model="cogview-3-flash",  # 可选：cogview-4, cogview-4-250304
    quality="standard",        # 可选：hd
    size="1024x1024"          # 可选：1024x1792, 1792x1024
)
image_url = result["data"][0]["url"]
```

### 批量图片生成

```python
from lib.image_video import batch_generate_images

prompts = ["日出", "日落", "星空", "彩虹"]
results = batch_generate_images(prompts, max_concurrent=2)
```

### 视频生成

```python
from lib.image_video import generate_video, wait_for_video

# 启动视频生成
video = generate_video(prompt="一朵花在阳光下缓缓开放", duration=5)
task_id = video["id"]

# 等待生成完成
final = wait_for_video(task_id)
video_url = final["video_result"][0]["url"]
```

## 模型选择

### 图片模型

| 模型 | 速度 | 质量 | 适用场景 |
|------|------|------|---------|
| cogview-3-flash | ⚡ 快 | ⭐⭐⭐ | 快速预览、大批量生成 |
| cogview-4-250304 | 🐢 中 | ⭐⭐⭐⭐ | 精细化生成 |
| cogview-4 | 🐌 慢 | ⭐⭐⭐⭐⭐ | 专业级高质量图片 |

### 视频模型

| 模型 | 速度 | 质量 | 适用场景 |
|------|------|------|---------|
| cogvideox-flash | ⚡ 快 | ⭐⭐⭐ | 快速预览 |
| cogvideox-2 | 🐢 中 | ⭐⭐⭐⭐ | 标准视频 |
| cogvideox-3 | 🐌 慢 | ⭐⭐⭐⭐⭐ | 高质量长视频 |

## 完整文档

详细使用指南请参考 [SKILL.md](./SKILL.md)

## 获取 API Key

访问 [智谱 AI BigModel 开放平台](https://open.bigmodel.cn/) 注册并获取 API Key。
