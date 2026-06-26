import { NormalizedNewsItem, NewsCategory, NewsConfig } from '../types';

export class NewsClassifier {
  private config: NewsConfig;

  constructor(config: NewsConfig) {
    this.config = config;
  }

  // 分类主入口
  classify(item: NormalizedNewsItem): NewsCategory {
    // 优先检查政策类
    if (this.isPolicy(item)) {
      return NewsCategory.POLICY;
    }

    // 检查上市公司
    if (this.isPublicCompany(item)) {
      return NewsCategory.PUBLIC_COMPANY;
    }

    // 默认为非上市公司/产业动态
    return NewsCategory.PRIVATE_COMPANY_OR_INDUSTRY;
  }

  // 批量分类
  classifyBatch(items: NormalizedNewsItem[]): Map<string, NewsCategory> {
    const result = new Map<string, NewsCategory>();

    for (const item of items) {
      result.set(item.id, this.classify(item));
    }

    return result;
  }

  // 判断是否为政策类
  private isPolicy(item: NormalizedNewsItem): boolean {
    const policyKeywords = this.config.classification.policy_keywords || [];
    const text = (item.title + ' ' + item.summary + ' ' + (item.full_text || '')).toLowerCase();

    return policyKeywords.some(keyword => text.includes(keyword));
  }

  // 判断是否为上市公司
  private isPublicCompany(item: NormalizedNewsItem): boolean {
    // 检查股票代码
    const hasStockCode = this.hasStockCode(item);

    if (hasStockCode) {
      return true;
    }

    // 检查来源是否为上市公司相关
    const source = item.source.toLowerCase();
    if (source.includes('财联社') || source.includes('证券时报') || source.includes('中国证券报')) {
      // 这些源经常报道上市公司新闻，但需要股票代码确认
      // 这里可以添加更多逻辑
    }

    return false;
  }

  // 检查是否包含股票代码
  private hasStockCode(item: NormalizedNewsItem): boolean {
    const patterns = this.config.classification.stock_code_patterns || [];
    const text = (item.title + ' ' + item.summary + ' ' + (item.full_text || ''));

    for (const pattern of patterns) {
      const regex = new RegExp(pattern);
      if (regex.test(text)) {
        return true;
      }
    }

    return false;
  }

  // TODO: 后续增强
  // 1. 支持更复杂的分类规则
  // 2. 添加行业分类（如机器人、地产、AI等）
  // 3. 支持自定义分类规则配置
  // 4. 添加分类置信度评分
  // 5. 考虑使用NLP模型进行更智能分类
}