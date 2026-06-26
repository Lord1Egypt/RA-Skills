# 二娃聚合群API - 飞书群聊与链上数据服务

## 工具介绍

**二娃聚合群API** 是一个专为加密社区打造的综合数据服务，聚合了飞书群组聊天记录总结、CA（合约地址）反向查询、以及链上代币数据分析能力。

### 核心能力

1. **飞书群聊AI总结** - 查询各大KOL群组的每日聊天总结
2. **CA反向溯源** - 输入合约地址，追踪讨论该代币的所有群组
3. **热门CA统计** - 发现社区热议的代币合约
4. **二级KOL数据** - 获取专业KOL的代币分析和推荐
5. **快讯消息** - 实时获取加密市场重要资讯
6. **链上数据查询** - 集成DexScreener、GMGN、Binance等数据源

---

## 认证信息

**认证方式**: Bearer Token

```
Authorization: Bearer <your-access-token>
```

**Token获取**: 联系管理员微信 **erwaNFT** 获取访问Token
- 每日调用限制：500次
- Token有效期：1年

---

## API 基础信息

- **Base URL**: `http://88.222.241.169`
- **文档地址**: `http://88.222.241.169/static/skill.md`
- **Swagger UI**: `http://88.222.241.169/docs`

---

## 核心功能

### 1. CA反向查询 - 追踪代币传播路径

通过CA地址查询哪些群组在讨论该代币。

**Endpoint**: `GET /api/v1/group_ca/by-ca/{ca_address}`

**示例请求**:
```bash
curl "http://88.222.241.169/api/v1/group_ca/by-ca/7m3HtU4RDiXWpAt546HHC7Lho3Qzvz6tx2MiAmLiHpLn" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

**响应示例**:
```json
{
  "ca": "7m3HtU4RDiXWpAt546HHC7Lho3Qzvz6tx2MiAmLiHpLn",
  "total_groups": 3,
  "groups": ["crazySen聊天", "孙哥聊天", "猴哥聊天"]
}
```

---

### 2. 获取最新CA - 发现新币

获取群聊中最新的合约地址（过滤条件：CA不为null且http为null）。

**Endpoint**: `GET /api/v1/group_ca/latest`

**示例请求**:
```bash
curl "http://88.222.241.169/api/v1/group_ca/latest?limit=5" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

**响应示例**:
```json
[
  {
    "id": 71295,
    "ca": "4HJe8T85a8XKXjC3XZDWxpPMCaTXUABp4XHcLTjdpump",
    "username": "生气了",
    "group_name": "猴哥聊天",
    "create_time": "2026-03-08T22:23:51",
    "http": null
  }
]
```

---

### 3. 热门CA统计 - 发现社区热点

统计指定日期被提及次数最多的CA。

**Endpoint**: `GET /api/v1/group_ca/popular`

**示例请求**:
```bash
# 查询今天被提及10次以上的CA
curl "http://88.222.241.169/api/v1/group_ca/popular" \
  -H "Authorization: Bearer YOUR_TOKEN"

# 查询昨天被提及20次以上的CA
curl "http://88.222.241.169/api/v1/group_ca/popular?date=2026-03-07&min_count=20" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

**响应示例**:
```json
[
  { "ca": "7m3HtU4...", "count": 23 },
  { "ca": "4HJe8T8...", "count": 18 }
]
```

---

### 4. 群聊AI总结 - KOL观点聚合

查询各大KOL群组的每日AI总结。

**Endpoint**: `GET /api/v1/summaries`

**群组类型映射**:

| 群组类型 | 对应群组 |
|---------|---------|
| **Meme群/土狗群** | cryptoD群、0xSun群、GDC群、猴哥群、金蛙群、985群、镭射猫群、crazySen群、0xAA群、AD群、区块日记群 |
| **空投群** | leng群、P总群、小鑫群、十一地主群、十一空投群、3D群群 |
| **打新群** | 中国万岁群、AKAKAY群、Meta群 |

**示例请求**:
```bash
# 查询Meme群今日总结
curl "http://88.222.241.169/api/v1/summaries?group_name=cryptoD&limit=10" \
  -H "Authorization: Bearer YOUR_TOKEN"

# 查询空投群今日总结
curl "http://88.222.241.169/api/v1/summaries?group_name=leng&limit=10" \
  -H "Authorization: Bearer YOUR_TOKEN"

# 查询指定日期
curl "http://88.222.241.169/api/v1/summaries?group_name=猴哥聊天&date=2026-03-07" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

**响应示例**:
```json
[
  {
    "id": 1,
    "group_name": "crazySen聊天",
    "content": "讨论多个pump.fun代币地址，重点关注SOL生态新项目...",
    "create_at": "2026-03-08T10:30:12"
  }
]
```

---

### 5. 二级KOL数据 - 专业分析

获取二级KOL的代币分析和推荐（自动过滤bitget等屏蔽词）。

**Endpoint**: `GET /api/v1/second_kol/latest`

**示例请求**:
```bash
# 获取最新10条KOL分析
curl "http://88.222.241.169/api/v1/second_kol/latest?limit=10" \
  -H "Authorization: Bearer YOUR_TOKEN"

# 获取指定KOL的数据
curl "http://88.222.241.169/api/v1/second_kol/kol/三木" \
  -H "Authorization: Bearer YOUR_TOKEN"

# 获取所有KOL列表
curl "http://88.222.241.169/api/v1/second_kol/kol_names" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

**响应示例**:
```json
[
  {
    "kol_name": "三木",
    "content": "OPN我之前给出比较高的预期...",
    "token": null,
    "image_urls": [],
    "sent_at": "2026-03-10T19:26:25"
  }
]
```

---

### 6. 快讯消息 - 市场动态

获取加密市场快讯消息。

**Endpoint**: `GET /api/v1/newsflash/today`

**示例请求**:
```bash
# 获取今日快讯
curl "http://88.222.241.169/api/v1/newsflash/today?limit=10" \
  -H "Authorization: Bearer YOUR_TOKEN"

# 获取指定日期
curl "http://88.222.241.169/api/v1/newsflash/date/2026-03-07" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

**响应示例**:
```json
[
  {
    "add_time": 1772884462,
    "title": "美国国防部任命前DOGE官员...",
    "content": "据路透社报道，美国国防部宣布任命...",
    "url": "https://www.reuters.com/..."
  }
]
```

---

### 7. Token使用查询 - 监控配额

查询当前Token的调用次数使用情况。

**Endpoint**: `GET /api/v1/token/usage`

**示例请求**:
```bash
curl "http://88.222.241.169/api/v1/token/usage" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

**响应示例**:
```json
{
  "token": "aaa3b7ad****3efc",
  "token_name": "API Token 500次/年",
  "daily_limit": 500,
  "used_today": 45,
  "remaining_today": 455,
  "reset_time": "2026-03-09 08:00:00"
}
```

---

## 完整工作流示例

### 场景：发现一个CA，想了解背景

```bash
# Step 1: 查哪些群组在讨论
GET /api/v1/group_ca/by-ca/{CA}

# Step 2: 查看链上基础数据（DexScreener直接访问）
https://api.dexscreener.com/latest/dex/tokens/{CA}

# Step 3: 安全审计（GMGN via Jina AI）
https://r.jina.ai/http://gmgn.ai/sol/token/{CA}

# Step 4: 获取AI叙事（Binance Web3）
https://web3.binance.com/bapi/defi/v1/public/wallet-direct/buw/wallet/token/ai/narrative/query?chainId=CT_501&contractAddress={CA}

# Step 5: 查看相关群聊总结
GET /api/v1/summaries?group_name={group}&date={date}
```

---

## 链上工具（无需Token，直接访问）

### DexScreener - 链上基础数据
```
https://api.dexscreener.com/latest/dex/tokens/{ca}
```
- 确认代币所在链
- 查看市值、流动性、持有者数量
- 查看K线图表

### GMGN.ai - 安全审计
```
https://r.jina.ai/http://gmgn.ai/{chain}/token/{ca}
```
- 合约安全审计
- 检测Bundler/Phishing标记
- 查看持仓分布

**Chain参数**: sol | bsc | base | eth

### Binance Web3 - CA叙事查询
```
https://web3.binance.com/bapi/defi/v1/public/wallet-direct/buw/wallet/token/ai/narrative/query?chainId={chain_id}&contractAddress={ca}
```

**Chain ID映射**:
- Solana: `CT_501`
- BSC: `56`
- Base: `8453`

---

## 技术参数

### 限流规则
- 每日限制：500次/Token
- 重置时间：北京时间每日08:00

### 响应格式
- Content-Type: `application/json`
- 编码: UTF-8

### HTTP状态码
- `200`: 成功
- `401`: Token无效或过期
- `429`: 超出每日调用限制
- `500`: 服务器错误

---

## 数据说明

| 数据表 | 记录数 | 更新频率 |
|-------|--------|---------|
| group_ca | ~70,000+ | 实时同步 |
| ai_summary | ~400+ | 每日AI总结 |
| newsflash | ~5,000+ | 实时 |
| second_kol | ~500+ | 实时 |

---

## 联系方式

- **管理员微信**: erwaNFT
- **服务器**: http://88.222.241.169
- **API文档**: http://88.222.241.169/static/skill.md

---

## 更新日志

- **2026-03-08**: 新增二级KOL数据接口、快讯接口、Token使用查询
- **2026-03-07**: 新增群组类型映射、热门CA统计
- **2026-03-06**: 新增CA反向查询、AI群聊总结

---

**提示**: 本文档对应的服务需要Token认证，请联系管理员获取访问权限。
