"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.extractColorTokens = extractColorTokens;
exports.hasActionIntent = hasActionIntent;
exports.extractSalientGradientColor = extractSalientGradientColor;
const color_normalization_1 = require("./color-normalization");
const COLOR_PROPERTIES = [
    'color',
    'backgroundColor',
    'borderTopColor',
    'borderRightColor',
    'borderBottomColor',
    'borderLeftColor',
    'outlineColor',
    'textDecorationColor',
];
function extractColorTokens(samples) {
    const grouped = new Map();
    for (const sample of samples) {
        for (const property of COLOR_PROPERTIES) {
            const extracted = extractEvidence(sample, property);
            if (!extracted)
                continue;
            grouped.set(extracted.value, [...(grouped.get(extracted.value) ?? []), extracted]);
        }
    }
    return Array.from(grouped.entries())
        .map(([value, evidence]) => {
        const usage = Array.from(new Set(evidence.map((item) => usageForProperty(item.property))));
        const score = round(evidence.reduce((total, item) => total + item.score, 0) + saturationBonus(value, evidence), 2);
        return {
            value,
            score,
            frequency: evidence.length,
            usage,
            evidence: evidence.sort((left, right) => right.score - left.score),
            warnings: warningsForToken(value, evidence),
        };
    })
        .sort((left, right) => right.score - left.score);
}
function hasActionIntent(value) {
    if (!value)
        return false;
    return /(^|\b)(primary|cta|submit|search|reserve|continue|checkout|buy|start|try|get|sign|join|create|book|subscribe|login|register|order|cart)(\b|$)|搜索|搜|购买|立即购买|马上抢|加入购物车|加购物车|去结算|结算|下单|提交订单|提交|领券|登录|注册|开通|订阅|开始|试用|预约/i.test(value);
}
function extractSalientGradientColor(value) {
    if (!value || value === 'none')
        return undefined;
    const candidates = [
        ...(value.match(/#[0-9a-f]{3,8}\b/gi) ?? []),
        ...(value.match(/rgba?\([^)]+\)/gi) ?? []),
        ...(value.match(/hsla?\([^)]+\)/gi) ?? []),
    ]
        .map((candidate) => (0, color_normalization_1.normalizeColor)(candidate))
        .filter((candidate) => Boolean(candidate));
    return candidates.find((candidate) => !(0, color_normalization_1.isNeutralColor)(candidate)) ?? candidates[0];
}
function extractEvidence(sample, property) {
    const originalValue = property === 'backgroundColor'
        ? extractSalientGradientColor(sample.styles.backgroundImage) ?? sample.styles.backgroundColor
        : sample.styles[property];
    const normalized = (0, color_normalization_1.normalizeColor)(originalValue);
    if (!normalized)
        return undefined;
    const context = sampleContext(sample);
    const isAction = hasActionIntent(context);
    const active = isActiveState(sample, context);
    const interactive = isInteractive(sample, context);
    const scoreInfo = scoreEvidence(sample, property, normalized, {
        isAction,
        active,
        interactive,
        gradient: property === 'backgroundColor' && Boolean(extractSalientGradientColor(sample.styles.backgroundImage)),
    });
    if (scoreInfo.score <= 0)
        return undefined;
    return {
        value: normalized,
        property: collapseBorderProperty(property),
        originalValue,
        tagName: sample.tagName.toLowerCase(),
        ...(sample.id ? { id: sample.id } : {}),
        ...(sample.className ? { className: sample.className } : {}),
        ...(sample.role ? { role: sample.role } : {}),
        ...(sample.text ? { text: sample.text.trim().slice(0, 80) } : {}),
        rect: sample.rect,
        isInteractive: interactive,
        isActionIntent: isAction,
        isActiveState: active,
        isAboveFold: sample.rect.top < 900,
        score: scoreInfo.score,
        weightReason: scoreInfo.reasons,
    };
}
function scoreEvidence(sample, property, value, flags) {
    const tag = sample.tagName.toLowerCase();
    const area = Math.max(0, sample.rect.width * sample.rect.height);
    const sqrtArea = Math.sqrt(area);
    const reasons = [];
    let score = 1;
    if (property === 'color') {
        score += 2;
        reasons.push('text color');
    }
    if (property === 'backgroundColor') {
        score += 2;
        reasons.push('background');
    }
    if (property.startsWith('border')) {
        score += 4;
        reasons.push('border');
    }
    if (property === 'outlineColor') {
        score += 8;
        reasons.push('outline');
    }
    if (property === 'textDecorationColor') {
        score += 4;
        reasons.push('text decoration');
    }
    if ((tag === 'body' || tag === 'html') && property === 'backgroundColor') {
        score += 95;
        reasons.push('body/html background');
    }
    if (tag === 'button' && property === 'backgroundColor') {
        score += 115;
        reasons.push('button background');
    }
    if ((tag === 'a' || sample.role === 'link') && property === 'color') {
        score += 70;
        reasons.push('link color');
    }
    if (flags.active) {
        score += 55;
        reasons.push('active/selected state');
    }
    if (flags.isAction) {
        score += property === 'backgroundColor' ? 40 : 18;
        reasons.push('action intent');
    }
    if (flags.gradient) {
        score += 24;
        reasons.push('gradient color');
    }
    if (tag === 'div' && property === 'backgroundColor') {
        score += 3;
        reasons.push('generic div background');
    }
    if (property === 'color' && !flags.interactive) {
        score += 3;
        reasons.push('generic text');
    }
    if (flags.interactive && property !== 'color') {
        score += 12;
        reasons.push('interactive paint');
    }
    if (sample.rect.top < 900) {
        score += 5;
        reasons.push('above fold');
    }
    score += Math.min(sqrtArea / 25, 20);
    if ((0, color_normalization_1.isNeutralColor)(value) && (property === 'backgroundColor' || property === 'color')) {
        score += 3;
    }
    return { score: round(score, 2), reasons };
}
function isInteractive(sample, context) {
    const tag = sample.tagName.toLowerCase();
    return (['button', 'a', 'input', 'select', 'textarea'].includes(tag) ||
        ['button', 'link', 'tab', 'menuitem'].includes(sample.role ?? '') ||
        /button|btn|link|cta|submit|search|buy|checkout|cart/i.test(context));
}
function isActiveState(sample, context) {
    return Boolean(sample.ariaSelected ||
        sample.ariaCurrent ||
        /\b(active|selected|current|checked|pressed|open)\b|aria-selected|aria-current/i.test(context));
}
function sampleContext(sample) {
    return [sample.tagName, sample.id, sample.className, sample.role, sample.text, sample.ariaCurrent].filter(Boolean).join(' ');
}
function collapseBorderProperty(property) {
    return property.startsWith('border') ? 'borderColor' : property;
}
function usageForProperty(property) {
    if (property === 'color')
        return 'text';
    if (property === 'backgroundColor')
        return 'background';
    if (property === 'outlineColor')
        return 'outline';
    if (property === 'textDecorationColor')
        return 'decoration';
    return 'border';
}
function saturationBonus(value, evidence) {
    if ((0, color_normalization_1.isNeutralColor)(value))
        return 0;
    const hasActionEvidence = evidence.some((item) => item.isActionIntent || item.isInteractive || item.isActiveState);
    return (0, color_normalization_1.saturationScore)(value) * (hasActionEvidence ? 36 : 14);
}
function warningsForToken(value, evidence) {
    const warnings = [];
    if (!value.startsWith('#'))
        warnings.push('Modern or unresolved color format preserved without numeric color analysis.');
    if (evidence.some((item) => item.property === 'backgroundColor' && item.originalValue.includes('gradient'))) {
        warnings.push('Extracted from gradient; review adjacent stops before treating as official.');
    }
    return warnings;
}
function round(value, precision) {
    const multiplier = 10 ** precision;
    return Math.round(value * multiplier) / multiplier;
}