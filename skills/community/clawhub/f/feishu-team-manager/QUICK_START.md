# 飞书团队管理器 - 5分钟快速开始指南

## 🎯 技能简介
**feishu-team-manager**（HR大姐头）是一个自动化招聘和管理飞书多Agent团队的技能。它可以帮助你：
- 快速招聘新的AI Agent员工
- 为每个Agent绑定独立的飞书机器人
- 实现精准的消息路由和身份管理

## 📦 安装步骤

### 方法1: 从ClawHub安装（推荐）
```bash
# 安装技能
clawhub install feishu-team-manager

# 如果遇到安全警告（正常现象），使用强制安装
clawhub install feishu-team-manager --force
```

**注意**：技能可能被VirusTotal标记为"可疑"，这是因为技能包含：
- 配置文件修改功能
- 系统命令执行（用于自动化部署）
- 外部API集成模式
这是正常现象，技能代码已开源可审查。

### 方法2: 手动安装
```bash
# 克隆或下载技能包
cd ~/.openclaw/workspace/skills/
git clone <技能仓库地址> feishu-team-manager

# 激活技能
openclaw gateway restart
```

## 🚀 快速开始

### 第1步: 激活HR大姐头
在OpenClaw对话中，直接说：
```
招聘一个HR大姐头
```
或
```
运行feishu-team-manager
```

系统会自动：
1. 创建HR Agent工作空间
2. 配置独立身份文件
3. 准备招聘工具

### 第2步: 招聘第一个Agent员工
对HR大姐头说：
```
招聘一个运维Agent，起名叫运维小弟
```

系统会：
1. 创建`运维小弟`的工作空间
2. 注入基础身份配置
3. 提示你提供飞书机器人凭据

### 第3步: 绑定飞书机器人
获取飞书机器人凭据（App ID和App Secret），然后说：
```
帮运维小弟绑定机器人，App ID是cli_xxx，Secret是yyy
```

系统会：
1. 自动注入飞书账号配置
2. 设置消息路由规则
3. 重启Gateway生效

## 📋 核心功能详解

### 1. 自动化招聘
```
招聘一个[角色]Agent，起名叫[名字]
```
示例：
- `招聘一个客服Agent，起名叫客服小美`
- `招聘一个运营Agent，起名叫运营总监`
- `招聘一个开发Agent，起名叫代码助手`

### 2. 机器人绑定
```
帮[Agent名字]绑定机器人，App ID是xxx，Secret是yyy
```
示例：
- `帮客服小美绑定机器人，App ID是cli_a1b2c3，Secret是sec_xyz`
- `帮运维小弟绑定机器人，App ID是cli_d4e5f6，Secret是sec_abc`

### 3. 团队状态检查
```
检查团队状态
```
查看所有已招聘的Agent和绑定状态。

## 🔧 故障排除

### 常见问题1: 技能安装失败
**症状**: `clawhub install` 失败
**解决**:
```bash
# 检查网络连接
ping clawhub.com

# 检查ClawHub登录状态
clawhub whoami

# 强制安装
clawhub install feishu-team-manager --force
```

### 常见问题2: 招聘后Agent不工作
**症状**: Agent已创建但无法响应
**解决**:
1. 检查Gateway状态: `openclaw gateway status`
2. 重启Gateway: `openclaw gateway restart`
3. 验证配置: `openclaw doctor`

### 常见问题3: 飞书机器人绑定失败
**症状**: 绑定后收不到消息
**解决**:
1. 验证App ID和Secret是否正确
2. 检查飞书机器人是否已启用
3. 确认机器人有消息接收权限

## 📊 监控和管理

### 查看技能使用统计
```bash
cd ~/.openclaw/workspace/skills/feishu-team-manager
python3 scripts/monitor_usage.py
```

### 验证安装完整性
```bash
cd ~/.openclaw/workspace/skills/feishu-team-manager
./test_installation.sh
```

## 🎨 高级功能

### 自定义Agent身份
每个Agent都有独立的身份文件，可以自定义：
- `IDENTITY.md`: Agent身份和角色
- `SOUL.md`: Agent核心目标和人格
- `AGENTS.md`: Agent工作准则

### 多团队管理
可以创建多个团队，每个团队有独立的：
- 工作空间
- 飞书机器人
- 消息路由规则

### 自动化巡检
技能包含自动巡检功能，定期检查：
- Agent健康状态
- 机器人连接状态
- 配置一致性

## 📞 获取帮助

### 官方资源
- **技能页面**: https://clawhub.com/skills/feishu-team-manager
- **问题反馈**: 在技能页面提交Issue
- **更新日志**: 查看`CHANGELOG.md`

### 社区支持
- **OpenClaw Discord**: https://discord.com/invite/clawd
- **GitHub讨论**: 技能仓库的Discussion板块

### 紧急联系
- **作者微信**: 通过赞赏码联系
- **作者邮箱**: 查看技能页面的作者信息

## 🔄 更新和维护

### 检查更新
```bash
clawhub update feishu-team-manager
```

### 强制更新到最新版
```bash
clawhub update feishu-team-manager --force
```

### 查看版本历史
```bash
cat ~/.openclaw/workspace/skills/feishu-team-manager/CHANGELOG.md
```

## 💡 最佳实践

### 命名规范
- 使用中文或英文名字
- 名字体现Agent角色
- 避免特殊字符

### 权限管理
- 为不同Agent分配不同权限的飞书机器人
- 生产环境使用独立的App ID
- 定期轮换App Secret

### 备份策略
- 技能自动备份配置文件
- 定期导出Agent工作空间
- 保存飞书机器人凭据

---

**最后更新**: 2026-04-23  
**技能版本**: 2.3.1  
**适用版本**: OpenClaw >= 2026.3.20  

> 提示：如果在使用中遇到任何问题，请先运行`./test_installation.sh`验证安装完整性。