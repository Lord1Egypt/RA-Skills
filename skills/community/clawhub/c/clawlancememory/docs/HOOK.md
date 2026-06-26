# Hook 集成指南

## 什么是 Hook？

Hook 是 OpenClaw 的插件机制，允许在特定事件发生时执行自定义代码。

## Memory Hook 工作原理

```
OpenClaw 启动
    ↓
触发 agent:bootstrap 事件
    ↓
Memory Hook 拦截 (handler.js)
    ↓
调用 Python 脚本 (session_start.py)
    ↓
从 LanceDB 检索记忆
    ↓
生成 USER_MEMORY.md
    ↓
注入到 agent context
    ↓
Agent 启动时读取记忆
```

## 启用 Hook

### 方法 1: 使用脚本

```bash
bash enable.sh
```

### 方法 2: OpenClaw 命令

```bash
openclaw hooks enable memory-system
```

### 方法 3: 手动启用

```bash
# 创建符号链接
ln -s /path/to/claw_lance/hooks/memory-system \
      ~/.openclaw/hooks/memory-system
```

## 配置文件

### HOOK.md

Hook 元数据：

```yaml
---
name: memory-system
description: "Injects user memory from LanceDB"
metadata:
  events: ["agent:bootstrap"]
---
```

### handler.js

Hook 处理器，负责：
1. 监听 `agent:bootstrap` 事件
2. 调用 Python 脚本
3. 注入记忆到 context

## 环境变量

| 变量 | 说明 | 默认值 |
|------|------|--------|
| `ZHIPU_API_KEY` | 智谱 AI API Key | 必须设置 |
| `OPENCLAW_USER_ID` | 用户 ID | "default_user" |

## 验证 Hook

### 检查文件

```bash
ls -la ~/.openclaw/hooks/memory-system/
```

应该包含：
- HOOK.md
- handler.js

### 查看日志

```bash
tail -f ~/.openclaw/logs/openclaw.log | grep "Memory"
```

### 测试对话

问："我负责什么项目？"

如果回答包含项目信息，说明 Hook 工作正常。

## 禁用 Hook

```bash
openclaw hooks disable memory-system
```

## 自定义 Hook

### 修改检索逻辑

编辑 `handler.js`：

```javascript
const memoryOutput = execSync(
  `${python} ${script} --user_id ${userId} --json`,
  {
    encoding: 'utf8',
    env: { ...process.env }
  }
);
```

### 修改注入格式

编辑 `formatMemorySection()` 函数。

## 故障排查

### Hook 不加载

1. 检查文件权限：`chmod +x handler.js`
2. 检查 Node.js 版本：`node --version`
3. 查看日志：`tail -f ~/.openclaw/logs/openclaw.log`

### Python 脚本报错

1. 检查虚拟环境：`source venv/bin/activate`
2. 检查依赖：`pip install -r requirements.txt`
3. 测试脚本：`python3 skill.py stats`

### 记忆不更新

记忆在每次 bootstrap 时重新加载，确保：
1. 记忆已保存
2. 重启 session
