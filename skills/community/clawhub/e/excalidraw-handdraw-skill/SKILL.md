---
name: excalidraw-handdraw
description: 根据提示词生成手绘风格图表的 skill。用于：(1) 创建架构图、流程图、ER 图等 Excalidraw 手绘风格图表 (2) 通过 Docker 本地运行 canvas 服务器 (3) 生成 PNG/SVG 图片 (4) 保存图片到指定目录 (5) 将图表插入或替换到文件指定位置 (6) 支持中文手写字体。触发词：画图、创建图表、生成图表、手绘风格、架构图、流程图、Excalidraw、保存图表到文件、插入图表。
---

# Excalidraw Handdraw Skill

## Step 0: 检查 Canvas 服务器状态

首先检查 Docker canvas 是否已运行：

```bash
docker ps | grep mcp_excalidraw-canvas
```

如果未运行，使用脚本启动：
```bash
./scripts/start-canvas.sh
```

确认服务可用：
```bash
curl -s http://localhost:3000/health
```

## Step 1: 理解用户需求

用户描述想要创建的图表类型，例如：
- "画一个微服务架构图"
- "创建一个用户登录流程图"
- "生成一个数据库 ER 图"
- "画一个网络拓扑图"

分析需求：
- 确定图表类型（架构图、流程图、ER 图等）
- 确定需要的元素（矩形、箭头、文字等）
- 确定是否需要中文标签

## Step 2: 创建图表元素

**⚠️ 重要：REST API 格式说明**
- **文字标签**：必须使用 `{"label": {"text": "文字"}}` 格式（不是 `text`）
- **箭头连接**：必须使用 `{"start": {"id": "id1"}, "end": {"id": "id2"}}` 格式（不是 `startElementId`）
- **箭头坐标**：箭头元素必须有 `x` 和 `y` 坐标（可以为 0）

**API 调用方式：**
- 使用 `POST /api/elements` 逐个创建元素（不支持批量创建）
- 每个元素必须包含完整的属性：id, type, x, y, width, height, label

**Playwright 操作示例：**
```javascript
async () => {
  const elements = [
    { id: "lb", type: "rectangle", x: 300, y: 50, width: 180, height: 60, label: { text: "负载均衡器" } },
    { id: "svc-a", type: "rectangle", x: 100, y: 200, width: 160, height: 60, label: { text: "服务 A" } },
    { id: "arrow1", type: "arrow", x: 0, y: 0, start: { id: "lb" }, end: { id: "svc-a" } }
  ];

  for (const el of elements) {
    await fetch('/api/elements', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(el)
    });
  }
  return { success: true };
}
```

参考坐标系统：
- 原点 (0,0) 在左上角
- x 向右增加，y 向下增加
- 元素宽度：`max(160, labelCharCount * 9)`
- 元素高度：单行 60px，双行 80px

**⚠️ 布局最佳实践（避免重叠和裁剪）：**
- 垂直间距：**140-180px**（不要小于 140px）
- 水平间距：**80-100px**（不要小于 80px）
- **顶部边距：startY 至少 100px**（避免顶部元素被裁剪）
- **底部边距：最后一个元素 Y + height 应小于 600px**
- 留白原则：宁可间距大，也不要太小
- 多行文字时：height = 行数 × 30px + 15px

## Step 3: 验证图表质量

创建后获取截图验证：
- 使用 `get_canvas_screenshot` 获取图片
- 检查文字是否截断
- 检查元素是否重叠
- 检查箭头是否穿过无关元素

发现问题时修复：
- 文字截断 → 增加元素宽度/高度
- 元素重叠 → 调整坐标位置
- 箭头穿过元素 → 使用曲线箭头或调整布局

## Step 4: 导出纯净图片（关键步骤）

**⚠️ 重要：必须使用 Canvas API 导出纯净图片，不要使用页面截图！**

使用 Playwright 执行 JavaScript，直接从 canvas 元素导出：

```javascript
async () => {
  const canvas = document.querySelector('canvas');
  if (!canvas) return { success: false };

  // 获取画布数据并下载
  const dataUrl = canvas.toDataURL('image/png');
  const link = document.createElement('a');
  link.download = 'diagram.png';
  link.href = dataUrl;
  link.click();

  return { success: true, downloaded: true };
}
```

**Playwright 操作步骤：**
1. 使用 `browser_evaluate` 执行上述 JavaScript
2. 图片会下载到 `.playwright-mcp/` 目录
3. 使用 `mv` 命令移动到目标位置

**示例：**
```
browser_evaluate → 执行导出 JS
→ 下载到 .playwright-mcp/diagram.png
→ mv .playwright-mcp/diagram.png ./output/diagram.png
```

**❌ 错误方式：**
- 使用 `browser_take_screenshot` - 会包含网页工具栏和侧边栏
- 使用 `browser_snapshot` + 截图 - 同样包含 UI 元素

**✅ 正确方式：**
- 使用 `browser_evaluate` 执行 canvas.toDataURL() 导出
- 这样得到的图片是纯净的，只有画布内容，白色背景

## Step 5: 保存到指定位置

图片下载后保存在 `.playwright-mcp/` 目录，使用 mv 命令移动到目标位置：

```bash
mv .playwright-mcp/diagram.png ./docs/diagrams/architecture.png
```

## Step 6: 插入到 Markdown 文件

将图片插入到 Markdown 文件：

```markdown
![公司架构图](./docs/diagrams/architecture.png)
```

## 常用命令参考

| 操作 | 方法 |
|------|------|
| 启动 Canvas | `docker ps \| grep mcp_excalidraw-canvas` 确认运行 |
| 停止 Canvas | `docker stop mcp_excalidraw-canvas` |
| 创建元素 | `browser_evaluate` 执行 `fetch('/api/elements', {...})` |
| 清除画布 | 点击页面 "Clear Canvas" 按钮 |
| 同步画布 | 点击页面 "Sync to Backend" 按钮 |
| 导出纯净图片 | `browser_evaluate` 执行 `canvas.toDataURL()` + 下载 |
| 移动图片 | `mv .playwright-mcp/diagram.png ./output/diagram.png` |

## 常用图表模板

### 组织架构图模板

```javascript
async () => {
  const elements = [];

  // 布局参数
  const config = {
    startY: 50,           // 起始 Y 坐标
    levelGap: 180,        // 层级垂直间距
    nodeWidth: 140,       // 节点宽度
    nodeHeight: 60,       // 节点高度
    hGap: 100             // 水平间距
  };

  // 第一层：CEO
  elements.push({
    id: "ceo", type: "rectangle",
    x: 300, y: config.startY,
    width: 160, height: config.nodeHeight,
    label: { text: "CEO\n总经理" }
  });

  // 第二层：高管层（水平排列）
  const level2 = ["CTO\n技术总监", "CFO\n财务总监", "COO\n运营总监", "CMO\n市场总监"];
  const level2Y = config.startY + config.levelGap;

  level2.forEach((label, i) => {
    elements.push({
      id: `l2-${i}`, type: "rectangle",
      x: 50 + i * (config.nodeWidth + config.hGap),
      y: level2Y,
      width: config.nodeWidth, height: config.nodeHeight,
      label: { text: label }
    });
    // 连接到 CEO
    elements.push({
      id: `arr-ceo-${i}`, type: "arrow",
      x: 0, y: 0,
      start: { id: "ceo" }, end: { id: `l2-${i}` }
    });
  });

  // 创建所有元素
  for (const el of elements) {
    await fetch('/api/elements', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(el)
    });
  }
  return { success: true };
}
```

### 流程图模板（水平布局）

```javascript
async () => {
  const steps = ["开始", "步骤1", "步骤2", "结束"];
  const config = { startX: 50, y: 100, boxWidth: 120, boxHeight: 50, gap: 80 };

  const elements = [];

  steps.forEach((label, i) => {
    elements.push({
      id: `step-${i}`, type: "rectangle",
      x: config.startX + i * (config.boxWidth + config.gap),
      y: config.y,
      width: config.boxWidth, height: config.boxHeight,
      label: { text: label }
    });

    // 连接箭头（从上一个到当前）
    if (i > 0) {
      elements.push({
        id: `arr-${i}`, type: "arrow",
        x: 0, y: 0,
        start: { id: `step-${i-1}` }, end: { id: `step-${i}` }
      });
    }
  });

  for (const el of elements) {
    await fetch('/api/elements', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(el)
    });
  }
  return { success: true };
}
```

### 垂直流程图模板

```javascript
async () => {
  const steps = ["输入", "处理", "输出"];
  const config = { x: 300, startY: 50, boxWidth: 160, boxHeight: 60, vGap: 150 };

  const elements = [];

  steps.forEach((label, i) => {
    elements.push({
      id: `node-${i}`, type: "rectangle",
      x: config.x,
      y: config.startY + i * (config.boxHeight + config.vGap),
      width: config.boxWidth, height: config.boxHeight,
      label: { text: label }
    });

    if (i > 0) {
      elements.push({
        id: `arr-${i}`, type: "arrow",
        x: 0, y: 0,
        start: { id: `node-${i-1}` }, end: { id: `node-${i}` }
      });
    }
  });

  for (const el of elements) {
    await fetch('/api/elements', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(el)
    });
  }
  return { success: true };
}
```

## 布局计算辅助函数

在编写 JavaScript 时，可使用以下辅助计算：

```javascript
// 水平居中计算
const centerX = (canvasWidth, elementWidth) => (canvasWidth - elementWidth) / 2;

// 多元素水平均匀分布
const distributeHorizontal = (count, elementWidth, totalWidth, startX) => {
  const totalGap = totalWidth - count * elementWidth;
  const gap = totalGap / (count + 1);
  return Array.from({length: count}, (_, i) => startX + gap + i * (elementWidth + gap));
};

// 计算元素所需宽度（根据文字）
const calcWidth = (text) => Math.max(120, text.length * 12);

// 计算元素所需高度（根据行数）
const calcHeight = (text) => {
  const lines = text.split('\n').length;
  return lines * 30 + 20;
};
```

## 注意事项

1. **Docker 必须运行**：Canvas 服务器通过 Docker 运行，确保 `mcp_excalidraw-canvas` 容器在运行
2. **中文支持**：Excalidraw 原生支持中文，无需额外配置
3. **导出纯净图片**：必须使用 `canvas.toDataURL()` 方式导出，不要用页面截图
4. **图片下载位置**：Playwright 下载的图片在 `.playwright-mcp/` 目录
5. **间距宁大勿小**：使用较大间距（150px+）避免重叠，宁可图表松散也不要拥挤
6. **箭头用元素引用**：使用 `start: {id}, end: {id}` 格式，让 Excalidraw 自动计算路径

## 故障排除

- **Canvas 无法连接**：检查 Docker 容器是否运行 `docker ps | grep mcp_excalidraw-canvas`
- **导出图片有 UI 元素**：确保使用 `canvas.toDataURL()` 而不是 `browser_take_screenshot`
- **元素创建失败**：确保每个元素包含完整属性（id, type, x, y, width, height）
- **元素重叠**：增大间距，垂直间距至少 150px，水平间距至少 80px
- **箭头位置错误**：使用 `start: {id}, end: {id}` 元素引用格式，而非手动 points
- **文字截断**：增加元素宽度，使用 `width = text.length * 12` 估算

## 常见错误及修复

| 问题 | 原因 | 解决方案 |
|------|------|----------|
| 矩形重叠 | 间距太小 | 垂直间距改为 150px+，水平 80px+ |
| 箭头乱连 | points 坐标错误 | 改用 `start: {id}, end: {id}` 格式 |
| 文字不全 | width/height 不足 | 根据字数行数计算足够尺寸 |
| 图表太密 | 整体布局紧凑 | 放大间距，宁可松散不要拥挤 |
| 连线穿过元素 | 布局未考虑路径 | 调整元素位置或使用曲线箭头 |
