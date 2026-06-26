# 安装配置工具指南

## 📦 ClawMerge v2.3.1+ 配套工具

ClawMerge v2.3.1 开始支持**自动导出公开配置**功能，需要安装以下配套脚本。

---

## 🚀 快速安装

### 方法 1：从 workspace 复制（推荐）

如果你已经从 workspace 备份恢复，脚本应该已经存在：

```bash
# 检查是否已安装
ls -la ~/.openclaw/workspace/scripts/export-public-config.py
```

如果不存在，从备份中提取：

```bash
# 从最新备份中提取
cd /tmp
tar -xzf ~/backups/clawmerge-*.tar.gz workspace/scripts/export-public-config.py
mv workspace/scripts/export-public-config.py ~/.openclaw/workspace/scripts/
```

### 方法 2：从 ClawHub 技能包中提取

```bash
# 安装 clawmerge 技能
clawhub install clawmerge

# 提取脚本
cp ~/.openclaw/workspace/skills/clawmerge/scripts/../../scripts/export-public-config.py \
   ~/.openclaw/workspace/scripts/
```

---

## 📋 安装验证

### 检查文件是否存在

```bash
# 检查导出脚本
ls -la ~/.openclaw/workspace/scripts/export-public-config.py

# 检查 configs 目录
ls -la ~/.openclaw/workspace/configs/
```

### 测试导出功能

```bash
# 手动运行一次
python3 ~/.openclaw/workspace/scripts/export-public-config.py

# 应该输出：
# 📋 Export Public Configuration
# ✅ 配置已导出：public-config.json
```

### 测试自动导出

```bash
# 运行备份（会自动导出）
cd ~/.openclaw/workspace/skills/clawmerge/scripts
./one-click-backup.sh --dry-run

# 应该看到：
# [0/5] Exporting public configuration...
# ✓ Public configuration exported
```

---

## 📁 文件结构

安装后的完整结构：

```
~/.openclaw/workspace/
├── scripts/
│   └── export-public-config.py  # ✅ 配置导出脚本
├── configs/
│   └── public-config.json       # ✅ 导出的公开配置
└── skills/
    └── clawmerge/
        └── scripts/
            └── one-click-backup.sh  # ✅ 备份脚本（v2.3.1+）
```

---

## ⚠️ 常见问题

### 问题 1：脚本不存在

**错误信息**：
```
[0/5] Exporting public configuration...
ℹ Export script not found (v2.3.0+ feature)
```

**解决方法**：
```bash
# 安装导出脚本
# 参考上面的"快速安装"部分
```

### 问题 2：configs 目录不存在

**错误信息**：
```
Permission denied: /home/user/.openclaw/workspace/configs
```

**解决方法**：
```bash
# 手动创建目录
mkdir -p ~/.openclaw/workspace/configs
```

### 问题 3：导出失败

**错误信息**：
```
⚠ Export script ran but may have warnings
```

**解决方法**：
```bash
# 查看详细错误
python3 ~/.openclaw/workspace/scripts/export-public-config.py

# 检查 openclaw.json 是否存在
ls -la ~/.openclaw/openclaw.json
```

---

## 🎯 功能说明

### 自动导出（v2.3.1+）

备份时自动执行：

```bash
./one-click-backup.sh
# 自动：
# [0/5] 导出公开配置
# [1/5] 导出 cron 任务
# ...
```

### 手动导出

也可以手动运行：

```bash
python3 export-public-config.py
```

---

## 📊 导出内容

**包含**：
- ✅ 股票持仓列表（38 只）
- ✅ 薛斯通道参数（N=102, M=7）
- ✅ 推送目标群 ID（2 个）
- ✅ Heartbeat 规则（重试 3 次）

**不包含**：
- ❌ API keys（用占位符标注）
- ❌ Gateway tokens
- ❌ 个人隐私信息

---

## 🔗 相关文档

- [CONFIG-BACKUP-GUIDE.md](../../../scripts/CONFIG-BACKUP-GUIDE.md) - 完整使用指南
- [SKILL.md](../SKILL.md) - ClawMerge 技能文档

---

**创建时间**：2026-03-22  
**版本**：v2.3.1  
**维护者**：小虾 🦐
