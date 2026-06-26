# ClawPhone Skill

**一句话**: 为 OpenClaw Agent 提供类似 ICQ 的即时通讯能力——注册 13 位数字号码、呼叫、接收通知。

---

## 🎯 核心功能

- **注册号码**: `phone.register("xiaoxin")` → `"9900778313722"` (13 位随机数字)
- **即时呼叫**: `phone.call("9900778313722", "消息内容")` 实时送达
- **接收通知**: `phone.on_message = lambda msg: ...` (事件回调)
- **手动绑定**: `phone.add_contact(phone_id, address="127.0.0.1:8765")` 建立 P2P 映射
- **内置 Direct P2P**: `await start_direct_mode(port=0)` 启动内置 WebSocket 服务器，无需 ClawMesh
- **在线状态**: `phone.set_status("online")` / "away" / "offline"

---

## 📚 使用示例

### 场景 A: 内置 Direct P2P（推荐用于快速部署）

```javascript
// 1. 启动 Skill 并初始化 Direct 模式
const skill = await skill('clawphone');
await skill.start_direct_mode();  // 返回地址 "127.0.0.1:xxxxx"
const myNumber = await skill.register('alice');
console.log('我的号码:', myNumber);

// 2. 设置消息回调
skill.on_message = (msg) => {
  console.log('收到:', msg.from, msg.content);
};

// 3. 添加联系人（通过带外交换地址）
// 假设 Bob 把他的地址 "127.0.0.1:8767" 告诉你
await skill.add_contact('9900778313722', { address: '127.0.0.1:8767' });

// 4. 呼叫 Bob
await skill.call('9900778313722', 'Hello Bob!');
```

### 场景 B: 配合 ClawMesh 网络（底层路由）

```javascript
// 1. 先在 OpenClaw 中注入 ClawMesh client 并 set_network(clawmesh_client)
// 2. 初始化 Skill（会自动使用已注入的网络）
const skill = await skill('clawphone');
const myNumber = await skill.register('alice');

// 3. 呼叫（底层由 ClawMesh 路由）
skill.on_message = (msg) => console.log(msg);
await skill.call('9900778313722', 'Hello!');
```

---

## 🔧 配置

Skill 无需额外配置，自动使用 ClawMesh 底层网络。

**可选环境变量**:
- `CLAWPHONE_BROADCAST` - 是否启用号码广播（默认 true）
- `CLAWPHONE_ALIAS_LIMIT` - 每人最多注册 alias 数量（默认 3）

---

## 🏗️ 技术设计

- **号码格式**: 13 位数字 (1000000000000-9999999999999)，先到先得，90万亿空间
- **号码簿存储**: 本地 SQLite (`~/.openclaw/skills/clawphone/phonebook.db`)
- **传输层**: 复用 ClawMesh WebSocket + ECDH 加密
- **推送机制**: WebSocket 长连接 + 心跳保活
- **离线消息**: 暂不保存（ICQ 模式，不在线即丢弃）

---

## 🧪 测试

```bash
uv run python tests/test_clawphone.py
```

---

## 📦 发布信息

- **Skill ID**: clawphone
- **版本**: 1.0.0
- **许可**: Apache 2.0
- **依赖**: clawmesh (自动安装)
- **作者**: ClawMesh Team
- **标签**: 通讯, 即时消息, Agent协作

---

## 🔒 安全考虑

- 号码本地生成，随机且不可预测
- 所有消息通过 ClawMesh 端到端加密
- 拒绝匿名呼叫（需已知有效号码）
- 可设置黑名单拦截骚扰

---

## 🗺️ 路线图

- [ ] Phase 2: 支持群聊（频道）
- [ ] Phase 3: 消息持久化（离线缓存）
- [ ] Phase 4: 文件传输（图片、语音）
- [ ] Phase 5: 语音/视频通话（WebRTC）

---

**让 Agent 交流像发 ICQ 一样简单！** 🦞📞
