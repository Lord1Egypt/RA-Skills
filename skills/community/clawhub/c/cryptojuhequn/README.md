# 二娃聚合群API

飞书群聊总结｜CA地址查询｜链上数据服务

## 简介

这是一个专为加密社区打造的综合数据服务API，聚合了飞书群组聊天记录总结、CA（合约地址）反向查询、以及链上代币数据分析能力。

## 主要功能

- ✅ **CA反向查询** - 输入合约地址，追踪讨论该代币的所有群组
- ✅ **热门CA统计** - 发现社区热议的代币合约
- ✅ **群聊AI总结** - 查询各大KOL群组的每日聊天总结
- ✅ **二级KOL数据** - 获取专业KOL的代币分析和推荐
- ✅ **快讯消息** - 实时获取加密市场重要资讯
- ✅ **链上数据** - 集成DexScreener、GMGN、Binance等数据源

## 快速开始

### 1. 获取Token

联系管理员微信 **erwaNFT** 获取访问Token

### 2. API调用示例

```bash
# 查询CA被哪些群组讨论
curl "http://88.222.241.169/api/v1/group_ca/by-ca/7m3HtU4..." \
  -H "Authorization: Bearer YOUR_TOKEN"

# 获取最新CA
curl "http://88.222.241.169/api/v1/group_ca/latest?limit=5" \
  -H "Authorization: Bearer YOUR_TOKEN"

# 查询群聊总结
curl "http://88.222.241.169/api/v1/summaries?group_name=cryptoD&limit=10" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

## 文档

- 完整API文档: [skill.md](./skill.md)
- Swagger UI: http://88.222.241.169/docs
- 在线文档: http://88.222.241.169/static/skill.md

## 技术栈

- **后端**: FastAPI + Python
- **数据库**: MySQL
- **认证**: Bearer Token
- **部署**: Systemd + Uvicorn

## 联系我们

- 管理员微信: **erwaNFT**
- 服务器地址: http://88.222.241.169

## License

MIT
