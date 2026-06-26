// 京东平台适配器
// 预留接驳现有 jingdong skill

import { BaseAdapter } from "./base";
import type { PlatformTraits } from "../engine/types";

export class JdAdapter extends BaseAdapter {
  platform = "jd" as const;

  getPlatformTraits(): PlatformTraits {
    return {
      strength: ["物流最快", "自营可信", "售后最强"],
      weakness: ["价格最高", "品类不如淘宝全"],
      bestFor: ["电子产品", "急需品", "礼品", "正品要求高的商品"],
      worstFor: ["低价日用品", "非标品"],
    };
  }

  // TODO: 接入现有 jingdong skill 的搜索和自营商品能力
  // import { jdSearch, jdDetail } from "~/jingdong/scripts";
}
