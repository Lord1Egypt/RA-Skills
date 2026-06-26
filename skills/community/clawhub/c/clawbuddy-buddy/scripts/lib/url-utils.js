/**
 * Shared URL utilities for buddy scripts.
 *
 * Usage:
 *   import { isLocalhostUrl } from './lib/url-utils.js';
 */

import net from 'net';

/**
 * Check if a URL points to a localhost, loopback, or private-network address.
 *
 * Accepts:
 *   - localhost, *.local (mDNS)
 *   - 127.0.0.1, ::1 (loopback)
 *   - 10.x.x.x, 172.16-31.x.x, 192.168.x.x (RFC 1918 private)
 *   - IPv6 bracket notation: http://[::1]:8080
 *
 * Used to prevent sending auth tokens or sensitive data to remote hosts.
 */
export function isLocalhostUrl(url) {
  try {
    const parsed = new URL(url);
    // Strip IPv6 brackets: [::1] → ::1
    const host = parsed.hostname.toLowerCase().replace(/^\[|\]$/g, '');

    if (host === 'localhost' || host.endsWith('.local')) {
      return true;
    }

    if (host === '::1') {
      return true;
    }

    const ipVersion = net.isIP(host);
    if (ipVersion === 4) {
      return isPrivateOrLoopbackIpv4(host);
    }

    if (ipVersion === 6) {
      return host === '::1';
    }

    return false;
  } catch {
    return false;
  }
}

/**
 * Strict RFC 1918 private-network and loopback check for IPv4 addresses.
 */
function isPrivateOrLoopbackIpv4(host) {
  const parts = host.split('.').map(Number);
  if (parts.length !== 4 || parts.some((p) => !Number.isInteger(p) || p < 0 || p > 255)) {
    return false;
  }

  return parts[0] === 127 ||                         // Loopback
         parts[0] === 10 ||                          // RFC 1918: 10.0.0.0/8
         (parts[0] === 192 && parts[1] === 168) ||   // RFC 1918: 192.168.0.0/16
         (parts[0] === 172 && parts[1] >= 16 && parts[1] <= 31); // RFC 1918: 172.16.0.0/12
}
