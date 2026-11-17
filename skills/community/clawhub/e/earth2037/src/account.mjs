import { GatewayError, checkUrl, requireValue } from './common.mjs';
import { readFileSync, writeFileSync, renameSync } from 'node:fs';
import { randomUUID } from 'node:crypto';
import { format } from 'node:util';

export class AccountClient {
  constructor(config, fetchImpl = fetch) {
    this.config = config; this.fetch = fetchImpl;
    this.base = checkUrl(config.accountUrl, 'https:', config.allowLocal).href.replace(/\/$/, '');
    this.accessToken = config.accessToken; this.refreshToken = config.refreshToken;
    this.context = { runtime_platform: config.runtimePlatform, distribution_channel: config.channel,
      device_id: config.deviceId, locale: config.locale };
  }
  async request(method, path, body, { authorized = true, headers = {}, retry = true } = {}) {
    if (authorized && !this.accessToken) await this.login();
    let response;
    try {
      response = await this.fetch(this.base + path, { method, redirect: 'error', signal: AbortSignal.timeout(this.config.timeoutMs),
        headers: { 'Content-Type': 'application/json', ...headers, ...(authorized ? { Authorization: format('Bearer %s', String(this.accessToken)) } : {}) },
        body: body === undefined ? undefined : JSON.stringify(body) });
    } catch { throw new GatewayError('account_network_error', 'Account Center request failed; writes may have an unknown outcome.'); }
    if (response.status === 401 && authorized && retry && this.refreshToken) {
      await this.refresh(); return this.request(method, path, body, { authorized, headers, retry: false });
    }
    const text = await response.text(); let data;
    try { data = text ? JSON.parse(text) : null; } catch { throw new GatewayError('account_invalid_response', 'Account Center returned invalid JSON'); }
    if (!response.ok) throw new GatewayError('account_rejected', 'Account Center rejected request', { status: response.status, code: data?.error?.code || data?.code });
    return data;
  }
  accept(session) {
    requireValue(session?.access_token, 'account_invalid_response', 'Missing access token');
    this.accessToken = session.access_token; this.refreshToken = session.refresh_token || this.refreshToken;
    this.identity = session.account;
    // Refresh handles rotate. Persist only in the explicitly configured private
    // file; never emit them to MCP, the journal, stdout or the repository.
    if (this.config.credentialFile && session.refresh_token) {
      const file = this.config.credentialFile;
      const existing = JSON.parse(readFileSync(file,'utf8'));
      const temp = format('%s.%s.tmp', file, randomUUID());
      writeFileSync(temp, format('%s\n', JSON.stringify({ ...existing, access_token:this.accessToken, refresh_token:this.refreshToken,
        device_id:this.config.deviceId, distribution_channel:this.config.channel })), { mode:0o600, flag:'wx' });
      renameSync(temp,file);
    }
    return { account: session.account, authenticated: true };
  }
  async login() {
    if (this.refreshToken) return this.refresh();
    requireValue(this.config.username && this.config.password, 'credentials_required', 'Configure a private credential file or EARTH2037_ACCESS_TOKEN before login.');
    return this.accept(await this.request('POST', '/v1/auth/password/login', {
      username: this.config.username, password: this.config.password, client_context: this.context,
    }, { authorized: false }));
  }
  async refresh() {
    return this.accept(await this.request('POST', '/v1/auth/refresh', { refresh_token: this.refreshToken,
      device_id: this.config.deviceId, distribution_channel: this.config.channel }, { authorized: false }));
  }
  async register(username) {
    requireValue(this.config.password, 'credentials_required', 'Configure password in private credential file before registration.');
    return this.accept(await this.request('POST', '/v1/auth/password/register', { username,
      password: this.config.password, preferred_locale: this.config.locale, client_context: this.context }, { authorized: false }));
  }
  async me() { this.identity = await this.request('GET', '/v1/me'); return this.identity; }
  directory() { return this.request('GET', format('/v1/server-directory?distribution_channel=%s', encodeURIComponent(this.config.channel)), undefined, { authorized: false }); }
  servers() { return this.request('GET', '/v1/servers'); }
  character(id) { return this.request('GET', format('/v1/servers/%s/character', encodeURIComponent(id))); }
  createCharacter(id, displayName, tribeId, key) { return this.request('POST', format('/v1/servers/%s/character', encodeURIComponent(id)),
    { display_name: displayName, tribe_id: tribeId }, { headers: { 'Idempotency-Key': key } }); }
  operation(id) { return this.request('GET', format('/v1/role-creation-operations/%s', encodeURIComponent(id))); }
  async changePassword() {
    requireValue(this.config.password && this.config.newPassword, 'credentials_required', 'Configure current and new password locally; do not send them through tools.');
    await this.request('POST', '/v1/auth/password/change', { current_password:this.config.password, new_password:this.config.newPassword });
    if(this.config.credentialFile) {
      const file=this.config.credentialFile;const existing=JSON.parse(readFileSync(file,'utf8'));
      existing.password=this.config.newPassword;delete existing.new_password;delete existing.access_token;delete existing.refresh_token;
      const temp=format('%s.%s.tmp',file,randomUUID());writeFileSync(temp,format('%s\n',JSON.stringify(existing)),{mode:0o600,flag:'wx'});renameSync(temp,file);
    }
    this.config.password=this.config.newPassword;this.config.newPassword=null;
    this.accessToken=null;this.refreshToken=null;this.identity=null;
    return { passwordChanged:true, authenticated:false, loginRequired:true };
  }
  ticket(id) { return this.request('POST', format('/v1/servers/%s/entry-ticket', encodeURIComponent(id)), {}); }
  async logout() {
    try { await this.request('POST', '/v1/auth/logout', { refresh_token: this.refreshToken, distribution_channel: this.config.channel }); }
    finally {
      this.accessToken = null; this.refreshToken = null; this.identity = null;
      if (this.config.credentialFile) {
        const file=this.config.credentialFile;const existing=JSON.parse(readFileSync(file,'utf8'));
        delete existing.access_token;delete existing.refresh_token;
        const temp=format('%s.%s.tmp',file,randomUUID());writeFileSync(temp,format('%s\n',JSON.stringify(existing)),{mode:0o600,flag:'wx'});renameSync(temp,file);
      }
    }
    return { authenticated: false };
  }
}
