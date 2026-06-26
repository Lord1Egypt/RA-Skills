# Skill 卸载流程详细指南

卸载流程要和新的安装逻辑保持一致。重点不是只删一个固定目录，而是先找到 skill 真正装在哪，再删那一份。

## 第一步：定位当前平台

先沿用安装阶段的同一套平台判断逻辑。

### Codex

候选目录：

- `.agents/skills/<skill-name>/`
- `~/.agents/skills/<skill-name>/`
- `~/.codex/skills/<skill-name>/`

相关配置：

- `~/.codex/config.toml`

### Claude Code

候选目录：

- `.claude/skills/<skill-name>/`
- `~/.claude/skills/<skill-name>/`

相关配置：

- `.claude/settings.json`
- `.claude/settings.local.json`
- `~/.claude/settings.json`

### OpenClaw

候选目录：

- `skills/<skill-name>/`
- `.agents/skills/<skill-name>/`
- `~/.agents/skills/<skill-name>/`
- `~/.openclaw/skills/<skill-name>/`

相关配置：

- `~/.openclaw/openclaw.json`

## 第二步：确认 skill 是否存在

检查候选目录时，至少确认：

1. 目录存在
2. 目录内有 `SKILL.md`
3. frontmatter 的 `name` 与目标 skill 一致，或目录名一致

如果同名 skill 同时存在多份：

1. 列出全部路径
2. 让用户确认删哪一份
3. 如果用户说“全部卸载”，再逐个删除

## 第三步：请求确认

建议展示这些信息：

```text
即将卸载以下 skill
名称: cocoloop
平台: Codex
路径: /absolute/path/to/skill
范围: 项目级 / 用户级
```

如果用户要求强制卸载，可以跳过确认。

## 第四步：执行卸载

处理顺序：

1. 删除目标 skill 目录
2. 如果该路径在平台配置里被显式引用，提示用户同步清理
3. 清理 Cocoloop 自己的缓存记录

### Codex 额外检查

如果 `~/.codex/config.toml` 里存在指向该 skill 的 `[[skills.config]]` 条目：

- 删除对应条目
- 或提示用户手动清理

### Claude Code 额外检查

Claude Code 通常不需要单独维护 skill 注册表，但如果团队把相关说明写进 `.claude/settings.json` 或本地说明文档里，也要提醒用户同步更新。

### OpenClaw 额外检查

如果 `~/.openclaw/openclaw.json` 的 `skills.load.extraDirs` 里还保留了一个已经废弃的个人 skill 目录，可以提醒用户继续保留或清理。

## 第五步：验证卸载结果

至少检查三件事：

1. 目录已经不存在
2. 不会再从同一路径读到 `SKILL.md`
3. 如果平台有显式路径配置，该配置已移除或已提醒用户处理

## 批量卸载

批量卸载时，把每个 skill 当成独立任务处理：

1. 定位
2. 确认
3. 删除
4. 汇总结果

如果一个 skill 卸载失败，不影响其他 skill 继续处理。

## 可选备份

如果用户担心误删，可以先备份：

```text
~/.cocoloop/backups/<skill-name>-<timestamp>.tar.gz
```

建议在下面几种情况下优先备份：

- 用户级 skill 将被覆盖或删除
- skill 来源已经不可访问
- 该 skill 带脚本或自定义资源较多

## 恢复思路

如果用户想恢复：

1. 查找备份压缩包
2. 解压到原来的目标目录
3. 重新执行一次安装后校验

## 错误处理

| 场景 | 处理方式 |
| --- | --- |
| 找不到 skill | 列出候选目录并说明未命中 |
| 权限不足 | 改为删除用户级目录，或提示用户提升权限 |
| 同名 skill 有多份 | 先列出路径，不要擅自全删 |
| 目录删掉了但配置仍引用 | 明确提醒用户还有残留配置 |
