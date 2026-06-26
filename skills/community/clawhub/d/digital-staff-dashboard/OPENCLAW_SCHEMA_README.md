# OpenClaw Schema 验证使用说明

本项目现已集成 OpenClaw 官方 JSON Schema 验证，确保对 `openclaw.json` 的修改符合官方语法规范。

## 功能特性

### 1. 官方 Schema 对齐
- 基于 OpenClaw 2026.4.1 版本的 runtime-schema 定义
- 完整支持 `agents.list`、`models.providers`、`gateway`、`tools` 等核心配置
- 支持 `subagents.allowAgents` 等嵌套配置验证

### 2. 非法命名检查
- **Agent ID 命名规则**：
  - 必须以字母开头 (`a-z`, `A-Z`)
  - 只能包含字母、数字、连字符(`-`)和下划线(`_`)
  - 最大长度 64 字符
  - 不能使用保留字（如 `class`, `function`, `null` 等）
  
- **非法字符检测**：
  - 检测 `<`, `>`, `:`, `"`, `/`, `\\`, `|`, `?`, `*` 等非法字符
  - 检测控制字符（`\x00-\x1f`）

### 3. Schema 验证
- 类型检查（object, array, string, integer, boolean, number）
- 必需字段检查（如 `agents.list[].id`）
- 枚举值检查（如 `thinkingDefault` 必须是特定值之一）
- 额外属性检查（防止写入非法属性）

## 使用方法

### 基本使用

```python
from openclaw_config import get_openclaw_config_manager

# 创建配置管理器（启用验证）
manager = get_openclaw_config_manager()

# 验证配置
config = manager.read_global_config()
result = manager.validate_config(config)
print(result)  # {'valid': True, 'errors': [], 'warnings': []}
```

### 创建 Agent（自动验证）

```python
# 创建新 Agent 时会自动验证名称和配置
result = manager.create_agent("my-agent", {
    "display_name": "My Agent",
    "emoji": "🤖",
    "model_provider": "deepseek",
    "model_id": "deepseek-chat"
})

if not result["success"]:
    print(f"创建失败: {result['error']}")
```

### 检查 Agent 名称

```python
# 预先检查名称是否合法
check = manager.check_agent_name_valid("test-agent")
if check["valid"]:
    print("名称合法")
else:
    print(f"名称不合法: {check['error']}")
    
# 检查警告
if check["warnings"]:
    print(f"警告: {check['warnings']}")
```

### 独立验证

```python
from openclaw_schema import validate_config, validate_agent_config

# 验证完整配置
result = validate_config({
    "agents": {
        "list": [{"id": "test", "name": "Test"}]
    }
})

# 验证单个 Agent
result = validate_agent_config({
    "id": "test",
    "identity": {"name": "Test", "emoji": "🤖"}
})
```

### 开发模式（跳过验证）

```python
# 在开发调试时可跳过验证
manager = get_openclaw_config_manager(skip_validation=True)
```

## Schema 定义文件

### `openclaw_schema.py`
包含完整的 JSON Schema 定义：
- `OPENCLAW_CONFIG_SCHEMA` - 主配置 schema
- `AGENT_LIST_ITEM_SCHEMA` - Agent 条目 schema
- `AGENT_IDENTITY_SCHEMA` - Agent 身份 schema
- `SUBAGENTS_SCHEMA` - Subagents 配置 schema
- `MODELS_SCHEMA` - Models 配置 schema
- `TOOLS_SCHEMA` - Tools 配置 schema

### 支持的配置项

#### Agents
- `agents.defaults` - 默认配置
  - `model`, `workspace`, `maxConcurrent`, `subagents`
  - `compaction`, `thinkingDefault`, `reasoningDefault`
  - `memorySearch`, `sandbox`, `tools`
- `agents.list[]` - Agent 列表
  - `id`, `name`, `workspace`, `agentDir`, `model`
  - `identity` (name, theme, emoji, avatar)
  - `subagents` (allowAgents, maxConcurrent)
  - `thinkingDefault`, `reasoningDefault`, `fastModeDefault`
  - `skills`, `memorySearch`

#### Models
- `models.mode` - `merge` 或 `replace`
- `models.providers` - Provider 配置
  - `baseUrl`, `apiKey`, `api`, `auth`, `models`

#### Gateway
- `gateway.port`, `gateway.mode`, `gateway.bind`
- `gateway.auth` - 认证配置
- `gateway.controlUi`, `gateway.remote`, `gateway.tailscale`

#### Tools
- `tools.profile` - `minimal`, `coding`, `messaging`, `full`
- `tools.allow`, `tools.deny` - 工具白名单/黑名单
- `tools.agentToAgent` - Agent 间调用配置
- `tools.exec` - 执行配置

#### Skills & Plugins
- `skills.entries` - Skill 启用配置
- `plugins.entries` - Plugin 启用配置
- `plugins.installs` - Plugin 安装信息

## 错误处理

### 常见错误类型

1. **非法命名**
   ```
   'id' ('123-agent') 命名不合法: 必须以字母开头
   'class' 是保留字，不能使用
   ```

2. **类型错误**
   ```
   'agents.list' 必须是数组类型
   'maxConcurrent' 必须是整数类型
   ```

3. **缺少必需字段**
   ```
   'root.agents.list[0]' 缺少必需属性: 'id'
   ```

4. **非法属性**
   ```
   'root.agents.list[0]' 包含非法属性: ['illegalProperty']
   ```

5. **枚举值错误**
   ```
   'thinkingDefault' 值必须是其中之一: ['off', 'minimal', 'low', ...]
   ```

## 注意事项

1. **profile 名称中的冒号**：`auth.profiles` 和 `models.providers` 的键名可以包含冒号（如 `kimi-coding:default`）
2. **Agent ID 唯一性**：配置中不能有重复的 Agent ID
3. **大小写敏感**：Agent ID 是大小写敏感的（`MyAgent` 和 `myagent` 是不同的）
4. **保留字列表**：详见 `openclaw_schema.RESERVED_KEYWORDS`

## 测试

运行内置测试：
```bash
cd /home/mike/workspace/agent-dashboard-v2
python3 openclaw_schema.py
python3 openclaw_config.py
```

## 参考

- OpenClaw 版本：2026.4.1
- Schema 来源：`/home/mike/.npm-global/lib/node_modules/openclaw/dist/runtime-schema-B34T_6nr.js`
