# OpenClaw 集成指南

## 问题说明

**为什么脚本使用演示数据？**

Node.js 脚本无法直接调用 OpenClaw 的 `web_search` 工具。`web_search` 是 OpenClaw 的内部工具，只能在 OpenClaw 主流程中使用。

## 解决方案

**由 OpenClaw 主流程负责搜索，然后调用脚本生成内容。**

### OpenClaw 主流程调用示例

```javascript
// 在 OpenClaw 主流程中（如直接对话或技能调用）

// 1. 使用 web_search 工具搜索真实资讯
const searchResults1 = await web_search({
  query: "AI 大模型 24 小时 新闻 2026 年 3 月",
  count: 10
});

const searchResults2 = await web_search({
  query: "OpenAI Anthropic Claude new release March 2026",
  count: 8
});

// 2. 合并并去重
const allResults = [...searchResults1.results, ...searchResults2.results];
const seen = new Set();
const uniqueResults = allResults.filter(item => {
  if (!item.url || seen.has(item.url)) return false;
  seen.add(item.url);
  return true;
});

// 3. 转换为脚本接受的格式
const newsData = uniqueResults.slice(0, 10).map((item, i) => ({
  title: item.title || `AI 资讯 ${i + 1}`,
  content: item.snippet || item.description || '暂无详细描述',
  url: item.url || '#',
  time: `${i * 3 + 2} 小时前`, // 根据实际时间计算
  source: extractDomain(item.url) || '网络来源'
}));

function extractDomain(url) {
  try {
    return new URL(url).hostname.replace('www.', '').split('.')[0];
  } catch (e) {
    return '网络来源';
  }
}

// 4. 调用生成脚本
const { execSync } = require('child_process');
const path = require('path');

const SKILL_DIR = '/Users/javastarboy/.openclaw/workspace/skills/ai-news-xiaohongshu';
const jsonStr = JSON.stringify(newsData);

execSync(`node "${path.join(SKILL_DIR, 'scripts/create-xiaohongshu-content.js')}" --news-json '${jsonStr}'`, {
  encoding: 'utf-8',
  stdio: 'inherit',
  cwd: SKILL_DIR
});
```

### 简化版（OpenClaw 直接处理）

如果不想调用脚本，也可以在 OpenClaw 主流程中直接生成所有内容：

```javascript
// OpenClaw 主流程中

// 1. 搜索
const results = await web_search({ query: "AI 大模型 24 小时 新闻", count: 10 });

// 2. 生成文案（直接在 OpenClaw 中）
const copy = generateXiaohongshuCopy(results.results);

// 3. 生成 HTML（直接在 OpenClaw 中）
const html = generateHTML(results.results);

// 4. 输出到文件
const fs = require('fs');
const path = require('path');
const outputDir = `/Users/javastarboy/.openclaw/workspace/skills/ai-news-xiaohongshu/output/${getDateStr()}`;
fs.mkdirSync(outputDir, { recursive: true });
fs.writeFileSync(path.join(outputDir, 'xiaohongshu-copy.md'), copy);
fs.writeFileSync(path.join(outputDir, 'cover.html'), html);
```

## 脚本参数说明

### create-xiaohongshu-content.js

**接收真实数据：**
```bash
node scripts/create-xiaohongshu-content.js --news-json '[{"title":"...", "url":"...", "content":"...", "time":"2 小时前", "source":"OpenAI"}]'
```

**使用演示数据：**
```bash
node scripts/create-xiaohongshu-content.js
# 或
node scripts/create-xiaohongshu-content.js --use-demo
```

### run-full-flow.js

使用演示数据运行完整流程：
```bash
node scripts/run-full-flow.js
```

## 数据格式

脚本接受的新闻数据格式：

```json
[
  {
    "title": "新闻标题",
    "content": "新闻摘要/描述",
    "url": "https://example.com/news",
    "time": "2 小时前",
    "source": "来源名称"
  }
]
```

## 输出文件

生成到 `output/日期/` 目录：

- `xiaohongshu-copy.md` - 小红书文案
- `cover.html` - HTML 封面（3:4 比例，可滑动）
- `news-summary.md` - 资讯汇总表格
- `sources.md` - 原始来源链接

## 最佳实践

1. **定时任务**：使用 OpenClaw cron 每天定时执行
2. **真实数据**：始终使用 `web_search` 搜索真实数据
3. **数据验证**：检查搜索结果的时间，确保是 24 小时内
4. **错误处理**：搜索失败时使用演示数据降级

## 示例：OpenClaw Cron 配置

```json
{
  "name": "每日 AI 资讯小红书",
  "schedule": {
    "kind": "cron",
    "expr": "0 9 * * *",
    "tz": "Asia/Shanghai"
  },
  "payload": {
    "kind": "agentTurn",
    "message": "请使用 ai-news-xiaohongshu 技能生成今日 AI 资讯，使用真实搜索数据"
  },
  "sessionTarget": "isolated"
}
```
