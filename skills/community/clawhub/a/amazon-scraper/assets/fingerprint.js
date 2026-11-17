/**
 * Sticky fingerprint per ISP port. Linux Chrome 119 = Playwright 1.40 kernel.
 * Same port → same viewport/tz/cores. Never reshuffle. No geolocation grant.
 */
'use strict';

const fs = require('fs');
const path = require('path');

const UA_LINUX_119 = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.6045.199 Safari/537.36';
const SEC_CH_119 = '"Google Chrome";v="119", "Chromium";v="119", "Not?A_Brand";v="24"';

const BY_PORT = {
    '8001': {
        label: 'nyc-linux-119',
        viewport: { width: 1920, height: 1080 },
        timezoneId: 'America/New_York',
        hardwareConcurrency: 8,
        deviceMemory: 8
    },
    '8002': {
        label: 'la-linux-119',
        viewport: { width: 1536, height: 864 },
        timezoneId: 'America/Los_Angeles',
        hardwareConcurrency: 8,
        deviceMemory: 8
    },
    '8003': {
        label: 'chi-linux-119',
        viewport: { width: 1440, height: 900 },
        timezoneId: 'America/Chicago',
        hardwareConcurrency: 4,
        deviceMemory: 8
    },
    '8004': {
        label: 'dal-linux-119',
        viewport: { width: 1366, height: 768 },
        timezoneId: 'America/Chicago',
        hardwareConcurrency: 12,
        deviceMemory: 16
    },
    '8005': {
        label: 'bos-linux-119',
        viewport: { width: 1680, height: 1050 },
        timezoneId: 'America/New_York',
        hardwareConcurrency: 10,
        deviceMemory: 8
    }
};

const FALLBACK = Object.values(BY_PORT);

function portFromProxy(proxyUrl) {
    if (!proxyUrl) return '';
    try {
        return new URL(proxyUrl).port || '';
    } catch {
        return '';
    }
}

function hashHost(s) {
    let h = 0;
    for (let i = 0; i < s.length; i++) h = (h * 31 + s.charCodeAt(i)) >>> 0;
    return h;
}

function fingerprintForProxy(proxyUrl) {
    const port = portFromProxy(proxyUrl);
    const base = (port && BY_PORT[port])
        ? { key: port, ...BY_PORT[port] }
        : (() => {
            const host = proxyUrl ? (() => { try { return new URL(proxyUrl).host; } catch { return 'none'; } })() : 'none';
            return { key: host, ...FALLBACK[hashHost(host) % FALLBACK.length] };
        })();
    return {
        ...base,
        userAgent: UA_LINUX_119,
        secChUa: SEC_CH_119,
        secChUaPlatform: '"Linux"',
        platform: 'Linux x86_64',
        locale: 'en-US',
        acceptLanguage: 'en-US,en;q=0.9',
        maxTouchPoints: 0
    };
}

function contextOptionsFromFingerprint(fp, parsedProxy) {
    const opts = {
        viewport: fp.viewport,
        userAgent: fp.userAgent,
        locale: fp.locale,
        timezoneId: fp.timezoneId,
        extraHTTPHeaders: {
            'Accept-Language': fp.acceptLanguage,
            'Sec-Ch-Ua': fp.secChUa,
            'Sec-Ch-Ua-Mobile': '?0',
            'Sec-Ch-Ua-Platform': fp.secChUaPlatform
        }
    };
    if (parsedProxy) opts.proxy = parsedProxy;
    return opts;
}

async function applyFingerprint(context, fp) {
    await context.addInitScript(({ cores, mem, plat, maxTouch }) => {
        try { Object.defineProperty(navigator, 'hardwareConcurrency', { get: () => cores }); } catch (e) {}
        try { Object.defineProperty(navigator, 'deviceMemory', { get: () => mem }); } catch (e) {}
        try { Object.defineProperty(navigator, 'platform', { get: () => plat }); } catch (e) {}
        try { Object.defineProperty(navigator, 'maxTouchPoints', { get: () => maxTouch }); } catch (e) {}
        try { Object.defineProperty(navigator, 'webdriver', { get: () => undefined }); } catch (e) {}
    }, {
        cores: fp.hardwareConcurrency,
        mem: fp.deviceMemory,
        plat: fp.platform,
        maxTouch: fp.maxTouchPoints
    });
}

/**
 * `namespace` keeps each target's cookie jar separate. Keying on the proxy port
 * alone made every job — Amazon and arbitrary third-party sites alike — read and
 * write one shared storageState file on disk.
 */
function statePathForProxy(proxyUrl, namespace = 'default') {
    const dir = process.env.FP_STATE_DIR || '/data/fingerprint-state';
    const safeNs = String(namespace).replace(/[^a-z0-9._-]/gi, '_').slice(0, 64) || 'default';
    const nsDir = path.join(dir, safeNs);
    fs.mkdirSync(nsDir, { recursive: true, mode: 0o700 });
    const port = portFromProxy(proxyUrl) || 'none';
    return path.join(nsDir, `${port}.json`);
}

async function createFingerprintedContext(browser, proxyUrl, parsedProxy, namespace = 'amazon') {
    const fp = fingerprintForProxy(proxyUrl);
    const statePath = statePathForProxy(proxyUrl, namespace);
    const opts = contextOptionsFromFingerprint(fp, parsedProxy || undefined);
    if (fs.existsSync(statePath)) opts.storageState = statePath;
    const context = await browser.newContext(opts);
    await applyFingerprint(context, fp);
    context._fpMeta = { statePath, label: fp.label };
    return context;
}

async function saveFingerprintStateFile(context) {
    const meta = context && context._fpMeta;
    if (!meta || !meta.statePath) return;
    await context.storageState({ path: meta.statePath });
    // The jar can hold session cookies for a logged-in account.
    try { fs.chmodSync(meta.statePath, 0o600); } catch (e) {}
}

async function warmupAmazon(page) {
    await page.goto('https://www.amazon.com/', { waitUntil: 'domcontentloaded', timeout: 60000 });
    await page.waitForTimeout(1000 + Math.floor(Math.random() * 800));
}

async function humanizeMouse(page) {
    try {
        const vs = page.viewportSize() || { width: 1280, height: 800 };
        const x = 80 + Math.random() * Math.max(200, vs.width * 0.55);
        const y = 80 + Math.random() * Math.max(160, vs.height * 0.45);
        await page.mouse.move(x, y, { steps: 8 + Math.floor(Math.random() * 8) });
    } catch (e) {}
}

async function saveFingerprintState(context) {
    try {
        await saveFingerprintStateFile(context);
    } catch (e) {
        console.error('Failed to persist storage state:', e.message);
    }
}

const LAUNCH_ARGS = [
    '--no-sandbox',
    '--disable-setuid-sandbox',
    '--force-webrtc-ip-handling-policy=disable_non_proxied_udp'
];

module.exports = {
    fingerprintForProxy,
    contextOptionsFromFingerprint,
    applyFingerprint,
    createFingerprintedContext,
    warmupAmazon,
    humanizeMouse,
    saveFingerprintState,
    portFromProxy,
    LAUNCH_ARGS
};
