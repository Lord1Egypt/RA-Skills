'use strict';
/**
 * _shared/client.js — 平台 /api/v1 API 客户端 (对齐转链 skill 同名模块)。
 *
 * - 内置全局 fetch, 单次请求默认 15s 超时 (AbortController), opts.timeoutMs 可覆盖
 * - 统一信封 {"code","message","data"}: code !== 0 抛 BizError
 * - HTTP 层失败 (连接拒绝/超时/非信封响应) 抛 NetworkError
 */
const REQUEST_TIMEOUT_MS = 15000;

let _insecureNoted = false;
let _httpWarned = false;
const _insecureHostsWarned = new Set();

/** 忽略 HTTPS 证书校验 (服务端自签/域名不匹配证书时由 insecure 配置开启)。进程级。 */
function allowInsecureTls() {
  process.env.NODE_TLS_REJECT_UNAUTHORIZED = '0';
}

/** 业务错误: code 为后端错误码 (1001/1002/3001/...) */
class BizError extends Error {
  constructor(code, message) {
    super(message);
    this.name = 'BizError';
    this.code = code;
  }
}

/** 网络/服务不可达错误 */
class NetworkError extends Error {
  constructor(message) {
    super(message);
    this.name = 'NetworkError';
    this.code = 'NETWORK_ERROR';
  }
}

class ApiClient {
  /** @param {{baseUrl: string, token?: string}} opts */
  constructor({ baseUrl, token }) {
    this.baseUrl = String(baseUrl).replace(/\/+$/, '');
    this.token = token || '';
  }

  /** 发起 API 请求, 成功返回信封 data。opts.timeoutMs 可覆盖默认 15s 超时。 */
  async request(method, apiPath, opts = {}) {
    const { body, headers = {}, timeoutMs = REQUEST_TIMEOUT_MS } = opts;
    // 明文 http + 携带 token 时提示一次 (每进程仅一次), 不打断请求
    if (!_httpWarned && this.token && this.baseUrl.startsWith('http://')) {
      _httpWarned = true;
      process.stderr.write('[warn] 当前服务地址为明文 http，token 会明文传输，建议确认网络安全或切换 https\n');
    }
    // insecure 生效时, 对每个 https 目标域名明确提示证书校验已关闭 (审计 S-P2-2:
    // 原先只有一行不含目标域名的提示, agent 通常不读 stderr, 风险不透明)
    if (!_insecureNoted && this.baseUrl.startsWith('https://')
        && process.env.NODE_TLS_REJECT_UNAUTHORIZED === '0') {
      _insecureNoted = true;
      _insecureHostsWarned.add(this.baseUrl);
      process.stderr.write(`[warn] 目标 ${this.baseUrl} 的 HTTPS 证书校验已关闭（insecure=true），存在中间人风险，请确认网络环境\n`);
    }
    const ctrl = new AbortController();
    const timer = setTimeout(() => ctrl.abort(), timeoutMs);
    let res;
    let payload = null;
    try {
      res = await fetch(this.baseUrl + '/api/v1' + apiPath, {
        method,
        headers: {
          ...(body ? { 'Content-Type': 'application/json' } : {}),
          ...(this.token ? { Authorization: `Bearer ${this.token}` } : {}),
          ...headers,
        },
        body: body ? JSON.stringify(body) : undefined,
        signal: ctrl.signal,
      });
      try {
        payload = await res.json();
      } catch (err) {
        if (err.name === 'AbortError') throw err;
        /* 非 JSON 响应, 按 HTTP 层错误处理 */
      }
    } catch (err) {
      if (err.name === 'AbortError') {
        throw new NetworkError(`请求超时（${Math.round(timeoutMs / 1000)}s）: ${this.baseUrl}`);
      }
      throw new NetworkError(`无法连接后端服务 ${this.baseUrl}: ${err.message}`);
    } finally {
      clearTimeout(timer);
    }

    if (payload && typeof payload.code === 'number') {
      if (payload.code === 0) return payload.data;
      throw new BizError(payload.code, payload.message || `业务错误 code=${payload.code}`);
    }
    if (res.status === 429) throw new BizError(4290, '触发限流，请稍后重试');
    throw new NetworkError(`后端返回异常响应 HTTP ${res.status}（期望统一信封 JSON）`);
  }

  // ---- auth ----
  // (审计 G3: 删除 sendSmsCode/register/login 三个遗留方法 —— 本 skill 终端无法展示
  //  图形/短信验证码, SKILL.md 明确一律走 --link, register/login 被调用也必被后端 2003 拒绝)
  logout() {
    return this.request('POST', '/auth/logout');
  }
  createCliSession() {
    return this.request('POST', '/auth/cli-session');
  }
  checkCliSession(accessToken) {
    return this.request('POST', '/auth/cli-session/check', { body: { access_token: accessToken } });
  }

  // ---- user ----
  profile() {
    return this.request('GET', '/user/profile');
  }

  // ---- tasks (平台采集; 2026-09 单服务融合后路径为 /platform/*, 与转链 /tasks 区分) ----
  submitTask(capability, items, idempotencyKey, force = false) {
    return this.request('POST', '/platform/tasks', {
      body: { capability, items, force },
      headers: { 'X-Idempotency-Key': idempotencyKey },
    });
  }
  getTask(taskId) {
    return this.request('GET', `/platform/tasks/${encodeURIComponent(taskId)}`);
  }
  createExport(taskId) {
    return this.request('POST', `/platform/tasks/${encodeURIComponent(taskId)}/export`);
  }
  getExport(exportId) {
    return this.request('GET', `/platform/exports/${encodeURIComponent(exportId)}`);
  }

  // ---- comments session (xhs_comments v2 分步会话采集, 2026-10-10) ----
  createCommentSession(url) {
    // 建会话内含转链 + 互动数采集 (服务端串行 HTTP), 放宽超时
    return this.request('POST', '/comments/sessions', { body: { url }, timeoutMs: 90000 });
  }
  getCommentSession(sessionId) {
    return this.request('GET', `/comments/sessions/${encodeURIComponent(sessionId)}`);
  }
  listCommentSessions(page = 1, pageSize = 20, status = '') {
    const q = `?page=${page}&page_size=${pageSize}` +
      (status ? `&status=${encodeURIComponent(status)}` : '');
    return this.request('GET', '/comments/sessions' + q);
  }
  stepCommentSession(sessionId, type, rootCommentId = '') {
    // 步进服务端最长执行 ~180s (滚动一页/展开一次 + 节点回传), 放宽超时
    return this.request('POST', `/comments/sessions/${encodeURIComponent(sessionId)}/step`, {
      body: { type, root_comment_id: rootCommentId }, timeoutMs: 200000,
    });
  }
  finishCommentSession(sessionId) {
    return this.request('POST', `/comments/sessions/${encodeURIComponent(sessionId)}/finish`);
  }
  listSessionComments(sessionId, page = 1, pageSize = 100) {
    return this.request('GET',
      `/comments/sessions/${encodeURIComponent(sessionId)}/comments?page=${page}&page_size=${pageSize}`);
  }

  // ---- dy comments session (dy_comments 分步会话采集, 2026-10-15) ----
  // 与 xhs comments session 平行, 路径前缀 /dy/comments; 步进参数为 root_cid
  createDyCommentSession(url) {
    // 建会话内含节点免费 probe 探测 (服务端默认 60s 超时), 放宽超时
    return this.request('POST', '/dy/comments/sessions', { body: { url }, timeoutMs: 90000 });
  }
  getDyCommentSession(sessionId) {
    return this.request('GET', `/dy/comments/sessions/${encodeURIComponent(sessionId)}`);
  }
  listDyCommentSessions(page = 1, pageSize = 20, status = '') {
    const q = `?page=${page}&page_size=${pageSize}` +
      (status ? `&status=${encodeURIComponent(status)}` : '');
    return this.request('GET', '/dy/comments/sessions' + q);
  }
  stepDyCommentSession(sessionId, type, rootCid = '') {
    // 步进服务端最长执行 ~180s (滚动一页/展开一次 + 节点回传), 放宽超时
    return this.request('POST', `/dy/comments/sessions/${encodeURIComponent(sessionId)}/step`, {
      body: { type, root_cid: rootCid }, timeoutMs: 200000,
    });
  }
  finishDyCommentSession(sessionId) {
    return this.request('POST', `/dy/comments/sessions/${encodeURIComponent(sessionId)}/finish`);
  }
  listDySessionComments(sessionId, page = 1, pageSize = 100) {
    return this.request('GET',
      `/dy/comments/sessions/${encodeURIComponent(sessionId)}/comments?page=${page}&page_size=${pageSize}`);
  }

  // ---- ks comments session (ks_comments 分步会话采集, 2026-10-16) ----
  // 与 dy comments session 平行, 路径前缀 /ks/comments; 步进参数为 root_cid
  createKsCommentSession(url) {
    // 建会话内含节点免费 probe 探测 (服务端默认 60s 超时), 放宽超时
    return this.request('POST', '/ks/comments/sessions', { body: { url }, timeoutMs: 90000 });
  }
  getKsCommentSession(sessionId) {
    return this.request('GET', `/ks/comments/sessions/${encodeURIComponent(sessionId)}`);
  }
  listKsCommentSessions(page = 1, pageSize = 20, status = '') {
    const q = `?page=${page}&page_size=${pageSize}` +
      (status ? `&status=${encodeURIComponent(status)}` : '');
    return this.request('GET', '/ks/comments/sessions' + q);
  }
  stepKsCommentSession(sessionId, type, rootCid = '') {
    // 步进服务端最长执行 ~180s (滚动一页/展开一次 + 节点回传), 放宽超时
    return this.request('POST', `/ks/comments/sessions/${encodeURIComponent(sessionId)}/step`, {
      body: { type, root_cid: rootCid }, timeoutMs: 200000,
    });
  }
  finishKsCommentSession(sessionId) {
    return this.request('POST', `/ks/comments/sessions/${encodeURIComponent(sessionId)}/finish`);
  }
  listKsSessionComments(sessionId, page = 1, pageSize = 100) {
    return this.request('GET',
      `/ks/comments/sessions/${encodeURIComponent(sessionId)}/comments?page=${page}&page_size=${pageSize}`);
  }

  // ---- b comments session (b_comments 分步会话采集, 2026-10-19) ----
  // 与 ks/dy comments session 平行, 路径前缀 /b/comments; 步进参数为 root_cid
  createBCommentSession(url) {
    // 建会话内含节点免费 probe 探测 (服务端默认 60s 超时), 放宽超时
    return this.request('POST', '/b/comments/sessions', { body: { url }, timeoutMs: 90000 });
  }
  getBCommentSession(sessionId) {
    return this.request('GET', `/b/comments/sessions/${encodeURIComponent(sessionId)}`);
  }
  listBCommentSessions(page = 1, pageSize = 20, status = '') {
    const q = `?page=${page}&page_size=${pageSize}` +
      (status ? `&status=${encodeURIComponent(status)}` : '');
    return this.request('GET', '/b/comments/sessions' + q);
  }
  stepBCommentSession(sessionId, type, rootCid = '') {
    // 步进服务端最长执行 ~180s (翻一页/翻一次回复 + 节点回传), 放宽超时
    return this.request('POST', `/b/comments/sessions/${encodeURIComponent(sessionId)}/step`, {
      body: { type, root_cid: rootCid }, timeoutMs: 200000,
    });
  }
  finishBCommentSession(sessionId) {
    return this.request('POST', `/b/comments/sessions/${encodeURIComponent(sessionId)}/finish`);
  }
  listBSessionComments(sessionId, page = 1, pageSize = 100) {
    return this.request('GET',
      `/b/comments/sessions/${encodeURIComponent(sessionId)}/comments?page=${page}&page_size=${pageSize}`);
  }

  // ---- wb comments session (wb_comments 分步会话采集, 2026-10-29) ----
  // 与 dy/ks/b comments session 平行, 路径前缀 /wb/comments; 步进参数为 root_cid
  // 微博主评论每页固定 20 条 (buildComments count 参数无效), 回复按 max_id 游标翻页
  createWbCommentSession(url) {
    // 建会话内含节点免费 probe 探测 (服务端默认 60s 超时), 放宽超时
    return this.request('POST', '/wb/comments/sessions', { body: { url }, timeoutMs: 90000 });
  }
  getWbCommentSession(sessionId) {
    return this.request('GET', `/wb/comments/sessions/${encodeURIComponent(sessionId)}`);
  }
  listWbCommentSessions(page = 1, pageSize = 20, status = '') {
    const q = `?page=${page}&page_size=${pageSize}` +
      (status ? `&status=${encodeURIComponent(status)}` : '');
    return this.request('GET', '/wb/comments/sessions' + q);
  }
  stepWbCommentSession(sessionId, type, rootCid = '') {
    // 步进服务端最长执行 ~180s (翻一页主评论/翻一页回复 + 节点回传), 放宽超时
    return this.request('POST', `/wb/comments/sessions/${encodeURIComponent(sessionId)}/step`, {
      body: { type, root_cid: rootCid }, timeoutMs: 200000,
    });
  }
  finishWbCommentSession(sessionId) {
    return this.request('POST', `/wb/comments/sessions/${encodeURIComponent(sessionId)}/finish`);
  }
  listWbSessionComments(sessionId, page = 1, pageSize = 100) {
    return this.request('GET',
      `/wb/comments/sessions/${encodeURIComponent(sessionId)}/comments?page=${page}&page_size=${pageSize}`);
  }
}

module.exports = { ApiClient, BizError, NetworkError, REQUEST_TIMEOUT_MS, allowInsecureTls };
