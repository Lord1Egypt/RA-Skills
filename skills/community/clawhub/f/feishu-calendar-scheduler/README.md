# 飞书日历智能调度器

基于 OpenClaw 的飞书日历智能调度工具，帮助企业自动化会议安排，提高工作效率。

## ✨ 功能特性

### 核心功能
- 🕒 **智能时间推荐**：基于规则推荐最佳会议时间
- 📅 **批量会议管理**：批量创建、修改、取消日程
- 📊 **报表分析**：会议统计和效率分析
- 🔗 **飞书集成**：无缝接入飞书日历和工作流

### 高级功能
- ⚡ **实时冲突检测**：避免时间冲突
- 🌐 **多时区支持**：全球团队协作
- 🎯 **个性化规则**：自定义调度偏好
- 📈 **效率优化**：基于历史数据的学习优化

## 🚀 快速开始

### 安装要求
- OpenClaw 2026.3.8+
- 飞书插件 (feishu-openclaw-plugin)
- Python 3.8+

### 安装步骤
```bash
# 1. 下载技能包
git clone https://github.com/openclaw-skills/feishu-calendar-scheduler.git

# 2. 运行安装脚本
cd feishu-calendar-scheduler
./install.sh

# 3. 验证安装
openclaw calendar-recommend --help
```

### 快速试用
```bash
# 推荐会议时间
openclaw calendar-recommend \
  --start "2026-03-17T09:00:00+08:00" \
  --end "2026-03-19T18:00:00+08:00" \
  --duration 60

# 批量创建周会
openclaw calendar-batch \
  --template "团队周会" \
  --start-date "2026-03-17" \
  --repeat 4 \
  --attendees "团队全员"

# 生成月度报表
openclaw calendar-report \
  --month "2026-03" \
  --format excel
```

## 💰 定价方案

### 免费试用 (7天)
- ✓ 最多10个会议
- ✓ 基础时间推荐
- ✓ 简单报表
- ✓ 社区支持

### 专业版 ¥99/月
- ✓ 无限会议数量
- ✓ 所有智能功能
- ✓ 高级报表和分析
- ✓ 邮件支持
- ✓ API 访问

### 企业版 ¥499/月
- ✓ 多团队管理
- ✓ 定制化开发
- ✓ 优先技术支持
- ✓ SLA 保证
- ✓ 培训服务

## 📋 使用示例

### 场景1：团队周会安排
```bash
# 为10人团队安排下周会议
openclaw calendar-recommend \
  --start "2026-03-24T09:00:00+08:00" \
  --end "2026-03-28T17:00:00+08:00" \
  --duration 90 \
  --attendees "user1,user2,user3,user4,user5,user6,user7,user8,user9,user10" \
  --format json
```

### 场景2：季度规划会议
```bash
# 批量创建季度会议
openclaw calendar-batch \
  --name "2026年Q2规划会" \
  --start-date "2026-04-01" \
  --frequency monthly \
  --count 3 \
  --duration 120 \
  --attendees "管理层,各部门负责人"
```

### 场景3：会议效率分析
```bash
# 分析上月会议效率
openclaw calendar-report \
  --period "2026-02" \
  --metrics "参与率,准时率,时长效率" \
  --output html
```

## 🔧 技术架构

```
┌─────────────────┐
│   用户界面层     │
│  • 命令行工具    │
│  • 飞书机器人    │
│  • Web界面      │
└────────┬────────┘
         │
┌────────▼────────┐
│   业务逻辑层     │
│  • 调度算法      │
│  • 冲突检测      │
│  • 规则引擎      │
└────────┬────────┘
         │
┌────────▼────────┐
│   数据访问层     │
│  • 飞书日历API   │
│  • 本地缓存      │
│  • 配置文件      │
└────────┬────────┘
         │
┌────────▼────────┐
│   存储层        │
│  • 飞书多维表格  │
│  • SQLite数据库 │
└─────────────────┘
```

## 📁 项目结构

```
feishu-calendar-scheduler/
├── SKILL.md              # 技能元数据
├── README.md             # 本文档
├── install.sh            # 安装脚本
├── scripts/              # 核心脚本
│   ├── recommend.py      # 时间推荐算法
│   ├── batch.py          # 批量管理
│   ├── report.py         # 报表生成
│   └── utils.py          # 工具函数
├── config/               # 配置文件
│   ├── default.json      # 默认配置
│   └── rules/            # 调度规则
├── docs/                 # 文档
│   ├── api.md           # API文档
│   ├── examples.md      # 示例文档
│   └── faq.md           # 常见问题
└── tests/               # 测试文件
    ├── test_recommend.py
    └── test_integration.py
```

## 🔐 许可证管理

### 试用期
- 安装后自动开始7天免费试用
- 试用期内功能完整
- 试用到期后需要购买许可证

### 许可证激活
```bash
# 购买后获取许可证密钥
openclaw calendar-license --activate YOUR_LICENSE_KEY

# 检查许可证状态
openclaw calendar-license --status
```

### 续费提醒
- 到期前7天开始提醒
- 到期前3天再次提醒
- 到期后进入功能受限模式

## 🤝 支持与贡献

### 获取帮助
- 📧 邮箱：support@clawhub.com
- 💬 社区：https://discord.com/invite/clawd
- 📖 文档：https://docs.clawhub.com/skills/feishu-calendar-scheduler

### 报告问题
- GitHub Issues: https://github.com/openclaw-skills/feishu-calendar-scheduler/issues
- 功能请求：通过社区或邮箱提交

### 贡献代码
1. Fork 项目仓库
2. 创建功能分支
3. 提交代码变更
4. 发起 Pull Request

## 📊 性能指标

- 时间推荐响应时间：< 100ms
- 批量操作支持：最多1000个会议
- 并发用户支持：最多100个并发
- 数据准确性：> 95%

## 🚀 路线图

### v1.0 (2026年3月)
- [x] 基础时间推荐算法
- [x] 简单会议管理
- [x] 命令行界面

### v1.1 (2026年4月)
- [ ] 飞书机器人集成
- [ ] 图形化配置界面
- [ ] 更多报表类型

### v1.2 (2026年5月)
- [ ] API 开放接口
- [ ] 第三方系统集成
- [ ] 高级算法优化

### v2.0 (2026年Q3)
- [ ] 机器学习优化
- [ ] 预测性调度
- [ ] 企业级功能

---

**开始您的智能日历之旅，提高会议效率，节省宝贵时间！**