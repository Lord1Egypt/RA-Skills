# Front-end security review checklist

## XSS

- `dangerouslySetInnerHTML` and `v-html` must have explicit reason and input sanitization.
- User input must not be inserted directly into the DOM, `innerHTML`, `document.write`.
- URL parameters must not be used directly in page rendering.
- Dynamically generated `<script>` tags must be sourced.
- Rich text uses libraries such as DOMPurify and configures tags, attributes, and protocol whitelists.

```ts
import DOMPurify from "dompurify";

const clean = DOMPurify.sanitize(dirtyHtml, {
  ALLOWED_TAGS: ["b", "i", "em", "strong", "a", "ul", "ol", "li", "p", "br"],
  ALLOWED_ATTR: ["href", "title"],
  ALLOWED_URI_REGEXP: /^(https?|mailto):/i,
});
```

## Safe redirection

```ts
function safeRedirect(url: string): string {
  if (url.startsWith("/") && !url.startsWith("//")) return url;
  return "/dashboard";
}
```

## CSP

- It is recommended to verify with `Content-Security-Policy-Report-Only` first.
- `default-src 'self'`, `object-src 'none'`, `frame-ancestors 'none'`, `base-uri 'self'` are common bottom lines.
- Avoid `'unsafe-eval''; inline scripts take precedence over nonce.

```http
Content-Security-Policy: default-src 'self'; script-src 'self'; object-src 'none'; frame-ancestors 'none'; base-uri 'self'; form-action 'self';
```

## Sensitive data

- It is prohibited to hard-code API Key, Secret, and password on the front end.
- LocalStorage/sessionStorage/IndexedDB is prohibited from storing plain text tokens, passwords, and credit card information.
- Prohibit URL query parameters from passing token or password.
- Console.log or error reports are prohibited from carrying private data.
- Token priority httpOnly + Secure + SameSite cookie.

## CSRF

- Change operations must carry CSRF tokens or use equivalent backend protection.
- Do not use GET for critical operations.
- Check whether the backend verifies `Origin` / `Referer`.

## Dependencies and third-party scripts

- Regularly review dependency security bulletins.
- Disallow script loading from unofficial CDNs unless SRI and source vetted.
- Dynamically loading third-party scripts must have business necessity and a downgrade strategy.

## Input verification and file upload

- Front-end verification is not a security boundary, and the back-end must be verified twice.
- File uploads verify MIME, size, extension and content; don't just look at the extension.
- Pay attention to ReDoS risks in regular verification.
