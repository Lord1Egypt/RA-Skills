# Scan-Script / Cronjob / Agent 三体架构

这是 bilibili-auto-transcript 使用的核心架构模式，适用于任何需要**定时扫描外部源 → 发现增量 → 由 AI 处理并通知**的任务。

## 架构示意

```
定时触发 (cronjob / 系统定时器)
    ↓
扫描脚本 (bilibili_scanner.py)
    → 调用外部 API 获取数据
    → 读取本地已处理记录 (processed_videos.txt)
    → 发现增量 (取差集)
    → stdout 输出新条目 (结构化文本)
    ↓ stdout
AI Agent（加载 skill）
    → 读取 stdout 中的新条目
    → 对每个新条目执行处理流程
    → 更新已处理记录
    → 通知用户
```

## 三个组件

### 1. 扫描脚本 (Scanner)
- 职责：只做"发现"，不做"处理"
- 执行方式：快速（通常 <1 秒），通过 cronjob 定时触发
- 输出格式：结构化的纯文本标记，方便 agent 解析
  - `NO_NEW_ITEMS` / `ALL_CAUGHT_UP` — 无增量，agent 不做事
  - `NEW_ITEMS:N` + 逐条详细信息 — 有增量，agent 启动处理
- 状态维护：维护一个 `processed_xxx.txt` 文件，每行一个唯一 ID

### 2. 定时触发器 (Cronjob/Scheduler)
- OpenClaw 内置 cronjob：
  - `no_agent=False`（默认）：script stdout 注入 prompt，agent 按 prompt 处理
  - `script=bilibili_scanner.py`（相对路径解析到 `~/.openclaw/workspace/skills/bilibili-auto-transcript/scripts/`）
  - `skills=[...]`：加载相关 skill 提供上下文
  - 无增量时 agent 只回复一句"无新内容"，不打扰用户
- 外部定时器：
  - 用 Linux systemd timer、crontab 等触发扫描

### 3. AI 处理器 (Agent)
- 职责：处理新条目（分析、转换、生成、通知）
- 输入：扫描脚本的 stdout
- 输出：最终交付给用户的结果（文件、消息、摘要等）
- skill 提供处理步骤的完整定义

## 适用场景

这个模式适用于：
- 监控网站/API 的新内容（博客、新闻、社交平台）
- 定时检查文件系统变化
- 定时抓取数据并生成报告
- 任何"定期巡检 → 发现增量 → AI 分析 → 通知"的工作流

## 关键设计原则

1. **扫描脚本必须快** — 它只是 API 调用 + 集合比对，不应包含耗时操作
2. **增量记录用唯一 ID** — 用数据集的原生 ID（如 avid），不用文件名或标题，避免重名/改名导致重复处理
3. **不重复不遗漏** — 处理完立即记录 ID，agent 中途失败也不会漏掉
4. **无增量时静默** — 用户只在有变化时才收到消息
5. **自愈** — 脚本/agent 处理失败不阻塞后续扫描，下次运行时重试发现
