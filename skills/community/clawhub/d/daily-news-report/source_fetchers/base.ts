import { SourceFetcher, RawNewsItem } from '../types';

export abstract class BaseFetcher implements SourceFetcher {
  abstract name: string;
  abstract priority: number;

  // 检查是否启用
  isEnabled(config: any): boolean {
    const primarySources = config.sources?.primary || [];
    const backupSources = config.sources?.backup || [];
    return primarySources.includes(this.name) || backupSources.includes(this.name);
  }

  // 抽象方法，子类必须实现
  abstract fetch(): Promise<RawNewsItem[]>;

  // 通用方法：清理HTML标签
  protected stripHtml(html?: string): string {
    if (!html) return '';
    return html.replace(/<[^>]*>/g, '').trim();
  }

  // 通用方法：清理多余的空格
  protected normalizeSpaces(text: string): string {
    return text.replace(/\s+/g, ' ').trim();
  }

  // 通用方法：提取文本中的数字
  protected extractNumbers(text: string): number[] {
    const matches = text.match(/\d+(\.\d+)?/g);
    return matches ? matches.map(Number) : [];
  }

  // 通用方法：检查是否包含排除词
  protected hasExcludedKeywords(text: string, excludeKeywords: string[]): boolean {
    return excludeKeywords.some(keyword => text.includes(keyword));
  }

  // 通用方法：生成唯一ID
  protected generateId(title: string, url: string): string {
    const crypto = require('crypto');
    return crypto.createHash('md5').update(title + url).digest('hex');
  }
}