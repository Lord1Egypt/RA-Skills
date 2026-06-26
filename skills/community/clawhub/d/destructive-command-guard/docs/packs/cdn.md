# CDN Packs

This document describes packs in the `cdn` category.

## Packs in this Category

- [Cloudflare Workers](#cdncloudflare_workers)
- [Fastly CDN](#cdnfastly)
- [AWS CloudFront](#cdncloudfront)

---

## Cloudflare Workers

**Pack ID:** `cdn.cloudflare_workers`

Protects against destructive Cloudflare Workers, KV, R2, and D1 operations via the Wrangler CLI.

### Keywords

Commands containing these keywords are checked against this pack:

- `wrangler`

### Safe Patterns (Allowed)

These patterns match safe commands that are always allowed:

| Pattern Name | Pattern |
|--------------|----------|
| `wrangler-whoami` | `wrangler\s+whoami\b` |
| `wrangler-kv-get` | `wrangler\s+kv:key\s+get\b` |
| `wrangler-kv-list` | `wrangler\s+kv:key\s+list\b` |
| `wrangler-kv-namespace-list` | `wrangler\s+kv:namespace\s+list\b` |
| `wrangler-r2-object-get` | `wrangler\s+r2\s+object\s+get\b` |
| `wrangler-r2-bucket-list` | `wrangler\s+r2\s+bucket\s+list\b` |
| `wrangler-d1-list` | `wrangler\s+d1\s+list\b` |
| `wrangler-d1-info` | `wrangler\s+d1\s+info\b` |
| `wrangler-dev` | `wrangler\s+dev\b` |
| `wrangler-tail` | `wrangler\s+tail\b` |
| `wrangler-version` | `wrangler\s+(?:-v\|--version\|version)\b` |
| `wrangler-help` | `wrangler\s+(?:-h\|--help\|help)\b` |

### Destructive Patterns (Blocked)

These patterns match potentially destructive commands:

| Pattern Name | Reason | Severity |
|--------------|--------|----------|
| `wrangler-delete` | wrangler delete removes a Worker from Cloudflare. | high |
| `wrangler-deployments-rollback` | wrangler deployments rollback reverts to a previous Worker version. | high |
| `wrangler-kv-key-delete` | wrangler kv:key delete removes a key from KV storage. | high |
| `wrangler-kv-namespace-delete` | wrangler kv:namespace delete removes an entire KV namespace. | high |
| `wrangler-kv-bulk-delete` | wrangler kv:bulk delete removes multiple keys from KV storage. | high |
| `wrangler-r2-object-delete` | wrangler r2 object delete removes an object from R2 storage. | high |
| `wrangler-r2-bucket-delete` | wrangler r2 bucket delete removes an entire R2 bucket. | high |
| `wrangler-d1-delete` | wrangler d1 delete removes a D1 database. | high |

### Allowlist Guidance

To allowlist a specific rule from this pack, add to your allowlist:

```toml
[[allow]]
rule = "cdn.cloudflare_workers:<pattern-name>"
reason = "Your reason here"
```

To allowlist all rules from this pack (use with caution):

```toml
[[allow]]
rule = "cdn.cloudflare_workers:*"
reason = "Your reason here"
risk_acknowledged = true
```

---

## Fastly CDN

**Pack ID:** `cdn.fastly`

Protects against destructive Fastly CLI operations like service, domain, backend, and VCL deletion.

### Keywords

Commands containing these keywords are checked against this pack:

- `fastly`

### Safe Patterns (Allowed)

These patterns match safe commands that are always allowed:

| Pattern Name | Pattern |
|--------------|----------|
| `fastly-service-list` | `fastly\s+service\s+list\b` |
| `fastly-service-describe` | `fastly\s+service\s+describe\b` |
| `fastly-service-search` | `fastly\s+service\s+search\b` |
| `fastly-domain-list` | `fastly\s+domain\s+list\b` |
| `fastly-domain-describe` | `fastly\s+domain\s+describe\b` |
| `fastly-backend-list` | `fastly\s+backend\s+list\b` |
| `fastly-backend-describe` | `fastly\s+backend\s+describe\b` |
| `fastly-vcl-list` | `fastly\s+vcl\s+list\b` |
| `fastly-vcl-describe` | `fastly\s+vcl\s+describe\b` |
| `fastly-version-list` | `fastly\s+version\s+list\b` |
| `fastly-whoami` | `fastly\s+whoami\b` |
| `fastly-profile` | `fastly\s+profile\b` |
| `fastly-version` | `fastly\s+(?:-v\|--version\|version)\b` |
| `fastly-help` | `fastly\s+(?:-h\|--help\|help)\b` |

### Destructive Patterns (Blocked)

These patterns match potentially destructive commands:

| Pattern Name | Reason | Severity |
|--------------|--------|----------|
| `fastly-service-delete` | fastly service delete removes a Fastly service entirely. | high |
| `fastly-domain-delete` | fastly domain delete removes a domain from a service. | high |
| `fastly-backend-delete` | fastly backend delete removes a backend origin server. | high |
| `fastly-vcl-delete` | fastly vcl delete removes VCL configuration. | high |
| `fastly-dictionary-delete` | fastly dictionary delete removes an edge dictionary. | high |
| `fastly-dictionary-item-delete` | fastly dictionary-item delete removes dictionary entries. | high |
| `fastly-acl-delete` | fastly acl delete removes an access control list. | high |
| `fastly-acl-entry-delete` | fastly acl-entry delete removes ACL entries. | high |
| `fastly-logging-delete` | fastly logging delete removes logging endpoints. | high |
| `fastly-version-activate` | fastly service version activate can cause service disruption if misconfigured. | high |
| `fastly-compute-delete` | fastly compute delete removes compute package. | high |

### Allowlist Guidance

To allowlist a specific rule from this pack, add to your allowlist:

```toml
[[allow]]
rule = "cdn.fastly:<pattern-name>"
reason = "Your reason here"
```

To allowlist all rules from this pack (use with caution):

```toml
[[allow]]
rule = "cdn.fastly:*"
reason = "Your reason here"
risk_acknowledged = true
```

---

## AWS CloudFront

**Pack ID:** `cdn.cloudfront`

Protects against destructive AWS CloudFront operations like deleting distributions, cache policies, and functions.

### Keywords

Commands containing these keywords are checked against this pack:

- `cloudfront`

### Safe Patterns (Allowed)

These patterns match safe commands that are always allowed:

| Pattern Name | Pattern |
|--------------|----------|
| `cloudfront-list-distributions` | `aws\s+cloudfront\s+list-distributions\b` |
| `cloudfront-list-cache-policies` | `aws\s+cloudfront\s+list-cache-policies\b` |
| `cloudfront-list-origin-request-policies` | `aws\s+cloudfront\s+list-origin-request-policies\b` |
| `cloudfront-list-functions` | `aws\s+cloudfront\s+list-functions\b` |
| `cloudfront-list-invalidations` | `aws\s+cloudfront\s+list-invalidations\b` |
| `cloudfront-get-distribution` | `aws\s+cloudfront\s+get-distribution\b` |
| `cloudfront-get-distribution-config` | `aws\s+cloudfront\s+get-distribution-config\b` |
| `cloudfront-get-cache-policy` | `aws\s+cloudfront\s+get-cache-policy\b` |
| `cloudfront-get-origin-request-policy` | `aws\s+cloudfront\s+get-origin-request-policy\b` |
| `cloudfront-get-function` | `aws\s+cloudfront\s+get-function\b` |
| `cloudfront-get-invalidation` | `aws\s+cloudfront\s+get-invalidation\b` |
| `cloudfront-describe-function` | `aws\s+cloudfront\s+describe-function\b` |

### Destructive Patterns (Blocked)

These patterns match potentially destructive commands:

| Pattern Name | Reason | Severity |
|--------------|--------|----------|
| `cloudfront-delete-distribution` | aws cloudfront delete-distribution removes a CloudFront distribution. | high |
| `cloudfront-delete-cache-policy` | aws cloudfront delete-cache-policy removes a cache policy. | high |
| `cloudfront-delete-origin-request-policy` | aws cloudfront delete-origin-request-policy removes an origin request policy. | high |
| `cloudfront-delete-function` | aws cloudfront delete-function removes a CloudFront function. | high |
| `cloudfront-delete-response-headers-policy` | aws cloudfront delete-response-headers-policy removes a response headers policy. | high |
| `cloudfront-delete-key-group` | aws cloudfront delete-key-group removes a key group used for signed URLs. | high |
| `cloudfront-create-invalidation` | aws cloudfront create-invalidation creates a cache invalidation (has cost implications). | high |

### Allowlist Guidance

To allowlist a specific rule from this pack, add to your allowlist:

```toml
[[allow]]
rule = "cdn.cloudfront:<pattern-name>"
reason = "Your reason here"
```

To allowlist all rules from this pack (use with caution):

```toml
[[allow]]
rule = "cdn.cloudfront:*"
reason = "Your reason here"
risk_acknowledged = true
```

---

