# EOS 图片处理参数参考

本文档汇总 EOS 图片处理的专用规则与参数字典，供 `scripts/eos_image.mjs` 和 skill 调用时查阅。

官方文档入口：

- 图片处理概述：https://ecloud.10086.cn/op-help-center/doc/article/95187
- 图片缩放：https://ecloud.10086.cn/op-help-center/doc/article/94758
- 自定义裁剪：https://ecloud.10086.cn/op-help-center/doc/article/94759
- 索引切割：https://ecloud.10086.cn/op-help-center/doc/article/95194
- 内切圆：https://ecloud.10086.cn/op-help-center/doc/article/95191
- 圆角矩形：https://ecloud.10086.cn/op-help-center/doc/article/95195
- 旋转：https://ecloud.10086.cn/op-help-center/doc/article/95197
- 格式转换：https://ecloud.10086.cn/op-help-center/doc/article/95196
- 质量变换：https://ecloud.10086.cn/op-help-center/doc/article/95200
- 图片水印：https://ecloud.10086.cn/op-help-center/doc/article/94762
- 获取图片信息：https://ecloud.10086.cn/op-help-center/doc/article/95198
- 获取图片主色调：https://ecloud.10086.cn/op-help-center/doc/article/95205
- 模糊效果：https://ecloud.10086.cn/op-help-center/doc/article/95206
- 亮度：https://ecloud.10086.cn/op-help-center/doc/article/95207
- 锐化：https://ecloud.10086.cn/op-help-center/doc/article/95208
- 对比度：https://ecloud.10086.cn/op-help-center/doc/article/95209

## 总体规则

- 图片处理只针对 EOS 中已有的图片对象。
- 请求统一通过 `GET /<bucket>/<key>?x-eos-process=<process-string>` 发起。
- 公共读对象可直接拼接 `x-eos-process`；私有对象必须把该查询参数纳入签名 URL。
- 处理型动作返回图片字节流，查询型动作如 `info`、`average-hue` 返回文本结果。
- EOS 默认不保存处理后的结果；只有追加 `|sys/saveas,...` 时才会把结果写回桶。
- 支持的原图格式包括：`BMP`、`PNG`、`GIF`、`JPEG`、`JPG`、`WEBP`、`TIFF`、`PPM`、`MNG`、`HEIC`、`HEIF`、`AVIF`、`PSD`、`DNG`，并支持 `livp`。
- 官方文档提示：并发超过 50 且原图大于 2 MB 的高计算场景，建议先咨询工单确认实际限制。

## 资源池

官方概述文档当前列出的可用资源池：

- fenhu1    （华东-苏州3）
- beijing7  （华北-北京6）
- ningbo1   （华东-杭州）
- zhengzhou1（华中-郑州）
- zhengzhou4（华中-郑州2）
- fujian1   （福建-厦门）
- fujian2   （福建-厦门2）
- fujian3   （福建-厦门3）

## 处理串格式

基础格式：

```text
image/<action>[,<param>_<value>...]/<action>[,<param>_<value>...]
```

持久化格式：

```text
image/<action>[,<param>_<value>...]/...|sys/saveas,o_<object-key-base64url>,b_<bucket-base64url>
```

规则说明：

- `image` 表示图片处理资源类型。
- 同一个 step 内，action 和参数用逗号分隔。
- 参数名与参数值之间使用下划线 `_`。
- 多个 step 之间使用 `/`，按顺序执行。
- `sys/saveas` 必须放在整条处理串末尾。
- `sys/saveas` 中：
  - `o` 为目标对象 key 的 URL-safe Base64
  - `b` 为目标桶名的 URL-safe Base64

## 常见组合示例

```text
image/resize,m_lfit,w_400,h_400
image/crop,g_center,w_300,h_300
image/resize,w_800,h_800/rounded-corners,r_24
image/resize,w_800,h_800/format,png
image/watermark,text_SGVsbG8,color_FFFFFF,size_36,g_southeast,x_20,y_20
image/info
image/average-hue
image/resize,w_1024,h_1024/format,png|sys/saveas,o_ZGVyaXZlZC9hLTAxLnBuZw,b_bXktYnVja2V0
```

## Action 字典

### `resize`

用途：缩放图片。

参数：

| 参数 | 是否必填 | 说明 | 取值 |
|---|---|---|---|
| `m` | 否 | 缩放模式 | `lfit` 默认、`mfit`、`fill`、`pad`、`fixed` |
| `w` | 否 | 目标宽度 | `[1,4096]` |
| `h` | 否 | 目标高度 | `[1,4096]` |
| `p` | 否 | 按百分比等比缩放 | `[1,1000]` |
| `limit` | 否 | 是否允许放大 | `1` 默认不放大；`0` 按参数缩放 |
| `color` | 条件必填 | `m=pad` 时的填充色 | 十六进制 RGB，默认 `000000` |

补充：

- `{w,h}` 与 `{p}` 冲突时，优先使用 `{w,h}`。
- `fill`、`pad`、`fixed` 建议同时指定 `w` 和 `h`。
- GIF 只支持缩小，不支持放大。

示例：

```text
image/resize,m_lfit,w_300,h_160
image/resize,m_pad,w_300,h_160,color_abcdef
image/resize,p_50
```

### `crop`

用途：按矩形区域裁剪。

参数：

| 参数 | 是否必填 | 说明 | 取值 |
|---|---|---|---|
| `w` | 否 | 裁剪宽度 | `[1,4096]` |
| `h` | 否 | 裁剪高度 | `[1,16384]` |
| `x` | 否 | 起点横坐标 | `[0,4096]` |
| `y` | 否 | 起点纵坐标 | `[0,4096]` |
| `g` | 否 | 原点位置 | `nw` 默认、`north`、`ne`、`west`、`center`、`east`、`sw`、`south`、`se` |

补充：

- `x` 或 `y` 超出限制时返回原图。
- 超出原图边界时，裁剪到边界为止。

示例：

```text
image/crop,x_100,y_50,w_100,h_100
image/crop,g_se,w_100,h_100
```

### `indexcrop`

用途：按固定步长切割后返回指定索引块。

参数：

| 参数 | 是否必填 | 说明 | 取值 |
|---|---|---|---|
| `x` | 二选一 | x 轴切割块宽度 | `[1,4096]` |
| `y` | 二选一 | y 轴切割块高度 | `[1,16384]` |
| `i` | 否 | 返回第几个切块 | `[0,4096)`，默认 `0` |

补充：

- `x` 与 `y` 只能任选其一。

示例：

```text
image/indexcrop,x_100,i_0
image/indexcrop,y_100,i_0
```

### `circle`

用途：裁成内切圆。

参数：

| 参数 | 是否必填 | 说明 | 取值 |
|---|---|---|---|
| `r` | 否 | 圆半径 | `[1,2048]` |

补充：

- 半径不能超过原图最小边的一半，超出时按最大内切圆处理。
- PNG、WebP、TIFF 圆外区域透明；JPG 等其他格式圆外区域白色填充。

示例：

```text
image/circle,r_100
```

### `rounded-corners`

用途：裁成圆角矩形。

参数：

| 参数 | 是否必填 | 说明 | 取值 |
|---|---|---|---|
| `r` | 否 | 圆角半径 | `[1,8192]` |

补充：

- PNG、WebP、TIFF 圆角外区域透明；JPG 等其他格式圆角外区域白色填充。

示例：

```text
image/rounded-corners,r_50
```

### `rotate`

用途：旋转图片。

参数：

| 参数 | 是否必填 | 说明 | 取值 |
|---|---|---|---|
| 角度值 | 是 | 顺时针旋转角度 | `[-360,360]` |

补充：

- 负数表示逆时针。
- 非 90 度倍数时，结果尺寸可能增大，并产生空白填充。

示例：

```text
image/rotate,90
image/rotate,-45
```

### `format`

用途：转换输出格式。

支持值：

- `jpg`
- `png`
- `webp`
- `bmp`
- `gif`
- `tiff`

示例：

```text
image/format,png
image/resize,w_1200,h_1200/format,webp
```

### `quality`

用途：调整压缩质量。

参数：

| 参数 | 是否必填 | 说明 | 取值 |
|---|---|---|---|
| `q` | 二选一 | 相对质量 | `[1,100]` |
| `Q` | 二选一 | 绝对质量 | `[1,100]` |

补充：

- `q` 是按原图质量的百分比再压缩。
- `Q` 是压到目标质量；若原图质量本身更低，则以原图质量为准。
- 官方文档说明：只有 JPG 能真正体现相对质量；WebP 等格式传 `q` 时效果等同于指定绝对质量。

示例：

```text
image/quality,q_80
image/quality,Q_90
```

### `watermark`

用途：添加图片水印或文字水印。

基础参数：

| 参数 | 是否必填 | 说明 | 取值 |
|---|---|---|---|
| `t` | 否 | 透明度 | `[0,100]`，默认 `100` |
| `g` | 否 | 水印位置 | `northwest`、`north`、`northeast`、`west`、`center`、`east`、`southwest`、`south`、`southeast` 默认 |
| `x` | 否 | 水平边距 | `[0,4096]`，默认 `10` |
| `y` | 否 | 垂直边距 | `[0,4096]`，默认 `10` |

图片水印参数：

| 参数 | 是否必填 | 说明 | 取值 |
|---|---|---|---|
| `image` | 是 | 同桶内水印图片对象名 | URL-safe Base64 |

文字水印参数：

| 参数 | 是否必填 | 说明 | 取值 |
|---|---|---|---|
| `text` | 是 | 水印文字内容 | URL-safe Base64；原始中文最大 64 字节 |
| `color` | 否 | 文字颜色 | 十六进制 RGB，默认 `000000` |
| `size` | 否 | 文字大小 | `(0,1000]`，默认 `40` |
| `rotate` | 否 | 文字顺时针旋转 | `[0,360]`，默认 `0` |

补充：

- 图片水印只能引用当前桶内对象。
- 图片水印仅支持 `JPG`、`PNG`、`BMP`、`WebP`、`TIFF`。
- 同一张图上的多个图片水印位置不能完全重叠。
- 文字水印暂不支持繁体中文。
- 带 Alpha 通道的 PNG 添加水印可能遮挡，官方建议追加 `/format,jpeg` 规避。

示例：

```text
image/watermark,text_SGVsbG8gV29ybGQ,color_FFFFFF,size_36,g_southeast,x_20,y_20
image/watermark,image_aW1hZ2UvcGFuZGEucG5n,t_80,g_center
```

### `info`

用途：获取图片基本信息和 EXIF 信息。

参数：无。

返回：XML 文本。

示例：

```text
image/info
```

### `average-hue`

用途：获取图片主色调。

参数：无。

返回：XML 文本，`<RGB>` 中为主色调值。

示例：

```text
image/average-hue
```

### `blur`

用途：高斯模糊。

参数：

| 参数 | 是否必填 | 说明 | 取值 |
|---|---|---|---|
| `r` | 是 | 模糊半径 | `[1,50]` |
| `s` | 是 | 标准差 | `[1,50]` |

示例：

```text
image/blur,r_3,s_2
image/blur,r_15,s_15
```

### `bright`

用途：调整亮度。

参数：

| 参数 | 是否必填 | 说明 | 取值 |
|---|---|---|---|
| 亮度值 | 是 | 亮度增减幅度 | `[-100,100]` |

补充：

- 小于 `0` 表示降低亮度。
- 等于 `0` 表示不调整。
- 大于 `0` 表示提高亮度。

示例：

```text
image/bright,50
image/bright,-50
```

### `sharpen`

用途：锐化图片。

参数：

| 参数 | 是否必填 | 说明 | 取值 |
|---|---|---|---|
| 锐化值 | 是 | 锐化强度 | `[50,399]` |

补充：

- 数值越大越清晰，但可能产生失真。

示例：

```text
image/sharpen,100
image/sharpen,50
```

### `contrast`

用途：调整对比度。

参数：

| 参数 | 是否必填 | 说明 | 取值 |
|---|---|---|---|
| 对比度值 | 是 | 对比度增减幅度 | `[-100,100]` |

补充：

- 小于 `0` 表示降低对比度。
- 等于 `0` 表示维持原图。
- 大于 `0` 表示提高对比度。

示例：

```text
image/contrast,50
image/contrast,-50
```
