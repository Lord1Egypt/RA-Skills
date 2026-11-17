---
name: fec-browser-storage
description: Use when choosing, implementing, or reviewing browser storage such as localStorage, sessionStorage, IndexedDB, cookies, client persistence, offline data, secure storage, or cleanup strategy; Chinese triggers include browser storage, client persistence.
---

# Browser storage

## Purpose

Choose the appropriate client storage solution based on data size, security requirements, and lifecycle.

## Procedure

1. First determine the data sensitivity, volume, life cycle, whether it needs to be spread across tabs, and whether it needs to be sent with the request.
2. Use localStorage for a small amount of non-sensitive preferences; use sessionStorage for tab-level temporary data; use IndexedDB for large amounts of structured data or offline caching; prioritize httpOnly cookies for authentication status.
3. Encapsulate unified key prefix, JSON parse/stringify, exception handling, expiration cleanup and quota protection.
4. Sensitive data is processed according to security rules, and plain text tokens, passwords, and credit card information are not put into storage that can be read by JS.
5. Review privacy mode, storage quotas, sanitization policies, and cross-browser compatibility.

## Detailed reference

Load [references/storage-patterns.md](references/storage-patterns.md) when it comes to storage selection tables, localStorage/sessionStorage wrappers, IndexedDB examples, cookie helpers, and sensitive data rules.

## Constraints

- localStorage/sessionStorage is a synchronous API, and big data reading and writing will block the main thread.
- Except for httpOnly cookies, client-side storage can be read by XSS.
- Cookies are automatically carried with each request and are not suitable for big data.
- There are browser differences in IndexedDB quota and privacy mode behavior.
- Do not pass token or sensitive data in the URL.

## Expected Output

Produce a unified storage/cookie/db package, the key has a namespace, the data has an expiration or cleanup policy, and sensitive data only enters the appropriate security boundary.
