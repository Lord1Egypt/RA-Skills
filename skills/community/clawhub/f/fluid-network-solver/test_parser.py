from src.parser import load_toml

sample_toml = """
[nodes]
  [nodes.tank]
  type = "source"
  pressure = 0.0

  [nodes.pump1]
  type = "pump"
  pressure = 5.0

  [nodes.valve1]
  type = "valve"
  initial_state = "open"

  [nodes.load1]
  type = "load"
  min_flow = 0.5
  min_pressure = 2.0

  [nodes.junction1]
  type = "junction"

[[edges]]
from = "tank"
to = "junction1"
resistance = 0.1

[[edges]]
from = "junction1"
to = "pump1"
resistance = 0.05

[[edges]]
from = "pump1"
to = "valve1"
resistance = 0.02

[[edges]]
from = "valve1"
to = "load1"
resistance = 0.03

[scenarios]
  [scenarios.normal]
  description = "正常工况"
  node_states = []
"""

net = load_toml(sample_toml)
print("节点:", list(net.nodes.keys()))
print("边数:", len(net.edges))
print("工况:", list(net.scenarios.keys()))