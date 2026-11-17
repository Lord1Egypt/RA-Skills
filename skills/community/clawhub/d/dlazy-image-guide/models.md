# 模型速查表

22 个图像工具的完整参数。积分为单次调用消耗，随参数变化的已标注。

数据对应 CLI `1.2.3` 时的线上清单。**清单是权威**——参数或价格存疑时用 `dlazy <model> -h` 和 `--dry-run` 现场确认，不要照抄这里的数字给用户报价。

## 文生图

| 模型 | 积分 | 提示词上限 | 尺寸参数 | 参考图 |
|---|---|---|---|---|
| `mj-imagine` | 5 | 2000 | `--aspect_ratio` | ✗ |
| `seedream-5.0-lite` | 5 | 500 | `--size 16:9` + `--resolution 2k` | ✓ |
| `seedream-5.0` | 5（4k 为 8） | 500 | `--size 16:9` + `--resolution 2k\|4k` | ✓ |
| `seedream-4.5` | 6 | 500 | `--size 16:9` + `--resolution` | ✓ |
| `seedream-5.0-pro` | 7 | 500 | `--size 16:9` + `--resolution` | ✓ |
| `banana2` | 7 / 10 / 14 / 21 | 2000 | `--imageSize 512\|1K\|2K\|4K` + `--aspectRatio` | ✓ |
| `viduq2-t2i` | 9 / 13 / 15 | 500 | `--aspectRatio` + `--resolution 1080p\|2K\|4K` | ✓ |
| `kling-image-o1` | 11 | 2500 | `--aspect_ratio` + `--clarity` | ✓ |
| `recraft-v3` | 11 | 2000 | `--aspect_ratio` + `--style` | ✗ |
| `recraft-v3-svg` | 11 | 2000 | `--aspect_ratio` + `--style` | ✗ |
| `recraft-v4` | 11 | 2000 | `--aspect_ratio` | ✗ |
| `recraft-v4-vector` | 11 | 2000 | `--aspect_ratio` | ✗ |
| `gpt-image-2` | 12 / 16 / 37 | 2000 | `--size 2048x1152` | ✓ |
| `jimeng-t2i` | 15 | 500 | `--size 2048*2048` | ✓ |
| `banana-pro` | 18（4K 为 30） | 2000 | `--imageSize 1K\|2K\|4K` + `--aspectRatio` | ✓ |
| `qwen-image-2-pro` | 20 | 1300 | `--size 2048*2048` | ✓ |
| `recraft-v4-pro` | 22 | 2000 | `--aspect_ratio` | ✗ |
| `recraft-v4-pro-vector` | 22 | 2000 | `--aspect_ratio` | ✗ |

`gpt-image-2` 的三档积分对应 `--quality low/medium/high`。**带参考图时翻倍**：25 / 33 / 60。

`banana2` 四档对应 `--imageSize 512/1K/2K/4K`。

## 图像后处理

这些工具只吃图片、不吃提示词，用来接在生成之后。

| 工具 | 积分 | 作用 | 输入 |
|---|---|---|---|
| `imageseg` | 1 | 抠图去背景 | `--image` |
| `vectorize` | 2 | 位图转矢量 | `--image` |
| `image-replicate` | 6 | 图像复刻/变体 | `--images` |
| `superres` | 10 | 超分放大 | `--image` |

抠图 1 积分、矢量化 2 积分——比重新生成便宜一个数量级。能后处理解决的，不要重新生成。

## 尺寸写法对照

这是最容易出错的地方。六种互不兼容的写法：

**像素 + `x`**（仅 `gpt-image-2`）
```
1024x1024  1536x1024  1024x1536  2048x2048
2048x1152  3840x2160  2160x3840  auto
```
16:9 只有 `2048x1152` 和 `3840x2160` 两个。

**像素 + `*`**（`jimeng-t2i`、`qwen-image-2-pro`）

`jimeng-t2i` 有 19 档，从 `1024*1024` 到 `6198*2656`，包含 4K/5K 超宽。
`qwen-image-2-pro` 只有 5 档：`2688*1536` `1536*2688` `2048*2048` `2368*1728` `1728*2368`。

**比例 + 分辨率**（seedream 全系、`viduq2-t2i`）
```
--size 1:1|4:3|3:4|16:9|9:16|3:2|2:3|21:9
--resolution 2k|4k          # vidu 用 1080p|2K|4K
```

**尺寸档 + 比例**（banana 系）
```
--imageSize 512|1K|2K|4K    # banana-pro 无 512
--aspectRatio ...
```

**只有比例**（recraft 全系、`mj-imagine`）
```
--aspect_ratio ...          # 注意是下划线
```

**比例 + 清晰度**（`kling-image-o1`）
```
--aspect_ratio ... --clarity 2k
```

注意 `--aspectRatio`（驼峰，banana/vidu）和 `--aspect_ratio`（下划线，recraft/mj/kling）的区别，写错会被当成未知参数。

## 异步与轮询

除 `gpt-image-2`、`imageseg`、`superres`、`vectorize` 外，其余均为异步任务。CLI 默认等待完成；加 `--no-wait` 立即返回 `generateId`，再用 `dlazy status <generateId> --wait` 轮询。

批量出图时用 `--no-wait` 先全部提交、再统一轮询，比串行等待快得多。

注意：即使工具标记为同步，服务端仍可能返回 `generateId`。自己写客户端时两种响应形状都要兼容。

## 输出

所有工具返回 `files.dlazy.com` 上的 URL：

```json
{"ok": true, "result": {"outputs": [{"type": "image", "url": "https://files.dlazy.com/....png"}]}}
```

传入本地图片路径时，CLI 会先上传到 `files.dlazy.com` 再引用。
