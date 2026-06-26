---
name: checkly-checks
description: Create and configure Checkly checks including API checks, browser checks, and multi-step checks. Covers check types, assertions, retry strategies, and Playwright integration. Use when creating synthetic monitoring checks, validating APIs, testing web applications, or defining check behavior. Triggers on create check, API check, browser check, Playwright, assertions, monitoring.
---

# checkly checks

Create API checks, browser checks, and multi-step checks.

## Check types overview

| Check Type | Use Case | Technology |
|------------|----------|------------|
| **API Check** | HTTP endpoints, REST APIs | HTTP requests + assertions |
| **Browser Check** | Web applications, user flows | Playwright/Puppeteer |
| **Multi-Step Check** | Complex browser workflows | Playwright (legacy) |
| **Playwright Check Suite** | Full test suites | Playwright projects |

## API Checks

Monitor HTTP endpoints with assertions.

### Basic API check

```typescript
// __checks__/api-status.check.ts
import { ApiCheck, AssertionBuilder } from 'checkly/constructs'

new ApiCheck('api-status-check', {
  name: 'API Status Check',
  request: {
    url: 'https://api.example.com/status',
    method: 'GET',
    assertions: [
      AssertionBuilder.statusCode().equals(200),
      AssertionBuilder.responseTime().lessThan(500),
    ],
  },
})
```

### API check with headers

```typescript
// Note: API_TOKEN is a user-defined environment variable for YOUR API checks.
// It is NOT required by Checkly CLI itself. Define it in your .env or CI secrets
// based on your application's authentication needs.

new ApiCheck('authenticated-api-check', {
  name: 'Authenticated API',
  request: {
    url: 'https://api.example.com/user/profile',
    method: 'GET',
    headers: [
      { key: 'Authorization', value: 'Bearer {{API_TOKEN}}' },  // Your custom token
      { key: 'Content-Type', value: 'application/json' },
    ],
    assertions: [
      AssertionBuilder.statusCode().equals(200),
      AssertionBuilder.jsonBody('$.user.id').isNotNull(),
      AssertionBuilder.jsonBody('$.user.email').matches(/^.+@.+\..+$/),
    ],
  },
  environmentVariables: [
    { key: 'API_TOKEN', value: process.env.API_TOKEN!, locked: true },
  ],
})
```

### API check with request body

```typescript
new ApiCheck('create-user-api', {
  name: 'Create User API',
  request: {
    url: 'https://api.example.com/users',
    method: 'POST',
    headers: [
      { key: 'Content-Type', value: 'application/json' },
    ],
    body: JSON.stringify({
      name: 'Test User',
      email: 'test@example.com',
    }),
    assertions: [
      AssertionBuilder.statusCode().equals(201),
      AssertionBuilder.jsonBody('$.id').isNotNull(),
      AssertionBuilder.header('Location').matches(/\/users\/\d+/),
    ],
  },
})
```

### Advanced assertions

```typescript
new ApiCheck('advanced-assertions', {
  name: 'Advanced API Assertions',
  request: {
    url: 'https://api.example.com/products',
    method: 'GET',
    assertions: [
      // Status code
      AssertionBuilder.statusCode().equals(200),
      
      // Response time
      AssertionBuilder.responseTime().lessThan(1000),
      
      // Headers
      AssertionBuilder.header('Content-Type').contains('application/json'),
      AssertionBuilder.header('X-RateLimit-Remaining').greaterThan(0),
      
      // JSON body (JSONPath)
      AssertionBuilder.jsonBody('$.products').isArray(),
      AssertionBuilder.jsonBody('$.products.length').greaterThan(0),
      AssertionBuilder.jsonBody('$.products[0].name').isNotNull(),
      AssertionBuilder.jsonBody('$.products[*].price').greaterThan(0),
      
      // Text body
      AssertionBuilder.textBody().contains('success'),
      
      // JSON Schema validation
      AssertionBuilder.jsonBody('$').hasSchema({
        type: 'object',
        properties: {
          products: { type: 'array' },
          total: { type: 'number' },
        },
        required: ['products', 'total'],
      }),
    ],
  },
})
```

### Setup and teardown scripts

```typescript
new ApiCheck('with-setup-teardown', {
  name: 'API with Setup/Teardown',
  setupScript: {
    content: `
      // Setup: Generate auth token
      const response = await fetch('https://api.example.com/auth/token', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          client_id: process.env.CLIENT_ID,
          client_secret: process.env.CLIENT_SECRET,
        }),
      })
      const { access_token } = await response.json()
      process.env.AUTH_TOKEN = access_token
    `,
  },
  request: {
    url: 'https://api.example.com/protected',
    method: 'GET',
    headers: [
      { key: 'Authorization', value: 'Bearer {{AUTH_TOKEN}}' },
    ],
    assertions: [
      AssertionBuilder.statusCode().equals(200),
    ],
  },
  teardownScript: {
    content: `
      // Teardown: Log result
      console.log('Check completed:', response.status)
    `,
  },
})
```

## Browser Checks

Monitor web applications with Playwright.

### Basic browser check

```typescript
// __checks__/homepage.spec.ts
import { test, expect } from '@playwright/test'

test('homepage loads successfully', async ({ page }) => {
  // Navigate
  const response = await page.goto('https://example.com')
  expect(response?.status()).toBeLessThan(400)
  
  // Verify title
  await expect(page).toHaveTitle(/Example Domain/)
  
  // Take screenshot
  await page.screenshot({ path: 'homepage.jpg' })
})
```

### Login flow check

```typescript
// __checks__/login.spec.ts
import { test, expect } from '@playwright/test'

// Note: TEST_EMAIL and TEST_PASSWORD are user-defined environment variables
// for YOUR specific checks - NOT required by Checkly CLI itself.
// Set them in your local .env or CI/CD secrets as needed for your app.

test('user can login', async ({ page }) => {
  // Navigate to login page
  await page.goto('https://app.example.com/login')
  
  // Fill credentials (using your own env vars)
  await page.fill('input[name="email"]', process.env.TEST_EMAIL!)
  await page.fill('input[name="password"]', process.env.TEST_PASSWORD!)
  
  // Submit form
  await page.click('button[type="submit"]')
  
  // Verify redirect to dashboard
  await expect(page).toHaveURL(/\/dashboard/)
  
  // Verify user is logged in
  await expect(page.locator('.user-name')).toContainText('Test User')
})
```

### E-commerce flow check

```typescript
// __checks__/checkout.spec.ts
import { test, expect } from '@playwright/test'

test('complete purchase flow', async ({ page }) => {
  // Browse products
  await page.goto('https://shop.example.com')
  await page.click('text=Shop Now')
  
  // Add to cart
  await page.click('button[data-testid="add-to-cart"]')
  await expect(page.locator('.cart-count')).toHaveText('1')
  
  // Go to checkout
  await page.click('a[href="/cart"]')
  await page.click('text=Proceed to Checkout')
  
  // Fill shipping info (use test card)
  await page.fill('input[name="cardNumber"]', '4242424242424242')
  await page.fill('input[name="expiry"]', '12/25')
  await page.fill('input[name="cvc"]', '123')
  
  // Complete order
  await page.click('button[type="submit"]')
  
  // Verify success
  await expect(page.locator('.order-confirmation')).toBeVisible()
  await expect(page).toHaveURL(/\/orders\/\d+/)
})
```

### Browser check with construct

```typescript
// __checks__/homepage-browser.check.ts
import { BrowserCheck } from 'checkly/constructs'

new BrowserCheck('homepage-browser-check', {
  name: 'Homepage Browser Check',
  frequency: 5,
  locations: ['us-east-1', 'eu-west-1'],
  code: {
    entrypoint: './homepage.spec.ts',
  },
})
```

## Multi-Step Checks

Complex browser workflows (legacy, prefer Browser Checks).

```typescript
// __checks__/multi-step.check.ts
import { MultiStepCheck } from 'checkly/constructs'

new MultiStepCheck('multi-step-check', {
  name: 'Multi-Step Flow',
  code: {
    entrypoint: './multi-step-script.js',
  },
  runtimeId: '2025.04',
})

// multi-step-script.js
const { chromium } = require('playwright')

async function run() {
  const browser = await chromium.launch()
  const page = await browser.newPage()
  
  await page.goto('https://example.com')
  await page.click('text=Login')
  // ... more steps
  
  await browser.close()
}

run()
```

## Check configuration

### Schedule configuration

```typescript
new ApiCheck('scheduled-check', {
  frequency: 5,  // minutes: 1, 5, 10, 15, 30, 60, 120, 1440
  locations: [
    'us-east-1',
    'us-west-1',
    'eu-west-1',
    'ap-southeast-1',
  ],
  activated: true,  // Schedule check to run
  muted: false,     // Send alerts
})
```

### Tags and organization

```typescript
new ApiCheck('tagged-check', {
  name: 'Tagged Check',
  tags: ['production', 'critical', 'api'],
})
```

### Alert configuration

```typescript
import { EmailAlertChannel, SlackAppAlertChannel } from 'checkly/constructs'

const emailChannel = new EmailAlertChannel('email-alerts', {
  address: 'team@example.com',
})

// For new Slack notifications, prefer the Checkly Slack App channel.
// Use project-discovered #channel names or @user handles; do not invent them.
const slackAppChannel = new SlackAppAlertChannel('slack-app-alerts', {
  name: 'Slack App alerts',
  slackChannels: ['#alerts'],
})

new ApiCheck('check-with-alerts', {
  name: 'Check with Alerts',
  alertChannels: [emailChannel, slackAppChannel],
})
```

### Retry strategies

```typescript
import { RetryStrategyBuilder } from 'checkly/constructs'

new ApiCheck('check-with-retries', {
  name: 'Check with Retries',
  retryStrategy: RetryStrategyBuilder.fixedStrategy({
    baseBackoffSeconds: 60,
    maxAttempts: 2,
    maxDurationSeconds: 600,
    sameRegion: true,
  }),
})
```

## Check patterns

### Check groups

```typescript
// __checks__/groups.ts
import { CheckGroup } from 'checkly/constructs'

export const criticalChecks = new CheckGroup('critical-checks', {
  name: 'Critical Checks',
  activated: true,
  muted: false,
  locations: ['us-east-1', 'eu-west-1'],
  frequency: 1,
  tags: ['critical'],
  environmentVariables: [
    { key: 'ENV', value: 'production' },
  ],
})

// __checks__/api.check.ts
import { ApiCheck } from 'checkly/constructs'
import { criticalChecks } from './groups'

new ApiCheck('critical-api', {
  name: 'Critical API',
  group: criticalChecks,  // Inherits group settings
  request: {
    url: 'https://api.example.com/health',
    method: 'GET',
  },
})
```

### Environment-specific checks

```typescript
const environment = process.env.NODE_ENV || 'production'

new ApiCheck(`api-check-${environment}`, {
  name: `API Check (${environment})`,
  request: {
    url: `https://api.${environment}.example.com/status`,
    method: 'GET',
  },
  tags: [environment],
})
```

### Shared helpers

```typescript
// __checks__/helpers.ts
import { AssertionBuilder } from 'checkly/constructs'

export const standardAssertions = [
  AssertionBuilder.statusCode().equals(200),
  AssertionBuilder.responseTime().lessThan(500),
]

// __checks__/api.check.ts
import { ApiCheck } from 'checkly/constructs'
import { standardAssertions } from './helpers'

new ApiCheck('api-check', {
  request: {
    url: 'https://api.example.com/status',
    assertions: standardAssertions,
  },
})
```

## Inspect deployed checks

Use these commands when you need to inspect checks that are already deployed in Checkly.

### List checks

```bash
npx checkly checks list
npx checkly checks list --status failing
npx checkly checks list --tag production --type PLAYWRIGHT
npx checkly checks list --search "Homepage" --output json
```

### Get check details

```bash
npx checkly checks get <check-id>
npx checkly checks get <check-id> --output json
npx checkly checks get <check-id> --stats-range last7Days --group-by location
npx checkly checks get <check-id> --results-limit 20 --filter-status failure
```

Look for `errorGroups`, `rootCause`, or `RCA` in the output when investigating failures. If Rocky AI already evaluated the issue, reuse that context in your diagnosis instead of restating the same first-pass analysis.

For `checks get`, detail and markdown output use an internal field projection for the recent-results table to avoid fetching full result bodies. Use `--output json` when you need complete result payloads; `--result <result-id>` and `--include-attempts` still request the full detail payloads.

### Investigate alerting behavior

Use this read-only flow when a user asks why an alert did or did not fire:

```bash
npx checkly checks list --output json --limit 100 --search "<check-name>"
npx checkly checks get <check-id> --output json
npx checkly api /v1/checks/<check-id>
npx checkly alert-channels list --output json --limit 100
```

If a selected check has `groupId`, fetch groups once and locate the matching group:

```bash
npx checkly api /v1/check-groups
```

Analyze only confirmed fields: `activated`, `muted`, `groupId`, `alertSettings`, `useGlobalAlertSettings`, `alertChannelSubscriptions`, `retryStrategy`, and `doubleCheck`. For channels, explain whether subscriptions are check-local, group-scoped, active, inactive, or unrelated. Do not use write methods, trigger checks, mutate incidents, or probe guessed account/global alerting endpoints. If output only shows `useGlobalAlertSettings: true`, report that global alert settings are selected but their policy details were not available in the inspected CLI/API output.

### Drill into a result or error group

```bash
npx checkly checks get <check-id> --result <result-id>
npx checkly checks get <check-id> --result <result-id> --include-attempts
npx checkly checks get <check-id> --error-group <error-group-id>
```

Use `--include-attempts` with `--result` when retry strategy details matter; the output surfaces individual retry-attempt detail for a selected result.

### Delete a deployed check

```bash
npx checkly checks delete <check-id> --dry-run
npx checkly checks delete <check-id> --force
```

Deletion is destructive. Checks managed by a CLI project are recreated on the next deploy, so remove those from project code instead of deleting only the deployed copy. Always run `--dry-run` first and get explicit user approval before running `--force`.

### Result assets

```bash
npx checkly assets list --check-id <check-id> --result-id <result-id>
npx checkly assets download --check-id <check-id> --result-id <result-id> --type trace --dir ./checkly-assets
```

Use `checkly-assets` when you need logs, traces, videos, screenshots, pcap captures, reports, or files attached to a failed result.

### View check stats

```bash
npx checkly checks stats
npx checkly checks stats --range last7Days --tag production
npx checkly checks stats <check-id-1> <check-id-2>
npx checkly checks stats --output json
```

## Troubleshooting

### Check fails locally but passes in UI

**Solution**: Test in Checkly runtime (not just Playwright):
```bash
npx checkly test  # Uses Checkly runtime
```

### Environment variables not working

**Solution**:
```typescript
environmentVariables: [
  { key: 'API_KEY', value: process.env.API_KEY!, locked: true },
]
```

### Browser check selector fails

**Solution**: Use more robust selectors:
```typescript
// ❌ Fragile
await page.click('.button')

// ✅ Better
await page.click('button[data-testid="submit"]')
await page.click('text=Submit')
```

## Related Skills

- See `checkly-test` to test checks locally
- See `checkly-deploy` to deploy checks
- See `checkly-playwright` for full test suites
- See `checkly-advanced` for retry strategies
