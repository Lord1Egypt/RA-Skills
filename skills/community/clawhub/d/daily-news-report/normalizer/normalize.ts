import { RawNewsItem, NormalizedNewsItem, NewsConfig } from '../types';

export class NewsNormalizer {
  private config: NewsConfig;

  constructor(config: NewsConfig) {
    this.config = config;
  }

  // 标准化单个新闻项
  normalize(item: RawNewsItem): NormalizedNewsItem {
    const sourcePriority = this.getSourcePriority(item.source);

    return {
      id: this.generateId(item.title, item.url),
      title: item.title.trim(),
      source: item.source,
      source_priority: sourcePriority,
      published_at: new Date(item.published_at),
      url: item.url,
      summary: item.summary || item.title,
      full_text: item.full_text,
      author: item.author,
      tags: item.tags || [],
      _raw: item
    };
  }

  // 批量标准化
  normalizeBatch(items: RawNewsItem[]): NormalizedNewsItem[] {
    return items
      .map(item => this.normalize(item))
      .filter(item => this.isValid(item))
      .sort((a, b) => b.published_at.getTime() - a.published_at.getTime());
  }

  // 验证数据有效性
  private isValid(item: NormalizedNewsItem): boolean {
    // 必须有标题和URL
    if (!item.title || !item.url) {
      return false;
    }

    // 标题不能太短或太长
    if (item.title.length < 5 || item.title.length > 500) {
      return false;
    }

    // 不能包含排除关键词
    const text = (item.title + ' ' + item.summary).toLowerCase();
    if (this.hasExcludedKeywords(text)) {
      return false;
    }

    // URL必须有效
    try {
      new URL(item.url);
    } catch {
      return false;
    }

    return true;
  }

  // 获取来源优先级
  private getSourcePriority(source: string): number {
    const sourcePriority = this.config.classification.source_priority || [];
    const index = sourcePriority.findIndex(s => source.toLowerCase().includes(s));

    if (index !== -1) {
      return 100 - index; // 越靠前优先级越高
    }

    return 0; // 默认优先级
  }

  // 检查是否包含排除关键词
  private hasExcludedKeywords(text: string): boolean {
    const excludeKeywords = this.config.exclude_keywords || [];
    return excludeKeywords.some(keyword => text.includes(keyword));
  }

  // 生成唯一ID
  private generateId(title: string, url: string): string {
    const crypto = require('crypto');
    return crypto.createHash('md5').update(title + url).digest('hex');
  }

  // TODO: 后续增强
  // 1. 添加日期范围过滤
  // 2. 支持内容长度限制
  // 3. 添加来源白名单/黑名单
  // 4. 支持内容质量评估
}