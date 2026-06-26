#!/usr/bin/env node

/**
 * fomo-news fetcher — pulls trending GitHub repos, social posts, and breaking news
 * Usage: node fetch.mjs <category> [--limit <n>] [--json]
 * Categories: all, github, social, tech, ai, economics, politics, news
 */

const CATEGORIES = ["all", "github", "social", "tech", "ai", "economics", "politics", "news"];
const args = process.argv.slice(2);
const category = (args[0] || "all").toLowerCase();
const limitIdx = args.indexOf("--limit");
const limit = limitIdx !== -1 ? parseInt(args[limitIdx + 1], 10) : 10;
const jsonMode = args.includes("--json");

if (!CATEGORIES.includes(category)) {
  console.error(`Unknown category: ${category}`);
  console.error(`Valid categories: ${CATEGORIES.join(", ")}`);
  process.exit(1);
}

// --- GitHub Trending ---
function daysAgo(n) {
  const d = new Date();
  d.setDate(d.getDate() - n);
  return d.toISOString().split("T")[0];
}

function getGitHubQueries() {
  return [
    // Fast risers: created in last 7 days, sorted by stars (truly new & hot)
    `created:>${daysAgo(7)}&sort=stars&order=desc&per_page=20`,
    // Growing fast: created in last 30 days, already 100+ stars
    `created:>${daysAgo(30)}+stars:>100&sort=stars&order=desc&per_page=20`,
    // Breakout projects: created in last 90 days, 500+ stars
    `created:>${daysAgo(90)}+stars:>500&sort=stars&order=desc&per_page=15`,
    // AI fast risers: created in last 30 days
    `topic:ai+created:>${daysAgo(30)}+stars:>50&sort=stars&order=desc&per_page=15`,
    // LLM fast risers: created in last 30 days
    `topic:llm+created:>${daysAgo(30)}+stars:>50&sort=stars&order=desc&per_page=15`,
  ];
}

async function fetchGitHub(max) {
  const headers = { "Accept": "application/vnd.github.v3+json", "User-Agent": "fomo-news/1.0" };
  if (process.env.GITHUB_TOKEN) headers["Authorization"] = `Bearer ${process.env.GITHUB_TOKEN}`;

  const seen = new Set();
  const repos = [];

  const results = await Promise.allSettled(
    getGitHubQueries().map(async (q) => {
      const url = `https://api.github.com/search/repositories?q=${q}`;
      const res = await fetch(url, { headers });
      if (!res.ok) throw new Error(`GitHub API ${res.status}`);
      return (await res.json()).items || [];
    })
  );

  for (const r of results) {
    if (r.status !== "fulfilled") continue;
    for (const item of r.value) {
      if (seen.has(item.id)) continue;
      seen.add(item.id);
      repos.push({
        name: item.full_name,
        description: (item.description || "").slice(0, 150),
        stars: item.stargazers_count,
        forks: item.forks_count,
        language: item.language || "Unknown",
        url: item.html_url,
        topics: (item.topics || []).slice(0, 5),
        created: item.created_at,
      });
    }
  }

  repos.sort((a, b) => b.stars - a.stars);
  return repos.slice(0, max || 50);
}

// --- RSS Feed Parser (lightweight, no deps) ---
function parseRSSItems(xml, maxItems = 10) {
  const items = [];
  const itemRegex = /<item>([\s\S]*?)<\/item>/gi;
  let match;
  while ((match = itemRegex.exec(xml)) !== null && items.length < maxItems) {
    const block = match[1];
    const get = (tag) => {
      const m = block.match(new RegExp(`<${tag}[^>]*>\\s*(?:<!\\[CDATA\\[)?([\\s\\S]*?)(?:\\]\\]>)?\\s*</${tag}>`, "i"));
      return m ? m[1].trim() : "";
    };
    items.push({
      title: get("title").replace(/<[^>]*>/g, ""),
      link: get("link"),
      pubDate: get("pubDate"),
      snippet: get("description").replace(/<[^>]*>/g, "").slice(0, 300),
    });
  }
  return items;
}

async function fetchRSS(url, maxItems = 10) {
  try {
    const res = await fetch(url, {
      headers: { "User-Agent": "fomo-news/1.0" },
      signal: AbortSignal.timeout(10000),
    });
    if (!res.ok) return [];
    const xml = await res.text();
    return parseRSSItems(xml, maxItems);
  } catch {
    return [];
  }
}

// --- Social Feeds ---
const SOCIAL_SOURCES = [
  // === Influential People — Google News RSS ===
  { name: "Sam Altman", handle: "@sama", url: "https://news.google.com/rss/search?q=%22Sam+Altman%22+when:3d&hl=en-US&gl=US&ceid=US:en", category: "ai" },
  { name: "Elon Musk", handle: "@elonmusk", url: "https://news.google.com/rss/search?q=%22Elon+Musk%22+when:3d&hl=en-US&gl=US&ceid=US:en", category: "tech" },
  { name: "Donald Trump", handle: "@realDonaldTrump", url: "https://news.google.com/rss/search?q=%22Donald+Trump%22+tech+OR+AI+OR+economy+when:3d&hl=en-US&gl=US&ceid=US:en", category: "politics" },
  { name: "Jensen Huang", handle: "@nvidia", url: "https://news.google.com/rss/search?q=%22Jensen+Huang%22+when:3d&hl=en-US&gl=US&ceid=US:en", category: "tech" },
  { name: "Dario Amodei", handle: "@DarioAmodei", url: "https://news.google.com/rss/search?q=%22Dario+Amodei%22+when:3d&hl=en-US&gl=US&ceid=US:en", category: "ai" },
  { name: "Satya Nadella", handle: "@satyanadella", url: "https://news.google.com/rss/search?q=%22Satya+Nadella%22+when:3d&hl=en-US&gl=US&ceid=US:en", category: "tech" },
  { name: "Sundar Pichai", handle: "@sundarpichai", url: "https://news.google.com/rss/search?q=%22Sundar+Pichai%22+AI+when:3d&hl=en-US&gl=US&ceid=US:en", category: "tech" },
  { name: "Mark Zuckerberg", handle: "@finkd", url: "https://news.google.com/rss/search?q=%22Mark+Zuckerberg%22+AI+OR+Meta+when:3d&hl=en-US&gl=US&ceid=US:en", category: "tech" },
  // === AI Lab Leaders ===
  { name: "Demis Hassabis", handle: "@demishassabis", url: "https://news.google.com/rss/search?q=%22Demis+Hassabis%22+when:3d&hl=en-US&gl=US&ceid=US:en", category: "ai" },
  { name: "Yann LeCun", handle: "@ylecun", url: "https://news.google.com/rss/search?q=%22Yann+LeCun%22+when:3d&hl=en-US&gl=US&ceid=US:en", category: "ai" },
  { name: "Ilya Sutskever", handle: "@ilyasut", url: "https://news.google.com/rss/search?q=%22Ilya+Sutskever%22+when:3d&hl=en-US&gl=US&ceid=US:en", category: "ai" },
  { name: "Andrej Karpathy", handle: "@karpathy", url: "https://news.google.com/rss/search?q=%22Andrej+Karpathy%22+when:3d&hl=en-US&gl=US&ceid=US:en", category: "ai" },
  { name: "Arthur Mensch", handle: "@arthurmensch", url: "https://news.google.com/rss/search?q=%22Arthur+Mensch%22+OR+%22Mistral+AI%22+when:3d&hl=en-US&gl=US&ceid=US:en", category: "ai" },
  // === Tech CEOs ===
  { name: "Tim Cook", handle: "@tim_cook", url: "https://news.google.com/rss/search?q=%22Tim+Cook%22+AI+OR+Apple+when:3d&hl=en-US&gl=US&ceid=US:en", category: "tech" },
  { name: "Andy Jassy", handle: "@ajassy", url: "https://news.google.com/rss/search?q=%22Andy+Jassy%22+AI+OR+AWS+when:3d&hl=en-US&gl=US&ceid=US:en", category: "tech" },
  { name: "Lisa Su", handle: "@LisaSu", url: "https://news.google.com/rss/search?q=%22Lisa+Su%22+AMD+when:3d&hl=en-US&gl=US&ceid=US:en", category: "tech" },
  // === AI Researchers & Thought Leaders ===
  { name: "Geoffrey Hinton", handle: "@geoffreyhinton", url: "https://news.google.com/rss/search?q=%22Geoffrey+Hinton%22+when:3d&hl=en-US&gl=US&ceid=US:en", category: "ai" },
  { name: "Fei-Fei Li", handle: "@drfeifei", url: "https://news.google.com/rss/search?q=%22Fei-Fei+Li%22+AI+when:3d&hl=en-US&gl=US&ceid=US:en", category: "ai" },
  { name: "Andrew Ng", handle: "@AndrewYNg", url: "https://news.google.com/rss/search?q=%22Andrew+Ng%22+AI+when:3d&hl=en-US&gl=US&ceid=US:en", category: "ai" },
  { name: "Emad Mostaque", handle: "@EMostaque", url: "https://news.google.com/rss/search?q=%22Emad+Mostaque%22+when:3d&hl=en-US&gl=US&ceid=US:en", category: "ai" },
  // === AI Investors ===
  { name: "Marc Andreessen", handle: "@pmarca", url: "https://news.google.com/rss/search?q=%22Marc+Andreessen%22+AI+OR+tech+when:3d&hl=en-US&gl=US&ceid=US:en", category: "tech" },
  { name: "Vinod Khosla", handle: "@vkhosla", url: "https://news.google.com/rss/search?q=%22Vinod+Khosla%22+AI+OR+tech+when:3d&hl=en-US&gl=US&ceid=US:en", category: "tech" },
  // === Personal blogs & newsletters ===
  { name: "Sam Altman", handle: "@sama", url: "https://blog.samaltman.com/feed", category: "ai", isBlog: true },
  // === Company official blogs ===
  { name: "OpenAI", handle: "@OpenAI", url: "https://openai.com/blog/rss.xml", category: "ai", isBlog: true },
  { name: "Anthropic", handle: "@AnthropicAI", url: "https://www.anthropic.com/rss.xml", category: "ai", isBlog: true },
  { name: "NVIDIA Blog", handle: "@NVIDIA", url: "https://blogs.nvidia.com/feed/", category: "tech", isBlog: true },
  { name: "Google AI", handle: "@GoogleAI", url: "https://blog.google/technology/ai/rss/", category: "ai", isBlog: true },
  { name: "Microsoft AI", handle: "@Microsoft", url: "https://blogs.microsoft.com/ai/feed/", category: "ai", isBlog: true },
  { name: "Meta AI", handle: "@MetaAI", url: "https://ai.meta.com/blog/rss/", category: "ai", isBlog: true },
];

async function fetchSocial(max) {
  const results = await Promise.allSettled(
    SOCIAL_SOURCES.map(async (src) => {
      const items = await fetchRSS(src.url, 8);
      return items.map((item) => ({
        author: src.name,
        handle: src.handle,
        category: src.category,
        platform: src.isBlog ? "blog" : "rss",
        title: item.title,
        link: item.link,
        pubDate: item.pubDate,
        snippet: item.snippet,
      }));
    })
  );

  const posts = results
    .filter((r) => r.status === "fulfilled")
    .flatMap((r) => r.value);

  posts.sort((a, b) => new Date(b.pubDate) - new Date(a.pubDate));
  return posts.slice(0, max);
}

// --- News Feeds ---
const NEWS_SOURCES = [
  // Tech & AI
  { name: "TechCrunch", url: "https://techcrunch.com/feed/", category: "tech" },
  { name: "Ars Technica", url: "https://feeds.arstechnica.com/arstechnica/index", category: "tech" },
  { name: "The Verge", url: "https://www.theverge.com/rss/index.xml", category: "tech" },
  { name: "Hacker News", url: "https://hnrss.org/frontpage", category: "tech" },
  { name: "Wired", url: "https://www.wired.com/feed/rss", category: "tech" },
  // AI specific
  { name: "MIT Tech Review AI", url: "https://www.technologyreview.com/feed/", category: "ai" },
  { name: "VentureBeat AI", url: "https://venturebeat.com/feed/", category: "ai" },
  // Economics
  { name: "Reuters Business", url: "https://www.rss.app/feeds/v1.1/tsYGKBcfOkSPYTXh.xml", category: "economics" },
  { name: "CNBC", url: "https://search.cnbc.com/rs/search/combinedcms/view.xml?partnerId=wrss01&id=100003114", category: "economics" },
  { name: "MarketWatch", url: "https://www.marketwatch.com/rss/topstories", category: "economics" },
  // Politics
  { name: "Reuters World", url: "https://www.rss.app/feeds/v1.1/tsMZOAj38SjPLDn3.xml", category: "politics" },
  { name: "AP News", url: "https://rsshub.app/apnews/topics/politics", category: "politics" },
  { name: "BBC News", url: "https://feeds.bbci.co.uk/news/rss.xml", category: "politics" },
  { name: "NPR News", url: "https://feeds.npr.org/1001/rss.xml", category: "politics" },
];

async function fetchNews(categories, max) {
  const sources = categories
    ? NEWS_SOURCES.filter((s) => categories.includes(s.category))
    : NEWS_SOURCES;

  const results = await Promise.allSettled(
    sources.map(async (src) => {
      const items = await fetchRSS(src.url, 10);
      return items.map((item) => ({
        source: src.name,
        category: src.category,
        title: item.title,
        link: item.link,
        pubDate: item.pubDate,
        snippet: item.snippet,
      }));
    })
  );

  const articles = results
    .filter((r) => r.status === "fulfilled")
    .flatMap((r) => r.value);

  articles.sort((a, b) => new Date(b.pubDate) - new Date(a.pubDate));
  return articles.slice(0, max);
}

// --- Time formatting ---
function timeAgo(dateStr) {
  if (!dateStr) return "recently";
  const diff = Date.now() - new Date(dateStr).getTime();
  const mins = Math.floor(diff / 60000);
  if (mins < 1) return "just now";
  if (mins < 60) return `${mins}m ago`;
  const hrs = Math.floor(mins / 60);
  if (hrs < 24) return `${hrs}h ago`;
  const days = Math.floor(hrs / 24);
  return `${days}d ago`;
}

// --- Formatters ---
function formatGitHub(repos) {
  if (!repos.length) return "No trending repos found.\n";
  let out = "## ⭐ GitHub Trending\n\n";
  out += "| Repo | Stars | Language | Description |\n";
  out += "|------|------:|----------|-------------|\n";
  for (const r of repos) {
    out += `| [${r.name}](${r.url}) | ${r.stars.toLocaleString()} | ${r.language} | ${r.description.slice(0, 80)} |\n`;
  }
  return out + "\n";
}

function formatSocial(posts) {
  if (!posts.length) return "No social updates found.\n";
  let out = "## 💬 Social Updates\n\n";
  for (const p of posts) {
    out += `- **${p.author}** — [${p.title}](${p.link}) · ${timeAgo(p.pubDate)}\n`;
  }
  return out + "\n";
}

function formatNews(articles, label) {
  if (!articles.length) return `No ${label} news found.\n`;
  const emojis = { tech: "💻", ai: "🤖", economics: "📈", politics: "🏛️", news: "📰" };
  let out = `## ${emojis[label] || "📰"} ${label.charAt(0).toUpperCase() + label.slice(1)} News\n\n`;
  for (const a of articles) {
    out += `- **[${a.title}](${a.link})** — ${a.source} · ${timeAgo(a.pubDate)}\n`;
    if (a.snippet) out += `  ${a.snippet.slice(0, 120)}\n`;
  }
  return out + "\n";
}

// --- Main ---
async function main() {
  const sections = [];

  if (category === "all" || category === "github") {
    const repos = await fetchGitHub(limit);
    if (jsonMode) sections.push({ type: "github", data: repos });
    else sections.push(formatGitHub(repos));
  }

  if (category === "all" || category === "social") {
    const posts = await fetchSocial(limit);
    if (jsonMode) sections.push({ type: "social", data: posts });
    else sections.push(formatSocial(posts));
  }

  if (category === "all" || category === "news") {
    const articles = await fetchNews(null, limit * 3);
    if (jsonMode) sections.push({ type: "news", data: articles });
    else sections.push(formatNews(articles, "news"));
  }

  if (category === "tech") {
    const articles = await fetchNews(["tech"], limit);
    if (jsonMode) sections.push({ type: "tech", data: articles });
    else sections.push(formatNews(articles, "tech"));
  }

  if (category === "ai") {
    const articles = await fetchNews(["ai"], limit);
    if (jsonMode) sections.push({ type: "ai", data: articles });
    else sections.push(formatNews(articles, "ai"));
  }

  if (category === "economics") {
    const articles = await fetchNews(["economics"], limit);
    if (jsonMode) sections.push({ type: "economics", data: articles });
    else sections.push(formatNews(articles, "economics"));
  }

  if (category === "politics") {
    const articles = await fetchNews(["politics"], limit);
    if (jsonMode) sections.push({ type: "politics", data: articles });
    else sections.push(formatNews(articles, "politics"));
  }

  if (jsonMode) {
    console.log(JSON.stringify(sections, null, 2));
  } else {
    const banner = "\n---\n\n<sub>📰 *Powered by [fomo-news](https://github.com/alibaba-flyai/fomo-news)* — real-time news in your terminal</sub>\n";
    console.log(sections.join("\n---\n\n") + banner);
  }
}

main().catch((err) => {
  console.error(`Error: ${err.message}`);
  process.exit(1);
});
