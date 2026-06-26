"""
designer.py - LLM 生成结构化设计描述
将自然语言描述转换为结构化的 JSON 设计描述

架构说明：
- 本身不调用任何 LLM API
- generate_structured_description() 返回 dict：
    - needs_llm: True  → 需要主 agent 调用 MiniMax，返回的 prompt 供主 agent 使用
    - needs_llm: False → 已有结构化 JSON（从 --from-llm 模式注入）
- 由主 agent 在两者之间传递数据
"""
import json
import re
import sys
from pathlib import Path

# 内置图表类型关键词
FLOW_KEYWORDS = ['流程', '步骤', '首先', '然后', '接着', '最后', '如果', '则', '判断', '分支', '开始', '结束']
SEQUENCE_KEYWORDS = ['发起', '响应', '调用', '返回', '消息', '时序', '交互', '请求', '应答']
ARCH_KEYWORDS = ['架构', '模块', '组件', '系统', '层次', '分层', '功能', '子系统']
NETWORK_KEYWORDS = ['网络', '拓扑', '服务器', '客户端', '设备', '连接', '网段', '网关', '路由器']
HIERARCHY_KEYWORDS = ['层级', '层次', '级别', '等级', '上层', '下层', '基层', '顶层']
FUNCTION_KEYWORDS = ['功能', '子功能', '模块', '划分', '拆解']
DEPLOYMENT_KEYWORDS = ['部署', '实例', '节点', '集群', '容器', '云', '服务器', '数据库']


def generate_structured_description(text: str, chart_type_hint: str = None) -> dict:
    """
    将自然语言描述转换为结构化的 draw.io 设计 JSON。

    本身不调用 LLM。
    - 如果 text 是原始描述：返回 {'needs_llm': True, 'llm_prompt': '...'}
    - 如果 text 已经是 JSON（--from-llm 模式）：返回 {'needs_llm': False, 'result': {...}}

    Args:
        text: 输入（原始描述 或 JSON 字符串）
        chart_type_hint: 可选的图表类型提示

    Returns:
        dict: {
            'needs_llm': bool,
            'llm_prompt': str (needs_llm=True 时),
            'result': dict (needs_llm=False 时)
        }
    """
    # 检测是否为 JSON 字符串（--from-llm 模式）
    stripped = text.strip()
    if stripped.startswith('{') and stripped.endswith('}'):
        try:
            result = json.loads(stripped)
            if isinstance(result, dict) and 'title' in result:
                return {'needs_llm': False, 'result': result}
        except json.JSONDecodeError:
            pass

    # 原始描述 → 需要 LLM 分析
    prompt = _build_llm_prompt(text, chart_type_hint)
    return {
        'needs_llm': True,
        'llm_prompt': prompt,
        'original_text': text
    }


def _build_llm_prompt(text: str, chart_type_hint: str = None) -> str:
    """构建发给 LLM 的 prompt（供主 agent 调用 MiniMax 使用）

    核心哲学：LLM 只需描述"节点内容和连接关系"，不计算坐标。
    坐标由本地 Python layout engine 自动计算。
    """
    chart_type_instruction = ""
    if chart_type_hint:
        chart_type_instruction = f"\n指定图表类型: {chart_type_hint}"

    return f"""请分析以下描述，生成图表的结构化设计 JSON。

{chart_type_instruction}

输入描述：
{text}

请生成符合以下 JSON Schema 的结构化设计：

{{
  "title": "图表标题",
  "type": "flowchart",
  "nodes": [
    {{
      "id": "节点ID（字符串，如'1'、'2'）",
      "label": "显示在节点内的文字（简洁，10字以内为佳）",
      "type": "start|end|process|decision|data|document"
    }}
  ],
  "edges": [
    {{
      "source": "源节点ID",
      "target": "目标节点ID",
      "label": "判断分支标签（是/否/Y/N，空字符串表示普通连线）"
    }}
  ]
}}

**绘制规范：**

1. 节点类型：
   - start/end：流程起点/终点，用 ellipse
   - process：普通处理步骤，用 rounded=1 矩形
   - decision：判断节点（是/否分支），用 rhombus 菱形
   - data：数据输入，用 parallelogram
   - document：文档，用 shape=document

2. 判断节点必须引出两条边：
   - 一条 label="是" 或 "Y"
   - 一条 label="否" 或 "N"

3. **重要：不要写 x, y, width, height — 本地引擎会自动计算布局**

4. 返回纯 JSON，不要任何说明文字

请直接输出 JSON：
"""


def _detect_chart_type(text: str) -> str:
    """检测最可能的图表类型（基于关键词）"""

    text_lower = text.lower()
    scores = {
        'flowchart': sum(1 for kw in FLOW_KEYWORDS if kw.lower() in text_lower),
        'sequence': sum(1 for kw in SEQUENCE_KEYWORDS if kw.lower() in text_lower),
        'architecture': sum(1 for kw in ARCH_KEYWORDS if kw.lower() in text_lower),
        'network': sum(1 for kw in NETWORK_KEYWORDS if kw.lower() in text_lower),
        'hierarchy': sum(1 for kw in HIERARCHY_KEYWORDS if kw.lower() in text_lower),
        'function': sum(1 for kw in FUNCTION_KEYWORDS if kw.lower() in text_lower),
        'deployment': sum(1 for kw in DEPLOYMENT_KEYWORDS if kw.lower() in text_lower),
    }
    return max(scores, key=scores.get) if max(scores.values()) > 0 else 'flowchart'


def _extract_json_from_text(text: str) -> dict:
    """从 LLM 输出中提取 JSON（主 agent 注入结果时使用）"""

    text = re.sub(r'```json\s*', '', text)
    text = re.sub(r'```\s*', '', text)
    text = text.strip()

    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass

    # 尝试提取 {...} 部分
    match = re.search(r'\{[\s\S]*\}', text)
    if match:
        try:
            return json.loads(match.group(0))
        except json.JSONDecodeError:
            pass

    raise ValueError(f"无法从文本中提取 JSON: {text[:200]}")


# ============== 规则引擎后备（仅处理极简单描述） ==============

def _generate_with_rules(text: str, chart_type_hint: str = None) -> dict:
    """使用内置规则生成结构化描述（后备方案，仅处理极简单流程）"""

    detected_type = chart_type_hint or _detect_chart_type(text)

    generators = {
        'sequence': _generate_sequence_design,
        'network': _generate_network_design,
        'architecture': _generate_architecture_design,
        'hierarchy': _generate_hierarchy_design,
        'function': _generate_function_design,
        'deployment': _generate_deployment_design,
    }

    generator = generators.get(detected_type, _generate_flowchart_design)
    return generator(text)


def _generate_flowchart_design(text: str) -> dict:
    """生成简单流程图设计（后备）"""

    import re
    # 尝试从 "开始 -> A -> B -> 结束" 格式提取步骤
    steps = re.split(r'[-–→.。\n]+', text)
    steps = [s.strip() for s in steps if s.strip() and s.strip() not in ['开始', '结束']]

    nodes = []
    edges = []
    node_id = 0
    x, y = 200, 100

    # 开始
    nodes.append({'id': str(node_id), 'label': '开始', 'type': 'start',
                  'x': x, 'y': y, 'width': 120, 'height': 60})
    prev_id = str(node_id)
    node_id += 1
    y += 100

    for step in steps[:10]:
        if any(kw in step for kw in ['如果', '是否', '判断', '?']):
            nodes.append({'id': str(node_id), 'label': step[:20], 'type': 'decision',
                          'x': x, 'y': y, 'width': 120, 'height': 100})
            edges.append({'id': str(node_id + 1000), 'source': prev_id, 'target': str(node_id), 'label': ''})
            prev_id = str(node_id)
            node_id += 1
            y += 120
        else:
            nodes.append({'id': str(node_id), 'label': step[:30], 'type': 'process',
                          'x': x, 'y': y, 'width': 120, 'height': 60})
            edges.append({'id': str(node_id + 1000), 'source': prev_id, 'target': str(node_id), 'label': ''})
            prev_id = str(node_id)
            node_id += 1
            y += 100

    nodes.append({'id': str(node_id), 'label': '结束', 'type': 'end',
                  'x': x, 'y': y, 'width': 120, 'height': 60})
    edges.append({'id': str(node_id + 1000), 'source': prev_id, 'target': str(node_id), 'label': ''})

    return {
        'title': '流程图',
        'type': 'flowchart',
        'nodes': nodes,
        'edges': edges,
        'layout': {'direction': 'TB', 'spacingX': 120, 'spacingY': 100}
    }


def _generate_sequence_design(text: str) -> dict:
    return {
        'title': '时序图', 'type': 'sequence',
        'nodes': [
            {'id': '0', 'label': '/参与者A', 'type': 'actor', 'x': 100, 'y': 50, 'width': 120, 'height': 50},
            {'id': '1', 'label': '/参与者B', 'type': 'actor', 'x': 280, 'y': 50, 'width': 120, 'height': 50},
        ],
        'edges': [
            {'id': '100', 'source': '0', 'target': '1', 'label': '1. 请求', 'style': 'solid'},
        ],
        'layout': {'direction': 'LR', 'spacingX': 180, 'spacingY': 100}
    }


def _generate_network_design(text: str) -> dict:
    return {
        'title': '网络拓扑图', 'type': 'network',
        'nodes': [
            {'id': '0', 'label': '云端服务', 'type': 'cloud', 'x': 300, 'y': 50, 'width': 150, 'height': 60},
            {'id': '1', 'label': '核心交换机', 'type': 'device', 'x': 300, 'y': 180, 'width': 120, 'height': 60},
        ],
        'edges': [{'id': '100', 'source': '0', 'target': '1', 'label': '', 'style': 'solid'}],
        'layout': {'direction': 'TB', 'spacingX': 150, 'spacingY': 130}
    }


def _generate_architecture_design(text: str) -> dict:
    return {
        'title': '系统功能架构图', 'type': 'architecture',
        'nodes': [
            {'id': '0', 'label': '表现层', 'type': 'module', 'x': 300, 'y': 50, 'width': 200, 'height': 60},
            {'id': '1', 'label': '业务逻辑层', 'type': 'module', 'x': 300, 'y': 150, 'width': 200, 'height': 60},
            {'id': '2', 'label': '数据访问层', 'type': 'module', 'x': 300, 'y': 250, 'width': 200, 'height': 60},
        ],
        'edges': [
            {'id': '100', 'source': '0', 'target': '1', 'label': '', 'style': 'solid'},
            {'id': '101', 'source': '1', 'target': '2', 'label': '', 'style': 'solid'},
        ],
        'layout': {'direction': 'TB', 'spacingX': 220, 'spacingY': 100}
    }


def _generate_hierarchy_design(text: str) -> dict:
    return {
        'title': '层级架构图', 'type': 'hierarchy',
        'nodes': [
            {'id': '0', 'label': '决策层', 'type': 'layer', 'x': 250, 'y': 50, 'width': 300, 'height': 80},
            {'id': '1', 'label': '管理层', 'type': 'layer', 'x': 250, 'y': 180, 'width': 300, 'height': 80},
            {'id': '2', 'label': '执行层', 'type': 'layer', 'x': 250, 'y': 310, 'width': 300, 'height': 80},
        ],
        'edges': [],
        'layout': {'direction': 'TB', 'spacingX': 320, 'spacingY': 130}
    }


def _generate_function_design(text: str) -> dict:
    return {
        'title': '功能结构图', 'type': 'function',
        'nodes': [
            {'id': '0', 'label': '主功能', 'type': 'parent', 'x': 300, 'y': 50, 'width': 200, 'height': 60},
            {'id': '1', 'label': '子功能1', 'type': 'child', 'x': 150, 'y': 150, 'width': 80, 'height': 120},
            {'id': '2', 'label': '子功能2', 'type': 'child', 'x': 300, 'y': 150, 'width': 80, 'height': 120},
            {'id': '3', 'label': '子功能3', 'type': 'child', 'x': 450, 'y': 150, 'width': 80, 'height': 120},
        ],
        'edges': [
            {'id': '100', 'source': '0', 'target': '1', 'label': ''},
            {'id': '101', 'source': '0', 'target': '2', 'label': ''},
            {'id': '102', 'source': '0', 'target': '3', 'label': ''},
        ],
        'layout': {'direction': 'TB', 'spacingX': 180, 'spacingY': 150}
    }


def _generate_deployment_design(text: str) -> dict:
    return {
        'title': '部署架构图', 'type': 'deployment',
        'nodes': [
            {'id': '0', 'label': '云服务器', 'type': 'server', 'x': 300, 'y': 50, 'width': 150, 'height': 60},
            {'id': '1', 'label': '应用服务', 'type': 'container', 'x': 200, 'y': 150, 'width': 120, 'height': 60},
            {'id': '2', 'label': '数据库', 'type': 'database', 'x': 400, 'y': 150, 'width': 120, 'height': 80},
        ],
        'edges': [
            {'id': '100', 'source': '0', 'target': '1', 'label': ''},
            {'id': '101', 'source': '1', 'target': '2', 'label': ''},
        ],
        'layout': {'direction': 'TB', 'spacingX': 200, 'spacingY': 120}
    }
