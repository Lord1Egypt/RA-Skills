"use strict";
var __createBinding = (this && this.__createBinding) || (Object.create ? (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    var desc = Object.getOwnPropertyDescriptor(m, k);
    if (!desc || ("get" in desc ? !m.__esModule : desc.writable || desc.configurable)) {
      desc = { enumerable: true, get: function() { return m[k]; } };
    }
    Object.defineProperty(o, k2, desc);
}) : (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    o[k2] = m[k];
}));
var __setModuleDefault = (this && this.__setModuleDefault) || (Object.create ? (function(o, v) {
    Object.defineProperty(o, "default", { enumerable: true, value: v });
}) : function(o, v) {
    o["default"] = v;
});
var __importStar = (this && this.__importStar) || (function () {
    var ownKeys = function(o) {
        ownKeys = Object.getOwnPropertyNames || function (o) {
            var ar = [];
            for (var k in o) if (Object.prototype.hasOwnProperty.call(o, k)) ar[ar.length] = k;
            return ar;
        };
        return ownKeys(o);
    };
    return function (mod) {
        if (mod && mod.__esModule) return mod;
        var result = {};
        if (mod != null) for (var k = ownKeys(mod), i = 0; i < k.length; i++) if (k[i] !== "default") __createBinding(result, mod, k[i]);
        __setModuleDefault(result, mod);
        return result;
    };
})();
Object.defineProperty(exports, "__esModule", { value: true });
exports.resolveLocale = resolveLocale;
exports.localize = localize;
exports.resolveGlobalApiLocale = resolveGlobalApiLocale;
exports.resolveServiceRegion = resolveServiceRegion;
exports.credentialApplyUrl = credentialApplyUrl;
exports.globalPolicyUrl = globalPolicyUrl;
const fs = __importStar(require("fs"));
const path = __importStar(require("path"));
let distribution;
function packagedDistribution() {
    if (distribution !== undefined)
        return distribution;
    try {
        const value = JSON.parse(fs.readFileSync(path.resolve(__dirname, "../distribution.json"), "utf8"));
        distribution = (value.region === "domestic" || value.region === "global") && typeof value.locale === "string"
            ? { region: value.region, locale: value.locale }
            : null;
    }
    catch {
        distribution = null;
    }
    return distribution;
}
const GLOBAL_API_LOCALES = new Set([
    "zh-Hans", "zh-Hant", "ja", "ko", "es", "es-MX", "fr", "fr-CA", "de", "pt-BR", "pt-PT", "it",
    "ru", "ar", "he", "id", "ms", "nl", "pl", "th", "tr", "uk", "vi", "hi",
]);
const GLOBAL_LOCALE_ALIASES = {
    "es-419": "es-MX",
    pt: "pt-BR",
};
function resolveLocale(value) {
    const packaged = packagedDistribution();
    if (packaged?.region === "domestic")
        return "zh";
    const language = String(value || packaged?.locale || process.env.LC_ALL || process.env.LC_MESSAGES || process.env.LANG || "").toLowerCase();
    return language.startsWith("zh") || language.includes("zh_") || language.includes("zh-") ? "zh" : "en";
}
function localize(locale, zh, en) {
    return resolveLocale(locale) === "zh" ? zh : en;
}
function resolveGlobalApiLocale(value) {
    const raw = String(value || "").trim().replace(/_/g, "-").replace(/\..*$/, "");
    if (!raw)
        return "en";
    const normalized = raw.toLowerCase();
    if (["zh", "zh-cn", "zh-sg", "zh-hans"].includes(normalized))
        return "zh-Hans";
    if (["zh-tw", "zh-hk", "zh-mo", "zh-hant"].includes(normalized))
        return "zh-Hant";
    const exact = [...GLOBAL_API_LOCALES].find((item) => item.toLowerCase() === raw.toLowerCase());
    if (exact)
        return exact;
    const alias = Object.entries(GLOBAL_LOCALE_ALIASES).find(([key]) => key.toLowerCase() === raw.toLowerCase())?.[1];
    if (alias)
        return alias;
    const primary = raw.split("-")[0].toLowerCase();
    return [...GLOBAL_API_LOCALES].find((item) => item.toLowerCase() === primary) || "en";
}
function resolveServiceRegion(value, locale) {
    const packaged = packagedDistribution();
    if (packaged)
        return packaged.region;
    const configured = String(value || process.env.SUBTITLE_REMOVER_REGION || "").trim().toLowerCase();
    if (configured === "domestic" || configured === "cn" || configured === "china")
        return "domestic";
    if (configured === "global" || configured === "overseas" || configured === "international")
        return "global";
    return resolveLocale(locale) === "zh" ? "domestic" : "global";
}
function credentialApplyUrl(locale, region) {
    if (resolveServiceRegion(region, locale) === "domestic")
        return "https://qzm.550wai.cn/api-keys";
    const globalLocale = resolveGlobalApiLocale(locale);
    return globalLocale === "en" ? "https://eraser.550wai.com/api/" : `https://eraser.550wai.com/${globalLocale}/api/`;
}
function globalPolicyUrl(page, locale) {
    const globalLocale = resolveGlobalApiLocale(locale);
    return globalLocale === "en" ? `https://eraser.550wai.com/${page}/` : `https://eraser.550wai.com/${globalLocale}/${page}/`;
}
//# sourceMappingURL=i18n.js.map