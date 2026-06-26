# Codex-CLI-Guardian

> Codex CLI 封装技能，详细说明见 [SKILL.md](./SKILL.md)

## 快速开始

1. **设置 API Key**
   ```bash
   bash skills/codex-cli-guardian/scripts/init-setup.sh
   ```

2. **告诉小萌你想做什么**，例如：
   - 「帮我写一个爬虫」
   - 「用 Codex 重构这个模块」
   - 「开发一个 REST API」

   小萌会先确认，然后用 Codex 执行。

3. **任务在后台运行**，完成后自动通知你。

## 管理命令

| 命令 | 说明 |
|------|------|
| `/codex-guardian status` | 查看当前状态 |
| `/codex-guardian list` | 查看任务历史 |
| `/codex-guardian kill` | 终止当前任务 |
| `/codex-guardian reset` | 重置状态 |

## 详细文档

- [SKILL.md](./SKILL.md) — 完整技能说明
- [EXAMPLES.md](./EXAMPLES.md) — 使用示例
- [REFERENCES.md](./REFERENCES.md) — 格式标准
- [CLI.md](./CLI.md) — Codex CLI 参考
