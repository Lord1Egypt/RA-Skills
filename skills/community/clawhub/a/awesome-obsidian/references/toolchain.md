# 工具链配置

## 已安装的 Skills

### 1. obsidian-git-vault

**用途**：Git 同步管理

**主要功能**：
- 推送/拉取笔记
- 查看历史版本
- 管理远程仓库

**常用命令**：
```bash
# 拉取最新
git pull origin main

# 提交变更
git add . && git commit -m "update: 笔记更新"

# 推送到远程
git push origin main

# 查看状态
git status

# 查看历史
git log --oneline -10
```

**配置信息**：
- 远程仓库：你的 Git 托管平台（GitHub/GitLab/Gitee 等）
- 默认分支：main
- 自动同步：建议手动触发

---

### 2. obsidian-organizer

**用途**：库整理与命名规范

**主要功能**：
- 审计文件命名
- 检查文件夹结构
- 自动修复命名问题

**常用命令**：
```bash
# 审计命名（预览）
python scripts/obsidian_audit.py <vault-path>

# 应用修复
python scripts/obsidian_audit.py <vault-path> --apply
```

**命名规则**：
- 中文笔记：`中文标题.md`
- 英文笔记：`kebab-case.md`
- 日期格式：`YYYY-MM-DD.md`
- 禁止：特殊符号、emoji

---

### 3. obsidian-daily-log

**用途**：每日时间线记录

**主要功能**：
- 记录时间戳活动
- 旅行日志
- 日程追踪

**使用方式**：
```markdown
## Timeline

- 09:00 — 开始工作
- 10:30 — 完成文档整理
- 14:00 — 会议讨论
- 18:00 — 健身
```

**触发词**：
- `/dailylog`
- `/travellog`
- `/timeline`
- "添加到今天的笔记"

---

### 4. excalidraw-handdraw

**用途**：手绘风格图表

**主要功能**：
- 创建架构图、流程图
- 手绘风格渲染
- 支持中文手写字体
- 导出 PNG/SVG

**使用方式**：
```
画一个用户登录流程图
创建一个微服务架构图
生成一个数据库 ER 图
```

**导出命令**：
```bash
# 启动 Canvas
./scripts/start-canvas.sh

# 导出图片
./scripts/export-canvas.sh /tmp/diagram.png

# 保存到指定位置
./scripts/save-to-file.sh --source /tmp/d.png --dest docs/d.png
```

---

## 工具链协同工作流

### 场景 1：从小艺帮记整理笔记

```
1. 查询小艺帮记收藏
   ↓
2. 整理成 Markdown 笔记
   ↓
3. 放入 inbox/
   ↓
4. 定期整理到正确位置
   ↓
5. Git 提交推送
```

### 场景 2：每日记录

```
1. 使用 obsidian-daily-log 记录时间线
   ↓
2. 在 journal/YYYY-MM-DD.md 中追加内容
   ↓
3. Git 提交推送
```

### 场景 3：整理混乱的库

```
1. 使用 obsidian-organizer 审计命名
   ↓
2. 查看问题列表
   ↓
3. 确认后应用修复
   ↓
4. Git 提交推送
```

### 场景 4：创建可视化笔记

```
1. 使用 excalidraw-handdraw 创建图表
   ↓
2. 导出为 PNG
   ↓
3. 插入到笔记中
   ↓
4. Git 提交推送
```

---

## 配置建议

### Git 配置

```bash
# 设置用户信息
git config user.name "Your Name"
git config user.email "your@email.com"

# 设置默认分支
git config init.defaultBranch main

# 设置自动换行
git config core.autocrlf input
```

### 定时任务

建议设置定时任务自动同步：

```bash
# 每 2 小时自动同步
0 */2 * * * cd /path/to/vault && git pull && git add . && git commit -m "auto sync" && git push
```

### 备份策略

1. **本地备份**：定期打包 vault 目录
2. **远程备份**：Git 仓库自动同步
3. **多地备份**：可配置多个远程仓库

---

## 故障排除

### Git 冲突

```bash
# 拉取时遇到冲突
git pull --rebase origin main

# 解决冲突后
git add .
git rebase --continue
git push origin main
```

### 命名审计失败

```bash
# 检查 Python 环境
python3 --version

# 检查脚本路径
ls scripts/obsidian_audit.py

# 手动运行
python3 scripts/obsidian_audit.py <vault-path>
```

### Canvas 无法启动

```bash
# 检查 Docker
docker ps | grep excalidraw

# 重启 Canvas
./scripts/stop-canvas.sh
./scripts/start-canvas.sh
```
