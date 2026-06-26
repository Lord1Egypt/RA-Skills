import Parser from 'rss-parser';
import * as cheerio from 'cheerio';
import type { NewsItem, NewsSource } from './types';

const parser = new Parser();

export class NewsFetcher {
  private sources: NewsSource[];

  constructor(sources: NewsSource[]) {
    this.sources = sources;
  }

  async fetchAll(): Promise<NewsItem[]> {
    const allNews: NewsItem[] = [];

    for (const source of this.sources) {
      try {
        console.log(`正在抓取：${source.name}...`);
        const news = await this.fetchFromSource(source);
        allNews.push(...news);
      } catch (error) {
        console.error(`抓取 ${source.name} 失败：`, error);
      }
    }

    return this.deduplicate(allNews);
  }

  private async fetchFromSource(source: NewsSource): Promise<NewsItem[]> {
    if (source.type === 'rss') {
      return this.fetchFromRSS(source);
    } else {
      return this.fetchFromWeb(source);
    }
  }

  private async fetchFromRSS(source: NewsSource): Promise<NewsItem[]> {
    const feed = await parser.parseURL(source.url);

    return feed.items.map(item => ({
      title: item.title || '',
      link: item.link || '',
      pubDate: new Date(item.pubDate || Date.now()),
      description: item.contentSnippet || item.content,
      source: source.name,
      category: source.category,
    }));
  }

  private async fetchFromWeb(source: NewsSource): Promise<NewsItem[]> {
    const response = await fetch(source.url);
    const html = await response.text();
    const $ = cheerio.load(html);

    const articles: NewsItem[] = [];

    $('.news-item, .article-item, .item').each((_, elem) => {
      const titleElem = $(elem).find('.title, h2, h3, .article-title').first();
      const linkElem = $(elem).find('a').first();
      const dateElem = $(elem).find('.date, .time, .pubdate').first();
      const viewsElem = $(elem).find('.views, .read-count').first();

      if (titleElem.length && linkElem.length) {
        articles.push({
          title: titleElem.text().trim(),
          link: new URL(linkElem.attr('href') || '', source.url).href,
          pubDate: dateElem.length ? this.parseDate(dateElem.text()) : new Date(),
          views: viewsElem.length ? parseInt(viewsElem.text().replace(/\D/g, '')) : undefined,
          source: source.name,
          category: source.category,
        });
      }
    });

    return articles;
  }

  private parseDate(dateStr: string): Date {
    const date = new Date(dateStr);
    return isNaN(date.getTime()) ? new Date() : date;
  }

  private deduplicate(newsList: NewsItem[]): NewsItem[] {
    const seen = new Set<string>();
    return newsList.filter(item => {
      const key = `${item.title}-${item.link}`;
      if (seen.has(key)) return false;
      seen.add(key);
      return true;
    });
  }

  async fetchByCategory(category: string): Promise<NewsItem[]> {
    const filteredSources = this.sources.filter(s => s.category === category);
    const fetcher = new NewsFetcher(filteredSources);
    return fetcher.fetchAll();
  }
}
