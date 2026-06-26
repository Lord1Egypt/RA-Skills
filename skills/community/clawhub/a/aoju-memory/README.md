# aoju-memory

> Long-term memory, learning, and self-evolution for AI agents powered by OpenClaw.

让 AI 真正记住你是谁、记住每次对话里发生的事、从错误中学习，而不是每次新建对话就失忆。

## 特性

- **长期记忆** — 跨 session 记住用户偏好、决策、重要事实
- **自我学习** — 从反馈和错误中提取教训，沉淀到记忆库
- **模式识别** — 自动发现反复出现的问题，更新行为准则
- **语义搜索** — 用关键词 + 上下文搜索记忆（无需 embedding 服务）
- **自我进化** — 每积累 5 条 lessons，自动 review，生成行为改进建议

## 文件结构

```
aoju-memory/
├── SKILL.md                    # Skill 定义（OpenClaw 格式）
├── scripts/
│   ├── mem_recall.py          # 搜索记忆：mem_recall "关键词"
│   ├── mem_learn.py           # 记录教训：mem_learn --incident "..." --lesson "..."
│   ├── mem_evolve.py          # 进化 review：mem_evolve [--dry-run]
│   └── mem_status.py          # 记忆系统健康状态
└── _meta.json                  # 包信息
```

## 安装

### 方式一：ClawHub（一键安装）
```bash
# 从 ClawHub 安装（推荐）
openclaw skills install aoju-memory  # from ClawHub
```

### 方式二：手动安装
```bash
# 从 ClawHub 安装（推荐）
# 克隆仓库
git clone https://github.com/chaibaoqing/aoju-memory.git
cd aoju-memory

# 复制到 OpenClaw workspace skills 目录
cp -r . ~/.openclaw/workspace/skills/aoju-memory/
```

## 使用

### 自动激活（推荐）

在 OpenClaw 的 `AGENTS.md` 里声明 skill，之后每次 session 启动自动运行：

```
## Session Startup
...
4. 激活 aoju-memory skill
```

### 手动调用

```bash
# 从 ClawHub 安装（推荐）
# 搜索记忆
python3 scripts/mem_recall.py "用户偏好" --limit 5

# 记录一条教训
python3 scripts/mem_learn.py \
  --incident "用户反馈说某个回答不准确" \
  --lesson "回答前先确认信息来源，避免凭空猜测" \
  --tags "communication,accuracy" \
  --confidence high

# 查看记忆系统健康
python3 scripts/mem_status.py

# 生成精美的 HTML 记忆报告（浏览器打开）
python3 scripts/mem_report.py -o memory-report.html
# 然后用浏览器打开 memory-report.html 查看带评分、图表、颜色的精美报告

# 进化 review（每积累 5 条教训后运行）
python3 scripts/mem_evolve.py --dry-run
```

## 记忆结构

```
~/.openclaw/workspace/
├── MEMORY.md                   # 长期记忆精选（人工维护）
└── memory/
    ├── YYYY-MM-DD.md          # 每日原始日志
    └── learnings/
        ├── YYYY-MM-DD.md      # 每日教训记录
        └── patterns.md        # 识别到的重复模式
```

## 自我进化流程

```
每次对话 → 用户反馈 或 重要决策
    ↓
mem_learn.py 记录教训
    ↓
积累 5 条教训
    ↓
mem_evolve.py 分析模式
    ↓
生成 patterns.md + 行为准则更新建议
    ↓
更新 SOUL.md / AGENTS.md
```

## License

MIT — 可自由使用、修改、分发。

**署名要求**：使用时需注明原作者。
