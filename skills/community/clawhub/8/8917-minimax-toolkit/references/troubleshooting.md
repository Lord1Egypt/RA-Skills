# Troubleshooting

## When to read this file
- Official doc verification fails
- Network access to MiniMax docs or API fails
- `coding_plan/remains` cannot be queried
- The checker falls back to offline mode

## Failure classes

### 1. Network unreachable
Typical symptoms:
- DNS resolution failure
- timeout
- connection refused

What to check:
1. Can the machine open `https://platform.minimaxi.com/docs/token-plan/faq`?
2. Can the machine reach `https://www.minimaxi.com/v1/api/openplatform/coding_plan/remains`?
3. Is outbound network restricted by firewall / proxy / VPN / gateway policy?

### 2. Web page fetch fails, API remains still works
Typical symptoms:
- doc page returns 403 / 429 / anti-bot page
- HTML structure changed
- page fetch tool unavailable

What to do:
1. Continue using local references in offline mode.
2. Use the remains API as the real-time quota source.
3. Save the checker report and review `references/api_info.md` manually.

### 3. API remains query fails
Typical symptoms:
- 401 / 403 → API key invalid or wrong key type
- 429 → rate limit or platform throttling
- 5xx → provider-side issue

What to check:
1. Is this a Token Plan API Key rather than a pay-as-you-go key?
2. Has the key expired or been rotated?
3. Is the MiniMax platform currently degraded?

### 4. Official naming changed
Typical symptoms:
- model names in docs do not match `quota_mapping.json`
- remains bucket names change unexpectedly

What to do:
1. Update `references/quota_mapping.json`
2. Update `references/api_info.md`
3. Re-run the checker

### 5. remains field semantics are unclear
Typical symptoms:
- API returns numeric fields, but they do not match the numbers shown in the Token Plan web console
- `current_interval_usage_count` / `current_interval_total_count` cannot be safely interpreted as used / remain without cross-check

What to do:
1. Treat remains output as raw reference data only.
2. Cross-check the same time window against the official Token Plan web console.
3. Do not make hard quota decisions until the field semantics are validated.

## Offline mode policy
If both doc fetch and remains query fail:
- Do not block the whole skill.
- Continue with local references only.
- Mark the result as **offline / unverified in this session**.
- Tell the user what failed and what to check.

## Suggested user-facing guidance
Use wording like:

```text
官方文档校验失败，已切换为离线模式，仅使用本地 references。
建议检查：
1. 当前网络是否可访问 MiniMax 官方文档
2. remains API 是否可访问
3. OpenClaw 当前环境是否允许网页读取
```
