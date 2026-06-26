# 易见类型定义指南

## 概述

易见平台处理视觉信息并返回结构化数据。理解这些类型可帮助你有效地使用技能输入和输出。

## 核心类型

### 基本类型

这些是在整个平台中使用的标量值。

| 类型 | 描述 | 示例 |
|------|------|------|
| `String` | 文本数据 | `"hello"` |
| `TemplateString` | 格式化文本 | `"Result: {value}"` |
| `Integer` | 整数 | `42` |
| `Double` | 浮点数 | `3.14` |
| `Boolean` | 真/假 | `true` |
| `Time` | 时间戳 | `"2026-03-12T10:00:00Z"` |

### 复杂类型

这些是包含视觉或检测信息的结构化对象。

#### Detection（检测）

表示图像中的检测对象。

```json
{
  "bbox": [x, y, width, height],
  "confidence": 0.94,
  "category": {
    "id": "person",
    "name": "人体",
    "confidence": 0.98
  },
  "track_id": 1,
  "ocr": null,
  "keypoints": null
}
```

**字段**：
- `bbox` - 边框 [x, y, width, height]（像素坐标）
- `confidence` - 检测置信度（0-1）
- `category` - 对象分类，包含 id、name、confidence
- `track_id` - 跟踪 ID（用于帧间跟踪，可选）
- `ocr` - 文本识别结果（可选）
- `keypoints` - 姿态/骨骼关键点（可选）

#### TrackDetection（跟踪检测）

与 `Detection` 相同，但用于视频帧间的时间跟踪。

#### Attribute（属性）

表示图像中检测到的属性或属性。

```json
{
  "attribute": "age",
  "answer": "adult",
  "confidence": 0.87
}
```

**字段**：
- `attribute` - 属性名称（例如"age"、"gender"、"expression"）
- `answer` - 属性值
- `confidence` - 置信度分数

#### Image（图像）

表示技能的视觉输入。

```json
{
  "imageData": "base64-encoded-image-data",
  "imageWidth": 1920,
  "imageHeight": 1080,
  "sourceId": "abc123def456",
  "imageId": "img001",
  "timestamp": 1705056000000
}
```

**字段**：
- `imageData` - Base64 编码的图像字节（从文件路径自动编码）
- `imageWidth` - 图像宽度（像素）
- `imageHeight` - 图像高度（像素）
- `sourceId` - 源标识符，用于视频流（文件 MD5 哈希）
- `imageId` - 唯一的图像标识符
- `timestamp` - 帧时间戳（毫秒）

#### ROI（关注区域 / 电子围栏）

定义用于分析的多边形区域。

**完整工作流：** 见 [roi-workflow.md](./roi-workflow.md)

**数据结构**:

```json
{
  "kind": "ROI",
  "name": "entrance",
  "points": [x1, y1, x2, y2, x3, y3, x4, y4]
}
```

**字段说明**:
- `kind` - 固定值"ROI"
- `name` - 区域描述名称（可选）
- `points` - 多边形顶点坐标数组，按顺序排列：`[x1,y1, x2,y2, x3,y3, ...]`

**示例**:

**矩形ROI - 收银区域**
```json
{
  "kind": "ROI",
  "name": "checkout-zone",
  "points": [100, 100, 300, 100, 300, 250, 100, 250]
}
```

**多边形ROI - L形仓库区域**
```json
{
  "kind": "ROI",
  "name": "warehouse-l-zone",
  "points": [100, 100, 400, 100, 400, 200, 300, 200, 300, 350, 100, 350]
}
```

**网格坐标输入**:
使用 `show-grid.mjs` 生成的网格坐标：
```
B1, E1, E3, B3  →  自动转换为像素坐标
```

#### Tripwire（绊线 / 穿越检测线）

定义用于穿越事件的检测线。

**完整工作流：** 见 [tripwire-workflow.md](./tripwire-workflow.md)

**核心概念 - 向量点乘法则**:

绊线穿越检测使用向量点乘：

1. **绊线向量** = p1 → p2 方向
2. **运动向量** = 前一帧到当前帧的对象移动
3. **点乘计算**：`dot = V_line.x * V_motion.x + V_line.y * V_motion.y`
4. **穿越判定**：
   - `dot > 0` → 正向穿越（Forward，A→B）
   - `dot < 0` → 反向穿越（Backward，B→A）
   - TwoWay: 两个方向都检测

**数据结构**:

```json
{
  "kind": "TripWire",
  "name": "door-entrance",
  "direction": "Forward",
  "points": [p1_x, p1_y, p2_x, p2_y, p3_x, p3_y, p4_x, p4_y]
}
```

**字段说明**:
- `kind` - 固定值"TripWire"
- `name` - 检测线描述名称（可选）
- `direction` - "Forward" | "Backward" | "TwoWay"
- `points` - 8元素数组：
  - p1, p2: 主检测线（用户指定）
  - p3, p4: A-B区域标记（标识穿越方向）

**自动生成A-B点**:

用户可以只提供 **2个点**（p1, p2 主检测线），系统会自动生成 **p3, p4**（A-B区域标记）：

1. **输入**: 用户给出2个点 `[p1_x, p1_y, p2_x, p2_y]`
2. **自动计算**:
   ```
   dx, dy = 主线方向向量 (p2 - p1)
   perpX, perpY = 旋转90度得到垂直向量
   distance = 30px (默认)
   p3 = p1 + perp * distance  (A区域标记)
   p4 = p2 + perp * distance  (B区域标记)
   ```
3. **结果**: 自动补全为完整的4点结构 `[p1_x, p1_y, p2_x, p2_y, p3_x, p3_y, p4_x, p4_y]`
4. **生成预览图**: 使用 `visualize.mjs` 将Tripwire可视化
   ```bash
   node scripts/visualize.mjs <image> '[]' preview.png \
     --overlays '[{
       "kind": "TripWire",
       "name": "绊线预览",
       "direction": "Forward",
       "points": [p1_x, p1_y, p2_x, p2_y, p3_x, p3_y, p4_x, p4_y]
     }]'
   ```
   输出：`preview.png` 显示绊线虚线、A/B标记、方向箭头
5. **用户确认**: 显示预览图让用户确认：
   - A/B区域位置是否正确
   - 方向箭头是否指向期望方向
   - 绊线是否跨越检测区域

**示例**:

用户输入：`[150, 100, 150, 300]` (竖直线)
系统自动生成：`[150, 100, 150, 300, 120, 100, 120, 300]` (左偏30px)
生成预览：
```bash
node scripts/visualize.mjs door.jpg '[]' preview.png \
  --overlays '[{"kind":"TripWire","name":"门","direction":"Forward","points":[150,100,150,300,120,100,120,300]}]'
```
用户看预览图确认A(左)→B(右)方向是否符合预期

**结构可视化**:
```
p1 --------> p2  (主检测线，p1→p2)
 ^            ^
 |            |
p3           p4  (A-B区域标记)

• Forward: 检测p3→p4方向的穿越（A→B）
• Backward: 检测p4→p3方向的穿越（B→A）
• TwoWay: 双向都检测
```

**方向可视化**:
- **Forward** - 绿色箭头在p4，表示A→B方向
- **Backward** - 红色箭头在p3，表示B→A方向
- **TwoWay** - 蓝色箭头在p3和p4，表示双向

**示例**:

**垂直检测线 - 人员进出统计**

```json
{
  "kind": "TripWire",
  "name": "door-entrance",
  "direction": "Forward",
  "points": [150, 100, 150, 300, 130, 100, 170, 300]
}
```

说明：
- p1(150,100) → p2(150,300): 竖直线
- p3(130,100) → p4(170,300): A-B标记（左右偏移30px）
- Forward: 只检测从左→右的穿越

**水平检测线 - 考勤打卡**

```json
{
  "kind": "TripWire",
  "name": "checkin-line",
  "direction": "TwoWay",
  "points": [100, 200, 400, 200, 100, 180, 400, 220]
}
```

说明：
- p1(100,200) → p2(400,200): 水平线
- p3(100,180) → p4(400,220): A-B标记（上下偏移20px）
- TwoWay: 双向都统计

### 数组类型

任何类型都可以包装在数组中：

```json
{
  "type": "Array<Detection>",
  "example": [
    { "bbox": [...], "confidence": 0.9, ... },
    { "bbox": [...], "confidence": 0.85, ... }
  ]
}
```

常见数组：
- `Array<Detection>` - 多个检测对象
- `Array<TrackDetection>` - 帧间跟踪的对象
- `Array<Attribute>` - 多个属性结果
- `Array<ROI>` - 多个区域
- `Array<Tripwire>` - 多条检测线

## 可视化和交互

### 检测可视化

使用 `visualize.mjs` 在图像上可视化检测结果：

```bash
node scripts/visualize.mjs photo.jpg '<detection-json>' output.jpg
```

**支持**：
- 带置信度分数的边框
- 类别标签
- 用于跟踪可视化的跟踪 ID
- 叠加层（ROI 区域、绊线线条）
- 文本注释

### ROI/绊线输入

用于区域和障碍的交互式输入：

1. 生成网格参考图像：
   ```bash
   node scripts/show-grid.mjs photo.jpg
   ```

2. 使用网格参考指定坐标：
   ```
   ROI: B1, E1, E3, B3
   Tripwire: A2 → G2 (direction: Forward)
   ```

3. 网格坐标自动转换为像素坐标

详见 [grid-guide.md](./grid-guide.md)。

## 视频帧提取

用于视频帧提取和多帧分析：

```json
{
  "imageData": "base64-frame-data",
  "sourceId": "video_abc123",        // 每个视频源唯一
  "imageId": "frame_001",             // 每帧唯一
  "timestamp": 1705056000000          // 帧时间戳，单位毫秒
}
```

**sourceId 计算**:
```
sourceId = MD5(视频文件的前 64KB) → 16 字符十六进制字符串
```

**timestamp 计算**:
```
timestamp = 帧索引 * 1000 / 帧率
```

详见 [video-guide.md](./video-guide.md)。

## 类型转换

### 输入转换

当将文件作为 `Image` 类型传递时：

```bash
# 文件路径自动转换为 base64
echo '{"input0":{"image":"photo.jpg"}}' | node invoke.mjs ep-detect
```

### 输出解析

检测结果会自动解析：

```javascript
// 原始输出
{ "detections": "[{\"bbox\": [...]}]" }

// 解析后的输出
{ "detections": [{ "bbox": [...] }] }  // JSON 数组，可以直接使用
```

## 最佳实践

1. **始终验证边框** - 确保坐标在图像边界内
2. **使用 track_id 以保持连续性** - 跟踪帧间的对象以获得更好的结果
3. **有效组合类型** - 使用 ROI 限制检测区域
4. **时间戳精度** - 为视频分析维持一致的时间戳计算
5. **sourceId 一致性** - 为来自同一源的所有帧保持 sourceId 常数

## 故障排除

**"无效的检测"**
- 检查边框格式：[x, y, width, height]
- 验证坐标为非负数
- 确保框在图像边界内

**"缺少关键点"**
- 并非所有技能都支持关键点
- 检查技能文档以了解支持的输出

**"ROI 未被识别"**
- 验证多边形是否闭合（第一个点 ≠ 最后一个点）
- 确保至少有 3 个点
- 检查点的顺序是否正确（顺时针或逆时针）

**"sourceId 不匹配"**
- 如果视频文件改变，重新计算 sourceId
- 对来自同一源的所有帧使用相同的 sourceId
