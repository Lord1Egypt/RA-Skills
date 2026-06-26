import type { NewsItem, CategorizedNews } from './types';

export class MarkdownGenerator {
  generate(categorizedNews: CategorizedNews): string {
    const date = this.formatDate(new Date());
    let md = '';

    md += `# ${date} 每日新闻汇总\n\n`;
    md += `> 生成时间：${new Date().toLocaleString('zh-CN', { hour12: false })}\n\n`;
    md += `---\n\n`;

    const totalNews = Object.values(categorizedNews).reduce((sum, items) => sum + items.length, 0);
    md += `📊 共整理 ${totalNews} 条新闻\n\n`;

    for (const [category, items] of Object.entries(categorizedNews)) {
      if (items.length === 0) continue;

      md += `## ${category}\n\n`;
      md += `共 ${items.length} 条新闻\n\n`;

      for (const item of items) {
        md += `### ${item.title}\n\n`;

        if (item.description) {
          md += `${this.cleanDescription(item.description)}\n\n`;
        }

        md += `- **来源**：${item.source}\n`;
        md += `- **发布时间**：${this.formatDate(item.pubDate)}\n`;

        if (item.views) {
          md += `- **阅读量**：${item.views.toLocaleString('zh-CN')}\n`;
        }

        md += `- **原文链接**：[${item.link}](${item.link})\n\n`;
        md += `---\n\n`;
      }
    }

    return md;
  }

  private formatDate(date: Date): string {
    return date.toLocaleDateString('zh-CN', {
      year: 'numeric',
      month: '2-digit',
      day: '2-digit',
    });
  }

  private cleanDescription(description: string): string {
    return description
      .replace(/<[^>]*>/g, '')
      .replace(/\s+/g, ' ')
      .trim()
      .substring(0, 200) + (description.length > 200 ? '...' : '');
  }

  generateSummary(
    categorizedNews: CategorizedNews,
    options: { filePath?: string; maxPerCategory?: number; maxPerSource?: number } = {}
  ): string {
    const date = this.formatDate(new Date());
    const maxPerCategory = options.maxPerCategory ?? 5;
    const maxPerSource = options.maxPerSource ?? 2;
    let summary = `📰 ${date} 新闻简报\n\n`;

    for (const [category, items] of Object.entries(categorizedNews)) {
      if (items.length === 0) continue;

      summary += `【${category}】${items.length} 条（摘要显示 ${Math.min(items.length, maxPerCategory)} 条）\n`;
      const selected = this.selectWithSourceCap(items, maxPerCategory, maxPerSource);
      const perSourceCounts = new Map<string, number>();
      for (const item of selected) {
        summary += `- ${item.title}（来源：${item.source}）\n`;
        perSourceCounts.set(item.source, (perSourceCounts.get(item.source) ?? 0) + 1);
      }

      if (items.length > selected.length) {
        summary += `- … 余下 ${items.length - selected.length} 条详见全文\n`;
      }
      summary += '\n';
    }

    if (options.filePath) {
      summary += `本地文档：${options.filePath}\n`;
    }

    return summary.trim();
  }

  private selectWithSourceCap(
    items: NewsItem[],
    maxTotal: number,
    maxPerSource: number
  ): NewsItem[] {
    const result: NewsItem[] = [];
    const sourceCounts = new Map<string, number>();

    for (const item of items) {
      const count = sourceCounts.get(item.source) ?? 0;
      if (count >= maxPerSource) continue;
      result.push(item);
      sourceCounts.set(item.source, count + 1);
      if (result.length >= maxTotal) break;
    }

    return result;
  }

  async saveLocal(markdown: string, savePath: string): Promise<string> {
    const { mkdir, writeFile } = await import('fs/promises');
    const { join } = await import('path');
    const { homedir } = await import('os');

    const resolvedPath = savePath.replace('~', homedir());
    const date = new Date().toISOString().split('T')[0];
    const fileName = `${date}.md`;
    const filePath = join(resolvedPath, fileName);

    await mkdir(resolvedPath, { recursive: true });
    await writeFile(filePath, markdown, 'utf-8');

    return filePath;
  }
}
