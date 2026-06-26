import { NormalizedNewsItem, RewriterResult } from '../types';

// 固定rewrite prompt
const REWRITE_PROMPT = `请将我提供的新闻按照以下规则改写成"一句话新闻"：

1. 结构要求：
   * 用 1–2 句完成整条新闻。
   * 主题要明确，突出核心事件（如发布、布局、出货、融资、合作、产品突破等）。

2. 内容要求：
   * 必须保留所有关键数据（如营收、出货量、占比、市场份额、融资金额、注册资本等）。
   * 保持文字简洁、行业研报级表达。

3. 风格要求：
   * 参考以下格式风格：
   "【公司名】关键动作 + 场景落地/战略意义；关键数据（出货/市占率/营收/利润等）。"

同时要遵守：
- 不编造数字
- 不增加无依据判断
- 公司名、政策名、股票代码、技术术语必须保留准确`;

export class NewsRewriter {
  // 改写单条新闻
  async rewrite(item: NormalizedNewsItem, config?: any): Promise<RewriterResult> {
    try {
      const content = this.buildContent(item);

      // TODO: 调用大模型API进行改写
      // 目前先返回模拟结果
      const rewritten = this.mockRewrite(item);

      console.log(`[Rewriter] Rewrote news: ${item.title.substring(0, 50)}...`);

      return {
        rewritten,
        success: true
      };
    } catch (error) {
      return {
        rewritten: '',
        success: false,
        error: error instanceof Error ? error.message : 'Unknown error'
      };
    }
  }

  // 批量改写
  async rewriteBatch(items: NormalizedNewsItem[], config?: any): Promise<RewriterResult[]> {
    const results = [];

    for (const item of items) {
      const result = await this.rewrite(item, config);
      results.push(result);
    }

    return results;
  }

  // 构改写内容
  private buildContent(item: NormalizedNewsItem): string {
    // 优先使用full_text，其次是summary，最后是title
    let content = item.full_text || item.summary || item.title;

    // 清理格式
    content = content.trim();

    // 如果内容太长，截取到合理长度
    if (content.length > 1000) {
      content = content.substring(0, 1000) + '...';
    }

    return content;
  }

  // 模拟改写（临时）
  private mockRewrite(item: NormalizedNewsItem): string {
    // 提取关键信息
    const keywords = this.extractKeywords(item);
    const data = this.extractData(item);

    // 根据标题构造改写
    const action = this.extractAction(item.title);
    const company = this.extractCompany(item.title);

    return `【${company || item.source}】${action}；${data}`;
  }

  // 提取动作
  private extractAction(title: string): string {
    const actions = [
      '发布', '推出', '布局', '融资', '完成', '达成', '获得', '启动',
      '签署', '合作', '收购', '并购', '投资', '建设', '开工', '投产'
    ];

    for (const action of actions) {
      if (title.includes(action)) {
        return action;
      }
    }

    return '相关动作';
  }

  // 提取公司名
  private extractCompany(title: string): string {
    // 简单提取：提取标题开头的公司名
    const firstPart = title.split(/发布|推出|融资|完成/)[0];

    if (firstPart.length > 2) {
      return firstPart.trim();
    }

    // 检查股票代码
    const stockCodeRegex = /\((603\d{3}|000\d{3}|688\d{3}|[0-9]{4})\)/;
    const match = title.match(stockCodeRegex);
    if (match) {
      return match[0];
    }

    return '某公司';
  }

  // 提取数据
  private extractData(item: NormalizedNewsItem): string {
    const text = item.full_text || item.summary || '';
    const numbers = text.match(/\d+(\.\d+)?[亿元千万万千百十]?/g);

    if (numbers && numbers.length > 0) {
      const dataSignals = numbers.slice(0, 2); // 取前两个数据
      return `数据：${dataSignals.join('、')}`;
    }

    return '具体数据待进一步获取';
  }

  // 提取关键词
  private extractKeywords(item: NormalizedNewsItem): string[] {
    // TODO: 实现关键词提取
    return [];
  }

  // TODO: 后续增强
  // 1. 集成真实的大模型API（如Claude、GPT等）
  // 2. 改进关键词提取逻辑
  // 3. 添加改写质量评估
  // 4. 支持多种改写风格
  // 5. 添加重试机制和错误处理
  // 6. 支持自定义prompt模板
}