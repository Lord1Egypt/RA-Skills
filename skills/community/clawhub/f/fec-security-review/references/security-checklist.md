# 前端安全审查清单

## XSS

- `dangerouslySetInnerHTML` 和 `v-html` 必须有明确理由和输入净化。
- 用户输入不得直接插入 DOM、`innerHTML`、`document.write`。
- URL 参数不得直接用于页面渲染。
- 动态生成的 `<script>` 标签必须审查来源。
- 富文本使用 DOMPurify 等库，并配置标签、属性、协议白名单。

```ts
import DOMPurify from "dompurify";

const clean = DOMPurify.sanitize(dirtyHtml, {
  ALLOWED_TAGS: ["b", "i", "em", "strong", "a", "ul", "ol", "li", "p", "br"],
  ALLOWED_ATTR: ["href", "title"],
  ALLOWED_URI_REGEXP: /^(https?|mailto):/i,
});
```

## 安全重定向

```ts
function safeRedirect(url: string): string {
  if (url.startsWith("/") && !url.startsWith("//")) return url;
  return "/dashboard";
}
```

## CSP

- 推荐先用 `Content-Security-Policy-Report-Only` 验证。
- `default-src 'self'`、`object-src 'none'`、`frame-ancestors 'none'`、`base-uri 'self'` 是常见底线。
- 避免 `'unsafe-eval'`；内联脚本优先 nonce。

```http
Content-Security-Policy: default-src 'self'; script-src 'self'; object-src 'none'; frame-ancestors 'none'; base-uri 'self'; form-action 'self';
```

## 敏感数据

- 禁止前端硬编码 API Key、Secret、密码。
- 禁止 localStorage/sessionStorage/IndexedDB 存明文 token、密码、信用卡信息。
- 禁止 URL query 参数传 token 或密码。
- 禁止 console.log 或错误上报携带隐私数据。
- Token 优先 httpOnly + Secure + SameSite cookie。

## CSRF

- 变更操作必须携带 CSRF token 或使用同等后端防护。
- 关键操作不要使用 GET。
- 检查后端是否校验 `Origin` / `Referer`。

## 依赖与第三方脚本

- 定期审查依赖安全公告。
- 禁止从非官方 CDN 加载脚本，除非有 SRI 和来源审查。
- 动态加载第三方脚本必须有业务必要性和降级策略。

## 输入校验与文件上传

- 前端校验不是安全边界，后端必须二次校验。
- 文件上传校验 MIME、大小、扩展名和内容；不能只看扩展名。
- 正则校验注意 ReDoS 风险。
