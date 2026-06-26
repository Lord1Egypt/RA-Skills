import { BrowserContext, Page } from 'playwright';
import { BaseAdapter } from './base-adapter.js';
import { PlatformConfig, OrderLogistics, LogisticsEvent } from '../types/index.js';

const PDD_CONFIG: PlatformConfig = {
  name: 'pdd',
  baseUrl: 'https://mobile.yangkeduo.com',
  loginUrl: 'https://mobile.yangkeduo.com/login.html',
  orderListUrl: 'https://mobile.yangkeduo.com/orders.html',
  selectors: {
    loginIndicator: '.login-page, .phone-login, [data-testid="login-form"]',
    orderItem: '[data-test="店铺名称"]',
    orderId: '',
    orderTitle: '[data-test="商品名称"]',
    orderStatus: '[data-test="订单状态"]',
    logisticsButton: '',
    trackingNumber: '',
    carrier: '',
    timeline: ''
  }
};

export class PDDAdapter extends BaseAdapter {
  constructor(context: BrowserContext) {
    super(PDD_CONFIG, context);
  }

  getName(): string {
    return '拼多多';
  }

  protected isLoginUrl(url: string): boolean {
    return url.includes('mobile.yangkeduo.com/login') || 
           url.includes('yangkeduo.com/phone_login');
  }

  async isLoggedIn(): Promise<boolean> {
    const page = await this.initPage();
    await page.setViewportSize({ width: 375, height: 812 });
    await page.goto(this.config.orderListUrl, { timeout: 10000 });
    return !(await this.detectLoginPage(page));
  }

  async getOrders(): Promise<OrderLogistics[]> {
    const page = await this.initPage();
    await page.setViewportSize({ width: 375, height: 812 });
    
    await this.safeGoto(this.config.orderListUrl);

    // Wait for order list to render
    await page.waitForTimeout(3000);
    
    // Wait for at least one store name element (indicates orders loaded)
    await page.waitForSelector('[data-test="店铺名称"]', { timeout: 15000 });

    // Extract comprehensive order data
    const orders = await page.evaluate(() => {
      const storeNames = document.querySelectorAll('[data-test="店铺名称"]');
      const orderStatuses = document.querySelectorAll('[data-test="订单状态"]');
      const productNames = document.querySelectorAll('[data-test="商品名称"]');
      const productPrices = document.querySelectorAll('[data-test="商品价格"]');
      
      const results: Array<{
        storeName: string;
        status: string;
        productName: string;
        price: string;
        orderId: string;
      }> = [];
      
      const count = Math.min(storeNames.length, orderStatuses.length);
      for (let i = 0; i < count; i++) {
        const storeEl = storeNames[i];
        const container = storeEl?.closest('[class*="U6SAh0Eo"]') || 
                         storeEl?.closest('div[class]');
        
        const dataAttr = (container as HTMLElement)?.getAttribute('data');
        const orderId = dataAttr ? `pdd-order-${dataAttr}` : `pdd-${i}`;
        
        results.push({
          storeName: storeEl?.textContent?.trim() || '',
          status: orderStatuses[i]?.textContent?.trim() || '',
          productName: productNames[i]?.textContent?.trim() || '',
          price: productPrices[i]?.textContent?.trim() || '',
          orderId: orderId
        });
      }
      
      return results;
    });

    console.log(`Found ${orders.length} orders`);

    // Get logistics for each order, only keep in_transit orders
    const results: OrderLogistics[] = [];
    for (const order of orders) {
      const logistics = await this.getOrderLogisticsFromPage(page, order);
      if (logistics && logistics.status === 'in_transit') {
        results.push(logistics);
      }
    }

    return results;
  }

  async getOrderLogisticsFromPage(page: Page, orderInfo: any): Promise<OrderLogistics | null> {
    try {
      const orderIndex = parseInt(orderInfo.orderId.replace('pdd-order-', ''));
      
      // Find all "更多" (More) buttons
      const moreButtons = await page.locator('text=更多').all();
      
      if (orderIndex >= moreButtons.length) {
        console.log(`No "更多" button for order ${orderInfo.orderId}`);
        return this.createBasicOrder(orderInfo);
      }

      // Click the "更多" button using JavaScript to avoid viewport issues
      const moreBtn = moreButtons[orderIndex];
      await moreBtn.evaluate(el => el.scrollIntoView({ behavior: 'instant', block: 'center' }));
      await page.waitForTimeout(300);
      await moreBtn.evaluate(el => (el as HTMLElement).click());
      await page.waitForTimeout(800);

      // Look for "查看物流" option in the popup
      const logisticsOption = page.locator('text=查看物流').first();
      
      if (!(await logisticsOption.isVisible().catch(() => false))) {
        console.log(`No "查看物流" option for order ${orderInfo.orderId}`);
        // Close popup by pressing Escape
        await page.keyboard.press('Escape').catch(() => {});
        await page.waitForTimeout(300);
        return this.createBasicOrder(orderInfo);
      }

      // Click "查看物流" using JavaScript
      await logisticsOption.evaluate(el => el.scrollIntoView({ behavior: 'instant', block: 'center' }));
      await page.waitForTimeout(200);
      await logisticsOption.evaluate(el => (el as HTMLElement).click());
      
      // Wait for logistics page to load
      await page.waitForTimeout(2000);

      // Extract logistics data from the logistics page
      const logisticsData = await page.evaluate(() => {
        const data: {
          trackingNumber: string;
          carrier: string;
          timeline: LogisticsEvent[];
          latestUpdate: string;
        } = {
          trackingNumber: '',
          carrier: '拼多多物流',
          timeline: [],
          latestUpdate: ''
        };

        // Try to find tracking number and carrier
        const pageText = document.body.innerText;
        
        // Common Chinese courier patterns
        const courierPatterns = [
          { name: '顺丰', regex: /顺丰[速快]?运?[:\s]*(SF\d{12,})/i },
          { name: '中通', regex: /中通[快]?递?[:\s]*(ZT\d{12,}|7\d{13}|5\d{13})/i },
          { name: '圆通', regex: /圆通[快]?递?[:\s]*(YT\d{12,})/i },
          { name: '申通', regex: /申通[快]?递?[:\s]*(ST\d{12,}|77\d{11})/i },
          { name: '韵达', regex: /韵达[快]?递?[:\s]*(YD\d{12,}|31\d{13})/i },
          { name: '京东', regex: /京东[快]?递?[:\s]*(JD\d{12,}|JDVA\d{10,})/i },
          { name: '邮政', regex: /邮政|EMS[:\s]*(E[MS]\d{9,}CN|\d{13})/i },
          { name: '极兔', regex: /极兔[快]?递?[:\s]*(JT\d{12,})/i },
          { name: '德邦', regex: /德邦[快]?递?[:\s]*(DPK\d{10,})/i }
        ];

        for (const courier of courierPatterns) {
          const match = pageText.match(courier.regex);
          if (match) {
            data.carrier = courier.name;
            data.trackingNumber = match[1];
            break;
          }
        }

        // If no specific pattern matched, try generic tracking number pattern
        if (!data.trackingNumber) {
          const genericMatch = pageText.match(/[运单号快递单号][:：\s]*(\d{10,20})/);
          if (genericMatch) {
            data.trackingNumber = genericMatch[1];
          }
        }

        // Try to find timeline items
        const timelineSelectors = [
          '[class*="timeline"]',
          '[class*="logistics"]',
          '.tracking-item',
          '[class*="route"]',
          '[class*="node"]'
        ];

        for (const selector of timelineSelectors) {
          const items = document.querySelectorAll(selector);
          if (items.length > 0) {
            items.forEach((item, index) => {
              const text = item.textContent || '';
              // Try to extract time
              const timeMatch = text.match(/(\d{4}[/-]\d{2}[/-]\d{2}[\s\d:]*)|(\d{2}:\d{2})/);
              const time = timeMatch ? timeMatch[0] : '';
              
              // Clean up the description
              const description = text.replace(/\s+/g, ' ').trim();
              
              if (description && description.length > 5) {
                data.timeline.push({
                  time,
                  location: '',
                  status: index === 0 ? 'latest' : 'history',
                  description
                });
              }
            });
            break;
          }
        }

        // If still no timeline, try to get any logistics-related text
        if (data.timeline.length === 0) {
          const logisticsSections = document.querySelectorAll('[class*="logistics"], [class*="express"], [class*="delivery"]');
          logisticsSections.forEach(section => {
            const text = section.textContent?.trim();
            if (text && text.length > 10) {
              data.timeline.push({
                time: '',
                location: '',
                status: 'info',
                description: text.substring(0, 200)
              });
            }
          });
        }

        data.latestUpdate = data.timeline[0]?.description || '';
        return data;
      });

      // Go back to order list
      await page.goBack();
      await page.waitForTimeout(1500);
      
      // Ensure we're back on the orders page and it's fully loaded
      await page.waitForSelector('[data-test="店铺名称"]', { timeout: 10000 });

      return {
        platform: 'pdd',
        orderId: orderInfo.orderId,
        orderTitle: orderInfo.productName,
        trackingNumber: logisticsData.trackingNumber,
        carrier: logisticsData.carrier,
        status: logisticsData.timeline.length > 0 ? 'in_transit' : this.parseStatus(orderInfo.status),
        timeline: logisticsData.timeline,
        latestUpdate: logisticsData.latestUpdate
      };
    } catch (error) {
      console.error(`Failed to get logistics for PDD order ${orderInfo.orderId}:`, error);
      // Try to go back even if failed
      try {
        await page.goBack();
        await page.waitForTimeout(1000);
      } catch {}
      return this.createBasicOrder(orderInfo);
    }
  }

  createBasicOrder(orderInfo: any): OrderLogistics {
    return {
      platform: 'pdd',
      orderId: orderInfo.orderId,
      orderTitle: orderInfo.productName,
      trackingNumber: '',
      carrier: '拼多多物流',
      status: this.parseStatus(orderInfo.status),
      timeline: [{
        time: new Date().toISOString(),
        location: '',
        status: orderInfo.status,
        description: `${orderInfo.storeName} - ${orderInfo.productName} (${orderInfo.price})`
      }],
      latestUpdate: orderInfo.status
    };
  }

  protected parseStatus(statusText: string): string {
    const status = statusText.toLowerCase();
    if (status.includes('待发货') || status.includes('待成团')) return 'pending';
    if (status.includes('待收货') || status.includes('运输中')) return 'shipped';
    if (status.includes('已签收') || status.includes('交易成功')) return 'delivered';
    if (status.includes('退款') || status.includes('售后')) return 'exception';
    return 'pending';
  }

  async getOrderLogistics(orderId: string): Promise<OrderLogistics | null> {
    return null;
  }
}