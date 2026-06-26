This wrapper runs `amazon_order_details_fetcher` with the JS browser runtime.

Input:
- JSON object string, e.g. `{"order_id":"113-...","browser":{"headless":false}}`

Behavior:
- Opens order details page (if order info provided)
- Extracts structured details from current page

Output:
- JSON string with `status` and `trace`.
