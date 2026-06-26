# 02 Backup（回滚点）

**目的**：万一升级炸了，能秒回滚。

**核心备份**：service unit + user 自定义 env。**binary 备份看情况**（如果大版本升级建议备份，小版本可以不备）。

## 一键备份

```bash
# 跑 scripts/backup-env.sh
bash ~/.openclaw/workspace-main/skills/gateway-upgrade-local-fork/scripts/backup-env.sh
```

或手动：

```bash
BACKUP_TS=$(date +%Y%m%d-%H%M%S)
echo "Backup timestamp: $BACKUP_TS"

# 1. 备份 service unit (核心, 必做)
cp ~/.config/systemd/user/openclaw-gateway.service{,.bak.$BACKUP_TS}

# 2. 备份 per agent qmd dbs (核心, 必做)
for db in $(find ~/.openclaw/agents/*/qmd/xdg-cache/qmd/ -name "index.sqlite"); do
    cp "$db" "$db.bak.$BACKUP_TS"
done

# 3. 备份 binary 目录 (大版本升级建议, 小版本可省)
# cp -r $HOME/openclaw-local{,.bak.$BACKUP_TS}

# 4. 备份 plugin configs (大版本升级建议)
# cp -r $HOME/openclaw-local/extensions{,.bak.$BACKUP_TS}

# 5. 记下 npm global packages 列表
npm list -g --depth=0 > /tmp/npm-global-pre-upgrade-$BACKUP_TS.txt

# 6. 记下 qmd doctor baseline
qmd doctor > /tmp/qmd-doctor-pre-upgrade-$BACKUP_TS.txt 2>&1
```

## 备份清单

| 项 | 路径 | 是否必做 |
|------|------|---------|
| service unit | `~/.config/systemd/user/openclaw-gateway.service.bak.<ts>` | ✅ **必做** |
| per agent dbs | `~/.openclaw/agents/*/qmd/xdg-cache/qmd/index.sqlite.bak.<ts>` | ✅ **必做** |
| binary 目录 | `$HOME/openclaw-local.bak.<ts>` | 大版本升级建议 |
| plugin configs | `$HOME/openclaw-local/extensions.bak.<ts>` | 大版本升级建议 |
| npm global 列表 | `/tmp/npm-global-pre-upgrade-<ts>.txt` | ✅ 推荐 |
| qmd doctor baseline | `/tmp/qmd-doctor-pre-upgrade-<ts>.txt` | ✅ 推荐 |

## 验证备份完整性

```bash
# 跑完检查 .bak 大小是不是合理
ls -la ~/.config/systemd/user/openclaw-gateway.service.bak.<ts>
du -sh $HOME/openclaw-local.bak.<ts>  # 如果有
# per agent dbs 数量应该是 33+1（main + 32 个其他），少一个就说明漏备份
ls ~/.openclaw/agents/*/qmd/xdg-cache/qmd/*.bak.<ts> | wc -l
```

## 注意事项

- **per agent db 数量必须 33+1（main + 32 个其他）**，少一个就说明漏备份
- **不要**备份全局 db（`~/.cache/qmd/index.sqlite`），那是 CLI 用的不是 OpenClaw service 用的
- **qmd binary 不一定每次都备份**——这次主要是 env 丢失 + qmd 大版本（2.0.1 → 2.5.3）才重装。日常小版本升级 qmd 不用动
- **service unit 备份是核心**——`$HOME/openclaw-local` 可以重装，service unit 里的 user env 丢了就找不回
