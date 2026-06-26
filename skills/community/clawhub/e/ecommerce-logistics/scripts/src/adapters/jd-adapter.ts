import { BrowserContext } from 'playwright';
import { BaseAdapter } from './base-adapter.js';
import { PlatformConfig, OrderLogistics, LogisticsEvent } from '../types/index.js';

const JD_CONFIG: PlatformConfig = {
  name: 'jd',
  baseUrl: 'https://www.jd.com',
  loginUrl: 'https://passport.jd.com/login.aspx',
  orderListUrl: 'https://order.jd.com/center/list.action',
  selectors: {
    loginIndicator: '.login-tab, .login-form, #loginname',
    orderItem: '.order-item, .order-list-item',
    orderId: '.order-number, .o-number',
    orderTitle: '.p-name a, .goods-name',
    orderStatus: '.order-status, .o-status',
    logisticsButton: '.view-logistics, .btn-logistics',
    trackingNumber: '.logistics-num, .waybill-num',
    carrier: '.logistics-company, .carrier',
    timeline: '.logistics-list li, .delivery-list li'
  }
};

export class JDAdapter extends BaseAdapter {
  constructor(context: BrowserContext) {
    super(JD_CONFIG, context);
  }

  getName(): string {
    return '京东';
  }

  protected isLoginUrl(url: string): boolean {
    return url.includes('passport.jd.com') || 
           url.includes('passport.jd.hk') ||
           url.includes('login.jd.com');
  }

  async isLoggedIn(): Promise<boolean> {
    const page = await this.initPage();
    // Add extra headers for JD
    await page.setExtraHTTPHeaders({
      'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
      'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
      'Cache-Control': 'max-age=0'
    });
    await page.goto(this.config.orderListUrl, { timeout: 10000, waitUntil: 'domcontentloaded' });
    // Wait a bit for any redirects
    await page.waitForTimeout(2000);
    return !(await this.detectLoginPage(page));
  }

  async getOrders(): Promise<OrderLogistics[]> {
    await this.safeGoto(this.config.orderListUrl);
    const page = await this.initPage();

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
      
      // JD logistics page
      const logisticsUrl = `https://order.jd.com/lazy/getOrderLogisticsInfo.action?orderId=${orderId}`;
      await this.safeGoto(logisticsUrl, { timeout: 15000 });

      const data = await page.evaluate((selectors) => {
        const trackingEl = document.querySelector(selectors.trackingNumber);
        const carrierEl = document.querySelector(selectors.carrier);
        const timelineEls = document.querySelectorAll(selectors.timeline);

        const timeline: LogisticsEvent[] = Array.from(timelineEls).map(el => ({
          time: el.querySelector('.time')?.textContent?.trim() || 
                el.querySelector('.date')?.textContent?.trim() || '',
          location: el.querySelector('.location')?.textContent?.trim() || '',
          status: el.querySelector('.status')?.textContent?.trim() || '',
          description: el.textContent?.trim() || ''
        }));

        return {
          trackingNumber: trackingEl?.textContent?.replace(/[^\w]/g, '') || '',
          carrier: carrierEl?.textContent?.trim() || '京东物流',
          timeline,
          latestUpdate: timeline[0]?.time || ''
        };
      }, this.config.selectors);

      return {
        platform: 'jd',
        orderId,
        trackingNumber: data.trackingNumber,
        carrier: data.carrier,
        status: this.parseStatus(data.timeline[0]?.status || ''),
        timeline: data.timeline,
        latestUpdate: data.latestUpdate
      };
    } catch (error) {
      console.error(`Failed to get logistics for JD order ${orderId}:`, error);
      return null;
    }
  }
}