---
name: checkly-constructs
description: Understand the Checkly constructs system including resource lifecycle, logical IDs, configuration inheritance, and the Session/Project abstraction. Use when debugging construct issues, understanding resource management, or working with advanced patterns. Triggers on constructs, logical ID, resource management, project structure.
---

# checkly constructs

The Checkly constructs system provides type-safe abstractions for monitoring resources.

## Core concepts

### Construct hierarchy

```
Construct (base)
├── Check
│   ├── RuntimeCheck
│   │   ├── ApiCheck
│   │   ├── PlaywrightCheck
│   │   └── RepairableRuntimeCheck
│   │       ├── BrowserCheck
│   │       └── MultiStepCheck
│   ├── AgenticCheck
│   └── Monitor
│       ├── HeartbeatMonitor
│       ├── TcpMonitor
│       ├── DnsMonitor
│       ├── IcmpMonitor
│       ├── UrlMonitor
│       ├── GrpcMonitor
│       ├── SslMonitor
│       └── TracerouteMonitor
├── CheckGroup
├── AlertChannel
├── StatusPage / StatusPageV3
├── StatusPageV3Component
└── StatusPageV3AutomationRule
```

### Logical IDs

Every construct needs a unique logical ID:

```typescript
new ApiCheck('api-status-check', {  // <- logical ID
  name: 'API Status Check',  // <- display name
})
```

**Rules:**
- Must be unique within resource type
- Pattern: `[A-Za-z0-9_-/#.]+`
- Use descriptive IDs: `'homepage-check'` not `'check-1'`

## Construct lifecycle

1. **Construction**: Instance created and registered
2. **Validation**: Configuration checked for errors
3. **Bundling**: Code and dependencies packaged
4. **Synthesis**: Converted to API payload
5. **Deployment**: Created/updated in Checkly

## Component-based Status Page V3

Import `StatusPageV3`, `StatusPageV3Component`, and `StatusPageV3AutomationRule` from `checkly/constructs`. A v3 page has no legacy cards or `StatusPageService` resources: declare its hierarchy with components that point to the page. A `SERVICE` may be nested beneath a same-page `GROUP` through `parent`.

```typescript
import {
  StatusPageV3,
  StatusPageV3AutomationRule,
  StatusPageV3Component,
} from 'checkly/constructs'

const statusPage = new StatusPageV3('example-status-page-v3', {
  name: 'Example Status Page',
  url: 'example-status-page-v3',
  customDomain: 'status.example.com',
  defaultTheme: 'AUTO',
  supportLink: 'https://support.example.com',
  themeColors: {
    light: {
      linkFontColor: '#005AC2',
      primaryButtonBackgroundColor: '#151A1E',
    },
    dark: { linkFontColor: '#248AFF' },
  },
})

const webApp = new StatusPageV3Component('example-web-app-group', {
  statusPage,
  type: 'GROUP',
  name: 'Web application',
  displayOrder: 1,
  expandedByDefault: true,
})

const signUp = new StatusPageV3Component('example-sign-up-service', {
  statusPage,
  parent: webApp,
  type: 'SERVICE',
  name: 'Sign up',
  description: 'The sign up flow',
  displayOrder: 1,
  showHistoricalData: false,
})

new StatusPageV3AutomationRule('example-api-down-rule', {
  statusPage,
  name: 'API down',
  firstUpdate: 'The API is down, we are investigating.',
  lastUpdate: 'The API has recovered.',
  tags: ['api:public'],
  coolDownMinutes: 5,
  components: [{ component: signUp, targetImpact: 'MAJOR_OUTAGE' }],
})
```

Automation rules open one incident when a failing check or its group has any tag listed by the rule, apply each component's `targetImpact`, and resolve the incident on recovery. They require Checkly's automated incident management add-on. `tags` must contain at least one item; target impacts are `UNDER_MAINTENANCE`, `DEGRADED_PERFORMANCE`, `PARTIAL_OUTAGE`, or `MAJOR_OUTAGE`.

Both component types accept `showHistoricalData` (default `true`); only a `GROUP` accepts `expandedByDefault` (default `false`). Omit either property to keep the backend default. `supportLink` appears in the page footer. `themeColors.light` and `themeColors.dark` accept partial color maps, so unspecified colors retain Checkly defaults; values must be three- or six-digit hex strings and unknown color keys fail validation. Custom theme colors require the corresponding Checkly plan feature.

Use `StatusPageV3.fromId(<physical-id>)` and `StatusPageV3Component.fromId(<physical-id>)` when code should reference existing UI-managed resources without managing them. A deployed logical ID cannot change generation between `StatusPage` and `StatusPageV3`; use a new logical ID for a v3 migration rather than redeploying the legacy ID as a different resource shape.

## Structured check intent

Use `intent` to give Checkly root-cause analysis and check-repair features durable guidance about what a check is meant to verify. Intent supplements descriptions and executable assertions; it does not replace either.

```typescript
new ApiCheck('dashboard-api', {
  name: 'Dashboard API',
  intent: {
    goal: 'Verify that authenticated users can open the dashboard.',
    constraints: [
      {
        type: 'REQUIRED_OUTCOME',
        statement: 'The dashboard displays the account overview.',
      },
      {
        type: 'MUST_PRESERVE',
        statement: 'Do not weaken the authentication assertion.',
      },
    ],
  },
  request: {
    method: 'GET',
    url: 'https://example.com/api/dashboard',
  },
})
```

Intent is supported by `ApiCheck`, `BrowserCheck`, `MultiStepCheck`, `PlaywrightCheck`, `TcpMonitor`, `DnsMonitor`, `IcmpMonitor`, `UrlMonitor`, and `GrpcMonitor`. It is not exposed on `AgenticCheck`, `HeartbeatMonitor`, `SslMonitor`, or `TracerouteMonitor`.

Deployment semantics are deliberate:

- Omit `intent` to leave any existing backend-authored intent unchanged.
- Provide an object to set or update intent.
- Set `intent: null` to explicitly clear it.

The CLI trims surrounding whitespace. `goal` is required and limited to 2,000 characters after trimming. Constraints use exact uppercase types `REQUIRED_OUTCOME` or `MUST_PRESERVE`; each statement is limited to 1,000 characters, and each type may appear at most 20 times. Unknown fields or constraint types fail validation.

## Session and Project

The Session singleton manages global state:

```typescript
// Internal - you don't normally interact with this
Session.current().addConstruct(check)
```

The Project aggregates all constructs:

```typescript
// Internal - happens automatically
project.addResource('check', check)
```

## Configuration inheritance

```typescript
// checkly.config.ts - global
checks: {
  frequency: 10,
  locations: ['us-east-1'],
}

// CheckGroup - group-level
const group = new CheckGroup('api', {
  frequency: 5,  // Overrides global
})

// Check - check-level
new ApiCheck('critical-api', {
  group: group,
  frequency: 1,  // Overrides group
})
```

## Related Skills

- See `checkly-checks` for practical check creation
- See `checkly-groups` for organization
