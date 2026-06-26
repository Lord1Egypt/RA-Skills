# Aegis Protocol 文件说明

**版本**: v0.12.2  
**最后更新**: 2026-04-05

---

## 📦 发布文件 (Push to GitHub/ClawHub)

这些文件会随版本发布到 GitHub 和 ClawHub：

| 文件 | 说明 | 必需 |
|------|------|------|
| `aegis-protocol.py` | 核心代码 | ✅ |
| `README.md` | 使用说明 | ✅ |
| `SKILL.md` | ClawHub 技能说明 | ✅ |
| `_meta.json` | 元数据 | ✅ |
| `SECURITY.md` | 安全说明 | ✅ |
| `CHANGELOG.md` | 版本历史 | ✅ |
| `ROADMAP.md` | 开发路线图 | ✅ |

**发布命令**:
```bash
# GitHub
git push origin main

# ClawHub
clawhub publish skills/aegis-protocol --version 0.12.2
```

---

## 💻 本地开发文件 (Local Only)

这些文件仅用于本地开发，**不发布**：

| 文件 | 说明 | 用途 |
|------|------|------|
| `WORKFLOW.md` | 多 Agent 工作流 | 开发流程定义 |
| `AGENT_TASKS.md` | 任务分配追踪 | 开发任务记录 |
| `DEVELOPMENT_REPORT.md` | 开发报告 | 阶段性总结 |
| `tests/` | 测试文件 | 本地测试 |
| `__pycache__/` | Python 缓存 | 自动生成的缓存 |
| `.pytest_cache/` | pytest 缓存 | 自动生成的缓存 |
| `.watchdog-config.json` | 运行时配置 | 用户配置 |
| `.healing-memory.json` | 恢复记录 | 运行时数据 |
| `.aegis-cache.json` | 检查结果缓存 | 运行时数据 |
| `.loop-history.json` | 循环检测历史 | 运行时数据 |

---

## 📁 完整目录结构

```
skills/aegis-protocol/
├── 📦 aegis-protocol.py        # 核心代码
├── 📦 README.md                # 使用说明
├── 📦 SKILL.md                 # ClawHub 说明
├── 📦 _meta.json               # 元数据
├── 📦 SECURITY.md              # 安全说明
├── 📦 CHANGELOG.md             # 版本历史
├── 📦 ROADMAP.md               # 路线图
├── 📦 FILES.md                 # 本文件
├── 💻 WORKFLOW.md              # 工作流 (本地)
├── 💻 AGENT_TASKS.md           # 任务追踪 (本地)
├── 💻 DEVELOPMENT_REPORT.md    # 开发报告 (本地)
├── 💻 tests/                   # 测试 (本地)
├── 💻 __pycache__/             # 缓存 (自动)
└── 💻 .pytest_cache/           # 缓存 (自动)
```

---

## 🚫 .gitignore (建议)

```gitignore
# Python
__pycache__/
*.py[cod]
*.pyo
.pytest_cache/

# 运行时数据
.watchdog-config.json
.healing-memory.json
.aegis-cache.json
.loop-history.json

# 本地开发
AGENT_TASKS.md
DEVELOPMENT_REPORT.md
```

---

## ✅ 发布检查清单

发布前确认：

- [ ] `_meta.json` 的 `files` 列表正确
- [ ] 本地开发文件未包含
- [ ] 测试通过
- [ ] CHANGELOG.md 更新
- [ ] ROADMAP.md 更新
- [ ] Git 提交信息清晰

---

*文件分类清晰 - 发布/本地分离* 🌀
