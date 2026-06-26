import { BaseFetcher } from './base';
import { RawNewsItem } from '../types';

export class ITHomeFetcher extends BaseFetcher {
  name = 'ithome';
  priority = 8;

  async fetch(): Promise<RawNewsItem[]> {
    // TODO: 实现IT之家新闻抓取
    // 实际实现需要：
    // 1. 分析IT之家网页结构
    // 2. 实现RSS解析或网页抓取
    // 3. 提取科技新闻

    const mockData: RawNewsItem[] = [
      {
        title: 'IT之家：某科技公司发布新一代AI大模型，推理性能提升50%',
        source: 'IT之家',
        published_at: new Date(Date.now() - 3600000).toISOString(),
        url: 'https://www.ithome.com/xxx',
        summary: '某科技公司发布新一代AI大模型，推理性能提升50%',
        full_text: '某科技公司发布新一代AI大模型，推理性能提升50%，支持多模态输入输出。'
      }
    ];

    console.log(`[ITHome] Fetched ${mockData.length} items`);
    return mockData;
  }

  // TODO: 后续实现
  // 1. 实现RSS解析或网页抓取
  // 2. 添加错误处理
  // 3. 支持分类筛选
  // 4. 添加缓存机制
}