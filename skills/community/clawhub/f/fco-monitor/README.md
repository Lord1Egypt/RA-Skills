# ⚽ FC Online官网监控Skill

[![OpenClaw Skill](https://img.shields.io/badge/OpenClaw-Skill-blue.svg)](https://clawhub.com)
[![Version](https://img.shields.io/badge/version-1.0.0-green.svg)](https://clawhub.com/skills/fco-monitor)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

自动监控FC Online（足球在线4）官网活动，发现新活动时及时通知。特别适合关注26TOTY/TOTYN赛季卡、TY礼包等游戏活动的玩家。

## ✨ 功能特性

- **🕒 定时监控**：可配置检查时间（默认每天8:00-23:00整点）
- **🔔 智能通知**：只有发现新活动时才发送通知
- **🎯 优先级识别**：自动识别高优先级活动（绝版礼包、限时折扣等）
- **📊 详细报告**：提供活动时间、内容、奖励等完整信息
- **⚡ 快速检查**：支持手动立即检查官网状态

## 🚀 快速开始

### 安装
```bash
# 通过SkillHub安装
openclaw skill install fco-monitor

# 或手动安装
git clone https://github.com/openclaw/skill-fco-monitor.git
cd skill-fco-monitor
./install.sh
```

### 基本使用
```bash
# 立即检查官网活动
fco-monitor check-now

# 设置定时监控（8:00-23:00，每小时）
fco-monitor setup 8 23 60

# 查看监控状态
fco-monitor status
```

## 📋 使用示例

### 在OpenClaw对话中使用
```
用户：帮我监控FC Online官网，每天8点到24点整点检查新活动。
助手：好的！已设置定时监控，每天8:00-23:00整点检查官网...
```

### 监控输出示例
```
🎯 【FC Online新活动通知】

🔥 高优先级活动
📅 发布时间：03/20
📝 活动内容：26TOTY绝版礼包上线
🎁 核心奖励：26TY/TYN赛季BEST1人9强球员包
⏰ 限时优惠：3月20日-3月31日折扣阶段
🔗 官网地址：https://fco.qq.com/main.shtml
```

## ⚙️ 配置说明

### 配置文件位置
```
/root/.openclaw/config/fco-monitor.json
```

### 主要配置项
```json
{
  "checkSchedule": {
    "startHour": 8,
    "endHour": 23,
    "intervalMinutes": 60
  },
  "keywords": {
    "highPriority": ["26TOTY", "绝版", "TY礼包", "限时折扣"],
    "normalPriority": ["赛季", "活动", "更新", "公告"]
  }
}
```

## 🏗️ 系统要求

- **OpenClaw**：>= 1.0.0
- **Node.js**：>= 14.0.0
- **系统工具**：curl, jq
- **网络**：可访问 https://fco.qq.com

## 📁 文件结构
```
fco-monitor/
├── SKILL.md          # 完整技能文档
├── README.md         # 本文件
├── package.json      # 包配置
├── fco-monitor.sh    # 主监控脚本
├── openclaw-integration.js # OpenClaw集成
├── install.sh        # 安装脚本
├── EXAMPLES.md       # 使用示例
├── QUICK_START.md    # 快速开始指南
└── LICENSE           # 许可证文件
```

## 🔧 开发指南

### 本地开发
```bash
# 克隆仓库
git clone https://github.com/openclaw/skill-fco-monitor.git
cd skill-fco-monitor

# 安装依赖
npm install

# 测试运行
npm test
```

### 添加新功能
1. Fork 本仓库
2. 创建功能分支 (`git checkout -b feature/新功能`)
3. 提交更改 (`git commit -m '添加新功能'`)
4. 推送到分支 (`git push origin feature/新功能`)
5. 创建 Pull Request

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

### 贡献者
- [OpenClaw Assistant](https://github.com/openclaw) - 初始版本

## 📄 许可证

本项目基于 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。

## 📞 支持

- 提交 Issue: [GitHub Issues](https://github.com/openclaw/skill-fco-monitor/issues)
- SkillHub 页面: [clawhub.com/skills/fco-monitor](https://clawhub.com/skills/fco-monitor)
- OpenClaw 文档: [docs.openclaw.ai](https://docs.openclaw.ai)

## 🌟 Star 历史

[![Star History Chart](https://api.star-history.com/svg?repos=openclaw/skill-fco-monitor&type=Date)](https://star-history.com/#openclaw/skill-fco-monitor&Date)

---

**让游戏监控更智能，不错过任何重要活动！** ⚽🎮