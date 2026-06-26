# 游戏开发最佳实践总结

> 整理日期：2026-05-25
> 归属：full-stack-architect技能

---

## 一、游戏开发技术选型

### 1.1 游戏引擎选择

**主流引擎：**
- **Unity**：C#、跨平台、2D/3D
- **Unreal Engine**：C++、高品质3D、蓝图系统
- **Godot**：GDScript、开源、轻量级
- **GameMaker Studio**：GML、2D游戏

**选型建议：**
- 2D游戏 → Unity、Godot、GameMaker
- 3D游戏 → Unity、Unreal Engine
- 独立开发 → Godot、GameMaker
- 大型项目 → Unity、Unreal Engine

---

### 1.2 技术栈搭配

**前端/客户端：**
- **Unity**：C#、Unity Editor、Asset Store
- **Unreal**：C++、Blueprint、UE Editor
- **Web游戏**：HTML5、Canvas、WebGL、Phaser

**后端/服务器：**
- **游戏服务器**：Node.js、C++、Go
- **数据库**：PostgreSQL、MongoDB、Redis
- **网络**：WebSocket、TCP/UDP、RPC

**工具链：**
- **版本控制**：Git、Perforce
- **构建**：Jenkins、GitHub Actions
- **测试**：Unity Test Framework、Unreal Automation Tool

---

## 二、Unity 最佳实践

### 2.1 项目结构

**推荐结构：**

```
Assets/
├── Scripts/            # C#脚本
│   ├── Managers/       # 管理类
│   ├── Systems/        # 系统类
│   ├── UI/             # UI脚本
│   ├── Utils/          # 工具类
│   └── Models/         # 数据模型
├── Prefabs/            # 预制体
├── Scenes/             # 场景
├── Resources/          # 资源
├── Materials/          # 材质
├── Textures/           # 纹理
├── Audio/              # 音频
└── Plugins/            # 插件
```

**命名规范：**
- 脚本：PascalCase（PlayerController.cs）
- 变量：camelCase
- 常量：UPPERCASE
- 方法：PascalCase
- 私有字段：_camelCase

---

### 2.2 性能优化

**内存管理：**
- 对象池模式
- 避免频繁创建和销毁对象
- 合理使用缓存
- 监控内存使用

**对象池示例：**

```csharp
public class ObjectPool<T> where T : MonoBehaviour
{
    private Queue<T> pool = new Queue<T>();
    private T prefab;
    private Transform parent;

    public ObjectPool(T prefab, int initialSize = 10, Transform parent = null)
    {
        this.prefab = prefab;
        this.parent = parent;
        
        for (int i = 0; i < initialSize; i++)
        {
            T obj = GameObject.Instantiate(prefab, parent);
            obj.gameObject.SetActive(false);
            pool.Enqueue(obj);
        }
    }

    public T Get()
    {
        if (pool.Count == 0)
        {
            T obj = GameObject.Instantiate(prefab, parent);
            obj.gameObject.SetActive(false);
            pool.Enqueue(obj);
        }

        T item = pool.Dequeue();
        item.gameObject.SetActive(true);
        return item;
    }

    public void Return(T item)
    {
        item.gameObject.SetActive(false);
        pool.Enqueue(item);
    }
}
```

**渲染优化：**
- LOD（Level of Detail）
- 批处理（Batching）
-  occlusion culling
- 合理设置相机视锥体

**示例：**

```csharp
// 启用 occlusion culling
UnityEngine.Rendering.OcclusionCullingSettings occlusionSettings = GetComponent<UnityEngine.Rendering.OcclusionCullingSettings>();
occlusionSettings.enabled = true;

// 设置 LOD
LODGroup lodGroup = GetComponent<LODGroup>();
LOD[] lods = new LOD[3];

lods[0] = new LOD(0.8f, new Renderer[] { highQualityRenderer });
lods[1] = new LOD(0.4f, new Renderer[] { mediumQualityRenderer });
lods[2] = new LOD(0.1f, new Renderer[] { lowQualityRenderer });

lodGroup.SetLODs(lods);
```

---

### 2.3 输入系统

**新输入系统：**

```csharp
using UnityEngine.InputSystem;

public class PlayerInputHandler : MonoBehaviour
{
    private PlayerInput playerInput;
    private InputAction moveAction;
    private InputAction jumpAction;

    private void Awake()
    {
        playerInput = GetComponent<PlayerInput>();
        moveAction = playerInput.actions["Move"];
        jumpAction = playerInput.actions["Jump"];

        jumpAction.performed += OnJump;
    }

    private void Update()
    {
        Vector2 moveInput = moveAction.ReadValue<Vector2>();
        // 处理移动
    }

    private void OnJump(InputAction.CallbackContext context)
    {
        if (context.performed)
        {
            // 处理跳跃
        }
    }

    private void OnDestroy()
    {
        jumpAction.performed -= OnJump;
    }
}
```

---

### 2.4 物理系统

**碰撞检测：**

```csharp
private void OnCollisionEnter(Collision collision)
{
    if (collision.gameObject.CompareTag("Enemy"))
    {
        // 处理与敌人的碰撞
    }
}

private void OnTriggerEnter(Collider other)
{
    if (other.CompareTag("Collectible"))
    {
        // 处理收集物
        other.gameObject.SetActive(false);
    }
}
```

**射线检测：**

```csharp
void Update()
{
    Ray ray = Camera.main.ScreenPointToRay(Input.mousePosition);
    RaycastHit hit;

    if (Physics.Raycast(ray, out hit, 100f))
    {
        Debug.DrawLine(ray.origin, hit.point, Color.red);
        // 处理射线检测结果
    }
}
```

---

### 2.5 UI 系统

**UGUI 最佳实践：**
- 使用 Canvas 分组
- 合理设置渲染模式
- 使用 TextMeshPro 替代 Text
- 避免过度使用 Canvas

**示例：**

```csharp
using UnityEngine.UI;
using TMPro;

public class UIManager : MonoBehaviour
{
    [SerializeField] private TextMeshProUGUI scoreText;
    [SerializeField] private Button pauseButton;

    private void Start()
    {
        pauseButton.onClick.AddListener(OnPauseButtonClicked);
    }

    public void UpdateScore(int score)
    {
        scoreText.text = "Score: " + score.ToString();
    }

    private void OnPauseButtonClicked()
    {
        // 处理暂停
    }
}
```

---

### 2.6 场景管理

**异步加载：**

```csharp
using UnityEngine.SceneManagement;
using System.Collections;

public class SceneLoader : MonoBehaviour
{
    public async void LoadSceneAsync(string sceneName)
    {
        var asyncOperation = SceneManager.LoadSceneAsync(sceneName);
        
        while (!asyncOperation.isDone)
        {
            float progress = asyncOperation.progress;
            // 更新加载进度条
            await Task.Yield();
        }
    }

    public void LoadSceneAdditive(string sceneName)
    {
        SceneManager.LoadScene(sceneName, LoadSceneMode.Additive);
    }

    public void UnloadScene(string sceneName)
    {
        SceneManager.UnloadSceneAsync(sceneName);
    }
}
```

---

### 2.7 网络 multiplayer

**UNET 示例：**

```csharp
using UnityEngine.Networking;

public class PlayerController : NetworkBehaviour
{
    [SyncVar] private Vector3 syncPosition;

    private void Update()
    {
        if (isLocalPlayer)
        {
            // 本地玩家移动
            transform.Translate(Input.GetAxis("Horizontal") * Time.deltaTime * 5f, 0, 0);
            CmdSyncPosition(transform.position);
        }
        else
        {
            // 同步其他玩家位置
            transform.position = Vector3.Lerp(transform.position, syncPosition, 0.1f);
        }
    }

    [Command]
    private void CmdSyncPosition(Vector3 position)
    {
        syncPosition = position;
    }
}
```

---

## 三、Unreal Engine 最佳实践

### 3.1 项目结构

**推荐结构：**

```
ProjectName/
├── Content/
│   ├── Blueprints/      # 蓝图
│   ├── C++/             # C++代码
│   ├── Materials/       # 材质
│   ├── Meshes/          # 模型
│   ├── Textures/        # 纹理
│   ├── Audio/           # 音频
│   ├── Levels/          # 关卡
│   └── UI/              # 界面
├── Source/
│   ├── ProjectName/     # 项目代码
│   └── ProjectName.Target.cs
└── ProjectName.uproject
```

**命名规范：**
- 类：PascalCase（ACharacter.h）
- 变量：camelCase
- 方法：PascalCase
- 蓝图：BP_前缀
- 材质：M_前缀
- 纹理：T_前缀

---

### 3.2 C++ 与蓝图

**C++ 示例：**

```cpp
// PlayerCharacter.h
#pragma once

#include "CoreMinimal.h"
#include "GameFramework/Character.h"
#include "PlayerCharacter.generated.h"

UCLASS()
class PROJECTNAME_API APlayerCharacter : public ACharacter
{
    GENERATED_BODY()

public:
    APlayerCharacter();

protected:
    virtual void BeginPlay() override;

public:
    virtual void Tick(float DeltaTime) override;
    virtual void SetupPlayerInputComponent(class UInputComponent* PlayerInputComponent) override;

    UFUNCTION(BlueprintCallable, Category = "Player")
    void Jump();

private:
    UPROPERTY(EditAnywhere, BlueprintReadOnly, Category = "Movement", meta = (AllowPrivateAccess = "true"))
    float MovementSpeed;

    void MoveForward(float Value);
    void MoveRight(float Value);
};

// PlayerCharacter.cpp
#include "PlayerCharacter.h"

APlayerCharacter::APlayerCharacter()
{
    PrimaryActorTick.bCanEverTick = true;
    MovementSpeed = 600.0f;
}

void APlayerCharacter::BeginPlay()
{
    Super::BeginPlay();
}

void APlayerCharacter::Tick(float DeltaTime)
{
    Super::Tick(DeltaTime);
}

void APlayerCharacter::SetupPlayerInputComponent(UInputComponent* PlayerInputComponent)
{
    Super::SetupPlayerInputComponent(PlayerInputComponent);
    
    PlayerInputComponent->BindAxis("MoveForward", this, &APlayerCharacter::MoveForward);
    PlayerInputComponent->BindAxis("MoveRight", this, &APlayerCharacter::MoveRight);
    PlayerInputComponent->BindAction("Jump", IE_Pressed, this, &APlayerCharacter::Jump);
}

void APlayerCharacter::MoveForward(float Value)
{
    if (Value != 0.0f)
    {
        AddMovementInput(GetActorForwardVector(), Value * MovementSpeed * GetWorld()->GetDeltaSeconds());
    }
}

void APlayerCharacter::MoveRight(float Value)
{
    if (Value != 0.0f)
    {
        AddMovementInput(GetActorRightVector(), Value * MovementSpeed * GetWorld()->GetDeltaSeconds());
    }
}

void APlayerCharacter::Jump()
{
    Super::Jump();
}
```

**蓝图最佳实践：**
- 使用事件驱动
- 合理使用蓝图接口
- 避免过度复杂的蓝图
- 性能关键部分使用C++

---

### 3.3 物理与碰撞

**碰撞检测：**

```cpp
// 在Actor类中
UFUNCTION()
void OnCollisionBegin(UPrimitiveComponent* OverlappedComponent, AActor* OtherActor, UPrimitiveComponent* OtherComp, int32 OtherBodyIndex, bool bFromSweep, const FHitResult& SweepResult);

UFUNCTION()
void OnCollisionEnd(UPrimitiveComponent* OverlappedComponent, AActor* OtherActor, UPrimitiveComponent* OtherComp, int32 OtherBodyIndex);

// 在BeginPlay中
void AMyActor::BeginPlay()
{
    Super::BeginPlay();
    
    UPrimitiveComponent* CollisionComponent = GetCollisionComponent();
    if (CollisionComponent)
    {
        CollisionComponent->OnComponentBeginOverlap.AddDynamic(this, &AMyActor::OnCollisionBegin);
        CollisionComponent->OnComponentEndOverlap.AddDynamic(this, &AMyActor::OnCollisionEnd);
    }
}

void AMyActor::OnCollisionBegin(UPrimitiveComponent* OverlappedComponent, AActor* OtherActor, UPrimitiveComponent* OtherComp, int32 OtherBodyIndex, bool bFromSweep, const FHitResult& SweepResult)
{
    if (OtherActor->ActorHasTag("Enemy"))
    {
        // 处理与敌人的碰撞
    }
}
```

---

### 3.4 UI 系统

**UMG 示例：**

```cpp
// 在PlayerController中
#include "Blueprint/UserWidget.h"
#include "MyHUDWidget.h"

class AMyPlayerController : public APlayerController
{
    UPROPERTY()
    UMyHUDWidget* HUDWidget;

protected:
    virtual void BeginPlay() override;
};

void AMyPlayerController::BeginPlay()
{
    Super::BeginPlay();
    
    // 创建HUD
    HUDWidget = CreateWidget<UMyHUDWidget>(this, HUDWidgetClass);
    if (HUDWidget)
    {
        HUDWidget->AddToViewport();
    }
}
```

**蓝图UI：**
- 使用布局系统
- 合理设置ZOrder
- 使用异步加载
- 避免过度绘制

---

### 3.5 性能优化

**LOD 示例：**

```cpp
// 在Actor类中
UPROPERTY(EditAnywhere, Category = "LOD")
TArray<UStaticMesh*> LODMeshes;

UPROPERTY(EditAnywhere, Category = "LOD")
TArray<float> LODDistances;

void AMyActor::UpdateLOD()
{
    APlayerCameraManager* CameraManager = UGameplayStatics::GetPlayerCameraManager(GetWorld(), 0);
    if (!CameraManager) return;
    
    FVector CameraLocation = CameraManager->GetCameraLocation();
    float Distance = FVector::Dist(CameraLocation, GetActorLocation());
    
    int32 LODIndex = 0;
    for (int32 i = 0; i < LODDistances.Num(); i++)
    {
        if (Distance > LODDistances[i])
        {
            LODIndex = i + 1;
        }
    }
    
    if (LODIndex < LODMeshes.Num())
    {
        UStaticMeshComponent* MeshComponent = GetMesh();
        if (MeshComponent)
        {
            MeshComponent->SetStaticMesh(LODMeshes[LODIndex]);
        }
    }
}
```

**渲染优化：**
- 使用 occlusion culling
- 合理设置材质复杂度
- 使用 instanced rendering
- 监控 draw calls

---

## 四、游戏架构模式

### 4.1 MVC 模式

**Model-View-Controller：**
- **Model**：数据和游戏逻辑
- **View**：可视化和用户界面
- **Controller**：处理输入和更新

**示例：**

```csharp
// Model
public class PlayerModel
{
    public int Health { get; set; }
    public int Score { get; set; }
    public float Speed { get; set; }

    public PlayerModel()
    {
        Health = 100;
        Score = 0;
        Speed = 5.0f;
    }
}

// View
public class PlayerView : MonoBehaviour
{
    [SerializeField] private Text healthText;
    [SerializeField] private Text scoreText;

    public void UpdateHealth(int health)
    {
        healthText.text = "Health: " + health;
    }

    public void UpdateScore(int score)
    {
        scoreText.text = "Score: " + score;
    }
}

// Controller
public class PlayerController : MonoBehaviour
{
    private PlayerModel model;
    private PlayerView view;

    private void Start()
    {
        model = new PlayerModel();
        view = GetComponent<PlayerView>();
        UpdateView();
    }

    private void Update()
    {
        // 处理输入
        if (Input.GetKeyDown(KeyCode.Space))
        {
            model.Score += 10;
            UpdateView();
        }
    }

    private void UpdateView()
    {
        view.UpdateHealth(model.Health);
        view.UpdateScore(model.Score);
    }
}
```

---

### 4.2 ECS 模式

**Entity-Component-System：**
- **Entity**：游戏对象
- **Component**：数据和属性
- **System**：逻辑处理

**Unity ECS 示例：**

```csharp
using Unity.Entities;
using Unity.Transforms;
using Unity.Mathematics;

// Component
public struct PositionComponent : IComponentData
{
    public float3 Value;
}

public struct MovementComponent : IComponentData
{
    public float3 Direction;
    public float Speed;
}

// System
public class MovementSystem : SystemBase
{
    protected override void OnUpdate()
    {
        float deltaTime = Time.DeltaTime;
        
        Entities
            .ForEach((ref PositionComponent position, in MovementComponent movement)
            => {
                position.Value += movement.Direction * movement.Speed * deltaTime;
            }).ScheduleParallel();
    }
}

// 创建Entity
public class GameManager : MonoBehaviour
{
    private void Start()
    {
        EntityManager entityManager = World.DefaultGameObjectInjectionWorld.EntityManager;
        
        Entity entity = entityManager.CreateEntity(
            typeof(PositionComponent),
            typeof(MovementComponent)
        );
        
        entityManager.SetComponentData(entity, new PositionComponent { Value = float3.zero });
        entityManager.SetComponentData(entity, new MovementComponent { Direction = new float3(1, 0, 0), Speed = 5.0f });
    }
}
```

---

### 4.3 状态模式

**游戏状态管理：**

```csharp
public abstract class GameState
{
    protected GameStateManager manager;

    public void SetManager(GameStateManager manager)
    {
        this.manager = manager;
    }

    public abstract void Enter();
    public abstract void Update();
    public abstract void Exit();
}

public class MainMenuState : GameState
{
    public override void Enter()
    {
        // 显示主菜单
        Debug.Log("Entering Main Menu State");
    }

    public override void Update()
    {
        // 处理菜单输入
        if (Input.GetKeyDown(KeyCode.Space))
        {
            manager.ChangeState(new GameplayState());
        }
    }

    public override void Exit()
    {
        // 隐藏主菜单
        Debug.Log("Exiting Main Menu State");
    }
}

public class GameplayState : GameState
{
    public override void Enter()
    {
        // 开始游戏
        Debug.Log("Entering Gameplay State");
    }

    public override void Update()
    {
        // 游戏逻辑
        if (Input.GetKeyDown(KeyCode.Escape))
        {
            manager.ChangeState(new PauseState());
        }
    }

    public override void Exit()
    {
        // 暂停游戏
        Debug.Log("Exiting Gameplay State");
    }
}

public class GameStateManager
{
    private GameState currentState;

    public void ChangeState(GameState newState)
    {
        if (currentState != null)
        {
            currentState.Exit();
        }
        
        currentState = newState;
        currentState.SetManager(this);
        currentState.Enter();
    }

    public void Update()
    {
        if (currentState != null)
        {
            currentState.Update();
        }
    }
}
```

---

## 五、游戏网络编程

### 5.1 网络架构

**客户端-服务器架构：**
- **权威服务器**：服务器验证所有操作
- **客户端预测**：客户端提前处理输入
- **状态同步**：服务器向客户端同步状态

**P2P 架构：**
- 对等连接
- 适合小型游戏
- 需要NAT穿透

---

### 5.2 Unity 网络

**Mirror 示例：**

```csharp
using Mirror;

public class NetworkPlayer : NetworkBehaviour
{
    [SyncVar] private string playerName;
    [SyncVar] private int score;

    public override void OnStartLocalPlayer()
    {
        // 本地玩家初始化
        Camera.main.GetComponent<CameraController>().SetTarget(transform);
    }

    [Command]
    public void CmdSetPlayerName(string name)
    {
        playerName = name;
    }

    [Command]
    public void CmdAddScore(int amount)
    {
        score += amount;
        RpcUpdateScore(score);
    }

    [ClientRpc]
    public void RpcUpdateScore(int newScore)
    {
        // 更新客户端UI
    }
}
```

---

### 5.3 网络优化

**带宽优化：**
- 数据压缩
- 增量同步
- 合理的同步频率
- 优先级排序

**延迟处理：**
- 客户端预测
- 服务器 reconciliation
- 插值和外推

**示例：**

```csharp
// 客户端预测
private Vector3 predictedPosition;
private Vector3 lastServerPosition;
private float timeSinceLastUpdate;

private void Update()
{
    if (isLocalPlayer)
    {
        // 本地移动
        Vector3 moveInput = new Vector3(Input.GetAxis("Horizontal"), 0, Input.GetAxis("Vertical"));
        transform.Translate(moveInput * speed * Time.deltaTime);
        predictedPosition = transform.position;
        
        // 发送输入到服务器
        CmdMove(moveInput);
    }
    else
    {
        // 平滑同步
        timeSinceLastUpdate += Time.deltaTime;
        float t = Mathf.Clamp01(timeSinceLastUpdate / syncInterval);
        transform.position = Vector3.Lerp(lastServerPosition, serverPosition, t);
    }
}

[Command]
private void CmdMove(Vector3 moveInput)
{
    // 服务器验证和处理
    transform.Translate(moveInput * speed * Time.deltaTime);
    RpcSyncPosition(transform.position);
}

[ClientRpc]
private void RpcSyncPosition(Vector3 position)
{
    if (!isLocalPlayer)
    {
        lastServerPosition = transform.position;
        serverPosition = position;
        timeSinceLastUpdate = 0;
    }
    else
    {
        // 服务器reconciliation
        float error = Vector3.Distance(predictedPosition, position);
        if (error > 0.1f)
        {
            transform.position = position;
            predictedPosition = position;
        }
    }
}
```

---

## 六、游戏 AI

### 6.1 行为树

**行为树示例：**

```csharp
public abstract class BTNode
{
    public abstract BTNodeStatus Execute();
}

public enum BTNodeStatus
{
    Success,
    Failure,
    Running
}

public class Sequence : BTNode
{
    private List<BTNode> children = new List<BTNode>();

    public void AddChild(BTNode node)
    {
        children.Add(node);
    }

    public override BTNodeStatus Execute()
    {
        foreach (var child in children)
        {
            BTNodeStatus status = child.Execute();
            if (status != BTNodeStatus.Success)
            {
                return status;
            }
        }
        return BTNodeStatus.Success;
    }
}

public class Selector : BTNode
{
    private List<BTNode> children = new List<BTNode>();

    public void AddChild(BTNode node)
    {
        children.Add(node);
    }

    public override BTNodeStatus Execute()
    {
        foreach (var child in children)
        {
            BTNodeStatus status = child.Execute();
            if (status != BTNodeStatus.Failure)
            {
                return status;
            }
        }
        return BTNodeStatus.Failure;
    }
}

public class PatrolNode : BTNode
{
    private Transform agent;
    private Vector3[] waypoints;
    private int currentWaypoint;

    public PatrolNode(Transform agent, Vector3[] waypoints)
    {
        this.agent = agent;
        this.waypoints = waypoints;
        currentWaypoint = 0;
    }

    public override BTNodeStatus Execute()
    {
        if (Vector3.Distance(agent.position, waypoints[currentWaypoint]) < 1.0f)
        {
            currentWaypoint = (currentWaypoint + 1) % waypoints.Length;
        }
        
        agent.position = Vector3.MoveTowards(agent.position, waypoints[currentWaypoint], 1.0f * Time.deltaTime);
        return BTNodeStatus.Running;
    }
}

public class EnemyAI : MonoBehaviour
{
    private BTNode behaviorTree;

    private void Start()
    {
        Vector3[] waypoints = new Vector3[] {
            new Vector3(0, 0, 0),
            new Vector3(10, 0, 0),
            new Vector3(10, 0, 10),
            new Vector3(0, 0, 10)
        };

        var patrolNode = new PatrolNode(transform, waypoints);
        var sequence = new Sequence();
        sequence.AddChild(patrolNode);

        behaviorTree = sequence;
    }

    private void Update()
    {
        behaviorTree.Execute();
    }
}
```

---

### 6.2 状态机

**AI 状态机：**

```csharp
public enum AIState
{
    Patrol,
    Chase,
    Attack,
    Retreat
}

public class AIStateMachine
{
    private AIState currentState;
    private AIController controller;

    public AIStateMachine(AIController controller)
    {
        this.controller = controller;
        currentState = AIState.Patrol;
    }

    public void Update()
    {
        switch (currentState)
        {
            case AIState.Patrol:
                Patrol();
                break;
            case AIState.Chase:
                Chase();
                break;
            case AIState.Attack:
                Attack();
                break;
            case AIState.Retreat:
                Retreat();
                break;
        }
    }

    private void Patrol()
    {
        // 巡逻逻辑
        if (controller.CanSeePlayer())
        {
            currentState = AIState.Chase;
        }
    }

    private void Chase()
    {
        // 追逐逻辑
        if (!controller.CanSeePlayer())
        {
            currentState = AIState.Patrol;
        }
        else if (controller.IsPlayerInAttackRange())
        {
            currentState = AIState.Attack;
        }
    }

    private void Attack()
    {
        // 攻击逻辑
        if (!controller.CanSeePlayer())
        {
            currentState = AIState.Patrol;
        }
        else if (!controller.IsPlayerInAttackRange())
        {
            currentState = AIState.Chase;
        }
        else if (controller.Health < 20)
        {
            currentState = AIState.Retreat;
        }
    }

    private void Retreat()
    {
        // 撤退逻辑
        if (controller.Health > 50)
        {
            currentState = AIState.Chase;
        }
    }
}
```

---

### 6.3 寻路

**A* 算法：**

```csharp
public class Node
{
    public int x, y;
    public int gCost, hCost;
    public int fCost => gCost + hCost;
    public Node parent;

    public Node(int x, int y)
    {
        this.x = x;
        this.y = y;
    }
}

public class AStarPathfinding
{
    private int[,] grid;
    private int gridWidth, gridHeight;

    public AStarPathfinding(int[,] grid)
    {
        this.grid = grid;
        gridWidth = grid.GetLength(0);
        gridHeight = grid.GetLength(1);
    }

    public List<Node> FindPath(Node startNode, Node targetNode)
    {
        List<Node> openSet = new List<Node>();
        HashSet<Node> closedSet = new HashSet<Node>();
        openSet.Add(startNode);

        while (openSet.Count > 0)
        {
            Node currentNode = openSet[0];
            for (int i = 1; i < openSet.Count; i++)
            {
                if (openSet[i].fCost < currentNode.fCost || 
                    (openSet[i].fCost == currentNode.fCost && openSet[i].hCost < currentNode.hCost))
                {
                    currentNode = openSet[i];
                }
            }

            openSet.Remove(currentNode);
            closedSet.Add(currentNode);

            if (currentNode.x == targetNode.x && currentNode.y == targetNode.y)
            {
                return RetracePath(startNode, currentNode);
            }

            foreach (Node neighbor in GetNeighbors(currentNode))
            {
                if (grid[neighbor.x, neighbor.y] == 1 || closedSet.Contains(neighbor))
                {
                    continue;
                }

                int newCostToNeighbor = currentNode.gCost + GetDistance(currentNode, neighbor);
                if (newCostToNeighbor < neighbor.gCost || !openSet.Contains(neighbor))
                {
                    neighbor.gCost = newCostToNeighbor;
                    neighbor.hCost = GetDistance(neighbor, targetNode);
                    neighbor.parent = currentNode;

                    if (!openSet.Contains(neighbor))
                    {
                        openSet.Add(neighbor);
                    }
                }
            }
        }

        return null; // 无路径
    }

    private List<Node> GetNeighbors(Node node)
    {
        List<Node> neighbors = new List<Node>();

        // 四向寻路
        if (node.x > 0) neighbors.Add(new Node(node.x - 1, node.y));
        if (node.x < gridWidth - 1) neighbors.Add(new Node(node.x + 1, node.y));
        if (node.y > 0) neighbors.Add(new Node(node.x, node.y - 1));
        if (node.y < gridHeight - 1) neighbors.Add(new Node(node.x, node.y + 1));

        return neighbors;
    }

    private int GetDistance(Node a, Node b)
    {
        int dx = Mathf.Abs(a.x - b.x);
        int dy = Mathf.Abs(a.y - b.y);
        return dx + dy; // 曼哈顿距离
    }

    private List<Node> RetracePath(Node startNode, Node endNode)
    {
        List<Node> path = new List<Node>();
        Node currentNode = endNode;

        while (currentNode != startNode)
        {
            path.Add(currentNode);
            currentNode = currentNode.parent;
        }

        path.Reverse();
        return path;
    }
}
```

---

## 七、游戏测试

### 7.1 测试策略

**测试类型：**
- **单元测试**：测试单独的函数和类
- **集成测试**：测试组件间的交互
- **性能测试**：测试游戏性能
- **功能测试**：测试游戏功能
- **回归测试**：测试修复后的功能

**Unity 测试示例：**

```csharp
using NUnit.Framework;
using UnityEngine.TestTools;

public class PlayerTests
{
    [Test]
    public void PlayerHealthDecreasesWhenDamaged()
    {
        // Arrange
        var player = new Player();
        int initialHealth = player.Health;
        int damage = 10;

        // Act
        player.TakeDamage(damage);

        // Assert
        Assert.AreEqual(initialHealth - damage, player.Health);
    }

    [UnityTest]
    public IEnumerator PlayerCanJump()
    {
        // Arrange
        var player = new GameObject().AddComponent<PlayerController>();
        float initialY = player.transform.position.y;

        // Act
        player.Jump();
        yield return new WaitForSeconds(0.5f);

        // Assert
        Assert.Greater(player.transform.position.y, initialY);
    }
}
```

---

### 7.2 性能分析

**Unity Profiler：**
- CPU 分析
- 内存分析
- 渲染分析
- 网络分析

**Unreal 分析器：**
- 会话前端
- 时序图
- 统计信息
- 内存分析

**示例：**

```csharp
// Unity 性能标记
using UnityEngine.Profiling;

void Update()
{
    using (new ProfilerMarker("EnemyAI.Update").Auto())
    {
        // AI 逻辑
    }
}

// 内存分析
void CheckMemory()
{
    long usedMemory = Profiler.GetTotalAllocatedMemoryLong();
    long reservedMemory = Profiler.GetTotalReservedMemoryLong();
    long systemMemory = Profiler.GetTotalUnusedReservedMemoryLong();
    
    Debug.Log($"Used: {usedMemory / 1024 / 1024} MB");
    Debug.Log($"Reserved: {reservedMemory / 1024 / 1024} MB");
    Debug.Log($"System: {systemMemory / 1024 / 1024} MB");
}
```

---

## 八、游戏发布

### 8.1 构建流程

**Unity 构建：**

```bash
# 命令行构建
unity -quit -batchmode -projectPath /path/to/project -buildWindows64Player /path/to/build/Game.exe

# 多平台构建
unity -quit -batchmode -projectPath /path/to/project -buildOSXUniversalPlayer /path/to/build/Game.app
unity -quit -batchmode -projectPath /path/to/project -buildAndroidPlayer /path/to/build/Game.apk
```

**Unreal 构建：**

```bash
# 命令行构建
UE4Editor-Cmd.exe /path/to/project/Project.uproject -run=BuildCookRun -project=/path/to/project/Project.uproject -platform=Win64 -configuration=Development -cook -build -stage -pak -archive -archivedirectory=/path/to/build
```

### 8.2 平台发布

**Steam 发布：**
- 创建 Steamworks 账户
- 设置应用信息
- 上传构建
- 设置定价和地区
- 提交审核

**Epic Games Store 发布：**
- 注册开发者账户
- 创建产品页面
- 上传构建
- 提交审核

**移动平台发布：**
- **iOS**：App Store Connect
- **Android**：Google Play Console

**Web 发布：**
- WebGL 构建
- 部署到网页服务器
- 考虑使用 itch.io、Kongregate 等平台

---

## 九、常见问题与解决方案

### 9.1 性能问题

**问题：** 游戏卡顿
**解决方案：**
- 使用性能分析工具
- 优化渲染
- 减少 draw calls
- 使用对象池
- 优化 AI 计算

**问题：** 内存泄漏
**解决方案：**
- 监控内存使用
- 正确释放资源
- 避免循环引用
- 使用 Profiler 分析

### 9.2 网络问题

**问题：** 延迟高
**解决方案：**
- 使用客户端预测
- 服务器 reconciliation
- 优化网络同步频率
- 选择合适的网络协议

**问题：** 同步错误
**解决方案：**
- 权威服务器验证
- 状态同步机制
- 处理网络中断
- 重试机制

### 9.3 AI 问题

**问题：** AI 行为不自然
**解决方案：**
- 调整行为树
- 添加随机因素
- 考虑环境因素
- 测试不同场景

**问题：** AI 性能差
**解决方案：**
- 优化寻路算法
- 减少 AI 更新频率
- 使用层次化 AI
- 避免复杂计算

---

## 十、最佳实践总结

1. **项目结构**：清晰的目录结构和命名规范
2. **性能优化**：内存管理、渲染优化、对象池
3. **架构模式**：MVC、ECS、状态模式
4. **网络编程**：权威服务器、客户端预测、状态同步
5. **AI 设计**：行为树、状态机、寻路算法
6. **测试策略**：单元测试、性能测试、回归测试
7. **发布流程**：多平台构建、应用商店发布
8. **代码质量**：代码规范、注释、文档
9. **团队协作**：版本控制、构建系统、任务管理
10. **用户体验**：流畅的 gameplay、合理的难度、良好的UI

---

## 相关资源

- [Unity 官方文档](https://docs.unity3d.com/Manual/index.html)
- [Unreal Engine 官方文档](https://docs.unrealengine.com/5.0/en-US/)
- [Game Development Patterns](https://gameprogrammingpatterns.com/)
- [Networking for Game Programmers](https://gafferongames.com/)
- [Game AI Pro](https://www.gameaipro.com/)
- [Unity Asset Store](https://assetstore.unity.com/)
- [Unreal Marketplace](https://www.unrealengine.com/marketplace)

