# HTTP Traps

- `HttpClient` returns cold Observable — each `subscribe()` fires new request, use `shareReplay`
- Interceptor must call `next.handle()` — omitting silently drops request
- Interceptor order matters — last registered runs first (innermost), auth should be early
- `responseType: 'text'` required for non-JSON — default JSON parse throws on HTML error pages
- `catchError` in interceptor must rethrow — swallowing breaks error handling downstream
- `withCredentials: true` needed for cookies cross-origin — CORS also needs server config
- Retry on error without delay hammers server — use `retry({ count: 3, delay: 1000 })`
