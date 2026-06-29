# API 参考

## 核心库 (drawio_gen)

- `DrawIOBuilder(name)` - 创建画布
- `builder.add_node(label, x, y, w, h, style, parent_id)` - 添加节点
- `builder.add_edge(source_id, target_id, label, style)` - 添加连线
- `builder.add_container(label, x, y, w, h, style)` - 添加容器
- `builder.connect(src_node, tgt_node, label, style)` - 连接两个节点
- `builder.save(filepath)` - 保存文件
- `Styles.*` - 20+预设样式

## 模板库 (drawio_templates)

- `create_flowchart(steps, title, direction)` - 流程图
- `create_architecture(layers, title)` - 分层架构图
- `create_class_diagram(classes, title)` - UML 类图
- `create_er_diagram(entities, title)` - ER 实体关系图
- `create_tree(root, children, x, y)` - 树形/组织图
- `create_sequence_diagram(actors, messages, title)` - 时序图
- `create_mindmap(center, branches, title)` - 思维导图
- `create_network_topology(devices, connections, title)` - 网络拓扑图

## 布局工具

- `vertical_layout(count, x, y, w, h, gap)` - 垂直排列
- `horizontal_layout(count, x, y, w, h, gap)` - 水平排列
- `grid_layout(rows, cols, x, y, w, h, gap_x, gap_y)` - 网格排列
- `auto_size_node(label)` - 根据文本自动计算节点大小

## 版本管理 (drawio_version)

```python
import sys
sys.path.insert(0, "{SKILL_DIR}/scripts")
from drawio_version import VersionManager

vm = VersionManager(base_dir="{workspace}")
vm.init("output.drawio", "初始版本")
vm.save_version("output.drawio", "更新了颜色")
vm.list_versions("output.drawio")
vm.restore_version("output.drawio", "v2")
vm.status("output.drawio")
```

## 样式预设

**节点样式**: `DEFAULT_NODE`, `BLUE_NODE`, `GREEN_NODE`, `ORANGE_NODE`, `RED_NODE`, `PURPLE_NODE`, `YELLOW_NODE`, `CYAN_NODE`, `GRAY_NODE`, `PINK_NODE`

**特殊形状**: `DIAMOND`(菱形), `CYLINDER`(圆柱/数据库), `CLOUD`(云), `CIRCLE`(圆), `HEXAGON`(六边形), `PARALLELOGRAM`(平行四边形), `DOCUMENT`(文档), `NOTE`(便签)

**标题样式**: `HEADER_BLUE`, `HEADER_GREEN`, `HEADER_ORANGE`, `HEADER_RED`, `HEADER_GRAY`

**连线样式**: `DEFAULT_EDGE`, `BOLD_EDGE`, `DASHED_EDGE`, `RED_EDGE`, `BLUE_EDGE`, `GREEN_EDGE`, `GRAY_EDGE`, `NO_ARROW`, `DIAMOND_ARROW`, `OPEN_ARROW`
