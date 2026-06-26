/**
 * Daily News Brief Type Definitions
 * 新闻聚合工具的类型定义
 */

export interface NewsItem {
  /** 新闻标题 */
  title: string;
  /** 新闻链接 */
  link: string;
  /** 发布时间 */
  pubDate: Date;
  /** 新闻描述（可选） */
  description?: string;
  /** 新闻来源（网站名称） */
  source: string;
  /** 新闻分类 */
  category: '科技' | '财经' | 'AI' | '智能体' | '';
  /** 阅读量（可选） */
  views?: number;
  /** 收藏数（可选） */
  favorites?: number;
  /** 评论数（可选） */
  comments?: number;
}

export interface NewsSource {
  /** 新闻源名称 */
  name: string;
  /** RSS 或网页 URL */
  url: string;
  /** 类型：rss 或 web */
  type: 'rss' | 'web';
  /** 分类 */
  category: '科技' | '财经' | 'AI' | '智能体';
}

export interface Config {
  /** 新闻源列表 */
  newsSources: NewsSource[];
  /** 定时任务 cron 表达式 */
  schedule: string;
  /** 是否保存本地文档 */
  saveLocalDoc: boolean;
  /** 本地文档保存路径 */
  localDocPath: string;
  /** 每类最多新闻数 */
  maxNewsPerCategory: number;
  /** 摘要每类最多条数 */
  summaryMaxPerCategory: number;
  /** 每类每来源最多条数 */
  maxPerSourcePerCategory: number;
  /** 摘要每类每来源最多条数 */
  summaryMaxPerSource: number;
  /** OpenClaw 推送配置 */
  push?: PushConfig;
}

export interface CategorizedNews {
  [category: string]: NewsItem[];
}

export interface FetchNewsOptions {
  /** 测试模式：只抓取少量新闻 */
  test?: boolean;
  /** 指定日期 */
  date?: string;
  /** 仅抓取指定分类 */
  category?: '科技' | '财经' | 'AI' | '智能体';
  /** 是否推送到 OpenClaw 通道 */
  push?: boolean;
}

export interface PushConfig {
  /** 是否启用 OpenClaw 推送 */
  enabled: boolean;
  /** 推送通道列表 */
  channels: string[];
  /** 通道目标（可选，按通道名映射） */
  targets?: Record<string, string>;
}
