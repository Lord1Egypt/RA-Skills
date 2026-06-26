# API Testing Patterns Reference

This reference provides standard templates for generating API tests in various languages.

## Python (Requests)
```python
import requests

url = "https://api.example.com/v1/endpoint"
headers = {
    "Authorization": "Bearer YOUR_TOKEN",
    "Content-Type": "application/json"
}
payload = {
    "key": "value"
}

response = requests.post(url, json=payload, headers=headers)
print(f"Status Code: {response.status_code}")
print(response.json())
```

## JavaScript (Fetch)
```javascript
const url = 'https://api.example.com/v1/endpoint';
const options = {
  method: 'POST',
  headers: {
    'Authorization': 'Bearer YOUR_TOKEN',
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({ key: 'value' })
};

fetch(url, options)
  .then(res => res.json())
  .then(json => console.log(json))
  .catch(err => console.error('error:' + err));
```

## cURL
```bash
curl --request POST \
     --url https://api.example.com/v1/endpoint \
     --header 'Authorization: Bearer YOUR_TOKEN' \
     --header 'Content-Type: application/json' \
     --data '{"key":"value"}'
```

## Go (net/http)
```go
package main

import (
	"bytes"
	"fmt"
	"net/http"
)

func main() {
	url := "https://api.example.com/v1/endpoint"
	payload := []byte(`{"key":"value"}`)
	req, _ := http.NewRequest("POST", url, bytes.NewBuffer(payload))
	req.Header.Set("Authorization", "Bearer YOUR_TOKEN")
	req.Header.Set("Content-Type", "application/json")

	client := &http.Client{}
	resp, _ := client.Do(req)
	defer resp.Body.Close()

	fmt.Println("Response Status:", resp.Status)
}
```
