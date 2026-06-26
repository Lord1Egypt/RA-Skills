# Upgrade & Reset — anamnesis-hub 升级与重置指南

> 覆盖版本升级路径、重置处理状态、迁移数据、卸载步骤。
> 最后更新：2026-05-17 | v1.13.1

---

## 一、版本升级路径

### 从旧版本升级（< v1.11）

| 旧版本 | 升级内容 | 操作 |
|--------|----------|------|
| < v1.9 | → v1.10：引入两阶段 pipeline | 运行 `auto_memory_extract.py --mode full` |
| v1.10 | → v1.11：引入 P3 candidates 机制 | 运行 `candidates_review.py stats` 初始化状态文件 |
| v1.11+ | → 最新：无需特殊迁移 | 直接覆盖脚本 |

### 升级步骤

```bash
cd /home/victor/github/anamnesis-hub

# 1. 拉取最新代码
git pull origin main

# 2. 检查版本
cat SKILL.md | grep version

# 3. 更新 openclaw skill（如果通过 clawhub 安装）
openclaw skills update victorqr/anamnesis-hub

# 4. 验证脚本可执行权限
chmod +x scripts/*.sh scripts/*.py

# 5. 可选：重置 session-extract 状态以重新全量处理历史会话
python3 scripts/session-extract.py --reset

# 6. 验证 healthcheck
bash scripts/daily-memory-pipeline.sh status
```

---

## 二、重置处理状态

### session-extract 重置

**场景**：历史会话需要重新提取，或 processedIds 状态损坏。

```bash
# 查看当前状态
cat memory/.session-extract-state.json

# 重置（清除 processedIds，重新全量运行）
python3 scripts/session-extract.py --reset

# 验证
cat memory/.session-extract-state.json
# 应显示: {"processedIds": []}
```

**效果**：重新扫描所有 .jsonl 文件，不再跳过已处理的会话。

---

### auto-memory 重置

**场景**：需要重新从 memos-cloud 缓存提取所有记忆。

**无专用 reset 参数**，但可以通过删除状态文件实现：
```bash
# 清除缓存，重新从云端拉取
rm user_workspace/memos-cloud-cache/memos-cloud-*.md
# 下次 sync-pull 会重新拉取全部历史
```

---

### facts.db 重建

**场景**：facts.sqlite 损坏或需要完全重建。

```bash
# 1. 备份现有 facts.db
cp ~/.openclaw/memory/facts.sqlite ~/.openclaw/memory/facts.sqlite.bak.$(date +%Y%m%d)

# 2. 删除现有 facts.db
rm ~/.openclaw/memory/facts.sqlite

# 3. 从 ARCHIVE.md 重新 seed
python3 scripts/seed-facts-db.py

# 4. 验证
python3 -c "
import sqlite3
conn = sqlite3.connect('/home/victor/.openclaw/memory/facts.sqlite')
n = conn.execute('SELECT COUNT(*) FROM facts').fetchone()[0]
e = conn.execute('SELECT COUNT(DISTINCT entity) FROM facts').fetchone()[0]
print(f'facts.db: {n} facts / {e} entities')
"
```

---

## 三、迁移数据

### 从备份恢复

```bash
# 恢复 MEMORY.md
cp ~/.openclaw/workspace/MEMORY.md.bak.20260512 ~/.openclaw/workspace/MEMORY.md

# 恢复 ARCHIVE.md
cp ~/.openclaw/workspace/ARCHIVE.md.bak.20260512 ~/.openclaw/workspace/ARCHIVE.md

# 恢复 facts.db
cp ~/.openclaw/memory/facts.sqlite.bak.20260512 ~/.openclaw/memory/facts.sqlite

# 恢复 memory/ 日志
cp -r ~/.openclaw/workspace/memory/*.md.bak.20260512 ~/.openclaw/workspace/memory/
```

### 迁移到新设备

```bash
# 1. 在新设备安装 anamnesis-hub
git clone https://github.com/VictorQR/anamnesis-hub.git
cd anamnesis-hub
bash scripts/auto-setup.sh

# 2. 复制 workspace 文件
rsync -avz --exclude='memos-cloud-*.md' --exclude='MEMORY_INDEX.md' \
  user@old-device:/home/victor/.openclaw/workspace/ \
  /home/victor/.openclaw/workspace/

# 3. 复制 memory-core 向量库（可选）
rsync -avz user@old-device:/home/victor/.openclaw/memory/ \
  /home/victor/.openclaw/memory/

# 4. 配置 MemOS API Token
# 将 ~/.openclaw/.env 从旧设备复制到新设备
```

---

## 四、卸载步骤

### 完全卸载

```bash
# 1. 停止并删除所有 cron 任务
openclaw cron list
# 手动删除每个 cron 任务：
openclaw cron remove --id <job-id>

# 2. 删除 memory-core 插件配置（从 openclaw.json 中移除）
# 编辑 ~/.openclaw/openclaw.json，删除 plugins.entries.memory-core

# 3. 删除 MemOS Cloud 插件配置（从 openclaw.json 中移除）
# 编辑 ~/.openclaw/openclaw.json，删除 plugins.entries.memos-cloud-openclaw-plugin

# 4. 重启 Gateway
openclaw gateway restart

# 5. 删除工作区文件（可选，保留备份）
# 先备份
tar -czf ~/anamnesis-hub-backup-$(date +%Y%m%d).tar.gz \
  ~/.openclaw/workspace/memory/ \
  ~/.openclaw/workspace/MEMORY.md \
  ~/.openclaw/workspace/ARCHIVE.md \
  ~/.openclaw/memory/main.sqlite

# 删除
rm -rf ~/.openclaw/workspace/memory/
rm -f ~/.openclaw/workspace/MEMORY.md
rm -f ~/.openclaw/workspace/ARCHIVE.md
rm -f ~/.openclaw/workspace/AGENTS.md
rm -f ~/.openclaw/workspace/SOUL.md
rm -f ~/.openclaw/workspace/USER.md
rm -f ~/.openclaw/workspace/TOOLS.md

# 6. 删除 scripts 目录
rm -rf ~/.openclaw/workspace/user_workspace/scripts/

# 7. 验证
openclaw memory status
# 应显示: memory-core not configured 或类似
```

---

## 五、常见问题

| 问题 | 原因 | 解决 |
|------|------|------|
| 升级后脚本报错 | 依赖路径变化 | 检查 `WORKSPACE` 变量是否指向正确路径 |
| 重置后重复提取 | state 未清除 | 确认 `processedIds` 列表为空 |
| 迁移后向量检索失效 | 向量库未同步 | `openclaw memory index --force` 重建索引 |
| MemOS Cloud 不同步 | API Token 失效 | 在新设备重新配置 token |
| Ollama 模型缺失 | 新设备未安装 | `ollama pull bge-m3` |

---

## 六、备份策略建议

| 数据 | 备份频率 | 保留份数 | 存储位置 |
|------|----------|----------|----------|
| MEMORY.md / ARCHIVE.md | 每日 | 7 份 | 本地 + 云端 |
| memory/YYYY-MM-DD.md | 每周 | 30 份 | 本地 |
| facts.sqlite | 每周 | 4 份 | 本地 |
| openclaw.json | 每次配置变更 | 3 份 | 本地 |
| .env | 每次 token 刷新 | 2 份 | 密码管理器 |