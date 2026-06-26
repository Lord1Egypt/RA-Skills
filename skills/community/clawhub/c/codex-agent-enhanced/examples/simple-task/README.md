# 示例：简单任务（仅 Telegram 通知）

适合场景：一次性任务，不需要状态追踪和 Cron 巡检。

## 配置

```bash
# 设置必需的环境变量
export OPENCLAW_AGENT_NAME="main"
export OPENCLAW_AGENT_CHAT_ID="7936836901"
export OPENCLAW_AGENT_CHANNEL="telegram"
```

## 执行任务

```bash
# 进入项目目录
cd /path/to/your/project

# 执行 Codex 任务
codex exec --full-auto "在 src/utils.py 中添加日期格式化函数"
```

## 预期结果

1. Codex 开始执行任务
2. 任务完成后，Telegram 收到通知：
   ```
   [MAIN] 🔔 Codex 任务完成
   
   📁 /path/to/your/project
   💬 已完成：在 src/utils.py 中添加了 format_date() 函数
   thread: 01abc123...
   ```

## 注意事项

- ❌ 不会更新状态文件
- ❌ 不会有 Cron 自动巡检
- ✅ 适合快速验证、原型开发

---

**相关文件**：
- `../../hooks/on_complete.py` — Notify hook 实现
- `../../docs/CONFIG_TEMPLATE.md` — 完整配置指南
