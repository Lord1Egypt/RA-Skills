# REFERENCES — Codex-CLI-Guardian 格式标准

> 本文件记录所有确认过的格式要求和内容标准

---

## 1. 目录结构

```
skills/codex-cli-guardian/
├── SKILL.md
├── REFERENCES.md
├── README.md
├── EXAMPLES.md
├── CLI.md                    # Codex CLI 正确用法
├── bin/
│   ├── codex-call.sh        # 主调用脚本（后台 + PTY）
│   └── session.sh            # 状态管理 / kill
├── scripts/
│   └── init-setup.sh         # API Key 验证 + 写入 credentials.env
├── state/
│   ├── current-task.json     # 运行中任务
│   ├── tasks/               # 任务历史
│   └── codex.lock           # PID 锁
├── workers/                  # Worker 模板
│   ├── standard-preamble.md
│   ├── reviewer.md
│   ├── researcher.md
│   ├── implementer.md
│   ├── verifier.md
│   ├── scout.md
│   ├── context-pack.md
│   └── patterns.md
```

---

## 2. API Key 管理

**存储文件**：`credentials.env`（skill 目录内）
**格式**：`OPENAI_API_KEY_0011AI=<key>`
**权限**：600

**验证流程（init-setup.sh）**：
1. 检测已有 key → 询问是否重设
2. 获取 Key（环境变量优先，否则要求用户输入）
3. **验证 Key**：实际调用 `codex --full-auto exec "echo ok"`
4. 验证成功 → 写入 `credentials.env`（权限 600）；验证失败 → 回到 STEP 2

**运行时**：codex-call.sh 从 skill 目录内的 `credentials.env` 读取 Key

---

## 3. current-task.json 格式

```json
{
  "task_id": "20260404-001",
  "description": "帮我写个爬虫",
  "status": "running",
  "started_at": "2026-04-04T20:10:00+08:00",
  "max_duration_minutes": 30
}
```

---

## 4. 任务历史 JSON 格式

```json
{
  "task_id": "20260404-001",
  "description": "帮我写个爬虫",
  "status": "done",
  "summary": "spider.py 已创建完成，包含多页面爬取",
  "started_at": "2026-04-04T20:10:00+08:00",
  "finished_at": "2026-04-04T20:13:00+08:00"
}
```

---

## 5. Codex 调用方式

```bash
script -q /dev/null env OPENAI_API_KEY_0011AI="<key>" \
  codex --full-auto exec -o /tmp/summary.txt "<task>"
```

**注意**：Codex exec 不支持 session 持久化，每次独立 session。

---

## 6. PID 锁（macOS 兼容）

```bash
if [[ -f "$LOCK_FILE" ]]; then
    pid=$(cat "$LOCK_FILE")
    if kill -0 "$pid" 2>/dev/null; then
        echo "⚠️ Codex 忙碌中，请稍后再试"
        exit 1
    fi
    rm -f "$LOCK_FILE"
fi
```

---

## 7. 超时策略

- **不自动终止**：超时后任务继续运行
- `session.sh status` 显示超时警告
- 主人决定：「终止任务」→ `session.sh kill`

---

## 8. session.sh 命令

| 命令 | 说明 |
|------|------|
| `status` | 健康检查（含超时警告） |
| `list` | 最近任务历史 |
| `kill` | 终止当前任务 |
| `reset` | 重置状态（不清历史） |

---

## 9. 消息格式规范

| 场景 | 格式 |
|------|------|
| **意图确认** | `🔍 检测到代码开发意图，要用 Codex 执行吗？` + 任务描述 + 操作提示 |
| 任务开始 | `🚀 已启动任务 [{task_id}]：{描述}` |
| 任务完成 | `✅ 任务 [{task_id}] 完成：` + summary |
| 任务失败 | `❌ 任务 [{task_id}] 失败：{原因}` |
| 忙碌拒绝 | `⚠️ Codex 忙碌中，请稍后再试` |
| 超时警告 | `⚠️ 已超时 N 分钟，请决定是否终止` |
| 健康检查 | 表格格式（见 SKILL.md） |

---

## 10. Worker 模板

详见 `workers/` 目录：
- `standard-preamble.md` — Worker 前言
- `reviewer.md` — 评审者
- `researcher.md` — 研究者
- `implementer.md` — 实现者
- `verifier.md` — 验证者
- `scout.md` — 侦察者
- `context-pack.md` — Context Pack

---

## 11. 编排模式

详见 `workers/patterns.md`：
- A: 三角评审（Fan-out）
- B: 评审→修复（Serial Chain）
- C: 侦察→行动→验证（Classic）
- D: 分片（Fan-out + Merge）
- E: 研究→综合
- F: 选项冲刺

---

## 12. Codex CLI 参考

详见 `CLI.md`：
- PTY wrapper 必须
- Git repo 必须
- `--full-auto` / `--yolo`
- `-o /path/to/output.txt` 输出捕获

---

*最后更新：2026-04-05*
