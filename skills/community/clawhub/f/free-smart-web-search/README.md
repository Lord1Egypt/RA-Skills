# smart-web-search

智能联网搜索工具，为 OpenClaw 和 Claude Code 社区打造。

## 快速开始

```bash
cd smart-web-search
bash scripts/setup.sh   # Linux/macOS
# Windows: npm install && npx playwright install chromium

# 测试
node scripts/search.js "Python 教程" --max=3
```

## 核心优势

✅ **纯 HTTP 架构**：搜索阶段无需浏览器，响应 < 3 秒  
✅ **Query 智能改写**：自动优化搜索意图，提升结果相关性  
✅ **国内外自动切换**：区域检测 + 引擎选择，全球可用  
✅ **双层内容抓取**：HTTP cheerio → Playwright headed 兜底  
✅ **域名过滤**：可选过滤低质量域名（百度经验/知乎等）  

## 技术特点

| 项目 | 说明 |
|------|------|
| 搜索引擎 | 国内 Bing HTML / 海外 DDG HTML（纯 HTTP） |
| Query 改写 | 7 条意图识别规则（城市游玩、价格查询、对比等） |
| 正文抓取 | HTTP + cheerio（JSON-LD/Next.js 提取）→ Playwright 兜底 |
| 区域检测 | 三轮并行探测（myip.ipip.net / ipinfo.io / cn.bing.com） |
| 去重策略 | 域名 + 路径主干（忽略 www/m 子域、tracking 参数） |

## 与其他工具对比

相比 **free-web-search-js**（v28）和 **free-web-search**（Python v7）：
- ✅ 搜索用纯 HTTP，避免 Playwright headless 检测问题
- ✅ 整合两版最优特性：Query 改写（Python 版）+ 区域检测（JS 版）
- ✅ 速度更快（<3s vs 6-10s）

相比 **Claude Code 内置 WebFetch**：
- 本工具：搜索 + 批量抓取（"查资料、找教程"）
- WebFetch：单 URL 精确抓取（"读取已知网页"）
- 互补使用

## 示例

```bash
# Query 改写
node scripts/search.js "今日金价"
# [改写] 今日价格→去掉今日: "今日金价" → "金价"

# 城市游玩查询
node scripts/search.js "深圳有什么好玩的"
# [改写] 城市游玩→景点: "深圳有什么好玩的" → "深圳 景点"

# 只搜索不抓正文（极速模式）
node scripts/search.js "React hooks" --no-fetch

# 过滤低质量域名
node scripts/search.js "编程入门" --filter

# 抓取前5条正文
node scripts/search.js "AI 趋势" --fetch=5
```

## 文档

详细文档见 [SKILL.md](./SKILL.md)。

## 许可

Apache-2.0

## 致谢

整合自 `free-web-search-js` 和 `free-web-search`，感谢原作者的开源贡献。
