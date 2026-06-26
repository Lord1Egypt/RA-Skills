package utils

import (
	"context"
	"log"
	"net/http"
	"net/url"
	"strings"
	"sync"
	"time"
)

type urlCheckResult struct {
	index int
	url   string
	valid bool
}

func DeduplicateAndValidateImageURLs(
	ctx context.Context,
	urls []string,
	timeout time.Duration,
) (validURLs []string, invalidURLs []string) {
	if len(urls) == 0 {
		return nil, nil
	}

	seen := make(map[string]struct{}, len(urls))
	uniqueURLs := make([]string, 0, len(urls))

	for _, rawURL := range urls {
		trimmed := strings.TrimSpace(rawURL)
		if trimmed == "" {
			continue
		}
		if _, exists := seen[trimmed]; exists {
			log.Printf("[DeduplicateAndValidateImageURLs] duplicate url skipped: %s", trimmed)
			continue
		}
		seen[trimmed] = struct{}{}
		uniqueURLs = append(uniqueURLs, trimmed)
	}

	if len(uniqueURLs) == 0 {
		return nil, nil
	}

	const maxConcurrency = 10

	client := &http.Client{
		Timeout: timeout,
		CheckRedirect: func(req *http.Request, via []*http.Request) error {
			if len(via) >= 10 {
				return http.ErrUseLastResponse
			}
			return nil
		},
	}

	resultCh := make(chan urlCheckResult, len(uniqueURLs))
	semaphore := make(chan struct{}, maxConcurrency)
	var wg sync.WaitGroup

	for i, u := range uniqueURLs {
		wg.Add(1)
		go func(idx int, rawURL string) {
			defer wg.Done()
			semaphore <- struct{}{}
			defer func() { <-semaphore }()

			valid := checkImageURL(ctx, client, rawURL, timeout)
			resultCh <- urlCheckResult{index: idx, url: rawURL, valid: valid}
		}(i, u)
	}

	go func() {
		wg.Wait()
		close(resultCh)
	}()

	results := make([]urlCheckResult, len(uniqueURLs))
	for r := range resultCh {
		results[r.index] = r
	}

	validURLs = make([]string, 0, len(uniqueURLs))
	invalidURLs = make([]string, 0)

	for _, r := range results {
		if r.valid {
			validURLs = append(validURLs, r.url)
		} else {
			invalidURLs = append(invalidURLs, r.url)
		}
	}

	return validURLs, invalidURLs
}

func checkImageURL(ctx context.Context, client *http.Client, rawURL string, timeout time.Duration) bool {
	parsed, err := url.Parse(rawURL)
	if err != nil {
		log.Printf("[DeduplicateAndValidateImageURLs] invalid url format: %s, err: %v", rawURL, err)
		return false
	}
	if parsed.Scheme != "http" && parsed.Scheme != "https" {
		log.Printf("[DeduplicateAndValidateImageURLs] invalid url scheme: %s, url: %s", parsed.Scheme, rawURL)
		return false
	}
	if parsed.Host == "" {
		log.Printf("[DeduplicateAndValidateImageURLs] empty host in url: %s", rawURL)
		return false
	}

	reqCtx, cancel := context.WithTimeout(ctx, timeout)
	defer cancel()

	req, err := http.NewRequestWithContext(reqCtx, http.MethodHead, rawURL, nil)
	if err != nil {
		log.Printf("[DeduplicateAndValidateImageURLs] create request failed: %s, err: %v", rawURL, err)
		return false
	}

	resp, err := client.Do(req)
	if err != nil {
		log.Printf("[DeduplicateAndValidateImageURLs] url check failed: %s, err: %v", rawURL, err)
		return false
	}
	defer resp.Body.Close()

	if resp.StatusCode >= 200 && resp.StatusCode < 400 {
		return true
	}

	log.Printf("[DeduplicateAndValidateImageURLs] url not accessible: %s, status: %d", rawURL, resp.StatusCode)
	return false
}
