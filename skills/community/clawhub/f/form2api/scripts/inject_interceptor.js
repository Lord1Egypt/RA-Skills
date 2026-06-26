/**
 * Form-to-API 网络拦截器
 * 注入到目标页面，Hook fetch + XHR，捕获所有网络请求
 * 使用方式：通过 CDP Runtime.evaluate 注入到页面
 */

(function () {
  if (window.__formApiInterceptorActive) {
    return { status: 'already_active', count: window.__capturedRequests.length };
  }

  window.__capturedRequests = [];
  window.__formApiInterceptorActive = true;
  window.__interceptorStartTime = Date.now();

  // ---- Hook fetch ----
  const origFetch = window.fetch;
  window.fetch = async function (...args) {
    const [input, options = {}] = args;
    const url = typeof input === 'string' ? input : (input.url || String(input));
    const method = (options.method || (input.method) || 'GET').toUpperCase();

    let requestBody = null;
    try {
      if (options.body) {
        requestBody = typeof options.body === 'string' ? options.body : JSON.stringify(options.body);
      }
    } catch (e) {}

    let requestHeaders = {};
    try {
      if (options.headers) {
        if (options.headers instanceof Headers) {
          options.headers.forEach((v, k) => { requestHeaders[k] = v; });
        } else {
          requestHeaders = { ...options.headers };
        }
      }
    } catch (e) {}

    const result = await origFetch.apply(this, args);
    const clone = result.clone();
    let responseBody = '';
    try { responseBody = await clone.text(); } catch (e) {}

    window.__capturedRequests.push({
      type: 'fetch',
      url,
      method,
      requestHeaders,
      requestBody,
      responseStatus: result.status,
      responseBody,
      timestamp: Date.now()
    });

    return result;
  };

  // ---- Hook XHR ----
  const origOpen = XMLHttpRequest.prototype.open;
  const origSend = XMLHttpRequest.prototype.send;
  const origSetHeader = XMLHttpRequest.prototype.setRequestHeader;

  XMLHttpRequest.prototype.open = function (method, url) {
    this.__xhrMethod = method ? method.toUpperCase() : 'GET';
    this.__xhrUrl = url;
    this.__xhrHeaders = {};
    return origOpen.apply(this, arguments);
  };

  XMLHttpRequest.prototype.setRequestHeader = function (name, value) {
    if (this.__xhrHeaders) this.__xhrHeaders[name] = value;
    return origSetHeader.apply(this, arguments);
  };

  XMLHttpRequest.prototype.send = function (body) {
    const self = this;
    this.addEventListener('loadend', function () {
      window.__capturedRequests.push({
        type: 'xhr',
        url: self.__xhrUrl || '',
        method: self.__xhrMethod || 'GET',
        requestHeaders: self.__xhrHeaders || {},
        requestBody: body || null,
        responseStatus: self.status,
        responseBody: self.responseText || '',
        timestamp: Date.now()
      });
    });
    return origSend.apply(this, arguments);
  };

  return { status: 'injected', message: 'Interceptor active. Submit the form now.' };
})();
