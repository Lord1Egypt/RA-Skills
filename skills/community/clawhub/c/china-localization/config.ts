/**
 * 安全配置文件 - 使用环境变量而非硬编码
 * 
 * 所有敏感信息都应该通过环境变量提供
 */

// Tavily API 配置
export const TAVILY_CONFIG = {
  apiKey: process.env.TAVILY_API_KEY || '',
  apiUrl: 'https://api.tavily.com/search',
};

// 飞书集成配置
export const FEISHU_CONFIG = {
  enabled: process.env.FEISHU_ENABLED === 'true',
  appId: process.env.FEISHU_APP_ID || '',
  appSecret: process.env.FEISHU_APP_SECRET || '',
  userAccessToken: process.env.FEISHU_USER_ACCESS_TOKEN || '',
};

// 微信集成配置
export const WECHAT_CONFIG = {
  enabled: process.env.WECHAT_ENABLED === 'true',
  appId: process.env.WECHAT_APP_ID || '',
  appSecret: process.env.WECHAT_APP_SECRET || '',
};

// 钉钉集成配置
export const DINGTALK_CONFIG = {
  enabled: process.env.DINGTALK_ENABLED === 'true',
  webhook: process.env.DINGTALK_WEBHOOK || '',
  appKey: process.env.DINGTALK_APP_KEY || '',
  appSecret: process.env.DINGTALK_APP_SECRET || '',
};

// 高德地图配置
export const AMAP_CONFIG = {
  enabled: process.env.AMAP_ENABLED === 'true',
  apiKey: process.env.AMAP_API_KEY || '',
};

// 支付宝配置
export const ALIPAY_CONFIG = {
  enabled: process.env.ALIPAY_ENABLED === 'true',
  appId: process.env.ALIPAY_APP_ID || '',
  privateKey: process.env.ALIPAY_PRIVATE_KEY || '',
  alipayPublicKey: process.env.ALIPAY_PUBLIC_KEY || '',
  sandbox: process.env.ALIPAY_SANDBOX === 'true' || true,
};