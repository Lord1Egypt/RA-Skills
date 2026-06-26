---
name: beauty-image
description: 商业化AI图片生成助手。40+场景模板, 30+风格词典, 智能意图识别, 结构化Prompt, 三引擎智能路由 (Wanx/Seedream4/Seedream5)。
version: 3.2.0
author: 圆规
metadata:
  openclaw:
    requires:
      env:
        - DASHSCOPE_API_KEY
        - ARK_API_KEY
        - DEEPSEEK_API_KEY
      bins:
        - uv
    primaryEnv: DASHSCOPE_API_KEY
    emoji: "🎨"
    homepage: https://github.com/xyva-yuangui/beauty-image
    os: ["darwin", "linux", "win32"]
---

# Beauty Image V3 — 商业化AI图片生成

AI 图片生成助手。**触发后必须先询问用户确认**，再执行生成。

V3升级: 意图识别(40+场景) + 结构化Prompt + 风格词典(30+) + 智能引擎路由

| 触发场景 | 询问确认内容 |
|----------|-------------|
| 名片设计 | 姓名、职称、公司、风格(赛博朋克/极简/金属) |
| 海报创作 | 主题、配色、排版风格、文字元素 |
| 头像/IP | 人物描述、风格、表情、背景 |
| 产品摄影 | 产品描述、背景、布光偏好 |
| 3D/材质 | 主体、材质(水晶/毛绒/充气/乐高)、场景 |
| 通用图片 | 画面描述、尺寸比例、风格、引擎选择 |

**执行流程**: 触发 → 意图识别 → 模板匹配 → 询问缺失信息 → Prompt构建 → 引擎路由 → 生成 → 展示

## Usage (V3 脚本, 推荐)

### 智能模式 (自动识别意图+模板+路由)
```bash
uv run {baseDir}/scripts/generate_image_v3.py --prompt "帮我做一张赛博朋克风格的个人名片"
uv run {baseDir}/scripts/generate_image_v3.py --prompt "画一只猫的水晶质感手办"
uv run {baseDir}/scripts/generate_image_v3.py --prompt "上海天气卡片"
uv run {baseDir}/scripts/generate_image_v3.py --prompt "做个毛绒版的苹果logo"
```

### 指定场景模板
```bash
uv run {baseDir}/scripts/generate_image_v3.py --prompt "猫" --scene 3d_crystal
uv run {baseDir}/scripts/generate_image_v3.py --prompt "武士" --scene art_ukiyoe_card --style 浮世绘
uv run {baseDir}/scripts/generate_image_v3.py --prompt "咖啡店" --scene 3d_miniature
```

### 指定字段 (JSON)
```bash
uv run {baseDir}/scripts/generate_image_v3.py --prompt "名片" --scene biz_card --fields '{"name":"圆规","title":"CEO","company":"XyvaClaw"}'
```

### Raw模式 (兼容V2, 直接传prompt)
```bash
uv run {baseDir}/scripts/generate_image_v3.py --prompt "一幅美丽的风景画" --raw
```

### 指定尺寸/比例
```bash
uv run {baseDir}/scripts/generate_image_v3.py --prompt "城市全景" --size 全景
uv run {baseDir}/scripts/generate_image_v3.py --prompt "手机壁纸" --size 9:16
uv run {baseDir}/scripts/generate_image_v3.py --prompt "小红书配图" --size 小红书
uv run {baseDir}/scripts/generate_image_v3.py --prompt "电影海报" --size 海报
```

### 列出模板/风格/引擎/尺寸
```bash
uv run {baseDir}/scripts/generate_image_v3.py --list-scenes
uv run {baseDir}/scripts/generate_image_v3.py --list-styles
uv run {baseDir}/scripts/generate_image_v3.py --list-providers
uv run {baseDir}/scripts/generate_image_v3.py --list-sizes
```

## 尺寸和比例 (15种 + 中文别名)

支持 15 种宽高比，可用比例名、中文别名或直接像素值指定。

| 比例 | wanx 尺寸 | 中文别名 |
|------|----------|---------|
| 1:1 | 1280×1280 | 正方, 头像 |
| 3:4 | 1104×1472 | 小红书, A4 |
| 4:3 | 1472×1104 | — |
| 9:16 | 960×1696 | 竖版, 手机壁纸 |
| 16:9 | 1696×960 | 横版, PPT, 名片 |
| 2:3 | 1048×1568 | 海报 |
| 3:2 | 1568×1048 | — |
| 1:2 | 904×1816 | — |
| 2:1 | 1808×912 | — |
| 9:21 | 840×1960 | 竖屏, 长图 |
| 21:9 | 1952×840 | 宽屏, 电影 |
| 1:3 | 744×2224 | 长海报 |
| 3:1 | 2216×744 | 横幅, banner |
| 1:4 | 640×2560 | 超长, 滚动长图 |
| 4:1 | 2560×640 | 全景, 超宽 |

Seedream 引擎支持 2K/3K 高分辨率输出。

## 场景模板 (26+)

| 分类 | 模板ID | 名称 | 推荐引擎 |
|------|--------|------|----------|
| 商务 | `biz_card` | 名片设计 | seedream5 |
| 商务 | `biz_poster` | 商业海报 | seedream5 |
| 商务 | `biz_product` | 产品摄影 | seedream4 |
| 社交 | `social_avatar` | 头像/IP | seedream4 |
| 社交 | `social_emoji` | 表情包 | wanx |
| 社交 | `social_card` | 金句卡片 | wanx |
| 创意 | `art_general` | 艺术创作 | seedream5 |
| 创意 | `art_ukiyoe_card` | 浮世绘闪卡 | seedream5 |
| 3D | `3d_crystal` | 水晶质感 | seedream5 |
| 3D | `3d_plush` | 毛绒玩具 | seedream4 |
| 3D | `3d_inflatable` | 充气玩具 | seedream4 |
| 3D | `3d_miniature` | 微缩房间 | seedream5 |
| 实用 | `util_weather` | 天气卡片 | seedream5 |
| 实用 | `util_fridge_magnet` | 冰箱贴 | seedream5 |
| 实用 | `util_food_map` | 美食地图 | seedream5 |
| 实用 | `util_storyboard` | 电影分镜 | seedream5 |
| 设计 | `design_ppt` | PPT页面 | seedream5 |
| 设计 | `design_logo` | Logo | wanx |
| 设计 | `design_packaging` | 包装设计 | seedream5 |
| 人物 | `person_portrait` | 写实肖像 | seedream5 |
| 人物 | `person_action_figure` | 手办 | seedream5 |
| 场景 | `scene_chalkboard` | 黑板粉笔画 | seedream4 |
| 电商 | `ecom_main` | 电商主图 | wanx |
| 电商 | `ecom_banner` | 电商横幅 | wanx |
| 内容 | `content_xhs` | 小红书配图 | seedream4 |
| 内容 | `content_blog` | 文章头图 | wanx |

## 风格词典 (20+)

赛博朋克, 浮世绘, 水墨画, 吉卜力, 像素风, 油画, 漫画, 波普艺术, 清明上河图,
水晶, 毛绒, 充气, 乐高, 黏土, 电影感, 产品摄影, 街拍, 胶片, 等距微缩, 3D渲染

## 引擎选择指南

| 引擎 | 适用场景 | 画质 | 速度 | 费用 |
|------|---------|------|------|------|
| **seedream5** | 最高画质，组图 | ⭐⭐⭐⭐⭐ | 中 | 中 |
| **seedream4** | 高画质，性价比 | ⭐⭐⭐⭐ | 较快 | 低 |
| **wanx** | 文字渲染好 | ⭐⭐⭐ | 快 | 低 |

V3自动按场景+风格路由引擎, 无需手动选择。

## API Key 配置 (首次使用必读)

本技能需要至少配置 **一个** API Key 才能使用。推荐配置通义万相 (免费额度较多)。

### 方式一: 环境变量 (推荐)

```bash
# 通义万相 (wanx引擎, 必选其一)
export DASHSCOPE_API_KEY=sk-xxxxxxxxxxxxxxxx

# 火山引擎 (seedream4/seedream5引擎, 可选, 画质更高)
export ARK_API_KEY=xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx

# DeepSeek (可选, 仅用于 --use-llm 深度意图解析)
export DEEPSEEK_API_KEY=sk-xxxxxxxxxxxxxxxx
```

### 方式二: openclaw.json 配置

在 `~/.openclaw/openclaw.json` 中添加:
```json
{
  "models": {
    "providers": {
      "wanxiang": { "apiKey": "sk-your-dashscope-key" },
      "ark": { "apiKey": "your-ark-api-key" },
      "deepseek": { "apiKey": "sk-your-deepseek-key" }
    }
  }
}
```

### API Key 获取地址

| 引擎 | Key名称 | 获取地址 | 说明 |
|------|---------|---------|------|
| **通义万相** | `DASHSCOPE_API_KEY` | https://dashscope.console.aliyun.com/apiKey | 阿里云百炼平台, 注册后有免费额度 |
| **Seedream** | `ARK_API_KEY` | https://console.volcengine.com/ark/region:ark+cn-beijing/apiKey | 火山引擎, 需开通方舟平台 |
| **DeepSeek** | `DEEPSEEK_API_KEY` | https://platform.deepseek.com/api_keys | 可选, 用于LLM意图解析 |

### 健康检查

```bash
uv run {baseDir}/scripts/check.py
```

## Workflow

1. 执行 generate_image_v3.py (优先) 或 generate_image_v2.py (V2兼容)
2. 解析输出中 `MEDIA_URL:` 开头的行
3. 用 markdown 语法展示图片: `![Generated Image](URL)`
4. 如有多张图, 逐一展示所有 `MEDIA_URL:` 行
5. 不下载图片，除非用户要求保存

## Legacy

V2脚本 `generate_image_v2.py` 仍可使用 (无模板/无意图识别):
```bash
uv run {baseDir}/scripts/generate_image_v2.py --prompt "描述" --provider auto
```

V1脚本 `generate_image.py` 仅支持万相:
```bash
uv run {baseDir}/scripts/generate_image.py --prompt "描述" --model wan2.6-t2i
```

## Notes

- V3自动识别场景并匹配模板, 构建结构化prompt
- 支持 `--use-llm` 启用DeepSeek意图解析 (低置信度时)
- 图片 URL 有效期 24 小时，请及时下载保存
- Seedream 5.0 lite 支持组图 (≤15张)
