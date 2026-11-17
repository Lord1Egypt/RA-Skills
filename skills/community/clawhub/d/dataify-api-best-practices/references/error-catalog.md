# Error catalog

| Category | Typical signal | Safe action |
| --- | --- | --- |
| missing_credentials | Environment variable absent | Show platform-specific setup |
| invalid_credentials | 401/403 | Open API-key management |
| insufficient_balance | 402 | Open balance management |
| rate_limited | 429 | Honor Retry-After; bounded retry for reads |
| invalid_input | 400/422 | Correct input; do not retry unchanged |
| remote_failure | terminal task failure or 5xx | Report evidence; retry only when safe |
| local_timeout | deadline exceeded | Resume same task ID |
| network | DNS/TLS/connect failure | Bounded retry for reads; preserve state |
