// 唯品会平台适配器

import { BaseAdapter } from "./base";
import type { PlatformTraits } from "../engine/types";

export class VipAdapter extends BaseAdapter {
  platform = "vip" as const;

  getPlatformTraits(): PlatformTraits {
    return {
      strength: ["品牌特卖", "正品保障", "价格有折扣"],
      weakness: ["品类有限", "需要挑选", "退换不如京东"],
      bestFor: ["品牌服装", "品牌鞋包", "品牌美妆"],
      worstFor: ["电子产品", "日用品", "食品"],
    };
  }
}
