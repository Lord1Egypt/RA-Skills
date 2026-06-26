# Backup Strategies

## 🚨 Emergency Recovery (First Section)

**If OpenClaw is completely broken and cannot start:**

### Quick Recovery (2 commands)
```bash
# 1. List critical backups
ls -lht ~/.openclaw/backups/critical/

# 2. Restore (replace with your backup file)
bash ~/.openclaw/workspace/skills/backup-manager/restore.sh ~/.openclaw/backups/critical/YOUR_BACKUP.tar.gz
```

### Why This Works
- **Independent script**: `restore.sh` is pure bash, no OpenClaw dependency
- **Auto-backup**: Creates backup of current state before restoring
- **Verification**: Checks file integrity after restore
- **Safe**: Requires confirmation before overwriting

### Emergency Guides
- **Quick**: `~/OPENCLAW_EMERGENCY_RECOVERY.md`
- **Detailed**: `~/.openclaw/backups/README.md`
- **Full**: `recovery-guide.md`

---

## Backup Targets

### Critical Configuration Files
1. **OpenClaw主配置**：`~/.openclaw/openclaw.json`
2. **模型配置**：`~/.openclaw/agents/main/agent/models.json`
3. **代理配置**：`~/.openclaw/agents/main/agent/agent.json`
4. **插件配置**：`~/.openclaw/plugins/` 目录结构

### Workspace重要文件
1. **身份文件**：`MEMORY.md`, `USER.md`, `SOUL.md`, `IDENTITY.md`
2. **待办清单**：`LAOCHEN_TODOLIST.md`, `XIACHEN_TODOLIST.md`, `OUR_TODOLIST.md`
3. **心跳配置**：`HEARTBEAT.md`
4. **工具配置**：`TOOLS.md`

### 技能配置
1. **重要技能配置**：关键技能的配置文件
2. **自定义脚本**：用户创建的脚本文件

### 自开发Skills（每周备份）
1. **arxiv-paper-collector**：arXiv论文收集系统
2. **backup-manager**：备份管理器
3. **pdf-processor**：PDF处理（翻译+概述）

## Retention Policies

### 备份保留策略
| 备份类型 | 保留期限 | 清理规则 |
|----------|----------|----------|
| **每日备份** | 7天 | 自动删除超过7天的每日备份 |
| **每周备份** | 4周 | 自动删除超过4周的每周备份 |
| **每月备份** | 12个月 | 自动删除超过12个月的每月备份 |
| **重大修改备份** | 永久 | 手动清理，或按项目生命周期管理 |

### 备份目录结构 (混合时间分层)
```
~/.openclaw/backups/
├── daily/                    # 每日备份 (保留7天)
│   ├── 2026/
│   │   ├── 03/
│   │   │   ├── 08/
│   │   │   │   ├── config_20260308_020000.tar.gz    # 配置备份 (2:00 AM)
│   │   │   │   └── critical_20260308_103015.tar.gz  # 关键修改前备份
│   │   │   └── 09/
│   │   └── 04/
│   └── latest -> 2026/03/08  # 最新备份软链接
├── weekly/                   # 每周备份 (保留4周)
│   ├── 2026/
│   │   ├── w10/
│   │   │   └── full_20260308_030000.tar.gz          # 完整备份 (周一3:00 AM)
│   │   └── w11/
│   └── latest -> 2026/w10/
├── monthly/                  # 每月备份 (保留12个月)
│   ├── 2026/
│   │   ├── 03/
│   │   │   └── full_20260301_040000.tar.gz          # 完整备份 (每月1日4:00 AM)
│   │   └── 04/
│   └── latest -> 2026/03/
└── critical/                 # 重大修改前备份 (手动清理)
    ├── before-glm-config-20260308_102514.tar.gz
    └── before-plugin-config-20260308_103015.tar.gz
```

### 压缩策略
| 备份类型 | 压缩格式 | 包含内容 | 典型大小 |
|----------|----------|----------|----------|
| **每日配置备份** | `.tar.gz` | 配置文件 + 关键.md文件 | 10-50KB |
| **每周完整备份** | `.tar.gz` | 整个工作空间 + 配置 | 100-500MB |
| **每月完整备份** | `.tar.gz` | 整个工作空间 + 配置 | 100-500MB |
| **关键修改前备份** | `.tar.gz` | 身份文件 + 配置 | 1-10MB |

## Backup Triggers

### 自动触发
1. **每日备份**：凌晨2点自动运行
2. **每周备份**：每周一凌晨3点运行
3. **每月备份**：每月1日凌晨4点运行

### 手动触发
1. **重大修改前**：配置变更前手动运行
2. **技能安装前**：安装新技能前备份
3. **系统升级前**：OpenClaw升级前备份

## Backup Verification

### 完整性检查
1. **文件存在性**：确认所有目标文件都已备份
2. **文件可读性**：验证备份文件可读取
3. **大小检查**：备份文件大小合理
4. **差异检查**：与上次备份对比变化

### 验证命令
```bash
# 检查备份完整性
find ~/.openclaw/backups/latest -type f -exec ls -la {} \;

# 验证文件可读性
find ~/.openclaw/backups/latest -type f -exec head -1 {} \;
```

## Storage Considerations

### 存储位置
1. **本地存储**：`~/.openclaw/backups/`（主要）
2. **外部存储**：可配置同步到外部存储（可选）

### 存储优化
1. **压缩备份**：使用tar.gz压缩减少存储空间
2. **增量备份**：仅备份变化文件（高级功能）
3. **去重存储**：相同文件只存储一次（高级功能）

## Risk Management

### 低风险操作
1. 创建新备份目录
2. 复制配置文件
3. 记录备份日志

### 中风险操作
1. 清理过期备份（需确认）
2. 压缩备份文件（需验证）

### 高风险操作
1. 恢复备份（覆盖现有文件）
2. 删除非过期备份

## Compliance

### 安全要求
1. **权限保护**：备份目录权限700，文件权限600
2. **敏感数据**：不备份明文密码或API密钥
3. **访问控制**：仅限OpenClaw用户访问

### 审计要求
1. **操作日志**：记录所有备份操作
2. **变更跟踪**：跟踪备份策略变更
3. **合规检查**：定期检查备份策略合规性
