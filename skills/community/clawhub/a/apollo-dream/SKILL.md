---
name: apollo-dream
description: >
  像睡觉做梦一样整理记忆，把重要的留下，不重要的忘掉。
version: 2.0.0
read_when:
  - 对话超过20轮时
  - Token快用完时
  - 需要整理上下文时
  - 任务完成后需要总结时
  - AI开始表现迟钝时
  - 需要建立记忆关联时
metadata:
  openclaw:
    emoji: "🌙"
    requires:
      bins: []
      env: []
    triggers:
      - 做梦
      - 记忆整理
      - 遗忘
      - 记忆关联
      - 上下文管理
      - 上下文压缩
    suite: apollo
---

# Apollo Dream - 做梦记忆机制

## 核心准则

**AI的记忆管理应该像人类睡眠中的做梦机制：在梦中整理记忆、强化重要连接、忘却无关细节。**

人类睡眠时大脑在做什么：
- **强化**：把短期记忆巩固成长期记忆
- **关联**：找到记忆和记忆之间的联系
- **忘却**：删除不重要的细节
- **重组**：把碎片化的记忆重新组织

## 三级做梦机制

| 层级 | 名称 | 类比 | 做什么 |
|------|------|------|--------|
| 1 | Microcompact | 浅睡呼吸 | 快速删token，不动结构 |
| 2 | Session Memory | REM睡眠整理 | 基于会话记忆压缩，保留结构 |
| 3 | Traditional Compact | 深度睡眠重组 | 完整摘要，建立记忆关联 |

## 触发时机

**应该触发做梦的场景：**
- 对话超过20轮
- Token使用超过70%
- 任务完成时
- 发现多个记忆点需要关联时
- AI开始表现迟钝/重复

## 做梦的操作

### ✅ 能实现的

```
1. 提炼关键结论 → 写到文件
2. 删除中间过程 → 只保留首尾状态
3. 保留重要上下文 → 关键决策、用户偏好
4. 跨会话关联 → 发现新旧记忆的联系
5. 忘却噪音 → 删除不重要的细节
```

### ❌ 待实现的（未来工作）

```
1. 自动发现记忆关联
   - 需要：跨会话知识图谱
   - 状态：待设计

2. 主动忘却机制
   - 需要：重要性评分系统
   - 状态：待设计

3. 记忆可视化
   - 需要：定期输出记忆地图
   - 状态：待设计
```

## 人类睡眠vs AI做梦

| 人类睡眠 | AI做梦 |
|---------|--------|
| 短期记忆→长期记忆 | 对话→文件 |
| 记忆关联 | 知识图谱 |
| 忘却不重要的事 | 丢弃token |
| REM整理 | 分层压缩 |

## 任务完成后的做梦流程

```
任务完成 →
  1. 提炼核心结论（what was done, key decisions）
  2. 提取重要发现（insights worth remembering）
  3. 记录未解决问题（for follow-up）
  4. 检查是否有记忆关联（与旧记忆的联系）
  5. 忘却噪音（不重要细节删除）
  6. 写入适当文件（memory/YYYY-MM-DD.md 或专题文件）
  7. 清理对话上下文
```

## 应用检查表

- [ ] 当前对话轮数是否超过20轮？
- [ ] Token使用是否超过70%？
- [ ] 当前任务是否已有明确结论可以提炼？
- [ ] 是否有应该写入文件的长期知识？
- [ ] 新记忆是否与旧记忆有关联？

## 待实现功能（TODO）

| 功能 | 描述 | 优先级 |
|------|------|--------|
| 记忆关联发现 | 自动发现新旧记忆之间的联系 | 高 |
| 重要性评分 | 给每条记忆打分，决定保留/忘却 | 中 |
| 主动忘却 | 不重要的记忆自动降级/删除 | 中 |
| 记忆可视化 | 输出记忆地图供人类阅读 | 低 |

## 参考

来源：Claude Code 上下文管理机制 + 人类睡眠记忆研究，512,000行源码研究

---

## v2.0 实施规格（2026-04-07）

### v2新功能

1. **Token精度算法**：使用字符/词/标点综合估算（scripts/token-estimator.py）
2. **信息密度检测**：识别高价值/低价值内容（scripts/density-detector.py）
3. **三层压缩**：Microcompact/Session Memory/Deep Compact（scripts/compressor.py）
4. **7天快照**：自动创建/清理记忆快照（scripts/snapshot.py）
5. **决策追踪**：识别并记录关键决策（scripts/decision-tracker.py）

### v1 实施规格（2026-04-06）

> 以下是 v1 最小可运行版本的实现规格。

### 触发指标（v1）

| 指标 | 定义 | 阈值 | 检测方式 |
|------|------|------|---------|
| 工作记忆积压 | 有 next_step 但 stale>=3轮 的任务数 | ≥ 3 | task-state.sh |
| 未闭合话题 | status=active/pending 的话题数 | ≥ 3 | topic-tracker.sh |
| 决策滞留率 | 有决策点但≥2轮未决策的任务数 | ≥ 2 | task-state.sh |
| Token使用率 | 当前会话token估算 | > 70000 | 对话历史文件大小 |

**触发规则：**
- 软触发：任一 backlog/unclosed/decision_latency 超过阈值
- 硬触发：Token > 70000（不可绕过）

### 独立裁判机制

心跳cron每次触发时，自动运行碎片化检测脚本：
```
heartbeat-logger.sh → 调用 dream-fragmentation-check.sh
```

检测结果写入：
- `/tmp/.dream-trigger` — 存在则主AI必须整理
- `/tmp/heartbeat-realtime.json` — 含 dream_trigger 字段

### 任务状态管理（主AI调用）

```bash
# 注册任务（开始时）
dream/task-state.sh register <id> <goal> <next_step>

# 推进了一步（重置stale轮次）
dream/task-state.sh update <id> --advance

# 已做决策
dream/task-state.sh update <id> --decide

# 完成任务（移除）
dream/task-state.sh close <id>

# 所有任务stale轮次+1（每次心跳后）
dream/task-state.sh stale

# 列出所有任务
dream/task-state.sh list
```

### 话题追踪（主AI调用）

```bash
# 标记新话题开始
dream/topic-tracker.sh mark <topic_name>

# 切换话题（自动pause旧话题）
dream/topic-tracker.sh switch <new_topic>

# 标记当前话题完成
dream/topic-tracker.sh done

# 标记当前话题暂停
dream/topic-tracker.sh pause

# 列出所有话题
dream/topic-tracker.sh list
```

### v1 整理流程

当 `/tmp/.dream-trigger` 存在时，主AI必须执行以下整理流程：

```
Step 1: 全量扫描（只读）
  → 读取 task-state + topic-state + 对话历史
  → 识别：决策、任务、偏好、未闭合回路

Step 2: 结构化抽取
  → 输出：任务列表、决策日志、实体表

Step 3: 冲突检测 + 去重
  → 发现：自相矛盾、重复定义、版本漂移

Step 4: 写入长期记忆
  → memory/YYYY-MM-DD.md
  → 相关专题文件

Step 5: 状态决策（关键步骤）
  → 逐个任务判断：
    - 推进（advance）：更新 next_step，重置 stale=0
    - 关闭（close）：放弃或已完成，移出任务列表
    - 保持（keep）：无法推进但不能关闭，stale 归零但保留
  → 逐个话题判断：
    - 完成（done）：话题结束，移出未闭合列表
    - 暂停（pause）：保持暂停状态
    - 激活（activate）：继续深入讨论
  → 调用 task-state.sh / topic-tracker.sh 执行状态变更

Step 6: 上下文压缩替换
  → 丢弃：过程噪音
  → 保留：结论 + 任务状态快照 + 索引

Step 7: 清理trigger
  → rm /tmp/.dream-trigger
  → 通知主AI整理完成
```

### v1 不做的事（v2+）

```
❌ 冲突检测 + 去重（v2）
❌ 跨会话关联（v2）
❌ 情绪处理（长期）
❌ 加权多维指标体系（v2+）
❌ 自动发现记忆关联（v2+）
❌ 整理后自动状态决策（v2）— 端到端测试发现缺失
```

### 实施文件清单

| 文件 | 作用 |
|------|------|
| scripts/dream/dream-fragmentation-check.sh | 碎片化检测主脚本 |
| scripts/dream/task-state.sh | 任务状态管理 |
| scripts/dream/topic-tracker.sh | 话题追踪 |
| scripts/heartbeat-logger.sh | 集成到心跳 |
| .dream/task-state.json | 任务状态存储 |
| .dream/topic-state.json | 话题状态存储 |
| .dream/metrics.json | 最近检测指标 |
| /tmp/.dream-trigger | 触发标志文件 |
