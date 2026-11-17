// Local operator credentials only. Never exported as Antenna peer authority.
export function localGatewayUrl(host) {
 const port = host.gateway?.port ?? 18789;
 if (!Number.isInteger(port) || port < 1 || port > 65535) throw Error('Valid local gateway port required');
 return `ws://127.0.0.1:${port}`;
}
export function operatorAuth(host, forbidden = [], env = process.env) {
 const auth = host.gateway?.auth ?? {};
 const mode = auth.mode ?? (auth.token !== undefined ? 'token' : 'password');
 if (!['token', 'password'].includes(mode)) throw Error('Token or password gateway authentication required');
 // Honor the explicitly selected local auth mode; never borrow the other credential.
 const value = auth[mode] === undefined && auth.mode === mode
  ? env[mode === 'password' ? 'OPENCLAW_GATEWAY_PASSWORD' : 'OPENCLAW_GATEWAY_TOKEN']
  : auth[mode];
 if (typeof value !== 'string' || !value.trim()) throw Error('Resolved local gateway credential required');
 if (forbidden.includes(value)) throw Error('Antenna bearer must differ from resolved operator credential');
 return {[mode]: value};
}
