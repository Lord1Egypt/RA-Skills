---
name: baidu-finance-search
version: 1.0.1
description: 百度财经搜索 skill。基于超哥方法论定制，支持雪球/知乎/东方财富/同花顺等站点的财经舆情搜索，适合短线情绪博弈和事件驱动分析。
emoji: 💹
---

# 百度财经搜索 Skill

基于**超哥方法论**定制的财经搜索工具，使用百度千帆 AI 搜索（web_summary）接口。

---

## 核心能力

| 场景 | 站点 | 用途 |
|------|------|------|
| **短线主线（情绪博弈）** | 雪球、东方财富 | 舆情热度、资金动向 |
| **短线非主线（事件驱动）** | 东方财富、同花顺 | 公告、政策、财报 |
| **中线（趋势跟随）** | 知乎、雪球 | 板块轮动分析 |

---

## API 信息

| 项目 | 值 |
|------|-----|
| **Endpoint** | `https://qianfan.baidubce.com/v2/ai_search/web_summary` |
| **认证** | `Authorization: Bearer {API_KEY}` |
| **请求方式** | POST |

---

## 使用方式

### 命令行调用

```bash
python3 skills/baidu-finance-search/scripts/search.py '<JSON参数>'
```

### 快捷搜索

```bash
# A股行情分析
python3 skills/baidu-finance-search/scripts/search.py '{
  "query": "如何看待今日A股行情",
  "sites": ["xueqiu.com", "www.eastmoney.com"]
}'

# 板块轮动分析
python3 skills/baidu-finance-search/scripts/search.py '{
  "query": "半导体板块轮动分析",
  "sites": ["xueqiu.com", "www.zhihu.com"]
}'

# 个股舆情
python3 skills/baidu-finance-search/scripts/search.py '{
  "query": "宁德时代 最新讨论",
  "sites": ["xueqiu.com"],
  "time_range": "3d"
}'
```

---

## 请求参数

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| `query` | string | ✅ 是 | - | 搜索问题 |
| `sites` | list | 否 | 雪球、东财 | 搜索站点列表 |
| `time_range` | string | 否 | 无 | 时间范围（1d/3d/1w/1m） |
| `top_k` | int | 否 | 10 | 返回结果数量 |
| `instruction` | string | 否 | 金融专家 | 系统指令 |

---

## 预设站点

| 站点 | 域名 | 说明 |
|------|------|------|
| 雪球 | xueqiu.com | 股民社区 |
| 东方财富 | www.eastmoney.com | 财经门户 |
| 同花顺 | www.10jqka.com.cn | 财经门户 |
| 知乎 | www.zhihu.com | 知识问答 |

---

## 配置

在 `skills/.env` 中配置：

```
BAIDU_API_KEY=bce-v3/ALTAK-xxx
```

---

## 与方法论对应

| 方法论场景 | 推荐站点 | 示例查询 |
|------------|----------|----------|
| 短线主线-情绪博弈 | 雪球、东财 | "如何看待今日A股行情" |
| 短线非主线-事件驱动 | 东财、同花顺 | "XX股票 公告解读" |
| 中线-趋势跟随 | 知乎、雪球 | "半导体板块轮动分析" |