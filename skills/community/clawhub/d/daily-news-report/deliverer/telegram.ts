import { DailyReport, DeliveryResult } from '../types';
import { exec } from 'child_process';

export class TelegramDeliverer {
  private chatId?: string;
  private botToken?: string;
  private enabled: boolean;

  constructor(config?: { chatId?: string; botToken?: string }) {
    this.chatId = config?.chatId;
    this.botToken = config?.botToken;
    this.enabled = !!this.chatId && !!this.botToken;
  }

  // 发送日报
  async deliver(report: DailyReport): Promise<DeliveryResult> {
    if (!this.enabled) {
      return {
        success: false,
        error: 'Telegram not configured'
      };
    }

    try {
      // 生成markdown格式的日报
      const markdown = this.generateMarkdown(report);

      // 发送到Telegram
      await this.sendMessage(markdown);

      console.log(`[Telegram] Report delivered successfully`);

      return {
        success: true,
        message: 'Report delivered successfully'
      };
    } catch (error) {
      const errorMessage = error instanceof Error ? error.message : 'Unknown error';

      console.error(`[Telegram] Delivery failed:`, errorMessage);
      console.error('[Telegram] Error details:', JSON.stringify(error, null, 2));

      return {
        success: false,
        error: errorMessage
      };
    }
  }

  // 生成markdown格式的日报
  private generateMarkdown(report: DailyReport): string {
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
  private formatItem(item: any): string {
    // 使用改写后的内容，如果没有则使用原标题
    const content = item.rewritten || item.title;

    let formatted = `- ${content}`;

    // 添加来源和时间
    const time = item.published_at.toLocaleTimeString('zh-CN', {
      hour: '2-digit',
      minute: '2-digit'
    });

    if (item.url) {
      formatted += `\n  来源：${item.source} ${time} [链接](${item.url})`;
    } else {
      formatted += `\n  来源：${item.source} ${time}`;
    }

    formatted += '\n';

    return formatted;
  }

  // 发送消息到Telegram
  private async sendMessage(text: string): Promise<void> {
    if (!this.botToken || !this.chatId) {
      throw new Error('Bot token or chat ID not configured');
    }

    // 截断消息（Telegram消息长度限制4096字符）
    const maxLength = 4000;
    const truncated = text.length > maxLength ? text.substring(0, maxLength) + '...' : text;

    // 使用curl发送消息
    const curlCommand = `curl -s -X POST "https://api.telegram.org/bot${this.botToken}/sendMessage" \\
      -d "chat_id=${this.chatId}" \\
      -d "text=${encodeURIComponent(truncated)}" \\
      -d "parse_mode=Markdown" \\
      -d "disable_web_page_preview=false"`;

    return new Promise((resolve, reject) => {
      exec(curlCommand, (error, stdout, stderr) => {
        if (error) {
          console.error(`[Telegram] curl error: ${error.message}`);
          console.error(`[Telegram] stderr: ${stderr}`);
          reject(error);
          return;
        }

        const response = JSON.parse(stdout);
        if (!response.ok) {
          throw new Error(`Telegram API error: ${response.description}`);
        }

        resolve();
      });
    });
  }

  // 配置Telegram
  configure(chatId: string, botToken: string): void {
    this.chatId = chatId;
    this.botToken = botToken;
    this.enabled = true;
  }

  // 检查是否已配置
  isConfigured(): boolean {
    return this.enabled;
  }

  // TODO: 后续增强
  // 1. 支持消息分段发送
  // 2. 添加图片/文档发送功能
  // 3. 支持HTML格式
  // 4. 添加发送重试机制
  // 5. 支持群组和频道
  // 6. 添加发送状态追踪
  // 7. 支持自定义消息模板
  // 8. 添加消息前缀/后缀配置
}