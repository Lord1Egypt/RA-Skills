import { NormalizedNewsItem } from '../types';

export class NewsDeduper {
  // 去重主入口
  dedupe(items: NormalizedNewsItem[]): NormalizedNewsItem[] {
    if (items.length === 0) {
      return [];
    }

    // 第一步：URL去重
    const urlDeduped = this.dedupeByUrl(items);

    // 第二步：标题规范化去重
    const titleDeduped = this.dedupeByTitle(urlDeduped);

    // 第三步：多源事件去重（保留财联社优先）
    const multiSourceDeduped = this.dedupeMultiSource(titleDeduped);

    // 第四步：预留语义相似去重（暂不实现）
    // const semanticDeduped = this.dedupeBySemantic(multiSourceDeduped);

    console.log(`[Deduper] ${items.length} → ${multiSourceDeduped.length} items`);

    return multiSourceDeduped;
  }

  // URL去重
  private dedupeByUrl(items: NormalizedNewsItem[]): NormalizedNewsItem[] {
    const urlMap = new Map<string, NormalizedNewsItem>();

    for (const item of items) {
      const normalizedUrl = this.normalizeUrl(item.url);

      if (!urlMap.has(normalizedUrl)) {
        urlMap.set(normalizedUrl, item);
      } else {
        // 如果新项优先级更高，则替换
        const existing = urlMap.get(normalizedUrl)!;
        if (item.source_priority > existing.source_priority) {
          urlMap.set(normalizedUrl, item);
        }
      }
    }

    return Array.from(urlMap.values());
  }

  // 标题规范化去重
  private dedupeByTitle(items: NormalizedNewsItem[]): NormalizedNewsItem[] {
    const titleMap = new Map<string, NormalizedNewsItem>();

    for (const item of items) {
      const normalizedTitle = this.normalizeTitle(item.title);

      if (!titleMap.has(normalizedTitle)) {
        titleMap.set(normalizedTitle, item);
      } else {
        // 保留优先级更高的
        const existing = titleMap.get(normalizedTitle)!;
        if (item.source_priority > existing.source_priority) {
          titleMap.set(normalizedTitle, item);
        }
      }
    }

    return Array.from(titleMap.values());
  }

  // 多源事件去重（保留财联社优先）
  private dedupeMultiSource(items: NormalizedNewsItem[]): NormalizedNewsItem[] {
    const eventMap = new Map<string, NormalizedNewsItem[]>();

    // 按事件分组
    for (const item of items) {
      const eventKey = this.generateEventKey(item);

      if (!eventMap.has(eventKey)) {
        eventMap.set(eventKey, []);
      }
      eventMap.get(eventKey)!.push(item);
    }

    // 每组保留一个（优先级最高的）
    const result: NormalizedNewsItem[] = [];
    for (const [key, group] of eventMap) {
      const bestItem = this.selectBestItem(group);
      result.push(bestItem);
    }

    return result;
  }

  // 生成事件Key（用于判断是否为同一事件）
  private generateEventKey(item: NormalizedNewsItem): string {
    // 简单策略：使用标题前100个字符作为key
    // 后续可以改进为更智能的实体识别
    const normalizedTitle = this.normalizeTitle(item.title);
    return normalizedTitle.substring(0, 100);
  }

  // 选择最优项（优先级最高的）
  private selectBestItem(items: NormalizedNewsItem[]): NormalizedNewsItem {
    // 按source_priority降序排序
    return items.sort((a, b) => b.source_priority - a.source_priority)[0];
  }

  // 标准化URL
  private normalizeUrl(url: string): string {
    try {
      const urlObj = new URL(url);
      return urlObj.origin + urlObj.pathname;
    } catch {
      return url;
    }
  }

  // 标准化标题
  private normalizeTitle(title: string): string {
    return title
      .toLowerCase()
      .replace(/[^\u4e00-\u9fa5a-z0-9\s]/g, '') // 移除非中文、英文、数字、空格的字符
      .replace(/\s+/g, ' ')
      .trim();
  }

  // TODO: 后续增强
  // 1. 实现语义相似去重（需要embedding或相似度计算）
  // 2. 改进事件分组算法（实体识别）
  // 3. 支持时间窗口去重（同一时间段的相似事件）
  // 4. 添加去重统计信息
  // 5. 支持配置去重阈值
}