"""
schemas.py - JSON Schema 定义
用于结构化设计描述的验证
"""

# 节点类型定义
NODE_TYPES = [
    # 流程图
    'start', 'end', 'process', 'decision', 'note', 'external',
    # 时序图
    'actor', 'entity', 'lifeline', 'activation', 'message', 'self_call', 'frame',
    # 网络拓扑
    'cloud', 'device', 'server', 'router', 'switch', 'subnet', 'bus',
    # 架构图
    'module', 'interface',
    # 层级图
    'layer',
    # 功能结构图
    'parent', 'child',
    # 部署图
    'container', 'database', 'storage',
]

# 图表类型
CHART_TYPES = [
    'flowchart',    # 流程图
    'sequence',     # 时序图
    'network',      # 网络拓扑图
    'architecture', # 系统功能架构图
    'hierarchy',    # 层级架构图
    'function',    # 功能结构图
    'deployment',  # 部署架构图
]

# 布局方向
LAYOUT_DIRECTIONS = ['LR', 'RL', 'TB', 'BT']


# JSON Schema 定义（用于文档参考）
DESIGN_JSON_SCHEMA = """
{
  "title": "图表标题",
  "type": "图表类型（见 CHART_TYPES）",
  "nodes": [
    {
      "id": "唯一ID（字符串，从0开始）",
      "label": "显示文字",
      "type": "节点类型（见 NODE_TYPES）",
      "x": "X坐标（像素）",
      "y": "Y坐标（像素）",
      "width": "宽度（像素，默认120）",
      "height": "高度（像素，默认60）",
      "style": "额外样式（可选）"
    }
  ],
  "edges": [
    {
      "id": "唯一ID",
      "source": "源节点ID",
      "target": "目标节点ID",
      "label": "连接线标签（可选）",
      "style": "额外样式（可选）"
    }
  ],
  "layout": {
    "direction": "布局方向（LR/RL/TB/BT）",
    "spacingX": "水平间距（像素，默认120）",
    "spacingY": "垂直间距（像素，默认100）"
  }
}
"""

# 样式预设参考
STYLE_REFERENCE = {
    'flowchart': {
        'start': 'rounded=1;fillColor=none;strokeColor=#000000;strokeWidth=2;fontStyle=bold;',
        'end': 'rounded=1;fillColor=none;strokeColor=#000000;strokeWidth=2;fontStyle=bold;',
        'process': 'fillColor=none;strokeColor=#000000;strokeWidth=1;',
        'decision': 'shape=diamond;fillColor=none;strokeColor=#000000;strokeWidth=1;',
        'note': 'dashed=1;fillColor=none;strokeColor=#000000;strokeWidth=1;',
        'external': 'dashed=1;fillColor=none;strokeColor=#000000;strokeWidth=1;',
    },
    'sequence': {
        'actor': 'fillColor=none;strokeColor=#000000;strokeWidth=1;',
        'entity': 'fillColor=none;strokeColor=#000000;strokeWidth=1;',
        'lifeline': 'strokeColor=#000000;strokeWidth=1;dashed=1;',
        'activation': 'fillColor=#000000;strokeColor=#000000;strokeWidth=1;',
        'message': 'strokeColor=#000000;strokeWidth=1;endArrow=classic;',
        'self_call': 'strokeColor=#000000;strokeWidth=1;endArrow=classic;',
        'frame': 'rounded=1;fillColor=none;strokeColor=#000000;strokeWidth=1;',
    },
    'network': {
        'cloud': 'shape=cloud;fillColor=none;strokeColor=#000000;strokeWidth=1;',
        'device': 'fillColor=none;strokeColor=#000000;strokeWidth=1;',
        'server': 'fillColor=none;strokeColor=#000000;strokeWidth=1;',
        'router': 'fillColor=none;strokeColor=#000000;strokeWidth=1;',
        'switch': 'fillColor=none;strokeColor=#000000;strokeWidth=1;',
        'subnet': 'rounded=1;fillColor=#E0E0E0;strokeColor=#000000;strokeWidth=1;',
        'bus': 'rounded=1;fillColor=#E0E0E0;strokeColor=#000000;strokeWidth=1;',
    },
    'architecture': {
        'module': 'rounded=0;fillColor=none;strokeColor=#000000;strokeWidth=2;',
        'interface': 'rounded=0;fillColor=none;strokeColor=#000000;strokeWidth=1;dashed=1;',
    },
    'hierarchy': {
        'layer': 'rounded=1;fillColor=none;strokeColor=#000000;strokeWidth=1;',
        'module': 'rounded=1;fillColor=none;strokeColor=#000000;strokeWidth=1;',
    },
    'function': {
        'parent': 'fillColor=none;strokeColor=#000000;strokeWidth=2;',
        'child': 'fillColor=none;strokeColor=#000000;strokeWidth=1;',
    },
    'deployment': {
        'server': 'fillColor=none;strokeColor=#000000;strokeWidth=1;',
        'container': 'rounded=1;fillColor=none;strokeColor=#000000;strokeWidth=1;',
        'database': 'shape=cylinder;fillColor=none;strokeColor=#000000;strokeWidth=1;',
        'cloud': 'shape=cloud;fillColor=none;strokeColor=#000000;strokeWidth=1;',
        'storage': 'shape=cylinder3;fillColor=none;strokeColor=#000000;strokeWidth=1;',
    },
}


def get_style(chart_type: str, node_type: str) -> str:
    """获取指定图表类型和节点类型的样式字符串"""
    preset = STYLE_REFERENCE.get(chart_type, STYLE_REFERENCE['flowchart'])
    return preset.get(node_type, preset.get('process', ''))


def validate_design(structured: dict) -> tuple:
    """
    验证结构化设计描述
    
    Returns:
        (is_valid, errors): 是否有效，以及错误列表
    """
    errors = []
    
    # 检查必填字段
    if 'title' not in structured:
        errors.append('缺少必填字段: title')
    
    if 'type' not in structured:
        errors.append('缺少必填字段: type')
    elif structured['type'] not in CHART_TYPES:
        errors.append(f'无效的图表类型: {structured["type"]}，有效值: {CHART_TYPES}')
    
    if 'nodes' not in structured:
        errors.append('缺少必填字段: nodes')
    elif not isinstance(structured['nodes'], list):
        errors.append('nodes 必须是数组')
    
    if 'edges' not in structured:
        errors.append('缺少必填字段: edges')
    elif not isinstance(structured['edges'], list):
        errors.append('edges 必须是数组')
    
    # 检查节点 ID 唯一性
    if 'nodes' in structured and isinstance(structured['nodes'], list):
        node_ids = [n.get('id') for n in structured['nodes'] if 'id' in n]
        if len(node_ids) != len(set(node_ids)):
            errors.append('节点 ID 必须唯一')
    
    # 检查边引用
    if 'nodes' in structured and 'edges' in structured:
        node_ids = set(n.get('id') for n in structured['nodes'] if 'id' in n)
        for edge in structured['edges']:
            src = edge.get('source')
            tgt = edge.get('target')
            if src not in node_ids:
                errors.append(f'边的源节点 ID 不存在: {src}')
            if tgt not in node_ids:
                errors.append(f'边的目标节点 ID 不存在: {tgt}')
    
    # 检查布局
    if 'layout' in structured:
        layout = structured['layout']
        if 'direction' in layout and layout['direction'] not in LAYOUT_DIRECTIONS:
            errors.append(f'无效的布局方向: {layout["direction"]}，有效值: {LAYOUT_DIRECTIONS}')
    
    return len(errors) == 0, errors
