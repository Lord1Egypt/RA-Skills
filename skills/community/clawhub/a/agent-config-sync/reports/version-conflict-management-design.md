# 版本冲突管理方案 — agent-config-sync v1.3.0

> **设计者**: acode (大师)
> **日期**: 2026-05-16
> **基准系统**: agent-config-sync v1.2（当前部署版本 v1.1→v1.1 pending sync）
> **适用范围**: 所有冲突场景（并发、跨会话、离线追赶、自引用、多Agent协同、回滚）

---

## 目录

1. [现状分析](#1-现状分析)
2. [冲突场景分析与解决方案](#2-冲突场景分析与解决方案)
   - [场景 A — 并发变更](#场景-a--并发变更)
   - [场景 B — 跨 AI 会话](#场景-b--跨-ai-会话)
   - [场景 C — 部分 Agent 离线](#场景-c--部分-agent-离线)
   - [场景 D — 变更冲突（鸡生蛋）](#场景-d--变更冲突鸡生蛋)
   - [场景 E — 多 Agent 联合变更](#场景-e--多-agent-联合变更)
   - [场景 F — 回滚需求](#场景-f--回滚需求)
3. [流程改进建议](#3-流程改进建议)
4. [方案依赖关系](#4-方案依赖关系)
5. [实施路线](#5-实施路线)
6. [与现有系统的兼容性说明](#6-与现有系统的兼容性说明)

---

## 1. 现状分析

### 1.1 当前部署状态

```
Master:  amaster (协调者)
Agents:  acode (编程), ainvest (投资), alive (助理)  —  3 个下游 Agent

Sync 版本: v1.1 (current) ≠ v1.0 (last_sync)  ← pending sync 待分发
```

### 1.2 核心基础设施

| 组件 | 位置 | 当前状态 | 作用 |
|:-----|:-----|:--------|:-----|
| 版本哨兵 | `memory/.current_system_version` | ✅ v1.1 | 声明当前目标版本 |
| 最后同步版本 | `memory/.last_sync_version` | ✅ v1.0 | 追踪已分发版本 |
| 变更日志 | `memory/CHANGELOG.md` | ✅ 含 v1.0-v1.1 | 结构化的变更记录 |
| 同步日志 | `memory/.sync_journal.jsonl` | ✅ 两阶段提交 | 同步原子性保障 |
| Agent 注册表 | `references/agent-registry.json` | ✅ 3 agents | Agent 单一真实来源 |
| 待处理同步 | `pending_sync_<V>_<SHA>.md` | (无待处理) | 离线 Agent 同步通知 |

### 1.3 现有版本冲突机制汇总

| 机制 | 成熟度 | 解决场景 |
|:-----|:------:|:---------|
| 版本名 pending_sync + SHA256 | ✅ 成熟 | 同名文件覆盖、完整性验证 |
| Journal 两阶段提交 | ✅ 成熟 | 部分 Agent 失败时原子性 |
| BOOTSTRAP 启动检查 | ✅ 成熟 | 跨会话恢复 |
| sentinel file 版本对比 | ✅ 成熟 | 避免重复触发 |
| CHANGELOG 影响范围字段 | ⚠️ 半成熟 | 变更路由（字段存在但未被充分利用） |
| 累积式 pending_sync（多版本共存） | ⚠️ 半成熟 | 多版本跳跃 |
| Journal 回滚标记 | ⚠️ 半成熟 | 回滚追踪（仅标记，不执行实际回滚） |

### 1.4 现有机制的不足

1. **无版本依赖链** — CHANGELOG 是线性的，但 Agent 不知道 "v3.2 的前置是 v3.1"
2. **无冲突检测** — 两个 pending_sync 文件同时存在时，没有合并策略
3. **无过期机制** — pending_sync 文件无 TTL，可能包含已被 supersede 的变更
4. **无自引用保护** — agent-config-sync 自身的修改没有隔离处理
5. **无排序约定** — 多 authors 的同时变更没有优先级定义
6. **无回滚执行** — Journal 只是标记 reverted，不实际执行回滚操作

---

## 2. 冲突场景分析与解决方案

---

### 场景 A — 并发变更

#### 问题描述

AMaster 正在分发 v3.1→v3.2 同步时，大师提交了 v3.3 代码优化。

- **时序**: AMaster 的 HEARTBEAT (time=T) 检测到 v3.2 pending → 卡在处理中
  ↓ 同时，acode 完成代码 → 通知 AMaster 写入了 v3.3 CHANGELOG → `.current_system_version` 被设为 v3.3
- **风险**: v3.2 和 v3.3 都有生成的 pending_sync 文件，agent 收到两个通知时不知所措

#### 风险分析

| 维度 | 评估 |
|:-----|:-----|
| **发生概率** | 🔴 高（3 个 Agent 活跃运行，变更频率 ≥ 1次/天） |
| **影响范围** | 🟡 中等（影响 1 次同步周期的正确性） |
| **数据风险** | 🟢 低（pending_sync 文件是幂等的，不会丢失数据） |
| **用户体验** | 🔴 高（Agent 收到两个版本通知，不知道先处理哪个） |
| **综合评级** | 🔴 **高风险** |

#### 解决方案：版本队列 + TTL 折叠

##### 核心思路

不要求 Agent 处理每个中间版本 — 允许「跳板升级」，即 v3.1 → v3.3 是安全的，前提是 v3.3 的 CHANGELOG 包含了 v3.2 的累积变更。

##### 机制设计

**A1. 版本链（VERSION_CHAIN）**

在 CHANGELOG.md 的每个版本条目中，增加 `depends_on` 字段：

```markdown
## v3.3 (2026-05-16)
**变更类型**: 🖥️ 系统代码
**影响范围**: acode, ainvest
**变更人**: acode
**紧急程度**: high
**前置版本**: v3.2
```

此字段由变更编写者声明。Agent 读取 pending_sync 时，先检查自己当前版本：
- 若 `当前版本 < 前置版本` → 需要按依赖链逐步升级
- 若 `当前版本 >= 前置版本` → 可直接应用

**A2. 版本折叠（Version Folding）**

当 Agent 发现有多个 pending_sync 文件时（v3.2 和 v3.3），按以下规则处理：

```
1. 排序: 所有 pending_sync 文件按版本号排序
2. 读取: 读取最新版本的 pending_sync 内容
3. 检查: 最新版本是否包含所有前置版本的变更（通过 depends_on 链）
4. 跳转: 若 depends_on 链覆盖 → 直接跳到最新版本
5. 不跳转: 若链断开（如 v3.2 和 v3.4，但 v3.3 是独立变更）→ 逐个处理
```

**A3. Master 端并发保护**

在 AMaster 的 HEARTBEAT sync check 中增加「分发锁」：

```
1. 读取 journal 中最后一条 prepared 记录的时间戳
2. 若 (now - ts) < 2 分钟 → 跳过本次检测，等待上轮分发完成
3. 若 (now - ts) >= 2 分钟 → 上轮可能失败，执行超时处理和重试
```

**A4. 变更原子写入**

CHANGELOG + `.current_system_version` 必须原子写入：

```
写流程:
  1. 锁定 → 写 CHANGELOG → 写 .current_system_version → 释放锁
  （使用 flock 或临时文件 + mv 原子替换）
```

#### 伪代码实现

```python
# Agent 侧: 处理多个 pending_sync 时的版本折叠
def process_pending_syncs(workspace):
    files = sorted(glob("pending_sync_v*.md"), key=extract_version)
    if not files:
        return

    if len(files) == 1:
        apply_sync(files[0])
        return

    # 多文件: 版本折叠
    latest = files[-1]
    latest_version = extract_version(latest)
    chain = build_dependency_chain(latest)

    current_ver = read_local_version()
    if current_ver in chain or is_greater_or_equal(current_ver, chain[0]):
        # 安全跳板
        apply_sync(latest)
        cleanup_all(files)  # 清理所有中间版本
    else:
        # 链断，逐个处理
        for f in files[1:]:  # 跳过第一个（已被包含在链中）
            apply_sync(f)
```

#### 所需新增字段/文件

| 新增项 | 位置 | 说明 |
|:------|:-----|:-----|
| `前置版本` 字段 | CHANGELOG.md 每个条目 | 声明前置依赖版本 |
| Dispatch lock | journal 记录 | 标记分发进行中 (status=dispatching) |
| 超时阈值配置 | agent-registry.json sync.dispatch_timeout_sec | 默认 120 秒 |

---

### 场景 B — 跨 AI 会话

#### 问题描述

今天做了一轮 P0 优化升了版本（v3.2），明天会话启动时 agent 发现 pending_sync_v3.2_xxx.md。

- **问题**: Agent 已重启，不知道这个 pending_sync 是否被后续版本覆盖。如果已经被 v3.3 覆盖，v3.2 就是 stale 的。
- **已有机制**: BOOTSTRAP 启动检查会列出并处理 pending_sync 文件

#### 风险分析

| 维度 | 评估 |
|:-----|:-----|
| **发生概率** | 🟡 中（新会话启动每天 1-3 次） |
| **影响范围** | 🟢 低（仅影响启动时的一次判断） |
| **数据风险** | 🟡 中（可能应用过时的配置覆盖新配置） |
| **用户体验** | 🟡 中（Agent 应用旧配置可能导致行为异常） |
| **综合评级** | 🟡 **中风险** |

#### 解决方案：时效性验证 + 版本对比

##### 机制设计

**B1. pending_sync 文件增加生成时间戳**

```
pending_sync_v3.2_a1b2c3d4e5f6.md

生成时间: 2026-05-15T14:30:00+08:00
过期时间: 2026-05-16T14:30:00+08:00  (TTL=24h，可在 registry 配置)
当前系统版本: v3.2
```

**B2. 启动时的时效性验证流程**

```
1. BOOTSTRAP 列出所有 pending_sync_*.md
2. 对每个文件:
   a. 提取 生成时间 + 过期时间
   b. 若 now > 过期时间 → 标记为 expired:
      - 记录到 MEMORY.md 的变更日志
      - 删除过期文件
      - 下次 heartbeat 向 AMaster 查询最新版本
   c. 若未过期 → 检查是否有更新的 pending_sync:
      - 同场景 A: 有 v3.3 文件 → 跳过 v3.2，处理 v3.3
      - 无更新文件 → 正常处理
3. 处理后删除文件
```

**B3. 版本新鲜度查询**

```
Agent 在过期文件后主动向 AMaster 查询:
  "latest_version = ?"
AMaster 返回: "v3.3, CHANGELOG see workspace-master/memory/CHANGELOG.md"
Agent 据此更新本地，跳过过期版本。
```

#### 伪代码

```python
def bootstrap_sync_check(workspace):
    files = glob("pending_sync_v*.md")
    now = int(time.time())

    valid_files = []
    for f in files:
        meta = parse_pending_sync_meta(f)
        if meta["expires_at"] and now > meta["expires_at"]:
            log_and_delete("Expired sync file: " + f)
            request_version_check_from_master()
            continue
        valid_files.append(f)

    if not valid_files:
        return

    # Version folding (same as Scenario A)
    process_pending_syncs(valid_files)
```

#### 所需新增字段

| 新增项 | 位置 | 说明 |
|:------|:-----|:-----|
| `生成时间` | pending_sync 文件头部 | ISO 8601 时间戳 |
| `过期时间` | pending_sync 文件头部 | 默认 24h，可配置 |
| `当前系统版本` | pending_sync 文件头部 | 生成时的系统版本 |
| `sync.ttl_hours` | agent-registry.json | TTL 配置项，默认 24 |

---

### 场景 C — 部分 Agent 离线

#### 问题描述

acode 正在执行大型编码任务（30 分钟+），错过了同步推送。ainvest 已经应用了 v3.2。

- **问题 1**: acode 回来后如何知道错过了多少个版本？
- **问题 2**: 如果中间 v3.2 → v3.3 → v3.4 三个版本，acode 应该逐个应用还是跳到最后？
- **已有机制**: pending_sync 累积文件 + 重试逻辑

#### 风险分析

| 维度 | 评估 |
|:-----|:-----|
| **发生概率** | 🟡 中（大型任务使 Agent 脱线 20-60 min） |
| **影响范围** | 🔴 高（错过多个版本后可能配置不一致） |
| **数据风险** | 🟡 中（版本跳跃如果冲突，配置可能损坏） |
| **用户体验** | 🟡 中（Agent 行为可能异常） |
| **综合评级** | 🔴 **高风险** |

#### 解决方案：增量追赶 + 快进折叠

##### 机制设计

**C1. Agent 本地版本追踪**

每个 Agent workspace 新增 `memory/.agent_sync_version` 文件，记录自己当前应用的系统版本：

```
~/.openclaw/workspace-acode/memory/.agent_sync_version → "v3.0"
~/.openclaw/workspace-ainvest/memory/.agent_sync_version → "v3.2"
~/.openclaw/workspace-alive/memory/.agent_sync_version → "v3.2"
```

**C2. 版本差异检测**

```
# Agent 启动/恢复时:
1. 读取自己的 .agent_sync_version → "v3.0"
2. 列出 pending_sync_v*.md → [v3.1.md, v3.2.md, v3.3.md, v3.4.md]
3. 计算版本差异: 从 v3.0 到 v3.4，缺失 v3.1-v3.4
4. 跳过标记:
   - 排序所有 pending 文件
   - 只保留本地版本之后的文件
   - 检查远程最新版本（通过 journal 查询）
```

**C3. 追赶策略**

```
策略选择:
  IF 缺失版本数 == 1:
    → 直接应用该版本
  ELIF 缺失版本数 >= 2 AND depends_on 链完整:
    → 检查版本链: v3.0 → v3.1 → v3.2 → v3.3 → v3.4
    → 若链完整: 跳跃到最新 v3.4，一次性应用
    → 更新 .agent_sync_version = v3.4
  ELIF 缺失版本数 >= 2 AND depends_on 链断:
    → 逐个应用，每步更新 .agent_sync_version
  ELSE:
    → 向 AMaster 发送消息，查询是否可以跳跃
```

**C4. Master 端重试优化**

AMaster 的 HEARTBEAT sync check 中增加「离线时长」追踪：

```
对于 journal 中 status=prepared 且 agent 为 pending 的记录:
  1. 计算 离线时长 = now - journal.ts
  2. 若 离线时长 > 1h:
     - 累积所有对应该 agent 的 pending 版本到最新版本
     - 检查当前 .current_system_version 是否更新
     - 若最新版本包含所有中间变更 → 发一个「追赶包」
  3. 若 离线时长 <= 1h:
     - 正常重试单版本分发
```

#### 所需新增文件

| 新增项 | 位置 | 说明 |
|:------|:-----|:-----|
| `.agent_sync_version` | 每个 agent workspace/memory/ | 本地已应用的版本 |
| journal.agent_offline_since | journal 记录 | Master 追踪离线时间 |

---

### 场景 D — 变更冲突（鸡生蛋）

#### 问题描述

需要修改 agent-config-sync 本身——比如升级 HEARTBEAT item 12 从 v1.2 到 v1.3，但这正是一个配置同步变更。

- **核心悖论**: 同步系统自身的文件变更需要被同步，但同步系统本身在运行中
- **风险**: 循环同步 → 同步系统分发自己的更新 → 触发了同步检查 → 再分发更新 → 无限循环

#### 风险分析

| 维度 | 评估 |
|:-----|:-----|
| **发生概率** | 🟢 低（sync 系统升级不频繁，1-2 次/月） |
| **影响范围** | 🔴 高（循环同步可导致 CPU 100% 和文件系统 I/O 爆炸） |
| **数据风险** | 🔴 高（文件被循环覆盖可能损坏） |
| **用户体验** | 🔴 高（系统不稳定） |
| **综合评级** | 🔴 **高风险（low prob, high impact）** |

#### 解决方案：隔离区 + 本身版本锁定

##### 机制设计

**D1. 同步系统文件黑名单**

在 agent-registry.json 新增字段，标记 sync 系统自身文件路径：

```json
{
  "sync": {
    "self_protect": {
      "quarantine": [
        "skills/agent-config-sync/SKILL.md",
        "skills/agent-config-sync/SECURITY.md",
        "skills/agent-config-sync/scripts/init_sync.sh",
        "skills/agent-config-sync/scripts/force_sync.sh",
        "skills/agent-config-sync/references/sync-setup.md",
        "skills/agent-config-sync/references/sync-journal.md",
        "skills/agent-config-sync/references/pending-sync-template.md",
        "skills/agent-config-sync/references/agent-registry.json"
      ],
      "sync_own_version_file": "skills/agent-config-sync/.sync_own_version",
      "allow_bootstrap_only": true
    }
  }
}
```

**D2. 隔离流程**

```
当 AMaster 检测到变更涉及 sync 系统自身文件时:

Step 1 — 验收阶段 (Master 端):
  a. 检查 CHANGELOG 条目的影响范围是否包含 agent-config-sync
  b. 若是 → 标记为「自身升级」类型
  c. 生成 isolated_sync_<VERSION>_<SHA>.md (非 pending_sync)
     - 文件放在 master workspace 而非 agent workspace
     - 内容只包含 sync 系统变更
  d. 不通过正常 HEARTBEAT 分发 — 而是写入专门的通知

Step 2 — 分发阶段:
  a. 不通过正常 sync_dispatch 流程
  b. 而是写入各 agent 的 BOOTSTRAP 头部:
     "⚠️ agent-config-sync 系统需要升级: 见 master memory/isolated_sync_vX.Y.md"
  c. Agent 下次启动时在 BOOTSTRAP 检查中看到这个通知
  d. Agent 主动向 AMaster 请求升级指令

Step 3 — 执行阶段 (Agent 端):
  a. AMaster 验证自己这边升级已完成（current >= isolated 版本）
  b. AMaster 发送 isolated_sync 文件给请求的 Agent
  c. Agent 执行: 先暂停正常 sync check，执行升级，然后重启 sync
```

**D3. 双重版本锁定**

```
sync 系统版本: skills/agent-config-sync/.sync_own_version → "v1.3"
系统配置版本: memory/.current_system_version → "v3.5"

两者独立递增:
  - .sync_own_version: 只在 agent-config-sync 自身升级时递增
  - .current_system_version: 在所有其他配置变更时递增

HEARTBEAT 检查流程:
  1. 对比 .current_system_version vs .last_sync_version
  2. 检查 CHANGELOG 中最新条目的影响范围
  3. 若影响范围包含 "agent-config-sync" → 走 isolated 流程
  4. 否则 → 走正常 sync_dispatch 流程
```

**D4. 循环检测机制**

```
HEARTBEAT 中的防循环保护:
  1. 读取 journal 最后 5 条记录
  2. 若发现连续 3 条记录涉及相同版本 → 疑似循环
  3. 终止本次分发，写入 WARNING 到 MEMORY.md
  4. 要求人工确认后继续
```

#### 伪代码

```python
def heartbeat_sync_check_enhanced():
    current = read(".current_system_version")
    last = read(".last_sync_version")

    # 循环检测
    if detect_loop(journal, current):
        log_warning("Possible sync loop detected for version: " + current)
        return

    if current == last:
        return

    # 自身升级检测
    changelog_entry = read_changelog_section(current)
    if "agent-config-sync" in changelog_entry.get("影响范围", ""):
        handle_self_upgrade(current, changelog_entry)
        return

    # 正常流程
    normal_sync_dispatch(current, last)
```

#### 所需新增文件/字段

| 新增项 | 位置 | 说明 |
|:------|:-----|:-----|
| `.sync_own_version` | skills/agent-config-sync/ | Sync 自身版本锁定 |
| `sync.self_protect` | agent-registry.json | 隔离区文件清单 |
| `isolated_sync_<V>.md` | master memory/ | 隔离同步通知文件 |
| loop_detection_count | journal 逻辑 | 最近 N 条相同版本计数 |

---

### 场景 E — 多 Agent 联合变更

#### 问题描述

元宝分析后建议调整策略参数 + 大师修改代码 + AMaster 更新配置，三者几乎同时发生。

- **问题 1**: 三个变更的版本顺序如何管理？
- **问题 2**: Agent 收到三个 pending_sync 时按什么顺序应用？
- **问题 3**: 如果变更之间有依赖（代码变更需要先于配置变更），如何保证？

#### 风险分析

| 维度 | 评估 |
|:-----|:-----|
| **发生概率** | 🟡 中（多 Agent 协作场景，每周 2-5 次） |
| **影响范围** | 🟡 中（应用顺序错误会导致功能异常） |
| **数据风险** | 🟡 中（参数不匹配可能产生错误结果） |
| **用户体验** | 🟡 中（Agent 行为不确定） |
| **综合评级** | 🟡 **中风险** |

#### 解决方案：依赖声明 + 拓扑排序 + 批量合入

##### 机制设计

**E1. 变更类型优先级矩阵**

```
┌──────────────────┬──────────────┬──────────────┬──────────────┬──────────────┐
│ 后 ↓ / 先 →       │ 🖥️系统代码    │ 🤖Agent配置   │ ⚙️OpenClaw   │ 🎯任务配置    │
├──────────────────┼──────────────┼──────────────┼──────────────┼──────────────┤
│ 🖥️系统代码        │ 版本顺序      │ 代码优先      │ 代码优先      │ 代码优先      │
│ 🤖Agent配置       │ 代码优先      │ 合并          │ 配置优先      │ 任务优先      │
│ ⚙️OpenClaw        │ 代码优先      │ 配置优先      │ 版本顺序      │ 任务优先      │
│ 🎯任务配置        │ 代码优先      │ 任务优先      │ 任务优先      │ 版本顺序      │
└──────────────────┴──────────────┴──────────────┴──────────────┴──────────────┘

规则:
  - "代码优先" = 系统代码变更应先于 Agent 配置
  - "配置优先" = Agent 配置变更应先于 OpenClaw 配置
  - "任务优先" = 任务配置（含 API Key）通常最后应用
  - "版本顺序" = 同类型变更按版本号应用
  - "合并" = 同类型可安全合并
```

**E2. CHANGELOG 依赖声明增强**

在 CHANGELOG 条目中增加 `协同依赖` 字段：

```markdown
## v3.5 (2026-05-16)
**变更类型**: 🖥️ 系统代码
**影响范围**: acode, ainvest
**变更人**: acode
**协同依赖**: v3.4 (必须)
**协同锁定**: v3.6 (等待)

### 修改
- 优化回测引擎参数计算逻辑
```

**E3. 拓扑排序逻辑**

```
当 Agent 收到多个 pending_sync 文件时:

1. 解析每个文件的依赖声明:
   v3.4 → 无依赖
   v3.5 → 依赖 v3.4
   v3.6 → 依赖 v3.4 + v3.5

2. 拓扑排序:
   应用顺序: v3.4 → v3.5 → v3.6

3. 检查环形依赖:
   v3.4 → 依赖 v3.5 → 依赖 v3.4  (循环!)
   → 标记冲突，拒绝应用，请求 AMaster 解决

4. 执行拓扑排序后的应用:

5. 全部处理完后删除所有 pending_sync 文件
```

**E4. Master 端批量合入（Batch Commit）**

AMaster 的 HEARTBEAT 可配置为「批量模式」：

```
在 agent-registry.json 中配置:
  "sync": {
    "batch_window_sec": 300,    # 5 分钟批量窗口
    "batch_mode": true
  }

批量模式逻辑:
  1. 检测到版本 mismatch
  2. 暂停立即分发，等待 batch_window_sec
  3. 窗口内新的变更累积到同一批次
  4. 窗口结束时，检查所有累积变更:
     a. 拓扑排序
     b. 合并变更（按影响范围合并到同一个版本号）
     c. 生成一个汇总的 pending_sync 文件
     d. 分发
```

**E5. 变更锁定（Change Lock）**

```
当多个变更同时进行时:
  1. 第一个发起者（如 acode）提交 v3.5 → 更新 CHANGELOG
  2. AMaster HEARTBEAT 检测到 v3.5 pending
  3. AMaster 检查 journal 是否有 prepared 状态的记录
  4. 若有 → 新变更 v3.6 进入「等待队列」
  5. v3.5 分发完成后，v3.6 自动出队
  6. 同时 AMaster 检查 v3.6 是否可以与 v3.5 合并:
     - 同一影响范围 → 建议合并（序列化 CHANGELOG）
     - 不同影响范围 → 可独立分发
```

#### 所需增强

| 新增/修改项 | 位置 | 说明 |
|:--------|:-----|:-----|
| `协同依赖` 字段 | CHANGELOG.md 每个条目 | 声明对前置版本的依赖 |
| `协同锁定` 字段 | CHANGELOG.md 每个条目 | 声明需要等待的版本 |
| 优先级矩阵 | SKILL.md / references | 作为规范文档 |
| batch_window_sec | agent-registry.json sync.* | 批量窗口配置 |
| 等待队列 | journal 中 | batch_mode 的 pending 暂存 |

---

### 场景 F — 回滚需求

#### 问题描述

v3.3 同步导致系统异常，需要回退到 v3.2。

- **问题 1**: 如何安全回滚？仅改 sentinel 文件不够
- **问题 2**: Agent 能不能 undo 之前的变更？
- **问题 3**: 如何确保回滚操作本身不会引发新的同步问题？
- **已有机制**: journal 可以标记 reverted，但无实际执行

#### 风险分析

| 维度 | 评估 |
|:-----|:-----|
| **发生概率** | 🟢 低（正常流程不会触发，只在异常时） |
| **影响范围** | 🔴 高（回滚失败会导致配置混乱） |
| **数据风险** | 🔴 高（回滚过程中数据处理不当可丢失配置） |
| **用户体验** | 🔴 高（系统不稳定） |
| **综合评级** | 🔴 **高风险（low prob, high impact）** |

#### 解决方案：快照对比 + 回滚清单 + 自校验回滚

##### 机制设计

**F1. 前置快照（Pre-Sync Snapshot）**

每次 Agent 应用同步前，自动创建被修改文件的快照：

```
~/.openclaw/workspace-acode/memory/.sync_snapshots/v3.2_pre/
├── TOOLS.md.bak
├── SOUL.md.bak
├── AGENTS.md.bak
├── config.json.bak (如果有)
└── snapshot_manifest.json   ← 快照清单
```

**snapshot_manifest.json 内容**:

```json
{
  "sync_version": "v3.2",
  "snapshot_time": "2026-05-16T08:30:00Z",
  "previous_version": "v3.1",
  "files": {
    "TOOLS.md": "sha256:a1b2c3...",
    "SOUL.md": "sha256:d4e5f6..."
  }
}
```

**F2. 回滚清单（Rollback Manifest）**

Master 端执行回滚时生成：

```markdown
# Revert Manifest — v3.3 → v3.2
**回滚原因**: v3.3 参数配置错误导致回测结果异常
**发起人**: AMaster
**回滚类型**: full

## 受影响文件
- [ ] TOOLS.md → 回退到 v3.2 快照
- [ ] config/quant_params.json → 回退到 v3.2 快照

## 受影响 Agent
- [ ] acode → 已回滚 ✅
- [ ] ainvest → 待回滚
- [ ] alive → 不适用

## 验证清单
- [ ] CHANGELOG 已添加 v3.3 revert 条目
- [ ] .current_system_version 已恢复
- [ ] 所有 pending_sync_v3.3 文件已清理
```

**F3. 回滚操作流程**

```
Step 1 — 触发 (Master 端):
  1. AMaster 写入回滚 CHANGELOG 条目:
     ## v3.3 (REVERTED — 2026-05-16)
     **回滚原因**: ...
     **回滚到**: v3.2

  2. AMaster 将 .current_system_version 设为 v3.2 (回滚后版本)
  3. system_version 降低触发 HEARTBEAT:
     - 但需特殊处理: current < last_sync

Step 2 — 分发回滚 (Master 端):
  1. HEARTBEAT 检测到 回滚变更 (revert_version 存在)
  2. 生成 revert_sync_v3.3_to_v3.2.md 文件
  3. 写入各 Agent workspace
  4. Journal 记录: {"type":"revert","from":"v3.3","to":"v3.2","status":"prepared"}

Step 3 — 应用回滚 (Agent 端):
  1. Agent 检测到 revert_sync 文件
  2. 从快照目录恢复所有 v3.2_pre 的文件
  3. 验证 SHA256 checksums
  4. 更新 .agent_sync_version = v3.2
  5. 删除 revert_sync 文件
```

**F4. 部分回滚（Selective Rollback）**

```
回滚类型:
  full:   回滚所有影响的文件
  partial: 只回滚指定文件/配置

partial 回滚清单:
  - 只恢复指定文件的快照
  - 其他文件保留 v3.3 状态
  - 版本号打补丁: v3.2.1 (partial revert of v3.3)
```

**F5. 回滚安全机制**

```
防循环:
  1. journal 记录回滚操作，标记 type=revert
  2. 回滚完成后，对比 .current == .last_sync
  3. 下一轮 HEARTBEAT 发现相同 → skip
  4. 防止: 回滚 → 再回滚 → 再回滚 的无限循环

防覆盖:
  1. 回滚前检查有无新的 pending_sync 文件
  2. 若有 → 撤回回滚操作，先处理新的变更
  3. 若变更与回滚冲突 → 停止，要求人工决策
```

#### 所需新增文件

| 新增项 | 位置 | 说明 |
|:------|:-----|:-----|
| `.sync_snapshots/` | 每个 agent workspace/memory/ | 同步前快照目录 |
| `snapshot_manifest.json` | 快照目录中 | 快照清单 + checksums |
| `revert_sync_<X>_to_<Y>.md` | agent workspace | 回滚通知文件 |
| `Revert Manifest` | master memory/ | 回滚清单文档 |

---

## 3. 流程改进建议

### 3.1 HEARTBEAT item 12 改进

#### 当前版本 (v1.2)

```
12. ⭐ 配置变更强制同步
    - 哨兵文件对比
    - 不一致时: 读 CHANGELOG → 生成签名 → 推送/写文件 → 记 journal
    - 触发类型枚举
    - 成功更新 last_sync
    - 失败不阻断 heartbeat
    - 重试 pending 记录
```

#### 建议 v1.3 增强版

```
12. ⭐ 配置变更同步（含版本冲突管理）
    ┌─ 前置检查 ────────────────────────────────────────────
    │ a. 循环检测: 检查 journal 最近 5 条，连续 3 条相同版本 → 报警跳过
    │ b. 分发锁: 上轮 prepared < 2min → 跳过；>= 2min → 超时处理
    │ c. 自身升级: 影响范围含 "agent-config-sync" → 走 isolated 流程
    ├─ 版本检测 ────────────────────────────────────────────
    │ d. 哨兵对比: .current != .last_sync → 有新版本
    │ e. 回滚检测: current < last_sync → 回滚操作，走 revert 流程
    │ f. 批量窗口: batch_mode=true → 等待 batch_window_sec，合并后分发
    ├─ 分发准备 ────────────────────────────────────────────
    │ g. 读 CHANGELOG 最新版本 (含 depends_on / 协同依赖字段)
    │ h. 动态获取 agent 列表 (registry)
    │ i. 生成 SHA256 签名 + TTL 过期时间
    │ j. PREPARE journal 记录 (含版本链信息)
    ├─ 分发执行 ────────────────────────────────────────────
    │ k. 逐个 agent: sessions_send 优先, pending_sync 回退
    │ l. 离线检测: 若 agent 已离线 > 1h → 生成累积追赶包
    │ m. COMMIT journal: 全部 done → committed; 部分 done → prepared
    └─ 收尾 ────────────────────────────────────────────────
    │ n. 更新 .last_sync_version
    │ o. 清理超过 TTL 的过期 prepared 记录 → abandoned
    │ p. 失败不阻断 heartbeat
```

### 3.2 pending_sync 流程改进

#### 改进内容

| # | 改进项 | 说明 |
|:--|:------|:-----|
| 1 | 文件头增强 | 增加生成时间、过期时间、当前版本字段 |
| 2 | 版本链嵌入 | 嵌入 depends_on 依赖链信息 |
| 3 | 类型标记 | pending_sync (正常) / revert_sync (回滚) / isolated_sync (自身升级) |
| 4 | 版本折叠 | Agent 收到多文件时，按优先级矩阵 + 拓扑排序处理 |
| 5 | 快照先于应用 | 应用变更前自动创建前置快照 |

#### 新文件模板

```markdown
# pending_sync_v3.5_a1b2c3d4.md

**类型**: pending_sync
**版本**: v3.5
**前置**: v3.4
**生成时间**: 2026-05-16T08:30:00+08:00
**过期时间**: 2026-05-17T08:30:00+08:00
**紧急程度**: high
**签名**: a1b2c3d4e5f6

## 变更详情
(从 CHANGELOG 提取的最新版本条目)

## 操作指令
1. 创建前置快照: mkdir -p memory/.sync_snapshots/v3.5_pre/
2. 备份受影响文件到快照目录
3. 应用变更
4. 更新 memory/.agent_sync_version = v3.5
5. 删除本文件
```

### 3.3 Journal 改进

#### 当前格式

```jsonl
{"ts":"...","from":"v3.0","to":"v3.1","status":"prepared","agents":{"acode":"pending",...}}
```

#### 建议 v1.3 格式

```jsonl
{
  "ts": "2026-05-16T08:30:00Z",
  "type": "normal|revert|isolated",
  "from": "v3.0",
  "to": "v3.1",
  "depends_on": "v3.0",
  "status": "prepared|dispatching|committed|failed|reverted|abandoned",
  "agents": {
    "acode": {"status": "done", "ts": "..."},
    "ainvest": {"status": "pending", "ts": "..."},
    "alive": {"status": "skipped", "reason": "no_affected_files"}
  },
  "changelog_section": "🖥️ 系统代码",
  "ttl_hours": 24,
  "batch_id": "batch_20260516_001",
  "loop_counter": 0
}
```

#### 改进说明

| 新增字段 | 作用 |
|:--------|:-----|
| `type` | 区分 normal / revert / isolated，用于后续处理路由 |
| `depends_on` | 在 journal 层面记录版本链 |
| `agents.<id>.status` | 增加 skipped 状态（agent 不受影响时跳过） |
| `agents.<id>.ts` | 每个 agent 的最后操作时间戳 |
| `changelog_section` | 从 CHANGELOG 提取变更类型，方便快速检索 |
| `ttl_hours` | 同步的有效期，超时后标记 abandoned |
| `batch_id` | 批量窗口分组 ID |
| `loop_counter` | 循环检测计数器 |

---

## 4. 方案依赖关系

### 4.1 改进项的依赖图

```
Phase 1 (基础层)
  ├─ P1.1: pending_sync 文件头增强 (时间戳 + TTL)
  ├─ P1.2: Agent .agent_sync_version 文件
  └─ P1.3: 变更原子写入 (flock / mv 替换)
      │
      ▼
Phase 2 (核心层)
  ├─ P2.1: CHANGELOG depends_on 字段
  │    └─ 前置: P1.1 (P1.2 可选)
  ├─ P2.2: 版本折叠 + 拓扑排序 (Agent 端)
  │    └─ 前置: P1.1, P1.2, P2.1
  ├─ P2.3: Master 端分发锁 + 超时处理
  │    └─ 前置: 无 (独立改进)
  ├─ P2.4: 离线追赶包
  │    └─ 前置: P1.2, P2.1
  └─ P2.5: 循环检测
       └─ 前置: P2.3
      │
      ▼
Phase 3 (高级层)
  ├─ P3.1: 自身升级隔离 (isolated_sync)
  │    └─ 前置: P2.5 (blacklist), P1.3 (原子写入)
  ├─ P3.2: 批量合入 (batch mode)
  │    └─ 前置: P2.1, P2.2
  ├─ P3.3: 回滚快照 + 回滚清单
  │    └─ 前置: P1.1, P2.2, P3.1 (自身保护)
  └─ P3.4: HEARTBEAT item 12 v1.3 完整重写
       └─ 前置: 所有 Phase 2 项
```

### 4.2 依赖矩阵

| ↙ 依赖 / 被依赖 → | P1.1 | P1.2 | P1.3 | P2.1 | P2.2 | P2.3 | P2.4 | P2.5 | P3.1 | P3.2 | P3.3 | P3.4 |
|:-------------------|:----:|:----:|:----:|:----:|:----:|:----:|:----:|:----:|:----:|:----:|:----:|:----:|
| P1.1 (文件头增强)        |  -   |  ○   |  ○   |  ●   |  ●   |  ○   |  ○   |  ○   |  ●   |  ○   |  ●   |  ○   |
| P1.2 (.agent_sync)     |  ○   |  -   |  ○   |  ○   |  ●   |  ○   |  ●   |  ○   |  ○   |  ○   |  ○   |  ○   |
| P1.3 (原子写入)         |  ○   |  ○   |  -   |  ○   |  ○   |  ○   |  ○   |  ○   |  ●   |  ○   |  ○   |  ○   |
| P2.1 (depends_on)     |  ●   |  ○   |  ○   |  -   |  ●   |  ○   |  ●   |  ○   |  ○   |  ●   |  ○   |  ○   |
| P2.2 (版本折叠)         |  ●   |  ●   |  ○   |  ●   |  -   |  ○   |  ○   |  ○   |  ○   |  ●   |  ●   |  ●   |
| P2.3 (分发锁)           |  ○   |  ○   |  ○   |  ○   |  ○   |  -   |  ○   |  ●   |  ○   |  ●   |  ○   |  ●   |
| P2.4 (离线追赶)         |  ○   |  ●   |  ○   |  ●   |  ○   |  ○   |  -   |  ○   |  ○   |  ○   |  ○   |  ●   |
| P2.5 (循环检测)         |  ○   |  ○   |  ○   |  ○   |  ○   |  ●   |  ○   |  -   |  ●   |  ○   |  ○   |  ●   |
| P3.1 (自身隔离)         |  ●   |  ○   |  ●   |  ○   |  ○   |  ○   |  ○   |  ●   |  -   |  ○   |  ●   |  ●   |
| P3.2 (批量合入)         |  ○   |  ○   |  ○   |  ●   |  ●   |  ●   |  ○   |  ○   |  ○   |  -   |  ○   |  ●   |
| P3.3 (回滚)             |  ●   |  ○   |  ○   |  ○   |  ●   |  ○   |  ○   |  ○   |  ●   |  ○   |  -   |  ●   |
| P3.4 (HEARTBEAT v1.3) |  ○   |  ○   |  ○   |  ○   |  ●   |  ●   |  ●   |  ●   |  ●   |  ●   |  ●   |  -   |

> ● = 必须前置, ○ = 可选/无依赖

---

## 5. 实施路线

### 5.1 Phase 划分

#### Phase 1 — 基础增强 (预估: 2-3 小时)

**目标**: 为后续所有冲突管理机制打好基础

| ID | 任务 | 工作量 | 影响文件 |
|:---|:-----|:------:|:---------|
| P1.1 | pending_sync 模板增加生成时间、过期时间、版本字段 | 30 min | pending-sync-template.md |
| P1.2 | 初始化脚本增加 `.agent_sync_version` 创建 | 30 min | init_sync.sh |
| P1.3 | force_sync.sh 增加原子写入 (flock / tempfile+mv) | 45 min | force_sync.sh, init_sync.sh |
| P1.4 | SECURITY.md 更新：增加版本冲突场景的权限说明 | 30 min | SECURITY.md |
| P1.5 | SKILL.md 更新：增加 Version Conflict Management 章节 | 45 min | SKILL.md |

**验收标准**:
- [ ] `pending_sync_vX.Y_<SHA>.md` 文件包含生成时间、过期时间、当前版本
- [ ] 每个 agent 的 `memory/.agent_sync_version` 文件存在
- [ ] 原子写入通过并发测试（两个进程同时写，不会损坏）

#### Phase 2 — 核心冲突处理 (预估: 4-6 小时)

**目标**: 解决 A/B/C 三个最常发生的冲突场景

| ID | 任务 | 工作量 | 影响文件 |
|:---|:-----|:------:|:---------|
| P2.1 | CHANGELOG depends_on 字段规范 + 模板更新 | 30 min | sync-setup.md, CHANGELOG.md |
| P2.2 | Agent 端版本折叠逻辑（伪代码 → SKILL.md 规范） | 1.5h | SKILL.md, pending-sync-template.md |
| P2.3 | Master 端分发锁 + 超时处理 | 1h | SKILL.md, sync-setup.md |
| P2.4 | 离线追赶包生成逻辑 | 1h | SKILL.md, sync-setup.md |
| P2.5 | 循环检测机制（journal 最近 N 条分析） | 1h | SKILL.md, sync-journal.md |
| P2.6 | sync-setup.md 重写 HEARTBEAT item 12 伪代码 | 1h | sync-setup.md |

**验收标准**:
- [ ] 并发变更时不会产生混乱的 pending_sync 文件
- [ ] Agent 能正确跳过过期/被覆盖的 pending_sync
- [ ] 离线 agent 回来后能检测到版本差距并追赶
- [ ] 循环检测能在 3 次重复分发后自动终止

#### Phase 3 — 高级场景处理 (预估: 6-8 小时)

**目标**: 解决 D/E/F 三个高影响低概率场景

| ID | 任务 | 工作量 | 影响文件 |
|:---|:-----|:------:|:---------|
| P3.1 | 自身升级隔离（self_protect 配置 + isolated_sync 流程） | 2h | agent-registry.json, SKILL.md, SECURITY.md |
| P3.2 | 批量合入（batch_mode + batch_window 配置) | 1.5h | agent-registry.json, sync-setup.md |
| P3.3 | 回滚快照机制 (snapshot_manifest + revert 流程) | 2h | SKILL.md, sync-setup.md, SECURITY.md |
| P3.4 | HEARTBEAT item 12 v1.3 完整重写 | 1.5h | sync-setup.md, quickstart.md |
| P3.5 | 全量集成测试 + 报告 | 1h | reports/ |

**验收标准**:
- [ ] agent-config-sync 自身升级走 isolated 流程，不触发循环
- [ ] 批量模式可在 5 分钟内合并多个变更并正确分发
- [ ] 回滚可以恢复到指定版本的快照，所有 agent 一致性恢复
- [ ] 所有 6 个场景通过集成测试

### 5.2 预估总工作量

| Phase | 时间 | 风险 |
|:------|:----:|:-----|
| Phase 1 — 基础增强 | 2-3h | 🟢 低 |
| Phase 2 — 核心冲突 | 4-6h | 🟡 中 |
| Phase 3 — 高级场景 | 6-8h | 🟡 中 |
| **总计** | **12-17h** | — |

### 5.3 建议实施节奏

```
Week 1:
  Day 1-2: Phase 1 (基础增强)
  Day 3-5: Phase 2.1-2.3 (并发处理 + 跨会话)
  Day 5-7: Phase 2.4-2.6 (离线追赶 + 循环检测)

Week 2:
  Day 8-9: Phase 3.1 (自身升级隔离)
  Day 10-11: Phase 3.2-3.3 (批量合入 + 回滚)
  Day 12: Phase 3.4 (HEARTBEAT 重写)
  Day 13-14: Phase 3.5 (测试 + 文档)
```

---

## 6. 与现有系统的兼容性说明

### 6.1 向后兼容

| 现有功能 | 兼容性 | 说明 |
|:--------|:------:|:-----|
| 版本哨兵文件 | ✅ 完全兼容 | `.current_system_version` / `.last_sync_version` 格式不变 |
| CHANGELOG.md | ✅ 完全兼容 | 新增字段为可选；旧版条目缺少 `depends_on` 时默认为无依赖 |
| .sync_journal.jsonl | ✅ 完全兼容 | 新增字段为可选项；旧记录缺少 type/ttl 等字段时使用默认值 |
| agent-registry.json | ✅ 完全兼容 | 新增 sync.* 字段为可选项；旧 registry 默认不启用新功能 |
| pending_sync 文件命名 | ✅ 完全兼容 | 文件头新增字段不影响文件识别（`ls pending_sync_*.md` 不变） |
| BOOTSTRAP 检查 | ✅ 增强 | 原有逻辑不变，增加时效性检查和版本折叠 |
| HEARTBEAT sync check | ✅ 增强 | 原有逻辑不变，增加循环检测/分发锁/回滚检测分支 |
| force_sync.sh | ✅ 增强 | 增加 `--confirm` 安全机制和原子写入；原有调用不变 |
| init_sync.sh | ✅ 增强 | 增加 `.agent_sync_version` 创建和 `.sync_snapshots/` 目录 |

### 6.2 升级路径

```
v1.2 (当前) → v1.3 (Phase 1) → v1.4 (Phase 2) → v2.0 (Phase 3)

v1.2 → v1.3:
  - 运行 init_sync.sh 更新 agent 端文件
  - 更新 agent-registry.json 增加 sync.ttl_hours 等新字段
  - 零破坏性变更

v1.3 → v1.4:
  - 更新 CHANGELOG 条目模板（增加 depends_on 字段）
  - 更新 HEARTBEAT item 12
  - 需要所有 agent 重新运行 init_sync.sh
  - 兼容旧版 pending_sync 文件（缺少新字段的默认为无过期时间）

v1.4 → v2.0:
  - 重大升级：自身隔离 + 批量模式 + 回滚快照
  - 需要所有 agent 停止后重新初始化
  - 需要创建 .sync_snapshots 目录
  - 建议在维护窗口内执行
```

### 6.3 不兼容场景及缓解措施

| 场景 | 风险 | 缓解 |
|:-----|:-----|:-----|
| v1.2 agent 收到 v2.0 pending_sync | 新字段无法解析 | v2.0 文件保留旧格式兼容字段（fallback） |
| v2.0 master 分发到 v1.2 agent | 回滚类型无法识别 | type 字段默认为 "normal"，不影响 v1.2 处理 |
| journal 格式升级 | 旧工具无法读新格式 | JSONL 格式不变，新增字段为可选 |
| agent-registry.json 结构变化 | 旧脚本解析失败 | 新增字段放在 sync.* 下，原有结构不变 |

### 6.4 RAM 兼容性

系统 3.5GB RAM 限制下的设计考量：

| 设计决策 | RAM 影响 | 说明 |
|:--------|:--------:|:-----|
| 文件级快照（非全量备份） | < 5 MB | 只快照被修改的文件，非整个 workspace |
| pending_sync 增量读取 | < 1 MB | 每个文件 < 5 KB，最多 10 个文件 |
| journal 最近 5 条分析 | < 5 KB | 只读最近 5 行，非全量加载 |
| 版本折叠（内存排序） | < 1 MB | 最多排序 10 个文件名 |
| 无新增进程 | 0 额外进程 | 所有逻辑为脚本中新增分支，不额外启动服务 |
| 无新增缓存 | 0 额外缓存 | 不使用 Redis/内存缓存 |

### 6.5 回退方案

如果 v2.0 出现问题：

```
紧急回退步骤:
  1. 停止所有 agent heartbeat
  2. 恢复 agent-registry.json 到 v1.2 备份
  3. 删除 .agent_sync_version 文件（可选，不影响 v1.2 运行）
  4. 删除 .sync_snapshots/ 目录（可选）
  5. 删除 pending_sync 文件中新增的头部字段行（或直接删除重新生成）
  6. 确认 CHANGELOG.md 中的 depends_on 字段不影响 v1.2 读取（可选字段）
  7. 重启 agent，v1.2 逻辑正常运行
```

---

## 附录

### A. 变更类型与优先级矩阵（完整版）

| 变更类型 | 图标 | 变更频率 | 影响范围 | 默认优先级 | 回滚难度 |
|:--------|:----:|:--------:|:--------:|:--------:|:--------:|
| 系统代码迭代 | 🖥️ | 中 | acode + all | high | 🟡 中 |
| OpenClaw 配置 | ⚙️ | 低 | all | high | 🟢 低 |
| 智能体配置 | 🤖 | 低 | 特定 agent(s) | normal | 🟢 低 |
| 任务/工作配置 | 🎯 | 中 | 特定 agent(s) | normal | 🟢 低 |
| 同步系统自身 | 🏗️ | 很低 | all (自身) | high | 🔴 高 |
| 回滚操作 | ↩️ | 很低 | 受影响的 agent | critical | 🔴 高 |

### B. Journal 状态机（v1.3）

```
                  ┌─────────┐
                  │ prepared │ ← 初始状态（版本 mismatch 检测到时）
                  └────┬─────┘
                       │
              ┌────────┼────────┐
              ▼        ▼        ▼
        ┌─────────┐ ┌─────────┐ ┌───────────┐
        │dispatching│ │ timeout │ │ abandoned │ (超过 TTL)
        └────┬─────┘ └────┬────┘ └───────────┘
             │             │
        ┌────┼────┐        └───→ 重试 → prepared
        ▼    ▼    ▼
   ┌─────────┐ ┌──────┐ ┌────────┐
   │committed│ │failed│ │reverted│
   └─────────┘ └──────┘ └────────┘
```

### C. 文件结构完整图（v2.0）

```
~/.openclaw/
├── workspace-amaster/          ← Master
│   ├── memory/
│   │   ├── .current_system_version
│   │   ├── .last_sync_version
│   │   ├── CHANGELOG.md
│   │   ├── .sync_journal.jsonl
│   │   ├── isolated_sync_<V>.md       ← 新增：自身升级隔离通知
│   │   ├── revert_manifest_<V>.md     ← 新增：回滚清单
│   │   └── batch_manifest_<ID>.json   ← 新增：批量合入清单
│   └── HEARTBEAT.md (含 item 12 v1.3)
│
├── workspace-acode/            ← Agent
│   ├── memory/
│   │   ├── .agent_sync_version        ← 新增：本地版本追踪
│   │   └── .sync_snapshots/           ← 新增：前置快照
│   │       ├── v3.2_pre/
│   │       │   ├── TOOLS.md.bak
│   │       │   └── snapshot_manifest.json
│   │       └── v3.3_pre/
│   ├── pending_sync_v*.md
│   ├── revert_sync_v*_to_v*.md        ← 新增：回滚通知
│   ├── BOOTSTRAP.md (含 sync 检查增强)
│   └── HEARTBEAT.md (含 sync 检查增强)
│
├── workspace-ainvest/
├── workspace-alive/
│
└── skills/agent-config-sync/
    ├── .sync_own_version              ← 新增：sync 自身版本锁定
    ├── SKILL.md                       (v2.0 更新)
    ├── SECURITY.md                    (v2.0 更新)
    ├── scripts/
    │   ├── init_sync.sh               (v2.0 更新)
    │   └── force_sync.sh              (v2.0 更新)
    └── references/
        ├── agent-registry.json        (v2.0 更新)
        ├── sync-setup.md              (v2.0 更新)
        ├── sync-journal.md            (v2.0 更新)
        ├── pending-sync-template.md   (v2.0 更新)
        └── quickstart.md              (v2.0 更新)
```

### D. 各场景与 Phase 的映射关系

| 场景 | Phase 1 覆盖 | Phase 2 覆盖 | Phase 3 覆盖 |
|:-----|:-----------:|:-----------:|:-----------:|
| A — 并发变更 | P1.3 (原子写入) | P2.1, P2.2, P2.3, P2.5 | P3.2 (批量合入) |
| B — 跨会话 | P1.1 (TTL/时间戳) | P2.2 (版本折叠) | — |
| C — 离线追赶 | P1.2 (版本追踪) | P2.1, P2.2, P2.4 | — |
| D — 鸡生蛋 | P1.3 (原子写入) | P2.5 (循环检测) | P3.1 (完全隔离) |
| E — 多Agent协同 | P1.1, P1.2 | P2.1, P2.2 | P3.2 (批量) |
| F — 回滚 | P1.1 | P2.2 (版本折叠) | P3.1 (自身保护), P3.3 |

---

> **报告路径**: `/home/admin/.openclaw/workspace-amaster/skills/agent-config-sync/reports/version-conflict-management-design.md`
>
> **下一步**: AMaster 审阅后决定实施优先级，acode 按 Phase 顺序逐步实现。
