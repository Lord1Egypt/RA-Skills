// 配置文件：免费额度、定价、版本信息

export const VERSION = '1.0.0';

export const PRICING = {
  free: {
    name: '免费版',
    quota: 10,          // 免费10次
    period: '永久',
  },
  basic: {
    name: '基础版',
    price: 9.9,         // 元/月
    quota: 500,         // 500次/月
    period: '月',
  },
  pro: {
    name: 'Pro版',
    price: 29.9,        // 元/月
    quota: Infinity,    // 无限次
    period: '月',
  },
} as const;

export const MCP_CONFIG = {
  name: 'douyindownload',
  displayName: '抖音视频解析',
  description: '去水印解析抖音视频，返回无水印下载地址',
  version: VERSION,
};

export const SUBSCRIPTION_KEY = 'DOUYIN_SUBSCRIPTION_KEY';
export const DEVICE_ID_KEY = 'DOUYIN_DEVICE_ID';

// 提示文案
export const PURCHASE_URL = 'https://mcppay.fushangsong.cc/';

export const UPGRADE_MESSAGES = {
  quotaExceeded: (left: number, total: number) =>
    `⚠️ 免费次数已用完（${left}/${total}）\n\n` +
    `💎 基础版：${PRICING.basic.price}元/月 = 500次\n` +
    `🚀 Pro版：${PRICING.pro.price}元/月 = 无限次\n\n` +
    `👉 点击购买：${PURCHASE_URL}\n\n` +
    `购买后输入激活码即可解锁`,

  invalidKey: () =>
    `❌ 授权码无效或已过期\n\n` +
    `请到 ${PURCHASE_URL} 购买获取有效激活码`,

  expiredKey: () =>
    `⏰ 授权码已过期\n\n` +
    `请到 ${PURCHASE_URL} 续费获取新激活码`,

  noKey: () =>
    `🔑 尚未激活\n\n` +
    `您当前使用的是免费版本，功能受限。\n\n` +
    `💎 基础版：${PRICING.basic.price}元/月 = 500次/月\n` +
    `🚀 Pro版：${PRICING.pro.price}元/月 = 无限次\n\n` +
    `👉 点击购买：${PURCHASE_URL}`,

  success: (left: number | '∞', plan: string) =>
    `✅ 授权码验证成功\n\n` +
    `📦 当前套餐：${plan}\n` +
    `📊 剩余次数：${left === Infinity ? '无限' : left}`,
};