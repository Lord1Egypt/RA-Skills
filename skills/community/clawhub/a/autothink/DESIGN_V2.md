# AutoThink v2 设计报告

## 🎯 需求分析

**用户需求**：持久化 thinking 模式设置
- 使用 `-h`/`-l`/`-m` 一次设置后，后续消息自动沿用
- 默认使用 high 模式（无需前缀）
- 不再进行复杂度分析，节省 token
- 随时可切换

---

## ✅ 实现方案

### 核心改动

1. **会话状态持久化**
   - 使用 `Map()` 存储 `sessionId -> thinkingLevel`
   - 同一会话中，首次设置后后续请求自动沿用

2. **关闭自动分析**
   - v2 默认 `autoAnalyze = false`
   - 无额外 token 消耗，纯粹状态管理

3. **默认模式**
   - 全局默认：`high`
   - 会话未设置时返回默认值

4. **前缀语法**
   - `-h` / `--high` → 设置并持久化 high
   - `-l` / `--low` → 设置并持久化 low
   - `-m` / `--medium` → 设置并持久化 medium

---

## 🔄 工作流程

```
用户发送: "-h 帮我设计一个分布式系统"
  ↓
1. 检测到前缀 "-h" → 模式切换
2. 提取模式 = "high"
3. 持久化到 sessionStates[sessionId] = "high"
4. 清理消息内容（移除 "-h "）
5. 使用 thinking=high 发送给 agent
6. 返回响应

用户后续发送: "那数据库怎么设计？"
  ↓
1. 无前缀 → 查找 sessionStates[sessionId]
2. 发现已有 "high" → 沿用
3. 直接使用 thinking=high 发送
4. 返回响应
```

---

## 📊 效果对比

| 指标 | v1 (自动分析) | v2 (持久化) |
|------|---------------|-------------|
| **首次设置** | 需分析（+token）| 前缀设置（+0 token 分析） |
| **后续消息** | 每次分析（+token）| 直接沿用（+0 token） |
| **响应速度** | 稍慢（分析耗时）| 快（无分析） |
| **控制精度** | 自动判断 | 手动全控 |

---

## 🧪 测试结果

```
测试 session: sess1
1. "你好"                          → high (默认)
2. "-h 帮我设计系统"               → high (设置并持久)
3. "现在几点了"                    → high (沿用)

测试 session: sess2
4. "-l 简单问题"                  → low (设置并持久)
5. "另一个问题"                   → low (沿用)

测试 session: sess3
6. "复杂分析"                     → high (默认)
```

✅ **通过**：会话隔离、模式持久、前缀覆盖

---

## 📁 更新文件清单

| 文件 | 状态 | 说明 |
|------|------|------|
| `src/index.js` | ✏️ 已更新 | Engine v2，增加状态管理 |
| `src/cli.js` | ✏️ 已更新 | 支持 --status/--reset 等命令 |
| `SKILL.md` | ⏳ 待更新 | 需更新文档描述 v2 语义 |
| `README.md` | ⏳ 待更新 | 需同步 v2 说明 |

---

## 🚀 可用命令

```bash
# 设置并持久化 high 模式
autothink -h "帮我设计一个电商系统"

# 后续消息自动沿用 high
autothink "数据库怎么设计？"
autothink "支付流程怎么实现？"

# 切换到 low
autothink -l "今天星期几？"

# 查看当前会话状态
autothink --status

# 重置会话（恢复默认 high）
autothink --reset

# 使用不同的 session ID
autothink --session-id my-session-123 -h "初始化设置"
```

---

## ⚙️ 高级配置

### 环境变量
- `AUTOTHINK_DEBUG=1` - 开启调试日志
- `OPENCLAW_SESSION_ID` - 显式指定会话 ID

### 编程 API
```javascript
const { AutoThinkEngine } = require('autothink');
const engine = new AutoThinkEngine();

// 直接使用
engine.setSessionThinking('sess-123', 'high');
const level = engine.detectThinkingMode('消息内容', 'sess-123', false);

// 查看状态
console.log(engine.getStatus('sess-123'));
```

---

## 🎓 发布建议

✅ **准备发布 v2.0.0**
- 更新 `_meta.json` 版本为 `2.0.0`
- 更新 `SKILL.md` 去掉自动分析描述
- 添加 v2 变更日志

---

## 📝 后续优化建议

1. **配置文件持久** - 可将状态保存到 `~/.autothink.json`，跨会话保持
2. **全局默认** - 通过 `autothink set-default high` 修改全局默认值
3. **统计信息** - 记录 token 节省量
4. **快捷命令** - `autothink on high` 等价于 `-h 消息`

---

需要我继续完善并发布 v2.0.0 吗？🐲
