# 发布说明

## 工具名称
二娃聚合群API - 飞书群聊与链上数据服务

## 一句话描述
专为加密社区打造的综合数据服务，聚合飞书群聊AI总结、CA反向查询、二级KOL分析和链上数据查询。

## 功能亮点

1. **CA反向溯源** - 输入合约地址，一键追踪所有讨论群组
2. **热门CA发现** - 统计社区热议代币，发现早期机会
3. **KOL群聊总结** - AI聚合各大KOL群组观点，省时高效
4. **二级KOL数据** - 专业分析师的代币推荐和策略
5. **实时快讯** - 加密市场重要资讯即时获取
6. **链上数据集成** - DexScreener、GMGN、Binance一键查询

## 适用场景

- 🔍 看到一个CA，想了解哪些KOL在讨论
- 📊 发现社区热点代币，追踪传播路径
- 💡 获取专业KOL的代币分析和操作建议
- 📰 快速了解加密市场重要动态
- 🔗 查询代币链上数据和安全信息

## 技术规格

- **协议**: HTTP REST API
- **认证**: Bearer Token
- **数据格式**: JSON
- **限流**: 500次/天/Token
- **Base URL**: http://88.222.241.169

## 核心接口

| 接口 | 功能 |
|-----|------|
| `GET /api/v1/group_ca/by-ca/{ca}` | CA反向查询 |
| `GET /api/v1/group_ca/latest` | 获取最新CA |
| `GET /api/v1/group_ca/popular` | 热门CA统计 |
| `GET /api/v1/summaries` | 群聊AI总结 |
| `GET /api/v1/second_kol/latest` | 二级KOL数据 |
| `GET /api/v1/newsflash/today` | 今日快讯 |
| `GET /api/v1/token/usage` | Token使用查询 |

## 群组覆盖

- **Meme/土狗群**: cryptoD、0xSun、GDC、猴哥、金蛙、985、镭射猫、crazySen等
- **空投群**: leng、P总、小鑫、十一地主、十一空投、3D群等
- **打新群**: 中国万岁、AKAKAY、Meta等

## 获取方式

联系管理员微信: **erwaNFT**

## 文档

- API文档: http://88.222.241.169/static/skill.md
- Swagger UI: http://88.222.241.169/docs

## 更新日志

- 2026-03-08: 新增二级KOL、快讯、Token使用查询
- 2026-03-07: 新增热门CA统计、群组类型映射
- 2026-03-06: 上线CA反向查询、AI群聊总结
