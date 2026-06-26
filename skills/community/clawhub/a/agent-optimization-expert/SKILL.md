---
name: agent-optimization-expert
version: 1.4.0
description: >
  Agent 优化专家 — 自动诊断和修复 Agent 执行问题（Cron 失败、工具报错、工作流中断、性能退化），
  兼容 OpenClaw 和 Hermes Agent，自带持续自我进化能力。
  Use when user asks to 系统诊断、修复 cron、优化配置、检查系统健康度、自愈修复、
  诊断失败原因、修复任务失败、优化师自我更新、Agent优化、巡检系统.
  不适用于业务逻辑问题排查、飞书内容编辑、数据查询类任务.
---

# Agent 优化专家

## 概述

基于 Anthropic / OpenAI 工程实践的 Agent 自愈引擎，覆盖「检测 → 诊断 → 修复 → 验证 → 学习 → 进化」闭环。
**兼容 OpenClaw 和 Hermes Agent 双环境**，自动识别当前平台并切换对应命令。

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

> **双环境适配**：OpenClaw 走 `openclaw cron` CLI，Hermes 走 `cronjob` 工具。
> 完整命令映射表和修复规则见 `references/dual-env-adaptation.md`

**快速诊断流程（通用）：**
1. 列出所有 Cron 任务，检查 enabled/schedule/最近运行状态
2. 定位失败 job，查看错误输出
3. 对照 `references/fix-templates.md` 执行修复
4. 手动触发一次验证修复结果

**常见修复类型：**
- **未执行** → 检查 enabled / schedule 表达式 / timezone
- **执行报错** → 检查错误输出 → 对照 fix-templates.md
- **超时** → timeout 加倍，若仍超时则拆分逻辑
- **disabled** → 重新启用

---

### 场景 2：工具调用连续失败

```bash
# Step 1 — 检查错误日志
cat learnings/error-log.md 2>/dev/null | tail -50

# Step 2 — 按错误类型定位（参照 references/error-taxonomy.md）
#   401/403 → 认证/权限问题
feishu_app_scopes          # 检查飞书权限（双环境通用）
echo $API_KEY | wc -c      # 检查 key 是否存在
#   429 → 限流，等待 + 指数退避重试
#   5xx → 服务端错误，稍后重试

# Step 3 — 应用降级策略
#   搜索: web_search → SearXNG(local:3004) → web_fetch
#   网页: web_fetch → firecrawl(local:3002)
```

---

### 场景 3：系统健康度巡检

```bash
# 资源检查（通用）
df -h /                     # 磁盘
free -m                     # 内存
docker ps                   # 容器状态

# 服务健康检查（通用）
curl -s http://localhost:3002/health  # Firecrawl
curl -s http://localhost:3003/health  # Crawl4AI
curl -s http://localhost:3004/health  # SearXNG（返回 HTML 即正常）

# Agent 平台状态
# OpenClaw → openclaw status
# Hermes → ps aux | grep hermes
```

---

### 场景 4：子 Agent 异常

**OpenClaw**：`openclaw subagents list` 查看 → `openclaw subagents kill <target>` 终止
**Hermes**：子 Agent 同步执行不卡死，超时检查 delegate_task timeout；Cron 子任务卡住用 `process(action='kill')`

---

## 自动触发机制

> 本 Skill 不会自己跑起来，需要环境提供"心跳"或"定时"机制。
> **双环境适配完整指南**（含 Cron Job 配置命令 + HEARTBEAT.md 配置模板）→ `references/dual-env-adaptation.md`

**一句话总结：**
- **Hermes 环境** → 用 `cronjob(action='create')` 创建每日自检 + 每周知识更新
- **OpenClaw 环境** → 在 `workspace/HEARTBEAT.md` 中配置心跳检查清单

---

## 诊断决策树

```
问题出现
│
├─ Cron 相关？
│   ├─ 任务未执行 → 检查 enabled / schedule / timezone
│   ├─ 执行报错 → 查错误输出 → 对照 fix-templates.md
│   └─ 超时 → timeout 加倍 or 拆分逻辑
│
├─ 工具调用相关？
│   ├─ 401/403 → 认证/权限
│   ├─ 429 → 指数退避重试
│   ├─ 5xx → 等待重试 + 记录
│   └─ 超时 → 网络检查 → 降级
│
├─ 子 Agent 相关？
│   ├─ spawn 失败 → task 过大 / 资源不足
│   ├─ 超时 → 增加 timeout / 优化 task
│   └─ 结果异常 → context 模式检查
│
└─ 系统相关？
    ├─ 磁盘满 → 清理 + docker prune
    ├─ 内存不足 → 停服务 + lightContext
    └─ 网络断开 → DNS / 防火墙
```

---

## 自愈闭环

```
检测（心跳/用户反馈/错误日志）
  → 诊断（快速扫描 → 错误分析 → 根因推理 → 修复建议）
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

---

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

---

## 自我进化机制

### 路径 1：错误驱动进化（每次诊断后）

```
修复完成
├─ 新错误类型？→ 新增 error-taxonomy + fix-templates
├─ 修复可复用？→ 写入 fix-templates
└─ 涉及工程模式？→ 更新对应 references/
```

### 路径 2：定期知识更新（每周）

1. SearXNG 搜索 Anthropic/OpenAI 最新工程文档
2. 对比 references/ 现有内容
3. 发现新模式追加到对应文件
4. 标记已过时实践（不删除，标「⚠️ 已废弃」）

```bash
curl -s "http://localhost:3004/search?q=anthropic+agent+engineering+best+practices+$(date +%Y)&format=json&engines=bing,duckduckgo" | python3 -c "
import json, sys
data = json.load(sys.stdin)
for r in data.get('results', [])[:5]:
    print(json.dumps({'title': r.get('title',''), 'url': r.get('url','')}, ensure_ascii=False))
"
```

### 路径 3：错误日志驱动进化

learnings/error-log.md 中相同错误模式 ≥3 次时：
1. 创建/更新 fix-templates.md 对应模板
2. 更新 error-taxonomy.md 优先级
3. 新型错误新增分类条目

---

## 参考文件

| 文件 | 何时读取 |
|------|---------|
| [references/dual-env-adaptation.md](references/dual-env-adaptation.md) | **首次使用必读** — 环境检测、命令映射、Cron/HEARTBEAT 配置 |
| [references/anthropic-patterns.md](references/anthropic-patterns.md) | 需要 Thinking/Tool Use/多 Agent 协调模式 |
| [references/openai-patterns.md](references/openai-patterns.md) | 需要 ReAct 循环/降级链/评估模式 |
| [references/error-taxonomy.md](references/error-taxonomy.md) | 工具调用失败分类诊断 |
| [references/fix-templates.md](references/fix-templates.md) | 确认修复方案后查具体命令 |
| [references/self-evolution.md](references/self-evolution.md) | 自我进化：收集最新实践 |

---

## 首次运行协议

首次被加载时（检查 `learnings/error-log.md` 不存在或为空），自动执行一次完整自检：

1. **系统健康度巡检**（场景 3）：磁盘/内存/容器/本地服务
2. **Cron 任务扫描**（场景 1）：检查最近失败的 job
3. **输出简短报告**：
   - ✅ 一切正常 → "已就位，系统健康"
   - ⚠️ 发现问题 → "已就位，发现 X 个问题：[列表]"
4. **创建 learnings/error-log.md**，记录"首次自检完成"
5. **后续不再自动触发**，等待用户指令或 Cron 调度

> 目的：给用户即时反馈，确认 Skill 已正确安装且能正常工作（Smoke Test）。

---

## 版本与更新记录

| 版本 | 日期 | 更新内容 |
|------|------|----------|
| v1.0 | 2026-05-18 | 初始创建（四层骨架 + 诊断决策树 + 修复模板） |
| v1.1 | 2026-05-18 | 添加自我进化机制（三条路径） |
| v1.3 | 2026-05-20 | **双环境适配**：兼容 OpenClaw + Hermes，环境自动检测、双路径命令映射、HEARTBEAT.md 与 Cron Job 双触发机制 |
| v1.4 | 2026-05-20 | **首次运行协议**：安装后首次加载自动执行 Smoke Test 自检，给用户即时反馈 |
