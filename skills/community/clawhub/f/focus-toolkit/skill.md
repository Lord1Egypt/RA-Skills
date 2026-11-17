## 🍅 Focus Toolkit — 专注力工具链

> A full-focus-lifecycle workflow for precise session tracking, ambient sound generation, and data-driven analytics.
> 一套完整的专注力管理技能：闹钟→番茄钟→背景音→注意力分析，全链路覆盖。

Focus on what matters. We'll handle the rest.

### ✨ 亮点 · Highlights
- **四大模块一体化**：闹钟/番茄钟/背景音/分析，四条脚本无缝协作
  *Four modules in one: natural-language alarm + pomodoro timer + 7 soundscapes + weekly analytics*
- **跨 session 持久化**：番茄数据不丢 · *Pomodoro state survives restarts*
- **cron 原生集成**：定时提醒不占用 AI 会话 · *Cron-powered reminders don't block your chat*
- **纯 Python**：四条脚本全部 stdlib，零依赖 · *Zero deps, stdlib only*

### 🎯 使用场景 · Use Cases
- 「开始专注，放段雨声，30 分钟后叫我」→ 闹钟+番茄+背景音三连
- 「我的番茄记录」「今天效率怎么样」→ 日报/周报
- 「每天早上9点提醒我站会」→ 自然语言设闹钟

### 📦 内容 · Contents
- `SKILL.md` — 完整全流程指南 · Full workflow guide
- `scripts/parse_time.py` — 中文时间解析 · CN time parser
- `scripts/log_session.py` — 番茄记录器 · Pomodoro logger
- `scripts/generate_soundscape.py` — 7 种背景音合成 · 7-type soundscape synth
- `scripts/analyze.py` — 注意力日报/周报 · Focus analytics engine

> ⚠️ focus-toolkit 已整合 natural-alarm、pomodoro-workflow、focus-soundscape、attention-analytics 四个独立技能。推荐使用 focus-toolkit，四个独立版本只维护不再更新。
