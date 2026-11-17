# HTTP 重试技能

**触发词**: timeouterror, econnreset, econnrefused, 429, retry, http error

## 问题
网络请求失败（超时、连接重置、限流）导致服务不稳定

## 解决方案
实现通用 HTTP 重试机制：
1. 指数退避（1s, 2s, 4s, 8s...）
2. AbortController 超时控制
3. 连接池复用
4. 状态码识别（5xx, 429 重试）

## 核心代码
```javascript
async function fetchWithRetry(url, options = {}, maxRetries = 3) {
  const { retryDelay = 1000, timeout = 30000, ...fetchOptions } = options;
  
  for (let attempt = 0; attempt <= maxRetries; attempt++) {
    try {
      const controller = new AbortController();
      const timeoutId = setTimeout(() => controller.abort(), timeout);
      
      const response = await fetch(url, {
        ...fetchOptions,
        signal: controller.signal
      });
      
      clearTimeout(timeoutId);
      
      // 429 或 5xx 重试
      if (response.status === 429 || response.status >= 500) {
        const delay = retryDelay * Math.pow(2, attempt);
        await new Promise(r => setTimeout(r, delay));
        continue;
      }
      
      return response;
    } catch (err) {
      if (attempt === maxRetries) throw err;
      await new Promise(r => setTimeout(r, retryDelay * Math.pow(2, attempt)));
    }
  }
}
```
