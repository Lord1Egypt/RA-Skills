import { BaseFetcher } from './base';
import { RawNewsItem } from '../types';

export class Kr36Fetcher extends BaseFetcher {
  name = '36kr';
  priority = 7;

  async fetch(): Promise<RawNewsItem[]> {
    // TODO: 实现36氪新闻抓取
    // 实际实现需要：
    // 1. 分析36氪API或网页结构
    // 2. 获取创业和投资新闻
    // 3. 提取融资信息

    const mockData: RawNewsItem[] = [
      {
        title: '36氪：某机器人公司完成A轮融资，金额达2亿元人民币',
        source: '36氪',
        published_at: new Date(Date.now() - 7200000).toISOString(),
        url: 'https://36kr.com/xxx',
        summary: '某机器人公司完成A轮融资，金额达2亿元人民币',
        full_text: '某机器人公司完成A轮融资，金额达2亿元人民币，由知名投资机构领投。'
      }
    ];

    console.log(`[36Kr] Fetched ${mockData.length} items`);
    return mockData;
  }

  // TODO: 后续实现
  // 1. 实现36氪API调用或网页抓取
  // 2. 添加错误处理
  // 3. 支持融资信息提取
  // 4. 添加缓存机制
}