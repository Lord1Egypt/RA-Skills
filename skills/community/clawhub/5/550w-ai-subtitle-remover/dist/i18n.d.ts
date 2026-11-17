export type SupportedLocale = "zh" | "en";
export type ServiceRegion = "domestic" | "global";
export declare function resolveLocale(value?: unknown): SupportedLocale;
export declare function localize(locale: unknown, zh: string, en: string): string;
export declare function resolveGlobalApiLocale(value?: unknown): string;
export declare function resolveServiceRegion(value?: unknown, locale?: unknown): ServiceRegion;
export declare function credentialApplyUrl(locale?: unknown, region?: unknown): string;
export declare function globalPolicyUrl(page: "privacy" | "terms", locale?: unknown): string;
