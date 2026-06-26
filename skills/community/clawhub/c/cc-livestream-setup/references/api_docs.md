# CC Live API Documentation Reference

## API Base URL
```
https://api.csslcloud.net/api/
```

## Authentication (THQS)

All API requests require THQS (Time-based Hash Query String) signature authentication.

### Signature Algorithm

1. Collect all request parameters (except `time` and `hash`)
2. URL encode all parameter keys and values using `quote_plus`
3. Sort parameters alphabetically by key
4. Concatenate as `key1=value1&key2=value2&...`
5. Append `&time={current_timestamp}&salt={api_key}`
6. Calculate MD5 hash of the concatenated string (uppercase hex)
7. Append `&hash={hash_result}`

### Example

https://doc.bokecc.com/live/developer/live_api/Appendix_2.html