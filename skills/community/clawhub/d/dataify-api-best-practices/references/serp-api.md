# SERP API

POST form-encoded parameters to `https://scraperapi.dataify.com/request`. Use a specific engine/vertical, a bounded timeout, and JSON output when parsing. Retry reads only for 429/5xx/network failures, honor `Retry-After`, add jitter, and cap attempts. Return parsed results—not internal engine fields—to end users.
