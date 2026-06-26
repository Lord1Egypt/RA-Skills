---
name: reference-pointers
description: 系统引用指针，记录核心配置文件、关键数据文件、运行进程、技能位置和故障排除引用
type: reference
---

# 系统引用指针

## 核心配置文件

### OpenClaw 主配置
- **文件路径**： `~/.openclaw/openclaw.json`
- **用途**： 全局配置，包含模型设置、插件配置、安全规则等
- **备份位置**： `~/.openclaw/backups/openclaw-YYYYMMDD.json`
- **重要字段**：
  - `models.default` - 默认模型配置
  - `plugins.enabled` - 启用的插件列表
  - `security.rules` - 安全规则定义
  - `memory.settings` - 记忆系统设置

### Agent 配置文件
- **SOUL.md**： `~/.openclaw/workspace/SOUL.md`
- **IDENTITY.md**： `~/.openclaw/workspace/IDENTITY.md`
- **USER.md**： `~/.openclaw/workspace/USER.md`
- **AGENTS.md**： `~/.openclaw/workspace/AGENTS.md`
- **TOOLS.md**： `~/.openclaw/workspace/TOOLS.md`

### 技能配置
- **技能目录**： `~/.openclaw/workspace/skills/`
- **系统技能**： `/usr/local/lib/node_modules/openclaw/skills/`
- **自定义技能**： `~/.openclaw/workspace/skills/`

## 关键数据文件

### 记忆系统文件
- **MEMORY.md**： `~/.openclaw/workspace/MEMORY.md` - 记忆索引
- **记忆目录**： `~/.openclaw/workspace/memory/` - 详细记忆文件
- **每日记忆**： `~/.openclaw/workspace/memory/YYYY-MM-DD.md`
- **用户画像**： `~/.openclaw/workspace/memory/user-profile.md`

### 日志文件
- **Gateway 日志**： `~/.openclaw/logs/gateway.log`
- **会话日志**： `~/.openclaw/logs/sessions/`
- **审计日志**： `~/.openclaw/workspace/memory/audit-logs/`
- **错误日志**： `~/.openclaw/logs/errors.log`

### 缓存文件
- **模型缓存**： `~/.openclaw/cache/models/`
- **会话缓存**： `~/.openclaw/cache/sessions/`
- **临时文件**： `~/.openclaw/tmp/`

## 运行进程

### 关键进程
| 进程名称 | 命令/标识 | 默认端口 | 用途 |
|----------|-----------|----------|------|
| OpenClaw Gateway | `openclaw gateway` | 18791 | 主网关服务 |
| 浏览器控制 | `chromium` | 9222 | 浏览器自动化 |
| 节点连接 | `openclaw nodes` | 动态 | 节点管理 |

### 监控命令
```bash
# 查看Gateway状态
openclaw gateway status

# 查看运行会话
openclaw sessions list

# 查看节点状态
openclaw nodes status

# 查看系统健康
openclaw status
```

## 技能位置

### 内置技能
- **技能创建器**： `/usr/local/lib/node_modules/openclaw/skills/skill-creator/`
- **GitHub Issues**： `/usr/local/lib/node_modules/openclaw/skills/gh-issues/`
- **Obsidian**： `/usr/local/lib/node_modules/openclaw/skills/obsidian/`
- **Apple 笔记**： `/usr/local/lib/node_modules/openclaw/skills/apple-notes/`

### 工作区技能
- **Claude Code进化**： `~/.openclaw/workspace/skills/claude-code-evolution/`
- **其他自定义技能**： `~/.openclaw/workspace/skills/[技能名称]/`

## 故障排除引用

### 常见问题
1. **Gateway无法启动**
   - 检查端口占用：`lsof -i :18791`
   - 查看日志：`tail -f ~/.openclaw/logs/gateway.log`
   - 重启服务：`openclaw gateway restart`

2. **模型连接失败**
   - 检查API密钥配置
   - 验证网络连接：`curl https://api.openai.com`
   - 查看模型配置：`openclaw config.get models`

3. **记忆检索失败**
   - 检查记忆文件权限
   - 验证记忆索引格式
   - 重建索引：运行记忆验证脚本

4. **工具无法使用**
   - 检查工具权限配置
   - 查看工具分类：`cat ~/.openclaw/workspace/memory/tools-classification-config.yaml`
   - 验证工具加载状态

### 调试命令
```bash
# 详细模式运行
openclaw --verbose

# 调试特定会话
openclaw sessions list --active-minutes 5

# 检查系统依赖
openclaw doctor

# 重置配置（谨慎使用）
openclaw config.reset --force
```

### 紧急恢复
1. **配置文件损坏**
   ```bash
   # 从备份恢复
   cp ~/.openclaw/backups/openclaw-YYYYMMDD.json ~/.openclaw/openclaw.json
   openclaw gateway restart
   ```

2. **记忆文件损坏**
   ```bash
   # 恢复最新备份
   cp -r ~/.openclaw/backups/memory-YYYYMMDD/ ~/.openclaw/workspace/memory/
   ```

3. **完全重置**
   ```bash
   # 警告：这将删除所有配置和数据
   openclaw factory-reset --confirm
   ```

## 外部资源

### 官方文档
- **OpenClaw文档**： https://docs.openclaw.ai
- **GitHub仓库**： https://github.com/openclaw/openclaw
- **社区Discord**： https://discord.com/invite/clawd

### 技能市场
- **ClawHub**： https://clawhub.ai
- **技能搜索**： `openclaw skills search [关键词]`

### 支持渠道
- **GitHub Issues**： https://github.com/openclaw/openclaw/issues
- **Discord社区**： #help 频道
- **邮件支持**： support@openclaw.ai

---

**最后更新**： YYYY-MM-DD  
**维护建议**： 定期更新此文件，保持引用准确  
**版本兼容**： OpenClaw 0.8.0+