# 羊毛猎人 (Deals Hunter) v2.1

基于什么值得买 Feed RSS + 慢慢买实时数据的多源羊毛推荐系统。

## ✨ 特性

- 🎯 **20 个商品推荐** - 每天 3 次推送，每次 20 个精选优惠
- 📊 **多数据源** - 什么值得买 (30个) + 慢慢买 (10个)
- 💰 **详细价格信息** - 当前价格、历史低价查询
- 📈 **价格曲线** - 提供慢慢买查询链接
- 🔗 **多平台购买** - 包含购买链接和比价链接
- ⏰ **定时推送** - 9:00 AM / 12:00 PM / 6:00 PM

## 📦 安装

```bash
npx clawhub install deals-hunter
```

## 🚀 使用方法

### 自动运行（推荐）

已配置 Cron Jobs：
- deals-morning (9:00 AM)
- deals-noon (12:00 PM)
- deals-evening (6:00 PM)

### 手动触发

```bash
cd /Users/xufan65/.openclaw/workspace
python3 scripts/multi-source-deals.py
```

## 📊 数据源

### 1. 什么值得买 Feed RSS
- URL: `http://feed.smzdm.com`
- 商品数: 30 个
- 类型: 实时优惠商品
- 优势: 纯优惠，无文章

### 2. 慢慢买
- URL: `https://cu.manmanbuy.com/`
- 商品数: 10 个
- 类型: 价格监控数据
- 优势: 实时价格

## 🔥 输出格式

每个商品包含：

```markdown
### 1. 商品名称

💰 **当前价格**: ¥XXX
📉 **历史低价**: 需访问商品页查看
📊 **价格趋势**: 建议使用慢慢买查询历史价格曲线

🛒 **购买链接**:
- 什么值得买: <https://...>
- 慢慢买比价: <https://...>

📡 **来源**: 什么值得买 / 慢慢买
💡 **提示**: 点击购买链接查看详细价格和历史趋势
```

## 📋 推送配置

**Discord 频道**: 
- 频道: `#scheduled`
- 线程: `🛒 daily-deals` (ID: 1481207243188867093)

**配置文件**: 
- `/Users/xufan65/.openclaw/workspace/config/deals-hunter.json`

## 🛠️ 技术栈

- **Python 3**: 数据抓取
- **feedparser**: RSS 解析
- **requests**: HTTP 请求
- **BeautifulSoup4**: HTML 解析
- **Discord**: 消息推送

## 📈 版本历史

### v2.1.0 (2026-03-11)
- ✅ 推荐数量提升到 20 个
- ✅ 添加历史价格查询链接
- ✅ 优化输出格式
- ✅ 修复 Discord 频道问题

### v2.0.0 (2026-03-11)
- ✅ 数据源升级到什么值得买 Feed RSS
- ✅ 从 11 个增加到 40 个优惠
- ✅ 创建多数据源脚本

### v1.0.0 (2026-03-09)
- ✅ 初始版本
- ✅ 基于慢慢买数据源

## 🎯 效果对比

| 指标 | v1.0 | v2.0 | v2.1 | 提升 |
|------|------|------|------|------|
| **数据源** | 1 个 | 2 个 | 2 个 | ⬆️ 100% |
| **优惠数量** | 11 个 | 40 个 | 40 个 | ⬆️ 264% |
| **推荐数量** | 5 个 | 10 个 | **20 个** | ⬆️ 300% |
| **历史价格** | ❌ | ❌ | ✅ | ✅ 新增 |

## ⚠️ 注意事项

1. 部分优惠有地区限制
2. 88VIP 价格需要会员资格
3. 优惠信息实时变化，建议尽快查看
4. 价格仅供参考，以实际购买页面为准

## 📝 待优化

- [ ] 配置 Tavily API 获取详细价格信息
- [ ] 添加京东、天猫、拼多多数据源
- [ ] 实现自动查询历史价格
- [ ] 添加价格趋势分析
- [ ] 支持用户偏好筛选

## 📄 许可证

MIT License

## 👤 作者

- ClawHub: https://clawhub.com/sunnyhot
- GitHub: https://github.com/sunnyhot

---

**发现问题？** 请在 [GitHub Issues](https://github.com/sunnyhot/deals-hunter/issues) 提交
