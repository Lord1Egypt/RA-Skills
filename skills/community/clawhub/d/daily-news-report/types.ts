// 核心数据类型定义

export interface RawNewsItem {
  title: string;
  source: string;
  published_at: string;
  url: string;
  summary?: string;
  full_text?: string;
  author?: string;
  tags?: string[];
}

export interface NormalizedNewsItem {
  id: string;
  title: string;
  source: string;
  source_priority: number;
  published_at: Date;
  url: string;
  summary: string;
  full_text?: string;
  author?: string;
  tags?: string[];
  // 原始数据保留
  _raw?: RawNewsItem;
}

export enum NewsCategory {
  POLICY = 'policy',
  PUBLIC_COMPANY = 'public_company',
  PRIVATE_COMPANY_OR_INDUSTRY = 'private_company_or_industry'
}

export interface ProcessedNewsItem extends NormalizedNewsItem {
  category: NewsCategory;
  category_score: number;
  focus_relevance: number;
  has_hard_data: boolean;
  data_signals: string[];
  rewritten?: string;
  final_score: number;
}

export interface NewsConfig {
  mode: 'all' | 'focused';
  focus_topics: string[];
  focus_keywords: Record<string, string[]>;
  sources: {
    primary: string[];
    backup: string[];
  };
  schedule: string[];
  max_items: number;
  include_links: boolean;
  timezone: string;
  include_keywords: string[];
  exclude_keywords: string[];
  classification: {
    policy_keywords: string[];
    stock_code_patterns: string[];
    source_priority: string[];
  };
}

export interface SourceFetcher {
  name: string;
  priority: number;
  fetch(): Promise<RawNewsItem[]>;
  isEnabled(config: NewsConfig): boolean;
}

export interface RewriterResult {
  rewritten: string;
  success: boolean;
  error?: string;
}

export interface DailyReport {
  date: string;
  generated_at: string;
  mode: string;
  total_items: number;
  items: {
    [NewsCategory.POLICY]: ProcessedNewsItem[];
    [NewsCategory.PUBLIC_COMPANY]: ProcessedNewsItem[];
    [NewsCategory.PRIVATE_COMPANY_OR_INDUSTRY]: ProcessedNewsItem[];
  };
}

export interface DeliveryResult {
  success: boolean;
  message?: string;
  error?: string;
}