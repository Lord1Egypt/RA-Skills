# cosercard-skill

Coser 模卡生成器 - 快速制作专业的 Cosplay/模特展示卡片

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue)](https://www.python.org/)
[![Pillow](https://img.shields.io/badge/Pillow-9.0%2B-green)](https://python-pillow.org/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

**版本**: v1.2 | **更新日期**: 2026-03-23

---

## 简介

这是一个专为 Coser、模特、摄影爱好者设计的模卡制作工具。无论是准备约拍、投递给摄影工作室，还是在社交平台展示作品，都能快速生成专业的展示卡片。

支持多种排版风格：wide 宽屏、sidebar 侧边栏、floating 浮动信息、magazine 杂志风、grid 网格等，满足不同场景需求。

---

## 功能特点

- 🎨 **多种排版** - wide、sidebar、floating、magazine、grid3/4/6、compact 等
- 🎭 **多样风格** - anime、japanese、elegant、cyber、retro、minimal、colorful
- 📐 **多尺寸输出** - 支持宽屏、手机竖屏、正方形、A4 打印等
- 🤖 **交互式操作** - 引导式填写，信息字段全部可选
- 🧠 **智能推荐** - 自动学习偏好，记住最佳配置
- 🔍 **批量预览** - 一次生成 6 种组合对比图，快速挑选满意的风格 *(v1.1)*
- ⚡ **快速模式** - 根据历史数据自动选最优配置，一条命令出图 *(v1.1)*
- 📊 **照片分析** - 自动统计横竖方图构成，智能匹配最佳模板 *(v1.2)*
- 🎨 **色调识别** - 分析照片主色调，自动匹配最合适的风格，纯 PIL 无额外依赖 *(v1.2)*

---

## 快速开始

### 安装

```bash
git clone https://github.com/Zaosusu/cosercard-skill.git
cd cosercard-skill
pip install -r requirements.txt
```

### 推荐工作流（最快拿到满意的模卡）

**第一步：批量预览，挑选风格**

传入照片后，先用 `-b` 生成一张包含 6 种组合的对比预览图：

```bash
cd scripts
python coser_card.py --photos "photos/*.jpg" --name "你的CN" -b
```

终端会先输出照片分析结果，再打印对照表：

```
🔍 照片分析结果:
   构成: 4张竖图 / 1张横图 / 1张方图
   推荐模板: magazine  推荐风格: anime

组合对照表:
  #1  --template magazine --style anime
  #2  --template sidebar --style elegant
  #3  --template wide --style cyber
  ...
```

**第二步：选中满意的，出全尺寸**

```bash
python coser_card.py --photos "photos/*.jpg" --name "你的CN" \
    --template magazine --style anime
```

---

### 其他使用方式

**全自动模式**（分析照片自动选模板+风格）：
```bash
python coser_card.py --photos "photos/*.jpg" --name "你的CN" \
    --template auto --style auto
```

**快速模式**（用历史最常用配置）：
```bash
python coser_card.py --photos "photos/*.jpg" --name "你的CN" -q
```

**交互式**（引导填写所有信息）：
```bash
python coser_card.py -i
```

**完整命令行**：
```bash
python coser_card.py \
    --photos "photos/*.jpg" \
    --name "你的CN" \
    --height 165 --weight 48 \
    --douyin "10w粉丝" \
    --location "东京" \
    --template magazine \
    --style auto \
    --formats wide
```

---

## 模板说明

| 模板 | 适合几张图 | 特点 |
|------|-----------|------|
| `auto` | 任意 | **⭐推荐**，根据照片横竖构成自动决定 |
| `magazine` | 3-7 张 | 黄金比例（主图占 61.8%），横竖混排效果最佳 *(v1.2)* |
| `wide` | 6-8 张 | 21:9 宽屏，左侧竖排信息栏，横图首选 |
| `sidebar` | 4-8 张 | 左侧信息栏 + 右侧图片网格 |
| `compact` | 3-5 张 | 左大图 + 右侧小图网格，竖图首选 |
| `floating` | 4-6 张 | 图片满铺，底部半透明信息栏 |
| `hero` | 1-3 张 | 主图大图 + 下方缩略图条 |
| `grid4` | 4 张 | 2x2 网格，方图首选 |
| `grid6` | 6 张 | 3x2 网格 |

## 风格说明

| 风格 | 配色 | 适合场景 | 自动识别条件 |
|------|------|---------|------------|
| `auto` | 自动识别 | 任意 | **⭐推荐**，分析照片色调决定 |
| `anime` | 深灰底 + 樱花粉 | 二次元、Cosplay | 暗色调或暖中色 |
| `cyber` | 深黑蓝 + 霓虹 | 科幻、暗黑风 | 暗色 + 冷色调 |
| `japanese` | 米白 + 樱花粉 | 日系清新 | 暖色低饱和 |
| `elegant` | 纯白 + 香槟金 | 模特、写真 | 灰调偏暗 |
| `minimal` | 纯白 + 浅灰 | 极简通用 | 亮灰低饱和 |
| `retro` | 暖黄 + 砖红 | 复古胶片 | 暖色高饱和 |
| `colorful` | 暖白 + 橙色 | 萌系、可爱 | 冷暖混合 |

## 输出格式

| 格式 | 尺寸 | 用途 |
|------|------|------|
| `wide` | 2560×1080 | 宽屏展示、电脑壁纸 |
| `mobile` | 1080×1920 | 手机竖屏、小红书/微博 |
| `square` | 1080×1080 | 正方形，微博/朋友圈 |
| `a4` | 2480×3508 | 打印用，300dpi |

---

## 可以做什么？

- 📸 **Cosplay 模卡** - 展示角色扮演作品，用于约拍或活动
- 👗 **模特 Casting Card** - 投递给摄影工作室的专业简历
- 📱 **社交平台展示** - 微博、小红书、抖音的展示图片
- 🖨️ **打印作品集** - A4 尺寸适合打印成纸质模卡

---

## 项目结构

```
cosercard-skill/
├── SKILL.md              # Skill 文档
├── README.md             # 说明文档
├── requirements.txt      # 依赖
├── LICENSE               # 许可证
├── learning_data.json    # 自动生成，记录使用偏好
├── examples/             # 示例
└── scripts/
    └── coser_card.py     # 主程序
```

---

## 技术栈

- Python 3.8+
- Pillow (PIL) — 包括色调分析，无需 sklearn / dlib 等重型依赖

---

## Changelog

**v1.2** (2026-03-23)
- 新增 `magazine` 杂志风黄金比例布局模板（主图占 61.8%，横竖混排最佳）
- 新增 `--template auto` 根据照片横竖构成自动选模板
- 新增 `--style auto` 根据照片主色调自动匹配风格（纯 PIL 实现）
- 新增 `analyze_photos()` 照片比例分析模块
- 新增 `auto_style_from_photos()` 色调分析模块
- `-b` 批量预览增加照片分析摘要输出，magazine 进入候选优先位

**v1.1** (2026-03-23)
- 新增 `-b / --batch-preview` 批量预览模式，一次对比 6 种组合
- 新增 `-q / --quick` 快速模式，自动读取历史偏好选配置
- 修复 `verify_card` 函数逻辑错误（原代码两个函数内容写混了）
- 新增按照片数量智能推荐模板逻辑

**v1.0** (2026-03-23)
- 初始版本发布

---

## License

MIT License

---

**GitHub**: https://github.com/Zaosusu/cosercard-skill
