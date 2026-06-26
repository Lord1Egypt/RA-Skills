import { ZhihuAdapter } from './zhihu.js';
import { BilibiliAdapter } from './bilibili.js';
import { BaijiahaoAdapter } from './baijiahao.js';
import { ToutiaoAdapter } from './toutiao.js';
import { XiaohongshuAdapter } from './xiaohongshu.js';
import { BaseAdapter } from '../lib/base-adapter.js';
import { PlatformName } from '../types/index.js';

export { ZhihuAdapter, BilibiliAdapter, BaijiahaoAdapter, ToutiaoAdapter, XiaohongshuAdapter };

/**
 * 适配器映射表
 */
const adapterMap: Record<PlatformName, () => BaseAdapter> = {
  zhihu: () => new ZhihuAdapter(),
  bilibili: () => new BilibiliAdapter(),
  baijiahao: () => new BaijiahaoAdapter(),
  toutiao: () => new ToutiaoAdapter(),
  xiaohongshu: () => new XiaohongshuAdapter(),
};

/**
 * 获取平台适配器
 */
export function getAdapter(platform: PlatformName): BaseAdapter {
  const createAdapter = adapterMap[platform];
  if (!createAdapter) {
    throw new Error(`Unknown platform: ${platform}`);
  }
  return createAdapter();
}

/**
 * 获取所有平台适配器
 */
export function getAllAdapters(): BaseAdapter[] {
  return Object.values(adapterMap).map(create => create());
}
