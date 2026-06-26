# 📰 每日新闻简报 Skill

基于历史模式及近期国际动向（如特朗普即将访华等），每天早上8点自动搜集并发布国际时事、经济形势、科技发展新闻的OpenClaw Skill。

## 🚀 快速开始

### 1. 安装依赖
```bash
cd "C:\Users\User\.openclaw\workspace\skills\daily-news-brief"
npm install
```

### 2. 配置
编辑 `config.json` 文件：
- 调整新闻源
- 设置发布渠道
- 配置历史模式关注点

### 3. 测试运行
```bash
npm test
```

### 4. 设置定时任务
```bash
npm run setup
```

## 📋 功能特性

### 🕐 定时自动执行
- 每天早上8点（北京时间）自动运行
- 支持自定义cron表达式
- 时区自动适配

### 🌍 多领域新闻覆盖
- **国际时事**：中美关系、中东局势、欧洲动态等
- **经济形势**：宏观经济、货币政策、市场动态等
- **科技发展**：人工智能、半导体、新能源、生物科技等

### 🧠 智能筛选与排序
- 基于历史模式优先级排序
- 关键词权重计算
- 新闻去重和过滤
- 特朗普访华等重大事件特别关注

### 📊 专业简报格式
- 统一Markdown格式
- 分类清晰，重点突出
- 包含历史回顾和趋势分析
- 支持多模板定制

### 🔌 多渠道发布
- 飞书集成
- 微信机器人
- 控制台输出
- 邮件通知（可选）
- 历史存档

## ⚙️ 配置说明

### 新闻源配置
```json
{
  "newsSources": {
    "international": ["https://news.cctv.com/world", ...],
    "economic": ["https://finance.sina.com.cn", ...],
    "technology": ["https://tech.sina.com.cn", ...]
  }
}
```

### 历史模式关注
```json
{
  "historicalPatterns": {
    "trumpVisit": true,
    "usChinaRelations": true,
    "middleEastTensions": true,
    "aiDevelopment": true,
    "economicPolicies": true
  }
}
```

### 发布渠道
```json
{
  "outputChannels": ["feishu", "console"],
  "recipients": ["ou_63fe82c05165ad03801998f88ef81025"]
}
```

## 📁 文件结构

```
daily-news-brief/
├── SKILL.md              # 技能详细文档
├── news-brief.js         # 主脚本
├── config.json           # 配置文件
├── package.json          # 依赖配置
├── README.md             # 本文件
├── templates/            # 模板目录
│   ├── brief-template.md # 简报模板
│   └── style.css         # 样式文件
├── history/              # 历史简报存档
│   └── 2026-03-04.md     # 每日简报文件
└── logs/                 # 日志目录
    └── news-brief.log    # 运行日志
```

## 🎯 新闻筛选逻辑

### 优先级关键词
- **国际时事**：特朗普、访华、中美、伊朗、中东等
- **经济形势**：GDP、通胀、美联储、贸易、股市等
- **科技发展**：AI、芯片、电动、光伏、基因等

### 历史模式匹配
- 特朗普访华相关新闻权重最高
- 中美关系动态特别关注
- 基于历史事件的相关性分析

### 智能排序算法
1. 关键词匹配度评分
2. 历史模式相关性
3. 新闻时效性
4. 来源权威性
5. 内容完整性

## 🔧 高级配置

### 自定义新闻源
1. 在 `config.json` 中添加新闻源URL
2. 在 `news-brief.js` 中添加对应的解析函数
3. 调整优先级关键词

### 扩展发布渠道
1. 在 `config.json` 的 `outputChannels` 中添加渠道
2. 在 `NewsPublisher` 类中添加对应的发布方法
3. 配置渠道认证信息

### 个性化模板
1. 编辑 `templates/brief-template.md`
2. 添加自定义变量和逻辑
3. 调整样式和格式

## 🛠️ 故障排除

### 常见问题

#### Q: 新闻获取失败
**A**: 检查网络连接，确认新闻源URL可用，调整超时设置

#### Q: 定时任务不执行
**A**: 检查cron表达式，确认时区设置，查看系统日志

#### Q: 发布到飞书失败
**A**: 检查OpenClaw Feishu集成配置，确认API权限

#### Q: 新闻内容重复
**A**: 调整去重阈值，优化关键词过滤

### 日志查看
```bash
# 查看运行日志
tail -f logs/news-brief.log

# 查看错误日志
grep ERROR logs/news-brief.log
```

### 手动测试
```bash
# 立即运行测试
npm test

# 查看详细调试信息
DEBUG=* npm test
```

## 📈 性能优化

### 缓存策略
- 新闻内容缓存1小时
- 源站状态监控
- 失败重试机制

### 资源管理
- 并发请求控制
- 内存使用监控
- 日志轮转清理

### 扩展性
- 模块化设计
- 插件系统支持
- 配置热更新

## 🔮 未来计划

### 短期目标
- [ ] 增加更多新闻源
- [ ] 优化自然语言处理
- [ ] 添加多语言支持
- [ ] 完善用户反馈机制

### 中期目标
- [ ] 引入机器学习推荐
- [ ] 开发移动端应用
- [ ] 集成日历提醒
- [ ] 添加语音播报功能

### 长期目标
- [ ] 构建新闻知识图谱
- [ ] 开发预测分析功能
- [ ] 建立专家评论系统
- [ ] 打造新闻社交平台

## 📞 技术支持

### 问题反馈
- GitHub Issues: [openclaw/skills](https://github.com/openclaw/skills/issues)
- 邮件支持: support@openclaw.ai

### 文档资源
- [OpenClaw文档](https://docs.openclaw.ai)
- [技能开发指南](https://docs.openclaw.ai/skills/development)
- [API参考](https://docs.openclaw.ai/api)

### 社区交流
- Discord: [OpenClaw社区](https://discord.com/invite/clawd)
- 微信群: 联系管理员获取

## 📄 许可证

MIT License

## 🙏 致谢

感谢所有新闻源提供者，以及OpenClaw社区的支持和贡献。

---

**最后更新**: 2026年3月4日  
**版本**: 1.0.0  
**维护者**: OpenClaw Assistant