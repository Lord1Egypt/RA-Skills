# draw.io XML 格式参考

## 标准文件结构

```xml
<mxfile host="app.diagrams.net" modified="..." agent="..." version="...">
  <diagram name="..." id="...">
    <mxGraphModel dx="..." dy="..." grid="1" guides="1"...>
      <root>
        <mxCell id="0"/>                                      <!-- root -->
        <mxCell id="1" parent="0"/>                           <!-- page -->
        <!-- vertices and edges below -->
      </root>
    </mxGraphModel>
  </diagram>
</mxfile>
```

## ID 分配规则

| ID | 用途 |
|----|------|
| 0 | Root（固定） |
| 1 | Page（固定） |
| 10+ | Vertex 节点 |
| 20+ | Edge 边 |

## 节点（mxCell + mxGeometry）

### 形状类型对应 style 关键词

| 节点 type | draw.io style |
|-----------|--------------|
| start / end | `ellipse` |
| process | `rounded=1` |
| decision | `rhombus` |
| document | `shape=document` |
| data | `shape=parallelogram` |

### 示例：处理节点

```xml
<mxCell id="10" value="处理步骤" style="rounded=1;whiteSpace=wrap;html=1;fillColor=none;strokeColor=#000000;fontSize=12;" vertex="1" parent="1">
  <mxGeometry x="200" y="120" width="160" height="50" as="geometry"/>
</mxCell>
```

### 示例：判断节点（菱形）

```xml
<mxCell id="11" value="判断条件？" style="rhombus;whiteSpace=wrap;html=1;fillColor=none;strokeColor=#000000;fontSize=12;" vertex="1" parent="1">
  <mxGeometry x="180" y="200" width="190" height="70" as="geometry"/>
</mxCell>
```

### 示例：开始/结束节点

```xml
<mxCell id="12" value="开始" style="ellipse;whiteSpace=wrap;html=1;fillColor=none;strokeColor=#000000;fontSize=12;fontStyle=1;" vertex="1" parent="1">
  <mxGeometry x="200" y="40" width="120" height="50" as="geometry"/>
</mxCell>
```

## 边（连接线）

### 基本样式

```xml
<mxCell id="20" style="endArrow=classic;html=1;strokeColor=#000000;strokeWidth=1;" edge="1" parent="1" source="10" target="11">
  <mxGeometry relative="1" as="geometry"/>
</mxCell>
```

### 带标签的边

```xml
<mxCell id="21" value="是" style="endArrow=classic;html=1;strokeColor=#000000;strokeWidth=1;" edge="1" parent="1" source="11" target="13">
  <mxGeometry relative="1" as="geometry">
    <mxPoint as="offset"/>
  </mxGeometry>
</mxCell>
```

### 显式 waypoints（强制路由）

```xml
<mxCell id="22" value="否" style="endArrow=classic;html=1;strokeColor=#000000;strokeWidth=1;exitX=1;exitY=0.5;exitDx=0;exitDy=0;entryX=0;entryY=0.5;entryDx=0;entryDy=0;" edge="1" parent="1" source="11" target="14">
  <mxGeometry relative="1" as="geometry">
    <Array as="points">
      <mxPoint x="500" y="235"/>
      <mxPoint x="500" y="320"/>
      <mxPoint x="560" y="320"/>
    </Array>
  </mxGeometry>
</mxCell>
```

## 关键属性说明

| 属性 | 说明 |
|------|------|
| `vertex="1"` | 标识这是一个节点 |
| `edge="1"` | 标识这是一条边 |
| `parent="1"` | 所属页面（固定为1） |
| `source="X"` | 边的起点节点ID |
| `target="X"` | 边的终点节点ID |
| `exitX/exitY` | 出口方向（0-1比例） |
| `entryX/entryY` | 入口方向 |
| `as="points"` | 中间路由点（waypoints） |
| `relative="1"` | 坐标是否相对于节点 |

## 常用 exitX/exitY 组合

| 方向 | exitX | exitY |
|------|-------|-------|
| 右 | 1 | 0.5 |
| 下 | 0.5 | 1 |
| 左 | 0 | 0.5 |
| 上 | 0.5 | 0 |

## 样式速查

| 效果 | style 片段 |
|------|-----------|
| 圆角矩形 | `rounded=1` |
| 菱形 | `rhombus` |
| 椭圆 | `ellipse` |
| 文档形状 | `shape=document` |
| 圆柱形 | `shape=cylinder` |
| 黑色边框 | `strokeColor=#000000` |
| 无填充 | `fillColor=none` |
| 斜体文字 | `fontStyle=1` |
| 粗体文字 | `fontStyle=2` |
| 单向箭头 | `endArrow=classic` |
| 虚线 | `dashed=1` |
