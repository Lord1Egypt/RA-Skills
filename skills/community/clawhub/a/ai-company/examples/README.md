# AI Company - 示例代码和工具

本目录包含AI Company系统的示例代码、初始化工具和配置文件，帮助你快速理解和使用。

## 🚀 快速开始

### 使用初始化脚本创建项目（推荐）

```bash
# 创建新的AI公司项目
python3 init_ai_company.py my-ai-company

# 进入项目目录
cd my-ai-company

# 配置环境变量
cp .env.example .env
# 编辑 .env 文件，添加你的API密钥

# 启动你的AI公司
python main.py start
```

## 示例文件

### 1. simple_ai_employee.py
展示如何创建一个基础的AI员工。

**功能**:
- AI员工基本结构
- 思考和规划能力
- 任务执行
- 记忆和学习
- 状态保存和加载

**运行**:
```bash
python simple_ai_employee.py
```

### 2. simple_event_bus.py
展示如何使用事件总线进行AI员工间通信。

**功能**:
- 事件订阅和发布
- 事件历史记录
- 异步事件处理
- 标准事件类型

**运行**:
```bash
python simple_event_bus.py
```

### 3. simple_coordinator.py
展示如何协调多个AI员工协同工作。

**功能**:
- AI团队协调
- 完整工作流程
- 事件驱动架构
- 状态监控

**运行**:
```bash
python simple_coordinator.py
```

## 快速开始

1. **运行单个AI员工**:
```bash
python simple_ai_employee.py
```

2. **运行事件总线演示**:
```bash
python simple_event_bus.py
```

3. **运行完整的AI公司演示**:
```bash
python simple_coordinator.py
```

## 实际应用

### 创建你自己的AI员工

```python
from simple_ai_employee import SimpleAIEmployee

# 创建自定义AI员工
my_ai = SimpleAIEmployee(
    name="my_custom_ai",
    role="我的专家",
    version="v1.0"
)

# 执行任务
task = {
    "id": "task_001",
    "description": "执行某个任务",
    "type": "custom"
}

result = my_ai.work(task)
print(result)
```

### 设置事件通信

```python
from simple_event_bus import SimpleEventBus, EventTypes

# 创建事件总线
event_bus = SimpleEventBus()

# 定义事件处理器
def handle_event(data):
    print(f"收到事件: {data}")

# 订阅事件
event_bus.subscribe("custom.event", handle_event)

# 发布事件
event_bus.publish("custom.event", {"message": "Hello"})
```

### 协调AI团队

```python
from simple_coordinator import SimpleAITeamCoordinator
from simple_ai_employee import SimpleAIEmployee

# 创建协调器
coordinator = SimpleAITeamCoordinator()

# 注册AI员工
coordinator.register_employee(
    SimpleAIEmployee("market_researcher", "市场研究专家")
)
coordinator.register_employee(
    SimpleAIEmployee("developer", "开发者")
)

# 启动团队
coordinator.start()
```

## 下一步

1. 阅读示例代码，理解基本概念
2. 修改示例，创建你自己的AI员工
3. 集成到你的项目中
4. 查看完整文档了解更多功能

## 注意事项

这些是简化的示例，用于教学目的。生产环境需要：

- 错误处理和重试机制
- 持久化存储
- 日志记录
- 监控和告警
- 安全性措施

查看主文档了解完整的实现方案。

## 贡献

欢迎提交你的示例代码！
