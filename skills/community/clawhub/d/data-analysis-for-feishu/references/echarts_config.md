# ECharts图表配置参考

## 通用配置说明

### 颜色配置
默认配色方案：`["#5470c6", "#91cc75", "#fac858", "#ee6666", "#73c0de", "#3ba272", "#fc8452", "#9a60b4", "#ea7ccc"]`
如需自定义配色，可以在生成配置时修改`DEFAULT_COLORS`变量。

## 各图表类型参数说明

### 1. 折线图 (line)
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| x_axis | List[str] | 是 | X轴数据，如日期、分类名称 |
| y_axis | List[float] | 是 | Y轴数值数据 |
| y_name | str | 否 | Y轴名称，如"销售额"、"访问量" |
| title | str | 是 | 图表标题 |
| smooth | bool | 否 | 是否平滑曲线，默认True |
| show_area | bool | 否 | 是否显示填充区域，默认True |

### 2. 柱状图 (bar)
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| x_axis | List[str] | 是 | X轴分类数据 |
| y_axis | List[float] | 是 | Y轴数值数据 |
| y_name | str | 否 | Y轴名称 |
| title | str | 是 | 图表标题 |
| rotate_label | int | 否 | X轴标签旋转角度，默认30 |
| borderRadius | int | 否 | 柱状图圆角，默认4 |

### 3. 饼图 (pie)
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| labels | List[str] | 是 | 分类标签 |
| values | List[float] | 是 | 对应数值 |
| title | str | 是 | 图表标题 |
| radius | List[str] | 否 | 饼图半径，默认["40%", "70%"]（环形） |
| show_percent | bool | 否 | 是否显示百分比，默认True |

### 4. 仪表盘 (gauge)
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| value | float | 是 | 当前数值 |
| title | str | 是 | 图表标题 |
| max | float | 否 | 最大值，默认100 |
| unit | str | 否 | 单位，默认"%" |
| start_angle | int | 否 | 起始角度，默认180 |
| end_angle | int | 否 | 结束角度，默认0 |

### 5. 雷达图 (radar)
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| indicators | List[Dict] | 是 | 指标配置，每个元素包含name和max字段 |
| values | List[float] | 是 | 对应指标的数值 |
| title | str | 是 | 图表标题 |
| series_name | str | 否 | 系列名称 |
| shape | str | 否 | 雷达图形状，"circle"（圆形）或"polygon"（多边形），默认circle |

## 自定义配置示例
如需更复杂的配置，可以直接修改对应生成函数的返回值，参考ECharts官方文档：https://echarts.apache.org/zh/option.html
