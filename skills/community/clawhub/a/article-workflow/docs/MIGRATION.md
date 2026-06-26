# Skill 迁移指南

## 背景

为了便于管理和迁移，将文章分析工作流相关的脚本和文档重构为一个独立的 Skill。

## 重构前后对比

### 重构前 ❌

```
~/.openclaw/workspace/
├── scripts/
│   ├── check_url_dup.py
│   └── monitor-articles.sh
├── docs/
│   ├── 文章分析自动化配置.md
│   ├── 文章质量评分标准.md
│   └── 文章分析工作流优化汇总.md
└── data/                    # 散落在工作区根目录
└── logs/                    # 散落在工作区根目录
```

**问题：**
- ❌ 文件分散，难以管理
- ❌ 不易迁移到其他工作区
- ❌ 没有统一的安装/卸载流程
- ❌ 配置分散

### 重构后 ✅

```
~/.openclaw/workspace/skills/article-workflow/
├── SKILL.md                 # Skill 定义
├── README.md                # 使用文档
├── install.sh               # 安装脚本
├── config.example.json      # 配置模板
├── .gitignore              # Git 忽略规则
├── scripts/
│   ├── check_url_dup.py
│   └── monitor.sh
├── docs/
│   ├── quality-score.md
│   └── automation.md
├── data/                   # 运行时数据（.gitignore）
│   ├── url_cache.json
│   └── stats.json
└── logs/                   # 日志（.gitignore）
    ├── workflow.log
    └── error.log
```

**优势：**
- ✅ 所有文件内聚在一个目录
- ✅ 可插拔（安装/卸载方便）
- ✅ 易迁移（复制整个目录即可）
- ✅ 配置集中管理
- ✅ 运行时数据隔离

---

## 安装方法

### 方法 1: 使用安装脚本（推荐）

```bash
cd ~/.openclaw/workspace/skills/article-workflow
./install.sh
```

### 方法 2: 手动安装

```bash
# 1. 创建目录
mkdir -p ~/.openclaw/workspace/skills/article-workflow/{scripts,docs,data,logs}

# 2. 复制文件
cp -r /path/to/article-workflow/* ~/.openclaw/workspace/skills/article-workflow/

# 3. 复制配置模板
cp config.example.json config.json

# 4. 设置权限
chmod +x scripts/*.sh scripts/*.py
```

---

## 配置方法

### 1. 复制配置模板

```bash
cd skills/article-workflow
cp config.example.json config.json
```

### 2. 编辑配置

```json
{
  "bitable": {
    "app_token": "你的多维表格 Token",
    "table_id": "表 ID"
  },
  "workflow": {
    "check_interval_hours": 6,
    "batch_limit": 10,
    "enable_quality_score": true,
    "enable_url_dedup": true
  }
}
```

### 3. 配置 Heartbeat（可选）

编辑 `~/.openclaw/workspace/HEARTBEAT.md`：

```markdown
### 每 6 小时
- [ ] 检查群聊未处理文章链接 → article-workflow
```

---

## 使用方法

### 分析文章

在飞书群聊中：

```
@机器人 分析这篇文章：https://mp.weixin.qq.com/s/xxx
```

### 监控命令

```bash
cd skills/article-workflow

# 查看状态
./scripts/monitor.sh status

# 生成周报
./scripts/monitor.sh report

# 清理数据
./scripts/monitor.sh cleanup
```

### URL 去重

```bash
# 检查 URL
python3 scripts/check_url_dup.py "https://example.com/article"

# 添加到缓存
python3 scripts/check_url_dup.py "https://example.com/article" \
  --add "标题" "record_id" "https://doc.url"
```

---

## 迁移到其他工作区

### 步骤

1. **打包 Skill**
   ```bash
   cd ~/.openclaw/workspace/skills
   tar -czf article-workflow.tar.gz article-workflow/
   ```

2. **复制到目标工作区**
   ```bash
   scp article-workflow.tar.gz user@host:/path/to/workspace/skills/
   ```

3. **解压安装**
   ```bash
   cd /path/to/workspace/skills
   tar -xzf article-workflow.tar.gz
   cd article-workflow
   ./install.sh
   ```

4. **配置**
   - 编辑 `config.json`
   - 配置飞书授权
   - 测试功能

---

## 卸载方法

```bash
# 1. 从 openclaw.json 移除配置（如果有）
# 2. 删除 Skill 目录
rm -rf ~/.openclaw/workspace/skills/article-workflow

# 3. 清理运行时数据（可选）
rm -rf ~/.openclaw/workspace/data/article-workflow
rm -rf ~/.openclaw/workspace/logs/article-workflow
```

---

## 文件说明

### 核心文件

| 文件 | 用途 | 是否必需 |
|------|------|---------|
| `SKILL.md` | Skill 定义和入口 | ✅ 必需 |
| `README.md` | 使用文档 | ✅ 必需 |
| `install.sh` | 安装脚本 | ✅ 必需 |
| `config.example.json` | 配置模板 | ✅ 必需 |
| `config.json` | 实际配置 | ✅ 必需（安装时自动生成） |

### 脚本文件

| 文件 | 用途 | 是否必需 |
|------|------|---------|
| `scripts/check_url_dup.py` | URL 去重检查 | ⚠️ 推荐 |
| `scripts/monitor.sh` | 监控日志 | ⚠️ 推荐 |
| `scripts/workflow.py` | 主工作流（待实现） | ❌ 可选 |

### 文档文件

| 文件 | 用途 |
|------|------|
| `docs/quality-score.md` | 质量评分标准 |
| `docs/automation.md` | 自动化配置说明 |

### 运行时文件（.gitignore）

| 文件 | 用途 | 清理周期 |
|------|------|---------|
| `data/url_cache.json` | URL 去重缓存 | 保留 1000 条 |
| `data/stats.json` | 统计数据 | 永久 |
| `logs/workflow.log` | 主日志 | 30 天 |
| `logs/error.log` | 错误日志 | 30 天 |

---

## 版本历史

### v1.0.0 (2026-03-14)

- ✅ 初始版本
- ✅ 完整的目录结构
- ✅ 安装脚本
- ✅ 配置模板
- ✅ 监控脚本
- ✅ URL 去重

---

## 常见问题

### Q: 如何更新 Skill？

```bash
cd skills/article-workflow
git pull  # 如果是 git 仓库
./install.sh  # 重新运行安装脚本
```

### Q: 配置文件包含敏感信息怎么办？

- ✅ `config.json` 已在 `.gitignore` 中
- ✅ 使用 `config.example.json` 作为模板
- ✅ 不要将 `config.json` 提交到版本控制

### Q: 如何备份数据？

```bash
# 备份数据目录
tar -czf article-workflow-data-backup.tar.gz \
  skills/article-workflow/data/
```

### Q: 如何查看日志？

```bash
# 查看实时日志
tail -f skills/article-workflow/logs/workflow.log

# 查看错误日志
tail -f skills/article-workflow/logs/error.log
```

---

## 最佳实践

1. **定期清理日志**
   ```bash
   ./scripts/monitor.sh cleanup
   ```

2. **每周查看报告**
   ```bash
   ./scripts/monitor.sh report
   ```

3. **监控 URL 缓存大小**
   ```bash
   cat data/url_cache.json | python3 -c "import sys,json; print(len(json.load(sys.stdin)['urls']))"
   ```

4. **备份重要数据**
   - 定期备份 `data/stats.json`
   - 导出 Bitable 数据

---

*最后更新：2026-03-14*
*版本：v1.0.0*
