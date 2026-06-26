import { BrowserContext } from 'playwright';
import { BaseAdapter } from './base-adapter.js';
import { PlatformConfig, OrderLogistics, LogisticsEvent } from '../types/index.js';

const DOUYIN_CONFIG: PlatformConfig = {
  name: 'douyin',
  baseUrl: 'https://www.douyin.com',
  loginUrl: 'https://sso.douyin.com/login',
  orderListUrl: 'https://www.douyin.com/mall/order',
  selectors: {
    loginIndicator: '.login-container, .scan-login, [data-e2e="login-page"]',
    orderItem: '.order-card, [data-e2e="order-item"]',
    orderId: '.order-id, [data-e2e="order-id"]',
    orderTitle: '.goods-title, [data-e2e="goods-name"]',
    orderStatus: '.order-status, [data-e2e="order-status"]',
    logisticsButton: '.logistics-btn, [data-e2e="view-logistics"]',
    trackingNumber: '.tracking-number, [data-e2e="tracking-no"]',
    carrier: '.carrier, [data-e2e="carrier-name"]',
    timeline: '.logistics-timeline-item, [data-e2e="timeline-item"]'
  }
};

export class DouyinAdapter extends BaseAdapter {
  constructor(context: BrowserContext) {
    super(DOUYIN_CONFIG, context);
  }

  getName(): string {
    return '抖音';
  }

  protected isLoginUrl(url: string): boolean {
    return url.includes('sso.douyin.com') || 
           url.includes('douyin.com/login') ||
           url.includes('sso.douyin.com/login');
  }

  async isLoggedIn(): Promise<boolean> {
    const page = await this.initPage();
    await page.goto(this.config.orderListUrl, { timeout: 10000 });
    return !(await this.detectLoginPage(page));
  }

  async getOrders(): Promise<OrderLogistics[]> {
    await this.safeGoto(this.config.orderListUrl);
    const page = await this.initPage();

    // Debug: take screenshot and save HTML
    await page.waitForTimeout(3000);
    await page.screenshot({ path: '/Users/charles/.ecommerce-logistics/douyin-orders-debug.png', fullPage: true });
    const html = await page.content();
    const fs = await import('fs');
    fs.writeFileSync('/Users/charles/.ecommerce-logistics/douyin-orders-debug.html', html);
    console.log('Debug: Screenshot and HTML saved');

    // Wait for order list
    await page.waitForSelector(this.config.selectors.orderItem, { timeout: 15000 });

    const orders = await page.evaluate((selectors) => {
      const items = document.querySelectorAll(selectors.orderItem);
      return Array.from(items).map(item => {
        const orderIdEl = item.querySelector(selectors.orderId);
        const titleEl = item.querySelector(selectors.orderTitle);
        const statusEl = item.querySelector(selectors.orderStatus);
        
        return {
          orderId: orderIdEl?.textContent?.replace(/[^\d]/g, '') || '',
          title: titleEl?.textContent?.trim() || '',
          status: statusEl?.textContent?.trim() || ''
        };
      });
    }, this.config.selectors);

    const results: OrderLogistics[] = [];
    for (const order of orders.slice(0, 10)) {
      if (order.orderId) {
        const logistics = await this.getOrderLogistics(order.orderId);
        if (logistics) {
          results.push(logistics);
        }
      }
    }

    return results;
  }

  async getOrderLogistics(orderId: string): Promise<OrderLogistics | null> {
    try {
      const page = await this.initPage();
      
      // Douyin logistics page
      const logisticsUrl = `https://www.douyin.com/mall/order/logistics?order_id=${orderId}`;
      await this.safeGoto(logisticsUrl, { timeout: 15000 });

      const data = await page.evaluate((selectors) => {
        const trackingEl = document.querySelector(selectors.trackingNumber);
        const carrierEl = document.querySelector(selectors.carrier);
        const timelineEls = document.querySelectorAll(selectors.timeline);

        const timeline: LogisticsEvent[] = Array.from(timelineEls).map(el => ({
          time: el.querySelector('.time')?.textContent?.trim() || '',
          location: el.querySelector('.location')?.textContent?.trim() || '',
          status: el.querySelector('.status')?.textContent?.trim() || '',
          description: el.textContent?.trim() || ''
        }));

        return {
          trackingNumber: trackingEl?.textContent?.replace(/[^\w]/g, '') || '',
          carrier: carrierEl?.textContent?.trim() || '抖音电商物流',
          timeline,
          latestUpdate: timeline[0]?.time || ''
        };
      }, this.config.selectors);

      return {
        platform: 'douyin',
        orderId,
        trackingNumber: data.trackingNumber,
        carrier: data.carrier,
        status: this.parseStatus(data.timeline[0]?.status || ''),
        timeline: data.timeline,
        latestUpdate: data.latestUpdate
      };
    } catch (error) {
      console.error(`Failed to get logistics for Douyin order ${orderId}:`, error);
      return null;
    }
  }
}