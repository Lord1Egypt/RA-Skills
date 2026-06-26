# Agent 配置体系 · 操作手册

> 版本: 2.0 | 更新: 2026-05-12

---

## 体系总览

```
                    ┌──────────────────────────┐
                    │   PROTOCOL.md (协议层)    │
                    │   抽象规则，不含业务内容    │
                    └──────────┬───────────────┘
                               │ 被引用
            ┌──────────────────┼──────────────────┐
            ▼                  ▼                  ▼
    ┌───────────────┐  ┌───────────────┐  ┌───────────────┐
    │ 4 个 TEMPLATE │  │ scaffold.sh   │  │ OPERATIONS.md │
    │ 文件格式标准   │  │ 自动化脚手架   │  │ 本文件        │
    └───────┬───────┘  └───────────────┘  └───────────────┘
            │ 定义格式
            ▼
    ┌───────────────────────────────────────────────┐
    │            openclaw.json (配置层)              │
    │     agent 定义 / skills / allowAgents         │
    └───────────────────────┬───────────────────────┘
                            │
            ┌───────────────┼───────────────┐
            ▼               ▼               ▼
    ┌──────────────┐ ┌──────────────┐ ┌──────────────┐
    │ {domain1}    │ │ {domain2}    │ │ {domain3}    │ ...
    │ N agents     │ │ N agents     │ │ N agents     │
    │ M 个MD文件    │ │ M 个MD文件   │ │ M 个MD文件    │
    └──────────────┘ └──────────────┘ └──────────────┘
```

---

## 协议如何被应用

协议不是"被参考的文档"，而是**被嵌入到每个 agent 的运行指令中**。

### 流转路径

```
PROTOCOL.md 定义规则
    ↓
TEMPLATE_*.md 定义文件结构（含「协议实现」章节）
    ↓
scaffold-domain.sh 从模板生成 agent 文件
    ↓
每个 AGENTS.md 顶部有「协议实现」表：
    §1 架构 → 我是 L1/L2，职责是什么
    §3.1 任务格式 → 我如何解析输入
    §3.2 回复格式 → 我必须用 <agent-response> 块
    §4 错误 → 超时重试 1 次 → 降级
    §5.1 spawn → 用 sessions_spawn 调子 agent
    ↓
agent 运行时读取 AGENTS.md → 自动遵循协议
```

### 协议变更如何传播

| 场景 | 需要改什么 |
|------|-----------|
| 协议新增章节（如 §6） | 1. 更新 PROTOCOL.md（规则） 2. 更新 TEMPLATE_AGENTS.md（模板） 3. 逐个 agent AGENTS.md 补充协议实现 |
| 协议修改现有章节 | 更新 PROTOCOL.md，模板和 agent 文件如受影响则同步 |
| 新增业务域 | 不改协议，跑 scaffold.sh |
| 删除业务域 | 从 openclaw.json 移除 + 删目录，不动协议 |

---

## 新增业务域（5 步）

### 方法一：脚手架（推荐）

```bash
cd ~/.openclaw/protocol
bash scaffold-domain.sh <域标> <经理名> "<spec1:角色1> <spec2:角色2>"
```

输出会自动生成：
- 完整的工作区目录和文件
- openclaw.json 配置片段
- sessions 目录创建命令

**然后手工做的事：**
1. 复制 JSON 到 openclaw.json
2. 编辑每个 agent 的业务特有占位符（核心信条、工作流、输出标准）
3. 创建 sessions 目录
4. 重启 Gateway

### 方法二：手动（理解原理用）

```
步骤 1: 拷贝模板 → 填写变量 → 保存到 workspace/{domain}/{role}/
步骤 2: openclaw.json → agents.list 追加新 agent
步骤 3: openclaw.json → defaults.subagents.allowAgents 追加
步骤 4: openclaw.json → main.subagents.allowAgents 追加 Manager
步骤 5: mkdir agents/{domain}/{role}/sessions
```

---

## 删除业务域

```
1. 从 openclaw.json agents.list 删除对应条目
2. 从 defaults.subagents.allowAgents 删除
3. 从 main.subagents.allowAgents 删除
4. rm -rf workspace/{domain}
5. rm -rf agents/{domain}
6. 重启 Gateway
```

---

## 修改现有 agent

### 改一个 agent 的操作流程

```
1. 直接编辑 workspace/{domain}/{role}/ 下的 MD 文件
2. 如果要改的是通用结构 → 先改 TEMPLATE_*.md，再改 agent 文件
3. 改 openclaw.json 中的 skills/allowAgents/model
4. 重启 Gateway
```

### 不改什么

| 场景 | 不该做的事 |
|------|-----------|
| 只想调一个 agent 的工作流程 | 不要改模板（那是全局标准） |
| 只想加一个子 agent | 不要改协议（协议不含业务内容） |
| 只想改一段文案 | 不要动 openclaw.json（那是路由配置） |

---

## 文件职责矩阵

| 文件 | 管什么 | 不管什么 |
|------|--------|---------|
| **PROTOCOL.md** | 通信契约、调用规范、错误策略 | 具体业务、具体 agent |
| **TEMPLATE_*.md** | agent 文件格式标准 | 业务内容 |
| **scaffold.sh** | 从模板生成新域 | 已有域的管理 |
| **openclaw.json** | agent 路由、模型、白名单 | agent 行为逻辑 |
| **AGENTS.md** | 一个 agent 的工作流程、反模式 | 全局协议（它只引用） |
| **IDENTITY.md** | agent 标识元数据 | 行为规范 |
| **SOUL.md** | 价值观、红线 | 操作流程 |
| **USER.md** | 服务对象、服务标准 | agent 内部逻辑 |

---

## 当前状态

| 指标 | 数值（示例） |
|------|:-----------:|
| 业务域 | N 个（如 fintech / ecommerce / marketing） |
| Agent 总数 | N |
| 配置文件 | N 个 MD 文件，与模板 v2.0 一致 |
| 模板 | 4 个 TEMPLATE_*.md |
| 工具 | scaffold.sh |
