# dida365-skill

`dida365-skill` 是一个基于 Python 3 标准库实现的 Claude Code / Gemini CLI Skill / OpenClaw Skill，用于通过 Dida365 (滴答清单) / TickTick OpenAPI 管理任务和项目。

它的目标是提供一组稳定、可组合的 CLI 子命令，让 AI 模型能够可靠地完成任务创建、查询、更新、删除、项目管理和高级字段操作。

## 🌟 主要能力

- **OAuth 2.0 授权**：完整的授权流支持。
- **项目管理**：创建、更新、删除及列出所有清单。
- **任务管理**：增删改查、标记完成、跨项目移动。
- **高级任务**：支持 Checklist (子任务) 以及通过 JSON 传入 OpenAPI 高级字段。
- **智能查询**：今日待办、未来到期、指定区间到期/已完成任务、高级筛选。
- **零依赖**：仅使用 Python 标准库，无需安装任何第三方包。

## 🛠️ 快速开始

### 1. 创建开发者应用

1. 登录 [滴答清单开发者平台](https://developer.dida365.com/manage)。
2. 创建新应用，并将 `OAuth redirect URL` 设置为：`http://localhost:18365/callback`。
3. 获取 `Client ID` 和 `Client Secret`。

### 2. 配置环境

```bash
cp .env.example .env
```

编辑 `.env` 文件，填入你的凭据：

```dotenv
DIDA_CLIENT_ID=your_client_id
DIDA_CLIENT_SECRET=your_client_secret
```

### 3. 完成授权

```bash
python3 index.py auth
```

按照提示在浏览器中完成授权。如果是远程服务器，可使用 `--code` 参数手动提交授权码。

## 📖 常用命令示例

### 项目清单

- **列出清单**：`python3 index.py project list`
- **查看项目任务**：`python3 index.py project get <projectId>`
- **创建清单**：`python3 index.py project create "工作"`

### 任务操作

- **创建任务**：`python3 index.py task create "写周报" --due 2026-03-20 --priority 5`
- **创建清单任务**：`python3 index.py task create-checklist "出差" --items "订票|订酒店"`
- **查看任务详情**：`python3 index.py task get <projectId> <taskId>`
- **完成任务**：`python3 index.py task complete <projectId> <taskId>`

### 查询与筛选

- **今日任务**：`python3 index.py search today`
- **未来 10 天任务**：`python3 index.py search upcoming 10`
- **高级筛选**：`python3 index.py search filter --priority 3,5 --tags 工作`
- **查看收集箱**：`python3 index.py search inbox`

## ⚡ 性能优化与缓存

为了减少网络请求并提高响应速度，本项目内置了**清单与任务缓存**功能：

- **自动缓存**：`project list`、`project get` 以及所有 `search` 命令的结果默认缓存 **365 分钟**。
- **全局配置**：可以通过环境变量 `DIDA_CACHE_MINUTES` 修改缓存时长。
- **强制更新**：在上述命令后添加 `--force` 参数（如 `python3 index.py project list --force`）可跳过缓存直接获取最新数据。
- **手动清空**：运行 `python3 index.py project clear-cache` 可立即清空本地缓存文件。
- **智能失效**：当执行创建、更新、删除或完成操作时，受影响的项目缓存会自动失效，确保下次查询时获取正确结果。

## 💡 使用技巧

1. **组合命令**：AI 模型在处理任务时，通常会先通过 `project list` 获取项目 ID，再通过 `project get` 获取任务列表。利用缓存可以显著加快这一过程。
2. **环境变量**：建议在 `.env` 中设置 `DIDA_CACHE_MINUTES=5` 以平衡速度与实时性。
3. **故障排查**：如果发现数据未及时同步（例如在网页端做了修改），请在命令中加入 `--force` 参数或运行 `clear-cache`。

### 高级 JSON 模式 (Raw Mode)

支持通过 stdin 传入 OpenAPI 风格的 JSON 以配置复杂字段：

```bash
cat <<'JSON' | python3 index.py task create-raw
{
  "title": "重复任务",
  "projectId": "inbox",
  "repeatFlag": "RRULE:FREQ=DAILY;INTERVAL=1"
}
JSON
```

## 📄 仓库说明

- `SKILL.md`: **AI 模型阅读专用**。包含详细的指令集、参数规范和故障排除方案。
- `index.py`: CLI 主入口，封装了全部业务逻辑。
- `auth.py`: 负责 OAuth 授权流与 Token 管理。
- `LICENSE`: MIT 开源许可证。

## 🤝 致谢与版权说明

本项目的最初版本由 [fanxing-6](https://github.com/fanxing-6/dida365-skill) 开发，目前进行了优化并重构。

本项目基于 **MIT License** 开源。在保留原作者版权信息的基础上，由 [woodcoal](https://github.com/woodcoal) 进行了优化与功能扩展，包括但不限于：

- 优化 CLI 命令结构，支持更清晰的层级调用（如 `project list`, `task create`）。
- 增强了 Checklist 和高级 JSON 字段的处理能力。
- 完善了面向 AI Agent (如 Claude Code, Gemini CLI, OpenClaw Skill) 的 `SKILL.md` 文档。

---

_声明：本工具并非滴答清单官方出品。_
