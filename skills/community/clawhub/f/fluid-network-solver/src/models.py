from dataclasses import dataclass
from typing import List, Dict, Optional

@dataclass
class Node:
    """网络中的节点"""
    id: str
    type: str  # 'source', 'pump', 'valve', 'load', 'junction'
    # 可选属性
    pressure: Optional[float] = None   # 源或泵的压力
    min_flow: Optional[float] = None   # 负载最小流量
    min_pressure: Optional[float] = None # 负载最小压力
    initial_state: str = "open"        # 阀门初始状态

@dataclass
class Edge:
    """管路（边）"""
    from_node: str
    to_node: str
    resistance: float          # 流阻系数 R
    model: str = "quadratic"   # 流阻模型: 'linear' 或 'quadratic'

@dataclass
class Scenario:
    """预定义工况"""
    name: str
    description: str
    node_states: Dict[str, Dict]  # 例如 {'valve1': {'state': 'closed'}}

@dataclass
class Network:
    """整个流体网络"""
    nodes: Dict[str, Node]
    edges: List[Edge]
    scenarios: Dict[str, Scenario]