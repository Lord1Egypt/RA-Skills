// 一号店平台适配器

import { BaseAdapter } from "./base";
import type { PlatformTraits } from "../engine/types";

export class YhdAdapter extends BaseAdapter {
  platform = "yhd" as const;

  getPlatformTraits(): PlatformTraits {
    return {
      strength: ["日常用品价格稳定", "物流较快"],
      weakness: ["品类有限", "知名度不如主流平台"],
      bestFor: ["日常用品", "食品", "快消品"],
      worstFor: ["电子产品", "服装", "非标品"],
    };
  }
}
