# 基于网格的 ROI / 绊线输入指南

## 概述

在命令行环境中手动指定 ROI 区域或绊线的确切像素坐标既繁琐又容易出错。基于网格的输入系统让你可以使用易于理解的网格坐标来代替。

## 工作原理

### 1. 生成网格参考图像

```bash
node scripts/show-grid.mjs photo.jpg [output-path] [--cols N] [--rows N]
```

这会在你的图像上创建带标签的网格叠加层：

```
       A     B     C     D     E     F     G
   0   ·─────·─────·─────·─────·─────·─────·
       │     │     │     │     │     │     │
   1   ·─────·─────·─────·─────·─────·─────·
       │     │     │     │     │     │     │
   2   ·─────·─────·─────·─────·─────·─────·
       │     │     │     │     │     │     │
   3   ·─────·─────·─────·─────·─────·─────·
       │     │     │     │     │     │     │
   4   ·─────·─────·─────·─────·─────·─────·
```

**输出**：
- `photo_grid.png` - 网格参考图像
- `photo_grid_metadata.json` - 坐标映射数据

### 2. 查看并识别坐标

查看网格图像并识别 ROI 或绊线的坐标：

- **列**：A、B、C、D、...（从左到右）
- **行**：0、1、2、3、...（从上到下）
- **交点**：网格线交叉的位置（用点标记）

### 3. 使用网格坐标指定

告诉系统网格坐标：

```
用户："在 B1、E1、E3、B3 创建检测区域"
```

系统自动转换为像素坐标：

```
B1 = (列B索引 × 网格宽度, 行1索引 × 网格高度)
E1 = (列E索引 × 网格宽度, 行1索引 × 网格高度)
E3 = (列E索引 × 网格宽度, 行3索引 × 网格高度)
B3 = (列B索引 × 网格宽度, 行3索引 × 网格高度)
```

## 使用示例

### 示例 1：定义检测区域（ROI）

```bash
# 生成网格
$ node scripts/show-grid.mjs office.jpg

# 查看网格图像以识别坐标，然后：
用户："我想要一个办公桌区域的检测区域：B2、G2、G5、B5"

转换为 ROI：
{
  "kind": "ROI",
  "points": [col_B, row_2, col_G, row_2, col_G, row_5, col_B, row_5]
}

# 使用 ROI 调用技能
$ echo '{"input0":{"image":"office.jpg","roi":"[...]"}}' | \
  node invoke.mjs ep-public-2403um2p
```

### 示例 2：定义穿越线（绊线）

```bash
# 生成网格
$ node scripts/show-grid.mjs hallway.jpg

# 查看网格图像，然后：
用户："在走廊中创建一条从 A3 到 H3 的绊线，检测从左到右的穿越"

转换为绊线：
{
  "kind": "TripWire",
  "points": [col_A, row_3, col_H, row_3],
  "direction": "Forward"
}

# 使用绊线调用技能
$ echo '{"input0":{"image":"hallway.jpg","tripwire":"[...]"}}' | \
  node invoke.mjs ep-public-ywbjb7tm
```

### 示例 3：多个 ROI

```bash
用户："我想要 3 个检测区域：入口（A1-C3）、中心（D1-F3）、出口（G1-H3）"

转换为三个 ROI 对象并作为 Array<ROI> 传递：
[
  {
    "kind": "ROI",
    "points": [col_A, row_1, col_C, row_1, col_C, row_3, col_A, row_3],
    "order": 0
  },
  {
    "kind": "ROI",
    "points": [col_D, row_1, col_F, row_1, col_F, row_3, col_D, row_3],
    "order": 1
  },
  {
    "kind": "ROI",
    "points": [col_G, row_1, col_H, row_1, col_H, row_3, col_G, row_3],
    "order": 2
  }
]
```

## 网格算法

网格大小会自动计算：

- **目标**：约 30-42 个交点，大致为方形单元
- **横向图像**（1920×1080）：7 列 × 4 行
- **纵向图像**（1080×1920）：4 列 × 7 行
- **方形图像**（800×800）：5 列 × 5 行

**手动覆盖**：
```bash
node scripts/show-grid.mjs photo.jpg --cols 10 --rows 6
```

## 命令参考

### 生成网格

```bash
node scripts/show-grid.mjs <input-image> [output-path] [--cols N] [--rows N]
```

**参数**：
- `<input-image>` - 输入图像文件路径
- `[output-path]` - 可选输出图像路径（默认：`<input>_grid.png`）
- `--cols N` - 覆盖列数
- `--rows N` - 覆盖行数

**输出**：
- 网格图像：`<output>.png`
- 元数据 JSON：`<output>_metadata.json`

### 使用网格坐标

在指定坐标时：

**有效格式**：
- 单个点：`A1`
- 序列：`A1、E1、E3、A3`（用于 ROI）
- 线：`A2 → G2`（用于绊线，显示方向）

**网格参考格式**：
- 列：A-Z，然后是 AA-AZ 等
- 行：0-9，然后是 10-99 等

## 可视化

### 查看网格图像

生成网格后，系统应该显示网格图像以便你可以直观地识别坐标。

### 调用前验证

在用坐标调用技能之前：

```bash
# 在原始图像上可视化选定的 ROI/绊线
node scripts/visualize.mjs office.jpg '<roi-or-tripwire-json>' preview.jpg
```

这可帮助你在处理前验证坐标是否正确。

## 提示和技巧

1. **从简单开始**：在使用复杂多边形前先从简单的矩形 ROI 开始
2. **使用均匀网格**：5×5 或 6×6 网格最容易参考
3. **记录你的区域**：为每个 ROI 指定有意义的名称（例如"入口"、"收银台"）
4. **重用坐标**：保存类似摄像机角度的坐标集
5. **先测试**：在处理前始终用 `visualize.mjs` 预览

## 故障排除

**"网格图像过于拥挤"**
- 降低网格密度：`--cols 4 --rows 4`
- 如果可能，增大图像大小

**"看不清网格线"**
- 网格使用半透明白色线条（50% 不透明度）
- 放大网格图像以获得更好的可见性

**"坐标似乎不对"**
- 验证列/行顺序（列 A-Z 从左到右，行 0-N 从上到下）
- 检查第一个点和最后一个点是否不同（多边形必须闭合）
- 确保点的顺序一致（全部顺时针或全部逆时针）

**"网格不适合图像"**
- 非常宽或非常高的图像可能有不均匀的单元格
- 使用 `--cols` 和 `--rows` 强制指定特定的网格尺寸

## 参考

- [类型定义](./types-guide.md) - ROI 和绊线类型规范
- [SKILL.md](./SKILL.md) - 主技能指南
