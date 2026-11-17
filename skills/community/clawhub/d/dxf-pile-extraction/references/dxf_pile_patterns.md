# DXF桩基图常见模式

本文档记录岩土工程桩基施工图DXF中常见的实体组织模式，用于指导自动提取。

## 桩的几何表示

### 模式1：块内CIRCLE（最常见）

桩定义为匿名块引用，块内包含CIRCLE圆。圆心=桩心，半径=桩径/2。

```
INSERT (BASE-ZM图层)
  ├── 名称: A$C4AAF42E9 (匿名块)
  ├── 插入点: (X0, Y0, 0)
  ├── 缩放: 1.0
  └── 块定义内:
      ├── CIRCLE × N (桩心=圆心)
      └── 其他图形元素
```

提取方法：
```python
# 遍历块定义，找到含CIRCLE的块
for block in doc.blocks:
    circles = [e for e in block if e.dxftype() == 'CIRCLE']
    if circles:
        # 记录块名
# 遍历INSERT实体
for insert in msp.query('INSERT'):
    if insert.dxf.name == block_name:
        block = doc.blocks[block_name]
        for circle in block:
            if circle.dxftype() != 'CIRCLE':
                continue
            # 世界坐标 = 插入点 + 块内圆心 × 缩放
            wx = insert.dxf.insert.x + circle.dxf.center.x * insert.dxf.xscale
            wy = insert.dxf.insert.y + circle.dxf.center.y * insert.dxf.yscale
            wr = circle.dxf.radius * insert.dxf.xscale  # 桩径 = wr × 2
```

### 模式2：LWPOLYLINE直径符号线

桩表示为45°方向的2点LWPOLYLINE，长度=桩径×√2。

```
LWPOLYLINE (BASE-ZM-BH图层)
  ├── 顶点数: 2
  ├── 起点P1(X1,Y1) = 桩心（重要：P1是桩心不是线段中点）
  └── 终点P2(X2,Y2) = P1 + 桩径×√2 @45°
```

这种模式的关键教训：**起点P1才是桩心**，不能取线段中点。

验证方法：检查圆是否存在，若存在，圆心应与P1重合。

### 模式3：直接CIRCLE

桩直接表示为CIRCLE实体（不在块内）。圆心=桩心，半径=桩径/2。

## 编号方式

### 格式1：数字编号（如本次项目）
图层: `桩编号`，颜色=3（绿色）
内容: `Z1`, `Z2`, ..., `Z419`（MTEXT）
位置: 桩心附近（1~3m偏移）

### 格式2：桩型+标高
图层: `BASE-ZM-BH`
内容: `GZH01,H=-6.500`（TEXT）
解析: `GZH01`=桩型, `H=-6.500`=桩顶相对标高

常见桩型前缀：
- `GZH`: 灌注桩 (Guan Zhu Huang)
- `YZ`: 预制桩 (Yu Zhi)
- `PHC`: 预应力管桩

## 等高线

### 等高线图层
- `g_sDgxLayer`: 中风化/微风化等高线
- 特点: POLYLINE或LWPOLYLINE

### 标高标注
- 同一图层的TEXT实体
- 内容为纯数字（如`-25`, `-30`, `-53`）
- 位置通常在等高线附近

### 标高-等高线匹配
- 最近距离匹配：每个标高TEXT匹配到最近的POLYLINE
- 一条等高线可能有0个或多个标高（中间等高线通常无标注）

## 桩型参数表

通常嵌入在图纸右下角，图层`TEXT_NOTE`。

格式示例：
```
GZH01  D=600  C40(P8)  Ra=3200kN
GZH02  D=800  C40(P8)  Ra=5200kN
GZH03  D=2000
GZH04  D=1200
GZH05  D=1400
GZH06  D=2200
```

提取正则: `(GZH\d+).*?[Dd]=(\d+)`

## 坐标系统

- 桩坐标通常为世界坐标系(WCS)
- 如有UCS，需转换
- 轴线网格（如`A-Grid$0$AXIS`图层）可用于坐标验证

## DXF编码注意事项

- 中文DWG转DXF后可能是GBK/GB2312编码
- ezdxf读取时可能需要指定编码：
  ```python
  doc = ezdxf.readfile(path)  # 自动检测
  # 或手动指定
  doc = ezdxf.read(path)  # 先读二进制，再手动解码
  ```
- 匿名块名前缀 `A$C` 是AutoCAD自动生成的

## 常见陷阱

1. **块内CIRCLE vs 模型空间CIRCLE**: 桩在块内时，INSERT的插入点不等于桩心
2. **LWPOLYLINE中点≠桩心**: 必须是P1起点
3. **多对一匹配**: 编号、轮廓、标高之间的匹配必须用贪心算法避免冲突
4. **重复实体**: 同一位置可能有两遍（误画），需标记
5. **标高基准**: 桩顶标高通常是相对标高，等高线是绝对标高，不能混用
6. **等高线覆盖不全**: 边缘桩可能缺少等高线数据，IDW插值可能失真
