# 06 紧急回滚

**触发**：升级后 OpenClaw 完全跑不起来（service 起不来 / crash loop / 关键功能挂）。

## 何时回滚

**回滚**：
- service 启不来（systemd 一直 restart）
- 关键功能 100% 挂（memory_search / per agent / GPU 全坏）
- OpenClaw binary 自身有 bug

**不回滚**（先看 references/05-verify.md 修）：
- watch 5min interval 跑得慢（lazy init）
- 个别 agent 0 vectors（串行 rebuild）
- qmd doctor 报 warning（不是 error）

## 回滚步骤

```bash
# 1. 停 service
systemctl --user stop openclaw-gateway.service

# 2. 恢复旧 binary
rm -rf $HOME/openclaw-local
mv $HOME/openclaw-local.bak.<timestamp> $HOME/openclaw-local

# 3. 恢复 service unit
cp ~/.config/systemd/user/openclaw-gateway.service.bak.<old-ver> \
   ~/.config/systemd/user/openclaw-gateway.service

# 4. 如果 qmd 也升级了, 恢复
# (看 /tmp/npm-global-pre-upgrade-<ts>.txt 对比)
npm install -g @tobilu/qmd@<old-version>

# 5. 重启
systemctl --user daemon-reload
systemctl --user start openclaw-gateway.service
sleep 5

# 6. 验证
systemctl --user status openclaw-gateway.service
qmd doctor
```

## 部分回滚（推荐）

如果只是某个 env 丢了或 qmd 撞 ABI，不需要回滚整个 binary：

```bash
# 修 service unit + restart
# 5.28 升级包改了 service unit 但没保留 user 自定义 env
# 重新追加丢失的 env (LD_LIBRARY_PATH / CUDA_HOME / QMD_EMBED_MODEL / HF_ENDPOINT)
# 参考 [references/03-upgrade.md](./03-upgrade.md) 步骤 3
systemctl --user daemon-reload
systemctl --user restart openclaw-gateway.service

# 重编 better-sqlite3 (修 ABI mismatch)
cd $(npm root -g)/@tobilu/qmd
npm rebuild better-sqlite3
systemctl --user restart openclaw-gateway.service
```

## 回滚后必做

```bash
# 1. 跑 qmd doctor 确认 GPU 加速
qmd doctor | grep -E "device|fingerprint"

# 2. 测 memory_search 工具
# (跟升级前一样操作, 应该回到升级前状态)

# 3. per agent qmd db 应该还是升级前状态
# (因为我们备份了 .bak, restore 后 db 内容还是老的)
```

## 留 .bak 多长时间

- **短期**（7 天）：保证升级稳定期
- **中期**（30 天）：覆盖 OpenClaw 已知 bug 修复期
- **长期**：可以删除释放磁盘（binary 备份可能 300-500MB × 多次升级）

```bash
# 30 天后清理老的 .bak
find $HOME -name "openclaw-local.bak.*" -mtime +30 -exec rm -rf {} \;
find $HOME/.config/systemd/user -name "*.service.bak.*" -mtime +30 -exec rm {} \;
```
