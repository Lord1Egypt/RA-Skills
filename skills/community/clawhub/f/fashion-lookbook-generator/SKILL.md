---
name: fashion-lookbook-generator
display_name: 服装种草图一键生成
display_name_en: Fashion Lookbook Generator
description: 一张服装参考图（或一个 Pinterest pin 链接）生成 6 类风格统一的种草/带货图（穿搭图、平铺图、单品细节、场景图、情侣搭配、品牌故事）。基于小红书/Pinterest 爆款内容结构，使用 ImageGen 图生图，遵循真实场景、自然光、胶片颗粒等去 AI 味风格锚点。触发词：种草图、穿搭图、lookbook、带货图、服装出图、平铺图、种草内容、服装营销图、pinterest链接、pin链接、pinterest 图片抓取。
description_zh: 一张服装参考图或 Pinterest 链接秒出 6 类风格统一的小红书/Pinterest 种草图
description_en: Generate 6 types of styled marketing photos from one clothing reference image or Pinterest link
category: multimodal
version: 1.1.0
author: 七上八下来打卡
---

# 服装种草图一键生成

## 📝 简介

输入一张服装参考图（产品图/穿搭照/电商图均可），自动产出 **6 类风格统一的种草图**，覆盖小红书和 Pinterest 高流量内容形态。全程使用 ImageGen 图生图，保持单品高度还原的同时注入真实生活质感。

## 🎯 六类输出与流量占比

| # | 类目 | 英文 | 流量占比 | input_fidelity | 场景要求 |
|---|------|------|---------|----------------|---------|
| 1 | Outfit 穿搭图 | Outfit | ~50% | 0.85 | 真人全身，行走/抓拍，真实场所（画廊、街角、地铁口） |
| 2 | Flat Lay 平铺图 | Flat Lay | ~10% | 0.78 | 俯拍，亚麻床单/木地板，加咖啡杯、杂志、香氛等道具 |
| 3 | 单品细节图 | Detail | ~15% | 0.70 | 面料纹理+五金配饰特写，浅景深 |
| 4 | Lifestyle 场景图 | Lifestyle | ~20% | 0.85 | 书店、咖啡店、艺术区等生活化场景，侧影/背影/半身 |
| 5 | 情侣搭配图 | Couple | - | 0.80 | 两人配色呼应，并肩街拍，中景 |
| 6 | 品牌故事图 | Brand Story | - | 0.75 | 静物组合，木椅搭衣、开放笔记本、晨光工作室，静奢氛围 |

> 通用参数：比例 3:4（`1024x1536`，小红书默认）；Pinterest 用 2:3。quality=high，style=photorealistic。

## 🎨 全程风格锚点（去 AI 味关键）

**必须包含**：
- `film photography aesthetic, soft film grain`（胶片颗粒）
- `natural window light / natural daylight`（自然光，禁棚拍灯）
- `candid, unposed, mid-stride, relaxed posture`（抓拍感，非摆拍）
- `real skin texture, natural skin`（真实肤质）
- `muted neutral color palette`（克制配色，以参考图主色系为准）
- `35mm lens / shallow depth of field`（镜头语言）

**必须禁用（写进 negative 语境）**：
- `no glossy sheen, no plastic skin, no waxy skin`（油光/塑料蜡感皮肤）
- `no harsh studio light, no white background`（棚拍白底）
- `no symmetrical posing`（对称呆板站姿）

## ⚙️ 工作流程

### Step 0: 判断输入类型

- 输入是**图片**（上传/粘贴/剪贴板截图）→ 直接进入 Step 1 收集输入
- 输入是 **Pinterest 链接**（`pinterest.com/pin/...`、`pin.it/...`）→ 先执行 **1A 抓图**，把主图下载到 `inputs/` 后再继续
- 输入是**其他链接**（公众号、小红书等网页）→ 先 WebFetch 提取正文，看是否含可用的服装图，再决定抓图或请用户直接给图

### Step 1: 收集输入

| 参数 | 提取规则 | 默认值 |
|------|---------|--------|
| 参考图 | 用户上传/粘贴的图片，保存到 `工作区/inputs/clothing_reference.jpg` | 必填 |
| Pinterest 链接 | 用户输入 `pinterest.com/pin/<id>` / `pin.it/<code>` 链接 → 先抓图再走图生图 | 二选一 |
| 比例 | 小红书→3:4；Pinterest→2:3 | 3:4 (1024x1536) |
| 模特 | 用户指定性别/人种/风格 | 东亚年轻女性 |
| 平台 | 小红书 / Pinterest | 小红书 |

**找图技巧**：用户粘贴的剪贴板截图通常在 `~/.workbuddy/clipboard-images/` 下，按时间取最新一张复制到工作区。

#### 1A. Pinterest 链接输入（新增）

当输入是 Pinterest pin 链接（`https://www.pinterest.com/pin/<pin_id>/` 或短链 `pin.it/<code>`）时，**先调用 `pinterest` skill 抓取主图**，把图片下载到 `工作区/inputs/` 后再走 Step 2 图生图流程。

> ⚠️ Pinterest 对未登录/爬虫请求可能返回**通用 fallback 页面**，其 og:image 固定为 `https://i.pinimg.com/originals/08/51/1c/08511c2b9f82a35a6eae7c0100f17c36.jpg`（尺寸 736×1308，标题常含 "Neat casual outfits"），这**不是**该 pin 的真实主图。必须通过以下校验发现 fallback：
> - 页面 HTML 中搜索 pin id，若**完全搜不到** → 极大可能是 fallback 页
> - 下载后计算 md5，若与已知 fallback 图相同 → 确认 fallback
> - 真实 pin 页的 title 会与该 pin 内容匹配

**推荐方法（真实渲染，避免 fallback）：**

```
1. 用 agent-browser 打开 pin 页（Pinterest 是 JS 渲染 SPA，curl 拿不到真实图）：
   # 若环境代理导致 Chromium 报 net::ERR_NO_SUPPORTED_PROXIES，先关闭 daemon 再重启浏览器重试：
   # （代理类问题按本机网络环境调整，不同机器配置不同，不要照搬其他环境的代理命令）
   agent-browser close --all
   agent-browser open "https://www.pinterest.com/pin/<pin_id>/"

2. 从渲染后的页面提取真实 og:image 和标题：
   agent-browser eval "document.querySelector('meta[property=\"og:image\"]')?.content"
   agent-browser eval "document.title"

3. 得到的 og:image 通常是 736x 尺寸（如 https://i.pinimg.com/736x/{hash}.jpg），直接用 736x URL 下载：
   curl -s -L "https://i.pinimg.com/736x/{hash}.jpg" \
     -H "User-Agent: Mozilla/5.0 ..." \
     -H "Referer: https://www.pinterest.com/" \
     -o "工作区/inputs/pinterest_reference.jpg"
   # 注意：i.pinimg.com 的 originals/{hash}.jpg 经常返回 403，优先使用页面给出的 736x URL

4. 用 PIL 验证 size/mode 非空，然后进入单品清单流程
```

**轻量方法（仅适用于部分 pin，可能 fallback）：**

```
1. 抓取 pin 页面 HTML：
   curl -s -L "https://www.pinterest.com/pin/<pin_id>/" \
     -H "User-Agent: Mozilla/5.0 ... Chrome/126.0" \
     -H "Accept-Language: en-US,en;q=0.9" --max-time 30 -o tmp/pin_page.html

2. 提取 og:image（警惕 fallback）：
   grep -o -E '<meta[^>]*property="og:image"[^>]*>' tmp/pin_page.html

3. 校验：页面中应能搜到 pin_id；title 应对应真实内容；下载图 md5 不应等于 fallback 图
```

- 抓不到或 fallback 时兜底：使用 agent-browser 渲染（推荐），或 Pinterest 官方 OAuth API（见 `~/.workbuddy/skills/pinterest/references/`）。
- 下载的图即作为参考图，后续 input_fidelity / 单品清单流程完全一致。

### Step 2: 建立单品清单

仔细读参考图，逐项列出（不漏单品，写入每条提示词）：
- 上装/下装/鞋/包（颜色+版型+材质，如"light gray oversized crewneck sweatshirt"）
- 配饰：项链/耳环/手表/墨镜（如"layered gold necklaces, gold hoop earrings, gold rectangular watch with mesh bracelet"）
- 其他：香水、手机壳等画面内道具

### Step 3: 推导候选场景

按 风格 × 正式度 × 季节 匹配真实场景，优先：美术馆/画廊、书店、街角咖啡、老城区街道、极简工作室。**禁止**：白墙棚拍、纯色背景。

### Step 4: 预览提示词 + 确认成本

向用户展示 6 条提示词矩阵（类目/场景/input_fidelity），说明约消耗 30–60 ImageGen 积分，确认后再出图。

### Step 5: 逐张出图

调用 ImageGen（ToolSearch 加载 → DeferExecuteTool 执行）：

```
ImageGen:
  prompt:  <单品清单> + <场景> + <风格锚点> + <禁用词>
  image:   ["<参考图绝对路径>"]
  size:    "1024x1536"
  quality: "high"
  style:   "photorealistic"
  input_fidelity: 按类目表
  output_dir: "<工作区>/outputs"
```

生成后重命名为 `01_outfit.png` ~ `06_brand_story.png`。

### Step 6: 汇总 + 发布建议

- **标题**：突出配色公式 + 情绪价值，如「灰蓝金三件套｜不费力的高级感」
- **标签**：#ootd #cleanfit #quietluxury + 单品词（#卫衣穿搭 #牛仔裤穿搭）
- **链接位**：平铺图/细节图放购买入口；穿搭图/场景图当首图引流
- present_files 展示全部 6 张

## 💡 提示词模板（可直接套用）

```
A candid full-body fashion editorial shot of a young East Asian woman wearing
<单品清单>. She is <动作: walking through / browsing in> <真实场景>.
Film photography aesthetic, soft grain, natural skin texture, relaxed posture,
mid-stride movement, unposed, 35mm lens, muted neutral color palette of <主色系>.
No glossy sheen, no plastic skin, no symmetrical posing.
```

## ⚠️ 注意事项

- 情侣图需为同伴设计**呼应但不撞色**的第二套 outfits（同色系不同单品）
- 平铺图道具别堆太满，非对称构图留白
- 细节图 input_fidelity 调低（0.70），避免过度复刻参考图构图
- 品牌故事图走"静奢"路线：旧木椅、open notebook、陶瓷杯、盆栽、晨光
- 换季/换品类（美妆、家居）同样适用此结构，调整场景库即可
