package common

import (
	"fmt"
	"time"
)

// ParseTime parses a time string to millisecond timestamp.
// Supports: unix ms, "15 minutes ago", "1 hour ago", "today", "yesterday",
// "2006-01-02 15:04:05", "2006-01-02"
func ParseTime(s string) (int64, error) {
	if s == "" {
		return 0, fmt.Errorf("时间参数不能为空")
	}

	now := time.Now()

	switch s {
	case "now":
		return now.UnixMilli(), nil
	case "today":
		t := time.Date(now.Year(), now.Month(), now.Day(), 0, 0, 0, 0, now.Location())
		return t.UnixMilli(), nil
	case "yesterday":
		t := time.Date(now.Year(), now.Month(), now.Day()-1, 0, 0, 0, 0, now.Location())
		return t.UnixMilli(), nil
	}

	// Try relative time: "15 minutes ago", "1 hour ago", "2 days ago"
	var amount int
	var unit string
	if n, _ := fmt.Sscanf(s, "%d %s ago", &amount, &unit); n == 2 {
		unit = trimTrailingS(unit)
		var d time.Duration
		switch unit {
		case "second":
			d = time.Duration(amount) * time.Second
		case "minute":
			d = time.Duration(amount) * time.Minute
		case "hour":
			d = time.Duration(amount) * time.Hour
		case "day":
			d = time.Duration(amount) * 24 * time.Hour
		default:
			return 0, fmt.Errorf("不支持的时间单位: %s", unit)
		}
		return now.Add(-d).UnixMilli(), nil
	}

	// Try absolute time formats
	layouts := []string{
		"2006-01-02 15:04:05",
		"2006-01-02T15:04:05",
		"2006-01-02",
		"2006/01/02 15:04:05",
		"2006/01/02",
	}
	for _, layout := range layouts {
		if t, err := time.ParseInLocation(layout, s, now.Location()); err == nil {
			return t.UnixMilli(), nil
		}
	}

	// Try direct unix timestamp (ms or seconds)
	var ts int64
	if n, _ := fmt.Sscanf(s, "%d", &ts); n == 1 {
		if ts > 1e12 {
			return ts, nil // already ms
		}
		return ts * 1000, nil // seconds to ms
	}

	return 0, fmt.Errorf("无法解析时间: %s", s)
}

func trimTrailingS(s string) string {
	if len(s) > 1 && s[len(s)-1] == 's' {
		return s[:len(s)-1]
	}
	return s
}

// DefaultTimeRange returns (from, to) as ms timestamps for the last N minutes.
func DefaultTimeRange(minutes int) (int64, int64) {
	now := time.Now()
	to := now.UnixMilli()
	from := now.Add(-time.Duration(minutes) * time.Minute).UnixMilli()
	return from, to
}
