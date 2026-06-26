import tomli
from .models import Network, Node, Edge, Scenario

def load_toml(toml_string: str) -> Network:
    """解析TOML字符串，返回Network对象"""
    data = tomli.loads(toml_string)

    # 解析节点
    nodes = {}
    for node_id, node_data in data.get("nodes", {}).items():
        nodes[node_id] = Node(
            id=node_id,
            type=node_data.get("type", "junction"),
            pressure=node_data.get("pressure"),
            min_flow=node_data.get("min_flow"),
            min_pressure=node_data.get("min_pressure"),
            initial_state=node_data.get("initial_state", "open")
        )

    # 解析边
    edges = []
    for edge_data in data.get("edges", []):
        edges.append(Edge(
            from_node=edge_data["from"],
            to_node=edge_data["to"],
            resistance=edge_data["resistance"],
            model=edge_data.get("model", "quadratic")
        ))

    # 解析工况
    scenarios = {}
    for sc_name, sc_data in data.get("scenarios", {}).items():
        node_states = {}
        for item in sc_data.get("node_states", []):
            node_id = item["node"]
            # 将除了node以外的键值对作为状态字典
            state_dict = {k: v for k, v in item.items() if k != "node"}
            node_states[node_id] = state_dict
        scenarios[sc_name] = Scenario(
            name=sc_name,
            description=sc_data.get("description", ""),
            node_states=node_states
        )

    return Network(nodes=nodes, edges=edges, scenarios=scenarios)