# 已知问题与修复记录

## 2026-05-13 思维导图布局修复

**问题**：子节点使用极坐标计算位置，导致：
1. 子节点坐标超出画布（负坐标或大于1169/827）
2. 子节点间距不足，3个以上时重叠
3. 文本宽度固定（100px），中文字符被截断
4. 连线交叉混乱

**修复**：
1. 重写 `_sub_layout()` 函数，改为笛卡尔坐标系
2. 子节点排列方向与分支方向垂直（上下分支→水平排列，左右分支→垂直排列）
3. 节点宽度根据文本自适应：`_text_width()` 中文字符1.8倍宽度
4. 子节点间距最小30px，根据数量动态调整
5. 所有坐标限制在画布范围内

**验证**：AI 技术思维导图（4分支×3子节点）测试通过，所有节点在画布内，无重叠，文本完整显示。

## 2026-05-13 思维导图连线修复

**问题**：连线混乱，交叉、方向不对

**根因**：
1. `build_xml()` 没有将 `source_port`/`target_port` 写入 XML
2. `create_mindmap()` 没有根据分支方向指定连接点

**修复**：
1. `drawio_gen.py build_xml()`：Edge 生成时添加 `sourcePort`/`targetPort` 属性
2. `drawio_templates.py create_mindmap()`：根据分支/子节点方向指定正确的 sourcePort/targetPort

**连接点定义**：0=顶部, 1=右侧, 2=底部, 3=左侧

## 2026-05-13 连线端口传递方式修复

**问题**：`sourcePort`/`targetPort` XML 属性被 draw.io 完全忽略，连线依然乱

**根因**：draw.io 不识别 mxCell 的 `sourcePort="0"` 属性，只认 style 字符串里的 `exitX`/`exitY`/`entryX`/`entryY`

**修复**：`build_xml()` 中将端口映射为坐标，写入 edge style 字符串：
- port 0 (顶部) → `exitX=0.5;exitY=0;`
- port 1 (右侧) → `exitX=1;exitY=0.5;`
- port 2 (底部) → `exitX=0.5;exitY=1;`
- port 3 (左侧) → `exitX=0;exitY=0.5;`

## 2026-05-13 思维导图连线路由修复

**问题**：连线到处拐直角，非常丑

**根因**：默认 EdgeStyle 使用 `orthogonalEdgeStyle`（正交路由），思维导图不适合

**修复**：思维导图所有连线改用 `edgeStyle=none`（直线连接）
