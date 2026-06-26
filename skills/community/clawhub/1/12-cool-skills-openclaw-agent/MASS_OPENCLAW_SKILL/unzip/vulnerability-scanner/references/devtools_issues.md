# Common DevTools Issues and How to Check Them

This document outlines common security-related issues that can be identified using browser developer tools (DevTools).

## 1. Exposed API Keys or Sensitive Information

**How to check:**
- Open DevTools (F12 or Ctrl+Shift+I).
- Go to the `Network` tab and refresh the page. Inspect requests and responses for hardcoded API keys, tokens, or other sensitive data.
- Go to the `Sources` tab and browse JavaScript files for embedded credentials.
- Check `Application` -> `Local Storage`, `Session Storage`, and `Cookies` for sensitive data.

## 2. Insecure Communications (Mixed Content)

**How to check:**
- Open DevTools and go to the `Console` tab.
- Look for warnings related to "Mixed Content" (HTTP resources loaded on an HTTPS page). This indicates potential vulnerabilities to eavesdropping or content injection.

## 3. Client-Side Input Validation Bypass

**How to check:**
- Identify input fields on the website.
- Use the `Elements` tab to remove or modify client-side validation attributes (e.g., `maxlength`, `pattern`, `required`).
- Attempt to submit invalid data. If the server accepts it, client-side validation is not backed by server-side validation, which is a security risk.

## 4. Unhandled JavaScript Errors

**How to check:**
- Go to the `Console` tab.
- Look for unhandled JavaScript errors that might reveal internal application logic, file paths, or debugging information that should not be exposed to the client.

## 5. Security Headers Missing or Misconfigured

**How to check:**
- Go to the `Network` tab and select the main document request.
- In the `Headers` section, inspect the `Response Headers` for security-related headers like:
    - `Content-Security-Policy` (CSP)
    - `X-Content-Type-Options`
    - `X-Frame-Options`
    - `Strict-Transport-Security` (HSTS)
- Missing or improperly configured headers can lead to various attacks (e.g., XSS, clickjacking).

## 6. Excessive Information in Responses

**How to check:**
- In the `Network` tab, inspect API responses.
- Look for excessive information in error messages or standard responses, such as stack traces, database error messages, or internal system details. This information can aid attackers.

## 7. DOM-based XSS (Cross-Site Scripting)

**How to check:**
- In the `Sources` tab, set breakpoints in JavaScript code that manipulates the DOM using user-controlled input.
- Test various XSS payloads in URL parameters or input fields and observe if they are reflected unsanitized in the DOM.

## 8. Insecure Direct Object References (IDOR)

**How to check:**
- Identify requests that use predictable IDs (e.g., `user_id=123`).
- Modify the ID in the request (e.g., `user_id=124`) and observe if you can access resources you shouldn't have access to without proper authorization.

## 9. Weak Authentication/Session Management

**How to check:**
- In the `Application` tab, inspect cookies and local/session storage.
- Look for session tokens that are easily guessable, don't expire, or are transmitted over insecure channels.
- Try to reuse expired session tokens or manipulate them.

## 10. Outdated Libraries/Frameworks

**How to check:**
- In the `Sources` tab, examine the loaded JavaScript libraries and their versions.
- Use online tools or vulnerability databases to check if these versions have known vulnerabilities.
