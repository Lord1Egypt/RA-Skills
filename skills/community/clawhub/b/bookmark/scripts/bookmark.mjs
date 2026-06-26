#!/usr/bin/env node

const DEFAULT_BASE_URL = process.env.BOOKMARK_BASE_URL?.trim() || "https://shuqianlan.com";
const DEFAULT_LIMIT = 6;
const DEFAULT_PAGE = 1;
const ITEM_DESC_LIMIT = 40;
const MARKDOWN_HARD_BREAK = "  \n";

function printUsage() {
  console.log(`Usage:
  node scripts/bookmark.mjs search "<query>" [--limit N] [--base-url URL]
  node scripts/bookmark.mjs latest [--limit N] [--page N] [--base-url URL]
  node scripts/bookmark.mjs categories [--limit N] [--base-url URL]
  node scripts/bookmark.mjs articles "<category>" [--limit N] [--page N] [--base-url URL]
  node scripts/bookmark.mjs links "<category>" [--limit N] [--base-url URL]`);
}

function fail(message) {
  console.error(message);
  process.exitCode = 1;
}

function readString(value) {
  return typeof value === "string" && value.trim() ? value.trim() : undefined;
}

function readNumber(value) {
  if (typeof value === "number" && Number.isFinite(value)) {
    return value;
  }
  if (typeof value === "string" && value.trim() && /^-?\d+$/u.test(value.trim())) {
    return Number(value.trim());
  }
  return undefined;
}

function readArticleCount(value) {
  if (value === null) {
    return null;
  }
  if (typeof value !== "number" || !Number.isFinite(value)) {
    return undefined;
  }
  return value;
}

function normalizeSearchTerm(value) {
  return value.normalize("NFKC").trim().toLowerCase();
}

function normalizeCategoryKey(value) {
  return normalizeSearchTerm(value).replace(/\s+/g, "");
}

function encodeKeyword(keyword) {
  return encodeURIComponent(keyword.trim().toLowerCase()).replace(/%/g, "_");
}

function decodeHtmlText(value) {
  return value
    .replace(/&nbsp;/giu, " ")
    .replace(/&amp;/giu, "&")
    .replace(/&lt;/giu, "<")
    .replace(/&gt;/giu, ">")
    .replace(/&quot;/giu, "\"")
    .replace(/&#39;/giu, "'");
}

function stripHtml(value) {
  return decodeHtmlText(value.replace(/<[^>]+>/gu, " ")).replace(/\s+/g, " ").trim();
}

function typePriority(type) {
  if (type.includes("文章")) {
    return 3;
  }
  if (type.includes("二级分类")) {
    return 2;
  }
  if (type.includes("一级分类")) {
    return 1;
  }
  return 0;
}

function isArticleItem(item) {
  return item.type.includes("文章");
}

function isCategoryItem(item) {
  return item.type.includes("分类");
}

function toBookmarkCategory(item) {
  if (!isCategoryItem(item)) {
    return undefined;
  }
  return {
    name: item.title,
    url: item.url,
    articleCount: item.articleCount ?? undefined,
  };
}

function dedupeCategories(categories) {
  const merged = new Map();
  for (const category of categories) {
    const existing = merged.get(category.url);
    if (!existing) {
      merged.set(category.url, category);
      continue;
    }
    merged.set(category.url, {
      ...category,
      articleCount: existing.articleCount ?? category.articleCount,
    });
  }
  return Array.from(merged.values());
}

function tokenizeSearchQuery(query) {
  const normalized = normalizeSearchTerm(query);
  if (!normalized) {
    return [];
  }

  const tokens = normalized.match(/[a-z0-9]+|[\u3400-\u9fff]+/giu) ?? [];
  const seen = new Set();
  const result = [];

  for (const token of tokens) {
    const normalizedToken = normalizeSearchTerm(token);
    if (!normalizedToken || seen.has(normalizedToken)) {
      continue;
    }
    seen.add(normalizedToken);
    result.push(normalizedToken);
  }

  return result;
}

function mergeTokenSearchResults(termResults) {
  const merged = new Map();
  let rank = 0;

  for (const termResult of termResults) {
    for (const item of termResult.items) {
      const existing = merged.get(item.url);
      if (existing) {
        existing.matchedTerms.add(termResult.term);
        continue;
      }

      merged.set(item.url, {
        ...item,
        matchedTerms: new Set([termResult.term]),
        firstRank: rank,
      });
      rank += 1;
    }
  }

  const rankedItems = Array.from(merged.values()).sort((left, right) => {
    const matchedDelta = right.matchedTerms.size - left.matchedTerms.size;
    if (matchedDelta !== 0) {
      return matchedDelta;
    }

    const typeDelta = typePriority(right.type) - typePriority(left.type);
    if (typeDelta !== 0) {
      return typeDelta;
    }

    return left.firstRank - right.firstRank;
  });

  const maxMatches = rankedItems[0]?.matchedTerms.size ?? 0;
  const filteredItems =
    maxMatches > 1
      ? rankedItems.filter((item) => item.matchedTerms.size === maxMatches)
      : rankedItems;

  return filteredItems.map(({ matchedTerms: _matchedTerms, firstRank: _firstRank, ...item }) => item);
}

function summarizeItemDesc(item) {
  const normalizedDesc = item.desc?.replace(/\s+/g, " ").trim();
  if (!normalizedDesc) {
    return undefined;
  }
  if (normalizeSearchTerm(normalizedDesc) === normalizeSearchTerm(item.title)) {
    return undefined;
  }
  return normalizedDesc.length > ITEM_DESC_LIMIT
    ? `${normalizedDesc.slice(0, ITEM_DESC_LIMIT).trimEnd()}...`
    : normalizedDesc;
}

function summarizeItemMeta(item) {
  const parts = [];
  if (item.firstCategory && item.secondCategory) {
    parts.push(`${item.firstCategory} > ${item.secondCategory}`);
  } else if (item.firstCategory) {
    parts.push(item.firstCategory);
  } else if (item.secondCategory) {
    parts.push(item.secondCategory);
  }

  if (item.updatedAt) {
    parts.push(`更新：${item.updatedAt}`);
  }

  return parts.length > 0 ? parts.join(" · ") : undefined;
}

function escapeMarkdownLinkLabel(text) {
  return text.replace(/\\/g, "\\\\").replace(/\[/g, "\\[").replace(/\]/g, "\\]");
}

function formatIndexedLine(index, content, numbered) {
  return numbered ? `${index + 1}、${content}` : content;
}

function renderArticleBlocks(items, limit, includeMeta = true) {
  const visibleItems = items.slice(0, limit);
  const numbered = visibleItems.length > 1;

  return visibleItems.map((item, index) => {
    const lines = [
      formatIndexedLine(index, `[${escapeMarkdownLinkLabel(item.title)}](${item.url})`, numbered),
    ];
    const desc = summarizeItemDesc(item);
    if (desc) {
      lines.push(`简介：${desc}`);
    }
    if (includeMeta) {
      const meta = summarizeItemMeta(item);
      if (meta) {
        lines.push(meta);
      }
    }
    return lines.join(MARKDOWN_HARD_BREAK);
  });
}

function renderArticleListReply({ intro, items, limit, browseLink, includeMeta = true }) {
  const parts = [intro, ...renderArticleBlocks(items, limit, includeMeta)];
  if (browseLink) {
    parts.push(`[${escapeMarkdownLinkLabel(browseLink.label)}](${browseLink.url})`);
  }
  return parts.join("\n\n");
}

function renderSearchReply(query, items, limit) {
  const intro =
    items.length > limit
      ? `找到 ${items.length} 条“${query}”相关结果，先看前 ${limit} 条：`
      : `找到 ${items.length} 条“${query}”相关结果：`;

  return renderArticleListReply({ intro, items, limit });
}

function renderLatestReply(page, limit) {
  const total = page.total ?? page.items.length;
  const intro = total > limit ? `最近更新，先看前 ${limit} 篇：` : "最近更新：";

  return renderArticleListReply({
    intro,
    items: page.items,
    limit,
    includeMeta: false,
    browseLink: page.browseUrl
      ? {
          label: "查看全部文章",
          url: page.browseUrl,
        }
      : undefined,
  });
}

function renderCategoryListReply(categories, limit) {
  const visibleCategories = categories.slice(0, limit);
  const intro = categories.length > limit ? `一级分类，先看前 ${limit} 个：` : "一级分类：";
  const numbered = visibleCategories.length > 1;

  const blocks = visibleCategories.map((category, index) => {
    const suffix = typeof category.articleCount === "number" ? `（${category.articleCount} 篇）` : "";
    return formatIndexedLine(
      index,
      `[${escapeMarkdownLinkLabel(category.name)}](${category.url})${suffix}`,
      numbered,
    );
  });

  return [
    intro,
    ...blocks,
    "继续看某个分类，直接运行 articles 或 links 子命令。",
  ].join("\n\n");
}

function renderCategoryArticlesReply(category, page, limit) {
  const total = page.total ?? page.items.length;
  const intro =
    total > limit
      ? `“${category.name}”文章，先看前 ${limit} 篇：`
      : `“${category.name}”文章：`;

  return renderArticleListReply({
    intro,
    items: page.items,
    limit,
    includeMeta: false,
    browseLink: {
      label: `打开“${category.name}”分类页`,
      url: page.browseUrl ?? category.url,
    },
  });
}

function renderCategoryLinksReply(category, links, limit) {
  const visibleLinks = links.slice(0, limit);
  const intro =
    links.length > limit
      ? `“${category.name}”常用链接，先看前 ${limit} 个：`
      : `“${category.name}”常用链接：`;
  const numbered = visibleLinks.length > 1;

  const blocks = visibleLinks.map((link, index) =>
    formatIndexedLine(index, `[${escapeMarkdownLinkLabel(link.name)}](${link.url})`, numbered),
  );

  return [
    intro,
    ...blocks,
    `[${escapeMarkdownLinkLabel(`打开“${category.name}”分类页`)}](${category.url})`,
  ].join("\n\n");
}

class ShuqianlanClient {
  constructor(baseUrl) {
    this.baseUrl = new URL(baseUrl);
  }

  async fetchJson(url) {
    const response = await fetch(url, {
      method: "GET",
      headers: {
        Accept: "application/json",
      },
    });

    if (response.status === 404) {
      return undefined;
    }
    if (!response.ok) {
      throw new Error(`request failed: ${response.status}`);
    }
    return response.json();
  }

  async fetchText(url) {
    const response = await fetch(url, {
      method: "GET",
      headers: {
        Accept: "text/html,application/xhtml+xml",
      },
    });

    if (response.status === 404) {
      return "";
    }
    if (!response.ok) {
      throw new Error(`request failed: ${response.status}`);
    }
    return response.text();
  }

  parseSearchItem(item) {
    const title = readString(item.title);
    const rawUrl = readString(item.url);
    if (!title || !rawUrl) {
      return [];
    }

    return [
      {
        type: readString(item.type) ?? "结果",
        title,
        desc: readString(item.desc),
        url: new URL(rawUrl, this.baseUrl).toString(),
        articleCount: readArticleCount(item.articleCount),
      },
    ];
  }

  parseArticleItem(article) {
    const title = readString(article.title);
    const rawUrl = readString(article.articleHtmlUrl);
    if (!title || !rawUrl) {
      return [];
    }

    return [
      {
        type: "文章",
        title,
        desc: readString(article.summary),
        url: new URL(rawUrl, this.baseUrl).toString(),
        firstCategory: readString(article.firstCategory),
        secondCategory: readString(article.secondCategory),
        updatedAt: readString(article.updateTime),
      },
    ];
  }

  parseCategoryPage(url) {
    const pathname = new URL(url, this.baseUrl).pathname;
    const match = /^\/static-article\/cate-page\/(first|second)\/([^/.]+)\.html$/u.exec(pathname);
    if (!match?.[1] || !match[2]) {
      return undefined;
    }

    return {
      kind: match[1],
      id: match[2],
    };
  }

  async searchKeyword(keyword) {
    const normalized = keyword.normalize("NFKC").trim().toLowerCase();
    if (!normalized) {
      return [];
    }

    const requestUrl = new URL(
      `/static-article/searchKeywords/${encodeKeyword(normalized)}.json`,
      this.baseUrl,
    );
    const payload = await this.fetchJson(requestUrl);
    if (payload?.code !== 200 || !Array.isArray(payload.data)) {
      return [];
    }
    return payload.data.flatMap((item) => this.parseSearchItem(item));
  }

  async listLatestArticles(page = DEFAULT_PAGE) {
    const safePage = page > 0 ? page : DEFAULT_PAGE;
    const requestUrl = new URL(`/static-article/page/page_${safePage}.json`, this.baseUrl);
    const payload = await this.fetchJson(requestUrl);
    if (!payload?.data || !Array.isArray(payload.data.articles)) {
      return {
        items: [],
        page: safePage,
        browseUrl: new URL(`/static-article/page/page_${safePage}.html`, this.baseUrl).toString(),
      };
    }

    return {
      items: payload.data.articles.flatMap((article) => this.parseArticleItem(article)),
      page: readNumber(payload.data.pageInfo?.page) ?? safePage,
      total: readNumber(payload.data.pageInfo?.totalCount),
      totalPages: readNumber(payload.data.pageInfo?.totalPages),
      browseUrl: new URL(`/static-article/page/page_${safePage}.html`, this.baseUrl).toString(),
    };
  }

  async listTopCategories() {
    const html = await this.fetchText(new URL("/static-article/index.html", this.baseUrl));
    const categories = [];
    const categoryPattern =
      /<a href="([^"]+)"[^>]*data-type="一级分类"[^>]*data-title="([^"]+)"[^>]*>([\s\S]*?)<\/a>/giu;

    for (const match of html.matchAll(categoryPattern)) {
      const rawUrl = readString(match[1]);
      const rawName = readString(match[2]) ?? stripHtml(match[3] ?? "");
      if (!rawUrl || !rawName) {
        continue;
      }

      const countMatch = /(\d+)\s*篇/iu.exec(match[3] ?? "");
      categories.push({
        name: decodeHtmlText(rawName),
        url: new URL(rawUrl, this.baseUrl).toString(),
        articleCount: countMatch ? Number(countMatch[1]) : undefined,
      });
    }

    return categories;
  }

  async listCategoryArticles(category, page = DEFAULT_PAGE) {
    const safePage = page > 0 ? page : DEFAULT_PAGE;
    const descriptor = this.parseCategoryPage(category.url);
    if (!descriptor) {
      return {
        items: [],
        page: safePage,
        browseUrl: category.url,
      };
    }

    const requestUrl = new URL(
      `/static-article/cate-page/${descriptor.kind}/${descriptor.id}/page_${safePage}.json`,
      this.baseUrl,
    );
    const payload = await this.fetchJson(requestUrl);
    if (!payload?.data || !Array.isArray(payload.data.articles)) {
      return {
        items: [],
        page: safePage,
        browseUrl: category.url,
      };
    }

    return {
      items: payload.data.articles.flatMap((article) => this.parseArticleItem(article)),
      page: readNumber(payload.data.pageInfo?.page) ?? safePage,
      total: readNumber(payload.data.pageInfo?.totalCount),
      totalPages: readNumber(payload.data.pageInfo?.totalPages),
      browseUrl: category.url,
    };
  }

  async listCategoryLinks(category) {
    const html = await this.fetchText(new URL(category.url, this.baseUrl));
    const containerMatch =
      /<div class="ml-auto flex items-center gap-3 flex-wrap justify-end text-right">([\s\S]*?)<\/div>/iu
        .exec(html);
    if (!containerMatch?.[1]) {
      return [];
    }

    const links = [];
    const linkPattern = /<a href="([^"]+)"[^>]*>([\s\S]*?)<\/a>/giu;
    for (const match of containerMatch[1].matchAll(linkPattern)) {
      const rawUrl = readString(match[1]);
      const name = stripHtml(match[2] ?? "");
      if (!rawUrl || !name) {
        continue;
      }
      links.push({
        name,
        url: new URL(rawUrl, this.baseUrl).toString(),
      });
    }

    return links;
  }
}

async function searchArticles(client, query) {
  const normalizedQuery = normalizeSearchTerm(query);
  const exactMatches = (await client.searchKeyword(normalizedQuery)).filter(isArticleItem);
  if (exactMatches.length > 0) {
    return exactMatches;
  }

  const tokens = tokenizeSearchQuery(query).filter((token) => token !== normalizedQuery);
  if (tokens.length === 0) {
    return [];
  }

  const termResults = await Promise.all(
    tokens.map(async (term) => ({
      term,
      items: (await client.searchKeyword(term)).filter(isArticleItem),
    })),
  );

  return mergeTokenSearchResults(termResults);
}

async function findCategory(client, query) {
  const normalizedQuery = normalizeCategoryKey(query);
  if (!normalizedQuery) {
    return undefined;
  }

  const [topCategories, matchedCategories] = await Promise.all([
    client.listTopCategories(),
    client.searchKeyword(normalizeSearchTerm(query)).then((items) =>
      items.flatMap((item) => {
        const category = toBookmarkCategory(item);
        return category ? [category] : [];
      }),
    ),
  ]);

  const categories = dedupeCategories([...matchedCategories, ...topCategories]);
  const exactMatch = categories.find((category) => normalizeCategoryKey(category.name) === normalizedQuery);
  if (exactMatch) {
    return exactMatch;
  }

  const partialMatches = categories.filter((category) => {
    const normalizedCategory = normalizeCategoryKey(category.name);
    return normalizedCategory.includes(normalizedQuery) || normalizedQuery.includes(normalizedCategory);
  });

  if (partialMatches.length === 0) {
    return undefined;
  }

  return partialMatches.sort((left, right) => left.name.length - right.name.length)[0];
}

function parseArgs(argv) {
  const args = [...argv];
  const command = args.shift();
  const options = {
    command,
    target: undefined,
    limit: DEFAULT_LIMIT,
    page: DEFAULT_PAGE,
    baseUrl: DEFAULT_BASE_URL,
  };

  while (args.length > 0) {
    const current = args.shift();
    if (!current) {
      continue;
    }

    if (current === "--limit") {
      const next = args.shift();
      const limit = readNumber(next);
      if (!limit || limit < 1 || limit > 50) {
        throw new Error("`--limit` must be an integer between 1 and 50.");
      }
      options.limit = limit;
      continue;
    }

    if (current === "--page") {
      const next = args.shift();
      const page = readNumber(next);
      if (!page || page < 1 || page > 999) {
        throw new Error("`--page` must be an integer between 1 and 999.");
      }
      options.page = page;
      continue;
    }

    if (current === "--base-url") {
      const next = args.shift();
      if (!readString(next)) {
        throw new Error("`--base-url` requires a URL.");
      }
      options.baseUrl = next.trim();
      continue;
    }

    if (current.startsWith("--")) {
      throw new Error(`Unknown option: ${current}`);
    }

    if (!options.target) {
      options.target = current;
      continue;
    }

    options.target = `${options.target} ${current}`;
  }

  return options;
}

async function main() {
  let options;
  try {
    options = parseArgs(process.argv.slice(2));
  } catch (error) {
    fail(error instanceof Error ? error.message : "Invalid arguments.");
    printUsage();
    return;
  }

  if (!options.command || options.command === "help" || options.command === "--help") {
    printUsage();
    return;
  }

  const client = new ShuqianlanClient(options.baseUrl);

  try {
    switch (options.command) {
      case "search": {
        if (!readString(options.target)) {
          throw new Error("Search requires a query.");
        }
        const items = await searchArticles(client, options.target);
        if (items.length === 0) {
          console.log(
            `书签篮里还没找到和“${options.target}”相关的书签。你可以换更短的关键词再试，比如“python”“cesium”或“教程”。`,
          );
          return;
        }
        console.log(renderSearchReply(options.target, items, options.limit));
        return;
      }
      case "latest": {
        const page = await client.listLatestArticles(options.page);
        if (page.items.length === 0) {
          console.log("书签篮暂时还没有可展示的最新文章。");
          return;
        }
        console.log(renderLatestReply(page, options.limit));
        return;
      }
      case "categories": {
        const categories = await client.listTopCategories();
        if (categories.length === 0) {
          console.log("书签篮暂时还没有可展示的分类。");
          return;
        }
        console.log(renderCategoryListReply(categories, options.limit));
        return;
      }
      case "articles": {
        if (!readString(options.target)) {
          throw new Error("Category articles require a category name.");
        }
        const category = await findCategory(client, options.target);
        if (!category) {
          console.log(`书签篮里暂时没找到“${options.target}”这个分类。你可以先让我列出分类列表，再继续看某个分类的文章或常用链接。`);
          return;
        }
        const page = await client.listCategoryArticles(category, options.page);
        if (page.items.length === 0) {
          console.log(`书签篮里还没找到和“${category.name}”相关的书签。你可以换更短的关键词再试，比如“python”“cesium”或“教程”。`);
          return;
        }
        console.log(renderCategoryArticlesReply(category, page, options.limit));
        return;
      }
      case "links": {
        if (!readString(options.target)) {
          throw new Error("Category links require a category name.");
        }
        const category = await findCategory(client, options.target);
        if (!category) {
          console.log(`书签篮里暂时没找到“${options.target}”这个分类。你可以先让我列出分类列表，再继续看某个分类的文章或常用链接。`);
          return;
        }
        const links = await client.listCategoryLinks(category);
        if (links.length === 0) {
          console.log(`“${category.name}”分类暂时没有配置常用链接。`);
          return;
        }
        console.log(renderCategoryLinksReply(category, links, options.limit));
        return;
      }
      default:
        throw new Error(`Unknown command: ${options.command}`);
    }
  } catch (error) {
    fail(error instanceof Error ? error.message : "Bookmark request failed.");
  }
}

await main();
