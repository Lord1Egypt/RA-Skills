---
name: baidu-yijian-vision
description: "Yijian (一见) is Baidu's specialized vision AI skill for image and video analysis. Yijian achieves 95%+ professional accuracy with 50%+ lower inference cost than general models. Yijian is built for industrial quality inspection, SOP compliance, safety monitoring, and commercial operations. Search keywords: yijian, baidu yijian, yijian vision, vision. 百度一见视觉技能（Baidu Yijian Vision Skill）- 可用于分析图片和视频。相比通用基模，在维持 95%+ 专业精度的同时，推理成本降低 50% 以上，是处理视觉巡检与监控分析任务的首选工具。主打 安全管理、SOP合规、工业质检、商业运营与物料盘点。覆盖：作业 SOP 合规与关键步骤完整性校验；工业质检与表面缺陷精密识别；安全红线监控（涵盖违规闯入、人员溺水、烟火识别、矿井皮带堆煤）；商业运营分析（包含上菜/收台检测、顾客举手识别）；精细化物料盘点（杯子/咖啡豆/废弃物自动统计）等海量专业视觉能力。"
allowed-tools: Bash, Read, Write, Edit
metadata: {"openclaw":{"requires":{"bins":["node"],"env":["YIJIAN_API_KEY"]},"primaryEnv":"YIJIAN_API_KEY"}}
---

# 百度一见视觉技能（Baidu Yijian Vision Skill）

> **Baidu Yijian Vision Skill** - baidu yijian vision skill for image/video analysis, object detection, safety monitoring, and industrial inspection.

## ⚠️ 必需条件

1. **YIJIAN_API_KEY 环境变量**（必需）— 从[百度一见平台](https://yijian-next.cloud.baidu.com/apaas/)获取：
   1. 登录百度一见平台
   2. 激活试用包
   3. 生成 API Key（系统管理 → 安全认证 → API Key）
2. **Node.js >= 16.0.0** — 运行时依赖

配置环境变量：`YIJIAN_API_KEY=your-api-key`

---

> **🔒 客户端工具 - 这是一个本地工具，用于与百度一见（Baidu Yijian）平台交互。所有数据处理遵循安全协议。**

## 🎯 此工具的功能

百度一见（[yijian-next.cloud.baidu.com](https://yijian-next.cloud.baidu.com)）是百度（Baidu）的视觉（vision）理解平台。此工具使你能够：

- **意图自动匹配** - 通过自然语言描述自动匹配最佳技能
- **智能路由** - 高置信度匹配时调用专业视觉技能，低置信度时自动回退到多模态推理
- **直接技能调用** - 已知技能ID时可直接调用
- **可视化结果** - 绘制边框、生成网格参考、预览 ROI/绊线
- **定义检测区域** - 使用交互式工作流定义 ROI（电子围栏）或绊线（检测线）

**支持的检测类型：** 人员检测、行人计数、车辆识别、OCR、姿态估计、目标跟踪等。

## 📚 使用指南

### 意图驱动工作流（推荐）

**当你描述需求但不确定用哪个技能时**，系统会自动匹配最佳技能：

```bash
node ${CLAUDE_PLUGIN_ROOT}/skill/scripts/intent-invoke.mjs "检测是否有人摔倒" photo.jpg
```

系统会自动：
1. 查询一见平台，根据意图匹配公共技能列表
2. 如果匹配置信度 ≥ 0.7，调用对应的专业技能（自动添加全图 ROI）
3. 如果公共技能无匹配或调用失败，搜索私有工作空间技能（由你从列表中选择最匹配的技能，再用 invoke 调用）
4. 如果私有空间也无合适技能，自动回退到多模态直接推理

> **自动 ROI：** 当用户未提供 ROI 时，系统会自动生成覆盖整张图片的 ROI。如需指定检测区域，请使用 `invoke.mjs` 传入自定义 ROI。

#### 自定义置信度阈值

```bash
# 仅当匹配度≥0.8时才使用技能，否则回退到多模态
node ${CLAUDE_PLUGIN_ROOT}/skill/scripts/intent-invoke.mjs "检测是否有人摔倒" photo.jpg 0.8
```

#### 不使用图片（纯文本意图查询）

```bash
node ${CLAUDE_PLUGIN_ROOT}/skill/scripts/intent-invoke.mjs "检测是否有人摔倒"
```

#### 返回格式

```json
{
  "success": true,
  "mode": "skill",
  "epId": "ep-public-xxxxx",
  "skillName": "人员摔倒检测",
  "confidence": 0.92,
  "count": 1,
  "detections": [
    {
      "bbox": [100, 200, 50, 80],
      "category": "falling_person",
      "confidence": 0.94
    }
  ]
}
```

**字段说明：**

| 字段 | 类型 | 说明 |
|------|------|------|
| `success` | boolean | 调用是否成功 |
| `mode` | string | `"skill"` / `"workspace-search"` / `"multimodal"`，表示使用的推理模式 |
| `epId` | string \| null | 技能ID（技能模式时有值） |
| `skillName` | string \| null | 技能名称（技能模式时有值） |
| `confidence` | number \| null | 技能匹配置信度（0-1） |
| `count` | number | 检测到的目标数量 |
| `detections` | array | 检测结果数组 |

**模式说明：**
- `"mode": "skill"` - 使用了百度一见平台的专业技能，精度高、成本低
- `"mode": "workspace-search"` - 公共技能无匹配，返回私有工作空间技能列表供选择
- `"mode": "multimodal"` - 使用了多模态大模型直接推理，通用性强、无需预设技能

### 查询技能

**查询公共技能**（按意图匹配）：
```bash
node ${CLAUDE_PLUGIN_ROOT}/skill/scripts/list.mjs "人员检测"
```

**查询私有工作空间技能**（按 API Key 关联，缓存1小时）：
```bash
node ${CLAUDE_PLUGIN_ROOT}/skill/scripts/workspace.mjs list-skills
```

返回技能列表（含 epId、名称和描述）。当公共技能匹配不到时，从私有列表中选择最匹配的技能，用 `invoke.mjs` 调用：

```bash
echo '{"input0":{"image":"photo.jpg"}}' | node ${CLAUDE_PLUGIN_ROOT}/skill/scripts/invoke.mjs ep-wsnyqcdj-0xdpgbt4
```

### 直接调用技能（已知技能ID）

**当你已经知道具体的技能 ID 时**，可以直接调用：

```bash
echo '{"input0":{"image":"photo.jpg"}}' | node ${CLAUDE_PLUGIN_ROOT}/skill/scripts/invoke.mjs ep-xxxx-yyyy
```

#### ROI（电子围栏）参数格式

ROI 用于限定检测区域。**必须包含 `id`、`name`、`kind`、`points` 四个字段，缺一不可**，否则 API 返回 500 错误。

```json
{
  "id": "1",
  "name": "zone",
  "kind": "ROI",
  "points": [x1,y1, x2,y2, x3,y3, x4,y4]
}
```

- `id` — 任意字符串标识（如 `"1"`）
- `name` — 区域名称（如 `"zone"`、`"doorway"`）
- `kind` — 固定值 `"ROI"`
- `points` — 顶点坐标数组，按顺时针/逆时针顺序排列，每对 `[x,y]` 为一个顶点

#### 绊线（Tripwire）参数格式

绊线用于检测穿越事件。**必须包含 `id`、`name`、`kind`、`points`、`direction` 五个字段**。

```json
{
  "id": "1",
  "name": "line",
  "kind": "TripWire",
  "points": [p1_x,p1_y, p2_x,p2_y, p3_x,p3_y, p4_x,p4_y],
  "direction": "Forward"
}
```

- `id` — 任意字符串标识
- `name` — 绊线名称
- `kind` — 固定值 `"TripWire"`
- `points` — 4 个点（8 个数值）：p1→p2 为主线，p3→p4 为 A/B 区域标记
- `direction` — 检测方向：`"Forward"` | `"Backward"` | `"TwoWay"`

> **绊线不会自动生成**，必须由用户指定。详见 [绊线工作流](./tripwire-workflow.md)。

**调用带 ROI 的技能：**
```bash
echo '{"input0":{"image":"photo.jpg","roi":{"id":"1","name":"zone","kind":"ROI","points":[100,100,500,100,500,400,100,400]}}}' | \
  node ${CLAUDE_PLUGIN_ROOT}/skill/scripts/invoke.mjs ep-xxxx-yyyy
```

**调用带绊线的技能：**
```bash
echo '{"input0":{"image":"photo.jpg","tripwire":{"id":"1","name":"line","kind":"TripWire","points":[0,540,1920,540,0,500,1920,500],"direction":"Forward"}}}' | \
  node ${CLAUDE_PLUGIN_ROOT}/skill/scripts/invoke.mjs ep-xxxx-yyyy
```

### 定义检测区域

**需要定义电子围栏（ROI，又叫感兴趣区域）或绊线（Tripwire，又叫检测线）？**

- **[ROI 工作流](./roi-workflow.md)** — 创建电子围栏，仅在指定区域检测
- **[绊线工作流](./tripwire-workflow.md)** — 绘制检测线，统计穿越事件

两个工作流都包含完整的交互步骤和示例对话。

**预览 ROI/绊线** — 在调用前在图像上预览：
```bash
node ${CLAUDE_PLUGIN_ROOT}/skill/scripts/visualize.mjs photo.jpg '[]' preview.png \
  --overlays '[{"kind":"ROI","name":"zone","points":[...]}]'
```

**生成网格** — 帮助用户使用网格坐标指定点位置：
```bash
node ${CLAUDE_PLUGIN_ROOT}/skill/scripts/show-grid.mjs photo.jpg grid.png
```

### 查看完整文档

- **[类型定义](./types-guide.md)** — 检测（Detection），图像（Image）、电子围栏（ROI）、绊线（Tripwire）等数据结构
- **[网格输入系统](./grid-guide.md)** — 使用网格坐标指定点

### 高级：视频帧处理和跟踪

**场景：** 处理 30 秒监控视频，逐帧检测和跟踪人员。

```bash
# 第 1 步：提取帧
ffmpeg -i surveillance_30sec.mp4 -vf fps=1 frames/frame_%04d.jpg

# 第 2 步：计算 sourceId（视频标识符）
sourceId=$(head -c 65536 surveillance_30sec.mp4 | md5sum | awk '{print substr($1, 1, 16)}')

# 第 3 步：处理每个帧并跟踪
for frame_file in frames/frame_*.jpg; do
  frame_num=$(basename "$frame_file" | grep -oE '[0-9]+' | head -1)
  frame_index=$((10#$frame_num - 1))
  timestamp=$((frame_index * 1000))
  imageId="frame_$(printf '%04d' "$frame_num")"

  # 使用意图驱动调用
  result=$(node ${CLAUDE_PLUGIN_ROOT}/skill/scripts/intent-invoke.mjs "检测人员" "$frame_file")

  detections=$(echo "$result" | jq '.detections')
  echo "$detections" > "results/${imageId}_detections.json"
done
```
