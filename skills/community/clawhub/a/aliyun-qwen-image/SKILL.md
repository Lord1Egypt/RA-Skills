---
name: qwen-image
description: >
  调用阿里云百炼（DashScope/Model Studio）平台上的千问及万相2.6模型，完成图像生成与编辑任务。
  当用户涉及以下任何场景时，必须使用此 skill：
  - 调用千问或万相2.6模型生成、编辑图片
  - 百炼平台图像相关 API
  - 使用 dashscope SDK 访问 qwen-image / wan2.6 模型
  - 文生图、图像编辑、图文混排输出
  - 用户提及 qwen-image、wan2.6-image、wan2.6-t2i 等关键词
version: 1.0.0
metadata:
  openclaw:
    requires:
      env:
        - DASHSCOPE_API_KEY
      anyBins:
        - uv
        - pip
    primaryEnv: DASHSCOPE_API_KEY
    install:
      - kind: uv
        package: uv
        bins: [uv]
    emoji: "🎨"
    homepage: https://help.aliyun.com/zh/model-studio/text-to-image
---

# Qwen Image Skill

通过运行捆绑的脚本实现所有图像功能。**先检查环境，再运行命令。**

## 第一步：确认地域（必须先问）

**各地域的 API Key 与请求地址完全独立，不可混用，否则鉴权失败。**

如果用户未说明地域，**必须先询问**：

> 您使用的是哪个地域的百炼服务？
>> - **中国大陆**（北京）→ `--region cn`（**默认，可省略**）
> - **弗吉尼亚**（美国，仅 wan26 支持）→ `--region us`

确认后，在所有命令中统一加上对应的 `--region` 参数。

## 第二步：环境检查

```bash
# 检查 uv 是否可用
command -v uv

# 检查 API Key
echo $DASHSCOPE_API_KEY
```

**关于 Python 依赖（dashscope、requests）：**

脚本顶部包含 [PEP 723](https://peps.python.org/pep-0723/) 内联依赖声明：

```python
# /// script
# requires-python = ">=3.9"
# dependencies = [
#   "dashscope>=1.25.8",
#   "requests>=2.31.0",
# ]
# ///
```

使用 `uv run` 时，`uv` 会**自动创建隔离虚拟环境并安装上述依赖**，无需手动操作。

**如果 `uv` 不存在**，先安装 uv：

```bash
pip install uv --break-system-packages
```

**如果无法使用 `uv`**，可改用 pip 手动安装依赖后直接运行脚本：

```bash
pip install "dashscope>=1.25.8" "requests>=2.31.0"
python $SKILL_SCRIPT text2img --prompt "..."
```

如果 API Key 为空：提示用户设置对应地域的 API Key：
- 中国大陆：`export DASHSCOPE_API_KEY="sk-xxx"`（百炼北京控制台获取）
- 海外：`export DASHSCOPE_API_KEY="sk-xxx"`（Model Studio 新加坡控制台获取）

## 第三步：脚本路径

```
SKILL_SCRIPT="<skill安装路径>/scripts/run.py"
```

安装位置因环境而异，请根据实际情况替换，例如：
- `~/.claude/skills/qwen-image/scripts/run.py`
- `~/.codex/skills/qwen-image/scripts/run.py`
- `/path/to/skills/qwen-image/scripts/run.py`

---

## 地域与功能限制

| 子命令 | 模型 | 中国大陆（cn） | 海外/新加坡（intl） | 弗吉尼亚（us） |
|--------|------|:---:|:---:|:---:|
| `text2img` | qwen-image-2.0-pro（默认）/ qwen-image-2.0 / qwen-image-max / qwen-image-plus / qwen-image | ✅ | ✅ | ❌ |
| `edit` | qwen-image-2.0-pro（默认）/ qwen-image-2.0 / qwen-image-edit-max / qwen-image-edit-plus / qwen-image-edit | ✅ | ✅ | ❌ |
| `wan26` | wan2.6-image（默认）/ wan2.6-t2i | ✅ | ✅ | ✅ |

---

## 模型选择指南

### text2img 可用模型

| 模型 | 特点 | 多图输出 |
|------|------|---------|
| `qwen-image-2.0-pro`（**默认**）| 旗舰，文字渲染/真实质感/语义遵循最强 | 1-6 张 |
| `qwen-image-2.0` | 加速版，兼顾效果与速度 | 1-6 张 |
| `qwen-image-max` | Max 系列，真实感更强，AI 痕迹更低 | 固定 1 张 |
| `qwen-image-plus` | Plus 系列，多样化艺术风格与文字渲染 | 固定 1 张 |
| `qwen-image` | 基础版（与 qwen-image-plus 能力相同） | 固定 1 张 |

### edit 可用模型

| 模型 | 特点 | 多图输出 |
|------|------|---------|
| `qwen-image-2.0-pro`（**默认**）| 旗舰，文字渲染/真实质感/语义遵循最强 | 1-6 张 |
| `qwen-image-2.0` | 加速版，兼顾效果与速度 | 1-6 张 |
| `qwen-image-edit-max` | Max 系列，工业设计/几何推理/角色一致性强 | 1-6 张 |
| `qwen-image-edit-plus` | Plus 系列，多图输出与自定义分辨率 | 1-6 张 |
| `qwen-image-edit` | 基础版，单图编辑和多图融合 | 固定 1 张 |

### wan26 可用模型

| 模型 | 用途 | 输入图 |
|------|------|------|
| `wan2.6-image`（**默认**）| 图像编辑（1-4张参考图）或图文混排/文生图 | 编辑：1-4 张；混排：0-1 张 |
| `wan2.6-t2i` | 纯文生图（图文混排输出） | 不支持 |

- **有 `--images`**（1-4张）→ 图像编辑模式（`wan2.6-image` 专用）
- **无 `--images`** 或 `--interleave`（最多1张图）→ 图文混排/文生图模式（流式输出文字+图片）
- **`--interleave` + 超过1张图** → 报错（混排模式最多1张输入图）

---

## 命令速查

> 默认地域为中国大陆（`--region cn`），可省略。海外用户需显式添加 `--region intl` 或 `--region us`。

### 千问文生图

```bash
uv run $SKILL_SCRIPT text2img \
  --prompt "冬日雪景中的古典中式庭院，飞檐斗拱" \
  --model qwen-image-2.0-pro \
  --size 2048*2048 \
  --n 1 \
  --region cn \
  --output-dir .
```

### 千问图像编辑（1-3 张输入图）

```bash
uv run $SKILL_SCRIPT edit \
  --prompt "将图中女孩的服装改为红色旗袍" \
  --images "https://example.com/photo.jpg" \
  --model qwen-image-2.0-pro \
  --size 1024*1024 \
  --n 1 \
  --region cn \
  --output-dir .
```

多图融合示例（最多3张）：

```bash
uv run $SKILL_SCRIPT edit \
  --prompt "使用图1的城市作为底图，将图2的卡通形象放置在建筑物周围" \
  --images "https://example.com/city.jpg" "https://example.com/character.png" \
  --model qwen-image-2.0-pro \
  --region cn \
  --output-dir .
```

### 万相2.6图像编辑（wan2.6-image，1-4张输入图）

```bash
uv run $SKILL_SCRIPT wan26 \
  --prompt "参考图1的风格和图2的背景，生成番茄炒蛋" \
  --images "https://example.com/style.png" "https://example.com/bg.jpg" \
  --model wan2.6-image \
  --n 1 \
  --size 1K \
  --region cn \
  --output-dir .
```

### 万相2.6文生图/图文混排（wan2.6-image 无图 或 wan2.6-t2i）

```bash
uv run $SKILL_SCRIPT wan26 \
  --prompt "给我一个3张图的辣椒炒肉教程" \
  --model wan2.6-t2i \
  --max-images 3 \
  --size 1280*1280 \
  --region cn \
  --output-dir .
```

---

## 常用参数参考

| 参数 | 说明 |
|------|------|
| `--region cn` | 中国大陆（北京，**默认值**） |
| `--region intl` | 海外/新加坡 |
| `--region us` | 弗吉尼亚（仅 wan26） |
| `--n` | 生成数量（text2img/edit: 2.0系列1-6张，其余固定1；wan26编辑模式1-4） |
| `--max-images` | wan26 图文混排模式最多生成图片数（1-5） |
| `--output-dir` | 保存目录（默认当前目录） |
| `--api-key` | API Key（可用环境变量代替） |
| `--no-extend` | 禁用提示词自动扩写 |
| `--seed` | 随机数种子（text2img / edit / wan26） |
| `--watermark` | 添加水印（text2img: Qwen-Image；wan26: AI生成） |

## 常用 size 值

### text2img / edit / wan26 图像编辑（总像素 512×512～2048×2048）

| size | 比例 |
|------|------|
| `2048*2048`（text2img 默认）| 1:1 |
| `2688*1536` | 16:9 横版 |
| `1536*2688` | 9:16 竖版 |

### wan26 图像编辑 size 档位

| size | 说明 |
|------|------|
| `1K`（**默认**）| 总像素约 1280×1280，比例跟随最后一张输入图 |
| `2K` | 总像素约 2048×2048，比例跟随最后一张输入图 |

### wan2.6-t2i 文生图（总像素 1280×1280～1440×1440）

| size | 比例 |
|------|------|
| `1280*1280`（**默认**）| 1:1 |
| `720*1280` | 9:16 竖版 |
| `1280*720` | 16:9 横版 |
| `1440*1440` | 1:1 高清 |

### wan2.6-image 图文混排/文生图（无图输入，总像素 768×768～1280×1280）

| size | 比例 |
|------|------|
| `1280*1280` | 1:1 |
| `720*1280` | 9:16 竖版 |
| `1280*720` | 16:9 横版 |

## 提示词指南

### 基础公式

**提示词 = 主体 + 场景 + 风格**

> 示例：`25岁中国女孩，圆脸，优雅的民族服装，室外，电影级光照，半身特写，商业摄影`

### 进阶公式

**提示词 = 主体描述 + 场景描述 + 风格 + 镜头语言 + 氛围词 + 细节修饰**

> 示例：`由羊毛毡制成的大熊猫，穿着蓝色警服马甲，大步奔跑，动物王国城市街道，夜晚明亮，摄影镜头，居中构图，毛毡风格，皮克斯风格，逆光，4K`

### 常用词典速查

| 维度 | 常用词 |
|------|--------|
| **景别** | 特写、近景、中景、远景 |
| **视角** | 平视、俯视、仰视、航拍 |
| **镜头** | 微距、超广角、长焦、鱼眼 |
| **风格** | 写实、水彩、水墨、工笔、3D卡通、粘土、折纸、超现实、废土风 |
| **光线** | 自然光、逆光、霓虹灯、氛围光、电影级光照、丁达尔效应 |

### 反向提示词推荐

```
低分辨率，低画质，肢体畸形，手指畸形，画面过饱和，蜡像感，人脸无细节，过度光滑，画面具有AI感，构图混乱，文字模糊，扭曲
```

---

## 注意事项

- 生成图片 URL **有效期 24 小时**，脚本已自动下载保存到本地
- `wan2.6-t2i` 不支持 `--images` 输入，仅用于文生图
- wan26 图文混排模式会同时保存文字内容（`*-wan26-text.txt`）和图片

## 故障排查

| 错误 | 解决方案 |
|------|---------|
| `No API key provided` | `export DASHSCOPE_API_KEY="sk-xxx"` |
| `Model not exist` | 检查模型名拼写，确认地域支持该模型 |
| `quota/permission/403` | API Key 无对应模型权限，或免费额度耗尽 |
| `Task timeout` | 重试或增加等待时间 |
