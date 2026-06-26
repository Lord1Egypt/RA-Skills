from src.parser import load_toml
from src.solver import Solver
from src.analyzer import Analyzer

# 测试网络：source(5) -> junction -> load，负载要求 min_pressure=2.0, min_flow=10.0
sample_toml = """
[nodes]
  [nodes.source]
  type = "source"
  pressure = 5.0

  [nodes.tank]
  type = "source"
  pressure = 0.0

  [nodes.junction]
  type = "junction"

  [nodes.load]
  type = "load"
  min_flow = 10.0
  min_pressure = 2.0

[[edges]]
from = "source"
to = "junction"
resistance = 0.1

[[edges]]
from = "junction"
to = "load"
resistance = 0.2

[[edges]]
from = "load"
to = "tank"
resistance = 0.01

[scenarios]
  [scenarios.normal]
  description = "正常工况"
  node_states = []
"""

net = load_toml(sample_toml)
solver = Solver(net)
net_scenario = solver.apply_scenario("normal")
result = solver.solve_linear(net_scenario)

analyzer = Analyzer(net)
report = analyzer.analyze(result)

print("分析报告:")
print(report)