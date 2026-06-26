// 拼多多平台适配器
// 预留接驳现有 pdd-shopping skill

import { BaseAdapter } from "./base";
import type { PlatformTraits } from "../engine/types";

export class PddAdapter extends BaseAdapter {
  platform = "pdd" as const;

  getPlatformTraits(): PlatformTraits {
    return {
      strength: ["价格最低", "百亿补贴", "拼团优惠"],
      weakness: ["物流慢", "售后弱", "假货风险较高"],
      bestFor: ["标准品", "低价日用品", "愿意等待"],
      worstFor: ["电子产品", "奢侈品", "急需品", "礼品"],
    };
  }

  // TODO: 接入现有 pdd-shopping skill 的搜索和百亿补贴检查能力
  // import { pddSearch, checkSubsidy } from "~/pdd-shopping/scripts";
}
