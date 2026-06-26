# 快速开始

## 安装依赖

```bash
cd auto-model-switch
npm install
```

## 配置

编辑 `config.yaml`，设置你的模型：

```yaml
models:
  - id: primary
    model: your-primary-model
    name: "主模型"
    daily_limit: 10000000  # 每日token限制
    priority: 1
  
  - id: backup-1
    model: your-backup-model
    name: "备用模型"
    daily_limit: null  # 无限制
    priority: 2
```

## 使用方法

### 1. 查看状态

```bash
node auto_model_switch.js status
```

输出：
```
📊 模型状态
当前：Astron Code
Token：8.5M / 10M (85%)

备用模型：
- GLM-4.5 (可用)
```

### 2. 手动切换

```bash
node auto_model_switch.js switch
```

### 3. 心跳检查（自动）

在 `HEARTBEAT.md` 中添加：

```markdown
- 运行: node ~/.openclaw/workspace/skills/auto-model-switch/heartbeat.js
```

或在心跳时调用：

```bash
node auto_model_switch.js heartbeat
```

### 4. 同步token使用量

```bash
node auto_model_switch.js sync
```

## 与OpenClaw集成

### 环境变量

```bash
export OPENCLAW_GATEWAY_URL="http://localhost:3000"
export OPENCLAW_GATEWAY_TOKEN="your-token"
```

### 自动切换

当token使用超过95%时，自动切换到备用模型。

## 测试

```bash
npm test
```
