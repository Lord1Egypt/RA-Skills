---
name: cosercard-skill
description: >
  Coser 模卡生成工具，快速制作专业的 Cosplay/模特展示卡片。
  支持多图自动排版、多种风格模板、信息展示、一键导出。
  Use when: (1) 需要制作 Coser/模特模卡 (2) 多张照片需要统一排版
  (3) 需要打印版/手机版/正方形版不同尺寸 (4) 快速生成展示卡片
  Keywords: coser, 模卡, 模特卡, casting card, 排版, 多图, 写真, 摄影
---

# cosercard-skill

Coser 模卡生成器 - 快速制作专业的 Cosplay/模特展示卡片

---

## 🚀 推荐工作流（最快拿到满意的模卡）

### 第一步：批量预览，挑选风格 `-b`

传入照片后，先跑批量预览，一次对比 6 种模板+风格组合：

```bash
cd skills/coser-card/scripts
python coser_card.py --photos "photos/*.jpg" --name "你的CN" -b
```

终端输出示例：

```
🔍 照片分析结果:
   构成: 4张竖图 / 1张横图 / 1张方图
   推荐模板: magazine  推荐风格: anime

🎬 正在批量生成 6 种预览组合...
  ✓ #1 magazine + anime
  ✓ #2 sidebar + elegant
  ✓ #3 wide + cyber
  ...

组合对照表:
  #1  --template magazine --style anime
  #2  --template sidebar --style elegant
  #3  --template wide --style cyber
  ...
```

预览图每格左上角标 `#编号`，底部标明模板+风格，保存在 `./output/`。

### 第二步：选中满意的，出全尺寸

比如看中了 #2：

```bash
python coser_card.py --photos "photos/*.jpg" --name "你的CN" \
    --template sidebar --style elegant
```

---

## 🤖 全自动模式

### 完全自动（最省事）

让程序自动分析照片比例和色调，选最合适的模板和风格：

```bash
python coser_card.py --photos "photos/*.jpg" --name "你的CN" \
    --template auto --style auto
```

终端输出示例：

```
🎨 自动识别风格: anime (二次元风)
📐 自动选择模板: magazine  (照片构成: 4竖/1横/1方)
```

### 快速模式 `-q`（读历史数据）

根据你过去用得最多的配置自动选，不用手动指定：

```bash
python coser_card.py --photos "photos/*.jpg" --name "你的CN" -q
```

---

## 📋 其他使用方式

### 交互式输入（引导填写）

```bash
python coser_card.py -i
```

### 完整命令行

```bash
python coser_card.py \
    --photos "photos/*.jpg" \
    --name "黑皮" \
    --height 160 --weight 45 --bust 34 --waist 54 --hip 63 --shoe 34 \
    --douyin "10w粉丝" \
    --location "东京" \
    --template wide \
    --style anime \
    --formats wide
```

---

## 🎨 可填写的信息

### 基本信息（必填）
| 字段 | 说明 | 示例 |
|------|------|------|
| CN名称 | 你的 Coser 名字 | 黑皮、赤西夜夜 |
| 照片路径 | 照片文件路径 | `D:\photos\*.jpg` |

### 身体数据（可选）
| 字段 | 说明 | 示例 |
|------|------|------|
| 身高 | 单位 cm | 165 |
| 体重 | 单位 kg | 48 |
| 胸围 | 单位 cm | 86 |
| 腰围 | 单位 cm | 62 |
| 臀围 | 单位 cm | 88 |
| 鞋码 | 鞋码数 | 37 |

### 社交账号（可选）
| 字段 | 说明 | 示例 |
|------|------|------|
| 抖音 | 粉丝数或ID | 10w粉丝 |
| 微博 | 微博ID | akane_weibo |
| B站 | B站ID | akane_bili |
| 小红书 | 小红书ID | akane_xhs |

### 联系方式（可选）
| 字段 | 说明 | 示例 |
|------|------|------|
| 微信/QQ/邮箱 | 联系方式 | wechat: xxxxxx |
| 所在城市 | 城市名 | 东京、上海 |

---

## 📐 模板类型

| 模板 | 说明 | 推荐张数 | 特点 |
|------|------|---------|------|
| `auto` | 自动选择 | 任意 | **⭐推荐**，根据照片比例构成自动决定 |
| `magazine` | 杂志黄金比例 | 3-7张 | 主图占 61.8%，右侧均分，混排最佳 **v1.2新增** |
| `wide` | 宽屏横向 | 6-8张 | 2560×1080，左侧信息栏+右侧网格 |
| `sidebar` | 侧边栏 | 6-8张 | 深色侧边栏，信息展示清晰 |
| `floating` | 浮动信息 | 4-6张 | 底部半透明悬浮栏 |
| `compact` | 紧凑布局 | 4-6张 | 左大图右网格，极小间隙，竖图首选 |
| `hero` | 主图+缩略图 | 4-6张 | 一张大图+下方缩略图条 |
| `grid4` | 四宫格 | 4张 | 经典四宫格，方图首选 |
| `grid6` | 六图网格 | 6张 | 3×2 网格 |
| `grid3` | 一大两小 | 3张 | 上方大图+下方两小图 |
| `film` | 电影胶片 | 3-6张 | 胶片孔装饰，复古感 |
| `vertical` | 竖排拼接 | 3-5张 | 照片纵向排列 |
| `sidebar_right` | 右侧边栏 | 6-8张 | 与 sidebar 镜像 |

### 自动模板选择逻辑（`--template auto`）

| 照片构成 | 张数 | 自动选择模板 |
|---------|------|------------|
| 竖图为主 | 1张 | hero |
| 竖图为主 | 2张 | sidebar |
| 竖图为主 | 3-4张 | compact |
| 竖图为主 | 5-6张 | sidebar |
| 竖图为主 | 7张+ | wide |
| 横图为主 | 4张+ | wide |
| 横图为主 | 2-3张 | floating |
| 方图为主 | 4张以内 | grid4 |
| 方图为主 | 5张+ | grid6 |
| 横竖混排 | 3张+ | **magazine** |

---

## 🎭 风格模板

| 风格 | 特点 | 适用场景 | 自动选条件 |
|------|------|----------|----------|
| `auto` | 自动识别 | 任意 | **⭐推荐**，分析照片色调决定 |
| `anime` | 深灰底+白字+樱花粉 | Coser模卡 | 暗色调或暖中色 |
| `cyber` | 深黑蓝+霓虹 | 科幻、机甲 | 暗色+冷色调 |
| `japanese` | 米白+樱花粉 | 日系、JK | 暖色低饱和 |
| `elegant` | 纯白+香槟金 | 正片、礼服 | 灰调偏暗 |
| `minimal` | 纯白+浅灰 | Casting | 亮灰低饱和 |
| `retro` | 暖黄+棕色 | 港风、昭和 | 暖色高饱和 |
| `colorful` | 暖白+橙色 | 萌系、可爱 | 冷暖混合 |

### 自动风格识别逻辑（`--style auto`）

程序用 PIL 对照片做主色调量化（无需额外依赖），分析色温（冷/暖/中）+ 亮度 + 饱和度，按以下规则决定：

```
整体暗 + 冷色  →  cyber
整体暗 + 其他  →  anime
低饱和 + 亮    →  minimal
低饱和 + 暗    →  elegant
暖色 + 高饱和  →  retro
暖色 + 低饱和  →  japanese
冷色为主       →  cyber
其他混合       →  colorful
```

---

## 📏 输出格式

| 格式 | 尺寸 | 用途 |
|------|------|------|
| `wide` | 2560×1080 | 宽屏展示、电脑展示 |
| `mobile` | 1080×1920 | 手机、Stories、小红书竖版 |
| `square` | 1080×1080 | 小红书、Instagram |
| `a4` | 2480×3508 | 打印、投递、作品集 |
| `banner` | 1500×500 | 微博头图 |
| `landscape` | 1920×1080 | 16:9 横向 |

---

## 💡 智能功能说明

### 照片比例分析（v1.2 新增）

`analyze_photos()` 自动统计照片构成：

```
portrait  = 宽高比 < 0.82  （竖图）
landscape = 宽高比 > 1.25  （横图）
square    = 其余            （方图）
```

结果影响 `--template auto` 的选择。

### 主色调自动风格匹配（v1.2 新增）

`auto_style_from_photos()` 纯 PIL 实现，无需安装 sklearn。分析步骤：

1. 将照片缩至 80×80
2. PIL 调色板量化提取 4 种主色
3. 计算色温（冷/暖/中）和感知亮度、饱和度
4. 按决策树选择最匹配的风格

### 批量预览（v1.1 新增）

`-b` 模式一次生成 6 种组合的缩略图拼在一张对比图里，每格标注编号和配置名，底部打印对照命令，看图即可决策。

### 智能图片裁剪

`smart_crop()` 优先保留图片上半部分（人脸区域在上方），避免人脸被裁掉。

### 自适应字体

文字太长时自动缩小字体，不截断不遮挡。

### 学习系统

每次生成自动记录配置到 `learning_data.json`，`-q` 快速模式读取历史频率最高的组合作为默认。

---

## 📝 完整命令行参数

```
--photos          照片路径（支持通配符 *.jpg）
--name            CN名称（必填）
--cn              英文名/罗马音
--height          身高 cm
--weight          体重 kg
--bust            胸围 cm
--waist           腰围 cm
--hip             臀围 cm
--shoe            鞋码
--douyin          抖音账号/粉丝数
--weibo           微博账号
--bilibili        B站账号
--xiaohongshu     小红书账号
--contact         联系方式
--location        所在城市
--template        排版模板（默认: grid4，支持 auto）
--style           风格模板（默认: minimal，支持 auto）
--formats         输出格式（默认: mobile）
--output          输出目录（默认: ./output）
--interactive, -i 交互式输入
--batch-preview, -b  批量生成6种组合预览图（推荐首次使用）
--quick, -q       快速模式：自动用历史最优配置
--watermark       添加水印
--demo            生成演示图片
```

---

## 📚 使用示例

### 示例 1：最快工作流

```bash
# 先看预览
python coser_card.py --photos "photos/*.jpg" --name "黑皮" -b

# 选中满意的出图
python coser_card.py --photos "photos/*.jpg" --name "黑皮" \
    --template magazine --style anime --formats wide
```

### 示例 2：完全自动

```bash
python coser_card.py --photos "photos/*.jpg" --name "黑皮" \
    --template auto --style auto --formats wide
```

### 示例 3：完整信息 + 多格式

```bash
python coser_card.py \
    --photos "D:\cosplay\*.jpg" \
    --name "赤西夜夜" --cn "Akane" \
    --height 168 --weight 50 --bust 86 --waist 62 --hip 88 --shoe 37 \
    --douyin "100w粉丝" --location "东京" \
    --template magazine --style auto \
    --formats wide,mobile
```

### 示例 4：打印版

```bash
python coser_card.py \
    --photos "highres*.jpg" \
    --name "CN名称" --height 170 --weight 53 \
    --template grid4 --style minimal --formats a4
```

---

## 📁 文件说明

```
coser-card/
├── SKILL.md                    # 本文档
├── README.md                   # 项目说明
├── requirements.txt            # 依赖：Pillow
├── learning_data.json          # 学习数据库（自动生成）
├── examples/
│   └── output/                 # 示例输出
└── scripts/
    └── coser_card.py           # 主程序
```

## ⚙️ 安装依赖

```bash
pip install Pillow
```

无需安装 sklearn、dlib、face_recognition 等重型依赖。

---

## 🤖 系统提示（AI Agent 使用）

当用户使用此 Skill 时，推荐按以下流程引导：

### 引导用户提供信息

```
你好！我来帮你制作 Coser 模卡。

请提供以下信息（不想填的可以直接回车跳过）：

【基本信息】
- CN名称: （如：赤西夜夜）
- 英文名/罗马音: （可选）

【身体数据】（可选）
- 身高/体重/三围/鞋码

【社交账号】（可选）
- 抖音/微博/B站/小红书

【联系方式】（可选）
- 微信/QQ/邮箱、所在城市

【照片】
- 照片路径: （支持通配符，如：D:\photos\*.jpg）
```

### 首次使用，推荐批量预览

```
建议先跑批量预览看效果：

python coser_card.py --photos "路径" --name "CN" -b

会生成一张包含 6 种组合的对比图，你选一个满意的再出全尺寸。
```

### 若用户图省事，推荐全自动

```
python coser_card.py --photos "路径" --name "CN" --template auto --style auto
```

程序会自动分析照片比例和色调，选最合适的组合。

### 保存用户偏好

当用户告知最佳配置后，调用：
```python
from coser_card import mark_as_best
mark_as_best(profile, template, style, format_type)
```

下次使用 `-q` 快速模式时会自动使用该配置。

---

## Changelog

**v1.2** (2026-03-23)
- 新增 `magazine` 杂志风黄金比例布局模板
- 新增 `--template auto` 根据照片比例构成自动选模板
- 新增 `--style auto` 根据照片主色调自动匹配风格（纯PIL，无额外依赖）
- 新增 `analyze_photos()` 照片比例分析模块
- 新增 `auto_style_from_photos()` 色调分析模块
- `-b` 批量预览增加照片分析摘要输出，magazine 进入候选优先位
- 修复 `smart_select_template()` 现在接受照片分析结果，更准确

**v1.1** (2026-03-23)
- 新增 `-b / --batch-preview` 批量预览模式
- 新增 `-q / --quick` 快速模式
- 修复 `verify_card` 函数逻辑错误

**v1.0** (2026-03-23)
- 初始版本

---

**版本**: v1.2  
**更新日期**: 2026-03-23  
**功能**: 12种模板（含auto）、8种风格（含auto）、6种格式、批量预览、色调自动匹配、纯PIL无重型依赖
