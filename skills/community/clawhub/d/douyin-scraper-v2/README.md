# 抖音爆款爬虫 Skill v2.0

使用抖音 Web API 获取热榜和搜索数据，**无需登录**。

## 🚀 快速开始

```bash
# 安装
cd douyin-scraper && npm install

# 搜索
node scripts/douyin_scraper.js search "海鲜" 20

# 热榜
node scripts/douyin_scraper.js hot 50

# 搜索建议
node scripts/douyin_scraper.js suggest "海鲜售卖"
```

## 📝 命令

| 命令 | 说明 | 示例 |
|------|------|------|
| `search <关键词> [数量]` | 搜索 (热榜匹配+建议) | `search "海鲜" 20` |
| `hot [数量]` | 获取热榜 | `hot 50` |
| `suggest <关键词>` | 搜索建议 | `suggest "海鲜"` |

选项: `--output <文件>` 保存 JSON

## ⚠️ 说明

抖音搜索 API 需登录，本工具在无登录环境下:
- 热榜: 直接获取 ✅
- 搜索建议: 直接获取 ✅  
- 搜索: 热榜匹配 + 建议补充 ✅

## 📄 许可

MIT
