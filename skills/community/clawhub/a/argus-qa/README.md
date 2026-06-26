# Argus — Automated Testing Skill

> Hundred-eyed. Never sleeps. Every fixed bug becomes a permanent eye.

增量式后端 API + 前端浏览器测试，带有持久化记忆。监控每次提交，丰富不充分的提交信息，并针对变更文件运行定向测试。

## 特性

- **提交监控** - 自动分析每次 git commit，提取可测试场景
- **锁定测试** - 来自修复提交的测试永远保留，防止回归
- **智能生成** - 扫描路由自动生成 API 测试
- **前后端全覆盖** - pytest 测后端，Playwright 测前端
- **健康评分** - 量化测试覆盖度和稳定性

## 安装

### 方法 1: 直接安装到 Claude Code

```bash
# 复制 skill 到 Claude Code skills 目录
cp -r argus-skill ~/.claude/skills/argus

# 重启 Claude Code 或重新加载技能
```

### 方法 2: 使用 Claude CLI

```bash
claude skills add /path/to/argus-skill
```

## 使用

```bash
# 初始化 Argus（仅需一次）
/argus init

# 运行完整测试
/argus

# 只测后端
/argus test --backend

# 只测前端
/argus test --frontend

# 基于当前分支 diff 运行相关测试
/argus test --diff

# 查看测试报告
/argus report
```

## 项目结构

```
.argus/
  catalog.md          # 测试知识库
  baseline.json       # 健康评分历史
  reports/
    YYYY-MM-DD.md     # 每次运行的报告
  commit-hook.sh      # git post-commit 钩子

tests/
  backend/
    conftest.py       # pytest 配置
    test_*.py         # 后端测试
  frontend/
    test_*.py         # 前端 Playwright 测试
```

## 环境要求

- Python 3.9+
- pytest + pytest-asyncio
- httpx (后端测试)
- playwright (前端测试)

所有依赖会在首次运行时自动安装。

## Catalog 格式

Argus 使用 `.argus/catalog.md` 作为测试知识库：

```markdown
last_scanned_commit: abc123

## test_example
- Type: backend
- Source: fix commit abc123 — 修复描述
- Protection: locked | regenerable
- Covers: /api/endpoint
- File: tests/backend/test_file.py::test_example
- Status: active ✅ | failing ❌ | skipped ⚠️
- Last run: 2026-03-30 passed
```

### 保护级别

| 级别 | 来源 | 说明 |
|------|------|------|
| `locked` | 修复提交 | 永不可删除或修改，防止回归 |
| `regenerable` | 自动生成 | 可重写或删除 |
| `deprecated` | 端点移除 | 待清理的过时测试 |

## 健康评分

评分维度：
- 锁定测试通过率 (40%)
- 端点覆盖率 (25%)
- 高风险路径覆盖 (20%)
- 测试稳定性 (15%)

## 许可证

MIT
