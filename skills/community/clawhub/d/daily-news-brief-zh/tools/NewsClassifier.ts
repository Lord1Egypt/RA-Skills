import type { NewsItem } from './types';

export class NewsClassifier {
  private categoryKeywords = {
    科技: ['科技', '技术', '互联网', '5G', '芯片', '手机', '电脑', '软件', '硬件', '操作系统', '云计算', '区块链', '网络安全'],
    财经: ['财经', '经济', '股市', '投资', '融资', 'IPO', '金融', '基金', '股票', '债券', '汇率', '并购'],
    AI: ['人工智能', 'AI', '大模型', 'GPT', '深度学习', '机器学习', '神经网络', '自然语言处理', '计算机视觉', '生成式AI', 'LLM', 'ChatGPT'],
    智能体: ['智能体', 'Agent', 'AI Agent', '自主代理', '智能代理', '多智能体', 'Agent系统'],
  };

  classify(item: NewsItem): string {
    const scores: Record<string, number> = {};

    for (const [category, keywords] of Object.entries(this.categoryKeywords)) {
      let score = 0;

      for (const keyword of keywords) {
        if (item.title.includes(keyword)) {
          score += 3;
        }
        if (item.description && item.description.includes(keyword)) {
          score += 1;
        }
      }

      scores[category] = score;
    }

    const sorted = Object.entries(scores).sort((a, b) => b[1] - a[1]);

    return sorted[0][1] > 0 ? sorted[0][0] : '科技';
  }

  classifyAll(items: NewsItem[]): NewsItem[] {
    return items.map(item => ({
      ...item,
      category: this.classify(item) as any,
    }));
  }

  categorize(items: NewsItem[]): Record<string, NewsItem[]> {
    const categorized: Record<string, NewsItem[]> = {
      科技: [],
      财经: [],
      AI: [],
      智能体: [],
    };

    for (const item of items) {
      if (categorized[item.category]) {
        categorized[item.category].push(item);
      } else {
        categorized['科技'].push(item);
      }
    }

    return categorized;
  }

  sortByPopularity(items: NewsItem[]): NewsItem[] {
    const now = new Date();

    return items.sort((a, b) => {
      const hoursSinceA = (now.getTime() - a.pubDate.getTime()) / (1000 * 60 * 60);
      const hoursSinceB = (now.getTime() - b.pubDate.getTime()) / (1000 * 60 * 60);

      const timeScoreA = hoursSinceA < 24 ? 100 : Math.max(1, 100 / hoursSinceA);
      const timeScoreB = hoursSinceB < 24 ? 100 : Math.max(1, 100 / hoursSinceB);

      const viewScoreA = a.views || 0;
      const viewScoreB = b.views || 0;

      const scoreA = timeScoreA * 0.6 + viewScoreA * 0.4;
      const scoreB = timeScoreB * 0.6 + viewScoreB * 0.4;

      return scoreB - scoreA;
    });
  }

  limitPerCategory(categorized: Record<string, NewsItem[]>, max: number): Record<string, NewsItem[]> {
    const limited: Record<string, NewsItem[]> = {};

    for (const [category, items] of Object.entries(categorized)) {
      limited[category] = this.sortByPopularity(items).slice(0, max);
    }

    return limited;
  }

  limitPerCategoryWithSourceCap(
    categorized: Record<string, NewsItem[]>,
    maxTotal: number,
    maxPerSource: number
  ): Record<string, NewsItem[]> {
    const limited: Record<string, NewsItem[]> = {};

    for (const [category, items] of Object.entries(categorized)) {
      const sorted = this.sortByPopularity(items);
      const sourceCounts = new Map<string, number>();
      const result: NewsItem[] = [];

      for (const item of sorted) {
        const count = sourceCounts.get(item.source) ?? 0;
        if (count >= maxPerSource) continue;

        result.push(item);
        sourceCounts.set(item.source, count + 1);
        if (result.length >= maxTotal) break;
      }

      limited[category] = result;
    }

    return limited;
  }
}
