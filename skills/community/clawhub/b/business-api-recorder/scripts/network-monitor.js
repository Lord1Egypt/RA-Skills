/**
 * 网络请求监控脚本
 * 注入到页面中，拦截所有fetch/XMLHttpRequest请求
 * 并存储到全局变量中供后续提取
 */

(function() {
    // 存储所有请求记录
    window.__OPENCLAW_NETWORK_LOG__ = {
        requests: [],
        startTime: new Date().toISOString(),
        pageUrl: window.location.href
    };

    // 生成唯一ID
    function generateId() {
        return 'req_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9);
    }

    // 记录请求
    function logRequest(type, data) {
        const record = {
            id: generateId(),
            timestamp: new Date().toISOString(),
            type: type,
            ...data
        };
        window.__OPENCLAW_NETWORK_LOG__.requests.push(record);
        console.log('[OpenClaw Network]', type, data.url || data.method, record);
        return record;
    }

    // ========== 拦截 Fetch ==========
    const originalFetch = window.fetch;
    window.fetch = async function(url, options = {}) {
        const requestId = generateId();
        const startTime = Date.now();
        
        // 记录请求
        const requestRecord = logRequest('fetch_request', {
            requestId: requestId,
            method: options.method || 'GET',
            url: url instanceof Request ? url.url : url.toString(),
            headers: options.headers || {},
            body: options.body || null,
            bodyType: typeof options.body
        });

        try {
            const response = await originalFetch.apply(this, arguments);
            const endTime = Date.now();
            
            // 尝试读取响应体
            let responseBody = null;
            let responseText = null;
            
            try {
                // 克隆响应以便读取
                const clonedResponse = response.clone();
                responseText = await clonedResponse.text();
                
                // 尝试解析为JSON
                try {
                    responseBody = JSON.parse(responseText);
                } catch (e) {
                    responseBody = responseText.substring(0, 5000); // 限制长度
                }
            } catch (e) {
                responseBody = '[无法读取响应体]';
            }

            // 记录响应
            logRequest('fetch_response', {
                requestId: requestId,
                url: requestRecord.url,
                status: response.status,
                statusText: response.statusText,
                headers: Object.fromEntries(response.headers.entries()),
                body: responseBody,
                duration: endTime - startTime
            });

            return response;
        } catch (error) {
            // 记录错误
            logRequest('fetch_error', {
                requestId: requestId,
                url: requestRecord.url,
                error: error.message,
                duration: Date.now() - startTime
            });
            throw error;
        }
    };

    // ========== 拦截 XMLHttpRequest ==========
    const originalXHROpen = XMLHttpRequest.prototype.open;
    const originalXHRSend = XMLHttpRequest.prototype.send;
    const originalXHRSetRequestHeader = XMLHttpRequest.prototype.setRequestHeader;

    XMLHttpRequest.prototype.open = function(method, url, async, user, password) {
        this.__openclaw = {
            id: generateId(),
            method: method,
            url: url,
            async: async,
            headers: {},
            startTime: null
        };
        return originalXHROpen.apply(this, arguments);
    };

    XMLHttpRequest.prototype.setRequestHeader = function(header, value) {
        if (this.__openclaw) {
            this.__openclaw.headers[header] = value;
        }
        return originalXHRSetRequestHeader.apply(this, arguments);
    };

    XMLHttpRequest.prototype.send = function(body) {
        const xhr = this;
        const xhrData = xhr.__openclaw;
        
        if (xhrData) {
            xhrData.startTime = Date.now();
            xhrData.body = body;

            // 记录请求
            logRequest('xhr_request', {
                requestId: xhrData.id,
                method: xhrData.method,
                url: xhrData.url,
                headers: xhrData.headers,
                body: body,
                bodyType: typeof body
            });

            // 监听响应
            xhr.addEventListener('load', function() {
                const endTime = Date.now();
                let responseBody = null;

                try {
                    responseBody = xhr.responseText;
                    try {
                        responseBody = JSON.parse(responseBody);
                    } catch (e) {
                        // 保持文本格式
                    }
                } catch (e) {
                    responseBody = '[无法读取响应]';
                }

                logRequest('xhr_response', {
                    requestId: xhrData.id,
                    url: xhrData.url,
                    status: xhr.status,
                    statusText: xhr.statusText,
                    headers: {}, // XHR不直接暴露响应头
                    body: responseBody,
                    duration: endTime - xhrData.startTime
                });
            });

            xhr.addEventListener('error', function() {
                logRequest('xhr_error', {
                    requestId: xhrData.id,
                    url: xhrData.url,
                    error: 'XHR error',
                    duration: Date.now() - xhrData.startTime
                });
            });
        }

        return originalXHRSend.apply(this, arguments);
    };

    // ========== 辅助函数 ==========
    
    // 获取所有请求记录
    window.__openclaw_getNetworkLog = function() {
        return window.__OPENCLAW_NETWORK_LOG__;
    };

    // 清空记录
    window.__openclaw_clearNetworkLog = function() {
        window.__OPENCLAW_NETWORK_LOG__ = {
            requests: [],
            startTime: new Date().toISOString(),
            pageUrl: window.location.href
        };
    };

    // 导出为JSON
    window.__openclaw_exportNetworkLog = function() {
        return JSON.stringify(window.__OPENCLAW_NETWORK_LOG__, null, 2);
    };

    // 按类型筛选
    window.__openclaw_filterRequests = function(type) {
        return window.__OPENCLAW_NETWORK_LOG__.requests.filter(r => r.type === type);
    };

    // 按URL筛选
    window.__openclaw_filterByUrl = function(pattern) {
        const regex = new RegExp(pattern, 'i');
        return window.__OPENCLAW_NETWORK_LOG__.requests.filter(r => 
            r.url && regex.test(r.url)
        );
    };

    // 统计信息
    window.__openclaw_getStats = function() {
        const logs = window.__OPENCLAW_NETWORK_LOG__;
        const requests = logs.requests;
        
        return {
            totalRequests: requests.filter(r => r.type.includes('request') && !r.type.includes('response')).length,
            fetchRequests: requests.filter(r => r.type === 'fetch_request').length,
            xhrRequests: requests.filter(r => r.type === 'xhr_request').length,
            errors: requests.filter(r => r.type.includes('error')).length,
            uniqueUrls: [...new Set(requests.filter(r => r.url).map(r => r.url))].length,
            pageUrl: logs.pageUrl,
            startTime: logs.startTime
        };
    };

    console.log('[OpenClaw] 网络监控已启动');
    console.log('[OpenClaw] 使用 __openclaw_getNetworkLog() 获取所有记录');
    console.log('[OpenClaw] 使用 __openclaw_getStats() 获取统计信息');
})();
