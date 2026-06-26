# Enterprise AI Assistant Bundle | 企业 AI 助手部署包

**一站式企业 AI 助手解决方案：飞书 + OpenClaw 集成，5 分钟搭建智能客服/群聊助手/自动化工作流**

## 🎯 适用场景

- 企业需要快速部署 AI 客服
- 团队需要智能群聊助手
- 自动化审批/通知/报表生成
- 零代码配置，开箱即用

## 📦 包含内容

1. **飞书机器人配置** - 完整配置文件 + 部署脚本
2. **OpenClaw 集成** - 预配置 AI 模型（DeepSeek/智谱/通义）
3. **常用技能包**：
   - 智能客服（自动回复 FAQ）
   - 群聊助手（会议安排/提醒）
   - 审批自动化（请假/报销）
   - 日报生成器

## 🚀 快速开始

### 1. 安装依赖
```bash
pip install openclaw lark
```

### 2. 配置飞书应用
1. 访问 [飞书开放平台](https://open.feishu.cn)
2. 创建企业自建应用
3. 获取 App ID 和 App Secret
4. 配置事件订阅（消息接收）

### 3. 运行部署脚本
```bash
python deploy.py --app-id YOUR_APP_ID --app-secret YOUR_APP_SECRET
```

### 4. 测试
在飞书群聊中 @机器人 发送消息，AI 将自动回复。

## 💰 定价

| 版本 | 价格 | 功能 |
|------|------|------|
| 基础版 | ¥99 | 单机器人 + 基础问答 |
| 高级版 | ¥299 | 多机器人 + 自定义技能 |
| 企业版 | ¥999 | 私有部署 + 定制开发 |

## 🔧 技术支持

- 微信：OpenClawCN（备注：企业 AI 助手）
- 邮箱：support@openclaw.cn
- Discord：https://discord.gg/clawd

## 📄 License

MIT License - 购买后可商用、可二次开发

---

**作者**：OpenClaw 中文社区
**版本**：1.0.0
**更新时间**：2026-03-17
