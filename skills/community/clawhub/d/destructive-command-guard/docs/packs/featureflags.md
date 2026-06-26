# Feature Flags Packs

This document describes packs in the `featureflags` category.

## Packs in this Category

- [Flipt](#featureflagsflipt)
- [LaunchDarkly](#featureflagslaunchdarkly)
- [Split.io](#featureflagssplit)
- [Unleash](#featureflagsunleash)

---

## Flipt

**Pack ID:** `featureflags.flipt`

Protects against destructive Flipt CLI and API operations.

### Keywords

Commands containing these keywords are checked against this pack:

- `flipt`

### Safe Patterns (Allowed)

These patterns match safe commands that are always allowed:

| Pattern Name | Pattern |
|--------------|----------|
| `flipt-flag-list` | `flipt\s+flag\s+list\b` |
| `flipt-flag-get` | `flipt\s+flag\s+get\b` |
| `flipt-flag-create` | `flipt\s+flag\s+create\b` |
| `flipt-flag-update` | `flipt\s+flag\s+update\b` |
| `flipt-segment-list` | `flipt\s+segment\s+list\b` |
| `flipt-segment-get` | `flipt\s+segment\s+get\b` |
| `flipt-segment-create` | `flipt\s+segment\s+create\b` |
| `flipt-namespace-list` | `flipt\s+namespace\s+list\b` |
| `flipt-namespace-get` | `flipt\s+namespace\s+get\b` |
| `flipt-namespace-create` | `flipt\s+namespace\s+create\b` |
| `flipt-rule-list` | `flipt\s+rule\s+list\b` |
| `flipt-rule-get` | `flipt\s+rule\s+get\b` |
| `flipt-rule-create` | `flipt\s+rule\s+create\b` |
| `flipt-evaluate` | `flipt\s+evaluate\b` |
| `flipt-help` | `flipt\s+(?:--help\|-h\|help)\b` |
| `flipt-version` | `flipt\s+(?:--version\|version)\b` |
| `flipt-server` | `flipt\s+(?:server\|serve)\b` |
| `flipt-config` | `flipt\s+config\b` |

### Destructive Patterns (Blocked)

These patterns match potentially destructive commands:

| Pattern Name | Reason | Severity |
|--------------|--------|----------|
| `flipt-flag-delete` | flipt flag delete permanently removes a feature flag. This cannot be undone. | high |
| `flipt-segment-delete` | flipt segment delete removes a segment and its constraints. | high |
| `flipt-namespace-delete` | flipt namespace delete removes a namespace and all its flags, segments, and rules. | high |
| `flipt-rule-delete` | flipt rule delete removes a targeting rule from a flag. | high |
| `flipt-constraint-delete` | flipt constraint delete removes a constraint from a segment. | high |
| `flipt-variant-delete` | flipt variant delete removes a variant from a flag. | high |
| `flipt-distribution-delete` | flipt distribution delete removes a distribution from a rule. | high |
| `flipt-api-delete` | DELETE request to Flipt API can remove flags, segments, or rules. | high |

### Allowlist Guidance

To allowlist a specific rule from this pack, add to your allowlist:

```toml
[[allow]]
rule = "featureflags.flipt:<pattern-name>"
reason = "Your reason here"
```

To allowlist all rules from this pack (use with caution):

```toml
[[allow]]
rule = "featureflags.flipt:*"
reason = "Your reason here"
risk_acknowledged = true
```

---

## LaunchDarkly

**Pack ID:** `featureflags.launchdarkly`

Protects against destructive LaunchDarkly CLI and API operations.

### Keywords

Commands containing these keywords are checked against this pack:

- `ldcli`
- `launchdarkly`

### Safe Patterns (Allowed)

These patterns match safe commands that are always allowed:

| Pattern Name | Pattern |
|--------------|----------|
| `ldcli-flags-list` | `ldcli\s+flags\s+list\b` |
| `ldcli-flags-get` | `ldcli\s+flags\s+get\b` |
| `ldcli-flags-create` | `ldcli\s+flags\s+create\b` |
| `ldcli-flags-update` | `ldcli\s+flags\s+update\b` |
| `ldcli-projects-list` | `ldcli\s+projects\s+list\b` |
| `ldcli-projects-get` | `ldcli\s+projects\s+get\b` |
| `ldcli-projects-create` | `ldcli\s+projects\s+create\b` |
| `ldcli-environments-list` | `ldcli\s+environments\s+list\b` |
| `ldcli-environments-get` | `ldcli\s+environments\s+get\b` |
| `ldcli-environments-create` | `ldcli\s+environments\s+create\b` |
| `ldcli-segments-list` | `ldcli\s+segments\s+list\b` |
| `ldcli-segments-get` | `ldcli\s+segments\s+get\b` |
| `ldcli-segments-create` | `ldcli\s+segments\s+create\b` |
| `ldcli-metrics-list` | `ldcli\s+metrics\s+list\b` |
| `ldcli-metrics-get` | `ldcli\s+metrics\s+get\b` |
| `ldcli-help` | `ldcli\s+(?:--help\|-h\|help)\b` |
| `ldcli-version` | `ldcli\s+(?:--version\|version)\b` |
| `launchdarkly-api-get` | `curl\s+.*(?:-X\s+GET\|--request\s+GET)\s+.*app\.launchdarkly\.com/api` |

### Destructive Patterns (Blocked)

These patterns match potentially destructive commands:

| Pattern Name | Reason | Severity |
|--------------|--------|----------|
| `ldcli-flags-delete` | ldcli flags delete permanently removes a feature flag. This cannot be undone. | high |
| `ldcli-flags-archive` | ldcli flags archive soft-deletes a feature flag. While recoverable, this affects all environments. | high |
| `ldcli-projects-delete` | ldcli projects delete removes an entire project and all its flags, environments, and settings. | high |
| `ldcli-environments-delete` | ldcli environments delete removes an environment and all its flag configurations. | high |
| `ldcli-segments-delete` | ldcli segments delete removes a user segment and its targeting rules. | high |
| `ldcli-metrics-delete` | ldcli metrics delete removes a metric and its experiment data. | high |
| `launchdarkly-api-delete-environments` | DELETE request to LaunchDarkly API removes environments. | high |
| `launchdarkly-api-delete-flags` | DELETE request to LaunchDarkly API removes feature flags. | high |
| `launchdarkly-api-delete-segments` | DELETE request to LaunchDarkly API removes segments. | high |
| `launchdarkly-api-delete-projects` | DELETE request to LaunchDarkly API removes projects. | high |
| `launchdarkly-api-delete-generic` | DELETE request to LaunchDarkly API can remove resources. | high |

### Allowlist Guidance

To allowlist a specific rule from this pack, add to your allowlist:

```toml
[[allow]]
rule = "featureflags.launchdarkly:<pattern-name>"
reason = "Your reason here"
```

To allowlist all rules from this pack (use with caution):

```toml
[[allow]]
rule = "featureflags.launchdarkly:*"
reason = "Your reason here"
risk_acknowledged = true
```

---

## Split.io

**Pack ID:** `featureflags.split`

Protects against destructive Split.io CLI and API operations.

### Keywords

Commands containing these keywords are checked against this pack:

- `split`
- `api.split.io`

### Safe Patterns (Allowed)

These patterns match safe commands that are always allowed:

| Pattern Name | Pattern |
|--------------|----------|
| `split-splits-list` | `split\s+splits\s+list\b` |
| `split-splits-get` | `split\s+splits\s+get\b` |
| `split-splits-create` | `split\s+splits\s+create\b` |
| `split-splits-update` | `split\s+splits\s+update\b` |
| `split-environments-list` | `split\s+environments\s+list\b` |
| `split-environments-get` | `split\s+environments\s+get\b` |
| `split-environments-create` | `split\s+environments\s+create\b` |
| `split-segments-list` | `split\s+segments\s+list\b` |
| `split-segments-get` | `split\s+segments\s+get\b` |
| `split-segments-create` | `split\s+segments\s+create\b` |
| `split-traffic-types-list` | `split\s+traffic-types\s+list\b` |
| `split-traffic-types-get` | `split\s+traffic-types\s+get\b` |
| `split-workspaces-list` | `split\s+workspaces\s+list\b` |
| `split-workspaces-get` | `split\s+workspaces\s+get\b` |
| `split-help` | `split\s+(?:--help\|-h\|help)\b` |
| `split-version` | `split\s+(?:--version\|version)\b` |
| `split-api-get` | `curl\s+.*(?:-X\s+GET\|--request\s+GET)\s+.*api\.split\.io` |

### Destructive Patterns (Blocked)

These patterns match potentially destructive commands:

| Pattern Name | Reason | Severity |
|--------------|--------|----------|
| `split-splits-delete` | split splits delete permanently removes a split definition. This cannot be undone. | high |
| `split-splits-kill` | split splits kill terminates a split, stopping all traffic to treatments. | high |
| `split-environments-delete` | split environments delete removes an environment and all its configurations. | high |
| `split-segments-delete` | split segments delete removes a segment and its targeting rules. | high |
| `split-traffic-types-delete` | split traffic-types delete removes a traffic type. This affects all splits using it. | high |
| `split-workspaces-delete` | split workspaces delete removes a workspace and all its resources. | high |
| `split-api-delete-splits` | DELETE request to Split.io API removes split definitions. | high |
| `split-api-delete-environments` | DELETE request to Split.io API removes environments. | high |
| `split-api-delete-segments` | DELETE request to Split.io API removes segments. | high |
| `split-api-delete-generic` | DELETE request to Split.io API can remove resources. | high |

### Allowlist Guidance

To allowlist a specific rule from this pack, add to your allowlist:

```toml
[[allow]]
rule = "featureflags.split:<pattern-name>"
reason = "Your reason here"
```

To allowlist all rules from this pack (use with caution):

```toml
[[allow]]
rule = "featureflags.split:*"
reason = "Your reason here"
risk_acknowledged = true
```

---

## Unleash

**Pack ID:** `featureflags.unleash`

Protects against destructive Unleash CLI and API operations.

### Keywords

Commands containing these keywords are checked against this pack:

- `unleash`

### Safe Patterns (Allowed)

These patterns match safe commands that are always allowed:

| Pattern Name | Pattern |
|--------------|----------|
| `unleash-features-list` | `unleash\s+features?\s+list\b` |
| `unleash-features-get` | `unleash\s+features?\s+get\b` |
| `unleash-features-create` | `unleash\s+features?\s+create\b` |
| `unleash-features-update` | `unleash\s+features?\s+update\b` |
| `unleash-features-enable` | `unleash\s+features?\s+enable\b` |
| `unleash-features-disable` | `unleash\s+features?\s+disable\b` |
| `unleash-projects-list` | `unleash\s+projects?\s+list\b` |
| `unleash-projects-get` | `unleash\s+projects?\s+get\b` |
| `unleash-projects-create` | `unleash\s+projects?\s+create\b` |
| `unleash-environments-list` | `unleash\s+environments?\s+list\b` |
| `unleash-environments-get` | `unleash\s+environments?\s+get\b` |
| `unleash-strategies-list` | `unleash\s+strategies?\s+list\b` |
| `unleash-strategies-get` | `unleash\s+strategies?\s+get\b` |
| `unleash-help` | `unleash\s+(?:--help\|-h\|help)\b` |
| `unleash-version` | `unleash\s+(?:--version\|version)\b` |
| `unleash-api-get` | `curl\s+.*(?:-X\s+GET\|--request\s+GET)\s+.*/api/admin/` |

### Destructive Patterns (Blocked)

These patterns match potentially destructive commands:

| Pattern Name | Reason | Severity |
|--------------|--------|----------|
| `unleash-features-delete` | unleash features delete permanently removes a feature toggle. This cannot be undone. | high |
| `unleash-features-archive` | unleash features archive soft-deletes a feature toggle. | high |
| `unleash-projects-delete` | unleash projects delete removes a project and all its feature toggles. | high |
| `unleash-environments-delete` | unleash environments delete removes an environment. | high |
| `unleash-strategies-delete` | unleash strategies delete removes a custom strategy. | high |
| `unleash-api-keys-delete` | unleash api-keys delete removes an API key. | high |
| `unleash-api-delete-features` | DELETE request to Unleash API removes feature toggles. | high |
| `unleash-api-delete-projects` | DELETE request to Unleash API removes projects. | high |
| `unleash-api-delete-generic` | DELETE request to Unleash API can remove resources. | high |

### Allowlist Guidance

To allowlist a specific rule from this pack, add to your allowlist:

```toml
[[allow]]
rule = "featureflags.unleash:<pattern-name>"
reason = "Your reason here"
```

To allowlist all rules from this pack (use with caution):

```toml
[[allow]]
rule = "featureflags.unleash:*"
reason = "Your reason here"
risk_acknowledged = true
```

---

