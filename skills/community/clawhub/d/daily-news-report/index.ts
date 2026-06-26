import fs from 'fs';
import path from 'path';
import { NewsConfig, RawNewsItem, NormalizedNewsItem, ProcessedNewsItem, DailyReport } from './types';
import { NewsNormalizer } from './normalizer/normalize';
import { NewsDeduper } from './deduper/dedupe';
import { NewsClassifier } from './classifier/classify';
import { NewsRewriter } from './rewriter/rewrite';
import { NewsRanker } from './ranker/rank';
import { CronScheduler } from './scheduler/cron';
import { TelegramDeliverer } from './deliverer/telegram';
import { createFetchers } from './source_fetchers';

export class DailyNewsBrief {
  private config: NewsConfig;
  private normalizer: NewsNormalizer;
  private deduper: NewsDeduper;
  private classifier: NewsClassifier;
  private rewriter: NewsRewriter;
  private ranker: NewsRanker;
  private scheduler: CronScheduler;
  private deliverer: TelegramDeliverer;

  constructor(config?: Partial<NewsConfig>) {
    // 加载配置
    this.config = this.loadConfig(config);

    // 初始化各个模块
    this.normalizer = new NewsNormalizer(this.config);
    this.deduper = new NewsDeduper();
    this.classifier = new NewsClassifier(this.config);
    this.rewriter = new NewsRewriter();
    this.ranker = new NewsRanker(this.config);
    this.scheduler = new CronScheduler(this.config);

    // 初始化推送模块
    const telegramConfig = {
      chatId: '',
      botToken: ''
    };
    this.deliverer = new TelegramDeliverer(telegramConfig);

    // 注册定时任务
    this.scheduler.register(() => this.run());
  }

  // 加载配置
  private loadConfig(overrides?: Partial<NewsConfig>): NewsConfig {
    const configPath = path.join(__dirname, 'config', 'default.json');

    let defaultConfig: NewsConfig;

    try {
      const configFile = fs.readFileSync(configPath, 'utf-8');
      defaultConfig = JSON.parse(configFile);
    } catch (error) {
      console.error('Failed to load config, using defaults:', error);
      defaultConfig = this.getDefaultConfig();
    }

    // 合并覆盖配置
    return {
      ...defaultConfig,
      ...overrides
    };
  }

  // 获取默认配置
  private getDefaultConfig(): NewsConfig {
    return {
      mode: 'all',
      focus_topics: ['robot', 'real_estate', 'ai'],
      focus_keywords: {},
      sources: {
        primary: ['cls', 'ithome', '36kr'],
        backup: []
      },
      schedule: ['08:00', '17:30', '22:30'],
      max_items: 15,
      include_links: true,
      timezone: 'Asia/Shanghai',
      include_keywords: [],
      exclude_keywords: ['广告', '推广', '营销', '软文'],
      classification: {
        policy_keywords: [
          '政府', '政策', '国务院', '发改委', '工信部', '证监会', '财政部', '商务部',
          '标准', '规划', '指导意见', '通知', '方案', '办法', '条例'
        ],
        stock_code_patterns: [
          '\\(603\\d{3}\\.SH\\)',
          '\\(000\\d{3}\\.SZ\\)',
          '\\(688\\d{3}\\.SH\\)',
          '\\(\\d{4}\\.HK\\)'
        ],
        source_priority: ['cls', 'yicai', 'zqrb', 'ssnews']
      }
    };
  }

  // 主流程：执行一次完整的日报生成
  async run(isTest: boolean = false): Promise<DailyReport> {
    console.log('========================================');
    console.log('Starting Daily News Brief...');
    console.log('========================================');

    try {
      // 1. 拉取新闻
      console.log('[Step 1] Fetching news...');
      const rawNews = await this.fetchNews();
      console.log(`[Step 1] Fetched ${rawNews.length} news items`);

      if (rawNews.length === 0) {
        console.warn('[Warning] No news fetched, exiting');
        return this.emptyReport();
      }

      // 2. 标准化
      console.log('[Step 2] Normalizing news...');
      const normalizedNews = this.normalizer.normalizeBatch(rawNews);
      console.log(`[Step 2] Normalized ${normalizedNews.length} news items`);

      // 3. 去重
      console.log('[Step 3] Deduplicating news...');
      const dedupedNews = this.deduper.dedupe(normalizedNews);
      console.log(`[Step 3] After dedup: ${dedupedNews.length} news items`);

      // 4. 过滤
      console.log('[Step 4] Filtering news...');
      const filteredNews = this.filterNews(dedupedNews);
      console.log(`[Step 4] After filter: ${filteredNews.length} news items`);

      // 5. 分类
      console.log('[Step 5] Classifying news...');
      const classifiedMap = this.classifier.classifyBatch(filteredNews);
      console.log(`[Step 5] Classified ${classifiedMap.size} news items`);

      // 6. 改写
      console.log('[Step 6] Rewriting news...');
      const processedNews = await this.processNews(filteredNews, classifiedMap);
      console.log(`[Step 6] Processed ${processedNews.length} news items`);

      // 7. 排序
      console.log('[Step 7] Ranking news...');
      const rankedNews = this.ranker.rank(processedNews);
      console.log(`[Step 7] Ranked ${rankedNews.length} news items`);

      // 8. 截取
      console.log('[Step 8] Trimming to max items...');
      const finalNews = this.trimToMaxItems(rankedNews);
      console.log(`[Step 8] Final count: ${finalNews.length} news items`);

      // 9. 生成报告
      console.log('[Step 9] Generating report...');
      const report = this.generateReport(finalNews);
      console.log(`[Step 9] Report generated with ${report.total_items} items`);

      // 10. 输出
      console.log('[Step 10] Outputting report...');
      this.outputReport(report);

      // 11. 推送（如果不是测试模式）
      if (!isTest && this.deliverer.isConfigured()) {
        console.log('[Step 11] Delivering to Telegram...');
        await this.deliverer.deliver(report);
        console.log('[Step 11] Delivery completed');
      }

      console.log('========================================');
      console.log('Daily News Brief completed successfully!');
      console.log('========================================');

      return report;
    } catch (error) {
      console.error('[Error] Daily News Brief failed:', error);
      throw error;
    }
  }

  // 拉取新闻
  private async fetchNews(): Promise<RawNewsItem[]> {
    const fetchers = createFetchers();
    const allItems: RawNewsItem[] = [];

    for (const fetcher of fetchers) {
      if (fetcher.isEnabled(this.config)) {
        try {
          const items = await fetcher.fetch();
          allItems.push(...items);
        } catch (error) {
          console.error(`[Fetcher] Failed to fetch from ${fetcher.name}:`, error);
        }
      }
    }

    return allItems;
  }

  // 过滤新闻
  private filterNews(items: NormalizedNewsItem[]): NormalizedNewsItem[] {
    let filtered = items;

    // 时间范围过滤（最近48小时）
    const cutoffTime = new Date(Date.now() - 48 * 60 * 60 * 1000);
    filtered = filtered.filter(item => item.published_at >= cutoffTime);

    // 包含关键词过滤
    if (this.config.include_keywords && this.config.include_keywords.length > 0) {
      filtered = filtered.filter(item => {
        const text = (item.title + ' ' + item.summary).toLowerCase();
        return this.config.include_keywords!.some(keyword =>
          text.includes(keyword.toLowerCase())
        );
      });
    }

    return filtered;
  }

  // 处理新闻（分类 + 改写）
  private async processNews(
    items: NormalizedNewsItem[],
    classifiedMap: Map<string, string>
  ): Promise<ProcessedNewsItem[]> {
    const processed: ProcessedNewsItem[] = [];

    for (const item of items) {
      const category = classifiedMap.get(item.id) as any;

      // 改写新闻
      const rewriteResult = await this.rewriter.rewrite(item);

      // 生成处理后的新闻项
      const processedItem = this.ranker.processForRanking(
        item,
        category,
        rewriteResult.success ? rewriteResult.rewritten : undefined
      );

      processed.push(processedItem);
    }

    return processed;
  }

  // 截取到最大数量
  private trimToMaxItems(items: ProcessedNewsItem[]): ProcessedNewsItem[] {
    if (items.length <= this.config.max_items) {
      return items;
    }

    return items.slice(0, this.config.max_items);
  }

  // 生成报告
  private generateReport(items: ProcessedNewsItem[]): DailyReport {
    const now = new Date();
    const itemsByCategory: {
      policy: ProcessedNewsItem[];
      public_company: ProcessedNewsItem[];
      private_company_or_industry: ProcessedNewsItem[];
    } = {
      policy: [],
      public_company: [],
      private_company_or_industry: []
    };

    for (const item of items) {
      itemsByCategory[item.category as keyof typeof itemsByCategory].push(item);
    }

    return {
      date: now.toISOString().split('T')[0],
      generated_at: now.toISOString(),
      mode: this.config.mode,
      total_items: items.length,
      items: itemsByCategory
    };
  }

  // 输出报告
  private outputReport(report: DailyReport): void {
    // 生成Markdown格式的报告
    const markdown = this.generateMarkdownReport(report);

    // 输出到terminal
    console.log('\n' + '='.repeat(50));
    console.log('📰 每日日报生成完成');
    console.log('='.repeat(50) + '\n');
    console.log(markdown);
    console.log('\n' + '='.repeat(50));
  }

  // 生成Markdown报告
  private generateMarkdownReport(report: DailyReport): string {
    const date = new Date(report.date).toLocaleDateString('zh-CN');
    const time = new Date(report.generated_at).toLocaleTimeString('zh-CN', {
      hour: '2-digit',
      minute: '2-digit'
    });

    let markdown = `# 每日日报｜${date} ${time}\n\n`;
    markdown += `监控模式：${report.mode === 'all' ? '全量模式' : '重点领域模式'}\n`;
    markdown += `新闻总数：${report.total_items} 条\n\n`;

    // 政策类
    if (report.items.policy.length > 0) {
      markdown += '## 一、政策\n\n';
      for (const item of report.items.policy) {
        markdown += this.formatItem(item);
      }
      markdown += '\n';
    }

    // 上市公司
    if (report.items.public_company.length > 0) {
      markdown += '## 二、上市公司\n\n';
      for (const item of report.items.public_company) {
        markdown += this.formatItem(item);
      }
      markdown += '\n';
    }

    // 非上市公司/产业动态
    if (report.items.private_company_or_industry.length > 0) {
      markdown += '## 三、非上市公司 / 产业动态\n\n';
      for (const item of report.items.private_company_or_industry) {
        markdown += this.formatItem(item);
      }
      markdown += '\n';
    }

    // 添加页脚
    markdown += '\n---\n';
    markdown += '*由Daily News Brief自动生成*';

    return markdown;
  }

  // 格式化单条新闻
  private formatItem(item: ProcessedNewsItem): string {
    const content = item.rewritten || item.title;
    const time = item.published_at.toLocaleTimeString('zh-CN', {
      hour: '2-digit',
      minute: '2-digit'
    });

    let formatted = `- ${content}`;

    if (this.config.include_links && item.url) {
      formatted += `\n  来源：${item.source} ${time} [链接](${item.url})`;
    } else {
      formatted += `\n  来源：${item.source} ${time}`;
    }

    formatted += '\n';

    return formatted;
  }

  // 生成空报告
  private emptyReport(): DailyReport {
    const now = new Date();

    return {
      date: now.toISOString().split('T')[0],
      generated_at: now.toISOString(),
      mode: this.config.mode,
      total_items: 0,
      items: {
        policy: [],
        public_company: [],
        private_company_or_industry: []
      }
    };
  }

  // 启动定时任务
  async startScheduler(): Promise<void> {
    await this.scheduler.start();
  }

  // 停止定时任务
  async stopScheduler(): Promise<void> {
    await this.scheduler.stop();
  }

  // 测试运行
  async testRun(): Promise<DailyReport> {
    console.log('[Test] Running in test mode (no delivery)');
    return this.run(true);
  }

  // 实际运行（会发送到Telegram）
  async realRun(): Promise<DailyReport> {
    console.log('[Run] Running in real mode (will deliver to Telegram)');
    return this.run(false);
  }
}

// CLI入口函数
export async function cli(): Promise<void> {
  const args = process.argv.slice(2);
  const command = args[0];

  const brief = new DailyNewsBrief();

  switch (command) {
    case 'start':
      await brief.startScheduler();
      console.log('[CLI] Scheduler started. Press Ctrl+C to stop.');
      break;

    case 'test':
      await brief.testRun();
      break;

    case 'run':
      await brief.realRun();
      break;

    case 'start':
      await brief.startScheduler();
      console.log('[CLI] Scheduler started. Press Ctrl+C to stop.');
      break;

    case 'config':
      console.log('[Config]', JSON.stringify(brief['config'], null, 2));
      break;

    default:
      console.log('[CLI] Usage:');
      console.log('  daily-news-brief run      - Run once');
      console.log('  daily-news-brief test     - Run in test mode (no delivery)');
      console.log('  daily-news-brief start    - Start scheduler');
      console.log('  daily-news-brief config   - Show current config');
  }
}

// 如果直接运行此文件
if (require.main === module) {
  cli().catch(error => {
    console.error('[CLI] Error:', error);
    process.exit(1);
  });
}

// 导出供外部调用
export default DailyNewsBrief;

// OpenClaw skill 入口
export function runSkill() {
  return cli();
}

// TODO: 后续增强
// 1. 添加数据库支持（存储历史报告）
// 2. 实现真实的Markdown文件输出
// 3. 添加命令行参数解析
// 4. 支持配置文件热加载
// 5. 添加日志系统
// 6. 实现健康检查接口
// 7. 添加性能监控
// 8. 支持多实例部署