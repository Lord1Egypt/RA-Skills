# anamnesis-hub — 文档索引

> 本目录包含 anamnesis-hub 技能的完整技术文档。
> 最新版本：v1.13.1 | 最后更新：2026-05-17

---

## 📚 文档总览

| 文档 | 说明 |
|------|------|
| **[architecture.md](architecture.md)** | 四层记忆架构设计、插件协同工作流、文件解剖、插件冲突说明 |
| **[setup-guide.md](setup-guide.md)** | 环境配置、手动安装步骤、cron 任务设置、所有配置参数详解 |
| **[memory-directory.md](memory-directory.md)** | `memory/` 目录结构、状态文件、LCM 防失控机制、P3 候选审核流程 |
| **[sync-api.md](sync-api.md)** | MemOS Cloud API 端点、同步状态文件、安全机制 |
| **[scripts-reference.md](scripts-reference.md)** | 所有脚本统一说明：用途、cron 触发时间、依赖关系、关键参数 |
| **[pipeline-stages.md](pipeline-stages.md)** | 日终管线 6 阶段详解：输入/输出/依赖/失败处理 |
| **[candidates-review.md](candidates-review.md)** | P3 记忆候选审核机制：Dreaming → 审核队列 → ARCHIVE.md 完整流程 |
| **[upgrade-reset.md](upgrade-reset.md)** | 升级路径、重置流程、卸载步骤 |

---

## 🗂️ 文档层级关系

```
入口：README.md / SKILL.md
    ↓
references/INDEX.md（本文档）
    ├── architecture.md       ← 必读：理解架构
    ├── setup-guide.md        ← 必读：安装配置
    ├── memory-directory.md   ← 进阶：目录结构
    ├── sync-api.md           ← 进阶：云同步
    ├── scripts-reference.md  ← 运维：脚本说明
    ├── pipeline-stages.md    ← 运维：管线流程
    ├── candidates-review.md ← 运维：候选审核
    └── upgrade-reset.md      ← 运维：升级重置
```

---

## 🔗 外部链接

| 平台 | 链接 |
|------|------|
| **ClawHub** | https://clawhub.ai/victorqr/anamnesis-hub |
| **GitHub** | https://github.com/VictorQR/anamnesis-hub |
| **Skill 安装** | `openclaw skills install victorqr/anamnesis-hub` |

---

## 📌 快速定位

| 场景 | 文档 |
|------|------|
| 首次安装 | `setup-guide.md` + `architecture.md` |
| 理解管线流程 | `pipeline-stages.md` + `scripts-reference.md` |
| 排查同步问题 | `sync-api.md` + `memory-directory.md` |
| 配置 cron | `setup-guide.md` 第 5 步 |
| P3 记忆审核 | `memory-directory.md` 第十节 + `candidates-review.md` |
| 升级/重置 | `upgrade-reset.md` |