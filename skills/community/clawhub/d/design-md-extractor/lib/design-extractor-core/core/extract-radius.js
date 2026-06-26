"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.extractRadiusTokens = extractRadiusTokens;
const RADIUS_PROPERTIES = ['borderTopLeftRadius', 'borderTopRightRadius', 'borderBottomRightRadius', 'borderBottomLeftRadius'];
function extractRadiusTokens(samples) {
    const { values, fullValues } = clusterRadiusValues(samples);
    return {
        values,
        scale: inferRadiusScale(values, fullValues),
    };
}
function clusterRadiusValues(samples) {
    const grouped = new Map();
    for (const sample of samples) {
        for (const property of RADIUS_PROPERTIES) {
            const value = parseRadiusValue(sample.styles[property] || sample.styles.borderRadius || '', sample);
            if (value === undefined)
                continue;
            const existing = grouped.get(value) ?? {
                usage: new Set(),
                evidence: [],
                frequency: 0,
                fullFrequency: 0,
                regularFrequency: 0,
            };
            existing.usage.add(property);
            existing.frequency += 1;
            if (isFullRadius(value, sample)) {
                existing.fullFrequency += 1;
            }
            else {
                existing.regularFrequency += 1;
            }
            if (existing.evidence.length < 5)
                existing.evidence.push(`${describeSample(sample)} ${property}`);
            grouped.set(value, existing);
        }
    }
    return {
        values: Array.from(grouped.entries())
            .map(([value, item]) => ({
            value,
            frequency: item.frequency,
            usage: Array.from(item.usage),
            evidence: item.evidence,
        }))
            .sort((left, right) => left.value - right.value),
        fullValues: new Set(Array.from(grouped.entries())
            .filter(([, item]) => item.fullFrequency > item.regularFrequency)
            .map(([value]) => value)),
    };
}
function inferRadiusScale(values, fullValues) {
    const nonFull = values.filter((token) => token.value > 0 && !fullValues.has(token.value)).sort((left, right) => left.value - right.value);
    const full = values
        .filter((token) => fullValues.has(token.value))
        .sort((left, right) => right.frequency - left.frequency || right.value - left.value)[0];
    return {
        sm: nearest(nonFull, 4) ?? nonFull[0],
        md: nearest(nonFull, 8) ?? nonFull[1] ?? nonFull[0],
        lg: nearest(nonFull, 16) ?? nonFull[2] ?? nonFull.at(-1),
        xl: nearest(nonFull, 24) ?? nonFull[3] ?? nonFull.at(-1),
        ...(full ? { full } : {}),
    };
}
function nearest(values, target) {
    return values
        .filter((token) => Math.abs(token.value - target) <= Math.max(2, target * 0.25))
        .sort((left, right) => Math.abs(left.value - target) - Math.abs(right.value - target) || right.frequency - left.frequency)[0];
}
function parseRadiusValue(value, sample) {
    const normalized = value.trim().toLowerCase();
    if (!normalized || normalized === '0px' || normalized === 'none')
        return undefined;
    if (normalized.endsWith('%')) {
        const percent = Number(normalized.slice(0, -1));
        if (!Number.isFinite(percent) || percent <= 0)
            return undefined;
        return percent >= 50 ? 9999 : round((Math.min(sample.rect.width, sample.rect.height) * percent) / 100, 2);
    }
    const match = normalized.match(/^(\d*\.?\d+)px$/);
    if (!match)
        return undefined;
    const parsed = Number(match[1]);
    if (!Number.isFinite(parsed) || parsed <= 0)
        return undefined;
    return round(parsed, 2);
}
function isFullRadius(value, sample) {
    const shortSide = Math.min(sample.rect.width, sample.rect.height);
    return value >= 999 || (value >= 64 && shortSide > 0 && value >= shortSide / 2);
}
function describeSample(sample) {
    return [sample.tagName.toLowerCase(), sample.id ? `#${sample.id}` : '', sample.className ? `.${sample.className}` : '']
        .filter(Boolean)
        .join('');
}
function round(value, precision) {
    const multiplier = 10 ** precision;
    return Math.round(value * multiplier) / multiplier;
}