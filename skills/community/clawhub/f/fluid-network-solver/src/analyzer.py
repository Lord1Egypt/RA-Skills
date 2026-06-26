
from typing import Dict, List, Set
from collections import deque
from .models import Network

class Analyzer:
    def __init__(self, network: Network):
        self.network = network

    def check_connectivity(self, net: Network) -> Dict[str, bool]:
        """检查每个负载是否与至少一个源连通（考虑阀门状态）"""
        # 构建邻接表（无向图，但根据阀门状态决定是否连接）
        graph = {}
        for node_id in net.nodes:
            graph[node_id] = []

        for edge in net.edges:
            from_node = edge.from_node
            to_node = edge.to_node
            # 检查阀门是否关闭：如果节点是valve且状态为closed，则不连接
            from_closed = (net.nodes[from_node].type == 'valve' and 
                          getattr(net.nodes[from_node], 'initial_state', 'open') == 'closed')
            to_closed = (net.nodes[to_node].type == 'valve' and 
                        getattr(net.nodes[to_node], 'initial_state', 'open') == 'closed')
            if not (from_closed or to_closed):
                # 双向连接
                graph[from_node].append(to_node)
                graph[to_node].append(from_node)

        sources = [node_id for node_id, node in net.nodes.items() if node.type in ['source', 'pump']]
        loads = [node_id for node_id, node in net.nodes.items() if node.type == 'load']

        connectivity = {}
        for load in loads:
            visited = set()
            queue = deque([load])
            found = False
            while queue and not found:
                cur = queue.popleft()
                if cur in visited:
                    continue
                visited.add(cur)
                if cur in sources:
                    found = True
                    break
                for neighbor in graph.get(cur, []):
                    if neighbor not in visited:
                        queue.append(neighbor)
            connectivity[load] = found
        return connectivity

    def analyze(self, solution: Dict, net_scenario: Network = None) -> Dict:
        """分析求解结果，返回负载状态和连通性报告"""
        pressures = solution.get('pressures', {})
        flows = solution.get('flows', {})

        if net_scenario is None:
            net_scenario = self.network

        load_status = {}
        for node_id, node in net_scenario.nodes.items():
            if node.type == 'load':
                p = pressures.get(node_id)
                inflow = 0.0
                for (f, t), q in flows.items():
                    if t == node_id:
                        inflow += q
                status = 'normal'
                reasons = []
                if node.min_pressure is not None and (p is None or p < node.min_pressure):
                    status = 'failed'
                    reasons.append(f'pressure {p:.4f} < {node.min_pressure}')
                if node.min_flow is not None and inflow < node.min_flow:
                    status = 'failed'
                    reasons.append(f'flow {inflow:.4f} < {node.min_flow}')
                load_status[node_id] = {
                    'status': status,
                    'pressure': p,
                    'flow': inflow,
                    'reasons': reasons
                }

        connectivity = self.check_connectivity(net_scenario)
        for load_id, info in load_status.items():
            info['connected'] = connectivity.get(load_id, False)

        return {'loads': load_status, 'connectivity': connectivity}