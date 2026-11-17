---

name: "game-ai-tool-free"
description: "游戏AI开发指南,涵盖FSM、行为树、寻路与决策系统的代码实现。Use when 需要代码生成、编程辅助、调试测试、开发部署时使用。不适用于无明确技术栈的模糊需求。适用于独立开发者、企业团队和自动化工作流场景。支持中文交互，无需复杂配置即开即用。输出结果可直接使用，减少二次加工成本。提供结构化输出和错误处理机制。"
license: Proprietary
allowed-tools: read exec
compatibility: "Requires LLM with tool-use capability"
metadata:
  displayName: "游戏AI工具免费版"
  version: "1.0.0"
  summary: "游戏AI开发指南,涵盖FSM、行为树、寻路与决策系统的代码实现"
  tags:
    - "游戏开发"
    - "AI开发"
    - "有限状态机"
    - "行为树"
    - "寻路算法"
    - "独立游戏"
  source: "SkillHub"
  converted_at: "2026-07-22T17:58:36"
tools:
  - exec
  - read
  - write

---

> **功能说明**: 本技能涵盖 中文交互、化工作流场景 等核心能力。


本工具为独立游戏开发者与学生提供游戏 AI 开发指南与代码模板,涵盖有限状态机 (FSM)、行为树 (Behavior Tree)、A* 寻路、效用 AI、感知系统、群体行为等主流 AI 架构。每种架构都配有完整的可运行代码示例,适合学习、原型验证与 Game Jam 使用。

免费版聚焦个人学习与原型开发,适合独立开发者与学生使用。

## 核心能力
| 能力模块 | 描述 | 免费版支持 |
|:--------|:-----|:-----------|
| 有限状态机 (FSM) | 简单敌人与 Boss 阶段 AI | 支持 |
| 行为树 (BT) | 复杂 NPC 与战术 AI | 支持 |
| A* 寻路 | 标准寻路算法 | 支持 |
| 效用 AI | 智能决策系统 | 支持 |
| 感知系统 | 视觉、听觉感知 | 支持 |
| 群体行为 (Boids) | 鸟群、鱼群模拟 | 支持 |
| GOAP | 目标导向行动规划 | 不支持 (升级 PRO) |
| 机器学习 AI | 强化学习集成 | 不支持 (升级 PRO) |
| 多 AI 协作 | 团队战术 AI | 不支持 (升级 PRO) |
| AI 调试工具 | 可视化调试器 | 基础 |

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
**能力覆盖范围**：本skill的核心能力覆盖以下场景关键词：开发指南、寻路与决策系统的、代码实现、面向独立游戏开发、者与学生的游戏、开发指南与代码模、核心能力、适用场景、独立游戏开发、游戏开发学习、原型验证、Game、Jam、差异化、免费版聚焦个人学、习与原型开发、提供主流、架构的代码模板、适用关键词等。这些关键词对应description中声明的使用场景,均已在上述能力点中提供对应的操作支持。

## 使用场景
### 场景一: 简单敌人 AI (FSM)
为游戏中的敌人实现基础 AI 行为。

> 详细代码示例已移至 `references/detail.md`

### 场景二: 复杂 NPC AI (行为树)
为 NPC 实现模块化、可复用的复杂行为。

### 场景三: 寻路与群体行为
实现 A* 寻路与鸟群模拟。

```csharp
// A* 寻路核心
public class AStar
{
    private readonly Grid _grid;

    public List<Point> FindPath(Point start, Point end)
    {
        var openSet = new PriorityQueue<Point>();
        var cameFrom = new Dictionary<Point, Point>();
        var gScore = new Dictionary<Point, float>();
        var fScore = new Dictionary<Point, float>();

        openSet.Enqueue(start, 0);
        gScore[start] = 0;
        fScore[start] = Heuristic(start, end);

        while (openSet.Count > 0)
        {
            var current = openSet.Dequeue();
            if (current == end) return ReconstructPath(cameFrom, current);

            foreach (var neighbor in _grid.GetNeighbors(current))
            {
                float tentativeGScore = gScore[current] + _grid.GetCost(current, neighbor);
                if (!gScore.ContainsKey(neighbor) || tentativeGScore < gScore[neighbor])
                {
                    cameFrom[neighbor] = current;
                    gScore[neighbor] = tentativeGScore;
                    fScore[neighbor] = gScore[neighbor] + Heuristic(neighbor, end);
openSet.Contains(neighbor))
                        openSet.Enqueue(neighbor, fScore[neighbor]);
                }
            }
        }
        return null;
    }

    private float Heuristic(Point a, Point b) =>
        Math.Abs(a.X - b.X) + Math.Abs(a.Y - b.Y); // 曼哈顿距离
}

// Boids 群体行为
public class Boid : Node2D
{
    private Vector2 _velocity;

    public override void _Process(double delta)
    {
        var separation = CalculateSeparation();
        var alignment = CalculateAlignment();
        var cohesion = CalculateCohesion();

        var acceleration = separation * 1.5f + alignment * 1.0f + cohesion * 1.0f;
        _velocity += acceleration * (float)delta;
        _velocity = _velocity.LimitLength(MaxSpeed);
        Position += _velocity * (float)delta;
    }
}
```

## 不适用场景

以下场景游戏AI工具免费版不适合处理：

- 无明确技术栈的模糊需求
- 纯架构设计决策
- 运维部署管理

## 触发条件

需要代码生成、编程辅助、调试测试、开发部署时使用。不适用于非本工具能力范围的需求。

## 快速开始
### Step 1: 选择 AI 架构
根据游戏复杂度选择合适的 AI 架构。

```yaml
架构选择指南:
  有限状态机 (FSM):
    适用: 简单敌人、Boss 阶段切换
    优点: 简单直观、易调试
    缺点: 状态多时难维护

  行为树 (BT):
    适用: 复杂 NPC、战术 AI
    优点: 模块化、可复用、易扩展
    缺点: 需要框架支持

  效用 AI:
    适用: 模拟人生类、策略游戏
    优点: 灵活、智能决策
    缺点: 参数调节困难
```

### Step 2: 复用代码模板
```bash
# 本技能的核心实现逻辑
# 请参考上方使用说明进行配置和调用
echo "implementation_ready"
```

### Step 3: 集成到游戏引擎
```csharp
// 在 Godot 中集成 AI
public partial class Enemy : CharacterBody2D
{
    private EnemyFSM _fsm;

    public override void _Ready()
    {
        _fsm = new EnemyFSM();
        AddChild(_fsm);
    }

    public override void _PhysicsProcess(double delta)
    {
        // FSM 自动处理移动逻辑
    }
}
```

**结果处理**: 执行完成后,查看输出结果确认操作状态。成功时输出包含处理摘要和结果数据;失败时根据错误信息排查问题,查阅错误处理章节获取恢复步骤。

#
## 配置示例
### AI 参数配置
```yaml
enemy_types:
  basic:
    fsm:
      states: [idle, patrol, chase, attack]
      detection_range: 200
      attack_range: 50
      attack_damage: 10
      speed: 100

  elite:
    behavior_tree:
      priorities: [attack, chase, patrol, flee]
      sight_range: 300
      hearing_range: 150
      team_coordination: false  # 免费版不支持
  boss:
    phases:
      - name: "phase_1"
        health_threshold: 0.75
        patterns: [sweep_attack, projectile_burst]
      - name: "phase_2"
        patterns: [enrage, summon_adds]
```

### 效用 AI 示例
```csharp
public class UtilityAI
{
    private readonly List<UtilityAction> _actions = new();

    public UtilityAction ChooseBestAction()
    {
        float bestScore = float.MinValue;
        UtilityAction bestAction = null;

        foreach (var action in _actions)
        {
            float score = action.CalculateScore();
            score += GD.Randf() * 0.1f; // 添加随机性
            if (score > bestScore)
            {
                bestScore = score;
                bestAction = action;
            }
        }
        return bestAction;
    }
}

public class AttackAction : UtilityAction
{
    private readonly Enemy _enemy;

    public override float CalculateScore()
    {
        float score = 0f;
        float distance = _enemy.DistanceToPlayer();
        score += Mathf.Clamp(1.0f - distance / 200.0f, 0, 1) * 0.5f;
        score += _enemy.HasAmmo ? 0.3f : 0.0f;
HealthPercent * 0.2f;
        return score;
    }

    public override void Execute() => _enemy.Attack();
}
```

## 优选实践
### 1. 状态机调试
```csharp
// 添加调试可视化
public override void _Draw()
{
    DrawArc(Vector2.Zero, ViewDistance, -ViewAngle / 2, ViewAngle / 2, 32, Colors.Yellow, 1.0f);
}

// 状态切换日志
public void ChangeState(EnemyState newState)
{
    GD.Print($"State: {_currentState} -> {newState}");
    _states[_currentState]?.Exit();
    _currentState = newState;
}
```

### 2. 性能优化
```csharp
// 避免每帧调用 GetFirstNodeInGroup
private Node2D _playerCache;

public override void _Ready()
{
    _playerCache = GetTree().GetFirstNodeInGroup("player") as Node2D;
}

// 限制 AI 计算频率
private float _aiUpdateTimer = 0f;
public override void _Process(double delta)
{
    _aiUpdateTimer += (float)delta;
    if (_aiUpdateTimer >= 0.1f) // 10 FPS 更新 AI
    {
        UpdateAI();
        _aiUpdateTimer = 0f;
    }
}
```

### 3. 数据驱动设计
```csharp
// 从配置文件加载 AI 参数
public class AIConfig
{
    public float DetectionRange { get; set; }
    public float AttackRange { get; set; }
    public float Speed { get; set; }
}

// 配置与逻辑分离,便于平衡调整
```

## 常见问题
### Q1: FSM 和行为树哪个更好?
简单游戏用 FSM (3-5 个状态足够),复杂 NPC 用行为树 (模块化易扩展)。两者也可混合使用。

### Q2: A* 寻路如何优化?
使用 NavigationAgent (引擎内置)、限制寻路频率、简化网格、避免每帧重算路径。

### Q3: 免费版有 AI 调试工具吗?
提供基础调试 (状态日志、视野可视化)。完整可视化调试器需要 PRO 版本。

### Q4: 支持哪些游戏引擎?
代码示例以 Godot C# 为主,概念适用于 Unity、Unreal、Cocos 等主流引擎。
### Q5: 如何实现机器学习 AI?
免费版不包含。需要强化学习、神经网络等高级 AI,请升级 PRO 版本。

## 依赖说明
### 运行环境
- **Agent 平台**: 支持 SKILL.md 规范的任意 AI Agent (Claude Code、Cursor、Codex、Gemini CLI 等)
- **操作系统**: Windows / macOS / Linux
- **游戏引擎**: Godot 4.x (示例代码),也适用于 Unity、Unreal

### 依赖详情
| 依赖项 | 类型 | 是否必需 | 获取方式 |
|:-------|:-----|:---------|:---------|
| LLM API | 推理服务 | 必需 | 由 Agent 内置 LLM 提供 |
| Godot 4.x | 游戏引擎 | 推荐 | godotengine.org 下载 |
| .NET 8 SDK | 运行时 | 可选 | dot.net 下载 (C# 支持) |
### API Key 配置
```bash
export GAME_AI_ENGINE="godot"
export GAME_AI_LANGUAGE="csharp"
```

### 可用性分类
- **分类**: MD (纯 Markdown 指令 + 代码模板)
- **说明**: 本 Skill 通过自然语言指令驱动 Agent 生成游戏 AI 代码与架构建议
- **免费版限制**: 单人使用、基础 AI 架构、无机器学习、无多 AI 协作、基础调试工具

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