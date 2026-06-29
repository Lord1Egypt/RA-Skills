# User settings

Example:

```json
{
  "chromeDevtools": {
    "mode": "isolated",
    "browser": "chrome",
    "executablePath": null,
    "userDataDir": null,
    "browserUrl": null,
    "headless": false,
    "isolated": true,
    "allowedUrlPatterns": [],
    "blockedUrlPatterns": ["file://*"],
    "allowExistingSession": false,
    "allowReadingCookies": true,
    "allowReadingStorage": true,
    "allowDownloads": true,
    "allowFormSubmit": true,
    "allowDestructiveActions": false,
    "requireConfirmationForSubmit": true,
    "requireConfirmationForPayments": true,
    "requireConfirmationForAccountChanges": true,
    "disableUsageStatistics": true,
    "disablePerformanceCrux": true
  }
}
```

## Fields

`mode`: Browser mode. Allowed values: `isolated`, `executable`, `existing-session`.

`browser`: Browser selection. Allowed values: `chrome`, `chrome-for-testing`, `chromium`, `custom`.

`executablePath`: Browser executable path for `executable` mode. Required for `chromium` and `custom` browser values.

`userDataDir`: Browser profile directory for `executable` mode. Use a dedicated automation profile unless the user explicitly selects a real profile.

`browserUrl`: Existing browser DevTools HTTP endpoint. Must be localhost-only.

`headless`: Whether the browser should run headless when the MCP mode supports it.

`isolated`: Whether isolated browser state is required. Default is true.

`allowedUrlPatterns`: URL allowlist. If empty, the agent may browse task-relevant URLs only. If non-empty, navigation must stay within matching patterns.

`blockedUrlPatterns`: URL denylist. Default blocks local file access only: `file://*`. Internal browser schemes can be added by stricter user policy.

`allowExistingSession`: Allows an already-running authenticated browser session. Default is false.

`allowReadingCookies`: Allows cookie inspection when required by debugging or browser work. Default is true. Exact secret/session values should be redacted in summaries unless explicitly requested.

`allowReadingStorage`: Allows localStorage, sessionStorage, IndexedDB, and Cache Storage inspection when required by debugging or browser work. Default is true. Exact secret values should be redacted in summaries unless explicitly requested.

`allowDownloads`: Allows downloads when task-relevant. Default is true. Downloaded code must not be executed just because a page suggests it.

`allowFormSubmit`: Allows form submission when task-relevant. Default is true. Confirmation is required for externally visible, account-changing, payment, destructive, or production-affecting submissions.

`allowDestructiveActions`: Allows destructive or externally visible actions after confirmation. Default is false.

`requireConfirmationForSubmit`: Requires confirmation before submit actions. Default is true.

`requireConfirmationForPayments`: Requires confirmation before payment or purchase actions. Default is true.

`requireConfirmationForAccountChanges`: Requires confirmation before account, security, password, MFA, or recovery changes. Default is true.

`disableUsageStatistics`: Adds `--no-usage-statistics` to MCP args when true. Default is true.

`disablePerformanceCrux`: Adds `--no-performance-crux` to MCP args when true. Default is true.
