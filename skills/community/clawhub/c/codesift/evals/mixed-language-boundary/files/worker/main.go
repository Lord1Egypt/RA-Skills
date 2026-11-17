// Command worker pushes order updates to the orders API and honors its rate limits.
package main

import (
	"encoding/json"
	"fmt"
	"net/http"
	"time"
)

// retryBody mirrors the 429 response body documented in docs/api.md.
type retryBody struct {
	RetryAfter int `json:"retry_after"`
}

// syncOrder posts one order and waits as instructed when the API rate-limits it.
func syncOrder(client *http.Client, baseURL, id string) error {
	for attempt := 0; attempt < 5; attempt++ {
		resp, err := client.Post(baseURL+"/orders/"+id+"/sync", "application/json", nil)
		if err != nil {
			return err
		}
		if resp.StatusCode != http.StatusTooManyRequests {
			resp.Body.Close()
			if resp.StatusCode >= 300 {
				return fmt.Errorf("order %s: sync failed with status %d", id, resp.StatusCode)
			}
			return nil
		}
		var body retryBody
		err = json.NewDecoder(resp.Body).Decode(&body)
		resp.Body.Close()
		if err != nil {
			return err
		}
		time.Sleep(time.Duration(body.RetryAfter) * time.Millisecond)
	}
	return fmt.Errorf("order %s: still rate-limited after 5 attempts", id)
}

// main syncs one sample order against a local API.
func main() {
	client := &http.Client{Timeout: 10 * time.Second}
	if err := syncOrder(client, "http://localhost:8080", "A1"); err != nil {
		fmt.Println(err)
	}
}
