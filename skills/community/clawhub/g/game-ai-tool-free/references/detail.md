# 详细参考 - game-ai-tool-free

> 本文件从SKILL.md拆分而来，包含详细代码示例和扩展章节。

## 代码示例 (csharp)

```csharp
// 行为树节点状态
public enum NodeStatus { Running, Success, Failure }

// 顺序节点 (全部成功才算成功)
public class Sequence : BTNode
{
    private readonly List<BTNode> _children = new();
    private int _currentChild = 0;

    public Sequence(params BTNode[] children) => _children.AddRange(children);

    public override NodeStatus Execute()
    {
        while (_currentChild < _children.Count)
        {
            var status = _children[_currentChild].Execute();
            if (status == NodeStatus.Running) return NodeStatus.Running;
            if (status == NodeStatus.Failure)
            {
                _currentChild = 0;
                return NodeStatus.Failure;
            }
            _currentChild++;
        }
        _currentChild = 0;
        return NodeStatus.Success;
    }
}

// 选择节点 (一个成功就算成功)
public class Selector : BTNode
{
    private readonly List<BTNode> _children = new();
    private int _currentChild = 0;

    public Selector(params BTNode[] children) => _children.AddRange(children);

    public override NodeStatus Execute()
    {
        while (_currentChild < _children.Count)
        {
            var status = _children[_currentChild].Execute();
            if (status == NodeStatus.Running) return NodeStatus.Running;
            if (status == NodeStatus.Success)
            {
                _currentChild = 0;
                return NodeStatus.Success;
            }
            _currentChild++;
        }
        _currentChild = 0;
        return NodeStatus.Failure;
    }
}

// 敌人 AI 组合示例
public class EnemyAI : Node
{
    private BTNode _behaviorTree;

    public override void _Ready()
    {
        _behaviorTree = new Selector(
            // 优先攻击
            new Sequence(
                new Condition(IsPlayerInRange),
                new Condition(HasAmmo),
                new Action(Attack)
            ),
            // 追击玩家
            new Sequence(
                new Condition(CanSeePlayer),
                new Action(ChasePlayer)
            ),
            // 默认巡逻
            new Action(Patrol)
        );
    }

    public override void _Process(double delta) => _behaviorTree.Execute();
}
```

## 代码示例 (csharp)

```csharp
// 敌人状态枚举
public enum EnemyState
{
    Idle, Patrol, Chase, Attack, Flee
}

public class EnemyFSM : Node
{
    private EnemyState _currentState;
    private Dictionary<EnemyState, IState> _states;

    public override void _Ready()
    {
        _states = new Dictionary<EnemyState, IState>
        {
            [EnemyState.Idle] = new IdleState(this),
            [EnemyState.Patrol] = new PatrolState(this),
            [EnemyState.Chase] = new ChaseState(this),
            [EnemyState.Attack] = new AttackState(this),
            [EnemyState.Flee] = new FleeState(this)
        };
        ChangeState(EnemyState.Idle);
    }

    public void ChangeState(EnemyState newState)
    {
        _states[_currentState]?.Exit();
        _currentState = newState;
        _states[_currentState]?.Enter();
    }

    public override void _Process(double delta)
    {
        _states[_currentState]?.Update(delta);
    }
}

// 追击状态示例
public class ChaseState : IState
{
    private readonly EnemyFSM _fsm;
    private NavigationAgent2D _navAgent;

    public ChaseState(EnemyFSM fsm)
    {
        _fsm = fsm;
        var owner = fsm.GetParent<CharacterBody2D>();
        _navAgent = owner.GetNode<NavigationAgent2D>("NavigationAgent2D");
    }

    public void Enter()
    {
        _fsm.GetParent<CharacterBody2D>()
            .GetNode<AnimationPlayer>("AnimationPlayer").Play("run");
    }

    public void Update(double delta)
    {
        var player = GetTree().GetFirstNodeInGroup("player") as Node2D;
        if (player == null) return;

        _navAgent.TargetPosition = player.GlobalPosition;
        var owner = _fsm.GetParent<CharacterBody2D>();
        var direction = owner.ToLocal(_navAgent.GetNextPathPosition()).Normalized();
        owner.Velocity = direction * owner.Speed;
        owner.MoveAndSlide();

        float distance = owner.GlobalPosition.DistanceTo(player.GlobalPosition);
        if (distance < 50)
            _fsm.ChangeState(EnemyState.Attack);
        else if (distance > 500)
            _fsm.ChangeState(EnemyState.Patrol);
    }

    public void Exit() { _fsm.GetParent<CharacterBody2D>().Velocity = Vector2.Zero; }
}
```

