# Spec: Image URL Deduplication and Accessibility Validation Utility

## 1. Background & Goal

When users upload images, the client may send duplicate or invalid image URLs. A utility function is needed to:

1. **Deduplicate** — preserve the order of first occurrence, remove duplicates.
2. **Validate accessibility** — send an HTTP HEAD request to each URL and confirm a 2xx status code.
3. **Filter and log** — invalid URLs are filtered out and logged for debugging.

## 2. Function Signature

```go
package utils

func DeduplicateAndValidateImageURLs(
    ctx context.Context,
    urls []string,
    timeout time.Duration,
) (validURLs []string, invalidURLs []string)
```

## 3. Detailed Design

### 3.1 Deduplication strategy

- Use `map[string]struct{}` to track seen URLs.
- Iterate the input list, skip already-seen URLs, preserve first-occurrence order.
- Apply `strings.TrimSpace` to each URL before deduplication; skip empty strings.

### 3.2 URL format validation

- Parse with `net/url.Parse`.
- Scheme must be `http` or `https`.
- Host must be non-empty.
- Malformed URLs are logged as warn and added to `invalidURLs`.

### 3.3 Accessibility validation

- Create a HEAD request with `http.NewRequestWithContext` bound to a timeout context.
- Status codes in the 200–399 range are considered accessible.
- Network errors or non-2xx/3xx status codes are logged as warn and added to `invalidURLs`.

### 3.4 Concurrency control

- Use `sync.WaitGroup` + a buffered channel semaphore for concurrent validation, default concurrency: 10.
- Results are collected via a channel and reordered to match the original input order.

### 3.5 Logging conventions

- Duplicate URL: `log.Info("duplicate url skipped: %s", url)`
- Malformed URL: `log.Warn("invalid url format: %s, err: %v", url, err)`
- Inaccessible URL: `log.Warn("url not accessible: %s, status: %d", url, statusCode)`
- Request failure: `log.Warn("url check failed: %s, err: %v", url, err)`

### 3.6 Edge cases

| Scenario | Behavior |
|----------|----------|
| Input is nil or empty slice | Return two empty slices |
| All URLs are invalid | validURLs is empty; invalidURLs contains all invalid URLs |
| All URLs are valid and unique | invalidURLs is empty |
| URL has leading/trailing whitespace | TrimSpace before processing |
| URL is an empty string | Skip; not counted in any return value |
| Timeout | Treated as inaccessible; logged |

## 4. Dependencies

- Standard library: `context`, `net/http`, `net/url`, `strings`, `sync`, `time`
- Project logging library

## 5. Test Points

1. Empty input returns empty slices.
2. Duplicate URLs — only the first occurrence is kept.
3. Malformed URLs are filtered into `invalidURLs`.
4. Inaccessible URLs are filtered into `invalidURLs`.
5. Valid URLs preserve original order.
6. Concurrency safety (large URL input).
7. Timeout scenario.
