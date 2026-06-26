package output

import (
	"encoding/csv"
	"encoding/json"
	"fmt"
	"io"
	"os"
	"sort"
	"strings"
)

type Format int

const (
	FormatJSON Format = iota
	FormatPretty
	FormatTable
	FormatCSV
)

func ParseFormat(s string) Format {
	switch strings.ToLower(s) {
	case "pretty":
		return FormatPretty
	case "table":
		return FormatTable
	case "csv":
		return FormatCSV
	default:
		return FormatJSON
	}
}

func PrintJSON(w io.Writer, data interface{}) {
	enc := json.NewEncoder(w)
	enc.SetEscapeHTML(false)
	_ = enc.Encode(data)
}

func PrintPretty(w io.Writer, data interface{}) {
	b, err := json.MarshalIndent(data, "", "  ")
	if err != nil {
		PrintJSON(w, data)
		return
	}
	fmt.Fprintln(w, string(b))
}

func PrintTable(w io.Writer, data interface{}) {
	items := extractItems(data)
	if len(items) == 0 {
		PrintPretty(w, data)
		return
	}
	keys := collectKeys(items)
	if len(keys) == 0 {
		PrintPretty(w, data)
		return
	}

	widths := make(map[string]int)
	for _, k := range keys {
		widths[k] = len(k)
	}
	rows := make([]map[string]string, len(items))
	for i, item := range items {
		row := make(map[string]string)
		for _, k := range keys {
			v := formatValue(item[k])
			row[k] = v
			if len(v) > widths[k] {
				widths[k] = len(v)
			}
		}
		rows[i] = row
	}

	header := ""
	sep := ""
	for _, k := range keys {
		header += fmt.Sprintf("%-*s  ", widths[k], k)
		sep += strings.Repeat("-", widths[k]) + "  "
	}
	fmt.Fprintln(w, strings.TrimRight(header, " "))
	fmt.Fprintln(w, strings.TrimRight(sep, " "))
	for _, row := range rows {
		line := ""
		for _, k := range keys {
			line += fmt.Sprintf("%-*s  ", widths[k], row[k])
		}
		fmt.Fprintln(w, strings.TrimRight(line, " "))
	}
}

func PrintCSV(w io.Writer, data interface{}) {
	items := extractItems(data)
	if len(items) == 0 {
		PrintJSON(w, data)
		return
	}
	keys := collectKeys(items)
	cw := csv.NewWriter(w)
	_ = cw.Write(keys)
	for _, item := range items {
		row := make([]string, len(keys))
		for i, k := range keys {
			row[i] = formatValue(item[k])
		}
		_ = cw.Write(row)
	}
	cw.Flush()
}

func FormatOutput(data interface{}, format Format) {
	w := os.Stdout
	switch format {
	case FormatPretty:
		PrintPretty(w, data)
	case FormatTable:
		PrintTable(w, data)
	case FormatCSV:
		PrintCSV(w, data)
	default:
		PrintJSON(w, data)
	}
}

func extractItems(data interface{}) []map[string]interface{} {
	switch v := data.(type) {
	case []map[string]interface{}:
		return v
	case []interface{}:
		result := make([]map[string]interface{}, 0, len(v))
		for _, item := range v {
			if m, ok := item.(map[string]interface{}); ok {
				result = append(result, m)
			}
		}
		return result
	case map[string]interface{}:
		for _, val := range v {
			if arr, ok := val.([]interface{}); ok && len(arr) > 0 {
				return extractItems(arr)
			}
		}
		return []map[string]interface{}{v}
	}
	return nil
}

func collectKeys(items []map[string]interface{}) []string {
	seen := make(map[string]bool)
	var keys []string
	for _, item := range items {
		for k := range item {
			if !seen[k] {
				seen[k] = true
				keys = append(keys, k)
			}
		}
	}
	sort.Strings(keys)
	return keys
}

func formatValue(v interface{}) string {
	if v == nil {
		return ""
	}
	switch val := v.(type) {
	case string:
		return val
	case float64:
		if val == float64(int64(val)) {
			return fmt.Sprintf("%d", int64(val))
		}
		return fmt.Sprintf("%g", val)
	case bool:
		if val {
			return "true"
		}
		return "false"
	default:
		b, _ := json.Marshal(val)
		return string(b)
	}
}

func PrintError(msg string) {
	fmt.Fprintf(os.Stderr, "Error: %s\n", msg)
}

func PrintSuccess(msg string) {
	fmt.Fprintf(os.Stdout, "✓ %s\n", msg)
}
