# 网络与安全面试题

## 初级

### 1. HTTP 和 HTTPS 的区别？

**考察点**：协议基础、安全意识

**参考答案**：
- HTTP 明文传输，HTTPS = HTTP + TLS/SSL 加密
- HTTPS 需要 CA 证书，默认端口 443（HTTP 是 80）
- HTTPS 防止中间人攻击、数据篡改、窃听

**TLS 握手简述**：
1. Client Hello（支持的加密套件、随机数）
2. Server Hello + 证书
3. 客户端验证证书，生成 Pre-Master Secret，用服务器公钥加密发送
4. 双方用三个随机数生成 Session Key，后续对称加密通信

---

### 2. HTTP 状态码有哪些，各自含义？

**考察点**：HTTP 基础

**参考答案**：
- **2xx 成功**：200 OK、201 Created、204 No Content
- **3xx 重定向**：301 永久重定向、302 临时重定向、304 Not Modified
- **4xx 客户端错误**：400 Bad Request、401 Unauthorized、403 Forbidden、404 Not Found
- **5xx 服务端错误**：500 Internal Server Error、502 Bad Gateway、503 Service Unavailable

---

### 3. 什么是 Cookie 和 Session？区别是什么？

**考察点**：状态管理基础

**参考答案**：
- **Cookie**：存储在浏览器，随请求自动携带，可设置过期时间
- **Session**：存储在服务端，通过 Session ID（通常存在 Cookie 中）标识用户

| 对比 | Cookie | Session |
|------|--------|---------|
| 存储位置 | 浏览器 | 服务器 |
| 安全性 | 较低（可被篡改） | 较高 |
| 容量 | ~4KB | 无限制 |
| 性能 | 不占服务器资源 | 占服务器内存 |

---

## 中级

### 4. HTTP/1.1、HTTP/2、HTTP/3 的区别？

**考察点**：协议演进、性能优化

**参考答案**：

**HTTP/1.1**：
- 持久连接（Keep-Alive），但同一连接串行处理请求
- 队头阻塞问题（Head-of-Line Blocking）
- 通过多域名分片、雪碧图等方式优化

**HTTP/2**：
- 二进制分帧（Binary Framing）
- 多路复用（Multiplexing）：一个连接并行多个请求流
- 头部压缩（HPACK）
- 服务器推送（Server Push）
- 仍存在 TCP 层队头阻塞

**HTTP/3**：
- 基于 QUIC 协议（UDP），彻底解决队头阻塞
- 0-RTT 或 1-RTT 建立连接
- 连接迁移（切换网络不断连）

---

### 5. 什么是 CORS？如何解决跨域问题？

**考察点**：浏览器安全、跨域方案

**参考答案**：

CORS（Cross-Origin Resource Sharing）：浏览器同源策略限制跨域请求，服务端通过响应头允许跨域。

**简单请求**（GET/POST + 普通 headers）：
```http
# 服务端响应头
Access-Control-Allow-Origin: https://example.com
Access-Control-Allow-Credentials: true
```

**预检请求**（OPTIONS）：非简单请求先发 OPTIONS：
```http
Access-Control-Allow-Origin: *
Access-Control-Allow-Methods: GET, POST, PUT, DELETE
Access-Control-Allow-Headers: Content-Type, Authorization
Access-Control-Max-Age: 86400
```

**其他跨域方案**：
- 开发环境：Vite/Webpack devServer proxy
- JSONP：仅 GET，已过时
- Nginx 反向代理：生产常用
- PostMessage：iframe 通信

---

### 6. XSS 和 CSRF 攻击原理及防御？

**考察点**：前端安全

**参考答案**：

**XSS（跨站脚本攻击）**：
- 原理：注入恶意脚本到页面，窃取 Cookie/劫持会话
- 类型：存储型（持久）、反射型（URL参数）、DOM型
- 防御：
  ```js
  // 1. 输出编码
  const escape = (str) => str.replace(/[&<>"']/g, (c) => ({
    '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;'
  })[c])
  
  // 2. CSP 响应头
  Content-Security-Policy: default-src 'self'; script-src 'self'
  
  // 3. HttpOnly Cookie（JS无法读取）
  Set-Cookie: token=xxx; HttpOnly; Secure; SameSite=Strict
  ```

**CSRF（跨站请求伪造）**：
- 原理：利用用户已登录状态，诱导发起恶意请求
- 防御：
  ```js
  // 1. CSRF Token（表单/请求头携带）
  headers: { 'X-CSRF-Token': getCsrfToken() }
  
  // 2. SameSite Cookie
  Set-Cookie: session=xxx; SameSite=Strict
  
  // 3. 检查 Referer/Origin
  ```

---

## 高级

### 7. JWT 和 Cookie-Session 方案如何选择？

**考察点**：认证方案设计

**参考答案**：

**JWT（JSON Web Token）**：
```
Header.Payload.Signature
// Payload 包含用户信息，服务端无需存储状态
```

| 对比 | JWT | Cookie-Session |
|------|-----|----------------|
| 服务端存储 | 无状态 | 需存储 Session |
| 横向扩展 | 天然支持 | 需共享 Session（Redis） |
| 注销 | 困难（需黑名单） | 直接删除 Session |
| 安全性 | Payload 可解码（非加密） | 服务端控制 |
| 适用场景 | 微服务、移动端、跨域 | 传统 Web 应用 |

**最佳实践**：
- Access Token 短期（15min） + Refresh Token 长期（7天）
- Refresh Token 存 HttpOnly Cookie，Access Token 存内存
- 注销时将 Refresh Token 加黑名单

---

### 8. 浏览器缓存策略详解？

**考察点**：缓存机制、性能优化

**参考答案**：

**强缓存**（不发请求）：
```http
Cache-Control: max-age=31536000, immutable  # 推荐
Expires: Wed, 01 Jan 2026 00:00:00 GMT      # 旧方式
```

**协商缓存**（发请求验证）：
```http
# 服务端返回
Last-Modified: Tue, 01 Apr 2026 12:00:00 GMT
ETag: "abc123"

# 客户端请求携带
If-Modified-Since: Tue, 01 Apr 2026 12:00:00 GMT
If-None-Match: "abc123"
# 未变化 → 304 Not Modified
```

**最佳实践**：
- HTML：`Cache-Control: no-cache`（每次验证）
- JS/CSS（带 hash）：`Cache-Control: max-age=31536000, immutable`
- API：`Cache-Control: no-store`

**缓存优先级**：Service Worker > Memory Cache > Disk Cache > 网络请求
