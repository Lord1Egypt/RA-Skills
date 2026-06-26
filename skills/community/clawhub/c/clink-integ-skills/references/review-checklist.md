# Review Checklist

Use this checklist after drafting a standard integration plan, a merchant skill for generic agent integration plan, a merchant skill for OpenClaw integration plan, or a doc-based answer.

This file is for final review and self-check. It is not the primary workflow document.

## Global Checks

- does the output stay aligned with the local Clink docs available in the current environment
- for OpenClaw agent review, did the review load and read `openclaw-payment-skills` through `node scripts/load_payment_skill_contexts.mjs --dependency openclaw-payment-skills --print-path`
- for generic agent review, did the review load and read `agentic-payment-skills` through `node scripts/load_payment_skill_contexts.mjs --dependency agentic-payment-skills --print-path`
- if payment skill context fell back to local files, does the output disclose that exact payment skill behavior is not confirmed latest
- are exact API claims backed by `api-reference/openapi.json`
- does the output avoid inventing undocumented behavior
- is the scenario routing correct

## Standard Integration Checks

- did the design identify the backend language or ask for it when needed
- did the design clarify registered vs non-registered product mode
- for registered product mode, does it explain where active `productId` and `priceId` come from
- for non-registered product mode, does it explain how merchant-defined line items are built into `priceDataList`
- for non-registered product mode, does it keep merchant-specific business inputs in the merchant order model
- for subscription purchases, does it explain whether the flow should create a new checkout session or route to customer portal
- does checkout map merchant `order_id` to `merchantReferenceId`
- does the design avoid treating `merchantReferenceId` as an idempotency key
- does the design keep `originalAmount` aligned with the merchant-defined checkout payload
- does webhook implementation include dashboard subscription and endpoint registration
- when a webhook signing key is requested or configured, does the output tell the user to get it from `Merchant Dashboard > Developers > Webhooks` by registering or selecting the webhook endpoint and copying the endpoint signing key
- when a Secret Key is requested or configured, does the output tell the user to get it from `Merchant Dashboard > Developers > API Keys` by clicking `Initialize Key`, copying it once, and storing it securely
- does the output avoid asking the user to paste real webhook signing keys or Secret Keys into chat, generated source code, docs, logs, or public repositories
- does webhook coverage include subscription lifecycle events when the product mode is subscription-based
- does webhook coverage include `order.refunded` or equivalent refunded-state handling when that state exists in the merchant order model
- does webhook implementation include signature verification, idempotency, retry handling, and out-of-order tolerance
- does the design avoid treating `successUrl` as the only confirmation signal
- does the design clearly separate payment confirmation from merchant fulfillment when downstream delivery exists
- does refund handling describe lifecycle behavior instead of assuming unsupported create APIs

## New User Onboarding Checks

- does onboarding guidance load official docs before giving exact dashboard paths or setup steps
- does it default setup and first checkout guidance to `sandbox`
- does it explain invited-user verification, password setup, and MFA without asking for sensitive values
- does it tell the user to confirm merchant selection and merchant profile under `Settings > Merchant`
- does it explain team access through `Settings > Users` and avoid giving Developer access to roles that docs say do not have it
- does it include Secret Key retrieval through `Merchant Dashboard > Developers > API Keys` and `Initialize Key`
- does it include webhook registration and signing key retrieval through `Merchant Dashboard > Developers > Webhooks`
- does it distinguish registered product mode from non-registered product mode before first checkout setup
- does it explain that subscription recurring payments require pre-created products according to the checkout docs
- does it route the user to standard integration, generic agent integration, OpenClaw integration, or validation after onboarding
- does it avoid inventing KYB, KYC, production activation, payout, or merchant approval details beyond docs-confirmed facts

## Merchant Skill for OpenClaw Integration Checks

- does the design use `openclaw-payment-skills` for the OpenClaw payment skill path
- does the design align exact OpenClaw payment tool names, return directives, and notification ownership with the loaded `openclaw-payment-skills` context
- does the merchant skill call, handle, and resume according to the loaded `openclaw-payment-skills` contract without adding duplicate payment-layer behavior
- does the design clearly distinguish merchant skill from `openclaw-payment-skills`
- does it define merchant server responsibilities
- does it include agent payment session creation/querying
- does it clarify whether the flow is session mode or direct mode
- does it define merchant integration metadata such as `server`, `confirm_tool`, and `confirm_args`
- does it include email verification handling via `customer.verify`
- does it define payment handoff ownership
- does it preserve the structured payment handoff contract instead of paraphrasing it
- does it separate payment-layer success from merchant-layer confirmation result
- does it call or describe merchant confirmation exactly once per payment result unless retry is explicitly required
- does it define merchant confirmation and task resume behavior

## Merchant Skill for Generic Agent Integration Checks

- does the design identify that the runtime is not OpenClaw when taking the merchant skill for generic agent path
- does it define merchant skill or merchant tool responsibilities before delegating to the generic agent runtime or adapter
- does the design use `agentic-payment-skills` / `clink-payment-skill` as the generic agent payment skill
- does the design align exact CLI flags, exit-code handling, refund behavior, and payment-method freshness rules with the loaded `agentic-payment-skills` context
- does the merchant skill or adapter call, handle, and resume according to the loaded `agentic-payment-skills` / `clink-payment-skill` contract without assuming OpenClaw runtime behavior
- does it account for `clink-cli` JSON output and exit code handling
- does it require Node.js >= 20 and `clink-cli` installation before payment operations
- does it avoid automatic `wallet init` during payment and handle exit code `3` or `4` as setup/auth recovery
- does it require payment-method freshness through `card binding-link` instead of trusting `card list` cache alone
- does it prevent `customerApiKey` exposure and require `CLINK_CUSTOMER_API_KEY` piping for customer API key configuration
- does it use `--dry-run` for preview or input verification requests
- does it define `clink-cli pay` status handling for status `1`, status `3`, status `4`, and status `6`
- does it require explicit refund request and original `orderId` for refund submission
- does it define the agent runtime contract instead of assuming OpenClaw-specific session, memory, tool, or resume behavior
- does it clarify session mode, direct mode, or adapter mode
- does it support merchant `402 Payment Required` handoff when the merchant uses that protocol
- does a merchant-originated payment handoff include structured `payment_required` data, exact payment parameters, correlation data, and a retry or resume target
- does it define how the generic agent invokes `clink-payment-skill` or the adapter around it
- does it prevent invented payment parameters and require explicit authorization before charge execution
- does it define the payment handoff contract and preserve it as structured data
- does it include merchant confirmation ownership and exactly-once or idempotent confirmation behavior
- does it define callback, polling, queue, or recovery behavior for asynchronous payment completion
- does it define task resume behavior after merchant confirmation
- does it separate merchant skill or tool, agent runtime, adapter, merchant server, `agentic-payment-skills`, webhook handler, notification sender, and recovery ownership
- does it include `customer.verify` handling when email verification is in scope

## Documentation Checks

- is the structure modular and easy to extend
- is the main `SKILL.md` concise
- are detailed workflows moved into reference modules
- are English and Chinese docs aligned when both are updated
- do validation-heavy answers point to generated artifacts or lint reports when that would help the developer more than prose
