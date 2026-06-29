# Archify 渲染器指南

## 快速开始

```bash
cd /root/.openclaw/workspace/skills/archify
node renderers/<type>/render-<type>.mjs <input>.json <output>.html
```

## 5种 Diagram 类型

### 1. Architecture（架构图）— 模型结构、系统组成

**适用场景**：模型整体架构、资源连接、网络拓扑
**渲染命令**：`node renderers/architecture/render-architecture.mjs input.json output.html`

**输入 JSON 示例**：
```json
{
  "schema_version": 1,
  "diagram_type": "architecture",
  "meta": { "title": "YOLO-MECD 模型架构", "subtitle": "柑橘检测网络", "output": "yolo-mecd.html" },
  "components": [
    { "id": "input", "type": "frontend", "label": "Input", "sublabel": "1200×1200 柑橘图像", "pos": [40, 200] },
    { "id": "backbone", "type": "backend", "label": "Backbone", "sublabel": "CSPDarknet + EMA", "pos": [280, 200] },
    { "id": "neck", "type": "backend", "label": "Neck", "sublabel": "CSPPC + PAFPN", "pos": [460, 200] },
    { "id": "head", "type": "backend", "label": "Detection Head", "sublabel": "YOLOv11 Head", "pos": [640, 200] },
    { "id": "output", "type": "external", "label": "Output", "sublabel": "检测框 + 类别", "pos": [820, 200] }
  ],
  "boundaries": [
    { "kind": "region", "label": "YOLO-MECD", "wraps": ["backbone", "neck", "head"] }
  ],
  "connections": [
    { "from": "input", "to": "backbone", "label": "图像", "variant": "emphasis" },
    { "from": "backbone", "to": "neck", "label": "特征", "variant": "emphasis" },
    { "from": "neck", "to": "head", "label": "特征", "variant": "emphasis" },
    { "from": "head", "to": "output", "label": "检测结果" }
  ],
  "cards": []
}
```

**组件类型对照**：
| type | 含义 | 颜色 |
|------|------|------|
| `frontend` | 输入/客户端 | 青蓝 |
| `backend` | 计算/服务 | 蓝灰 |
| `database` | 存储/缓存 | 绿灰 |
| `cloud` | 云服务 | 蓝紫 |
| `security` | 安全组件 | 红灰 |
| `messagebus` | 消息队列 | 橙灰 |
| `external` | 外部/输出 | 灰 |

### 2. Workflow（流程图）— 训练/检测流程

**适用场景**：训练Pipeline、检测步骤、决策分支
**渲染命令**：`node renderers/workflow/render-workflow.mjs input.json output.html`

**输入 JSON 示例**：
```json
{
  "schema_version": 1,
  "diagram_type": "workflow",
  "meta": { "title": "YOLO-MECD 训练流程", "subtitle": "柑橘检测模型训练", "output": "training-workflow.html" },
  "lanes": [
    { "id": "data", "label": "数据处理" },
    { "id": "model", "label": "模型训练" },
    { "id": "eval", "label": "评估" }
  ],
  "nodes": [
    { "id": "collect", "lane": "data", "col": 0, "type": "frontend", "label": "收集图像", "sublabel": "1200张柑橘" },
    { "id": "annotate", "lane": "data", "col": 1, "type": "frontend", "label": "数据标注", "sublabel": "Bounding Box" },
    { "id": "augment", "lane": "data", "col": 2, "type": "frontend", "label": "数据增强", "sublabel": "翻转/裁剪" },
    { "id": "train", "lane": "model", "col": 1, "type": "backend", "label": "模型训练", "sublabel": "YOLOv11s + EMA", "tag": "blocking" },
    { "id": "eval", "lane": "eval", "col": 2, "type": "backend", "label": "评估测试", "sublabel": "mAP@50" }
  ],
  "edges": [
    { "from": "collect", "to": "annotate", "label": "采集", "variant": "emphasis", "fromSide": "bottom", "toSide": "top", "route": "drop" },
    { "from": "annotate", "to": "augment", "fromSide": "bottom", "toSide": "top", "route": "drop" },
    { "from": "augment", "to": "train", "fromSide": "bottom", "toSide": "top", "route": "drop" },
    { "from": "train", "to": "eval", "label": "验证", "variant": "emphasis", "fromSide": "bottom", "toSide": "top", "route": "drop" }
  ],
  "cards": []
}
```

### 3. Dataflow（数据流图）— 数据处理管道

**适用场景**：多阶段数据处理、ETL流水线、特征工程
**渲染命令**：`node renderers/dataflow/render-dataflow.mjs input.json output.html`

### 4. Lifecycle（状态图）— 训练阶段/检测状态

**适用场景**：模型训练阶段、检测状态机、生命周期
**渲染命令**：`node renderers/lifecycle/render-lifecycle.mjs input.json output.html`

### 5. Sequence（时序图）— 多方交互

**适用场景**：API调用链、多模块交互、推理时序
**渲染命令**：`node renderers/sequence/render-sequence.mjs input.json output.html`

## 论文结构图生成指南

### YOLO系列论文 → Architecture
- Backbone / Neck / Head 三段式架构
- 特征金字塔连接

### 训练流程论文 → Workflow
- 数据输入 → 预处理 → 模型前向 → 损失计算 → 反向传播

### 数据处理论文 → Dataflow
- 原始数据 → 清洗 → 增强 → 特征提取 → 模型输入

### 状态机相关论文 → Lifecycle
- 初始化 → 训练中 → 验证 → 终端状态

## 常见错误处理

| 错误信息 | 解决方法 |
|---------|---------|
| `node: command not found` | 使用完整路径：`/usr/bin/node` |
| 布局重叠 | 调整 `col` 值错开列，或增大 `pos` 间距 |
| 标签超出边界 | 减小标签文字长度，或调整 `labelDy` 偏移 |

## 输出文件

生成的 `.html` 文件：
- 自带暗色/亮色主题切换
- 可导出 PNG / JPEG / WebP / SVG
- 直接在浏览器打开即可交互