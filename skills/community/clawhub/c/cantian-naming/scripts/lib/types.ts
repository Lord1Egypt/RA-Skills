export type Wuxing = "金" | "木" | "水" | "火" | "土";

export type WugeRelation = "同" | "生" | "克" | "泄" | "耗";
export type WugeRelationDirection = "同" | "我生" | "生我" | "我克" | "克我";

export type GeResult = {
  number: number;
  luck: string;
  wuxing: Wuxing;
};

export type HanziRecord = {
  simplified: string;
  kangxi?: string;
  pinyin: string[];
  radical: string;
  strokeCount: number;
  wugeStrokeCount: number;
  level: 1 | 2 | 3;
  element?: Wuxing;
};
