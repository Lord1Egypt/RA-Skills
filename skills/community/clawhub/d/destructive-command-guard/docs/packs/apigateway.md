# API Gateway Packs

This document describes packs in the `apigateway` category.

## Packs in this Category

- [AWS API Gateway](#apigatewayaws)
- [Kong API Gateway](#apigatewaykong)
- [Google Apigee](#apigatewayapigee)

---

## AWS API Gateway

**Pack ID:** `apigateway.aws`

Protects against destructive AWS API Gateway CLI operations for both REST APIs and HTTP APIs.

### Keywords

Commands containing these keywords are checked against this pack:

- `aws`
- `apigateway`
- `apigatewayv2`

### Safe Patterns (Allowed)

These patterns match safe commands that are always allowed:

| Pattern Name | Pattern |
|--------------|----------|
| `apigateway-get-rest-api` | `aws\s+apigateway\s+get-rest-api\b` |
| `apigateway-get-rest-apis` | `aws\s+apigateway\s+get-rest-apis\b` |
| `apigateway-get-resources` | `aws\s+apigateway\s+get-resources\b` |
| `apigateway-get-resource` | `aws\s+apigateway\s+get-resource\b` |
| `apigateway-get-method` | `aws\s+apigateway\s+get-method\b` |
| `apigateway-get-stages` | `aws\s+apigateway\s+get-stages\b` |
| `apigateway-get-stage` | `aws\s+apigateway\s+get-stage\b` |
| `apigateway-get-deployments` | `aws\s+apigateway\s+get-deployments\b` |
| `apigateway-get-deployment` | `aws\s+apigateway\s+get-deployment\b` |
| `apigateway-get-api-keys` | `aws\s+apigateway\s+get-api-keys\b` |
| `apigateway-get-api-key` | `aws\s+apigateway\s+get-api-key\b` |
| `apigateway-get-authorizers` | `aws\s+apigateway\s+get-authorizers\b` |
| `apigateway-get-models` | `aws\s+apigateway\s+get-models\b` |
| `apigateway-get-usage-plans` | `aws\s+apigateway\s+get-usage-plans\b` |
| `apigateway-get-domain-names` | `aws\s+apigateway\s+get-domain-names\b` |
| `apigatewayv2-get-apis` | `aws\s+apigatewayv2\s+get-apis\b` |
| `apigatewayv2-get-api` | `aws\s+apigatewayv2\s+get-api\b` |
| `apigatewayv2-get-routes` | `aws\s+apigatewayv2\s+get-routes\b` |
| `apigatewayv2-get-route` | `aws\s+apigatewayv2\s+get-route\b` |
| `apigatewayv2-get-integrations` | `aws\s+apigatewayv2\s+get-integrations\b` |
| `apigatewayv2-get-integration` | `aws\s+apigatewayv2\s+get-integration\b` |
| `apigatewayv2-get-stages` | `aws\s+apigatewayv2\s+get-stages\b` |
| `apigatewayv2-get-stage` | `aws\s+apigatewayv2\s+get-stage\b` |
| `apigatewayv2-get-authorizers` | `aws\s+apigatewayv2\s+get-authorizers\b` |
| `apigatewayv2-get-domain-names` | `aws\s+apigatewayv2\s+get-domain-names\b` |
| `apigateway-help` | `aws\s+apigateway\s+(?:help\|\-\-help)\b` |
| `apigatewayv2-help` | `aws\s+apigatewayv2\s+(?:help\|\-\-help)\b` |

### Destructive Patterns (Blocked)

These patterns match potentially destructive commands:

| Pattern Name | Reason | Severity |
|--------------|--------|----------|
| `apigateway-delete-rest-api` | aws apigateway delete-rest-api permanently removes a REST API and all its resources. | high |
| `apigateway-delete-resource` | aws apigateway delete-resource removes an API resource and its methods. | high |
| `apigateway-delete-method` | aws apigateway delete-method removes an HTTP method from a resource. | high |
| `apigateway-delete-stage` | aws apigateway delete-stage removes a deployment stage from an API. | high |
| `apigateway-delete-deployment` | aws apigateway delete-deployment removes a deployment from an API. | high |
| `apigateway-delete-api-key` | aws apigateway delete-api-key removes an API key. | high |
| `apigateway-delete-authorizer` | aws apigateway delete-authorizer removes an authorizer from an API. | high |
| `apigateway-delete-model` | aws apigateway delete-model removes a model from an API. | high |
| `apigateway-delete-domain-name` | aws apigateway delete-domain-name removes a custom domain name. | high |
| `apigateway-delete-usage-plan` | aws apigateway delete-usage-plan removes a usage plan. | high |
| `apigatewayv2-delete-api` | aws apigatewayv2 delete-api permanently removes an HTTP API. | high |
| `apigatewayv2-delete-route` | aws apigatewayv2 delete-route removes a route from an HTTP API. | high |
| `apigatewayv2-delete-integration` | aws apigatewayv2 delete-integration removes an integration from an HTTP API. | high |
| `apigatewayv2-delete-stage` | aws apigatewayv2 delete-stage removes a stage from an HTTP API. | high |
| `apigatewayv2-delete-authorizer` | aws apigatewayv2 delete-authorizer removes an authorizer from an HTTP API. | high |
| `apigatewayv2-delete-domain-name` | aws apigatewayv2 delete-domain-name removes a custom domain name from an HTTP API. | high |
| `apigatewayv2-delete-route-response` | aws apigatewayv2 delete-route-response removes a route response from an HTTP API. | high |
| `apigatewayv2-delete-integration-response` | aws apigatewayv2 delete-integration-response removes an integration response. | high |

### Allowlist Guidance

To allowlist a specific rule from this pack, add to your allowlist:

```toml
[[allow]]
rule = "apigateway.aws:<pattern-name>"
reason = "Your reason here"
```

To allowlist all rules from this pack (use with caution):

```toml
[[allow]]
rule = "apigateway.aws:*"
reason = "Your reason here"
risk_acknowledged = true
```

---

## Kong API Gateway

**Pack ID:** `apigateway.kong`

Protects against destructive Kong Gateway CLI, deck CLI, and Admin API operations.

### Keywords

Commands containing these keywords are checked against this pack:

- `kong`
- `deck`
- `8001`

### Safe Patterns (Allowed)

These patterns match safe commands that are always allowed:

| Pattern Name | Pattern |
|--------------|----------|
| `kong-version` | `kong\s+(?:version\|--version\|-v)\b` |
| `kong-help` | `kong\s+(?:help\|--help\|-h)\b` |
| `kong-health` | `kong\s+health\b` |
| `kong-check` | `kong\s+check\b` |
| `kong-config-parse` | `kong\s+config\s+(?:parse\|init)\b` |
| `deck-version` | `deck\s+(?:version\|--version)\b` |
| `deck-help` | `deck\s+(?:help\|--help\|-h)\b` |
| `deck-ping` | `deck\s+ping\b` |
| `deck-dump` | `deck\s+dump\b` |
| `deck-diff` | `deck\s+diff\b` |
| `deck-validate` | `deck\s+validate\b` |
| `deck-convert` | `deck\s+convert\b` |
| `deck-file` | `deck\s+file\b` |
| `kong-admin-explicit-get` | `curl\s+.*(?:-X\s+GET\|--request\s+GET)\s+.*(?:localhost\|127\.0\.0\.1):8001/` |

### Destructive Patterns (Blocked)

These patterns match potentially destructive commands:

| Pattern Name | Reason | Severity |
|--------------|--------|----------|
| `deck-reset` | deck reset removes ALL Kong configuration. This is extremely dangerous and irreversible. | high |
| `deck-sync-destructive` | deck sync with --select-tag can remove entities not matching the tag. | high |
| `kong-admin-delete-services` | DELETE request to Kong Admin API removes services. | high |
| `kong-admin-delete-routes` | DELETE request to Kong Admin API removes routes. | high |
| `kong-admin-delete-plugins` | DELETE request to Kong Admin API removes plugins. | high |
| `kong-admin-delete-consumers` | DELETE request to Kong Admin API removes consumers. | high |
| `kong-admin-delete-upstreams` | DELETE request to Kong Admin API removes upstreams. | high |
| `kong-admin-delete-targets` | DELETE request to Kong Admin API removes targets. | high |
| `kong-admin-delete-certificates` | DELETE request to Kong Admin API removes certificates. | high |
| `kong-admin-delete-snis` | DELETE request to Kong Admin API removes SNIs. | high |
| `kong-admin-delete-generic` | DELETE request to Kong Admin API can remove configuration. | high |

### Allowlist Guidance

To allowlist a specific rule from this pack, add to your allowlist:

```toml
[[allow]]
rule = "apigateway.kong:<pattern-name>"
reason = "Your reason here"
```

To allowlist all rules from this pack (use with caution):

```toml
[[allow]]
rule = "apigateway.kong:*"
reason = "Your reason here"
risk_acknowledged = true
```

---

## Google Apigee

**Pack ID:** `apigateway.apigee`

Protects against destructive Google Apigee CLI and apigeecli operations.

### Keywords

Commands containing these keywords are checked against this pack:

- `apigee`
- `apigeecli`

### Safe Patterns (Allowed)

These patterns match safe commands that are always allowed:

| Pattern Name | Pattern |
|--------------|----------|
| `gcloud-apigee-apis-list` | `gcloud\s+apigee\s+apis\s+list\b` |
| `gcloud-apigee-apis-describe` | `gcloud\s+apigee\s+apis\s+describe\b` |
| `gcloud-apigee-environments-list` | `gcloud\s+apigee\s+environments\s+list\b` |
| `gcloud-apigee-environments-describe` | `gcloud\s+apigee\s+environments\s+describe\b` |
| `gcloud-apigee-developers-list` | `gcloud\s+apigee\s+developers\s+list\b` |
| `gcloud-apigee-developers-describe` | `gcloud\s+apigee\s+developers\s+describe\b` |
| `gcloud-apigee-products-list` | `gcloud\s+apigee\s+products\s+list\b` |
| `gcloud-apigee-products-describe` | `gcloud\s+apigee\s+products\s+describe\b` |
| `gcloud-apigee-organizations-list` | `gcloud\s+apigee\s+organizations\s+list\b` |
| `gcloud-apigee-organizations-describe` | `gcloud\s+apigee\s+organizations\s+describe\b` |
| `gcloud-apigee-deployments-list` | `gcloud\s+apigee\s+deployments\s+list\b` |
| `gcloud-apigee-deployments-describe` | `gcloud\s+apigee\s+deployments\s+describe\b` |
| `apigeecli-apis-list` | `apigeecli\s+apis\s+list\b` |
| `apigeecli-apis-get` | `apigeecli\s+apis\s+get\b` |
| `apigeecli-products-list` | `apigeecli\s+products\s+list\b` |
| `apigeecli-products-get` | `apigeecli\s+products\s+get\b` |
| `apigeecli-developers-list` | `apigeecli\s+developers\s+list\b` |
| `apigeecli-developers-get` | `apigeecli\s+developers\s+get\b` |
| `apigeecli-envs-list` | `apigeecli\s+envs\s+list\b` |
| `apigeecli-envs-get` | `apigeecli\s+envs\s+get\b` |
| `apigeecli-orgs-list` | `apigeecli\s+orgs\s+list\b` |
| `apigeecli-orgs-get` | `apigeecli\s+orgs\s+get\b` |
| `gcloud-apigee-help` | `gcloud\s+apigee\s+(?:--help\|-h\|help)\b` |
| `apigeecli-help` | `apigeecli\s+(?:--help\|-h\|help\|version)\b` |

### Destructive Patterns (Blocked)

These patterns match potentially destructive commands:

| Pattern Name | Reason | Severity |
|--------------|--------|----------|
| `gcloud-apigee-apis-delete` | gcloud apigee apis delete removes an API proxy from Apigee. | high |
| `gcloud-apigee-environments-delete` | gcloud apigee environments delete removes an Apigee environment. | high |
| `gcloud-apigee-developers-delete` | gcloud apigee developers delete removes a developer from Apigee. | high |
| `gcloud-apigee-products-delete` | gcloud apigee products delete removes an API product from Apigee. | high |
| `gcloud-apigee-organizations-delete` | gcloud apigee organizations delete removes an entire Apigee organization. EXTREMELY DANGEROUS. | high |
| `gcloud-apigee-deployments-undeploy` | gcloud apigee deployments undeploy removes an API deployment. | high |
| `apigeecli-apis-delete` | apigeecli apis delete removes an API proxy from Apigee. | high |
| `apigeecli-products-delete` | apigeecli products delete removes an API product from Apigee. | high |
| `apigeecli-developers-delete` | apigeecli developers delete removes a developer from Apigee. | high |
| `apigeecli-envs-delete` | apigeecli envs delete removes an Apigee environment. | high |
| `apigeecli-orgs-delete` | apigeecli orgs delete removes an entire Apigee organization. EXTREMELY DANGEROUS. | high |
| `apigeecli-apps-delete` | apigeecli apps delete removes a developer app from Apigee. | high |
| `apigeecli-keyvaluemaps-delete` | apigeecli keyvaluemaps delete removes a key-value map from Apigee. | high |
| `apigeecli-targetservers-delete` | apigeecli targetservers delete removes a target server from Apigee. | high |

### Allowlist Guidance

To allowlist a specific rule from this pack, add to your allowlist:

```toml
[[allow]]
rule = "apigateway.apigee:<pattern-name>"
reason = "Your reason here"
```

To allowlist all rules from this pack (use with caution):

```toml
[[allow]]
rule = "apigateway.apigee:*"
reason = "Your reason here"
risk_acknowledged = true
```

---

