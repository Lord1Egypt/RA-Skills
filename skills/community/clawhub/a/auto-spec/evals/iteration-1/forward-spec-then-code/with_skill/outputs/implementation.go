package utils

import (
	"context"
	"log"
	"net/http"
	"net/url"
	"strings"
	"time"
)

func DeduplicateAndValidateImageURLs(ctx context.Context, urls []string) []string {
	if len(urls) == 0 {
		return []string{}
	}

	seen := make(map[string]struct{}, len(urls))
	deduped := make([]string, 0, len(urls))
	for _, rawURL := range urls {
		trimmed := strings.TrimSpace(rawURL)
		if trimmed == "" {
			continue
		}
		if _, exists := seen[trimmed]; exists {
			continue
		}
		seen[trimmed] = struct{}{}
		deduped = append(deduped, trimmed)
	}

	if len(deduped) == 0 {
		return []string{}
	}

	client := &http.Client{
		Timeout: 5 * time.Second,
		CheckRedirect: func(req *http.Request, via []*http.Request) error {
			return http.ErrUseLastResponse
		},
	}

	valid := make([]string, 0, len(deduped))
	for _, u := range deduped {
		parsed, err := url.Parse(u)
		if err != nil || (parsed.Scheme != "http" && parsed.Scheme != "https") {
			log.Printf("[DeduplicateAndValidateImageURLs] invalid URL format, filtered: %s, err: %v", u, err)
			continue
		}

		resp, err := client.Head(u)
		if err != nil {
			log.Printf("[DeduplicateAndValidateImageURLs] HEAD request failed, filtered: %s, err: %s", u, err.Error())
			continue
		}
		resp.Body.Close()

		if resp.StatusCode < 200 || resp.StatusCode >= 300 {
			log.Printf("[DeduplicateAndValidateImageURLs] non-2xx status %d, filtered: %s", resp.StatusCode, u)
			continue
		}

		valid = append(valid, u)
	}

	return valid
}
