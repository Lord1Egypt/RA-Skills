#!/usr/bin/env node

/**
 * Token Auto-Refresh Script
 * 
 * Uses stored auth-state (cookies/localStorage) to refresh the JWT token
 * in headless mode — no manual login required.
 * 
 * Run this before sync.js if the token might be expired.
 * Safe to run frequently — it checks expiry first.
 */

const fs = require('fs');
const path = require('path');

const ROOT = path.join(__dirname, '..');
const AUTH_STATE_FILE = path.join(ROOT, '.auth-state.json');
const TOKEN_CACHE_FILE = path.join(ROOT, '.token-cache.json');
const REFRESH_BUFFER_SECONDS = 600; // refresh if < 10 min left

async function needsRefresh() {
    if (!fs.existsSync(TOKEN_CACHE_FILE)) return true;
    try {
        const cache = JSON.parse(fs.readFileSync(TOKEN_CACHE_FILE, 'utf8'));
        if (!cache.tokenExpireAt) return true;
        const remaining = cache.tokenExpireAt - Date.now() / 1000;
        console.log(`⏱️  Token expires in ${Math.round(remaining / 60)} minutes`);
        return remaining < REFRESH_BUFFER_SECONDS;
    } catch (e) {
        return true;
    }
}

async function refreshToken() {
    if (!fs.existsSync(AUTH_STATE_FILE)) {
        console.error('❌ No auth-state.json found. Run dashboard.js first to login.');
        process.exit(1);
    }

    // Check refresh_token expiry
    try {
        const authState = JSON.parse(fs.readFileSync(AUTH_STATE_FILE, 'utf8'));
        for (const origin of authState.origins || []) {
            for (const item of origin.localStorage || []) {
                if (item.name === 'refresh_token_expire_at') {
                    const rtExp = parseInt(item.value);
                    const remaining = rtExp - Date.now() / 1000;
                    if (remaining < 86400) {
                        console.error('⚠️  Refresh token expires in < 24h! Need manual re-login soon.');
                    }
                    if (remaining < 0) {
                        console.error('❌ Refresh token expired. Must login manually via dashboard.js');
                        process.exit(1);
                    }
                }
            }
        }
    } catch (e) { /* ignore parse errors */ }

    const { chromium } = require('playwright');
    const browser = await chromium.launch({ headless: true });
    
    try {
        const context = await browser.newContext({ storageState: AUTH_STATE_FILE });
        const page = await context.newPage();

        await page.goto('https://www.biji.com/note', { 
            waitUntil: 'networkidle', 
            timeout: 30000 
        });

        // Wait for auto-login to complete
        await new Promise(r => setTimeout(r, 3000));

        const authInfo = await page.evaluate(() => ({
            token: localStorage.getItem('token'),
            tokenExpireAt: localStorage.getItem('token_expire_at'),
            refreshToken: localStorage.getItem('refresh_token'),
            refreshTokenExpireAt: localStorage.getItem('refresh_token_expire_at')
        }));

        if (!authInfo.token) {
            console.error('❌ Failed to get token from page. May need manual re-login.');
            process.exit(1);
        }

        // Save new token
        fs.writeFileSync(TOKEN_CACHE_FILE, JSON.stringify({
            token: authInfo.token,
            tokenExpireAt: authInfo.tokenExpireAt ? parseInt(authInfo.tokenExpireAt) : null,
            savedAt: new Date().toISOString()
        }, null, 2));

        // Save updated auth state
        await context.storageState({ path: AUTH_STATE_FILE });

        const exp = new Date(parseInt(authInfo.tokenExpireAt) * 1000);
        const rtExp = new Date(parseInt(authInfo.refreshTokenExpireAt) * 1000);
        console.log(`✅ Token refreshed! Expires: ${exp.toLocaleString()}`);
        console.log(`📅 Refresh token expires: ${rtExp.toLocaleDateString()}`);
        
    } finally {
        await browser.close();
    }
}

(async () => {
    const force = process.argv.includes('--force');
    
    if (!force && !(await needsRefresh())) {
        console.log('✅ Token still valid, no refresh needed.');
        return;
    }

    console.log('🔄 Refreshing token...');
    await refreshToken();
})();
