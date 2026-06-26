# FetchNews Workflow

新闻抓取和整理主流程。

## 工作流程

### 步骤 1：读取配置

读取配置文件 `~/.daily-news-brief/config.json`：

```typescript
import { readFileSync } from 'fs';
import { join } from 'path';

const configPath = join(process.env.HOME, '.daily-news-brief/config.json');
const config = JSON.parse(readFileSync(configPath, 'utf-8'));
```

### 步骤 2：抓取新闻

对每个配置的新闻源进行抓取：

```typescript
// NewsFetcher.ts

async function fetchFromRSS(url: string) {
  const response = await fetch(url);
  const xml = await response.text();
  const parsed = parseRSS(xml); // 使用 rss-parser 库

  return parsed.items.map(item => ({
    title: item.title,
    link: item.link,
    pubDate: new Date(item.pubDate),
    description: item.description,
    source: url,
    category: '' // 待分类
  }));
}

async function fetchFromWeb(url: string) {
  const response = await fetch(url);
  const html = await response.text();
  const $ = cheerio.load(html);

  const articles = [];

  // 根据不同网站的 DOM 结构解析
  $('.news-item').each((i, elem) => {
    articles.push({
      title: $(elem).find('.title').text(),
      link: $(elem).find('a').attr('href'),
      pubDate: new Date($(elem).find('.date').text()),
      views: parseInt($(elem).find('.views').text()) || 0,
      source: url,
      category: ''
    });
  });

  return articles;
}
```

### 步骤 3：新闻去重

根据标题和链接去重：

```typescript
function deduplicateNews(newsList: NewsItem[]) {
  const seen = new Set();
  return newsList.filter(item => {
    const key = `${item.title}-${item.link}`;
    if (seen.has(key)) return false;
    seen.add(key);
    return true;
  });
}
```

### 步骤 4：新闻分类

使用关键词匹配和 NLP 分类：

```typescript
// NewsClassifier.ts

const categoryKeywords = {
  '科技': ['科技', '技术', '互联网', '5G', '芯片', '手机', '电脑', '软件'],
  '财经': ['财经', '经济', '股市', '投资', '融资', 'IPO', '金融'],
  'AI': ['人工智能', 'AI', '大模型', 'GPT', '深度学习', '机器学习', '神经网络'],
  '智能体': ['智能体', 'Agent', 'AI Agent', '自主代理', '智能代理']
};

function classifyNews(item: NewsItem) {
  const scores = {};

  for (const [category, keywords] of Object.entries(categoryKeywords)) {
    let score = 0;
    for (const keyword of keywords) {
      if (item.title.includes(keyword)) score += 2;
      if (item.description && item.description.includes(keyword)) score += 1;
    }
    scores[category] = score;
  }

  // 返回得分最高的分类
  return Object.entries(scores).sort((a, b) => b[1] - a[1])[0][0];
}
```

### 步骤 5：热度排序

按发布时间和阅读量综合排序：

```typescript
function sortNewsByPopularity(newsList: NewsItem[]) {
  return newsList.sort((a, b) => {
    // 时间权重：最新 24 小时内的新闻优先
    const now = new Date();
    const hoursSinceA = (now.getTime() - a.pubDate.getTime()) / (1000 * 60 * 60);
    const hoursSinceB = (now.getTime() - b.pubDate.getTime()) / (1000 * 60 * 60);

    const timeScoreA = hoursSinceA < 24 ? 100 : 100 / hoursSinceA;
    const timeScoreB = hoursSinceB < 24 ? 100 : 100 / hoursSinceB;

    // 阅读量权重
    const viewScoreA = a.views || 0;
    const viewScoreB = b.views || 0;

    // 综合得分
    const scoreA = timeScoreA * 0.6 + viewScoreA * 0.4;
    const scoreB = timeScoreB * 0.6 + viewScoreB * 0.4;

    return scoreB - scoreA;
  });
}
```

### 步骤 6：筛选正规媒体

根据域名白名单筛选：

```typescript
const trustedDomains = [
  '36kr.com', 'huxiu.com', 'caixin.com', 'thepaper.cn',
  'jiqizhixin.com', 'xinzhiyuan.ai', 'infoq.cn'
];

function filterTrustedMedia(newsList: NewsItem[]) {
  return newsList.filter(item => {
    const domain = new URL(item.link).hostname;
    return trustedDomains.some(trusted => domain.includes(trusted));
  });
}
```

### 步骤 7：限制每类新闻数量

```typescript
function limitNewsPerCategory(newsList: NewsItem[], max: number) {
  const categorized = {};
  for (const item of newsList) {
    if (!categorized[item.category]) categorized[item.category] = [];
    if (categorized[item.category].length < max) {
      categorized[item.category].push(item);
    }
  }
  return categorized;
}
```

### 步骤 8：生成 Markdown 文档

```typescript
// MarkdownGenerator.ts

function generateMarkdown(categorizedNews: Record<string, NewsItem[]>) {
  const date = new Date().toLocaleDateString('zh-CN', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit'
  });

  let md = `# ${date} 每日新闻汇总\n\n`;
  md += `> 生成时间：${new Date().toLocaleString('zh-CN')}\n\n`;
  md += `---\n\n`;

  for (const [category, items] of Object.entries(categorizedNews)) {
    if (items.length === 0) continue;

    md += `## ${category}\n\n`;
    md += `共 ${items.length} 条新闻\n\n`;

    for (const item of items) {
      md += `### ${item.title}\n\n`;
      if (item.description) {
        md += `${item.description}\n\n`;
      }
      md += `- **来源**：${item.source}\n`;
      md += `- **发布时间**：${item.pubDate.toLocaleString('zh-CN')}\n`;
      if (item.views) md += `- **阅读量**：${item.views}\n`;
      md += `- **原文链接**：[${item.link}](${item.link})\n\n`;
      md += `---\n\n`;
    }
  }

  return md;
}
```

### 步骤 9：保存本地文档

```typescript
import { mkdirSync, writeFileSync } from 'fs';

function saveLocalMarkdown(md: string, config: Config) {
  const date = new Date().toISOString().split('T')[0];
  const dir = config.localDocPath.replace('~', process.env.HOME);
  const filePath = join(dir, `${date}.md`);

  mkdirSync(dir, { recursive: true });
  writeFileSync(filePath, md, 'utf-8');

  console.log(`✅ 本地文档已保存：${filePath}`);
}
```

### 步骤 10：发送到聊天窗口

将整理好的新闻发送给用户：

```text
📰 2026-03-17 新闻简报

【科技】10 条（摘要显示 5 条）
- AI 芯片新进展（来源：36氪）
- 云计算价格战（来源：虎嗅网）
- …

【AI】12 条（摘要显示 5 条）
- 多模态模型发布（来源：机器之心）
- …

本地文档：~/daily-news-brief/每日新闻/2026-03-17.md
```

### 步骤 11：错误处理和日志

```typescript
async function runFetchNews() {
  try {
    console.log(`[${new Date().toISOString()}] 开始抓取新闻`);

    // 执行上述步骤...

    console.log(`[${new Date().toISOString()}] 新闻抓取完成`);
  } catch (error) {
    console.error(`[${new Date().toISOString()}] 错误：`, error);

    // 保存错误日志
    const logDir = join(process.env.HOME, '.daily-news-brief/logs');
    const logFile = join(logDir, 'error.log');
    mkdirSync(logDir, { recursive: true });
    appendFileSync(logFile, `[${new Date().toISOString()}] ${error}\n`);
  }
}
```

## 命令行参数

```bash
# 手动执行
node tools/FetchNews.ts

# 测试模式（只抓取少量新闻）
node tools/FetchNews.ts --test

# 指定日期
node tools/FetchNews.ts --date 2026-03-17

# 仅抓取指定分类
node tools/FetchNews.ts --category AI

# 推送到 OpenClaw 通道
node tools/FetchNews.ts --push

# 禁止推送（仅本地输出）
node tools/FetchNews.ts --no-push
```

说明：若 OpenClaw 没有默认目标，可在 `~/.daily-news-brief/config.json` 配置 `push.targets`。

## 依赖库

```json
{
  "dependencies": {
    "rss-parser": "^3.13.0",
    "cheerio": "^1.0.0-rc.12",
    "date-fns": "^3.0.0"
  }
}
```

## 完整代码结构

```text
tools/
├── FetchNews.ts           # 主入口文件
├── Configure.ts           # 配置管理 CLI
├── NewsFetcher.ts         # 新闻抓取工具
├── NewsClassifier.ts      # 新闻分类工具
├── MarkdownGenerator.ts   # MD 文档生成工具
└── types.ts              # TypeScript 类型定义
```
