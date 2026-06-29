# 坐标系与布局规则

## 坐标系规则

- 画布坐标：左上角(0,0)，X向右增大，Y向下增大
- **容器子节点坐标是相对于容器的**：parent_id指向容器时，子节点x/y是相对于容器左上角的偏移
- 页面默认：1169x827 (A4横向)
- 建议起始坐标：x>=40, y>=40

## 布局精度规则

### 思维导图 (create_mindmap)

**布局策略**：
- 中心节点在画布中央，宽度根据文本自适应
- 分支节点均匀分布在中心周围（半径220）
- 子节点排列方向与分支方向垂直：
  - 上下分支 → 子节点水平排列
  - 左右分支 → 子节点垂直排列
- 所有节点宽度根据文本自适应（中文字符1.8倍宽度）
- 子节点间距最小30px，自动调整避免重叠
- 连线使用正交路由（orthogonalEdgeStyle）

**精确参数**：
```
中心节点: 字体16px, 高度60, 内边距30px
分支节点: 字体13px, 高度50, 内边距24px, 半径220
子节点:   字体11px, 高度40, 内边距20px, 间距30px
```

### 架构图 (create_architecture)

**布局策略**：
- 画布宽度1100，左右边距40
- 容器宽度 = 画布宽 - 2*边距 = 1020
- 容器header高度28px（swimlane startSize）
- 容器内边距：左右20px，上下12px
- 子节点高度50px，水平间距16px
- 子节点宽度按可用空间均匀分配
- 层间距30px
- 子节点使用相对坐标（parent_id指向容器）

**精确参数**：
```
CANVAS_W = 1100, MARGIN_X = 40, MARGIN_Y = 40
CONTAINER_W = 1020
CONTAINER_HEADER_H = 28
CONTAINER_PAD_X = 20, CONTAINER_PAD_Y = 12, CONTAINER_BOTTOM_PAD = 12
COMP_MIN_W = 100, COMP_H = 50, COMP_GAP_X = 16
LAYER_GAP = 30
```

## 连线连接点规则

### 连接点定义

- `0` = 顶部 (Top)
- `1` = 右侧 (Right)
- `2` = 底部 (Bottom)
- `3` = 左侧 (Left)

### 思维导图连线

**中心→分支**：

| 分支方向 | sourcePort (中心) | targetPort (分支) |
|----------|-------------------|-------------------|
| 上       | 0 (顶部输出)      | 2 (底部输入)      |
| 下       | 2 (底部输出)      | 0 (顶部输入)      |
| 左       | 3 (左侧输出)      | 1 (右侧输入)      |
| 右       | 1 (右侧输出)      | 3 (左侧输入)      |

**分支→子节点**：

| 子节点位置 | sourcePort (分支) | targetPort (子节点) |
|------------|-------------------|---------------------|
| 上方       | 0 (顶部输出)      | 2 (底部输入)        |
| 下方       | 2 (底部输出)      | 0 (顶部输入)        |
| 左侧       | 3 (左侧输出)      | 1 (右侧输入)        |
| 右侧       | 1 (右侧输出)      | 3 (左侧输入)        |

### XML输出（关键）

draw.io 通过 **style 字符串中的 `exitX`/`exitY`/`entryX`/`entryY`** 控制连线出入点，**不是** mxCell 的 sourcePort/targetPort 属性。

正确做法（在 `build_xml()` 中将端口信息写入 edge style）：
```
exitX=0.5;exitY=0;exitDx=0;exitDy=0;entryX=0.5;entryY=1;entryDx=0;entryDy=0;
```

错误做法（draw.io 不认这个属性，直接忽略）：
```xml
<mxCell ... source="node1" target="node2" sourcePort="0" targetPort="2">
```

### 连线路由样式

| 图表类型 | 推荐路由 | style |
|----------|----------|-------|
| 思维导图 | 直线 | `edgeStyle=none;html=1;` |
| 流程图 | 正交折线 | `edgeStyle=orthogonalEdgeStyle;...` |
| 架构图 | 正交虚线 | `edgeStyle=orthogonalEdgeStyle;...dashed=1;...` |
| 时序图 | 直线 | `edgeStyle=none;html=1;` |
