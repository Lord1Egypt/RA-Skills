import { HttpTransport, ExchangeClient, InfoClient } from '@nktkas/hyperliquid';

/**
 * Create HttpTransport pointed at the configured API URL.
 *
 * @param {{ yaml: object }} cfg  Result of loadConfig()
 * @returns {HttpTransport}
 */
const ALLOWED_API_URLS = new Set([
  'https://api.hyperliquid.xyz',
  'https://api.hyperliquid-testnet.xyz',
]);

export function createTransport(cfg) {
  const apiUrl = (cfg?.yaml?.api_url ?? 'https://api.hyperliquid.xyz').replace(/\/$/, '');
  if (!ALLOWED_API_URLS.has(apiUrl)) {
    throw new Error(
      `Disallowed api_url "${apiUrl}". Must be one of: ${[...ALLOWED_API_URLS].join(', ')}`,
    );
  }
  const isTestnet = cfg?.yaml?.network === 'testnet';
  // Default 60 s — SymbolConverter.create() fires meta+spotMeta in parallel; spotMeta returns a
  // large payload that can take >30 s on testnet or under load. SDK default (10 s) is too short.
  // Configurable via `request_timeout_ms` in hyperliquid.yaml.
  const timeout = cfg?.yaml?.request_timeout_ms ?? 60_000;
  return new HttpTransport({ apiUrl, isTestnet, timeout });
}

/**
 * Create an InfoClient (read-only queries).
 *
 * @param {HttpTransport} transport
 * @returns {InfoClient}
 */
export function createInfoClient(transport) {
  return new InfoClient({ transport });
}

/**
 * Create an ExchangeClient (trading operations).
 * wallet must be an ethers.Wallet (v6) instance.
 *
 * @param {HttpTransport} transport
 * @param {import('ethers').Wallet} wallet
 * @returns {ExchangeClient}
 */
export function createExchangeClient(transport, wallet) {
  return new ExchangeClient({ transport, wallet });
}
