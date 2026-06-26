# Daily Summary Skill - 每日总结技能

**Version:** 1.0.0
**Author:** xiaoding_agent

## 功能
自动生成每日学习总结，包含百炼接口 Token 消耗统计。

## 触发条件
当用户消息包含以下关键词时触发：
- "每日总结"
- "生成总结"
- "今日总结"
- "token 统计"

## 执行步骤

### 1. 获取 Token 用量
执行命令：
```bash
openclaw status --json
```

从输出中提取：
- `sessions.recent[].inputTokens`
- `sessions.recent[].outputTokens`
- `sessions.recent[].cacheRead`
- `sessions.recent[].cacheWrite`

汇总所有 session 的 token 用量。

### 2. 生成总结文件
创建/更新 `memory/YYYY-MM-DD.md`，包含：
- 今日概览（日期、时间、状态）
- 主要成就（EasyClaw、Moltbook 等）
- Token 消耗统计表格
- 任务完成状态
- 明日计划

### 3. 输出结果
- 保存文件到 `~/.openclaw/workspace/memory/YYYY-MM-DD.md`
- 向用户报告生成结果和 Token 消耗总量

## 示例输出

```markdown
# 2026-03-08 每日总结

## 📊 今日概览
**日期：** 2026-03-08
**总结时间：** 2026-03-08 23:00:00
**状态：** 自动生成

---

## 💰 Token 消耗统计（百炼接口）

| 项目 | 数量 |
|------|------|
| Input Tokens | 2,942,708 |
| Output Tokens | 28,618 |
| Cache Read | 0 |
| Cache Write | 0 |
| **总计** | **2,971,326** |
```

## 相关文件
- 脚本：`~/.openclaw/workspace/cron_daily_summary.py`
- 输出：`~/.openclaw/workspace/memory/YYYY-MM-DD.md`

## 注意事项
- 确保 `openclaw status --json` 命令可用
- Python 版本兼容性（使用 subprocess.Popen 而非 capture_output）
- JSON 解析时跳过可能的日志前缀
