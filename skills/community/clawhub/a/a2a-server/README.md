# 📡 A2A Server - Agent-to-Agent Communication

**版本**: v0.1.0  
**状态**: ⏳ 开发中（Phase 2 实施）  
**协议**: WebSocket

---

## 🎯 功能特性

- ✅ **Agent 注册与发现** - 动态注册和能力发现
- ✅ **P2P 消息转发** - Agent 间直接通信
- ✅ **RPC 调用** - 请求/响应模式
- ✅ **发布/订阅** - 频道广播
- ✅ **能力发现** - 按能力搜索 Agent
- ✅ **离线消息队列** - 支持离线 Agent
- ✅ **心跳机制** - 自动检测离线
- ⏳ **信任链授权** - 待实现
- ⏳ **消息签名** - 待实现

---

## 🚀 快速开始

### 1. 安装依赖

```bash
cd skills/a2a-server
npm install
```

### 2. 启动服务器

```bash
npm start
# 或
node src/server.js
```

**环境变量**:
- `A2A_PORT` - 端口（默认 8080）
- `A2A_HOST` - 主机（默认 localhost）
- `A2A_VERBOSE` - 详细日志（默认 false）

### 3. 客户端连接

```javascript
const { A2AClient } = require('./src/client');

const client = new A2AClient('ws://localhost:8080', {
  agentId: 'my-agent',
  capabilities: ['search', 'analyze'],
  verbose: true,
});

await client.connect();
```

---

## 📖 使用示例

### Agent 注册

```javascript
const client = new A2AClient('ws://localhost:8080', {
  agentId: 'planner-agent',
  capabilities: ['planning', 'analysis'],
  metadata: {
    version: '1.0.0',
    author: 'Clawd'
  }
});

await client.connect();
// 自动注册
```

### RPC 调用

```javascript
// 调用远程 Agent
const result = await client.call('executor-agent', {
  action: 'execute',
  task: 'analyze code',
  params: { code: '...' }
});

console.log(result);
```

### 发布/订阅

```javascript
// 订阅频道
await client.subscribe('notifications');

client.on('message', (payload, from) => {
  console.log(`收到消息 from ${from}:`, payload);
});

// 发布消息
await client.publish('notifications', {
  type: 'task-complete',
  taskId: '123'
});
```

### 能力发现

```javascript
// 发现所有 Agent
const agents = await client.discover();

// 按能力发现
const searchAgents = await client.discover({
  capability: 'search'
});

// 按元数据筛选
const v1Agents = await client.discover({
  filter: { version: '1.0.0' }
});
```

---

## 🏗️ 架构设计

```
┌──────────────┐     ┌──────────────┐
│   Agent A    │ ──→ │  A2A Server  │
│  (Planner)   │ ←── │  (WebSocket) │
└──────────────┘     └──────────────┘
                            │
                     ┌──────────────┐
                     │   Agent B    │
                     │  (Executor)  │
                     └──────────────┘
```

### 消息类型

| 类型 | 方向 | 用途 |
|------|------|------|
| `register` | C→S | Agent 注册 |
| `registered` | S→C | 注册确认 |
| `call` | C→S→C | RPC 调用 |
| `response` | C→S→C | RPC 响应 |
| `publish` | C→S | 发布消息 |
| `subscribe` | C→S | 订阅频道 |
| `discover` | C→S | 能力发现 |
| `heartbeat` | C→S | 心跳 |

---

## 📊 API 参考

### A2AServer

#### `constructor(options)`
- `port` - 端口（默认 8080）
- `host` - 主机（默认 localhost）
- `verbose` - 详细日志
- `heartbeatInterval` - 心跳间隔（默认 30000ms）

#### `start()`
启动服务器

#### `stop()`
停止服务器

#### `getStats()`
获取统计信息

#### `getAgents()`
获取已注册 Agent 列表

#### `broadcast(payload, exclude)`
广播消息

---

### A2AClient

#### `constructor(serverUrl, options)`
- `agentId` - Agent ID
- `capabilities` - 能力列表
- `callTimeout` - 调用超时（默认 30000ms）
- `maxReconnectAttempts` - 最大重连次数

#### `connect()`
连接服务器

#### `disconnect()`
断开连接

#### `call(targetAgentId, payload, options)`
RPC 调用

#### `publish(channel, payload)`
发布消息

#### `subscribe(channel)`
订阅频道

#### `discover(options)`
能力发现

#### `getStatus()`
获取连接状态

---

## 🧪 测试

```bash
npm test
```

**测试覆盖**:
- ✅ 服务器启动/停止
- ✅ Agent 注册/注销
- ✅ RPC 调用
- ✅ 发布/订阅
- ✅ 能力发现
- ✅ 心跳机制

---

## 🔗 集成示例

### 与 Multi-Agent 集成

```javascript
const { MultiAgentOrchestrator } = require('../multi-agent');
const { A2AClient } = require('../a2a-server');

// 创建 A2A 客户端
const a2a = new A2AClient('ws://localhost:8080', {
  agentId: 'planner-agent',
  capabilities: ['planning']
});

await a2a.connect();

// 创建编排器
const orchestrator = new MultiAgentOrchestrator();

// 注册远程工具
orchestrator.registerTool('remote-execute',
  async (params) => {
    const agents = await a2a.discover({ capability: 'execution' });
    if (agents.length === 0) {
      throw new Error('No executor found');
    }
    
    return await a2a.call(agents[0].agentId, params);
  },
  { description: '远程执行', keywords: ['执行', '远程'] }
);
```

### 与 ReAct 集成

```javascript
const { ReActOrchestrator } = require('../react-orchestrator');
const { A2AClient } = require('../a2a-server');

const orchestrator = new ReActOrchestrator();
const a2a = new A2AClient('ws://localhost:8080', {
  agentId: 'react-agent',
  capabilities: ['reasoning', 'tool-use']
});

await a2a.connect();

// 注册远程工具
orchestrator.registerTool('remote-search',
  async (params) => {
    const agents = await a2a.discover({ capability: 'search' });
    return await a2a.call(agents[0].agentId, params);
  },
  { description: '远程搜索', keywords: ['搜索', '远程'] }
);
```

---

## 📋 下一步计划

### Phase 2: 能力发现与授权（本周）
- [ ] 信任链实现
- [ ] 消息签名验证
- [ ] 黑名单机制

### Phase 3: 集成测试（下周）
- [ ] Multi-Agent A2A 支持
- [ ] ReAct 远程工具调用
- [ ] 端到端测试

---

## 📚 参考资料

- `A2A-RESEARCH.md` - A2A 调研报告
- `USAGE-GUIDE.md` - React Orchestrator 使用指南
- [WebSocket API](https://developer.mozilla.org/en-US/docs/Web/API/WebSocket)

---

*最后更新：2026-03-18*  
*状态：⏳ Phase 2 实施中*
