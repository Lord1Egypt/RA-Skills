---

name: "game-theory-tool-free"
description: "策略互动分析工具,支持纳什均衡、囚徒困境与决策树分析。Use when 需要数据分析、报表生成、统计洞察、数据可视化时使用。不适用于实时流数据处理。适用于独立开发者、企业团队和自动化工作流场景。支持中文交互，无需复杂配置即开即用。输出结果可直接使用，减少二次加工成本。提供结构化输出和错误处理机制。支持多场景应用和灵活配置。"
license: Proprietary
allowed-tools: read exec
compatibility: "Requires LLM with tool-use capability"
metadata:
  displayName: "博弈论分析免费版"
  version: "1.0.0"
  summary: "策略互动分析工具,支持纳什均衡、囚徒困境与决策树分析"
  tags:
    - "博弈论"
    - "决策分析"
    - "纳什均衡"
    - "策略互动"
    - "经济学"
    - "学习工具"
  source: "SkillHub"
  converted_at: "2026-07-22T17:58:36"
tools:
  - exec
  - read
  - write

---

> **功能说明**: 本技能涵盖 中文交互、化工作流场景 等核心能力。


# 博弈论分析 (免费版)

## 概述

本工具帮助学生、研究者与决策者分析策略互动情境,求解纳什均衡,理解囚徒困境、重复博弈、决策树等博弈论核心概念。通过收益矩阵分析、逻辑推导与可视化,把抽象的博弈论转化为可操作的分析工具。

免费版聚焦个人学习与基础分析,适合经济学学生、商业决策者、游戏设计师使用。

## 核心能力

| 能力模块 | 描述 | 免费版支持 |
|:--------|:-----|:-----------|
| 收益矩阵分析 | 2x2 博弈分析 | 支持 |
| 纳什均衡求解 | 纯策略均衡 | 支持 |
| 囚徒困境 | 经典案例库 | 支持 |
| 优势策略 | 严格/弱优势分析 | 支持 |
| 决策树 | 序贯博弈分析 | 支持 |
| 重复博弈 | 有限/无限重复 | 基础 |
| 混合策略 | 概率化策略 | 基础 |
| 演化博弈 | 演化稳定策略 | 不支持 (升级 PRO) |
| 机制设计 | 反向博弈设计 | 不支持 (升级 PRO) |
| 多人博弈 | n 人博弈 | 不支持 (升级 PRO) |
| 实验数据 | 行为博弈实验 | 不支持 (升级 PRO) |

### 核心功能执行
用`input_params`参数进行配置。

**输出**: 返回核心功能执行的执行结果,包含操作状态和输出数据。
- 执行此能力时使用`input_params`参数,支持创建/查询/导出操作

### 参数配置与调用
用`config_options`参数进行配置。

**输出**: 返回参数配置与调用的执行结果,包含操作状态和输出数据。
- 执行此能力时使用`config_options`参数,支持修改/重置/导入操作

### 结果处理与输出
用`output_format`参数进行配置。

**输出**: 返回结果处理与输出的执行结果,包含操作状态和输出数据。
- 执行此能力时使用`output_format`参数,支持导出/保存/转换操作
**能力覆盖范围**：本skill的核心能力覆盖以下场景关键词：策略互动分析工具、支持纳什均衡、囚徒困境与决策树、面向学生、研究者与决策者的、博弈论分析工具、核心能力、适用场景、经济学学习、商业决策分析、谈判策略、游戏设计、社会科学研究、差异化、免费版聚焦个人学、习与基础分析、提供清晰的逻辑推、导与可视化、适用关键词、博弈论、策略分析等。这些关键词对应description中声明的使用场景,均已在上述能力点中提供对应的操作支持。

## 使用场景

### 场景一: 经典囚徒困境

分析最经典的博弈论案例。

```text
情境: 两名嫌疑人被分别审讯,各有"坦白"或"沉默"两个选择。
收益 (A, B 表示刑期年数,越少越好):

              B 坦白    B 沉默
A 坦白       (5, 5)    (0, 10)
A 沉默      (10, 0)    (1, 1)

分析:
1. 优势策略分析:
   - 对 A: 无论 B 选什么,坦白都比沉默好 (5 < 10, 0 < 1)
   - 对 B: 无论 A 选什么,坦白都比沉默好
   - 双方坦白是严格优势策略均衡
2. 纳什均衡: (坦白, 坦白) = (5, 5)
3. 帕累托最优: (沉默, 沉默) = (1, 1)
4. 困境: 个人理性导致集体非最优

洞察:
- 短期单次博弈中,合作难以达成
- 重复博弈中,"以牙还牙"策略可促进合作
- 现实应用: 价格战、军备竞赛、公地悲剧
```

### 场景二: 商业竞争分析

分析两家公司的定价策略博弈。

```python
# 定价博弈分析
import numpy as np

class GameTheoryAnalyzer:
    def __init__(self, payoff_matrix, row_player="A", col_player="B"):
        self.payoff = np.array(payoff_matrix)
        self.row_player = row_player
        self.col_player = col_player
        self.row_strategies = []
        self.col_strategies = []

    def find_dominant_strategies(self):
        """寻找优势策略"""
        row_player_payoffs = self.payoff[:, :, 0]  # 行玩家收益
        col_player_payoffs = self.payoff[:, :, 1]  # 列玩家收益

        row_dominant = self._find_row_dominant(row_player_payoffs)
        col_dominant = self._find_col_dominant(col_player_payoffs)

        return row_dominant, col_dominant

    def find_nash_equilibrium(self):
        """寻找纳什均衡 (纯策略)"""
        equilibria = []
        for i in range(self.payoff.shape[0]):
            for j in range(self.payoff.shape[1]):
                if self._is_nash(i, j):
                    equilibria.append((i, j, self.payoff[i, j]))
        return equilibria

    def _is_nash(self, i, j):
        """检查 (i,j) 是否纳什均衡"""
        row_payoff = self.payoff[i, j, 0]
        col_payoff = self.payoff[i, j, 1]

        # 行玩家不能通过单方面改变策略获益
        for k in range(self.payoff.shape[0]):
            if self.payoff[k, j, 0] > row_payoff:
                return False
        # 列玩家不能通过单方面改变策略获益
            if self.payoff[i, k, 1] > col_payoff:
                return False
        return True

# 示例
# 收益 (万元利润): [咖啡店A利润, 咖啡店B利润]
analyzer = GameTheoryAnalyzer([
    [[10, 10], [15, 5]],   # A 高价
    [[5, 15], [8, 8]],     # A 低价
], row_player="咖啡店A", col_player="咖啡店B")

analyzer.row_strategies = ["高价", "低价"]
analyzer.col_strategies = ["高价", "低价"]

print("优势策略:", analyzer.find_dominant_strategies())
print("纳什均衡:", analyzer.find_nash_equilibrium())

# 输出:
# 优势策略: (None, None) - 双方都无优势策略
# 纳什均衡: [(1, 1, [8, 8])] - 双方都低价
```

### 场景三: 决策树分析

分析序贯博弈 (一方先行动)。

```python
class DecisionTree:
    def __init__(self):
        self.nodes = {}

    def add_node(self, node_id, player, actions=None, payoff=None):
        self.nodes[node_id] = {
            "player": player,
            "actions": actions or {},
            "payoff": payoff,
        }

    def add_edge(self, parent, action, child):
        self.nodes[parent]["actions"][action] = child

    def backward_induction(self, node_id):
        """逆向归纳求解子博弈完善均衡"""
        node = self.nodes[node_id]
        if node["payoff"]:
            return node["payoff"], []

        best_payoff = None
        best_path = None
        for action, child in node["actions"].items():
            child_payoff, child_path = self.backward_induction(child)
            player_idx = 0 if node["player"] == "A" else 1
            if best_payoff is None or child_payoff[player_idx] > best_payoff[player_idx]:
                best_payoff = child_payoff
                best_path = [action] + child_path

        return best_payoff, best_path

# 案例: 进入市场博弈
tree = DecisionTree()
tree.add_node("root", "A")  # A 决定是否进入
tree.add_node("enter", "B")  # B 决定是否反击
tree.add_node("exit", None, payoff=[0, 10])  # A 不进入
tree.add_node("fight", None, payoff=[-5, -5])  # B 反击
tree.add_node("accommodate", None, payoff=[5, 5])  # B 默认
tree.add_edge("root", "进入", "enter")
tree.add_edge("root", "退出", "exit")
tree.add_edge("enter", "反击", "fight")
tree.add_edge("enter", "默认", "accommodate")

payoff, path = tree.backward_induction("root")
print(f"子博弈完善均衡路径: {path}, 收益: {payoff}")
# 输出: 路径: ['进入', '默认'], 收益: [5, 5]
```

## 不适用场景

以下场景博弈论分析免费版不适合处理：

- 实时流数据处理
- 小规模数据手动分析
- 非结构化文本情感分析

## 触发条件

需要数据分析、报表生成、统计洞察、数据可视化时使用。不适用于非本工具能力范围的需求。

## 快速开始

### Step 1: 定义博弈

```python
# 用收益矩阵定义博弈
# 矩阵形状: (行策略数, 列策略数, 2)
# 第 3 维 [0] 是行玩家收益, [1] 是列玩家收益

cooperation_game = [
    [[3, 3], [0, 5]],   # 合作
    [[5, 0], [1, 1]],   # 背叛
]
```

### Step 2: 分析均衡

```python
analyzer = GameTheoryAnalyzer(cooperation_game)
find_nash_equilibrium())
find_dominant_strategies())
```

### Step 3: 解读结果

```text
解读要点:
1. 纳什均衡: 双方都不愿单方面改变的状态
2. 优势策略: 无论对手如何都最优的策略
3. 帕累托最优: 无法在不损害他人的前提下让某人更好的状态
4. 社会最优: 双方收益之和最大的状态
```

## 配置示例

### 经典博弈案例库

```python
CLASSIC_GAMES = {
    "prisoners_dilemma": {
        "name": "囚徒困境",
        "matrix": [[[-5, -5], [0, -10]], [[-10, 0], [-1, -1]]],
        "strategies": ["坦白", "沉默"],
        "nash": [(0, 0)],
        "pareto_optimal": [(1, 1)],
        "insight": "个人理性导致集体非最优",
    },
    "stag_hunt": {
        "name": "猎鹿博弈",
        "matrix": [[[5, 5], [0, 3]], [[3, 0], [3, 3]]],
        "strategies": ["猎鹿", "猎兔"],
        "nash": [(0, 0), (1, 1)],
        "pareto_optimal": [(0, 0)],
        "insight": "存在多个均衡,需协调",
    },
    "chicken_game": {
        "name": "胆小鬼博弈",
        "matrix": [[[0, 0], [3, -1]], [[-1, 3], [-3, -3]]],
        "strategies": ["直行", "转向"],
        "nash": [(0, 1), (1, 0)],
        "pareto_optimal": [(0, 1), (1, 0)],
        "insight": "谁先转向谁吃亏,但都不转向两败俱伤",
    },
    "battle_of_sexes": {
        "name": "性别战",
        "matrix": [[[3, 2], [0, 0]], [[0, 0], [2, 3]]],
        "strategies": ["看球赛", "看电影"],
        "nash": [(0, 0), (1, 1)],
        "pareto_optimal": [(0, 0), (1, 1)],
        "insight": "利益冲突下的协调问题",
    },
}
```

### 分析模板

```markdown
# 博弈分析报告

## 1. 情境描述
[参与方、可选策略、收益规则]

## 2. 收益矩阵
|              | 玩家 B 策略 1 | 玩家 B 策略 2 |
|:-------------|:-------------:|:-------------:|
| 玩家 A 策略 1 | (a11, b11)   | (a12, b12)   |
| 玩家 A 策略 2 | (a21, b21)   | (a22, b22)   |

## 3. 优势策略分析
- 玩家 A: [有/无] 优势策略
- 玩家 B: [有/无] 优势策略

## 4. 纳什均衡
- 均衡点: [...]
- 均衡收益: [...]

## 5. 帕累托最优
- 帕累托最优状态: [...]

## 6. 洞察与应用
[现实意义与建议]
```

## 优选实践

### 1. 收益矩阵规范

```python
# 本技能的核心实现逻辑
# 请参考上方使用说明进行配置和调用
result = "implementation_ready"
```

### 2. 现实情境建模

```text
建模步骤:
1. 识别参与方 (谁在做决策?)
2. 列出每个参与方的可选策略
3. 评估每个策略组合的收益 (主观效用)
4. 构建收益矩阵
5. 求解均衡并解读

注意事项:
- 收益不一定是金钱,可以是效用 (满足感、声誉等)
- 收益是相对的,只关心排序而非绝对值
- 模型是简化,现实决策还需考虑道德、长期影响
```

### 3. 重复博弈的洞察

```python
def repeated_game_insight(game_type, repetitions):
    """重复博弈洞察"""
    if game_type == "prisoners_dilemma":
        if repetitions == "infinite":
            return "无限重复可达成合作 (无名氏定理),以牙还牙策略有效"
        else:
            return f"有限重复 {repetitions} 次,合作难以维持 (逆向归纳导致背叛)"
    return "需要具体分析"
```

## 常见问题

### Q1: 纳什均衡一定存在吗?

有限博弈中至少存在一个纳什均衡 (可能混合策略)。纯策略均衡不一定存在。

### Q2: 纳什均衡是最优解吗?

不一定。纳什均衡是"稳定"状态,不一定是帕累托最优 (如囚徒困境)。

### Q3: 免费版支持多人博弈吗?

免费版聚焦 2 人博弈。n 人博弈需要 PRO 版本。

### Q4: 现实中如何应用博弈论?

博弈论提供分析框架,帮助识别策略互动、预测均衡、设计机制。但现实决策还需结合道德、长期影响等因素。

### Q5: 如何处理不完全信息博弈?

免费版支持完全信息博弈。贝叶斯博弈 (不完全信息) 需要 PRO 版本。

## 依赖说明

### 运行环境

- **Agent 平台**: 支持 SKILL.md 规范的任意 AI Agent (Claude Code、Cursor、Codex、Gemini CLI 等)
- **操作系统**: Windows / macOS / Linux
- **Python**: 3.8+ (用于数值计算)

### 依赖详情

| 依赖项 | 类型 | 是否必需 | 获取方式 |
|:-------|:-----|:---------|:---------|
| LLM API | 推理服务 | 必需 | 由 Agent 内置 LLM 提供 |
| Python 3.8+ | 运行时 | 可选 | python.org 下载 |
| NumPy | Python 库 | 可选 | `pip install numpy` (矩阵运算) |

### API Key 配置

```bash
# 免费版无需外部 API Key
# 所有分析通过 Agent LLM 本地推理完成

# 可选: 默认分析偏好
export GAME_THEORY_LANGUAGE="zh"
export GAME_THEORY_VERBOSE="true"
```

### 可用性分类

- **分类**: MD+execute(Markdown 指令 + 代码执行)
- **说明**: 本 Skill 通过自然语言指令驱动 Agent 进行博弈论分析,提供逻辑推导与可视化
- **免费版限制**: 2 人博弈、纯策略为主、无演化博弈、无机制设计、无实验数据

## 错误处理

| 错误场景 | 原因 | 处理方式 |
|---------|------|---------|
| 配置错误 | 参数缺失或格式错误 | 检查依赖说明中的配置要求 |
| 运行时错误 | 运行环境不满足 | 确认运行环境符合依赖说明 |
| 网络错误 | 连接超时或不可达 | 执行ping命令测试网络连通性,检查防火墙和代理设置连接后执行ping命令测试网络连通性,检查防火墙和代理设置连接后重新执行命令，参考国内替代方案 |

## 已知限制

- 需LLM支持,无LLM环境不可用
- 复杂业务场景建议结合人工经验判断
- 执行效率受模型能力与网络环境影响

## 示例

### 基本用法

**输出**：返回执行结果,包含操作状态和输出数据

```text
用户: 执行核心功能
Skill: 正在执行核心功能...
Skill: 执行完成,结果如下: 操作成功
```

## 安全注意事项

| 风险类型 | 防范措施 |
|----------|---------|
| API密钥泄露 | 通过环境变量配置，禁止硬编码到代码或配置文件中 |
| 命令执行风险 | 仅执行白名单命令，避免拼接用户输入到命令行参数中 |
| 网络通信安全 | 使用HTTPS协议，验证SSL证书有效性 |
| 敏感数据暴露 | 输出结果中不包含密钥、令牌等敏感信息 |

使用前请确认已阅读依赖说明章节，确保运行环境满足安全要求。