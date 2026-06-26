"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.inferColorRoles = inferColorRoles;
const color_normalization_1 = require("./color-normalization");
function inferColorRoles(tokens) {
    const primary = choosePrimary(tokens);
    const background = best(tokens, scoreBackground);
    const textPrimary = best(tokens, (token) => scoreTextPrimary(token, background?.value));
    const surface = best(tokens.filter((token) => token.value !== background?.value), scoreSurface);
    const textSecondary = best(tokens.filter((token) => token.value !== textPrimary?.value), scoreTextSecondary);
    const border = best(tokens, scoreBorder);
    const primaryForeground = choosePrimaryForeground(primary, tokens);
    const success = best(tokens, (token) => scoreStatus(token, 'success'));
    const warning = best(tokens, (token) => scoreStatus(token, 'warning'));
    const danger = best(tokens, (token) => scoreStatus(token, 'danger'));
    const neutral = best(tokens, scoreNeutral);
    const warnings = buildGlobalWarnings({ primary, background, textPrimary });
    return {
        primary: toRoleToken('primary', primary, 'No primary/action color evidence found.'),
        ...(primaryForeground ? { primaryForeground: toRoleToken('primaryForeground', primaryForeground) } : {}),
        background: toRoleToken('background', background, 'No page background evidence found.'),
        ...(surface ? { surface: toRoleToken('surface', surface) } : {}),
        textPrimary: toRoleToken('textPrimary', textPrimary, 'No primary text color evidence found.'),
        ...(textSecondary ? { textSecondary: toRoleToken('textSecondary', textSecondary) } : {}),
        ...(border ? { border: toRoleToken('border', border) } : {}),
        ...(success ? { success: toRoleToken('success', success) } : {}),
        ...(warning ? { warning: toRoleToken('warning', warning) } : {}),
        ...(danger ? { danger: toRoleToken('danger', danger) } : {}),
        ...(neutral ? { neutral: toRoleToken('neutral', neutral) } : {}),
        warnings,
    };
}
function choosePrimary(tokens) {
    const candidates = tokens
        .map((token) => ({ token, score: scorePrimary(token) }))
        .filter((entry) => entry.score > 0);
    const vivid = candidates.filter((entry) => !(0, color_normalization_1.isNeutralColor)(entry.token.value));
    return (vivid.length ? vivid : candidates).sort((left, right) => right.score - left.score)[0]?.token;
}
function scorePrimary(token) {
    let score = 0;
    for (const evidence of token.evidence) {
        const context = evidenceContext(evidence);
        if (evidence.property === 'backgroundColor' && evidence.tagName === 'button')
            score += 90 + evidence.score;
        if (evidence.property === 'backgroundColor' && evidence.isInteractive)
            score += 42 + evidence.score;
        if (evidence.property === 'borderColor' && evidence.isActiveState)
            score += 36 + evidence.score;
        if (evidence.property === 'color' && evidence.tagName === 'a')
            score += 28 + evidence.score;
        if (evidence.isActionIntent)
            score += 34;
        if (evidence.isActiveState)
            score += 38;
        if (/primary|brand|accent|cta/i.test(context))
            score += 22;
        if (/nav|tab|menu/i.test(context) && evidence.isActiveState)
            score += 16;
    }
    if ((0, color_normalization_1.isNeutralColor)(token.value))
        score -= 45;
    if ((0, color_normalization_1.isNearWhite)(token.value))
        score -= 80;
    score += (0, color_normalization_1.saturationScore)(token.value) * 36;
    return score;
}
function scoreBackground(token) {
    const backgroundEvidence = token.evidence.filter((item) => item.property === 'backgroundColor');
    if (!backgroundEvidence.length)
        return 0;
    let score = 0;
    for (const evidence of backgroundEvidence) {
        if (evidence.tagName === 'body' || evidence.tagName === 'html')
            score += 120;
        if (/main|app|root|page/.test(evidenceContext(evidence)))
            score += 22;
        score += Math.min(Math.sqrt(evidence.rect.width * evidence.rect.height) / 8, 70);
    }
    if ((0, color_normalization_1.isNeutralColor)(token.value))
        score += 16;
    return score;
}
function scoreSurface(token) {
    const backgroundEvidence = token.evidence.filter((item) => item.property === 'backgroundColor');
    if (!backgroundEvidence.length)
        return 0;
    let score = 0;
    for (const evidence of backgroundEvidence) {
        const context = evidenceContext(evidence);
        if (evidence.tagName === 'body' || evidence.tagName === 'html')
            score -= 90;
        if (/card|surface|panel|dialog|main|section|article|input/.test(context))
            score += 24;
        score += Math.min(Math.sqrt(evidence.rect.width * evidence.rect.height) / 18, 28);
    }
    if ((0, color_normalization_1.isNeutralColor)(token.value))
        score += 12;
    return score;
}
function scoreTextPrimary(token, background) {
    const textEvidence = token.evidence.filter((item) => item.property === 'color' && !item.isInteractive);
    if (!textEvidence.length)
        return 0;
    let score = textEvidence.length * 15 + Math.min(token.frequency, 60);
    if ((0, color_normalization_1.isNeutralColor)(token.value))
        score += 18;
    if ((0, color_normalization_1.isDarkColor)(token.value))
        score += 10;
    if (background && (0, color_normalization_1.contrastRatio)(token.value, background) < 3)
        score -= 70;
    score -= token.evidence.filter((item) => item.property === 'backgroundColor').length * 20;
    return score;
}
function scoreTextSecondary(token) {
    const textEvidence = token.evidence.filter((item) => item.property === 'color' && !item.isInteractive);
    if (!textEvidence.length || (!(0, color_normalization_1.isNeutralColor)(token.value) && (0, color_normalization_1.saturationScore)(token.value) > 0.18))
        return 0;
    const luminance = (0, color_normalization_1.relativeLuminance)(token.value);
    return textEvidence.length * 12 + (luminance > 0.1 && luminance < 0.78 ? 20 : 0);
}
function scoreBorder(token) {
    const borderEvidence = token.evidence.filter((item) => item.property === 'borderColor' || item.property === 'outlineColor');
    if (!borderEvidence.length)
        return 0;
    let score = borderEvidence.length * 12;
    if ((0, color_normalization_1.isNeutralColor)(token.value))
        score += 14;
    if ((0, color_normalization_1.relativeLuminance)(token.value) > 0.45)
        score += 10;
    return score;
}
function scoreStatus(token, status) {
    const pattern = {
        success: /success|positive|valid|complete|done|成功|完成/,
        warning: /warning|warn|caution|pending|notice|警告|提醒|待/,
        danger: /danger|error|destructive|invalid|fail|delete|remove|错误|失败|删除|危险/,
    }[status];
    let score = 0;
    for (const evidence of token.evidence) {
        if (pattern.test(evidenceContext(evidence)))
            score += 70 + evidence.score;
    }
    return score;
}
function scoreNeutral(token) {
    if (!(0, color_normalization_1.isNeutralColor)(token.value))
        return 0;
    return token.score;
}
function choosePrimaryForeground(primary, tokens) {
    if (!primary)
        return undefined;
    const foregroundEvidence = primary.evidence.filter((primaryEvidence) => primaryEvidence.property === 'backgroundColor' && primaryEvidence.tagName === 'button');
    if (!foregroundEvidence.length)
        return undefined;
    const textCandidates = tokens.filter((token) => token.evidence.some((evidence) => evidence.property === 'color' &&
        foregroundEvidence.some((primaryEvidence) => sameElement(primaryEvidence, evidence))));
    return textCandidates.sort((left, right) => right.score - left.score)[0];
}
function toRoleToken(role, token, fallbackWarning) {
    if (!token) {
        return {
            value: '#000000',
            confidence: 0,
            evidence: [],
            warnings: fallbackWarning ? [fallbackWarning] : [],
        };
    }
    return {
        value: token.value,
        confidence: confidenceFromScore(scoreForRole(role, token)),
        evidence: token.evidence.slice(0, 5).map(describeEvidence),
        warnings: token.warnings,
    };
}
function scoreForRole(role, token) {
    if (role === 'primary')
        return scorePrimary(token);
    if (role === 'background')
        return scoreBackground(token);
    if (role === 'surface')
        return scoreSurface(token);
    if (role === 'textPrimary')
        return scoreTextPrimary(token);
    if (role === 'textSecondary')
        return scoreTextSecondary(token);
    if (role === 'border')
        return scoreBorder(token);
    if (role === 'success')
        return scoreStatus(token, 'success');
    if (role === 'warning')
        return scoreStatus(token, 'warning');
    if (role === 'danger')
        return scoreStatus(token, 'danger');
    if (role === 'neutral')
        return scoreNeutral(token);
    return token.score;
}
function buildGlobalWarnings(tokens) {
    const warnings = [];
    if (tokens.primary?.value && (0, color_normalization_1.isNeutralColor)(tokens.primary.value)) {
        warnings.push('Primary color is neutral; review action and brand evidence.');
    }
    if (tokens.textPrimary?.value && tokens.background?.value && (0, color_normalization_1.contrastRatio)(tokens.textPrimary.value, tokens.background.value) < 3) {
        warnings.push('Text primary has low contrast against background.');
    }
    return warnings;
}
function best(tokens, scorer) {
    return tokens
        .map((token) => ({ token, score: scorer(token) }))
        .filter((entry) => entry.score > 0)
        .sort((left, right) => right.score - left.score)[0]?.token;
}
function evidenceContext(evidence) {
    return [evidence.tagName, evidence.id, evidence.className, evidence.role, evidence.text].filter(Boolean).join(' ').toLowerCase();
}
function isHashedClass(className) {
    if (className.startsWith('atm_'))
        return true;
    // Matches typical random CSS-in-JS or compiled hashes like "c13cw3wj" or "i1hf2lh8"
    // Length > 5 and contains both a letter and a number
    if (className.length > 5 && /[a-z]/i.test(className) && /[0-9]/.test(className))
        return true;
    // If it's a long random-looking alphanumeric string (length > 8) without standard hyphens/underscores
    if (className.length > 8 && !className.includes('-') && !className.includes('_'))
        return true;
    return false;
}
function simplifyProperty(property) {
    if (property === 'backgroundColor')
        return 'bg';
    if (property === 'color')
        return 'text';
    if (property === 'borderColor')
        return 'border';
    if (property === 'outlineColor')
        return 'outline';
    if (property === 'textDecorationColor')
        return 'deco';
    return property;
}
function describeEvidence(evidence) {
    const prop = simplifyProperty(evidence.property);
    const classes = evidence.className
        ? evidence.className.split(/\s+/).filter(c => !isHashedClass(c)).slice(0, 1)
        : [];
    const selector = [
        evidence.tagName,
        evidence.id ? `#${evidence.id}` : '',
        classes.length ? `.${classes[0]}` : '',
    ]
        .join('')
        .trim();
    const text = evidence.text ? ` "${evidence.text}"` : '';
    return `${prop} on ${selector}${text}`;
}
function sameElement(left, right) {
    return (left.tagName === right.tagName &&
        left.id === right.id &&
        left.className === right.className &&
        left.text === right.text &&
        left.rect.top === right.rect.top &&
        left.rect.left === right.rect.left);
}
function confidenceFromScore(score) {
    return Math.max(0.35, Math.min(0.98, Math.round((score / (score + 22)) * 100) / 100));
}