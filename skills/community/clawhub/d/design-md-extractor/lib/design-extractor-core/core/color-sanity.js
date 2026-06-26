"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.collectColorWarnings = collectColorWarnings;
const color_normalization_1 = require("./color-normalization");
function collectColorWarnings(colors) {
    const issues = [];
    if (colors.primary.value && (0, color_normalization_1.isNeutralColor)(colors.primary.value)) {
        issues.push({
            severity: 'warning',
            role: 'primary',
            message: 'Primary color is neutral; review CTA, link, active, and brand evidence.',
        });
    }
    if (colors.textPrimary.value && colors.background.value && (0, color_normalization_1.contrastRatio)(colors.textPrimary.value, colors.background.value) < 3) {
        issues.push({
            severity: 'critical',
            role: 'textPrimary',
            message: 'Text primary has low contrast against the inferred page background.',
        });
    }
    if (!colors.border) {
        issues.push({
            severity: 'info',
            role: 'border',
            message: 'No border color evidence was found.',
        });
    }
    return issues;
}