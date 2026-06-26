import { BaseFetcher } from './base';
import { CLSFetcher } from './cls';
import { ITHomeFetcher } from './ithome';
import { Kr36Fetcher } from './36kr';
import { SourceFetcher } from '../types';

// 导出所有fetcher类
export { BaseFetcher, CLSFetcher, ITHomeFetcher, Kr36Fetcher };

// 创建fetcher实例的工厂函数
export function createFetchers(): SourceFetcher[] {
  return [
    new CLSFetcher(),
    new ITHomeFetcher(),
    new Kr36Fetcher()
  ];
}

// TODO: 后续可以添加更多fetcher
// - JiemianFetcher
// - YicaiFetcher
// - ZqrbFetcher
// - XinhuaFetcher
// - GovFetcher
// 等