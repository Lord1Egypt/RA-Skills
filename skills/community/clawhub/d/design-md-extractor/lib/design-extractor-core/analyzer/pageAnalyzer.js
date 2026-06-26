"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.collectPageMeta = collectPageMeta;
exports.collectVisibleElements = collectVisibleElements;
exports.extractCssVariables = extractCssVariables;
exports.analyzeCurrentPage = analyzeCurrentPage;
exports.buildDesignSnapshot = buildDesignSnapshot;
exports.collectRawPageAnalysis = collectRawPageAnalysis;
exports.collectColorSamples = collectColorSamples;
exports.collectLayoutSamples = collectLayoutSamples;
const color_sanity_1 = require("../core/color-sanity");
const detect_components_1 = require("../core/detect-components");
const detect_design_system_1 = require("../core/detect-design-system");
const extract_colors_1 = require("../core/extract-colors");
const extract_radius_1 = require("../core/extract-radius");
const extract_shadows_1 = require("../core/extract-shadows");
const extract_spacing_1 = require("../core/extract-spacing");
const extract_typography_1 = require("../core/extract-typography");
const infer_color_roles_1 = require("../core/infer-color-roles");
const DEFAULT_VISIBLE_ELEMENT_LIMIT = 800;
const KEY_ELEMENT_SELECTORS = ['main', 'header', 'nav', 'button', 'a', 'input'];
const COLOR_SAMPLE_SELECTOR = [
    'html',
    'body',
    'main',
    'header',
    'nav',
    'section',
    'article',
    'aside',
    'div',
    'button',
    'a',
    'input',
    'textarea',
    'select',
    'label',
    'h1',
    'h2',
    'h3',
    'p',
    '[role="button"]',
    '[role="link"]',
    '[role="tab"]',
    '[aria-selected="true"]',
    '[aria-current]',
    '[class*="active" i]',
    '[class*="selected" i]',
    '[class*="current" i]',
    '[class*="primary" i]',
    '[class*="cta" i]',
    '[class*="success" i]',
    '[class*="warning" i]',
    '[class*="danger" i]',
    '[class*="error" i]',
].join(',');
const LAYOUT_SAMPLE_SELECTOR = [
    'html',
    'body',
    'main',
    'header',
    'nav',
    'section',
    'article',
    'aside',
    'div',
    'button',
    'a',
    'input',
    'textarea',
    'select',
    'label',
    'h1',
    'h2',
    'h3',
    'h4',
    'h5',
    'h6',
    'p',
    'span',
    'small',
    'li',
    '[role="button"]',
    '[role="link"]',
    '[role="tab"]',
    '[class*="card" i]',
    '[class*="panel" i]',
    '[class*="modal" i]',
    '[class*="popover" i]',
    '[class*="floating" i]',
].join(',');
function collectPageMeta() {
    const link = document.querySelector('link[rel*="icon"]');
    return {
        title: document.title,
        url: window.location.href,
        hostname: window.location.hostname,
        analyzedAt: new Date().toISOString(),
        favicon: link?.href || `${window.location.origin}/favicon.ico`,
    };
}
function collectVisibleElements({ limit = DEFAULT_VISIBLE_ELEMENT_LIMIT, } = {}) {
    const summaries = [];
    const elements = Array.from(document.body.querySelectorAll('*'));
    for (const element of elements) {
        if (summaries.length >= limit)
            break;
        if (!isVisibleElement(element))
            continue;
        summaries.push({
            tagName: element.tagName.toLowerCase(),
            ...(element.id ? { id: element.id } : {}),
            ...(element.className && typeof element.className === 'string' ? { className: element.className } : {}),
        });
    }
    return summaries;
}
function extractCssVariables() {
    const records = new Map();
    collectVariablesFromElement(document.documentElement, 'documentElement', records);
    if (document.body) {
        collectVariablesFromElement(document.body, 'body', records);
    }
    for (const selector of KEY_ELEMENT_SELECTORS) {
        const element = document.querySelector(selector);
        if (element) {
            collectVariablesFromElement(element, selector, records);
        }
    }
    return Array.from(records.values());
}
function analyzeCurrentPage() {
    return buildDesignSnapshot(collectRawPageAnalysis());
}
function buildDesignSnapshot(rawAnalysis) {
    const colorTokens = (0, extract_colors_1.extractColorTokens)(rawAnalysis.raw.colorSamples);
    const colors = (0, infer_color_roles_1.inferColorRoles)(colorTokens);
    const sanityIssues = (0, color_sanity_1.collectColorWarnings)(colors);
    const typography = (0, extract_typography_1.extractTypographyTokens)(rawAnalysis.raw.layoutSamples);
    const spacing = (0, extract_spacing_1.extractSpacingTokens)(rawAnalysis.raw.layoutSamples);
    const radius = (0, extract_radius_1.extractRadiusTokens)(rawAnalysis.raw.layoutSamples);
    const shadows = (0, extract_shadows_1.extractShadowTokens)(rawAnalysis.raw.layoutSamples);
    const components = (0, detect_components_1.detectComponents)(rawAnalysis.raw.layoutSamples);
    const designSystem = (0, detect_design_system_1.detectDesignSystem)({
        cssVariables: rawAnalysis.raw.cssVariables,
        layoutSamples: rawAnalysis.raw.layoutSamples,
    });
    return {
        meta: rawAnalysis.meta,
        raw: {
            cssVariables: rawAnalysis.raw.cssVariables,
            elementCounts: rawAnalysis.raw.elementCounts,
            colorTokens,
        },
        tokens: {
            colors: {
                ...colors,
                warnings: [...colors.warnings, ...sanityIssues.map((issue) => `${issue.role}: ${issue.message}`)],
            },
            typography,
            spacing,
            radius,
            shadows,
        },
        components,
        designSystem,
    };
}
function collectRawPageAnalysis() {
    const limit = 800;
    const keyElementSelectors = ['main', 'header', 'nav', 'button', 'a', 'input'];
    const colorSampleSelector = [
        'html',
        'body',
        'main',
        'header',
        'nav',
        'section',
        'article',
        'aside',
        'div',
        'button',
        'a',
        'input',
        'textarea',
        'select',
        'label',
        'h1',
        'h2',
        'h3',
        'p',
        '[role="button"]',
        '[role="link"]',
        '[role="tab"]',
        '[aria-selected="true"]',
        '[aria-current]',
        '[class*="active" i]',
        '[class*="selected" i]',
        '[class*="current" i]',
        '[class*="primary" i]',
        '[class*="cta" i]',
        '[class*="success" i]',
        '[class*="warning" i]',
        '[class*="danger" i]',
        '[class*="error" i]',
    ].join(',');
    const layoutSampleSelector = [
        'html',
        'body',
        'main',
        'header',
        'nav',
        'section',
        'article',
        'aside',
        'div',
        'button',
        'a',
        'input',
        'textarea',
        'select',
        'label',
        'h1',
        'h2',
        'h3',
        'h4',
        'h5',
        'h6',
        'p',
        'span',
        'small',
        'li',
        '[role="button"]',
        '[role="link"]',
        '[role="tab"]',
        '[class*="card" i]',
        '[class*="panel" i]',
        '[class*="modal" i]',
        '[class*="popover" i]',
        '[class*="floating" i]',
    ].join(',');
    function collectInjectedPageMeta() {
        const link = document.querySelector('link[rel*="icon"]');
        return {
            title: document.title,
            url: window.location.href,
            hostname: window.location.hostname,
            analyzedAt: new Date().toISOString(),
            favicon: link?.href || `${window.location.origin}/favicon.ico`,
        };
    }
    function collectInjectedVisibleElements() {
        const summaries = [];
        const elements = Array.from(document.body.querySelectorAll('*'));
        for (const element of elements) {
            if (summaries.length >= limit)
                break;
            if (!isInjectedVisibleElement(element))
                continue;
            summaries.push({
                tagName: element.tagName.toLowerCase(),
                ...(element.id ? { id: element.id } : {}),
                ...(element.className && typeof element.className === 'string' ? { className: element.className } : {}),
            });
        }
        return summaries;
    }
    function collectInjectedVariablesFromElement(element, source, records) {
        const styles = getComputedStyle(element);
        for (const propertyName of Array.from(styles)) {
            if (!propertyName.startsWith('--'))
                continue;
            const value = styles.getPropertyValue(propertyName).trim();
            if (!value)
                continue;
            records.set(`${source}:${propertyName}`, {
                name: propertyName,
                value,
                source,
            });
        }
    }
    function extractInjectedCssVariables() {
        const records = new Map();
        collectInjectedVariablesFromElement(document.documentElement, 'documentElement', records);
        if (document.body) {
            collectInjectedVariablesFromElement(document.body, 'body', records);
        }
        for (const selector of keyElementSelectors) {
            const element = document.querySelector(selector);
            if (element) {
                collectInjectedVariablesFromElement(element, selector, records);
            }
        }
        return Array.from(records.values());
    }
    function collectInjectedColorSamples() {
        const htmlSample = toInjectedColorSample(document.documentElement);
        const bodySample = document.body ? toInjectedColorSample(document.body) : undefined;
        const elements = Array.from(document.body.querySelectorAll(colorSampleSelector))
            .filter(isInjectedVisibleElement)
            .slice(0, 260)
            .map(toInjectedColorSample);
        return [htmlSample, bodySample, ...elements].filter((sample) => Boolean(sample));
    }
    function toInjectedColorSample(element) {
        const styles = getComputedStyle(element);
        const rect = element.getBoundingClientRect();
        const className = typeof element.className === 'string' ? element.className : '';
        return {
            tagName: element.tagName.toLowerCase(),
            ...(element.id ? { id: element.id } : {}),
            ...(className ? { className } : {}),
            ...(element.getAttribute('role') ? { role: element.getAttribute('role') } : {}),
            ...(visibleInjectedText(element) ? { text: visibleInjectedText(element) } : {}),
            ariaSelected: element.getAttribute('aria-selected') === 'true',
            ariaCurrent: element.getAttribute('aria-current'),
            rect: roundedInjectedRect(rect),
            styles: collectInjectedColorStyles(styles),
        };
    }
    function collectInjectedColorStyles(styles) {
        return {
            color: styles.color,
            backgroundColor: styles.backgroundColor,
            backgroundImage: styles.backgroundImage,
            borderTopColor: styles.borderTopColor,
            borderRightColor: styles.borderRightColor,
            borderBottomColor: styles.borderBottomColor,
            borderLeftColor: styles.borderLeftColor,
            outlineColor: styles.outlineColor,
            textDecorationColor: styles.textDecorationColor,
        };
    }
    function collectInjectedLayoutSamples() {
        const htmlSample = toInjectedLayoutSample(document.documentElement);
        const bodySample = document.body ? toInjectedLayoutSample(document.body) : undefined;
        const elements = Array.from(document.body.querySelectorAll(layoutSampleSelector))
            .filter(isInjectedVisibleElement)
            .slice(0, 360)
            .map(toInjectedLayoutSample);
        return [htmlSample, bodySample, ...elements].filter((sample) => Boolean(sample));
    }
    function toInjectedLayoutSample(element) {
        const styles = getComputedStyle(element);
        const rect = element.getBoundingClientRect();
        const className = typeof element.className === 'string' ? element.className : '';
        return {
            tagName: element.tagName.toLowerCase(),
            ...(element.id ? { id: element.id } : {}),
            ...(className ? { className } : {}),
            ...(element.getAttribute('role') ? { role: element.getAttribute('role') } : {}),
            ...(element instanceof HTMLAnchorElement && element.href ? { href: element.href } : {}),
            ...(element instanceof HTMLInputElement && element.type ? { inputType: element.type } : {}),
            ...(element.isContentEditable ? { isContentEditable: true } : {}),
            hasHeading: Boolean(element.querySelector('h1,h2,h3,h4,h5,h6,[role="heading"]')),
            hasImage: Boolean(element.querySelector('img,picture,svg')),
            hasButton: Boolean(element.querySelector('button,[role="button"],input[type="button"],input[type="submit"]')),
            ...(visibleInjectedText(element) ? { text: visibleInjectedText(element) } : {}),
            rect: roundedInjectedRect(rect),
            styles: collectInjectedLayoutStyles(styles),
        };
    }
    function collectInjectedLayoutStyles(styles) {
        return {
            color: styles.color,
            backgroundColor: styles.backgroundColor,
            borderTopColor: styles.borderTopColor,
            borderRightColor: styles.borderRightColor,
            borderBottomColor: styles.borderBottomColor,
            borderLeftColor: styles.borderLeftColor,
            borderTopWidth: styles.borderTopWidth,
            borderRightWidth: styles.borderRightWidth,
            borderBottomWidth: styles.borderBottomWidth,
            borderLeftWidth: styles.borderLeftWidth,
            cursor: styles.cursor,
            width: styles.width,
            height: styles.height,
            fontFamily: styles.fontFamily,
            fontSize: styles.fontSize,
            fontWeight: styles.fontWeight,
            lineHeight: styles.lineHeight,
            letterSpacing: styles.letterSpacing,
            paddingTop: styles.paddingTop,
            paddingRight: styles.paddingRight,
            paddingBottom: styles.paddingBottom,
            paddingLeft: styles.paddingLeft,
            marginTop: styles.marginTop,
            marginRight: styles.marginRight,
            marginBottom: styles.marginBottom,
            marginLeft: styles.marginLeft,
            gap: styles.gap,
            rowGap: styles.rowGap,
            columnGap: styles.columnGap,
            borderTopLeftRadius: styles.borderTopLeftRadius,
            borderTopRightRadius: styles.borderTopRightRadius,
            borderBottomRightRadius: styles.borderBottomRightRadius,
            borderBottomLeftRadius: styles.borderBottomLeftRadius,
            borderRadius: styles.borderRadius,
            boxShadow: styles.boxShadow,
            textShadow: styles.textShadow,
        };
    }
    function roundedInjectedRect(rect) {
        return {
            width: Math.round(rect.width),
            height: Math.round(rect.height),
            top: Math.round(rect.top),
            left: Math.round(rect.left),
        };
    }
    function visibleInjectedText(element) {
        const text = (element.getAttribute('aria-label') || element.innerText || element.textContent || '').replace(/\s+/g, ' ').trim();
        return text ? text.slice(0, 80) : undefined;
    }
    function isInjectedVisibleElement(element) {
        const styles = getComputedStyle(element);
        const rect = element.getBoundingClientRect();
        const isHidden = styles.display === 'none' ||
            styles.visibility === 'hidden' ||
            styles.opacity === '0' ||
            element.hidden ||
            element.getAttribute('aria-hidden') === 'true';
        return !isHidden && isInjectedRectInViewport(rect);
    }
    function isInjectedRectInViewport(rect) {
        const viewportWidth = window.innerWidth || document.documentElement.clientWidth;
        const viewportHeight = window.innerHeight || document.documentElement.clientHeight;
        return rect.width > 0 && rect.height > 0 && rect.right > 0 && rect.bottom > 0 && rect.left < viewportWidth && rect.top < viewportHeight;
    }
    const visibleElements = collectInjectedVisibleElements();
    return {
        meta: collectInjectedPageMeta(),
        raw: {
            cssVariables: extractInjectedCssVariables(),
            elementCounts: {
                totalVisible: visibleElements.length,
                limitedTo: limit,
                byTag: visibleElements.reduce((counts, element) => {
                    counts[element.tagName] = (counts[element.tagName] ?? 0) + 1;
                    return counts;
                }, {}),
            },
            colorSamples: collectInjectedColorSamples(),
            layoutSamples: collectInjectedLayoutSamples(),
        },
    };
}
function collectVariablesFromElement(element, source, records) {
    const styles = getComputedStyle(element);
    for (const propertyName of Array.from(styles)) {
        if (!propertyName.startsWith('--'))
            continue;
        const value = styles.getPropertyValue(propertyName).trim();
        if (!value)
            continue;
        const key = `${source}:${propertyName}`;
        records.set(key, {
            name: propertyName,
            value,
            source,
        });
    }
}
function countVisibleElements(elements, limit) {
    return {
        totalVisible: elements.length,
        limitedTo: limit,
        byTag: elements.reduce((counts, element) => {
            counts[element.tagName] = (counts[element.tagName] ?? 0) + 1;
            return counts;
        }, {}),
    };
}
function collectColorSamples({ limit = 260 } = {}) {
    const htmlSample = toColorSample(document.documentElement);
    const bodySample = document.body ? toColorSample(document.body) : undefined;
    const elements = Array.from(document.body.querySelectorAll(COLOR_SAMPLE_SELECTOR))
        .filter(isVisibleElement)
        .slice(0, limit)
        .map(toColorSample);
    return [htmlSample, bodySample, ...elements].filter((sample) => Boolean(sample));
}
function collectLayoutSamples({ limit = 360 } = {}) {
    const htmlSample = toLayoutSample(document.documentElement);
    const bodySample = document.body ? toLayoutSample(document.body) : undefined;
    const elements = Array.from(document.body.querySelectorAll(LAYOUT_SAMPLE_SELECTOR))
        .filter(isVisibleElement)
        .slice(0, limit)
        .map(toLayoutSample);
    return [htmlSample, bodySample, ...elements].filter((sample) => Boolean(sample));
}
function toColorSample(element) {
    const styles = getComputedStyle(element);
    const rect = element.getBoundingClientRect();
    const className = typeof element.className === 'string' ? element.className : '';
    return {
        tagName: element.tagName.toLowerCase(),
        ...(element.id ? { id: element.id } : {}),
        ...(className ? { className } : {}),
        ...(element.getAttribute('role') ? { role: element.getAttribute('role') } : {}),
        ...(visibleText(element) ? { text: visibleText(element) } : {}),
        ariaSelected: element.getAttribute('aria-selected') === 'true',
        ariaCurrent: element.getAttribute('aria-current'),
        rect: roundedRect(rect),
        styles: collectColorStyles(styles),
    };
}
function collectColorStyles(styles) {
    return {
        color: styles.color,
        backgroundColor: styles.backgroundColor,
        backgroundImage: styles.backgroundImage,
        borderTopColor: styles.borderTopColor,
        borderRightColor: styles.borderRightColor,
        borderBottomColor: styles.borderBottomColor,
        borderLeftColor: styles.borderLeftColor,
        outlineColor: styles.outlineColor,
        textDecorationColor: styles.textDecorationColor,
    };
}
function toLayoutSample(element) {
    const styles = getComputedStyle(element);
    const rect = element.getBoundingClientRect();
    const className = typeof element.className === 'string' ? element.className : '';
    return {
        tagName: element.tagName.toLowerCase(),
        ...(element.id ? { id: element.id } : {}),
        ...(className ? { className } : {}),
        ...(element.getAttribute('role') ? { role: element.getAttribute('role') } : {}),
        ...(element instanceof HTMLAnchorElement && element.href ? { href: element.href } : {}),
        ...(element instanceof HTMLInputElement && element.type ? { inputType: element.type } : {}),
        ...(element.isContentEditable ? { isContentEditable: true } : {}),
        hasHeading: Boolean(element.querySelector('h1,h2,h3,h4,h5,h6,[role="heading"]')),
        hasImage: Boolean(element.querySelector('img,picture,svg')),
        hasButton: Boolean(element.querySelector('button,[role="button"],input[type="button"],input[type="submit"]')),
        ...(visibleText(element) ? { text: visibleText(element) } : {}),
        rect: roundedRect(rect),
        styles: collectLayoutStyles(styles),
    };
}
function collectLayoutStyles(styles) {
    return {
        color: styles.color,
        backgroundColor: styles.backgroundColor,
        borderTopColor: styles.borderTopColor,
        borderRightColor: styles.borderRightColor,
        borderBottomColor: styles.borderBottomColor,
        borderLeftColor: styles.borderLeftColor,
        borderTopWidth: styles.borderTopWidth,
        borderRightWidth: styles.borderRightWidth,
        borderBottomWidth: styles.borderBottomWidth,
        borderLeftWidth: styles.borderLeftWidth,
        cursor: styles.cursor,
        width: styles.width,
        height: styles.height,
        fontFamily: styles.fontFamily,
        fontSize: styles.fontSize,
        fontWeight: styles.fontWeight,
        lineHeight: styles.lineHeight,
        letterSpacing: styles.letterSpacing,
        paddingTop: styles.paddingTop,
        paddingRight: styles.paddingRight,
        paddingBottom: styles.paddingBottom,
        paddingLeft: styles.paddingLeft,
        marginTop: styles.marginTop,
        marginRight: styles.marginRight,
        marginBottom: styles.marginBottom,
        marginLeft: styles.marginLeft,
        gap: styles.gap,
        rowGap: styles.rowGap,
        columnGap: styles.columnGap,
        borderTopLeftRadius: styles.borderTopLeftRadius,
        borderTopRightRadius: styles.borderTopRightRadius,
        borderBottomRightRadius: styles.borderBottomRightRadius,
        borderBottomLeftRadius: styles.borderBottomLeftRadius,
        borderRadius: styles.borderRadius,
        boxShadow: styles.boxShadow,
        textShadow: styles.textShadow,
    };
}
function roundedRect(rect) {
    return {
        width: Math.round(rect.width),
        height: Math.round(rect.height),
        top: Math.round(rect.top),
        left: Math.round(rect.left),
    };
}
function visibleText(element) {
    const text = (element.getAttribute('aria-label') || element.innerText || element.textContent || '').replace(/\s+/g, ' ').trim();
    return text ? text.slice(0, 80) : undefined;
}
function isVisibleElement(element) {
    const styles = getComputedStyle(element);
    const rect = element.getBoundingClientRect();
    if (styles.display === 'none' || styles.visibility === 'hidden' || styles.opacity === '0') {
        return false;
    }
    if (element.hidden || element.getAttribute('aria-hidden') === 'true') {
        return false;
    }
    return isRectInViewport(rect);
}
function isRectInViewport(rect) {
    const viewportWidth = window.innerWidth || document.documentElement.clientWidth;
    const viewportHeight = window.innerHeight || document.documentElement.clientHeight;
    return rect.width > 0 && rect.height > 0 && rect.right > 0 && rect.bottom > 0 && rect.left < viewportWidth && rect.top < viewportHeight;
}