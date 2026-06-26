"use strict";
// 配置文件：免费额度、定价、版本信息
Object.defineProperty(exports, "__esModule", { value: true });
exports.UPGRADE_MESSAGES = exports.PURCHASE_URL = exports.DEVICE_ID_KEY = exports.SUBSCRIPTION_KEY = exports.MCP_CONFIG = exports.PRICING = exports.VERSION = void 0;
exports.VERSION = '1.0.0';
exports.PRICING = {
    free: {
        name: '免费版',
        quota: 10, // 免费10次
        period: '永久',
    },
    basic: {
        name: '基础版',
        price: 9.9, // 元/月
        quota: 500, // 500次/月
        period: '月',
    },
    pro: {
        name: 'Pro版',
        price: 29.9, // 元/月
        quota: Infinity, // 无限次
        period: '月',
    },
};
exports.MCP_CONFIG = {
    name: 'douyindownload',
    displayName: '抖音视频解析',
    description: '去水印解析抖音视频，返回无水印下载地址',
    version: exports.VERSION,
};
exports.SUBSCRIPTION_KEY = 'DOUYIN_SUBSCRIPTION_KEY';
exports.DEVICE_ID_KEY = 'DOUYIN_DEVICE_ID';
// 提示文案
exports.PURCHASE_URL = 'https://mcppay.fushangsong.cc/';
exports.UPGRADE_MESSAGES = {
    quotaExceeded: (left, total) => `⚠️ 免费次数已用完（${left}/${total}）\n\n` +
        `💎 基础版：${exports.PRICING.basic.price}元/月 = 500次\n` +
        `🚀 Pro版：${exports.PRICING.pro.price}元/月 = 无限次\n\n` +
        `👉 点击购买：${exports.PURCHASE_URL}\n\n` +
        `购买后输入激活码即可解锁`,
    invalidKey: () => `❌ 授权码无效或已过期\n\n` +
        `请到 ${exports.PURCHASE_URL} 购买获取有效激活码`,
    expiredKey: () => `⏰ 授权码已过期\n\n` +
        `请到 ${exports.PURCHASE_URL} 续费获取新激活码`,
    noKey: () => `🔑 尚未激活\n\n` +
        `您当前使用的是免费版本，功能受限。\n\n` +
        `💎 基础版：${exports.PRICING.basic.price}元/月 = 500次/月\n` +
        `🚀 Pro版：${exports.PRICING.pro.price}元/月 = 无限次\n\n` +
        `👉 点击购买：${exports.PURCHASE_URL}`,
    success: (left, plan) => `✅ 授权码验证成功\n\n` +
        `📦 当前套餐：${plan}\n` +
        `📊 剩余次数：${left === Infinity ? '无限' : left}`,
};
//# sourceMappingURL=config.js.map