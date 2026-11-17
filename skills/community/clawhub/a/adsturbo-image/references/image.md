# AI Image Creation / Image

Script: `scripts/image.py`

## create — Text-to-Image / Image Editing

```bash
# Text-to-image
python3 scripts/image.py create --prompt "Minimalist skincare product shot, soft natural light"

# Image editing (passing image_urls means editing)
python3 scripts/image.py create --prompt "Replace the background with a marble countertop" \
  --image-urls https://.../product.jpg
```

`--image-urls` empty = text-to-image, non-empty = edit these images. Each call produces exactly one image. Returns `result_url` synchronously by default; add `--async-mode` to get back a `workspace_id` and poll it yourself.

### Model Capabilities and Parameters (Important)

The value sets for `ratio` / `resolution` **vary by model** — check the table before constructing a request:

| Model | Text-to-Image | Editing | ratio | resolution |
|---|---|---|---|---|
| `nanobanana-pro` (default) | ✅ | ✅ | 1:1 / 3:2 / 2:3 / 3:4 / 4:3 / 4:5 / 5:4 / 5:7 / 7:5 / 9:16 / 16:9 / 21:9 / 1:4 / 4:1 | 1k / 2k / 4k / 8k |
| `nano-banana-2` | ✅ | ✅ | same as above + 1:8 / 8:1 | 0.5k / 1k / 2k / 4k |
| `nano-banana-2-fast` | ✅ | ✅ | same as above + 1:8 / 8:1 | 2k / 4k |
| `seedream-5.0-pro` | ✅ | ✅ | 1:1 / 1:2 / 2:1 / 1:3 / 3:1 / 2:3 / 3:2 / 3:4 / 4:3 / 4:5 / 5:4 / 9:16 / 16:9 / 9:21 / 21:9 | 2k (default) / 1k |
| `seedream-5.0-lite` | ✅ | ✅ | 1:1 / 1:2 / 2:1 / 1:3 / 3:1 / 1:4 / 4:1 / 1:8 / 8:1 / 2:3 / 3:2 / 3:4 / 4:3 / 4:5 / 5:4 / 5:7 / 7:5 / 9:16 / 16:9 / 9:21 / 21:9 | — |
| `gpt-image-2` | ✅ | ✅ | 1:1 / 1:2 / 2:1 / 1:3 / 3:1 / 2:3 / 3:2 / 3:4 / 4:3 / 4:5 / 5:4 / 9:16 / 16:9 / 9:21 / 21:9 | 1k / 2k / 4k |
| `grok-2-image` | ✅ | — | not validated | — |
| `grok-imagine-image` | — | ✅ | 1:1 / 3:2 / 2:3 / 3:4 / 4:3 / 4:5 / 5:4 / 9:16 / 16:9 / 21:9 | — |

`grok-2-image` is text-to-image only; `grok-imagine-image` is editing only. Confirm whether the user wants text-to-image or editing before choosing a model. Leave `resolution` empty for models that do not support it.

## E-commerce and Marketing Images

```bash
# Product image set
python3 scripts/image.py ecommerce \
  --reference-image-urls https://.../product.jpg \
  --methods hero_banner lifestyle_scene close_detail \
  --user-input "Emphasize portability and quick-dry"

# Promotional poster
python3 scripts/image.py poster --event-info "Double 11, 50% off storewide, starts Nov 1" \
  --reference-image-urls https://.../logo.png
```

`ecommerce --methods` accepted values (omit to produce the default hero image):

| method | Output |
|---|---|
| `hero_banner` | Hero image (default) |
| `lifestyle_scene` | Usage scenario image |
| `how_to_use` | How-to-use image |
| `close_detail` | Close-up detail image |
| `material` | Material image |
| `brand_closing` | Brand closing image |

Passing multiple methods at once produces a full set. `--product-info` supplies product details, `--language` sets the copy language, `--aspect-ratio` sets the aspect ratio.

## Image Retouching

```bash
# Cutout (background removal)
python3 scripts/image.py cutout --image-url https://.../product.jpg --output-format png

# Watermark removal / object removal
python3 scripts/image.py erase --image-url https://.../photo.jpg \
  --instruction "Remove the watermark in the bottom-right corner"

# Upscaling
python3 scripts/image.py upscale --image-url https://.../small.jpg --scale 4
```

`erase` supports two ways of specifying what to remove: `--mask-url` for precise region marking (white = the area to remove), or `--instruction` to describe what to remove in natural language. `--quantity` can produce multiple candidates at once.

## Assets Must Be Publicly Accessible URLs

```bash
python3 scripts/upload.py image ./product.jpg
```

## Time Reference

| Operation | Estimated time |
|---|---|
| `create` | 30 seconds – 1 minute (synchronous by default) |
| `cutout` / `erase` / `upscale` | 30 seconds – 2 minutes |
| `ecommerce` / `poster` | 1–3 minutes, longer for multiple images |

All operations except `create` are asynchronous and poll automatically by default; if it times out, use `query --workspace-id <id>` to keep waiting.

---

# AI 图片创作 / Image

脚本：`scripts/image.py`

## create — 文生图 / 图片编辑

```bash
# 文生图
python3 scripts/image.py create --prompt "极简风格的护肤品摆拍，柔和自然光"

# 图片编辑（传了 image_urls 就是编辑）
python3 scripts/image.py create --prompt "把背景换成大理石台面" \
  --image-urls https://.../product.jpg
```

`--image-urls` 空 = 文生图，非空 = 编辑这些图。每次固定出 1 张。默认同步返回 `result_url`；加 `--async-mode` 则返回 `workspace_id` 自行轮询。

### 模型能力与参数（关键）

`ratio` / `resolution` 的取值集**因模型而异**，构造请求前先核对：

| 模型 | 文生图 | 编辑 | ratio | resolution |
|---|---|---|---|---|
| `nanobanana-pro`（默认） | ✅ | ✅ | 1:1 / 3:2 / 2:3 / 3:4 / 4:3 / 4:5 / 5:4 / 5:7 / 7:5 / 9:16 / 16:9 / 21:9 / 1:4 / 4:1 | 1k / 2k / 4k / 8k |
| `nano-banana-2` | ✅ | ✅ | 同上 + 1:8 / 8:1 | 0.5k / 1k / 2k / 4k |
| `nano-banana-2-fast` | ✅ | ✅ | 同上 + 1:8 / 8:1 | 2k / 4k |
| `seedream-5.0-pro` | ✅ | ✅ | 1:1 / 1:2 / 2:1 / 1:3 / 3:1 / 2:3 / 3:2 / 3:4 / 4:3 / 4:5 / 5:4 / 9:16 / 16:9 / 9:21 / 21:9 | 2k（默认）/ 1k |
| `seedream-5.0-lite` | ✅ | ✅ | 1:1 / 1:2 / 2:1 / 1:3 / 3:1 / 1:4 / 4:1 / 1:8 / 8:1 / 2:3 / 3:2 / 3:4 / 4:3 / 4:5 / 5:4 / 5:7 / 7:5 / 9:16 / 16:9 / 9:21 / 21:9 | — |
| `gpt-image-2` | ✅ | ✅ | 1:1 / 1:2 / 2:1 / 1:3 / 3:1 / 2:3 / 3:2 / 3:4 / 4:3 / 4:5 / 5:4 / 9:16 / 16:9 / 9:21 / 21:9 | 1k / 2k / 4k |
| `grok-2-image` | ✅ | — | 不校验 | — |
| `grok-imagine-image` | — | ✅ | 1:1 / 3:2 / 2:3 / 3:4 / 4:3 / 4:5 / 5:4 / 9:16 / 16:9 / 21:9 | — |

`grok-2-image` 只能文生，`grok-imagine-image` 只能编辑。选模型前先确认用户要的是文生还是编辑。`resolution` 不支持的模型必须留空。

## 电商与营销图

```bash
# 商品图套图
python3 scripts/image.py ecommerce \
  --reference-image-urls https://.../product.jpg \
  --methods hero_banner lifestyle_scene close_detail \
  --user-input "主打便携和快干"

# 活动海报
python3 scripts/image.py poster --event-info "双11 全场五折，11月1日开抢" \
  --reference-image-urls https://.../logo.png
```

`ecommerce --methods` 可选值，不传则出默认主图：

| method | 产出 |
|---|---|
| `hero_banner` | 主图（默认） |
| `lifestyle_scene` | 使用场景图 |
| `how_to_use` | 使用图 |
| `close_detail` | 细节特写图 |
| `material` | 材质图 |
| `brand_closing` | 品牌收尾图 |

一次传多个 method 就出一套图。`--product-info` 给商品参数、`--language` 定文案语言、`--aspect-ratio` 定画幅。

## 图片精修

```bash
# 抠图（去背景）
python3 scripts/image.py cutout --image-url https://.../product.jpg --output-format png

# 去水印 / 消除杂物
python3 scripts/image.py erase --image-url https://.../photo.jpg \
  --instruction "去掉右下角的水印"

# 高清放大
python3 scripts/image.py upscale --image-url https://.../small.jpg --scale 4
```

`erase` 两种指定方式：`--mask-url` 精确框定（白色为要消除的区域），或 `--instruction` 用自然语言描述消除什么。`--quantity` 可以一次出多个候选。

## 素材必须是公网 URL

```bash
python3 scripts/upload.py image ./product.jpg
```

## 耗时参考

| 操作 | 预计 |
|---|---|
| `create` | 30 秒 – 1 分钟（默认同步） |
| `cutout` / `erase` / `upscale` | 30 秒 – 2 分钟 |
| `ecommerce` / `poster` | 1–3 分钟，出多张更久 |

除 `create` 外都是异步，默认自动轮询；超时用 `query --workspace-id <id>` 续等。
