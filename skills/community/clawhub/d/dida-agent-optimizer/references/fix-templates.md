# 常见修复模板库

## Cron 修复模板

### 1. 修复 sessionTarget/payload 不匹配

**诊断**:
```bash
openclaw cron get <jobId>
```

**修复命令**:
```bash
# 情况 A: main session 需要 systemEvent
openclaw cron update <jobId> \
  --patch '{"payload":{"kind":"systemEvent","text":"..."},"sessionTarget":"main"}'

# 情况 B: isolated session 需要 agentTurn  
openclaw cron update <jobId> \
  --patch '{"payload":{"kind":"agentTurn","message":"..."},"sessionTarget":"isolated"}'
```

**验证**:
```bash
openclaw cron runs <jobId> --limit 1
```

### 2. 修复超时问题

**诊断**:
```bash
openclaw cron runs <jobId>
# 查找 "timed out" 或 "timeout" 错误
```

**修复命令**:
```bash
# 增加超时时间
openclaw cron update <jobId> \
  --patch '{"payload":{"timeoutSeconds":300}}'
```

### 3. 修复 disabled 状态

**诊断**:
```bash
openclaw cron list --includeDisabled
# 查找 enabled: false 的任务
```

**修复命令**:
```bash
openclaw cron update <jobId> --patch '{"enabled":true}'
```

### 4. 修复 cron 表达式

**诊断**:
```bash
openclaw cron get <jobId>
# 检查 schedule.expr 和 schedule.tz
```

**修复命令**:
```bash
# 更新为正确的 cron 表达式（本地时间）
openclaw cron update <jobId> \
  --patch '{"schedule":{"kind":"cron","expr":"0 9 * * 1-5","tz":"Asia/Shanghai"}}'
```

## 工具修复模板

### 5. 刷新飞书权限

**诊断**:
```bash
feishu_app_scopes
```

**修复**: 提示用户在飞书开放平台申请所需权限

### 6. 服务健康检查

**诊断**:
```bash
# 检查 Docker 服务
docker ps --filter "status=exited"

# 检查端口
curl -s http://localhost:3002/health  # Firecrawl
curl -s http://localhost:3004/health  # SearXNG
curl -s http://localhost:3003/health  # Crawl4AI
```

**修复**:
```bash
# 重启特定服务
cd ~/firecrawl && docker compose up -d
cd ~/searxng && docker compose up -d
```

### 7. 清理磁盘空间

**诊断**:
```bash
df -h /
du -sh ~/.openclaw/workspace/memory/ 2>/dev/null
du -sh ~/.openclaw/workspace/learnings/ 2>/dev/null
```

**修复**:
```bash
# 清理超过 30 天的日志
find ~/.openclaw/workspace/memory/ -name "*.md" -mtime +30 -delete 2>/dev/null

# 清理 Docker 无用资源
docker system prune -f 2>/dev/null
```

## 子 Agent 修复模板

### 8. 子 Agent 超时

**诊断**:
```bash
openclaw subagents list --recentMinutes 60
# 查找超时或失败的子 Agent
```

**修复**:
```bash
# 终止卡死的子 Agent
openclaw subagents kill <target>

# 重新生成，增加超时
sessions_spawn(task="...", runTimeoutSeconds=600)
```

### 9. 子 Agent 上下文过大

**诊断**:
```bash
openclaw sessions list --limit 10
# 检查 session 大小
```

**修复**:
```bash
# 使用轻量上下文
sessions_spawn(task="...", lightContext=true)

# 或使用隔离上下文
sessions_spawn(task="...", context="isolated")
```

## 系统修复模板

### 10. Gateway 重启

**诊断**:
```bash
openclaw status
```

**修复**:
```bash
openclaw gateway restart --reason "优化修复后重启"
```

### 11. 内存压力

**诊断**:
```bash
free -m
# 检查可用内存
```

**修复**:
```bash
# 停止非必要服务
cd ~/firecrawl && docker compose stop  # 按需启动
cd ~/crawl4ai-server && ...  # 检查是否需要

# 或重启 Gateway
openclaw gateway restart
```

## 验证模板

### 修复后验证清单

```markdown
## 修复验证
- [ ] cron 任务正常运行: `openclaw cron list`
- [ ] 错误日志无新错误: `cat learnings/error-log.md`
- [ ] 相关工具可用: 测试调用
- [ ] 用户通知: 告知修复结果
```

### 修复报告格式

```markdown
## 🔧 修复报告

**问题**: [问题描述]
**根因**: [原因分析]
**修复**: [执行的操作]
**状态**: ✅ 已修复 / ⚠️ 部分修复 / ❌ 需要人工干预
**验证**: [验证结果]
**后续**: [预防措施或待办事项]
```
