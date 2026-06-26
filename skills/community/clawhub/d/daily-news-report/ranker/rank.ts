import { NormalizedNewsItem, ProcessedNewsItem, NewsCategory, NewsConfig } from '../types';

export class NewsRanker {
  private config: NewsConfig;

  constructor(config: NewsConfig) {
    this.config = config;
  }

  // 对处理后的新闻进行排序
  rank(items: ProcessedNewsItem[]): ProcessedNewsItem[] {
    // 按最终分数降序排序
    const sorted = [...items].sort((a, b) => {
      // 第一层：分类优先级
      const categoryDiff = this.getCategoryPriority(a.category) - this.getCategoryPriority(b.category);
      if (categoryDiff !== 0) {
        return -categoryDiff; // 优先级越高排名越前
      }

      // 第二层：最终评分
      if (b.final_score !== a.final_score) {
        return b.final_score - a.final_score;
      }

      // 同分按时间排序（新的在前）
      return b.published_at.getTime() - a.published_at.getTime();
    });

    return sorted;
  }

  // 生成处理后的新闻项（带评分）
  processForRanking(normalized: NormalizedNewsItem, category: NewsCategory, rewritten?: string): ProcessedNewsItem {
    return {
      ...normalized,
      category,
      category_score: this.calculateCategoryScore(category, normalized),
      focus_relevance: this.calculateFocusRelevance(normalized),
      has_hard_data: this.hasHardData(normalized),
      data_signals: this.extractDataSignals(normalized),
      rewritten,
      final_score: this.calculateFinalScore(normalized, category)
    };
  }

  // 获取分类优先级
  private getCategoryPriority(category: NewsCategory): number {
    switch (category) {
      case NewsCategory.POLICY:
        return 100; // 政策优先级最高
      case NewsCategory.PUBLIC_COMPANY:
        return 90; // 上市公司次之
      case NewsCategory.PRIVATE_COMPANY_OR_INDUSTRY:
        return 80; // 产业动态最低
      default:
        return 0;
    }
  }

  // 计算分类评分
  private calculateCategoryScore(category: NewsCategory, item: NormalizedNewsItem): number {
    const baseScore = this.getCategoryPriority(category);

    // 源优先级加分
    const sourceBonus = item.source_priority * 0.1;

    return baseScore + sourceBonus;
  }

  // 计算主题相关性评分
  private calculateFocusRelevance(item: NormalizedNewsItem): number {
    if (this.config.mode !== 'focused') {
      return 50; // 全量模式下默认中等相关性
    }

    const text = (item.title + ' ' + item.summary).toLowerCase();
    let relevanceScore = 0;

    // 检查每个focus topic
    for (const topic of this.config.focus_topics || []) {
      const keywords = this.config.focus_keywords[topic] || [];

      // 计算匹配的关键词数量
      const matchCount = keywords.filter(keyword => text.includes(keyword)).length;

      if (matchCount > 0) {
        relevanceScore += matchCount * 20; // 每个匹配关键词加20分
      }
    }

    return Math.min(relevanceScore, 100); // 最高100分
  }

  // 检查是否包含硬数据
  private hasHardData(item: NormalizedNewsItem): boolean {
    const text = item.full_text || item.summary || '';

    // 检查数字模式
    const patterns = [
      /\d+亿/,
      /\d+千万/,
      /\d+百万/,
      /\d+万/,
      /\d+%/,
      /\d+亿元/,
      /\d+千万/,
      /\d+万/,
      /\d+台/,
      /\d+个/
    ];

    return patterns.some(pattern => pattern.test(text));
  }

  // 提取数据信号
  private extractDataSignals(item: NormalizedNewsItem): string[] {
    const text = item.full_text || item.summary || '';
    const signals: string[] = [];

    // 提取各种数据
    const numberPattern = /\d+(\.\d+)?[亿元千万万千百十]?/g;
    const matches = text.match(numberPattern);

    if (matches) {
      signals.push(...matches.slice(0, 3)); // 最多取3个数据
    }

    return signals;
  }

  // 计算最终评分
  private calculateFinalScore(item: NormalizedNewsItem, category: NewsCategory): number {
    const categoryScore = this.calculateCategoryScore(category, item);
    const focusRelevance = this.calculateFocusRelevance(item);
    const hardDataBonus = this.hasHardData(item) ? 10 : 0;

    // 时间新鲜度加分（最近24小时内）
    const hoursSincePublish = (Date.now() - item.published_at.getTime()) / (1000 * 60 * 60);
    const timeBonus = hoursSincePublish <= 24 ? 5 : 0;

    // 综合评分
    const finalScore = categoryScore * 0.4 + focusRelevance * 0.3 + hardDataBonus + timeBonus;

    return Math.round(finalScore * 100) / 100; // 保留两位小数
  }

  // TODO: 后续增强
  // 1. 实现更复杂的评分算法
  // 2. 支持用户自定义权重
  // 3. 添加用户行为反馈（点击率、停留时间等）
  // 4. 实现机器学习模型优化排序
  // 5. 支持分领域个性化排序
  // 6. 添加评分日志和调试功能
}