export interface LogisticsEvent {
  time: string;
  location: string;
  status: string;
  description: string;
}

export interface OrderLogistics {
  platform: Platform;
  orderId: string;
  orderTitle?: string;
  trackingNumber: string;
  carrier: string;
  status: LogisticsStatus;
  timeline: LogisticsEvent[];
  latestUpdate: string;
  createdAt?: string;
  price?: string;
}

export type Platform = 'taobao' | 'jd' | 'pdd' | 'douyin';

export type LogisticsStatus = 
  | 'pending'      // 待发货
  | 'shipped'      // 已发货
  | 'in_transit'   // 运输中
  | 'out_for_delivery' // 派送中
  | 'delivered'    // 已签收
  | 'exception'    // 异常
  | 'cancelled';   // 已取消

export interface PlatformConfig {
  name: string;
  baseUrl: string;
  loginUrl: string;
  orderListUrl: string;
  selectors: {
    loginIndicator: string;
    orderItem: string;
    orderId: string;
    orderTitle: string;
    orderStatus: string;
    logisticsButton: string;
    trackingNumber: string;
    carrier: string;
    timeline: string;
  };
}

export interface AuthState {
  cookies: any[];
  lastRefreshed: number;
  expiresAt?: number;
}

export interface QueryOptions {
  platform?: Platform | 'all';
  dataDir: string;
  headless?: boolean;
  timeout?: number;
}

export interface RateLimitConfig {
  maxRequests: number;
  windowMs: number;
}