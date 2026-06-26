import { BrowserContext, Page } from 'playwright';
import { BaseAdapter } from './base-adapter.js';
import { PlatformConfig, OrderLogistics, LogisticsEvent } from '../types/index.js';

const TAOBAO_CONFIG: PlatformConfig = {
  name: 'taobao',
  baseUrl: 'https://www.taobao.com',
  loginUrl: 'https://login.taobao.com',
  orderListUrl: 'https://buyertrade.taobao.com/trade/itemlist/list_bought_items.htm',
  selectors: {
    loginIndicator: '.login-box, #J_Quick2Static, .login-form, .login-page',
    orderItem: '',
    orderId: '',
    orderTitle: '',
    orderStatus: '',
    logisticsButton: '',
    trackingNumber: '',
    carrier: '',
    timeline: ''
  }
};

export class TaobaoAdapter extends BaseAdapter {
  constructor(context: BrowserContext) {
    super(TAOBAO_CONFIG, context);
  }

  getName(): string {
    return '淘宝';
  }

  protected isLoginUrl(url: string): boolean {
    return url.includes('login.taobao.com') || 
           url.includes('login.m.taobao.com') ||
           url.includes('login.alibaba.com');
  }

  async isLoggedIn(): Promise<boolean> {
    const page = await this.initPage();
    await page.goto(this.config.orderListUrl, { timeout: 10000 });
    const isLoginPage = await this.detectLoginPage(page);
    console.log(`  [DEBUG] Taobao isLoggedIn check - isLoginPage: ${isLoginPage}, URL: ${page.url()}`);
    return !isLoginPage;
  }

  async getOrders(): Promise<OrderLogistics[]> {
    const page = await this.initPage();
    
    await this.safeGoto(this.config.orderListUrl);
    
    // Check if we got redirected to login
    if (await this.detectLoginPage(page)) {
      console.log('  [DEBUG] Redirected to login page, need re-auth');
      throw new Error('LOGIN_REQUIRED');
    }
    
    // Wait for order list to load and scroll to load all
    await page.waitForTimeout(3000);
    await page.evaluate(() => window.scrollBy(0, 1000));
    await page.waitForTimeout(1000);

    // Find all orders with logistics buttons
    const ordersWithLogistics = await page.evaluate(() => {
      const results: Array<{
        orderId: string;
        title: string;
        status: string;
        price: string;
        logisticsIndex: number;
      }> = [];
      
      // Find all "查看物流" text nodes and their containers
      const walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
      let node;
      let logisticsIndex = 0;
      
      while (node = walker.nextNode()) {
        if (!node.textContent?.includes('查看物流')) continue;
        
        // Find the order container
        let container: Element | null = node.parentElement;
        for (let i = 0; i < 10 && container; i++) {
          const text = container.textContent || '';
          if (text.includes('订单号')) {
            break;
          }
          container = container.parentElement;
        }
        
        if (!container) continue;
        
        const containerText = container.textContent || '';
        
        // Extract order ID
        const orderMatch = containerText.match(/订单号[:：]?\s*(\d{10,})/);
        const orderId = orderMatch ? orderMatch[1] : '';
        
        if (!orderId || results.find(r => r.orderId === orderId)) continue;
        
        // Extract title
        let title = '';
        const links = container.querySelectorAll('a');
        for (const link of links) {
          const linkText = link.textContent?.trim() || '';
          if (linkText.length > 10 && 
              !linkText.includes('查看') && 
              !linkText.includes('删除') &&
              !linkText.includes('申请') &&
              !linkText.includes('确认') &&
              !linkText.includes('评价')) {
            title = linkText.replace(/\[交易快照\]/g, '').trim();
            break;
          }
        }
        
        // Extract status
        let status = '';
        if (containerText.includes('交易成功')) status = '交易成功';
        else if (containerText.includes('卖家已发货')) status = '卖家已发货';
        else if (containerText.includes('待发货')) status = '待发货';
        else if (containerText.includes('待收货')) status = '待收货';
        else if (containerText.includes('已发货')) status = '已发货';
        else if (containerText.includes('退款')) status = '退款中';
        
        // Extract price
        const priceMatches = containerText.match(/￥(\d+\.?\d{0,2})/g);
        const price = priceMatches ? priceMatches[0] : '';
        
        results.push({ orderId, title, status, price, logisticsIndex });
        logisticsIndex++;
      }
      
      return results;
    });

    console.log(`Found ${ordersWithLogistics.length} orders with logistics buttons`);

    // Get logistics details for each order
    const results: OrderLogistics[] = [];
    for (const order of ordersWithLogistics.slice(0, 10)) {
      const logistics = await this.getOrderLogistics(order, page);
      if (logistics) {
        results.push(logistics);
      }
    }

    return results;
  }

  async getOrderLogistics(order: any, page: Page): Promise<OrderLogistics | null> {
    try {
      // Click the logistics button
      const clicked = await page.evaluate((index) => {
        const walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
        let node;
        let currentIndex = 0;
        
        while (node = walker.nextNode()) {
          if (!node.textContent?.includes('查看物流')) continue;
          
          if (currentIndex === index) {
            // Find clickable parent
            let el: Element | null = node.parentElement;
            for (let i = 0; i < 5 && el; i++) {
              if (el.tagName === 'A' || el.tagName === 'BUTTON' || el.getAttribute('role') === 'button') {
                (el as HTMLElement).click();
                return true;
              }
              el = el.parentElement;
            }
            // Click parent as fallback
            if (node.parentElement) {
              (node.parentElement as HTMLElement).click();
              return true;
            }
          }
          currentIndex++;
        }
        return false;
      }, order.logisticsIndex);

      if (!clicked) {
        console.log(`Failed to click logistics for order ${order.orderId}`);
        return null;
      }

      // Wait for modal to appear
      await page.waitForTimeout(2000);

      // Extract logistics data
      const data = await page.evaluate(() => {
        const modal = document.querySelector('.next-overlay-wrapper, [class*="modal"], [class*="dialog"]');
        const content = modal?.textContent || document.body.textContent || '';
        
        // Look for tracking info
        let trackingNumber = '';
        let carrier = '';
        
        const patterns = [
          { regex: /(顺丰)[^：]*[：:]\s*(SF\d{12,})/, name: '顺丰' },
          { regex: /(中通)[^：]*[：:]\s*(\d{12,})/, name: '中通' },
          { regex: /(圆通)[^：]*[：:]\s*(YT?\d{12,})/, name: '圆通' },
          { regex: /(申通)[^：]*[：:]\s*(ST?\d{12,})/, name: '申通' },
          { regex: /(韵达)[^：]*[：:]\s*(\d{12,})/, name: '韵达' },
          { regex: /(EMS)[^：]*[：:]\s*(\d{9,})/, name: 'EMS' },
          { regex: /(邮政)[^：]*[：:]\s*(\d{9,})/, name: '邮政' },
          { regex: /(极兔)[^：]*[：:]\s*(JT\d{12,})/, name: '极兔' },
          { regex: /(京东)[^：]*[：:]\s*(JD\d{12,})/, name: '京东' },
          { regex: /运单号[：:]\s*(\d{10,})/, name: '' },
          { regex: /快递单号[：:]\s*(\d{10,})/, name: '' }
        ];
        
        for (const p of patterns) {
          const match = content.match(p.regex);
          if (match) {
            carrier = p.name || match[1] || '未知快递';
            trackingNumber = match[2] || match[1];
            break;
          }
        }
        
        // Extract timeline
        const timeline: LogisticsEvent[] = [];
        const items = document.querySelectorAll('.logistics-item, .tracking-item, [class*="logistics"] [class*="item"], .next-timeline-item');
        
        for (const item of items) {
          const time = item.querySelector('.time, [class*="time"]')?.textContent?.trim() || '';
          const desc = item.textContent?.trim() || '';
          if (desc && desc.length > 5 && !desc.includes('查看物流')) {
            timeline.push({
              time,
              location: '',
              status: timeline.length === 0 ? 'latest' : 'history',
              description: desc.substring(0, 200)
            });
          }
        }

        return { carrier, trackingNumber, timeline };
      });

      // Close modal
      await page.keyboard.press('Escape').catch(() => {});
      await page.waitForTimeout(300);
      await page.mouse.click(10, 10).catch(() => {});
      await page.waitForTimeout(500);

      // Determine status
      let status: string;
      const statusText = order.status.toLowerCase();
      if (statusText.includes('待发货')) status = 'pending';
      else if (statusText.includes('发货') || statusText.includes('运输') || statusText.includes('派送')) status = 'in_transit';
      else if (statusText.includes('成功') || statusText.includes('签收')) status = 'delivered';
      else status = 'pending';

      return {
        platform: 'taobao',
        orderId: order.orderId,
        orderTitle: order.title,
        trackingNumber: data.trackingNumber,
        carrier: data.carrier || '淘宝物流',
        status,
        timeline: data.timeline,
        latestUpdate: data.timeline[0]?.description || order.status
      };
    } catch (error) {
      console.error(`Failed to get logistics for Taobao order ${order.orderId}:`, error);
      return null;
    }
  }

  protected parseStatus(statusText: string): string {
    const status = statusText.toLowerCase();
    if (status.includes('待发货') || status.includes('待付款')) return 'pending';
    if (status.includes('待收货') || status.includes('运输中') || status.includes('已发货') || status.includes('卖家已发货')) return 'shipped';
    if (status.includes('已签收') || status.includes('交易成功') || status.includes('已完成')) return 'delivered';
    if (status.includes('退款') || status.includes('售后')) return 'exception';
    return 'pending';
  }
}