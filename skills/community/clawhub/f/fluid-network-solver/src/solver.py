import numpy as np
from typing import Dict, Tuple, List
import copy
from .models import Network

class Solver:
    def __init__(self, network: Network):
        self.network = network

    def apply_scenario(self, scenario_name: str) -> Network:
        """根据工况修改网络状态，返回新的网络对象（深拷贝）"""
        net = copy.deepcopy(self.network)
        if scenario_name not in net.scenarios:
            return net  # 无该工况，使用默认状态
        scenario = net.scenarios[scenario_name]
        # 修改节点属性
        for node_id, state_dict in scenario.node_states.items():
            if node_id in net.nodes:
                node = net.nodes[node_id]
                for attr, value in state_dict.items():
                    if hasattr(node, attr):
                        setattr(node, attr, value)
        return net

    def solve_linear(self, net: Network) -> Dict:
        """
        线性求解器（节点压力法）
        假设每条边满足 Q = (P_from - P_to) / R
        对每个未知压力节点，列流入流量总和为0的方程
        """
        # 1. 区分固定压力节点和未知节点
        fixed_nodes = []
        unknown_nodes = []
        for node_id, node in net.nodes.items():
            # 如果节点有 pressure 属性且不为 None，视为固定压力节点
            if node.pressure is not None:
                fixed_nodes.append(node_id)
            else:
                unknown_nodes.append(node_id)

        # 对未知节点编号
        node_to_idx = {node_id: i for i, node_id in enumerate(unknown_nodes)}
        n_unknown = len(unknown_nodes)

        if n_unknown == 0:
            # 所有节点压力已知，直接计算流量
            pressures = {node_id: node.pressure for node_id, node in net.nodes.items()}
            flows = self._compute_flows(net, pressures)
            return {'pressures': pressures, 'flows': flows}

        # 初始化矩阵 A (n_unknown x n_unknown) 和向量 b (n_unknown)
        A = np.zeros((n_unknown, n_unknown))
        b = np.zeros(n_unknown)

        # 2. 组装矩阵
        for edge in net.edges:
            from_node = edge.from_node
            to_node = edge.to_node
            R = edge.resistance
            if R <= 0:
                continue

            # 检查阀门是否关闭：如果节点是阀门且状态为 closed，则跳过该边
            from_closed = (net.nodes[from_node].type == 'valve' and
                          getattr(net.nodes[from_node], 'initial_state', 'open') == 'closed')
            to_closed = (net.nodes[to_node].type == 'valve' and
                        getattr(net.nodes[to_node], 'initial_state', 'open') == 'closed')
            if from_closed or to_closed:
                continue  # 阀门关闭，该边断开

            G = 1.0 / R  # 导纳

            from_fixed = from_node in fixed_nodes
            to_fixed = to_node in fixed_nodes

            if from_fixed and to_fixed:
                # 两端固定，不影响未知节点
                continue
            elif from_fixed and not to_fixed:
                # from固定，to未知
                j = node_to_idx[to_node]
                A[j, j] += G
                b[j] += G * net.nodes[from_node].pressure
            elif not from_fixed and to_fixed:
                # from未知，to固定
                i = node_to_idx[from_node]
                A[i, i] += G
                b[i] += G * net.nodes[to_node].pressure
            else:
                # 两端未知
                i = node_to_idx[from_node]
                j = node_to_idx[to_node]
                A[i, i] += G
                A[i, j] -= G
                A[j, j] += G
                A[j, i] -= G

        # 3. 求解线性方程组
        try:
            P_unknown = np.linalg.solve(A, b)
        except np.linalg.LinAlgError:
            print("警告：矩阵奇异，求解失败")
            return {'pressures': {}, 'flows': {}}

        # 4. 构建所有节点的压力字典
        pressures = {}
        for node_id in fixed_nodes:
            pressures[node_id] = net.nodes[node_id].pressure
        for idx, node_id in enumerate(unknown_nodes):
            pressures[node_id] = P_unknown[idx]

        # 5. 计算每条边的流量（同样需考虑阀门关闭）
        flows = self._compute_flows(net, pressures)

        return {'pressures': pressures, 'flows': flows}

    def _compute_flows(self, net: Network, pressures: Dict[str, float]) -> Dict[Tuple[str, str], float]:
        """根据压力计算每条边的流量（有向），考虑阀门关闭"""
        flows = {}
        for edge in net.edges:
            from_node = edge.from_node
            to_node = edge.to_node
            # 检查阀门关闭
            from_closed = (net.nodes[from_node].type == 'valve' and
                          getattr(net.nodes[from_node], 'initial_state', 'open') == 'closed')
            to_closed = (net.nodes[to_node].type == 'valve' and
                        getattr(net.nodes[to_node], 'initial_state', 'open') == 'closed')
            if from_closed or to_closed:
                flows[(from_node, to_node)] = 0.0
                continue
            from_p = pressures.get(edge.from_node, 0)
            to_p = pressures.get(edge.to_node, 0)
            delta_p = from_p - to_p
            R = edge.resistance
            if R <= 0:
                q = 0
            else:
                if edge.model == 'linear':
                    q = delta_p / R
                else:  # quadratic 简化处理
                    q = delta_p / R
            flows[(edge.from_node, edge.to_node)] = q
        return flows