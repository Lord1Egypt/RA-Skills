export declare const VERSION = "1.0.0";
export declare const PRICING: {
    readonly free: {
        readonly name: "免费版";
        readonly quota: 10;
        readonly period: "永久";
    };
    readonly basic: {
        readonly name: "基础版";
        readonly price: 9.9;
        readonly quota: 500;
        readonly period: "月";
    };
    readonly pro: {
        readonly name: "Pro版";
        readonly price: 29.9;
        readonly quota: number;
        readonly period: "月";
    };
};
export declare const MCP_CONFIG: {
    name: string;
    displayName: string;
    description: string;
    version: string;
};
export declare const SUBSCRIPTION_KEY = "DOUYIN_SUBSCRIPTION_KEY";
export declare const DEVICE_ID_KEY = "DOUYIN_DEVICE_ID";
export declare const PURCHASE_URL = "https://mcppay.fushangsong.cc/";
export declare const UPGRADE_MESSAGES: {
    quotaExceeded: (left: number, total: number) => string;
    invalidKey: () => string;
    expiredKey: () => string;
    noKey: () => string;
    success: (left: number | "\u221E", plan: string) => string;
};
//# sourceMappingURL=config.d.ts.map