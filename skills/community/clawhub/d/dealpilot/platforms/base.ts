// 平台适配器基类
// 所有平台适配器需实现 PlatformAdapter 接口

import type { Platform, PlatformTraits } from "../engine/types";

export interface PlatformAdapter {
  platform: Platform;
  search(query: string, options?: any): Promise<any[]>;
  getProductDetail(url: string): Promise<any>;
  calcFinalPrice(product: any): Promise<any>;
  assessSeller(url: string): Promise<any>;
  getPlatformTraits(): PlatformTraits;
}

export abstract class BaseAdapter implements PlatformAdapter {
  abstract platform: Platform;

  async search(query: string, options?: any): Promise<any[]> {
    throw new Error("STUB: 实现平台搜索");
  }

  async getProductDetail(url: string): Promise<any> {
    throw new Error("STUB: 实现商品详情获取");
  }

  async calcFinalPrice(product: any): Promise<any> {
    throw new Error("STUB: 实现最终价格计算");
  }

  async assessSeller(url: string): Promise<any> {
    throw new Error("STUB: 实现卖家风险评估");
  }

  getPlatformTraits(): PlatformTraits {
    return {
      strength: [],
      weakness: [],
      bestFor: [],
      worstFor: [],
    };
  }
}
