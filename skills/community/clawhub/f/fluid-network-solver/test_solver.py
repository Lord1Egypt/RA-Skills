from src.parser import load_toml
from src.solver import Solver

# 简单串联网络：source (5.0) --R=0.1--> junction --R=0.2--> load (0.0)
sample_toml = """
[nodes]
  [nodes.source]
  type = "source"
  pressure = 5.0

  [nodes.junction]
  type = "junction"

  [nodes.load]
  type = "load"
  pressure = 0.0           # 负载压力固定为0（回油）

[[edges]]
from = "source"
to = "junction"
resistance = 0.1

[[edges]]
from = "junction"
to = "load"
resistance = 0.2

[scenarios]
  [scenarios.normal]
  description = "正常工况"
  node_states = []
"""

net = load_toml(sample_toml)
solver = Solver(net)
net_scenario = solver.apply_scenario("normal")
result = solver.solve_linear(net_scenario)

print("压力分布:")
for node, p in result['pressures'].items():
    print(f"  {node}: {p:.4f}")

print("流量分布:")
for (f, t), q in result['flows'].items():
    print(f"  {f} -> {t}: {q:.4f}")