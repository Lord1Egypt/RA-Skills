# Troubleshooting

Use this file when install finished but the result is not actually usable.

## Common failure buckets

### Dashboard not reachable
Check:
- process is running
- upstream is listening on the expected port
- reverse proxy target is correct
- firewall or cloud security group allows the intended traffic
- DNS points to the right host

### API key fails
Check:
- wrong key copied
- header format mismatch
- stale config after regeneration
- request is hitting the wrong endpoint

### Connected provider but no models
Check:
- auth really completed
- provider session did not expire
- provider is connected but not mapped to exposed models
- dashboard needs refresh or reload

### Model not found
Check:
- exact model identifier
- alias versus upstream model name
- routing rules that rewrite model names
- model removed or unavailable upstream

### 401 or 403
Usually auth, token, scope, or provider session state.

### 404
Usually wrong base URL, wrong path, or wrong reverse proxy route.

### 429
Usually account quota, provider rate limit, or multi-account rotation not working as expected.

### 502 or 504
Usually reverse proxy issue, crashed upstream process, or provider timeout.

### Streaming mismatch
Check whether the downstream client expects a different streaming shape than the upstream route provides.

## Recovery rule

Do not keep changing multiple layers at once. Isolate the failing layer in this order:
1. local CLIProxy process
2. local API request
3. reverse proxy or network edge
4. provider onboarding state
5. downstream OpenClaw client config
