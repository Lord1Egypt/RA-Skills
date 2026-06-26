---
name: bigmodel-image-video
description: 使用 BigModel (CogView/CogVideoX) API 生成高质量图片和视频。当用户需要"生成图片"、"制作视频"、"AI 绘画"、"创建封面"、"设计海报"、"视觉内容生成"、或任何需要创建图像/视频内容的场景时使用此技能。即使没有明确提到"生成"，只要用户需要创建、设计或制作视觉内容（如小说封面、产品图片、宣传图、短视频等），都应该主动使用此技能。
---

# BigModel 生成图片和视频

使用智谱 AI 的 BigModel API 生成高质量图片和视频。支持单张/批量图片生成、视频生成（含 AI 音频）。

---

## 🚀 快速开始

### 1. 设置 API Key

**必需步骤** - 只需设置一次：

```bash
# 临时设置（当前会话）
export BIGMODEL_API_KEY=your_api_key_here

# 永久设置（推荐）
echo 'export BIGMODEL_API_KEY=your_api_key_here' >> ~/.zshrc
source ~/.zshrc
```

> 获取 API Key：访问 [智谱 AI BigModel 开放平台](https://open.bigmodel.cn/)

### 2. 快速使用

**最简单的方式** - 使用提供的脚本：

```bash
# 生成图片
python scripts/generate.py "一只可爱的橘猫"

# 生成视频
python scripts/generate.py "海边日落" --video

# 批量生成
python scripts/generate.py "日出 日落 星空 彩虹" --batch

# 查看所有选项
python scripts/generate.py --help
```

**编程方式** - 在 Python 代码中使用：

```python
import sys
sys.path.insert(0, '.claude/skills/image-video-generation/lib')

from image_video import generate_image

result = generate_image(prompt="描述内容")
print(result["data"][0]["url"])
```

---

## 📖 使用场景与示例

### 场景 1：小说/书籍封面

```bash
# 武侠小说封面（竖版）
python scripts/generate.py "中国武侠小说封面，水墨画风格，远山如黛，云雾缭绕，一把长剑插在岩石上，月光洒下" --size 1024x1792

# 言情小说封面
python scripts/generate.py "浪漫的粉色花瓣飘落，温柔的夕阳，温暖的色调" --size 1024x1792

# 科幻小说封面
python scripts/generate.py "未来城市，霓虹灯光，赛博朋克风格，高科技感" --size 1024x1792
```

### 场景 2：社交媒体内容

```bash
# 小红书风格图片
python scripts/generate.py "清新文艺风格，自然光线，极简构图，高饱和度"

# 朋友圈配图
python scripts/generate.py "生活记录，温馨日常，柔和光线"

# 头像生成
python scripts/generate.py "可爱的卡通风格猫咪头像，简洁背景"
```

### 场景 3：电商产品图

```bash
# 产品展示
python scripts/generate.py "白色背景上的蓝色运动鞋，专业产品摄影，柔和光线" --quality hd

# 场景展示
python scripts/generate.py "产品放在木质桌面上，温馨的家居环境，自然光"
```

### 场景 4：短视频制作

```bash
# 5秒短视频
python scripts/generate.py "一朵花在阳光下缓缓开放" --video --duration 5

# 10秒高质量视频
python scripts/generate.py "城市夜景，车流穿梭，灯光流动" --video --duration 10 --quality hd
```

### 场景 5：批量生成

```bash
# 批量生成不同风格的图片
python scripts/generate.py "日出时的山景 蓝色大海的海滩 秋天的森林小路 雪后的村庄" --batch

# 批量生成产品变体
python scripts/generate.py "红色款产品 蓝色款产品 黑色款产品 白色款产品" --batch
```

---

## 🎯 参数选择指南

### 图片模型选择

| 模型 | 速度 | 质量 | 适用场景 | 推荐指数 |
|------|------|------|---------|---------|
| **cogview-3-flash** | ⚡⚡⚡ | ⭐⭐⭐ | 快速测试、大量生成、预览 | 🌟🌟🌟 |
| **cogview-4-250304** | ⚡⚡ | ⭐⭐⭐⭐ | 日常使用、平衡质量与速度 | 🌟🌟🌟🌟 |
| **cogview-4** | ⚡ | ⭐⭐⭐⭐⭐ | 专业级、高质量输出 | 🌟🌟🌟🌟🌟 |

**建议：**
- 快速测试 → `cogview-3-flash`
- 日常使用 → `cogview-4-250304`
- 最终输出 → `cogview-4` + `--quality hd`

### 视频模型选择

| 模型 | 速度 | 质量 | 适用场景 | 推荐指数 |
|------|------|------|---------|---------|
| **cogvideox-flash** | ⚡⚡⚡ | ⭐⭐⭐ | 快速预览、测试效果 | 🌟🌟🌟 |
| **cogvideox-2** | ⚡⚡ | ⭐⭐⭐⭐ | 标准视频、日常使用 | 🌟🌟🌟🌟 |
| **cogvideox-3** | ⚡ | ⭐⭐⭐⭐⭐ | 高质量长视频 | 🌟🌟🌟🌟🌟 |

**建议：**
- 快速测试 → `cogvideox-flash`
- 日常使用 → `cogvideox-2`
- 高质量输出 → `cogvideox-3`

### 尺寸选择

| 尺寸 | 比例 | 适用场景 |
|------|------|---------|
| **1024x1024** | 1:1 | 正方形、头像、社交媒体 |
| **1024x1792** | 9:16 | 竖版、封面、海报 |
| **1792x1024** | 16:9 | 横版、横幅、风景 |

---

## 💡 Prompt 编写技巧

### 好的 Prompt 特征

✅ **具体明确** - 描述主体、风格、场景
✅ **细节丰富** - 包含光线、角度、氛围
✅ **风格明确** - 指定艺术风格、质量要求

### 示例对比

❌ 不好：`一只猫`

✅ 好：`一只橘色的短毛猫，坐在窗台上晒太阳，温暖的下午光线，柔和的景深效果，专业摄影`

### 常用风格关键词

**风格类：**
- 水墨画、油画、水彩、素描、卡通、写实
- 赛博朋克、极简主义、复古、现代、传统

**光线类：**
- 自然光、柔和光线、强烈对比、逆光、侧光

**氛围类：**
- 温馨、神秘、浪漫、科技感、清新、厚重

**质量类：**
- 专业摄影、高清、8K、电影级、精细细节

---

## ⚙️ 高级用法

### 直接使用 Python API

```python
import sys
sys.path.insert(0, '.claude/skills/image-video-generation/lib')

from image_video import generate_image, batch_generate_images, generate_video, wait_for_video

# 单张图片
result = generate_image(
    prompt="描述内容",
    model="cogview-3-flash",
    quality="standard",
    size="1024x1024",
)
url = result["data"][0]["url"]

# 批量图片
prompts = ["描述1", "描述2", "描述3"]
results = batch_generate_images(prompts, max_concurrent=3)

# 视频生成
video = generate_video(prompt="描述内容", duration=5)
task_id = video["id"]
final = wait_for_video(task_id)
video_url = final["video_result"][0]["url"]
```

### 自定义并发控制

批量生成时控制并发数以优化性能：

```python
results = batch_generate_images(
    prompts,
    max_concurrent=5  # 增加并发数（建议不超过 5）
)
```

---

## 📚 完整参考文档

详细的 API 文档和更多示例请参考：

- **完整 API 参考**：见 `lib/image_video.py` 中的函数文档
- **示例代码**：见 `examples/` 目录
- **README**：见 `README.md` 获取快速入门

---

## ❓ 故障排除

### 常见问题

**Q: 提示 "需要设置 BIGMODEL_API_KEY 环境变量"**
- A: 未设置 API Key，参考"快速开始"第1步设置

**Q: 生成速度很慢**
- A: 尝试使用 `cogview-3-flash` 或 `cogvideox-flash` 模型

**Q: 视频生成失败**
- A: 简化 prompt 或更换模型，检查网络连接

**Q: 批量生成时中断**
- A: 降低并发数，使用 `--concurrent 2`

**Q: 图片质量不够高**
- A: 使用 `--quality hd` 和 `cogview-4` 模型

### 获取帮助

```bash
# 查看脚本帮助
python scripts/generate.py --help

# 测试 API Key 是否有效
python scripts/generate.py "test"  # 如果有效会生成测试图片
```

---

## 🎯 最佳实践

1. **先快速测试** - 使用 flash 模型快速验证效果
2. **再精细调整** - 满意后用高质量模型生成最终版本
3. **保存好 Prompt** - 记录有效的 prompt 供后续复用
4. **批量处理** - 相似需求的图片使用批量生成
5. **合理选择尺寸** - 根据用途选择合适的尺寸比例
