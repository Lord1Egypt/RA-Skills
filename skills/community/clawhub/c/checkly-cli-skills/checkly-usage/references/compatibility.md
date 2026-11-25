# Usage CLI compatibility

Checkly CLI **10.3.0 or later** is required for optional projection IDs, unit-aware usage fields, spending-cap commands, and the combined pricing-rule keys `apiAndMultistepChecks` and `browserAndPlaywrightChecks`. CLI 10.2.x does not accept those two filter values; do not pass them to `--pricing-rule` on that toolchain.

The credit-total fields in the skill's JSON migration table were removed/renamed in 10.3.0, not retained as aliases. CLI 10.2.x uses the old credit fields; consumers of current output must use the mapped unit fields and inspect `unit` before interpreting amounts. Upgrading the CLI does not authorize a spending-cap change.

Immutable source comparison: [10.2.0 usage types and pricing-rule keys](https://github.com/checkly/checkly-cli/blob/2b32bb6e0dd4377ca901f3091dd7a7710bcb0b13/packages/cli/src/rest/usage.ts) and [10.3.0 usage types and pricing-rule keys](https://github.com/checkly/checkly-cli/blob/c58d58c171152336dfc87f2e7b77e742f9b4ffa5/packages/cli/src/rest/usage.ts). [Filter validation](https://github.com/checkly/checkly-cli/blob/c58d58c171152336dfc87f2e7b77e742f9b4ffa5/packages/cli/src/helpers/usage.ts) enforces the accepted pricing-rule keys.
