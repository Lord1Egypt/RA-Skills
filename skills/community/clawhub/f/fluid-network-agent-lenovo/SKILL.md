---
description: 从 TOML 读取稳态不可压缩流体网络，计算各节点压力与各管路流量/压差（可选速度），并按工况输出连通性与负载可靠性（PASS/FAIL）。当用户给出网络 TOML 或询问某工况下系统是否能正常工作时使用。
---

# 流体网络求解与可靠性报告

该 Skill 会从 TOML 里读取：
- 节点：`junction`（未知压力）和 `reservoir`（固定压力）
- 管路：阻力模型（`linear` 或 `quadratic`），可选的 `gating` 用于表示阀门/故障开关
- 工况：有限变量赋值（例如 `valve_v1 = "open"/"closed"`）
- 功能判据：由一个或多个负载节点组成的 PASS/FAIL 规则

然后对每个工况计算：
- 节点压力与各管路流量/压差（需要几何信息时可给出速度）
- 仅基于启用边的连通性，并按阈值判断负载/功能是否可靠（PASS/FAIL）


用户要做下面任意一件事时用这个 Skill：
- 计算“各节点压力 / 各管路流量/流速 / 系统流路”
- 提供流体网络 TOML，或要求把需求整理成 TOML
- 需要对多个阀门/故障工况做对比，并判断“哪个工况能让哪个负载/功能工作”


- TOML 文件路径；至少包含 `nodes`、`edges`，`scenarios` / `functions` / `analysis` 可选但推荐。

如果用户没有提供 TOML，让 Agent 按 `reference.md` 的格式补全成可运行版本（参考 `examples/example_network.toml`）。

## 执行顺序

1. 先确认用户想看什么：要不要按“工况”对比、以及每个负载/功能的阈值条件。
2. 检查 TOML 字段是否齐全（缺什么就让用户补齐，或让 Agent 补齐最小可运行字段）。
3. 跑计算：`python scripts/run_fluid_network.py --input <toml_path> --format markdown`（需要指定工况就加 `--scenario <scenario_id>`）。
4. 失败就按报错定位字段/引用问题，并最多重试两轮。
5. 输出 Markdown 报告，按工况给出连通性、各边结果和功能 PASS/FAIL。

## 输出格式


```markdown
# Fluid Network Scenario Report

## Scenario: <id>
### Connectivity
- Reachable nodes from sources: ...
### Edge results
- <edge_id>: enabled=..., Q=... m3/s, v=... m/s|n/a, dP=... Pa, R_eff=...
### Function reliability
- <function_id>: PASS|FAIL
  - Load <load_node_id>: PASS|FAIL, connected=..., p=... Pa, flow=... m3/s
```

## 约定与假设（输出时保持一致）

- Steady-state, incompressible, network-level mass balance at `junction` nodes.
- Flow direction uses edge orientation: positive `Q` is `from -> to`.
- Linear model: `dP = R * Q`. Quadratic model: `dP = R * Q^2`.
- If an edge is scenario-disabled by gating, the solver multiplies its resistance by a large factor
  to approximate a blocked pipe (and connectivity uses enabled=boolean).

