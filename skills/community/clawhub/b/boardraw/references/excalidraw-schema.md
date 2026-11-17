# Excalidraw (.excalidraw) 原始 JSON 格式参考

只有在 `scripts/excalidraw_builder.py` 提供的方法满足不了需求时才需要读这份文档——多数情况下直接用 builder 就够了。

## 文件顶层结构

```json
{
  "type": "excalidraw",
  "version": 2,
  "source": "https://excalidraw.com",
  "elements": [ ... ],
  "appState": { "gridSize": null, "viewBackgroundColor": "#ffffff" },
  "files": {}
}
```

`files` 用于内嵌图片元素的 base64 数据，key 是 `fileId`，普通图形/文字/箭头场景用不到，留空对象即可。

## 所有元素通用字段

| 字段 | 说明 |
|---|---|
| `id` | 唯一字符串，随便生成（builder 用 16 位随机字母数字） |
| `type` | `rectangle` \| `ellipse` \| `diamond` \| `arrow` \| `line` \| `text` \| `freedraw` \| `image` \| `frame` |
| `x`, `y` | 元素外接矩形左上角坐标（对 arrow/line 是 points 里最小 x/y 对应的位置） |
| `width`, `height` | 外接矩形宽高 |
| `angle` | 弧度制旋转角，一般填 `0` |
| `strokeColor` | 描边色，十六进制，如 `#1e1e1e` |
| `backgroundColor` | 填充色，`transparent` 或十六进制 |
| `fillStyle` | `hachure`（默认，手绘斜线填充）\| `cross-hatch` \| `solid`（纯色块） |
| `strokeWidth` | 1（细）/ 2（中，默认）/ 4（粗） |
| `strokeStyle` | `solid` \| `dashed` \| `dotted` |
| `roughness` | 0（建筑师风格，接近直线）/ 1（艺术家风格，默认，手绘感）/ 2（卡通风格，更夸张） |
| `opacity` | 0–100 |
| `groupIds` | 分组 id 数组，多个元素共用同一个 id 即可编组 |
| `frameId` | 所属 frame 的 id，不属于任何 frame 就是 `null` |
| `roundness` | 矩形/图片是否圆角：圆角填 `{"type": 3}`，直角填 `null`；箭头/线条的平滑角是 `{"type": 2}` |
| `seed` | 随机整数，决定手绘笔触的随机形状，任意随机数即可 |
| `version` | 从 1 开始，每次编辑 +1 |
| `versionNonce` | 随机整数，每次编辑换一个新值 |
| `isDeleted` | `false` |
| `boundElements` | 数组，记录"哪些元素绑定在我身上"，格式 `[{"id": "...", "type": "text"}]` 或 `"arrow"`。**双向关系**：形状绑定了文字，文字也要通过 `containerId` 指回形状；箭头绑定了两个形状，两个形状的 `boundElements` 里也都要包含这条箭头 |
| `updated` | 毫秒时间戳 |
| `link` | `null` 或点击元素跳转的 URL |
| `locked` | `false` |

## `text` 专有字段

- `text` / `originalText`：显示文字，两者保持一致即可
- `fontSize`：16 (S) / 20 (M，默认) / 28 (L) / 36 (XL)
- `fontFamily`：1 = Excalifont（手写体，默认）/ 2 = Helvetica（普通印刷体）/ 3 = Cascadia Code（等宽代码字体）
- `textAlign`：`left` \| `center` \| `right`
- `verticalAlign`：`top` \| `middle` \| `bottom`
- `containerId`：如果这段文字是"绑定"在某个形状/箭头里的标签（用 `label()` / `arrow(..., label=...)` 生成），这里填容器元素的 id；独立文本填 `null`
- `lineHeight`：约 1.25

绑定文字的位置需要按容器居中计算（`x = 容器x + (容器宽 - 文字宽)/2`，`y` 同理）——`ExcalidrawDoc.label()` 已经处理好了这个计算，手写时不要漏。

## `arrow` / `line` 专有字段

- `points`：坐标数组 `[[x1,y1],[x2,y2],...]`，**是相对元素自身 x/y 的相对坐标**，第一个点通常是 `[0,0]`
- `startBinding` / `endBinding`：`null`（不吸附任何节点）或 `{"elementId": "...", "focus": 0, "gap": 4}`，只有 `arrow` 有这两个字段，`line` 恒为 `null`
- `startArrowhead` / `endArrowhead`：`null`（无箭头）\| `"arrow"`（默认三角箭头）\| `"triangle"` \| `"dot"` \| `"bar"`。普通流程图箭头是 `startArrowhead: null, endArrowhead: "arrow"`；双向箭头两端都填非 null；`line` 没有这两个字段（或都填 `null`）
- `lastCommittedPoint`：`null` 即可

## `frame` 专有字段

- `name`：显示在 frame 左上角的标题
- frame 本身不需要 `boundElements`，被框住的子元素通过自己的 `frameId` 指向这个 frame 的 `id` 即可，不需要 frame 反向记录成员列表

## `freedraw`（自由手绘笔触，builder 未封装，需要时手写）

```json
{
  "type": "freedraw",
  "points": [[0,0],[2,3],[5,8], ...],
  "pressures": [],
  "simulatePressure": true,
  "strokeColor": "#1e1e1e",
  "backgroundColor": "transparent",
  "fillStyle": "hachure",
  "roughness": 1,
  "opacity": 100
}
```
其余通用字段同上。`points` 同样是相对坐标。

## `image`（builder 未封装，需要时手写）

图片元素需要同时在顶层 `files` 里塞入 base64 数据：

```json
// elements 里
{
  "type": "image",
  "fileId": "abc123",
  "status": "saved",
  "x": 40, "y": 40, "width": 200, "height": 150,
  "scale": [1, 1]
}
// 顶层 files 里
"files": {
  "abc123": {
    "mimeType": "image/png",
    "id": "abc123",
    "dataURL": "data:image/png;base64,....",
    "created": 1700000000000
  }
}
```

## 调色板（Excalidraw 默认色板，builder 里 `stroke=`/`bg=` 的字符串取值）

描边色（`STROKE_COLORS`）：`black #1e1e1e` / `red #e03131` / `green #2f9e44` / `blue #1971c2` / `orange #f08c00`

填充色（`BG_COLORS`）：`transparent` / `red #ffc9c9` / `green #b2f2bb` / `blue #a5d8ff` / `yellow #ffec99` / `orange #ffd8a8` / `violet #d0bfff`

也可以直接传任意十六进制字符串，不局限于上面这几个预设名字。
