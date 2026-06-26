// 淘宝平台适配器
// 预留接驳现有 taobao skill

import { BaseAdapter } from "./base";
import type { PlatformTraits } from "../engine/types";

export class TaobaoAdapter extends BaseAdapter {
  platform = "taobao" as const;

  getPlatformTraits(): PlatformTraits {
    return {
      strength: ["品类最全", "有旗舰店", "售后相对稳定"],
      weakness: ["价格不是最低", "存在刷单风险"],
      bestFor: ["非标品", "个性化商品", "品牌商品"],
      worstFor: ["低价标准品", "需要快速到手"],
    };
  }

  // TODO: 接入现有 taobao skill 的搜索和详情能力
  // import { taobaoSearch } from "~/taobao/scripts/search";
  // import { taobaoDetail } from "~/taobao/scripts/detail";
}
