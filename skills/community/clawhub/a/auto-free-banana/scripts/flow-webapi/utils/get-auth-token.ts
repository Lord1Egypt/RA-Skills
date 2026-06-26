import process from 'node:process';

import { AuthError } from '../exceptions.js';
import { cookie_header, fetch_with_timeout } from './http.js';
import { logger } from './logger.js';
import { read_cookie_file, write_cookie_file, type CookieMap } from './cookie-file.js';
import { resolveFlowWebCookiePath } from './paths.js';
import { load_browser_auth, type FlowAuthResult } from './load-browser-cookies.js';

/**
 * Try to refresh the access token using the session API with cookies.
 */
async function refresh_token_via_session(cookies: CookieMap, verbose: boolean): Promise<string | null> {
  try {
    const res = await fetch_with_timeout('https://labs.google/fx/api/auth/session', {
      method: 'GET',
      headers: {
        'Cookie': cookie_header(cookies),
        'Accept': 'application/json',
      },
      redirect: 'follow',
      timeout_ms: 15_000,
    });

    if (!res.ok) {
      if (verbose) logger.debug(`Session refresh failed: ${res.status} ${res.statusText}`);
      return null;
    }

    const data = await res.json() as Record<string, unknown>;
    const token = (data.access_token ?? data.accessToken) as string | undefined;
    if (typeof token === 'string' && token.startsWith('ya29.')) {
      if (verbose) logger.debug('Token refreshed via /fx/api/auth/session');
      return token;
    }

    return null;
  } catch (e) {
    if (verbose) logger.debug(`Session refresh error: ${e instanceof Error ? e.message : String(e)}`);
    return null;
  }
}

export type AuthResult = {
  accessToken: string;
  cookies: CookieMap;
};

/**
 * Get a valid OAuth access token for Flow API.
 *
 * Strategy: cached file → refresh via session API → Chrome CDP login
 */
export async function get_auth_token(verbose: boolean = false): Promise<AuthResult> {
  const forceLogin = !!(process.env.FLOW_WEB_LOGIN?.trim() || process.env.FLOW_WEB_FORCE_LOGIN?.trim());

  if (!forceLogin) {
    // Try cached token
    const cached = await read_cookie_file();
    if (cached) {
      // Check if token might still be valid (we can't tell without trying)
      if (verbose) logger.debug('Found cached token, checking...');

      // Try refreshing with cookies to get a fresh token
      const refreshed = await refresh_token_via_session(cached.cookies, verbose);
      if (refreshed) {
        await write_cookie_file(refreshed, cached.cookies, resolveFlowWebCookiePath(), 'refresh').catch(() => {});
        return { accessToken: refreshed, cookies: cached.cookies };
      }

      // Use cached token as-is (may still be valid)
      if (cached.accessToken.startsWith('ya29.')) {
        if (verbose) logger.debug('Using cached access token (could not refresh, may still be valid)');
        return { accessToken: cached.accessToken, cookies: cached.cookies };
      }
    }
  }

  // Fallback: Chrome CDP login
  if (verbose) logger.info('Starting Chrome CDP auth flow...');
  let result: FlowAuthResult;
  try {
    result = await load_browser_auth(verbose);
  } catch (e) {
    throw new AuthError(
      `Failed to authenticate with Flow. ${e instanceof Error ? e.message : String(e)}`,
    );
  }

  if (!result.accessToken || !result.accessToken.startsWith('ya29.')) {
    throw new AuthError('Failed to obtain a valid OAuth access token from Chrome.');
  }

  return { accessToken: result.accessToken, cookies: result.cookies };
}

export const getAuthToken = get_auth_token;
