"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.detectDesignSystem = detectDesignSystem;
const candidates = [
    {
        id: 'shadcn',
        label: 'shadcn/ui',
        cssVariablePatterns: [
            /^--background$/,
            /^--foreground$/,
            /^--primary$/,
            /^--primary-foreground$/,
            /^--secondary$/,
            /^--muted$/,
            /^--accent$/,
            /^--destructive$/,
            /^--border$/,
            /^--input$/,
            /^--ring$/,
            /^--radius$/,
        ],
        classPatterns: [
            /\bbg-background\b/,
            /\btext-foreground\b/,
            /\bborder-input\b/,
            /\bdata-\[state=/,
            /\bring-offset-background\b/,
        ],
    },
    {
        id: 'bootstrap',
        label: 'Bootstrap',
        cssVariablePatterns: [/^--bs-/],
        classPatterns: [/\bbtn\b/, /\bbtn-primary\b/, /\bcontainer(?:-\w+)?\b/, /\brow\b/, /\bcol(?:-\w+)?-\d+\b/, /\bcard\b/],
    },
    {
        id: 'material',
        label: 'Material Design',
        cssVariablePatterns: [/^--md-sys-/, /^--mdc-/, /^--mat-/],
        classPatterns: [/\bmdc-/, /\bmat-mdc-/, /\bmat-/, /\bMui[A-Za-z]+-root\b/],
    },
    {
        id: 'antd',
        label: 'Ant Design',
        cssVariablePatterns: [/^--ant-/, /^--ant[A-Z]/],
        classPatterns: [/\bant-/, /\bant-btn\b/, /\bant-card\b/, /\bant-input\b/],
    },
    {
        id: 'primer',
        label: 'Primer',
        cssVariablePatterns: [/^--color-/, /^--base-size-/, /^--borderWidth-/],
        classPatterns: [/\bButton\b/, /\bbtn-primary\b/, /\bBox\b/, /\bcolor-bg-/, /\bcolor-fg-/],
    },
];
function detectDesignSystem(input) {
    const cssVariables = input.cssVariables.map((variable) => variable.name);
    const classes = input.layoutSamples.flatMap((sample) => classParts(sample.className));
    const roles = input.layoutSamples.flatMap((sample) => [sample.role, sample.id].filter(isString));
    const scored = candidates
        .map((definition) => scoreCandidate(definition, cssVariables, classes, roles))
        .sort((a, b) => b.score - a.score);
    const best = scored[0];
    if (!best || best.score < 3) {
        return {
            id: 'generic',
            label: 'Generic',
            confidence: 0.1,
            evidence: ['No known design system signature matched'],
        };
    }
    return {
        id: best.definition.id,
        label: best.definition.label,
        confidence: Math.min(0.98, Number((best.score / 8).toFixed(2))),
        evidence: best.evidence.slice(0, 8),
    };
}
function scoreCandidate(definition, cssVariables, classes, roles) {
    const evidence = new Set();
    let score = 0;
    for (const variable of cssVariables) {
        if (!definition.cssVariablePatterns.some((pattern) => pattern.test(variable)))
            continue;
        score += 1;
        evidence.add(`CSS variable ${variable}`);
    }
    for (const className of classes) {
        if (!definition.classPatterns.some((pattern) => pattern.test(className)))
            continue;
        score += 1;
        evidence.add(`class ${className}`);
    }
    for (const role of roles) {
        if (!definition.rolePatterns?.some((pattern) => pattern.test(role)))
            continue;
        score += 1;
        evidence.add(`role/id ${role}`);
    }
    return {
        definition,
        score,
        evidence: Array.from(evidence),
    };
}
function classParts(className) {
    if (!className)
        return [];
    return className.split(/\s+/).filter(Boolean);
}
function isString(value) {
    return typeof value === 'string' && value.length > 0;
}