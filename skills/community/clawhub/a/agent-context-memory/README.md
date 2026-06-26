# Agent 上下文管理方法论 (context-management)

让 AI Agent 跨 session 保持记忆、快速恢复上下文、持续积累经验。

**核心理念：文件 > 大脑。写下来，别靠"记住"。**

## 安装

```bash
clawhub install context-management
```

或手动安装：将整个文件夹复制到 `~/.openclaw/skills/context-management/`。

## 解决什么问题

每次新 session，agent 都是全新的——没有记忆、没有上下文、没有教训。这个 skill 通过**分层文件体系 + 启动协议 + 记忆生命周期管理**解决这个问题。

## 五层文件体系

| 层级 | 文件 | 职责 |
|------|------|------|
| 身份层 | `SOUL.md` | Agent 人格、原则、边界 |
| 用户层 | `USER.md` | 用户信息、偏好、定时任务 |
| 路由层 | `AGENTS.md` | 启动协议、技能路由、工作流 |
| 环境层 | `TOOLS.md` | 本机配置（换机器只改这个） |
| 记忆层 | `MEMORY.md` + `memory/` | 长期精华 + 每日原始记录 |

## 三个关键机制

1. **启动协议** — 每次 session 按固定顺序加载上下文
2. **记忆生命周期** — 即时写入 daily 文件 → 每周提炼到 MEMORY.md → 过时内容淘汰
3. **双源搜索策略** — 本地记忆 + 外部知识库联合检索

## 自动提炼脚本

附带 `scripts/memory_distill.py`，自动扫描 `memory/YYYY-MM-DD.md`，提取"技术收获"和"问题+修复"对，去重后追加到 MEMORY.md。

```bash
# 预览
python3 skills/context-management/scripts/memory_distill.py --all --dry-run

# 正式写入
python3 skills/context-management/scripts/memory_distill.py --all

# 接入 cron（每周日 23:00）
0 23 * * 0 cd ~/.openclaw/workspace && python3 skills/context-management/scripts/memory_distill.py --all >> logs/memory_distill.log 2>&1
```

## 设计原则

| 原则 | 说明 |
|------|------|
| **单一职责** | 每个文件只管一件事 |
| **文件 > 大脑** | 所有重要信息写文件 |
| **分层加载** | 按需加载，节省上下文窗口 |
| **写入即时，提炼定期** | daily 随时写，MEMORY.md 定期炼 |
| **可复现的不存** | 能从代码推导的不放 MEMORY.md |
| **换机器只改一个文件** | 环境差异隔离在 TOOLS.md |

## 适用场景

- 长期运行的 AI Agent（OpenClaw、Cursor Agent、自定义 agent）
- 需要跨 session 保持上下文的任何 agent 框架
- 多 agent 协作场景（通过共享 MEMORY.md 传递经验）

## 项目结构

```
context-management/
├── SKILL.md                # 完整方法论文档（ClawHub 必需）
├── claw.json               # ClawHub 清单文件
├── README.md               # 项目文档
└── scripts/
    └── memory_distill.py   # 自动提炼脚本
```

## 前置条件

- Python 3.10+（提炼脚本需要）
- OpenClaw 工作区（或任何支持 AGENTS.md 的 agent 框架）

## License

MIT
