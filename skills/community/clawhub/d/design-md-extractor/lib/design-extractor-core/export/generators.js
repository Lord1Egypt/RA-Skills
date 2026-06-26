"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.generateDesignMd = generateDesignMd;
exports.generateCssVariables = generateCssVariables;
exports.generateTailwindConfig = generateTailwindConfig;
exports.generateTokensJson = generateTokensJson;
const colorRoles = [
    'primary',
    'primaryForeground',
    'background',
    'surface',
    'textPrimary',
    'textSecondary',
    'border',
    'success',
    'warning',
    'danger',
    'neutral',
];
const spacingScale = ['xs', 'sm', 'md', 'lg', 'xl'];
const radiusScale = ['sm', 'md', 'lg', 'xl', 'full'];
const shadowScale = ['sm', 'md', 'lg', 'card', 'floating'];
const typographyRoles = ['heading', 'body', 'caption', 'button', 'input'];
const colorLabels = {
    primary: 'Primary',
    primaryForeground: 'Primary foreground',
    background: 'Background',
    surface: 'Surface',
    textPrimary: 'Text primary',
    textSecondary: 'Text secondary',
    border: 'Border',
    success: 'Success',
    warning: 'Warning',
    danger: 'Danger',
    neutral: 'Neutral',
};
const colorVarNames = {
    primary: 'primary',
    primaryForeground: 'primary-foreground',
    background: 'background',
    surface: 'surface',
    textPrimary: 'text-primary',
    textSecondary: 'text-secondary',
    border: 'border',
    success: 'success',
    warning: 'warning',
    danger: 'danger',
    neutral: 'neutral',
};
function generateDesignMd(snapshot) {
    const primaryFont = getPrimaryFontFamily(snapshot);
    const colors = buildDesignColors(snapshot);
    const typography = buildDesignTypography(snapshot, primaryFont);
    const rounded = buildDesignRounded(snapshot);
    const spacing = buildDesignSpacing(snapshot);
    const shadows = shadowEntries(snapshot);
    const components = buildDesignComponents(snapshot, colors, rounded, spacing);
    const designSystem = getDesignSystem(snapshot);
    const description = buildDesignDescription(snapshot, colors, primaryFont);
    const lines = [
        '---',
        'version: alpha',
        'name: extracted-design-system',
        `description: ${quoteYaml(description)}`,
        'source:',
        `  title: ${quoteYaml(snapshot.meta.title || 'Current page')}`,
        `  url: ${quoteYaml(snapshot.meta.url || '')}`,
        `  hostname: ${quoteYaml(snapshot.meta.hostname || 'current-page')}`,
        `  analyzedAt: ${quoteYaml(snapshot.meta.analyzedAt)}`,
        'designSystem:',
        `  id: ${quoteYaml(designSystem.id)}`,
        `  label: ${quoteYaml(designSystem.label)}`,
        `  confidence: ${formatConfidence(designSystem.confidence)}`,
        ...(designSystem.evidence.length
            ? ['  evidence:', ...designSystem.evidence.map((item) => `    - ${quoteYaml(item)}`)]
            : []),
        'confidence:',
        `  primaryColor: ${formatConfidence(snapshot.tokens.colors.primary.confidence)}`,
        `  cssVariablesFound: ${snapshot.raw.cssVariables.length}`,
        `  visibleElementsSampled: ${snapshot.raw.elementCounts.totalVisible}`,
        'colors:',
        ...Object.entries(colors).map(([name, value]) => `  ${name}: ${quoteYaml(value)}`),
        'typography:',
        ...Object.entries(typography).flatMap(([name, token]) => [
            `  ${name}:`,
            `    fontFamily: ${quoteYaml(token.fontFamily)}`,
            `    fontSize: ${formatPx(token.fontSize)}`,
            `    fontWeight: ${token.fontWeight}`,
            `    lineHeight: ${formatLineHeight(token.fontSize, token.lineHeight)}`,
            `    letterSpacing: ${formatPx(token.letterSpacing)}`,
        ]),
        'rounded:',
        ...numberEntries(rounded).map(([name, value]) => `  ${name}: ${formatPx(value)}`),
        'spacing:',
        ...numberEntries(spacing).map(([name, value]) => `  ${name}: ${formatPx(value)}`),
        shadows.length ? 'shadows:' : undefined,
        ...shadows.map(([name, value]) => `  ${name}: ${quoteYaml(value)}`),
        'components:',
        ...Object.entries(components).flatMap(([name, spec]) => componentYamlLines(name, spec)),
        '---',
        '',
        '# DESIGN.md',
        '',
        '## Overview',
        '',
        `${description} Values are extracted locally from the current page and should be treated as a practical design-system starting point, not a hand-authored brand book.`,
        '',
        '## Key Characteristics',
        '',
        `- Primary accent is \`{colors.primary}\` (${colors.primary}); pair it with \`{colors.on-primary}\`.`,
        `- Default canvas is \`{colors.canvas}\` (${colors.canvas}) with primary text \`{colors.ink}\` (${colors.ink}).`,
        `- Main surface token is \`{colors.surface}\` (${colors.surface}); use it for cards, panels, and form controls.`,
        `- Primary font stack is \`${primaryFont}\`; preserve the detected family before introducing new fonts.`,
        `- Design system signal: ${designSystem.label} (${Math.round(designSystem.confidence * 100)}%).`,
        '',
        '## Colors',
        '',
        '### Core Roles',
        `- **Primary** (\`{colors.primary}\` - ${colors.primary}): main CTA, selected state, and high-emphasis accents.`,
        `- **On Primary** (\`{colors.on-primary}\` - ${colors['on-primary']}): text and icons placed on primary surfaces.`,
        `- **Canvas** (\`{colors.canvas}\` - ${colors.canvas}): page background.`,
        `- **Surface** (\`{colors.surface}\` - ${colors.surface}): cards, panels, inputs, menus.`,
        `- **Ink** (\`{colors.ink}\` - ${colors.ink}): headings and primary body text.`,
        `- **Muted** (\`{colors.muted}\` - ${colors.muted}): secondary text, captions, helper copy.`,
        `- **Hairline** (\`{colors.hairline}\` - ${colors.hairline}): borders and dividers.`,
        '',
        '## Typography',
        '',
        '| Token | Size | Weight | Line Height | Letter Spacing | Use |',
        '|---|---:|---:|---:|---:|---|',
        ...Object.entries(typography).map(([name, token]) => `| \`{typography.${name}}\` | ${formatPx(token.fontSize)} | ${token.fontWeight} | ${formatLineHeight(token.fontSize, token.lineHeight)} | ${formatPx(token.letterSpacing)} | ${typographyUse(name)} |`),
        '',
        '## Layout',
        '',
        ...layoutSpacingGuidance(snapshot, spacing),
        '- Prefer centered content with responsive grids; collapse multi-column card grids to one column on narrow screens.',
        '- Keep repeated UI dense and scannable; avoid decorative nested cards unless the source page clearly uses them.',
        '',
        '## Elevation & Shapes',
        '',
        ...roundedGuidance(rounded),
        shadows.length
            ? `- Use \`{shadows.${shadows[0][0]}}\` for extracted elevated surfaces; keep shadows restrained.`
            : '- No strong shadow scale was detected; prefer borders and surface contrast over heavy shadows.',
        '',
        '## Components',
        '',
        ...Object.keys(components).flatMap((name) => componentMarkdownLines(name, components[name])),
        '',
        '## Interaction States',
        '',
        `- Hover: subtly deepen \`{colors.primary}\` surfaces or increase border contrast; do not introduce unrelated hues.`,
        `- Focus: use a visible 2px ring based on \`{colors.primary}\` with a 2px offset.`,
        '- Active: keep the same semantic token pair and add a pressed treatment such as darker background or reduced translate-y.',
        '- Disabled: reduce emphasis with muted text, lower contrast surfaces, and no hover-only affordance.',
        '',
        '## Do',
        '',
        '- Use semantic token references such as `{colors.primary}`, `{spacing.md}`, and `{rounded.lg}`.',
        '- Pair foreground/background tokens intentionally, especially `{colors.primary}` with `{colors.on-primary}`.',
        '- Use component recipes before inventing one-off styling.',
        '- Preserve detected typography scale and spacing rhythm when creating new screens.',
        '',
        '## Do Not',
        '',
        '- Do not hard-code hex values when a token exists.',
        '- Do not apply pill radius to normal cards or panels.',
        '- Do not overuse shadows if the extracted system is mostly flat or border-based.',
        '- Do not introduce AI calls, remote assets, or hidden data collection from this document.',
        '',
        '## Usage Notes',
        '',
        '- Use semantic tokens first; avoid hard-coded colors in new UI.',
        '- Treat extracted values as a starting system and prefer corrected tokens when present.',
        '- Keep interaction states accessible and preserve contrast around primary, text, and border tokens.',
        '',
        '## Known Gaps',
        '',
        '- Hover, active, disabled, and focus states are inferred from static page samples.',
        '- Responsive grid rules are generic defaults unless component evidence was detected.',
        '- Brand voice, illustration style, and motion are not guaranteed unless visible in sampled CSS.',
        '- User corrections should override extracted values.',
    ].filter((line) => line !== undefined);
    return `${lines.join('\n')}\n`;
}
function getDesignSystem(snapshot) {
    return (snapshot.designSystem ?? {
        id: 'generic',
        label: 'Generic',
        confidence: 0.1,
        evidence: ['No known design system signature matched'],
    });
}
function generateCssVariables(snapshot) {
    const lines = [
        ':root {',
        ...colorEntries(snapshot).map(([role, value]) => `  --design-color-${colorVarNames[role]}: ${value};`),
        `  --design-font-family-sans: ${getPrimaryFontFamily(snapshot)};`,
        ...typographyEntries(snapshot).flatMap(([role, token]) => [
            `  --design-font-size-${role}: ${formatPx(token.fontSize)};`,
            `  --design-line-height-${role}: ${formatPx(token.lineHeight)};`,
            `  --design-font-weight-${role}: ${token.fontWeight};`,
            `  --design-letter-spacing-${role}: ${formatPx(token.letterSpacing)};`,
        ]),
        ...spacingEntries(snapshot).map(([name, value]) => `  --design-spacing-${name}: ${formatPx(value)};`),
        ...radiusEntries(snapshot).map(([name, value]) => `  --design-radius-${name}: ${formatPx(value)};`),
        ...shadowEntries(snapshot).map(([name, value]) => `  --design-shadow-${name}: ${value};`),
        '}',
    ];
    return `${lines.join('\n')}\n`;
}
function generateTailwindConfig(snapshot) {
    const colorLines = colorEntries(snapshot).map(([role]) => `        ${camelKey(role)}: 'var(--design-color-${colorVarNames[role]})',`);
    const fontSizeLines = typographyEntries(snapshot).map(([role]) => `        ${role}: ['var(--design-font-size-${role})', { lineHeight: 'var(--design-line-height-${role})', fontWeight: 'var(--design-font-weight-${role})', letterSpacing: 'var(--design-letter-spacing-${role})' }],`);
    const spacingLines = spacingEntries(snapshot).map(([name]) => `        ${name}: 'var(--design-spacing-${name})',`);
    const radiusLines = radiusEntries(snapshot).map(([name]) => `        ${name}: 'var(--design-radius-${name})',`);
    const shadowLines = shadowEntries(snapshot).map(([name]) => `        ${name}: 'var(--design-shadow-${name})',`);
    return [
        '/** @type {import("tailwindcss").Config} */',
        'export default {',
        '  theme: {',
        '    extend: {',
        '      colors: {',
        ...colorLines,
        '      },',
        '      fontFamily: {',
        "        sans: ['var(--design-font-family-sans)'],",
        '      },',
        '      fontSize: {',
        ...fontSizeLines,
        '      },',
        '      spacing: {',
        ...spacingLines,
        '      },',
        '      borderRadius: {',
        ...radiusLines,
        '      },',
        '      boxShadow: {',
        ...shadowLines,
        '      },',
        '    },',
        '  },',
        '};',
        '',
    ].join('\n');
}
function generateTokensJson(snapshot) {
    const tokens = {
        $schema: 'https://design-tokens.github.io/community-group/format/',
        $description: `Design tokens extracted locally from ${snapshot.meta.hostname || snapshot.meta.url || 'current page'}.`,
        color: Object.fromEntries(colorEntries(snapshot).map(([role, value]) => [camelKey(role), dtcgToken('color', value)])),
        typography: Object.fromEntries(typographyEntries(snapshot).map(([role, token]) => [
            role,
            dtcgToken('typography', {
                fontFamily: token.fontFamily,
                fontSize: formatPx(token.fontSize),
                fontWeight: token.fontWeight,
                lineHeight: formatPx(token.lineHeight),
                letterSpacing: formatPx(token.letterSpacing),
            }),
        ])),
        spacing: Object.fromEntries(spacingEntries(snapshot).map(([name, value]) => [name, dtcgToken('dimension', formatPx(value))])),
        radius: Object.fromEntries(radiusEntries(snapshot).map(([name, value]) => [name, dtcgToken('dimension', formatPx(value))])),
        shadow: Object.fromEntries(shadowEntries(snapshot).map(([name, value]) => [name, dtcgToken('shadow', value)])),
    };
    return `${JSON.stringify(tokens, null, 2)}\n`;
}
function colorEntries(snapshot) {
    return colorRoles.flatMap((role) => {
        const token = snapshot.tokens.colors[role];
        return token?.value ? [[role, token.value]] : [];
    });
}
function typographyEntries(snapshot) {
    return typographyRoles.flatMap((role) => {
        const token = snapshot.tokens.typography.roles[role];
        return token ? [[role, token]] : [];
    });
}
function spacingEntries(snapshot) {
    return spacingScale.flatMap((name) => {
        const token = snapshot.tokens.spacing.scale[name];
        return typeof token?.value === 'number' ? [[name, token.value]] : [];
    });
}
function radiusEntries(snapshot) {
    return radiusScale.flatMap((name) => {
        const token = snapshot.tokens.radius.scale[name];
        return typeof token?.value === 'number' ? [[name, token.value]] : [];
    });
}
function shadowEntries(snapshot) {
    return shadowScale.flatMap((name) => {
        const token = snapshot.tokens.shadows.scale[name];
        return token?.value ? [[name, token.value]] : [];
    });
}
function componentHintLines(snapshot) {
    const lines = Object.entries(snapshot.components).flatMap(([kind, candidates]) => {
        const candidate = candidates?.[0];
        if (!candidate)
            return [];
        const styles = [
            candidate.style.backgroundColor && `background ${candidate.style.backgroundColor}`,
            candidate.style.color && `text ${candidate.style.color}`,
            candidate.style.borderRadius && `radius ${candidate.style.borderRadius}`,
            candidate.style.padding && `padding ${candidate.style.padding}`,
            candidate.style.boxShadow && `shadow ${candidate.style.boxShadow}`,
        ].filter(isString);
        return [`- ${kind}: ${styles.length ? styles.join(', ') : 'detected from page components'}`];
    });
    return lines.length ? lines : ['- No component styles were detected with enough confidence.'];
}
function buildDesignColors(snapshot) {
    const colors = snapshot.tokens.colors;
    const primary = colors.primary.value;
    const background = colors.background.value;
    const surface = colors.surface?.value || background;
    const textPrimary = colors.textPrimary.value;
    const textSecondary = colors.textSecondary?.value || textPrimary;
    const border = colors.border?.value || '#E5E7EB';
    return {
        primary,
        'primary-active': colors.primary.value,
        'primary-disabled': colors.neutral?.value || border,
        'on-primary': colors.primaryForeground?.value || '#FFFFFF',
        canvas: background,
        surface,
        'surface-soft': colors.neutral?.value || surface,
        ink: textPrimary,
        body: textPrimary,
        muted: textSecondary,
        hairline: border,
        success: colors.success?.value || '#16A34A',
        warning: colors.warning?.value || '#D97706',
        error: colors.danger?.value || '#DC2626',
    };
}
function buildDesignTypography(snapshot, primaryFont) {
    const heading = snapshot.tokens.typography.roles.heading;
    const body = snapshot.tokens.typography.roles.body;
    const caption = snapshot.tokens.typography.roles.caption;
    const button = snapshot.tokens.typography.roles.button;
    const displaySize = heading ? Math.max(heading.fontSize, 28) : 32;
    const bodySize = body?.fontSize ?? 16;
    const bodyLineHeight = body?.lineHeight ?? Math.round(bodySize * 1.5);
    return {
        display: normalizeTypographyToken(heading, {
            fontFamily: heading?.fontFamily || primaryFont,
            fontSize: displaySize,
            fontWeight: heading?.fontWeight ?? 700,
            lineHeight: heading?.lineHeight ?? Math.round(displaySize * 1.2),
            letterSpacing: heading?.letterSpacing ?? 0,
        }),
        'title-md': {
            fontFamily: heading?.fontFamily || primaryFont,
            fontSize: Math.max(Math.round(displaySize * 0.68), bodySize + 2),
            fontWeight: heading?.fontWeight ?? 600,
            lineHeight: Math.max(Math.round(displaySize * 0.86), bodyLineHeight),
            letterSpacing: heading?.letterSpacing ?? 0,
        },
        'body-md': normalizeTypographyToken(body, {
            fontFamily: body?.fontFamily || primaryFont,
            fontSize: bodySize,
            fontWeight: body?.fontWeight ?? 400,
            lineHeight: bodyLineHeight,
            letterSpacing: body?.letterSpacing ?? 0,
        }),
        caption: normalizeTypographyToken(caption, {
            fontFamily: caption?.fontFamily || body?.fontFamily || primaryFont,
            fontSize: caption?.fontSize ?? Math.max(bodySize - 2, 12),
            fontWeight: caption?.fontWeight ?? 500,
            lineHeight: caption?.lineHeight ?? Math.max(Math.round(bodySize * 1.25), 16),
            letterSpacing: caption?.letterSpacing ?? 0,
        }),
        button: normalizeTypographyToken(button, {
            fontFamily: button?.fontFamily || body?.fontFamily || primaryFont,
            fontSize: button?.fontSize ?? Math.max(bodySize - 2, 13),
            fontWeight: button?.fontWeight ?? 600,
            lineHeight: button?.lineHeight ?? Math.max(bodySize, 16),
            letterSpacing: button?.letterSpacing ?? 0,
        }),
    };
}
function buildDesignRounded(snapshot) {
    const scale = snapshot.tokens.radius.scale;
    const rounded = {};
    if (scale.sm) {
        rounded.xs = scale.sm.value;
        rounded.sm = scale.sm.value;
    }
    if (scale.md)
        rounded.md = scale.md.value;
    if (scale.lg)
        rounded.lg = scale.lg.value;
    if (scale.xl)
        rounded.xl = scale.xl.value;
    if (scale.full) {
        rounded.pill = scale.full.value;
        rounded.full = scale.full.value;
    }
    return rounded;
}
function buildDesignSpacing(snapshot) {
    const scale = snapshot.tokens.spacing.scale;
    const spacing = {};
    if (scale.xs) {
        spacing.xxs = scale.xs.value;
        spacing.xs = scale.xs.value;
    }
    if (scale.sm)
        spacing.sm = scale.sm.value;
    if (scale.md)
        spacing.md = scale.md.value;
    if (scale.lg)
        spacing.lg = scale.lg.value;
    if (scale.xl) {
        spacing.xl = scale.xl.value;
        spacing.xxl = Math.max(scale.xl.value, scale.lg?.value ?? scale.md?.value ?? scale.xl.value);
        spacing.section = Math.max(scale.xl.value * 3, scale.md?.value ?? scale.xl.value);
    }
    return spacing;
}
function buildDesignComponents(snapshot, colors, rounded, spacing) {
    const button = snapshot.components.button?.[0]?.style;
    const card = snapshot.components.card?.[0]?.style;
    const input = snapshot.components.input?.[0]?.style;
    const controlBlockPadding = spacingRef(spacing, ['xs', 'sm', 'md']);
    const controlInlinePadding = spacingRef(spacing, ['md', 'sm', 'lg', 'xs']);
    const panelPadding = spacingRef(spacing, ['xl', 'lg', 'md', 'sm', 'xs']);
    const badgeBlockPadding = spacingRef(spacing, ['xxs', 'xs', 'sm']);
    const badgeInlinePadding = spacingRef(spacing, ['sm', 'md', 'xs']);
    const controlRadius = roundedRef(rounded, ['md', 'sm', 'lg', 'xs']);
    const panelRadius = roundedRef(rounded, ['lg', 'md', 'xl', 'sm']);
    const badgeRadius = roundedRef(rounded, ['pill', 'full', 'md', 'sm']);
    return {
        'button-primary': {
            backgroundColor: '{colors.primary}',
            textColor: '{colors.on-primary}',
            typography: '{typography.button}',
            rounded: controlRadius,
            padding: `${controlBlockPadding} ${controlInlinePadding}`,
            height: button?.height || '40px',
        },
        'button-secondary': {
            backgroundColor: '{colors.surface}',
            textColor: '{colors.ink}',
            borderColor: '{colors.hairline}',
            typography: '{typography.button}',
            rounded: controlRadius,
            padding: `${controlBlockPadding} ${controlInlinePadding}`,
        },
        card: {
            backgroundColor: card?.backgroundColor === colors.primary ? '{colors.surface}' : '{colors.surface}',
            textColor: '{colors.ink}',
            borderColor: '{colors.hairline}',
            rounded: panelRadius,
            padding: panelPadding,
            boxShadow: card?.boxShadow || '{shadows.card}',
        },
        'text-input': {
            backgroundColor: input?.backgroundColor ? '{colors.surface}' : '{colors.surface}',
            textColor: '{colors.ink}',
            borderColor: '{colors.hairline}',
            typography: '{typography.body-md}',
            rounded: controlRadius,
            padding: `${controlBlockPadding} ${badgeInlinePadding}`,
            height: input?.height || '40px',
        },
        'badge-pill': {
            backgroundColor: '{colors.surface-soft}',
            textColor: '{colors.ink}',
            typography: '{typography.caption}',
            rounded: badgeRadius,
            padding: `${badgeBlockPadding} ${badgeInlinePadding}`,
        },
        'focus-ring': {
            color: '{colors.primary}',
            width: '2px',
            offset: '2px',
        },
    };
}
function layoutSpacingGuidance(snapshot, spacing) {
    const lines = [`- Base spacing unit: \`${formatPx(snapshot.tokens.spacing.baseUnit)}\`.`];
    if (spacing.md && spacing.xl) {
        lines.push(`- Use \`{spacing.md}\` (${formatPx(spacing.md)}) for compact control gaps and \`{spacing.xl}\` (${formatPx(spacing.xl)}) for card or section padding.`);
    }
    else if (spacing.md) {
        lines.push(`- Use \`{spacing.md}\` (${formatPx(spacing.md)}) for compact control gaps and component padding.`);
    }
    else if (spacing.lg) {
        lines.push(`- Use \`{spacing.lg}\` (${formatPx(spacing.lg)}) for larger component and section padding.`);
    }
    else if (spacing.sm || spacing.xs) {
        const [name, value] = spacing.sm ? ['sm', spacing.sm] : ['xs', spacing.xs];
        lines.push(`- Use \`{spacing.${name}}\` (${formatPx(value)}) as the clearest extracted spacing step.`);
    }
    else {
        lines.push('- No stable spacing scale was detected; prefer compact, consistent gaps until more evidence is available.');
    }
    return lines;
}
function roundedGuidance(rounded) {
    const lines = [];
    if (rounded.md) {
        lines.push(`- Buttons and inputs use \`{rounded.md}\` (${formatPx(rounded.md)}).`);
    }
    else if (rounded.sm) {
        lines.push(`- Buttons and inputs use \`{rounded.sm}\` (${formatPx(rounded.sm)}).`);
    }
    else {
        lines.push('- No stable control radius was detected; keep button and input corners modest.');
    }
    if (rounded.lg) {
        lines.push(`- Cards and larger panels use \`{rounded.lg}\` (${formatPx(rounded.lg)}).`);
    }
    else if (rounded.md) {
        lines.push(`- Cards and larger panels use \`{rounded.md}\` (${formatPx(rounded.md)}).`);
    }
    if (rounded.pill) {
        lines.push('- Use `{rounded.pill}` only for badges, chips, and fully rounded controls.');
    }
    return lines;
}
function spacingRef(spacing, names) {
    const name = names.find((candidate) => typeof spacing[candidate] === 'number');
    return name ? `{spacing.${name}}` : 'not detected';
}
function roundedRef(rounded, names) {
    const name = names.find((candidate) => typeof rounded[candidate] === 'number');
    return name ? `{rounded.${name}}` : 'not detected';
}
function numberEntries(values) {
    return Object.entries(values).filter((entry) => typeof entry[1] === 'number');
}
function componentYamlLines(name, spec) {
    return [`  ${name}:`, ...Object.entries(spec).map(([key, value]) => `    ${key}: ${quoteYaml(value)}`)];
}
function componentMarkdownLines(name, spec) {
    const label = name
        .split('-')
        .map((part) => part.charAt(0).toUpperCase() + part.slice(1))
        .join(' ');
    const styles = Object.entries(spec)
        .map(([key, value]) => `${key} ${value}`)
        .join(', ');
    return [`### ${label}`, '', `Use \`{components.${name}}\`: ${styles}.`, ''];
}
function buildDesignDescription(snapshot, colors, primaryFont) {
    const cssVarSignal = snapshot.raw.cssVariables.length
        ? `${snapshot.raw.cssVariables.length} CSS variables were detected`
        : 'no CSS variables were detected';
    const componentSignal = Object.values(snapshot.components).some((candidates) => candidates?.length)
        ? 'component candidates were found'
        : 'component candidates were limited';
    return `A locally extracted interface system for ${snapshot.meta.hostname || 'the current page'}. It centers on ${colors.canvas} canvas surfaces, ${colors.primary} primary accents, ${colors.ink} text, and ${primaryFont} typography; ${cssVarSignal} and ${componentSignal}.`;
}
function normalizeTypographyToken(token, fallback) {
    return {
        fontFamily: token?.fontFamily || fallback.fontFamily,
        fontSize: token?.fontSize ?? fallback.fontSize,
        fontWeight: token?.fontWeight ?? fallback.fontWeight,
        lineHeight: token?.lineHeight ?? fallback.lineHeight,
        letterSpacing: token?.letterSpacing ?? fallback.letterSpacing,
    };
}
function typographyUse(name) {
    const uses = {
        display: 'Hero and major section headings',
        'title-md': 'Card titles and compact section headings',
        'body-md': 'Default body copy and form text',
        caption: 'Badges, metadata, helper text',
        button: 'Buttons and compact controls',
    };
    return uses[name] ?? 'General UI text';
}
function quoteYaml(value) {
    return `"${value.replace(/\\/g, '\\\\').replace(/"/g, '\\"')}"`;
}
function formatConfidence(value) {
    if (typeof value !== 'number' || Number.isNaN(value))
        return '0';
    return Number(value.toFixed(2)).toString();
}
function formatLineHeight(fontSize, lineHeight) {
    if (!fontSize || !lineHeight)
        return '1';
    const ratio = lineHeight / fontSize;
    return Number.isInteger(ratio) ? ratio.toString() : ratio.toFixed(2).replace(/0+$/, '').replace(/\.$/, '');
}
function getPrimaryFontFamily(snapshot) {
    return (snapshot.tokens.typography.fontFamilies[0]?.value ||
        snapshot.tokens.typography.roles.body?.fontFamily ||
        snapshot.tokens.typography.roles.heading?.fontFamily ||
        'system-ui, sans-serif');
}
function formatTypographyShort(token) {
    return `${formatPx(token.fontSize)} / ${formatPx(token.lineHeight)} / ${token.fontWeight}`;
}
function formatPx(value) {
    if (typeof value !== 'number' || Number.isNaN(value)) {
        return '0px';
    }
    return `${Number.isInteger(value) ? value : Number(value.toFixed(3))}px`;
}
function camelKey(role) {
    return role;
}
function dtcgToken($type, $value) {
    return { $type, $value };
}
function isString(value) {
    return typeof value === 'string';
}