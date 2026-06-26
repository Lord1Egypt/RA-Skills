# 技能更新模板

## 更新流程规范

### 1. 版本规划
```markdown
## [X.Y.Z] - YYYY-MM-DD

### Added (新功能)
- [ ] 

### Changed (功能变更)
- [ ] 

### Deprecated (即将弃用)
- [ ] 

### Removed (已移除)
- [ ] 

### Fixed (问题修复)
- [ ] 

### Security (安全更新)
- [ ] 
```

### 2. 文件更新清单

#### 必须更新的文件
- [ ] `CHANGELOG.md` - 添加新版本记录
- [ ] `SKILL.md` - 更新文档（如有功能变更）
- [ ] `_meta.json` - 版本号自动更新（发布时）

#### 可能需要更新的文件
- [ ] `index.js` - 核心逻辑
- [ ] `scripts/` 目录下的Python脚本
- [ ] `assets/` 目录下的模板和资源
- [ ] `QUICK_START.md` - 快速开始指南
- [ ] `INSTALLATION_TEST.md` - 安装验证指南

### 3. 测试清单

#### 预发布测试
- [ ] 运行安装测试: `./test_installation.sh`
- [ ] 验证核心功能:
  - [ ] 招聘功能: `python3 scripts/recruit_agent.py test_agent test_role`
  - [ ] 绑定功能: `python3 scripts/bind_bot.py test_agent test_app test_secret` (模拟)
  - [ ] 环境检查: `python3 scripts/check_env.py`
- [ ] 验证文档:
  - [ ] 所有Markdown文件语法正确
  - [ ] 图片链接可访问
  - [ ] 代码示例可运行

#### 兼容性测试
- [ ] OpenClaw版本兼容性
- [ ] 操作系统兼容性（Linux）
- [ ] Python版本兼容性（3.8+）
- [ ] Node.js版本兼容性

### 4. 发布流程

#### 步骤1: 本地验证
```bash
# 1. 更新版本号
echo "当前版本: 2.3.1"
echo "目标版本: X.Y.Z"

# 2. 运行完整测试
cd ~/.openclaw/workspace/skills/feishu-team-manager
./test_installation.sh

# 3. 验证监控脚本
python3 scripts/monitor_usage.py
```

#### 步骤2: 更新CHANGELOG
在`CHANGELOG.md`文件顶部添加新版本记录：
```markdown
## [X.Y.Z] - YYYY-MM-DD

### Added
- 新功能描述

### Changed  
- 变更描述

### Fixed
- 修复问题描述
```

#### 步骤3: 发布到ClawHub
```bash
# 发布新版本
clawhub publish . \
  --slug "feishu-team-manager" \
  --name "飞书团队管理器 (HR 大姐头)" \
  --version "X.Y.Z" \
  --changelog "vX.Y.Z: 更新描述" \
  --tags "feishu,lark,hr,recruitment,agent-management,team"
```

#### 步骤4: 验证发布
```bash
# 检查发布状态
clawhub list | grep feishu-team-manager

# 从ClawHub重新安装验证
clawhub install feishu-team-manager --force
```

### 5. 版本命名规范

#### 语义化版本 (SemVer)
- **主版本号 (X)**: 不兼容的API修改
- **次版本号 (Y)**: 向下兼容的功能性新增
- **修订号 (Z)**: 向下兼容的问题修正

#### 版本示例
- `1.0.0`: 初始发布
- `1.1.0`: 新增功能，兼容1.0.0
- `1.1.1`: 修复bug，兼容1.1.0
- `2.0.0`: 重大更新，不兼容1.x

### 6. 回滚流程

#### 发现严重问题
如果发布后发现严重问题，立即执行：

```bash
# 1. 回滚到上一个版本
clawhub install feishu-team-manager@上一个版本号 --force

# 2. 更新CHANGELOG添加回滚说明
# 在最新版本记录中添加回滚说明

# 3. 通知用户
# 在技能页面发布公告
```

#### 回滚记录模板
```markdown
## [X.Y.Z] - YYYY-MM-DD (已回滚)

### ⚠ 重要通知
此版本因发现严重问题 [问题描述] 已被回滚。
请用户立即升级到版本 [安全版本号]。

### 问题详情
- 问题描述
- 影响范围
- 临时解决方案

### 回滚操作
- 回滚时间: YYYY-MM-DD HH:MM
- 回滚版本: 从 X.Y.Z 回滚到 X.Y.(Z-1)
- 操作人员: [姓名]
```

### 7. 更新通知模板

#### Discord公告模板
```
🎉 **feishu-team-manager vX.Y.Z 已发布!**

**更新内容**:
- 新增功能1
- 修复问题2
- 优化体验3

**立即更新**:
```bash
clawhub update feishu-team-manager
```

**技能页面**: https://clawhub.com/skills/feishu-team-manager
**完整日志**: 查看CHANGELOG.md

#feishu #skill-update
```

#### 飞书群公告模板
```
【技能更新通知】飞书团队管理器 vX.Y.Z 已发布

📋 更新内容：
✅ 新增功能：描述
✅ 问题修复：描述  
✅ 体验优化：描述

🔧 更新方法：
1. 命令行：clawhub update feishu-team-manager
2. 或重新安装：clawhub install feishu-team-manager --force

📖 详细更新日志：查看技能目录下的 CHANGELOG.md

如有问题，请及时反馈！
```

### 8. 质量检查清单

#### 代码质量
- [ ] 无语法错误
- [ ] 代码注释完整
- [ ] 错误处理完善
- [ ] 日志记录清晰

#### 文档质量  
- [ ] 更新日志完整
- [ ] 使用说明准确
- [ ] 示例代码可运行
- [ ] 故障排除指南完善

#### 用户体验
- [ ] 安装流程顺畅
- [ ] 功能使用直观
- [ ] 错误提示友好
- [ ] 性能表现良好

### 9. 发布后监控

#### 监控指标
- 下载量变化
- 用户反馈收集
- 错误率统计
- 使用频率分析

#### 监控脚本
```bash
# 发布后24小时运行监控
cd ~/.openclaw/workspace/skills/feishu-team-manager
python3 scripts/monitor_usage.py
```

### 10. 模板使用说明

1. **复制此模板**到新文件 `UPDATE_PLAN_vX_Y_Z.md`
2. **填写具体内容**，勾选完成的项目
3. **按照流程执行**，确保每个步骤都完成
4. **保存记录**，作为版本发布的历史文档

---
**模板版本**: 1.0.0  
**最后更新**: 2026-04-23  
**维护者**: feishu-team-manager 开发团队