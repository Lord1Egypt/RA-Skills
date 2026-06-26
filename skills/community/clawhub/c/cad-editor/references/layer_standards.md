# 行业图层命名规范

## 命名规则

```
图层名 = 领域前缀_功能_细分（可选）

最大长度：255 字符（建议≤31字符兼容旧版）
允许字符：字母、数字、下划线、连字符、$
不允许：空格、< > / \ " : ; ? * | = ' `
不区分大小写（CAD内部统一为大写）
```

## 建筑制图 (GB/T 50104)

### 标准图层列表

| 图层名 | 颜色(ACI) | 线型 | 线宽(mm) | 说明 |
|--------|----------|------|---------|------|
| A-WALL | 1 (红) | Continuous | 0.50 | **墙体** — 外墙/内墙 |
| A-WALL-FULL | 1 (红) | Continuous | 0.50 | 实心墙 |
| A-DOOR | 3 (绿) | Continuous | 0.25 | 门 |
| A-WIND | 4 (青) | Continuous | 0.25 | 窗 |
| A-COLS | 1 (红) | Continuous | 0.50 | 柱子 |
| A-COLS-PATT | 8 (灰) | Continuous | 0.25 | 柱填充 |
| A-STAIR | 2 (黄) | Continuous | 0.25 | 楼梯 |
| A-BALN | 3 (绿) | Continuous | 0.18 | 阳台/栏杆 |
| A-FIXT | 5 (蓝) | Continuous | 0.18 | 卫浴/家具 |
| A-EQPM | 6 (品红) | Continuous | 0.18 | 设备 |
| A-AXIS | 1 (红) | CENTER | 0.13 | 轴线 |
| A-DIMS | 4 (青) | Continuous | 0.18 | 尺寸标注 |
| A-TEXT | 7 (白) | Continuous | 0.18 | 文字说明 |
| A-HATCH | 8 (灰) | ANSI31 | 0.13 | 材料填充 |
| A-TITL | 7 (白) | Continuous | 0.50 | 图框/标题栏 |

### 常见组合
```python
# 简化版建筑模板
ARCH_LAYERS = {
    'A-WALL':   {'color': 1, 'linetype': 'Continuous', 'lineweight': 50},
    'A-DOOR':   {'color': 3, 'linetype': 'Continuous', 'lineweight': 25},
    'A-WIND':   {'color': 4, 'linetype': 'Continuous', 'lineweight': 25},
    'A-COLS':   {'color': 1, 'linetype': 'Continuous', 'lineweight': 50},
    'A-DIMS':   {'color': 4, 'linetype': 'Continuous', 'lineweight': 18},
    'A-TEXT':   {'color': 7, 'linetype': 'Continuous', 'lineweight': 18},
    'A-HATCH':  {'color': 8, 'linetype': 'ANSI31',     'lineweight': 13},
}
```

## 机械制图 (GB/T 4457-4 / GB/T 14665)

### 标准图层

| 图层名 | 颜色 | 线型 | 线宽 | 说明 |
|--------|------|------|------|------|
| M-OUTLINE | 7 | Continuous | 0.50 | **轮廓线**（粗实线）|
| M-CENTER | 1 (红) | CENTER | 0.13 | 中心线/轴线 |
| M-HIDDEN | 2 (黄) | HIDDEN | 0.25 | **隐藏线**（虚线）|
| M-DIM | 4 (青) | Continuous | 0.18 | 尺寸标注 |
| M-TEXT | 7 | Continuous | 0.18 | 文字 |
| M-SECT | 1 (红) | ANSI31 | 0.13 | 剖面填充 |
| M-THREAD | 3 (绿) | Continuous | 0.25 | 螺纹大径 |
| M-THREAD-MINOR | 3 (绿) | Continuous | 0.13 | 螺纹小径 |
| M-PHANTOM | 6 | PHANTOM | 0.13 | 假想轮廓 |
| M-CUT | 1 (红) | Continuous | 0.70 | **剖切线**（特粗）|

### 线宽规范（GB/T）
```
粗实线  0.50~0.70 mm  → 轮廓线/剖切线
中实线  0.25~0.35 mm  → 螺纹/隐藏线/可见过渡线
细实线  0.13~0.18 mm  → 尺寸/文字/中心线/剖面线
特粗线  0.70~1.00 mm  → 图框/标题栏外框
```

## 电气制图 (GB/T 4728)

### 标准图层

| 图层名 | 颜色 | 线型 | 说明 |
|--------|------|------|------|
| E-WIRE | 5 (蓝) | Continuous | 导线/线路 |
| E-SYMB | 7 (白) | Continuous | 电气符号 |
| E-DIM | 4 (青) | Continuous | 尺寸/标注 |
| E-TEXT | 7 (白) | Continuous | 文字说明 |
| E-EQUIP | 1 (红) | Continuous | 设备外形 |
| E-PANEL | 6 (品红) | Continuous | 配电箱/柜 |
| E-LIGHT | 3 (绿) | Continuous | 灯具 |
| E-CTRL | 2 (黄) | Continuous | 控制回路 |

## 结构制图 (平法规则)

### 标准图层

| 图层名 | 颜色 | 线型 | 说明 |
|--------|------|------|------|
| S-BEAM | 1 (红) | Continuous | 梁轮廓 |
| S-COL | 1 (红) | Continuous | 柱轮廓 |
| S-SLAB | 1 (红) | Continuous | 板轮廓 |
| S-REBAR-M | 3 (绿) | Continuous | **主筋**（粗）|
| S-REBAR-S | 3 (绿) | Continuous | **箍筋/分布筋**（细）|
| S-REBAR-TOP | 2 (黄) | Continuous | **负筋/面筋** |
| S-CONC | 8 (灰) | SOLID | 混凝土填充 |
| S-FTG | 1 (红) | Continuous | 基础轮廓 |
| S-DIM | 4 (青) | Continuous | 标注 |
| S-TEXT | 7 (白) | Continuous | 文字/配筋标注 |

## 管道/暖通

### 标准图层

| 图层名 | 颜色 | 线型 | 说明 |
|--------|------|------|------|
| P-PIPE | 5 (蓝) | Continuous | 管道双线 |
| P-PIPE-CL | 1 (红) | CENTER | 管道中心线 |
| P-VALV | 7 (白) | Continuous | 阀门 |
| P-FITT | 4 (青) | Continuous | 管件（弯头/三通等）|
| P-DIM | 4 (青) | Continuous | 标注 |
| P-TEXT | 7 (白) | Continuous | 文字 |
| P-INSU | 9 (浅灰) | Continuous | 保温层 |
| P-FLANGE | 2 (黄) | Continuous | 法兰 |

## 线型名称速查

| 线型名 | 说明 | 用途 |
|--------|------|------|
| Continuous | 实线 | 默认，轮廓/标注 |
| CENTER | 点划线（长-点-长）| 中心线/轴线 |
| DASHED | 虚线（短划） | 隐藏线 |
| HIDDEN | 隐藏虚线 | 不可见边 |
| PHANTOM | 双点划线 | 假想轮廓 |
| DOT | 点线 | 特殊标记 |
| DIVIDE | 交替长短划 | 分界线 |
| BORDER | 边框双线 | 图框外边界 |
| ANSI31 | 45°斜线填充 | 金属剖面 |
| AR-CONC | 混凝土+骨料图案 | 混凝土填充 |
| AR-SAND | 砂土图案 | 土建填充 |
| AR-HBONE | 骨骼图案 | 保温材料 |
