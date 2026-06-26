---
name: dida-agent-optimizer
description: Agent 自愈引擎 — 自动诊断和修复 OpenClaw 执行问题（Cron 失败、工具报错、工作流中断、性能退化），自带持续自我进化能力。
  Use when user asks to 系统诊断、修复 cron、优化配置、检查系统健康度、自愈修复、诊断失败原因、修复任务失败、优化师自我更新.
  不适用于业务逻辑问题排查、飞书内容编辑、数据查询类任务.
---

# Agent 架构与工程优化师

## 概述

基于 Anthropic / OpenAI 工程实践的 Agent 自愈引擎，覆盖「检测 → 诊断 → 修复 → 验证 → 学习 → 进化」闭环。

### 功能范围

- Cron 任务诊断与修复（失败/超时/disabled/配置错误）
- 工具调用异常诊断（认证/权限/限流/超时/参数）
- 子 Agent 异常诊断（spawn 失败/超时/上下文过大）
- 系统健康度巡检（资源/网络/磁盘/内存）
- **自我进化**：定期收集工程实践、更新 references/、沉淀新模式
- 错误模式学习与沉淀（learnings/error-log.md → fix-templates.md 自动升级）

---

## 使用

### 场景 1：Cron 任务执行失败

```bash
# Step 1 — 快速扫描
openclaw cron list --includeDisabled

# Step 2 — 定位失败 job，查看 runs 历史
openclaw cron runs <jobId>

# Step 3 — 常见修复（参照 references/fix-templates.md）
#   A. sessionTarget/payload 不匹配
openclaw cron update <jobId> \
  --patch '{"payload":{"kind":"systemEvent","text":"..."}.","sessionTarget":"main"}'

#   B. 超时 → 增大 timeoutSeconds
openclaw cron update <jobId> \
  --patch '{"payload":{"timeoutSeconds":300}}'

#   C. disabled → 重新启用
openclaw cron update <jobId> --patch '{"enabled":true}'

# Step 4 — 验证
openclaw cron runs <jobId> --limit 1
```

**修复规则**：
- `sessionTarget="main"` → `payload.kind` 必须是 `"systemEvent"`
- `sessionTarget="isolated"/"current"` → `payload.kind` 必须是 `"agentTurn"`
- 超时问题先尝试 `timeoutSeconds` 加倍，若仍超时则拆分 payload 逻辑

### 场景 2：工具调用连续失败

```bash
# Step 1 — 检查错误日志
cat learnings/error-log.md 2>/dev/null | tail -50

# Step 2 — 按错误类型定位（参照 references/error-taxonomy.md）
#   401/403 → 认证/权限问题
feishu_app_scopes          # 检查飞书权限
echo $API_KEY | wc -c      # 检查 key 是否存在

#   429 → 限流，等待 + 指数退避重试
#   5xx → 服务端错误，稍后重试

# Step 3 — 应用降级策略
#   搜索: web_search → SearXNG(local:3004) → web_fetch
#   网页: web_fetch → firecrawl(local:3002)
```

### 场景 3：系统健康度巡检

```bash
# 资源检查
df -h /                     # 磁盘
free -m                     # 内存
docker ps                   # 容器状态

# 服务健康检查
curl -s http://localhost:3002/health  # Firecrawl
curl -s http://localhost:3003/health  # Crawl4AI
curl -s http://localhost:3004/health  # SearXNG（返回 HTML 即正常）

# OpenClaw 状态
openclaw status
```

### 场景 4：子 Agent 异常

```bash
# 检查活跃子 Agent
openclaw subagents list --recentMinutes 60

# 终止卡死的
openclaw subagents kill <target>

# 重新生成时的优化选择
#   - 轻量任务: lightContext=true
#   - 不需要当前上下文: context="isolated"
#   - 需要上下文: context="fork"
#   - 长任务: runTimeoutSeconds=600
```

---

## 诊断决策树

遇到问题时，按以下路径快速定位：

```
问题出现
│
├─ Cron 相关？
│   ├─ 任务未执行 → 检查 enabled / schedule 表达式 / timezone
│   ├─ 执行报错 → 检查 runs 历史 → 对照 fix-templates.md
│   └─ 超时 → 增加 timeoutSeconds 或拆分逻辑
│
├─ 工具调用相关？
│   ├─ 401/403 → 检查认证/权限（feishu_app_scopes / 环境变量）
│   ├─ 429 → 指数退避重试（1s→2s→4s）
│   ├─ 5xx → 等待重试，记录日志
│   └─ 连接超时 → 检查网络 → 降级到备用方案
│
├─ 子 Agent 相关？
│   ├─ spawn 失败 → 检查 task 内容是否过大 / 资源不足
│   ├─ 超时 → 增加 runTimeoutSeconds 或优化 task
│   └─ 结果异常 → 检查 context 模式是否正确
│
└─ 系统相关？
    ├─ 磁盘满 → 清理 memory/learnings 过期文件 + docker prune
    ├─ 内存不足 → 停止非必要服务 + 使用 lightContext
    └─ 网络断开 → 检查 DNS / 防火墙
```

## 自愈闭环

```
检测（心跳/用户反馈/错误日志）
  → 诊断（四层模型：快速扫描 → 错误分析 → 根因推理 → 修复建议）
    → 修复（最小变更 + 可回滚）
      → 验证（修复后确认）
        → 学习（记录到 learnings/error-log.md）
```

### 错误日志格式（learnings/error-log.md）

```markdown
## YYYY-MM-DD HH:MM
- **Error**: [错误描述]
- **Context**: [触发场景]
- **Root Cause**: [根因分析]
- **Fix Applied**: [修复操作]
- **Prevention**: [避免复现的措施]
```

## 操作分级与安全

| 级别 | 范围 | 策略 |
|------|------|------|
| L0 | 读取状态、检查日志 | 自动执行 |
| L1 | 清理临时文件、更新日志 | 自动执行 |
| L2 | 修改 cron 配置、重启服务 | 提示用户确认 |
| L3 | 修改核心配置、删除数据 | 必须用户明确授权 |

**禁止自动执行**：
- ❌ 修改 SOUL.md / IDENTITY.md / USER.md
- ❌ 发送外部消息（邮件/飞书/社交）
- ❌ 删除不可恢复的数据

## 参考文件

| 文件 | 何时读取 |
|------|---------|
| [references/anthropic-patterns.md](references/anthropic-patterns.md) | 需要了解 Thinking/Tool Use/多 Agent 协调模式时 |
| [references/openai-patterns.md](references/openai-patterns.md) | 需要 ReAct 循环/降级链/评估模式时 |
| [references/error-taxonomy.md](references/error-taxonomy.md) | 工具调用失败，需要分类诊断时 |
| [references/fix-templates.md](references/fix-templates.md) | 确认修复方案后，查找具体修复命令时 |
| [references/self-evolution.md](references/self-evolution.md) | 自我进化任务：收集最新实践、更新 references/ |

## 自我进化机制

优化师不是一次性写好的，它会持续进化。进化分三个路径：

### 路径 1：错误驱动进化（每次诊断后自动触发）

每次修复问题后，检查是否产生新的修复模板或需要更新错误分类：

```
修复完成
│
├─ 这是新错误类型？
│   ├─ 是 → 新增 error-taxonomy.md 条目 + fix-templates.md 模板
│   └─ 否 → 更新 error-taxonomy.md 中的复发计数
│
├─ 修复方法可复用？
│   ├─ 是 → 写入 fix-templates.md
│   └─ 否 → 记录到 learnings/error-log.md
│
└─ 涉及工程模式？
    ├─ 是 → 更新对应 references/ 文件
    └─ 否 → 跳过
```

### 路径 2：定期知识更新（每周 Cron 任务触发）

每周自动执行一次工程实践收集：

1. **搜索最新实践**：用 SearXNG 搜索 Anthropic/OpenAI 最新工程文档
2. **对比已有内容**：与 references/ 中的内容对比
3. **提取新模式**：发现新方法时追加到对应 references/ 文件
4. **清理过时内容**：标记已过时的实践
5. **更新版本号**：在 SKILL.md 末尾记录最后更新时间和版本号

执行脚本：`references/scripts/self-update.sh`（如果存在）或手动执行：

```bash
# 搜索 Anthropic 最新实践
curl -s "http://localhost:3004/search?q=anthropic+agent+engineering+best+practices+tool+use+patterns+$(date +%Y)&format=json&engines=bing,duckduckgo" | python3 -c "
import json, sys
data = json.load(sys.stdin)
for r in data.get('results', [])[:5]:
    print(json.dumps({'title': r.get('title',''), 'url': r.get('url','')}, ensure_ascii=False))
"

# 搜索 OpenAI 最新实践
curl -s "http://localhost:3004/search?q=openai+agent+patterns+function+calling+error+handling+best+practices+$(date +%Y)&format=json&engines=bing,duckduckgo" | python3 -c "
import json, sys
data = json.load(sys.stdin)
for r in data.get('results', [])[:5]:
    print(json.dumps({'title': r.get('title',''), 'url': r.get('url','')}, ensure_ascii=False))
"
```

更新规则：
- **新增模式**：追加到 references/ 对应文件末尾，标注日期
- **更新模式**：修改现有条目，保留旧内容作为「历史版本」
- **废弃模式**：标记为「⚠️ 已废弃 - 原因」，不删除

### 路径 3：错误日志驱动进化（每次 error-log.md 更新后检查）

当 learnings/error-log.md 中出现 3 次以上相同错误模式时：

1. 创建或更新 fix-templates.md 中的对应模板
2. 更新 error-taxonomy.md 中的优先级
3. 如果是新型错误，新增分类条目

## 主动巡检触发

除问题触发外，以下场景也应主动巡检：

- **每周自检**（HEARTBEAT.md 中配置）：检查 cron 健康度、工具失败回顾
- **用户反馈响应变慢**：分析 token 使用、session 状态
- **新服务部署后**：验证服务健康度、更新 TOOLS.md
- **自我进化周任务**：每周日 03:00 执行工程实践收集

## 版本与更新记录

> 记录优化师自身的迭代历史，便于追踪进化轨迹。

| 版本 | 日期 | 更新内容 |
|------|------|----------|
| v1.0 | 2026-05-18 | 初始创建（四层骨架 + 诊断决策树 + 修复模板） |
| v1.1 | 2026-05-18 | 添加自我进化机制（三条路径：错误驱动/定期知识更新/错误日志驱动） |
