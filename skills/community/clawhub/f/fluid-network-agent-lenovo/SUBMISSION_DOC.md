# 算法 + 行业解决方案笔试文档

题目：流体网络求解与 Agent Skill 封装（稳态、不可压缩）


日期：2026-03-19

---

## 0. 题目目标与简化物理模型

在液压、环控、化工等场景中，系统往往可抽象为“节点 + 管路（带阻力）+ 设备（泵/阀/故障）”的网络。

本题限定：

1. 稳态、不可压缩
2. 节点处满足质量守恒（质量守恒在数值上等价于“流量代数和为 0”）
3. 管路阻力采用经验简化模型：
   1. 线性模型：`dP = R * Q`
   2. 二次模型：`dP = R * Q^2`

输出目标：

1. 在给定源头压力与网络参数下，求解节点压力与各管路流量/流速
2. 在不同工况（阀门开关、故障组合）下，分析系统连通性与负载可靠性
3. 将以上能力封装为 Cursor/Agent Skill，支持由自然语言触发，生成 TOML、执行计算并输出“工况分析报告”

---

## 1. 为什么要“工况（scenario）有限组合”，避免指数爆炸

工业系统的真实开关/故障组合可能非常多。若把每个开关都枚举成全部拓扑状态，工况数会指数级增长。

本解法采用两层建模来避免全量遍历：

1. 网络拓扑（nodes/edges）只描述“物理可能连通的骨架”，每条边带阻力模型，并可带 gating（门控条件）
2. 工况（scenarios）只列举有限的、用户关心的变量赋值组合（例如 `valve_v1="open"` vs `valve_v1="closed"`）
3. 对于 gating 关闭的边，不需要真正改拓扑，而是用“等效大阻力”近似为阻断；并且连通性分析只把 `enabled=true` 的边加入 BFS 图

因此计算只对 `scenarios` 列表做有限次求解，避免了指数爆炸。

---

## 2. TOML Schema 设计（结构化数据设计）

为方便脚本解析，TOML 至少要包含 `nodes` 和 `edges`；`scenarios`、`functions` 可选，但当你需要“工况对比”和“功能判定”时，最好把它们补上。

### 2.1 顶层键（Top-level）

- `nodes`: `[[nodes]]` 数组（每个元素描述一个节点）
- `edges`: `[[edges]]` 数组（每个元素描述一条管路/边）
- `scenarios`（可选）：`[[scenarios]]` 数组（每个元素描述一种工况）
- `functions`（可选）：`[[functions]]` 数组（每个 function 表示一个系统功能可靠性判据，通常由一个或多个 load 节点构成）
- `analysis`（可选）：`[analysis]`（控制报告的阈值判定指标等）
- `source_node_ids`（可选）：数组（指定连通性 BFS 的起点；如果缺省，则采用 `nodes[].role=="source"` 的所有节点）

单位约定（建议统一写清楚，便于面试交流）：

1. 压力：`Pa`
2. 流量：`m3/s`
3. 阻力模型参数 `R` 要与模型匹配：
   1. 线性：`dP = R * Q`
   2. 二次：`dP = R * Q^2`

### 2.2 nodes 表结构

节点类型用 `kind` 区分：

1. `reservoir`：固定压力节点（可作为源头/回流/负载最小工作点的压力对照）
2. `junction`：未知压力节点（求解器计算其压力）

建议 roles：

- `role="source"`：源头，用于连通性 BFS 起点（可选）
- `role="load"`：负载节点，用于阈值可靠性判定（必须配阈值）

示例：

```toml
[[nodes]]
id = "S"
kind = "reservoir"
role = "source"
pressure_pa = 3.0e6

[[nodes]]
id = "J1"
kind = "junction"

[[nodes]]
id = "L1"
kind = "reservoir"
role = "load"
pressure_pa = 1.2e5
min_flow_m3s = 1.0e-3
min_pressure_pa = 1.0e5
```

说明：

1. `reservoir` 节点会被当做固定压力（可在 scenarios 中用 `reservoir_pressure_overrides_pa` 覆盖）
2. `load` 节点的 `min_flow_m3s` 与 `min_pressure_pa` 用于最终 PASS/FAIL 判断

### 2.3 edges 表结构

边表示管路/阻力元件，结构包含：

- `id`
- `from`
- `to`
- `resistance_model`：阻力模型
- `gating`（可选）：门控条件，决定该边是否等效启用
- `area_m2` 或 `diameter_m`（可选）：用于估算速度

#### 阻力模型 resistance_model

两种模型：

1. 线性：`kind="linear"`，`dP = R * Q`
2. 二次：`kind="quadratic"`，`dP = R * Q^2`

示例（线性管）：

```toml
[[edges]]
id = "E_S_J"
from = "S"
to = "J1"

[edges.resistance_model]
kind = "linear"
R = 5.0e5

diameter_m = 0.02
```

#### gating 门控（用于“阀门/故障组合”）

gating 用变量赋值决定边是否启用。

关键字段：

- `enabled_when_mode`：
  - `all`：所有 conditions 都匹配才启用
  - `any`：任一 condition 匹配就启用
- `conditions`：数组，每个条件包含：
  - `variable`：变量名（例如 `valve_v1`）
  - `equals`：变量取值（例如 `"open"`）
- `disabled_resistance_multiplier`：当 gating 失效时，将边阻力乘以该倍数（默认 `1e12`），近似阻断

示例（阀门关闭会阻断这条边）：

```toml
[[edges]]
id = "E_J_L1"
from = "J1"
to = "L1"

[edges.resistance_model]
kind = "quadratic"
R = 8.0e10

diameter_m = 0.015

[edges.gating]
enabled_when_mode = "all"
disabled_resistance_multiplier = 1e12

[[edges.gating.conditions]]
variable = "valve_v1"
equals = "open"
```

### 2.4 scenarios 表结构

scenarios 是有限的工况集合，每个 scenario 定义：

- `id`
- `variables`：变量赋值（例如开关状态、故障标志）
- `reservoir_pressure_overrides_pa`（可选）：对某些 reservoir 在该工况下强制覆盖压力

示例：

```toml
[[scenarios]]
id = "normal"

[scenarios.variables]
valve_v1 = "open"

[[scenarios]]
id = "valve_closed"

[scenarios.variables]
valve_v1 = "closed"
```

### 2.5 functions 表结构（可靠性判据）

每个 function 定义：

- `id`
- `load_node_ids`: 需要同时/或满足阈值的 load 节点列表
- `criteria_mode`：
  - `all`：function 只有当所有指定 load 都 PASS 才 PASS
  - `any`：任一 load PASS 则 function PASS

示例：

```toml
[[functions]]
id = "serve_L1"
load_node_ids = ["L1"]
criteria_mode = "all"
```

如果完全省略 `functions`，实现会默认把每个 `role="load"` 的节点单独作为一个 function。

### 2.6 analysis 表结构（可选）

- `flow_metric`：
  - `abs`：用负载节点“净流量绝对值”进行阈值判断
  - `inflow`：只统计正向入流（当你定义流向时更贴近工程口径）
- `topology_direction`：连通性 BFS 的边方向策略（当前默认 `undirected`）
- `flow_abs_threshold_m3s_for_path`：用于报告路径阈值（本版本以可扩展为主）

示例：

```toml
[analysis]
flow_metric = "abs"
topology_direction = "undirected"
```

---

## 3. 流体网络求解器（Python 实现思路）

实现上把问题拆成几块：
1. `reservoir` 压力固定
2. `junction` 压力未知，靠节点质量守恒约束求出来
3. 每条边给出 `dP` 与 `Q` 的关系（线性或二次）
4. gating 关闭的边不改拓扑，而是把阻力乘上很大的系数，等效“基本不通”

### 3.1 网元与符号约定

1. 边 `e` 从 `from` 指向 `to`
2. 流量符号约定：
   - 正 `Q_e` 表示从 `from -> to`
3. 压力差约定：
   - `dP = p_from - p_to`
4. 模型：
   - 线性：`dP = R * Q` => `Q = dP / R`
   - 二次：`dP = R * Q^2` => `Q = sign(dP) * sqrt(|dP|/R)`

### 3.2 线性情况：线性方程组

若所有边都是线性模型，未知量取 `junction` 的压力向量 `p_unknown`。

质量守恒在节点 `k` 表示为：

`sum_over_incident_edges g * (p_k - p_other) = 0`

其中 `g = 1/R` 为导纳（conductance），`p_other` 若为 reservoir 则是已知压力。

最终得到线性方程组：

`A * p_unknown = b`

用高斯消元（带主元）求解即可得到所有 junction 压力，再由每条边的 `dP` 计算 `Q` 与可选速度。

### 3.3 非线性情况：Newton 迭代

当出现二次模型边时，`Q` 与压力之间非线性。

实现中采取数值雅可比 + Newton 更新：

1. 构造残差函数：每个 junction 节点的质量守恒残差
2. 初始猜测：取 reservoir 压力的平均
3. 对压力向量做迭代更新：
   - 计算雅可比矩阵（数值差分）
   - 解线性修正量 `J * dx = -f`
   - 用阻尼因子进行稳定更新
4. 收敛后得到压力，再计算各边流量

工程上：该算法适用于“规模不大、工况有限”的竞赛/笔试任务。

---

## 4. 流路分析器：连通性 + 功能可靠性

流路分析器分两步：

1. 拓扑连通性（connectivity）
2. 功能可靠性（function reliability）

### 4.1 连通性分析（BFS）

连通性图只使用当前工况下被启用的边：

- 若边 gating 让其 `enabled=true`，则加入 BFS
- 若边 gating 关闭，则不加入 BFS（即使数值求解中用大阻力近似）

起点：

1. 如果 TOML 提供了 `source_node_ids`，则从这些节点开始
2. 否则从 `nodes[].role=="source"` 的节点开始

得到：

1. 每个 node 是否可达（reachable）

### 4.2 负载阈值与 PASS/FAIL

对每个 load 节点：

1. 取求解器输出的节点压力 `p`
2. 计算该节点的“净流量”：
   - 使用边流量符号约定，判断该节点是 outflow 还是 inflow
3. 根据 `analysis.flow_metric`：
   1. `abs`：用 `abs(net_inflow)` 与 `min_flow_m3s` 比较
   2. `inflow`：只在 `net_inflow>0` 时计入有效流量
4. 同时满足：
   - `p >= min_pressure_pa`
   - `flow >= min_flow_m3s`

则该 load 节点 PASS，否则 FAIL。

对 function：

- `criteria_mode="all"`：function 只有当其包含的所有 load 都 PASS 才 PASS
- `criteria_mode="any"`：function 只要任一 load PASS 就 PASS

---

## 5. Skill 封装与 Agent 协同（Cursor/Clawhub）

我把数据结构（TOML Schema）、稳态求解和流路可靠性分析组织成一套固定流程。给出网络 TOML 和要对比的工况后，后续计算和报告整理就能直接生成，少做重复劳动。

### 5.1 Skill 目录结构

这个 Skill 目录里我放了这些东西：

1. `SKILL.md`：说明 Agent 怎么调用
2. `scripts/`：命令行入口（把 TOML 跑完并输出报告）
3. `src/`：解析/求解/分析代码
4. `examples/`：样例 TOML，方便检查字段是否对得上

### 5.2 `SKILL.md` 内容应该强调什么

`SKILL.md` 里我会把下面几件事说清楚：

1. 输入是什么（TOML 文件路径、`scenario id` 等）
2. 怎么执行（生成/校验 TOML -> 跑求解器 -> 输出连通性与可靠性）
3. 出错时怎么定位（字段缺失、类型不对、节点引用不存在）
4. 报告长什么样（每个工况的可达节点、各边的 `Q/v/dP`，以及功能 PASS/FAIL）

---

## 6. 可运行示例与报告生成

### 6.1 使用示例 TOML

样例文件：`examples/example_network.toml`

它包含：

1. 一个源头 reservoir `S`
2. 一个回流/另一固定压力 reservoir `R`
3. 一个 junction `J1`
4. 一个用阀门 gating 控制的负载管路到 `L1`
5. 两个 scenarios：`normal`（阀开）与 `valve_closed`（阀关）

### 6.2 运行脚本生成报告

在有 Python 运行环境（Python 3.11+）的情况下：

运行全部 scenarios：

```bash
python scripts/run_fluid_network.py --input examples/example_network.toml --format markdown
```

运行指定 scenarios：

```bash
python scripts/run_fluid_network.py --input examples/example_network.toml --scenario normal --format markdown
```

输出为 Markdown，包含每个 scenario 的：

1. Connectivity（可达节点）
2. Edge results（每条边的 enabled、Q、v、dP、R_eff）
3. Function reliability（PASS/FAIL + 负载细节）

---

## 7. 发布到 Clawhub 并获取 Skill 链接

下面的“发布步骤”是通用流程，你实际用的时候按 Clawhub CLI 的提示替换参数即可。

### 7.1 前置条件

1. `bun`
2. 能执行 `clawhub` CLI（通常由仓库脚本或安装完成）
3. 已登录 Clawhub（需要 token 或 GitHub 授权，具体按 Clawhub 指引）

### 7.2 发布步骤（通用）

1. 确保你要发布的目录内包含 `SKILL.md` 和依赖文件（可选 scripts/src/examples）
2. 执行 publish 命令，并指定：
   - `--slug`：唯一 slug（小写 + 连字符）
   - `--name`：显示名称
   - `--version`：语义化版本号（例如 `1.0.0`）
   - `--changelog`：发布说明

示例（把下面参数替换为你的）：

```bash
bun clawhub publish . \
  --slug fluid-network-agent-<your-id> \
  --name "Fluid Network Agent" \
  --version 1.0.0 \
  --tags latest \
  --changelog "initial release"
```

如果你希望“发布后立刻同步/校验”，可运行 `clawhub inspect` 或 `clawhub sync`（按官方 CLI 文档）。

### 7.3 提交材料中的“Skill 链接”

发布成功后，Clawhub 一般会返回该 skill 的页面链接或 slug 安装路径。

邮件里可以把下面几项带上（评卷更方便看懂）：

1. Skill 页面链接
2. 版本号（例如 1.0.0）
3. 简短说明：该 Skill 支持输入 TOML 并输出 scenario 报告

---

## 8. 最终交付清单（建议按面试/笔试要求准备）

1. Skill 链接（Clawhub 发布后提供）
2. 邮件附件或正文中提供：
   1. `examples/example_network.toml`（样例证明）
   2. 你的 `SKILL.md`（作为封装说明）
   3.（可选）一份示例输出报告（运行脚本后得到的 markdown）
3. 若对方要求“代码可读性”，建议保留：
   - `src/fluid_network/schema.py`
   - `src/fluid_network/solver.py`
   - `src/fluid_network/path_analyzer.py`
   - `scripts/run_fluid_network.py`

---

## 9. 你可以直接复制到笔试答题纸的“简短总结”

用 TOML 写出流体网络的拓扑、阻力模型，以及一组“有限工况变量”（阀门/故障状态）。`gating` 决定每个工况下边是否启用；边被禁用时用等效大阻力近似阻断，并且连通性只沿启用边做 BFS，从而避免全枚举导致的指数增长。求解器对 `junction` 节点建立稳态质量守恒：线性模型用线性方程组求解，含二次阻力时用 Newton 迭代得到压力，再回算各边流量与压差（需要速度时再计算）。最后在每个工况下结合负载阈值 `min_flow_m3s` 和 `min_pressure_pa` 给出功能 PASS/FAIL，把解析、求解和报告生成封成 Skill，输入 TOML 和工况就能直接得到对比结果。

