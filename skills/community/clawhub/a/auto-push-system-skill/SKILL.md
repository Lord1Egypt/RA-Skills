---
name: auto-push-system-skill
description: 全自动化AI内容监控与飞书推送工作流，支持多源内容检测、自动文档创建、智能错误恢复。当用户需要自动化推送AI生成的内容（播客摘要、技能学习总结、对话简报等）到飞书时使用此技能。
---

# AI内容自动推送系统技能

## 📊 技能概述
**AI内容自动推送系统** - 一个成熟的生产级自动化工作流，能够监控、处理并将AI生成的内容推送到飞书，实现零人工干预。

### 核心功能
✅ **全自动化** - 零人工干预  
✅ **多源监控** - AI播客摘要、技能学习总结、对话简报  
✅ **智能内容检测** - 实时检测新内容生成  
✅ **智能推送** - 自动创建飞书文档和通知  
✅ **错误恢复** - 内置容错和自愈机制  
✅ **日志与审计** - 完整的执行历史和状态跟踪  

---

## 🏗️ 系统架构

### **核心组件**
1. **内容监控器** - 检测日志文件中的`CONTENT_READY`信号
2. **文档创建器** - 将内容转换为飞书文档
3. **通知管理器** - 向目标聊天/群组发送提醒
4. **状态跟踪器** - 记录所有操作和结果
5. **调度器** - 按预定计划执行任务

### **工作流程**
```
内容生成 → 日志信号 → 自动检测 → 飞书文档创建 → 通知 → 记录保存
```

---

## 🛠️ 安装与配置

### **系统要求**
- OpenClaw Gateway 正在运行
- 飞书应用已获得用户授权
- Cron服务已启用

### **快速设置**
```bash
# 1. 将技能复制到工作区
cp -r /path/to/skill ~/.openclaw/workspace/skills/auto-push-system

# 2. 安装依赖
bash ~/.openclaw/workspace/skills/auto-push-system/scripts/install.sh

# 3. 配置设置
bash ~/.openclaw/workspace/skills/auto-push-system/scripts/configure.sh
```

---

## ⚙️ 配置说明

### **基本设置**
```bash
# 通知目标聊天ID
TARGET_CHAT_ID="oc_c133e85bd6eb593e08dcf7aed3a8530b"

# 日志文件位置
AI_PODCAST_LOG="/var/log/ai-podcast-digest.log"
SKILL_DIGEST_LOG="/var/log/skill-digest.log"
CONVERSATION_LOG="/var/log/conversation-brief.log"

# 内容检测模式
CONTENT_PATHS="/tmp/*.md"
CONTENT_SIGNAL="CONTENT_READY"
```

### **调度配置**
```bash
# AI播客摘要：每天12:00, 22:30
0 12 * * * /bin/bash /path/to/ai-podcast-digest.sh
30 22 * * * /bin/bash /path/to/ai-podcast-digest.sh

# 其他任务
0 8 * * * /bin/bash /path/to/skill-digest.sh
0 22 * * * /bin/bash /path/to/conversation-brief.sh
```

---

## 🚀 使用指南

### **1. 手动执行**
```bash
# 检查系统状态
bash ~/.openclaw/workspace/skills/auto-push-system/scripts/status.sh

# 运行单次内容检查
bash ~/.openclaw/workspace/skills/auto-push-system/scripts/check-content.sh

# 强制推送特定内容
bash ~/.openclaw/workspace/skills/auto-push-system/scripts/push-content.sh /path/to/content.md
```

### **2. 自动化监控**
系统自动执行：
- 每5分钟扫描日志文件
- 检测`CONTENT_READY`信号
- 创建飞书文档
- 发送通知
- 记录所有操作

### **3. 支持的内容类型**
- 🎙️ AI播客摘要
- 📚 技能学习总结  
- 💬 对话简报

---

## 🔍 监控与维护

### **健康检查**
```bash
# 系统健康检查
bash ~/.openclaw/workspace/skills/auto-push-system/scripts/health-check.sh

# 查看执行日志
tail -f /var/log/auto-push-system.log
```

### **日志位置**
- `/var/log/auto-push-system.log` - 主执行日志
- `/var/log/auto-push-cron.log` - Cron执行日志
- `/var/log/processed-records.jsonl` - 成功处理的内容记录

### **状态命令**
```bash
# 查看最近活动
bash ~/.openclaw/workspace/skills/auto-push-system/scripts/activity-report.sh

# 生成性能报告
bash ~/.openclaw/workspace/skills/auto-push-system/scripts/performance-report.sh
```

---

## 🚨 故障排除

### **常见问题与解决方案**

| 问题 | 症状 | 解决方案 |
|------|------|----------|
| **飞书授权失败** | `unknown command 'feishu_create_doc'` | 确保飞书应用已正确授权 |
| **Cron未运行** | 无日志或活动 | 检查cron服务状态：`systemctl --user status cron` |
| **内容未检测** | 新文件未处理 | 验证日志文件包含`CONTENT_READY`信号 |
| **API频率限制** | 错误429或类似 | 实施指数退避或批量处理 |

### **诊断命令**
```bash
# 运行完整诊断
bash ~/.openclaw/workspace/skills/auto-push-system/scripts/diagnostics.sh

# 测试飞书连接性
bash ~/.openclaw/workspace/skills/auto-push-system/scripts/test-feishu.sh
```

---

## 📈 高级功能

### **1. 智能内容优先级**
- 实时内容评分
- 基于优先级的推送调度
- 自适应交付优化

### **2. 动态调度管理**
- 时区感知执行
- 基于内容负载的自适应时间
- 跨可用资源的负载均衡

### **3. 分析与洞察**
- 推送成功率
- 用户参与度指标
- 性能优化建议

### **4. 安全与合规**
- 端到端加密
- 访问控制和审计跟踪
- GDPR/CCPA合规准备

---

## 🎯 性能指标

### **关键性能指标**
| 指标 | 目标 | 描述 |
|------|------|------|
| **可用性** | 99.9% | 系统可用性 |
| **检测率** | >95% | 新内容检测准确率 |
| **推送成功率** | >98% | 成功创建飞书文档率 |
| **平均处理时间** | <60秒 | 从内容就绪到通知的时间 |

### **优化技巧**
- 使用高效的正则表达式进行日志扫描
- 实现增量日志读取
- 缓存频繁访问的数据
- 优化API调用频率

---

## 🔗 集成指南

### **1. 与现有AI内容系统集成**
```bash
# 添加内容生成钩子
# 当内容就绪时，添加信号：
echo "CONTENT_READY path=/path/to/content.md title=您的标题" >> /var/log/您的应用.log
```

### **2. 与自定义通知系统集成**
```bash
# 扩展通知处理器
bash ~/.openclaw/workspace/skills/auto-push-system/scripts/extend-notifications.sh
```

### **3. 与数据分析平台集成**
```bash
# 导出活动数据
bash ~/.openclaw/workspace/skills/auto-push-system/scripts/export-analytics.sh
```

---

## 📄 文档结构

### **文件组织**
```
skills/auto-push-system/
├── SKILL.md                  # 此文件 - 主文档
├── README.md                # 快速开始指南
├── LICENSE                 # 许可证文件
├── scripts/                # 所有可执行脚本
│   ├── install.sh         # 安装脚本
│   ├── configure.sh       # 配置脚本
│   ├── run.sh            # 主执行脚本
│   ├── check-content.sh   # 内容监控
│   ├── push-content.sh    # 内容推送逻辑
│   └── status.sh          # 系统状态检查
├── config/                # 配置文件
│   ├── settings.conf     # 主设置
│   ├── schedules.conf   # 任务调度
│   └── notifications.conf # 通知设置
├── examples/             # 使用示例
│   ├── basic-setup.sh   # 基本配置示例
│   ├── custom-content.sh # 自定义内容集成
│   └── advanced-features.sh # 高级使用
└── tests/               # 测试脚本
    ├── unit-tests.sh    # 单元测试
    ├── integration.sh  # 集成测试
    └── performance.sh  # 性能测试
```

---

## 📚 附加资源

### **学习材料**
- [工作流设计最佳实践](docs/workflow-design.md)
- [错误处理模式](docs/error-handling.md)
- [性能优化指南](docs/performance.md)
- [安全实现](docs/security.md)

### **社区支持**
- 加入OpenClaw Discord社区
- 访问ClawHub知识库
- 参与社区论坛
- 为开源改进做贡献

---

## 🚀 开始使用清单

### **✅ 预安装**
- [ ] OpenClaw Gateway正在运行
- [ ] 飞书应用已授权
- [ ] Cron服务已启用
- [ ] 有足够的磁盘空间

### **✅ 安装步骤**
1. [ ] 将技能文件复制到工作区
2. [ ] 运行安装脚本
3. [ ] 配置设置
4. [ ] 设置调度
5. [ ] 测试基本功能

### **✅ 安装后**
1. [ ] 验证cron作业已设置
2. [ ] 测试内容检测
3. [ ] 验证飞书通知
4. [ ] 检查系统日志
5. [ ] 确认自动化正常工作

---

## 🎉 技能部署与发布

### **发布到ClawHub**
```bash
# 1. 打包技能
bash ~/.openclaw/workspace/skills/auto-push-system/scripts/package-skill.sh

# 2. 上传到ClawHub
# 访问 https://clawhub.com 并上传打包的技能
```

### **技能元数据**
```json
{
  "name": "AI内容自动推送系统",
  "version": "1.0.1",
  "description": "全自动化的AI内容监控与飞书推送工作流",
  "author": "Bianca1227",
  "license": "MIT",
  "keywords": ["自动化", "人工智能", "飞书", "内容", "工作流", "推送"],
  "compatibility": {
    "openclaw": ">=1.0.0"
  },
  "requirements": [
    "飞书OAuth授权",
    "Cron服务访问权限"
  ]
}
```

---

## 🌟 专业技巧与最佳实践

### **1. 监控卓越性**
- 设置系统故障的自动警报
- 实施主动健康检查
- 维护全面的审计跟踪

### **2. 可扩展性策略**
- 设计以适应不断增加的内容量
- 实现并行处理能力
- 优化资源利用率

### **3. 维护掌握**
- 安排定期系统审计
- 根据使用模式更新配置
- 基于性能指标进行优化

### **4. 可靠性重点**
- 实现冗余处理路径
- 设计健壮的错误恢复机制
- 确保一致的内容交付质量

---

## 🔄 未来路线图

### **计划中的增强功能**
- 🔄 **多平台支持** (微信、钉钉、Slack)
- 🔄 **高级AI内容过滤** (基于机器学习的相关性评分)
- 🔄 **实时分析仪表板**
- 🔄 **多语言内容支持**
- 🔄 **与流行AI工具集成** (ChatGPT, Claude, Gemini)

### **社区贡献**
- 鼓励开源协作
- 支持自定义内容类型的插件系统
- 易于扩展的模块化架构

---

## 📞 支持与联系

### **获取帮助**
- **文档**: [docs.openclaw.ai](https://docs.openclaw.ai)
- **社区**: [Discord OpenClaw社区](https://discord.com/invite/openclaw)
- **问题**: 在GitHub仓库报告错误

### **技能信息**
- **版本**: 1.0.1
- **发布日期**: 2026-03-31
- **作者**: Bianca1227
- **许可证**: MIT

---

**🎯 准备好部署一个坚如磐石的AI内容自动化系统了吗？**  
从快速安装开始，体验零接触内容推送自动化！