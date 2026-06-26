# DeduplicateAndValidateImageURLs Spec

## Overview

A utility function that accepts a list of user-uploaded image URLs, deduplicates them, validates their accessibility, and returns the deduplicated list of accessible URLs. Invalid URLs are filtered out and logged.

## Glossary

- **Deduplication**: exact-string deduplication of full URLs, preserving the order of first occurrence.
- **Accessibility validation**: sending an HTTP HEAD request to the URL and checking whether the response status code is 2xx.
- **Invalid URL**: a URL that is malformed (cannot be parsed) or fails accessibility validation (network error or non-2xx status code).

## Behavioral Contracts

### Scenario 1: Normal deduplication and validation

- **Precondition**: none
- **Input**: `ctx context.Context`, `urls []string` (list of user-uploaded image URLs)
- **Expected behavior**:
  1. Deduplicate `urls` in order of appearance (keep the first occurrence, discard subsequent duplicates)
  2. Validate the format of each deduplicated URL (`net/url.Parse` and scheme must be http/https)
  3. Send an HTTP HEAD request (5-second timeout) to each format-valid URL and check whether the status code is 2xx
  4. Return all URLs that pass validation (preserving original order)
- **Postcondition**: the returned list has no duplicates and every URL is accessible
- **Example**:
  ```
  Input:  ["https://a.com/1.jpg", "https://b.com/2.jpg", "https://a.com/1.jpg", "https://c.com/3.jpg"]
  Assume https://c.com/3.jpg returns 404
  Output: ["https://a.com/1.jpg", "https://b.com/2.jpg"]
  Log:    records that https://c.com/3.jpg failed validation
  ```

### Scenario 2: Empty list input

- **Precondition**: none
- **Input**: `urls` is `nil` or an empty slice
- **Expected behavior**: return an empty slice immediately without making any network requests
- **Postcondition**: returns `[]string{}` (non-nil empty slice)

### Scenario 3: All duplicates

- **Precondition**: none
- **Input**: all elements in `urls` are identical, e.g. `["https://a.com/1.jpg", "https://a.com/1.jpg"]`
- **Expected behavior**: after deduplication, only one URL remains; validate it
- **Postcondition**: returns a slice with 0 or 1 element

### Scenario 4: Malformed URL

- **Precondition**: none
- **Input**: `urls` contains malformed strings, e.g. `"not-a-url"`, `"ftp://x.com/a.jpg"`, `""`
- **Expected behavior**:
  1. Malformed URLs are filtered out immediately without making a network request
  2. Log the filtered URL and reason via `log.Warn`
- **Postcondition**: the returned list contains no malformed URLs

### Scenario 5: Network timeout or request failure

- **Precondition**: the target server is unreachable or the response times out
- **Input**: a list containing unreachable URLs
- **Expected behavior**:
  1. A HEAD request that times out after 5 seconds is treated as inaccessible
  2. Log the failed URL and error message via `log.Warn`
  3. Does not affect validation of other URLs (each URL is validated independently)
- **Postcondition**: only URLs that pass validation are returned

### Scenario 6: Whitespace in URLs

- **Precondition**: none
- **Input**: URLs may have leading or trailing whitespace, e.g. `" https://a.com/1.jpg "`
- **Expected behavior**: apply `strings.TrimSpace` to each URL before deduplication and validation
- **Postcondition**: returned URLs have no leading or trailing whitespace

## Constraints & Boundaries

- **Performance**: single HEAD request timeout is 5 seconds; the function does not validate concurrently (sequential) — callers can wrap it in goroutines if concurrency is needed.
- **What we don't do**:
  - Does not download image content — only validates accessibility (HEAD request)
  - Does not normalize URLs (e.g., case normalization, query parameter sorting) — deduplication is exact string matching after TrimSpace
  - Does not retry failed requests

## Dependencies

- `context`: standard library, for passing context
- `net/http`: standard library, for HEAD requests
- `net/url`: standard library, for URL format validation
- Project logging library: for recording invalid URLs

## Function Signature

```go
func DeduplicateAndValidateImageURLs(ctx context.Context, urls []string) []string
```

## Open Questions

None.
