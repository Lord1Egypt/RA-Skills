"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.extractSpacingTokens = extractSpacingTokens;
const SPACING_PROPERTIES = [
    'paddingTop',
    'paddingRight',
    'paddingBottom',
    'paddingLeft',
    'marginTop',
    'marginRight',
    'marginBottom',
    'marginLeft',
    'gap',
    'rowGap',
    'columnGap',
];
function extractSpacingTokens(samples) {
    const values = clusterSpacingValues(samples);
    const baseUnit = inferBaseUnit(values);
    return {
        baseUnit,
        values,
        scale: inferSpacingScale(values),
    };
}
function clusterSpacingValues(samples) {
    const grouped = new Map();
    for (const sample of samples) {
        for (const property of SPACING_PROPERTIES) {
            const value = parseSpacingValue(sample.styles[property]);
            if (value === undefined)
                continue;
            const existing = grouped.get(value) ?? { usage: new Set(), evidence: [], frequency: 0 };
            existing.usage.add(property);
            existing.frequency += 1;
            if (existing.evidence.length < 5)
                existing.evidence.push(`${describeSample(sample)} ${property}`);
            grouped.set(value, existing);
        }
    }
    return Array.from(grouped.entries())
        .map(([value, item]) => ({
        value,
        frequency: item.frequency,
        usage: Array.from(item.usage),
        evidence: item.evidence,
    }))
        .sort((left, right) => left.value - right.value);
}
function inferBaseUnit(values) {
    const total = values.reduce((sum, token) => sum + token.frequency, 0);
    const scoreFor = (candidate) => values.reduce((sum, token) => {
        const remainder = token.value % candidate;
        const distance = Math.min(remainder, candidate - remainder);
        return sum + (distance <= 0.5 ? token.frequency : 0);
    }, 0);
    const score8 = scoreFor(8);
    const score10 = scoreFor(10);
    if (total > 0 && score10 / total >= 0.6 && score10 > score8)
        return 10;
    if (total > 0 && score8 / total >= 0.6)
        return 8;
    return 4;
}
function inferSpacingScale(values) {
    const sorted = values.filter((token) => token.value > 0).sort((left, right) => left.value - right.value);
    const scale = {};
    scale.xs = nearest(sorted, 4) ?? sorted[0];
    scale.sm = nearest(sorted, 8) ?? sorted[1] ?? sorted[0];
    scale.md = nearest(sorted, 16) ?? sorted[2] ?? sorted[0];
    scale.lg = nearest(sorted, 24) ?? sorted[3] ?? sorted.at(-1);
    scale.xl = nearest(sorted, 32) ?? sorted[4] ?? sorted.at(-1);
    return scale;
}
function nearest(values, target) {
    return values
        .filter((token) => Math.abs(token.value - target) <= Math.max(2, target * 0.25))
        .sort((left, right) => Math.abs(left.value - target) - Math.abs(right.value - target) || right.frequency - left.frequency)[0];
}
function parseSpacingValue(value) {
    const normalized = value.trim().toLowerCase();
    if (!normalized || normalized === 'auto' || normalized === 'normal')
        return undefined;
    const match = normalized.match(/^(-?\d*\.?\d+)px$/);
    if (!match)
        return undefined;
    const parsed = Number(match[1]);
    if (!Number.isFinite(parsed) || parsed <= 0 || parsed > 240)
        return undefined;
    return round(parsed, 2);
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