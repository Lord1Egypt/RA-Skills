#!/usr/bin/env bash
# ==============================================================================
# FeatureLint - Feature Flag Hygiene Analyzer
# Pattern Definitions (90 patterns across 6 categories)
# Format: REGEX|SEVERITY|CHECK_ID|DESCRIPTION|RECOMMENDATION
# POSIX ERE syntax throughout
# ==============================================================================
set -euo pipefail

# ==============================================================================
# Category 1: SF - Stale Flags (SF-001 to SF-015)
# Detects feature flags that are outdated, unused, or should be removed
# Tier: Free
# ==============================================================================
FEATURELINT_SF_PATTERNS=(
  # SF-001: Flag check with TODO/FIXME comment nearby
  '(TODO|FIXME|HACK|XXX)[[:space:]].*([Ff]lag|[Ff]eature[[:space:]]*[Ff]lag|[Tt]oggle)|error|SF-001|Flag check accompanied by TODO/FIXME comment suggests deferred cleanup|Remove the flag and resolve the TODO; schedule a cleanup ticket if not immediately actionable'

  # SF-002: Hardcoded flag value (always true/false)
  '([Ff]lag|[Ff]eature[Ff]lag|[Tt]oggle)[[:space:]]*=[[:space:]]*(true|false|True|False|TRUE|FALSE)[[:space:]]*;|warning|SF-002|Feature flag hardcoded to a constant boolean value|Remove the flag and its conditional branches; the flag is effectively permanent'

  # SF-003: Feature flag name containing "temp" or "temporary"
  '([Ff]lag|[Ff]eature|[Tt]oggle)[_-]*(temp|temporary|tmp)[_-]*[[:alnum:]]|warning|SF-003|Flag name contains temp or temporary suggesting it should have been removed|Create a removal ticket and schedule cleanup within the current sprint'

  # SF-004: Commented-out flag conditional
  '(\/\/|#|\/\*)[[:space:]]*(if|when|unless)[[:space:]]*.*([Ff]lag|[Ff]eature[Ff]lag|[Tt]oggle)|warning|SF-004|Commented-out feature flag conditional found in codebase|Delete the commented code entirely; version control preserves history if needed'

  # SF-005: Flag with date reference in past year
  '([Ff]lag|[Ff]eature|[Tt]oggle).*20(19|20|21|22|23|24)[_-](0[1-9]|1[0-2])|warning|SF-005|Feature flag contains a date reference that appears to be stale|Review whether the flag has served its purpose and remove if rollout is complete'

  # SF-006: Boolean literal in flag evaluation
  '(isEnabled|isActive|isOn|evaluate)[[:space:]]*\([[:space:]]*(true|false)|error|SF-006|Boolean literal passed directly to flag evaluation function|Use a proper flag key string instead of a hardcoded boolean value'

  # SF-007: Flag variable assigned but never toggled
  'const[[:space:]]+(FLAG|FEATURE|TOGGLE)[_[:alnum:]]*[[:space:]]*=[[:space:]]*(true|false)|warning|SF-007|Flag variable declared as constant suggesting it is never dynamically toggled|Move flag evaluation to your flag SDK or remove the constant entirely'

  # SF-008: Unused flag import/require
  '(import|require).*([Ff]lag[Ss]ervice|[Ff]eature[Ff]lag|[Ff]lag[Pp]rovider|[Ff]lag[Cc]lient).*[[:space:]]*(\/\/|#)[[:space:]]*unused|info|SF-008|Feature flag module imported but marked as unused|Remove the unused import to reduce bundle size and confusion'

  # SF-009: Flag with "old" or "legacy" in name
  '([Ff]lag|[Ff]eature|[Tt]oggle)[_-]*(old|legacy|deprecated|obsolete)[_-]*[[:alnum:]]|warning|SF-009|Flag name contains old or legacy indicating it should be cleaned up|Remove the legacy flag and migrate to the replacement if one exists'

  # SF-010: Dead else branch after permanent flag
  'if[[:space:]]*\([[:space:]]*(true|TRUE|True)[[:space:]]*\)[[:space:]]*\{[^}]*\}[[:space:]]*else|error|SF-010|Dead else branch after a permanently enabled flag condition|Remove the else branch since the condition is always true'

  # SF-011: Flag enabled in all environments
  '(dev|staging|prod|production|test)[[:space:]]*:[[:space:]]*(true|enabled|on)[[:space:]]*.*(dev|staging|prod|production|test)[[:space:]]*:[[:space:]]*(true|enabled|on)|warning|SF-011|Flag appears to be enabled across all environments|If the flag is enabled everywhere it should be removed and code made permanent'

  # SF-012: Flag check followed by unreachable code
  'return[[:space:]].*([Ff]lag|[Ff]eature|[Tt]oggle).*\n.*return[[:space:]]|warning|SF-012|Flag check results in unreachable code below|Remove the unreachable code path or restructure the flag conditional'

  # SF-013: Disabled flag block still in codebase
  '([Ff]lag|[Ff]eature|[Tt]oggle)[[:space:]]*=[[:space:]]*(false|False|FALSE|off|OFF|disabled)|info|SF-013|Disabled feature flag block still present in codebase|Remove the disabled flag and its gated code to reduce dead code'

  # SF-014: Constant flag export
  'export[[:space:]]+(const|default)[[:space:]]+(FLAG|FEATURE|TOGGLE)[_[:alnum:]]*[[:space:]]*=|warning|SF-014|Feature flag exported as a constant value|Move flag evaluation to runtime SDK calls instead of compile-time constants'

  # SF-015: Stale experiment flag name
  '([Ff]lag|[Ff]eature|[Tt]oggle)[_-]*(experiment|exp|ab[_-]*test|variant)[_-]*[[:alnum:]]|info|SF-015|Experiment or A/B test flag still present in codebase|Verify experiment conclusion and remove the flag with its losing variant code'
)

# ==============================================================================
# Category 2: FC - Flag Complexity (FC-001 to FC-015)
# Detects overly complex flag usage patterns
# Tier: Free
# ==============================================================================
FEATURELINT_FC_PATTERNS=(
  # FC-001: Nested flag conditions (flag inside flag check)
  'if.*([Ff]lag|[Ff]eature|[Tt]oggle).*if.*([Ff]lag|[Ff]eature|[Tt]oggle)|error|FC-001|Nested feature flag conditions create complex branching logic|Extract inner flag checks into separate functions or combine flags into a single evaluation'

  # FC-002: Flag combined with complex boolean (3+ conditions)
  '([Ff]lag|[Ff]eature|[Tt]oggle).*&&.*&&.*&&|warning|FC-002|Feature flag combined with three or more boolean conditions|Simplify by extracting complex conditions into a named helper function'

  # FC-003: More than 3 flags checked in single function
  '(isEnabled|isActive|isOn|getFlag|evaluate|variation).*\n.*(isEnabled|isActive|isOn|getFlag|evaluate|variation).*\n.*(isEnabled|isActive|isOn|getFlag|evaluate|variation)|warning|FC-003|Multiple feature flag evaluations in a single function|Consolidate flag checks into a single configuration object or strategy pattern'

  # FC-004: Flag spanning multiple files without abstraction
  '(getFlag|isEnabled|evaluate|variation)[[:space:]]*\([[:space:]]*["\x27](feature[_-]|flag[_-]|toggle[_-]|ff[_-])[[:alnum:]_-]*["\x27]|info|FC-004|Raw flag key string used without abstraction layer|Create a centralized flag registry module to manage all flag keys'

  # FC-005: Flag in hot path without caching
  'for[[:space:]]*\(.*\).*\{[^}]*(getFlag|isEnabled|evaluate|variation)|error|FC-005|Feature flag evaluated inside a loop without caching the result|Cache the flag value before the loop to avoid repeated SDK calls'

  # FC-006: Deeply nested ternary with flag
  '([Ff]lag|[Ff]eature|[Tt]oggle).*\?.*\?.*\?|warning|FC-006|Deeply nested ternary expression involving feature flag|Replace nested ternaries with explicit if-else blocks or a lookup table'

  # FC-007: Flag condition duplicated across files
  'if[[:space:]]*\([[:space:]]*(isEnabled|isActive|getFlag|evaluate)[[:space:]]*\([[:space:]]*["\x27][[:alnum:]_-]*["\x27][[:space:]]*\)|info|FC-007|Same flag condition pattern appears in multiple locations|Extract the flag check into a shared utility or hook for single-point-of-change'

  # FC-008: Flag combined with permission check in complex expression
  '([Ff]lag|[Ff]eature|[Tt]oggle).*(permission|role|access|auth).*&&|warning|FC-008|Feature flag interleaved with permission or authorization logic|Separate flag evaluation from authorization checks into distinct layers'

  # FC-009: Multiple flag SDK calls in single render
  '(useFlag|useFeature|useFlagVariation|useFeatureFlag).*\n.*(useFlag|useFeature|useFlagVariation|useFeatureFlag)|warning|FC-009|Multiple feature flag hook calls in a single component render|Consolidate into a single useFlags hook or create a flag context provider'

  # FC-010: Flag entanglement (result depends on ordering)
  '([Ff]lag|[Ff]eature|[Tt]oggle)[[:alnum:]_]*[[:space:]]*&&[[:space:]]*([Ff]lag|[Ff]eature|[Tt]oggle)[[:alnum:]_]*[[:space:]]*&&[[:space:]]*([Ff]lag|[Ff]eature|[Tt]oggle)|error|FC-010|Multiple flags combined with logical AND creating ordering dependency|Document flag dependencies and consider combining into a composite flag'

  # FC-011: Excessive flag branching (switch-case)
  'switch[[:space:]]*\([[:space:]]*(flag|feature|toggle|variant|variation)|warning|FC-011|Switch statement on flag or variant value creates excessive branching|Use a strategy pattern or lookup map instead of switch-case for flag variants'

  # FC-012: Flag check in loop body
  'while[[:space:]]*\(.*\)[[:space:]]*\{[^}]*(getFlag|isEnabled|evaluate|isActive)|warning|FC-012|Feature flag evaluated inside a while loop body|Hoist the flag evaluation outside the loop and cache the result'

  # FC-013: Flag composition without helper
  '(getFlag|isEnabled|evaluate|variation).*\|\|.*(getFlag|isEnabled|evaluate|variation)|warning|FC-013|Multiple flag evaluations composed inline without a helper|Create a named function that encapsulates the composite flag logic'

  # FC-014: Flag-gated import without lazy loading
  'import[[:space:]].*from.*\n.*if.*(flag|feature|toggle|isEnabled)|info|FC-014|Static import gated behind a flag check wastes bundle size|Use dynamic import or lazy loading for flag-gated modules'

  # FC-015: Cyclic flag dependency
  '([Ff]lag|[Ff]eature|[Tt]oggle)[[:alnum:]_]*.*depends[Oo]n.*([Ff]lag|[Ff]eature|[Tt]oggle)|error|FC-015|Potential cyclic dependency between feature flags detected|Map flag dependencies and eliminate cycles using a dependency graph'
)

# ==============================================================================
# Category 3: FS - Flag Safety (FS-001 to FS-015)
# Detects flags in security-critical or high-risk code paths
# Tier: Pro
# ==============================================================================
FEATURELINT_FS_PATTERNS=(
  # FS-001: Flag controlling security-critical path (auth/login)
  '([Ff]lag|[Ff]eature|[Tt]oggle).*(auth|login|signIn|sign[_-]in|authenticate)|error|FS-001|Feature flag controls a security-critical authentication path|Avoid gating authentication behind feature flags; use dedicated security configuration'

  # FS-002: Flag gating authorization middleware
  'if.*(flag|feature|toggle|isEnabled).*(middleware|authorize|checkPermission|guard)|error|FS-002|Feature flag gates authorization or middleware execution|Authorization logic must not be conditionally disabled by feature flags'

  # FS-003: Flag on database migration/schema change
  '([Ff]lag|[Ff]eature|[Tt]oggle).*(migrate|migration|schema|alter[Tt]able|createTable)|error|FS-003|Feature flag controlling database migration or schema change|Database migrations should be deterministic and not gated by runtime flags'

  # FS-004: Flag with no default/fallback value
  '(getFlag|evaluate|variation|isEnabled)[[:space:]]*\([[:space:]]*["\x27][[:alnum:]_-]*["\x27][[:space:]]*\)|warning|FS-004|Flag evaluation without a default or fallback value parameter|Always provide a safe default value when evaluating feature flags'

  # FS-005: Flag in error handling path
  '(catch|except|rescue|onError|handleError).*([Ff]lag|[Ff]eature|[Tt]oggle|isEnabled)|error|FS-005|Feature flag evaluated inside error handling or catch block|Error handling paths should be deterministic and not depend on flag state'

  # FS-006: Feature flag in payment/billing flow
  '([Ff]lag|[Ff]eature|[Tt]oggle).*(payment|billing|charge|invoice|checkout|stripe|paypal)|error|FS-006|Feature flag detected in payment or billing code path|Payment flows require thorough testing; avoid toggling payment logic with flags'

  # FS-007: Flag controlling data deletion
  '([Ff]lag|[Ff]eature|[Tt]oggle).*(delete|remove|purge|destroy|truncate|drop)|error|FS-007|Feature flag controlling a data deletion operation|Data deletion should never be gated by a feature flag; use explicit admin actions'

  # FS-008: Flag in encryption/decryption path
  '([Ff]lag|[Ff]eature|[Tt]oggle).*(encrypt|decrypt|cipher|hash|hmac|crypto)|error|FS-008|Feature flag detected in encryption or decryption code path|Cryptographic operations must not be conditionally applied via feature flags'

  # FS-009: Flag on rate limiting/throttling
  '([Ff]lag|[Ff]eature|[Tt]oggle).*(rateLimit|rate[_-]limit|throttle|quota)|warning|FS-009|Feature flag controls rate limiting or throttling configuration|Rate limiting should be configured via dedicated infrastructure not feature flags'

  # FS-010: Flag gating API authentication
  '([Ff]lag|[Ff]eature|[Tt]oggle).*(apiKey|api[_-]key|bearer|token[Vv]alidat|jwt[Vv]erif)|error|FS-010|Feature flag gates API authentication or token validation|API authentication must always be enforced; never gate it behind a feature flag'

  # FS-011: Flag controlling PII handling
  '([Ff]lag|[Ff]eature|[Tt]oggle).*(pii|personal[Dd]ata|gdpr|ccpa|anonymize|redact)|warning|FS-011|Feature flag controlling PII handling or data privacy logic|Privacy and compliance logic should not be toggled by feature flags'

  # FS-012: Kill-switch without documentation
  '(kill[_-]*[Ss]witch|circuit[_-]*[Bb]reaker|emergency[_-]*[Ss]top)[[:space:]]*=[[:space:]]|warning|FS-012|Kill-switch or circuit breaker defined without inline documentation|Document the kill-switch purpose, trigger conditions, and restoration procedure'

  # FS-013: Flag modifying database write path
  '([Ff]lag|[Ff]eature|[Tt]oggle).*(insert|update|upsert|save|persist|write[Tt]o[Dd]b)|warning|FS-013|Feature flag modifies a database write operation path|Ensure flag-gated write paths have rollback strategies and data integrity checks'

  # FS-014: Flag on session management
  '([Ff]lag|[Ff]eature|[Tt]oggle).*(session|cookie|csrf|xsrf|[Ss]ession[Mm]anag)|error|FS-014|Feature flag controlling session or cookie management|Session management should be deterministic and not dependent on feature flags'

  # FS-015: Flag in audit logging path
  '([Ff]lag|[Ff]eature|[Tt]oggle).*(audit|auditLog|audit[_-]log|compliance[Ll]og)|error|FS-015|Feature flag detected in audit logging or compliance path|Audit logging must always be active and never conditionally disabled by flags'
)

# ==============================================================================
# Category 4: SM - SDK Misuse (SM-001 to SM-015)
# Detects incorrect or suboptimal feature flag SDK usage
# Tier: Pro
# ==============================================================================
FEATURELINT_SM_PATTERNS=(
  # SM-001: Missing flag evaluation default value
  '\.(getFlag|evaluate|variation|boolVariation|stringVariation)[[:space:]]*\([[:space:]]*["\x27][^"]*["\x27][[:space:]]*\)|warning|SM-001|Feature flag SDK call missing a default fallback value|Always pass a default value as the second argument to flag evaluation methods'

  # SM-002: Flag evaluated in loop (should cache)
  '(for|while|forEach|map)[[:space:]]*\(.*\).*\.(getFlag|evaluate|variation|isEnabled)|error|SM-002|Feature flag SDK evaluated repeatedly inside a loop|Cache the flag result in a variable before the loop to avoid repeated evaluations'

  # SM-003: Hardcoded flag key strings (not constants)
  '(getFlag|evaluate|variation|isEnabled)[[:space:]]*\([[:space:]]*["\x27][a-z][a-z0-9_-]*["\x27]|info|SM-003|Hardcoded flag key string literal instead of a named constant|Define flag keys as constants in a shared module for type safety and refactoring'

  # SM-004: Missing flag context/user targeting
  '(getFlag|evaluate|variation|isEnabled)[[:space:]]*\([[:space:]]*["\x27][^"]*["\x27][[:space:]]*,[[:space:]]*["\x27]|warning|SM-004|Flag evaluation missing user context for targeting rules|Pass a user or context object to enable proper flag targeting and segmentation'

  # SM-005: Flag client initialized without timeout
  '(init|initialize|create)[Cc]lient[[:space:]]*\([[:space:]]*\{[^}]*(key|sdkKey|apiKey)[^}]*\}[[:space:]]*\)|warning|SM-005|Feature flag client initialized without a connection timeout|Set a timeout on the SDK client initialization to prevent hanging on startup'

  # SM-006: Missing flag change listener cleanup
  '(on|addEventListener|subscribe)[[:space:]]*\([[:space:]]*["\x27](flag|feature|change|update)|warning|SM-006|Feature flag change listener registered without cleanup logic|Add corresponding removeEventListener or unsubscribe in cleanup or teardown'

  # SM-007: Flag SDK initialized multiple times
  '(init|initialize|create)[[:space:]]*(Client|SDK|Provider|Instance).*\n.*(init|initialize|create)[[:space:]]*(Client|SDK|Provider|Instance)|error|SM-007|Feature flag SDK appears to be initialized multiple times|Initialize the flag SDK once at application startup and share the instance'

  # SM-008: Synchronous flag evaluation in async context
  '(async|await).*\.(getFlag|evaluate|variation|isEnabled)[[:space:]]*\([^)]*\)[[:space:]]*[^;]*[[:space:]]*[^a][^w]|info|SM-008|Synchronous flag evaluation used within an async function context|Use the async variant of the flag SDK method for consistency in async contexts'

  # SM-009: Missing flag SDK error handling
  '\.(getFlag|evaluate|variation|isEnabled)[[:space:]]*\([^)]*\)[[:space:]]*$|warning|SM-009|Feature flag evaluation without error handling or try-catch wrapper|Wrap flag evaluations in try-catch blocks to handle SDK failures gracefully'

  # SM-010: No fallback when SDK unavailable
  '(flagClient|flagService|featureClient)[[:space:]]*\.[[:space:]]*(getFlag|evaluate|variation)[[:space:]]*\(|warning|SM-010|Flag SDK call without fallback strategy when service is unavailable|Implement a fallback mechanism for when the flag SDK service is unreachable'

  # SM-011: Flag variation called without user context
  '(variation|boolVariation|stringVariation|numberVariation)[[:space:]]*\([[:space:]]*["\x27][^"]*["\x27][[:space:]]*,[[:space:]]*(null|undefined|nil|\{\})|warning|SM-011|Flag variation evaluated with null or empty user context|Provide a valid user context object for proper flag targeting and evaluation'

  # SM-012: Stale flag value after SDK update
  'const[[:space:]]+[[:alnum:]_]*[Ff]lag[[:alnum:]_]*[[:space:]]*=[[:space:]]*(getFlag|evaluate|variation|isEnabled)|info|SM-012|Flag value stored in const may become stale after SDK updates|Use a reactive pattern or hook to ensure the flag value stays current'

  # SM-013: Missing flag SDK shutdown/close
  '(process|app)\.(on|exit|close)[[:space:]]*\([[:space:]]*["\x27](exit|close|SIGTERM|SIGINT|beforeExit)|info|SM-013|Application exit handler does not include flag SDK shutdown call|Call flagClient.close or flush in your shutdown handler to ensure data is sent'

  # SM-014: Flag key typo risk (string literal)
  '(getFlag|evaluate|variation|isEnabled)[[:space:]]*\([[:space:]]*["\x27][[:alnum:]]*[[:upper:]][[:alnum:]]*[[:upper:]][[:alnum:]]*["\x27]|info|SM-014|Flag key uses mixed casing which increases typo risk|Use consistent kebab-case or snake_case for flag key naming to reduce typos'

  # SM-015: No flag SDK connection retry
  '(init|initialize|create)[[:space:]]*(Client|SDK)[[:space:]]*\([^)]*\)[[:space:]]*;[[:space:]]*$|info|SM-015|Flag SDK initialization without retry or reconnection configuration|Configure retry logic and reconnection parameters for SDK initialization'
)

# ==============================================================================
# Category 5: FL - Flag Lifecycle (FL-001 to FL-015)
# Detects lifecycle management issues with feature flags
# Tier: Team
# ==============================================================================
FEATURELINT_FL_PATTERNS=(
  # FL-001: Flag older than 90 days without cleanup TODO
  '([Ff]lag|[Ff]eature|[Tt]oggle).*[Cc]reated.*(20[0-2][0-9])[^T]*[^O]*[^D]*[^O]|info|FL-001|Feature flag appears to be older than 90 days without a cleanup note|Add a cleanup TODO with a target date and link to a tracking ticket'

  # FL-002: Permanent flags mixed with release flags
  '(permanent|long[_-]*lived|core)[[:space:]]*(flag|feature|toggle).*(release|rollout|launch)|warning|FL-002|Permanent flags mixed with release flags in the same module|Separate permanent operational flags from temporary release flags into distinct files'

  # FL-003: Kill-switch without expiration plan
  '(kill[_-]*[Ss]witch|circuit[_-]*[Bb]reaker|emergency[_-]*[Ff]lag)[[:space:]]*[=:][[:space:]]*|warning|FL-003|Kill-switch or circuit breaker defined without an expiration plan|Document the expected lifetime and review schedule for the kill-switch'

  # FL-004: Flag percentage rollout without monitoring
  '(percentage|percent|rollout[_-]*pct|rollout[Pp]ercent)[[:space:]]*[=:][[:space:]]*[0-9]|info|FL-004|Flag percentage rollout configured without associated monitoring|Set up monitoring and alerting for metrics affected by the gradual rollout'

  # FL-005: Flag targeting with PII (email/name in targeting)
  '(target|segment|user[Cc]ontext).*(@|email|[Ff]irst[Nn]ame|[Ll]ast[Nn]ame|phone)|warning|FL-005|Feature flag targeting rules contain potential PII like email or name|Use anonymized user identifiers instead of PII for flag targeting rules'

  # FL-006: No flag removal ticket/issue reference
  '([Ff]lag|[Ff]eature|[Tt]oggle)[[:space:]]*[=:][[:space:]]*[^/]*[^/]*[^J][^I][^R][^A][^-]$|info|FL-006|Feature flag defined without a reference to a removal ticket or issue|Add a comment with the ticket URL for tracking flag cleanup work'

  # FL-007: Feature flag without owner annotation
  '([Ff]lag|[Ff]eature|[Tt]oggle)[[:space:]]*[=:][[:space:]]*[{]|info|FL-007|Feature flag defined without an owner or team annotation|Add an owner annotation to every flag definition for accountability'

  # FL-008: Abandoned experiment flag
  '(experiment|exp|ab[_-]*test)[[:space:]]*(flag|feature|toggle).*[=:][[:space:]]*(false|off|disabled|0)|warning|FL-008|Experiment or A/B test flag appears to be abandoned in disabled state|Remove the experiment flag and its associated code paths after conclusion'

  # FL-009: Flag created without cleanup date
  '(new|create|register|add)[[:space:]]*(Flag|Feature|Toggle)[[:space:]]*\([[:space:]]*[{][^}]*[}][[:space:]]*\)|info|FL-009|Feature flag created without a cleanup or expiration date|Include a cleanupDate or expiresAt field when registering new flags'

  # FL-010: Flag rollout at 100% without removal
  '(rollout|percentage|percent)[[:space:]]*[=:][[:space:]]*100|warning|FL-010|Feature flag at 100 percent rollout should be removed|A flag at full rollout is effectively permanent; remove it and make the code default'

  # FL-011: Gradual rollout without metrics check
  '(rollout|canary|gradual|incremental)[[:space:]]*(flag|feature|toggle)[^m]*[^e]*[^t]*[^r]*[^i]*[^c]|info|FL-011|Gradual rollout flag configured without associated metrics validation|Define success and error metrics to monitor during the gradual rollout phase'

  # FL-012: Flag with no associated test
  '([Ff]lag|[Ff]eature|[Tt]oggle)[[:alnum:]_]*[[:space:]]*[=:][[:space:]]*(true|false|["\x27])|info|FL-012|Feature flag definition found without a corresponding test reference|Write tests covering both the enabled and disabled states of the flag'

  # FL-013: Flag enabled but feature code removed
  '(isEnabled|isActive|getFlag|evaluate)[[:space:]]*\([[:space:]]*["\x27][[:alnum:]_-]*["\x27].*\)[[:space:]]*[;][[:space:]]*$|info|FL-013|Flag evaluation exists but the gated feature code may have been removed|Verify the flag still gates active code; remove the evaluation if the feature is gone'

  # FL-014: Release flag still gating after GA
  '(release|launch|ga|general[_-]*availability)[[:space:]]*(flag|feature|toggle)[[:space:]]*[=:][[:space:]]*(true|enabled)|warning|FL-014|Release flag still active after general availability|Remove the release flag since the feature is now generally available'

  # FL-015: Temporary flag without expiry metadata
  '(temp|temporary|short[_-]*lived)[[:space:]]*(flag|feature|toggle)[[:space:]]*[=:][[:space:]]|warning|FL-015|Temporary flag defined without expiry metadata or cleanup date|Add expiresAt or maxLifetimeDays metadata to temporary flag definitions'
)

# ==============================================================================
# Category 6: FA - Flag Architecture (FA-001 to FA-015)
# Detects architectural issues with feature flag design and placement
# Tier: Team
# ==============================================================================
FEATURELINT_FA_PATTERNS=(
  # FA-001: Flag evaluated at wrong layer (UI checking backend flag)
  '(component|render|jsx|tsx|vue|html).*\.(getFlag|evaluate|variation|isEnabled)[[:space:]]*\([[:space:]]*["\x27](backend|server|api|service)|warning|FA-001|UI layer evaluating a backend or server-side feature flag|Evaluate backend flags on the server and pass the result to the UI layer'

  # FA-002: Flag coupling between services (shared flag keys)
  '(service|microservice|api)[[:space:]]*(flag|feature|toggle)[[:space:]]*[=:][[:space:]]*["\x27](shared|common|global)|warning|FA-002|Feature flag key shared between services creates coupling|Each service should own its flag definitions; use events for cross-service coordination'

  # FA-003: Flag not evaluated at edge/entry point
  '(handler|controller|endpoint|route|resolver).*\{[^}]*(getFlag|isEnabled|evaluate|variation)|info|FA-003|Feature flag evaluated deep in handler instead of at the entry point|Evaluate flags at the request entry point and pass the result as context'

  # FA-004: Missing flag audit logging
  '(getFlag|evaluate|variation|isEnabled)[[:space:]]*\([^)]*\)[[:space:]]*[;][[:space:]]*[^l]*[^o]*[^g]|info|FA-004|Feature flag evaluation without corresponding audit log entry|Log flag evaluations for debugging and audit trail purposes'

  # FA-005: No centralized flag definition/registry
  '["\x27](flag|feature|toggle)[_-][[:alnum:]_-]*["\x27][[:space:]]*[,)][[:space:]]*$|info|FA-005|Flag key used inline without a centralized registry or definition file|Create a flag registry module that defines all flag keys as named exports'

  # FA-006: Flag configuration in code vs config store
  '(const|let|var)[[:space:]]+(FLAG|FEATURE|TOGGLE)[_[:alnum:]]*[[:space:]]*=[[:space:]]*\{[^}]*(key|name|default)|warning|FA-006|Feature flag configuration embedded in application code|Move flag configuration to an external config store or environment variables'

  # FA-007: Flag evaluation in shared library without injection
  '(lib|shared|common|util|utils)[[:space:]]*[/].*\.(getFlag|evaluate|variation|isEnabled)|warning|FA-007|Feature flag evaluated directly in shared library code|Inject the flag value via dependency injection instead of evaluating in shared code'

  # FA-008: Server-side flag leaked to client
  '(res|response)\.(json|send|render).*([Ff]lag|[Ff]eature|[Tt]oggle)[[:alnum:]_]*[[:space:]]*[=:]|warning|FA-008|Server-side feature flag value leaked to client response|Filter internal flag state from API responses to prevent client exposure'

  # FA-009: Flag state stored in local storage
  '(localStorage|sessionStorage|window\.localStorage)\.(setItem|getItem).*([Ff]lag|[Ff]eature|[Tt]oggle)|warning|FA-009|Feature flag state stored in browser local storage|Evaluate flags from the SDK on each load rather than caching in local storage'

  # FA-010: Inconsistent flag naming convention
  '(getFlag|evaluate|variation|isEnabled)[[:space:]]*\([[:space:]]*["\x27][A-Z][[:alnum:]]*["\x27]|info|FA-010|Flag key uses PascalCase which may be inconsistent with project conventions|Adopt a consistent naming convention like kebab-case for all flag keys'

  # FA-011: Missing flag documentation/description
  '(registerFlag|createFlag|defineFlag|addFlag)[[:space:]]*\([[:space:]]*[{][^}]*key[^}]*[}]|info|FA-011|Feature flag registered without a description or documentation field|Add a description field explaining the flag purpose and expected behavior'

  # FA-012: Flag evaluated after side effect
  '(save|write|send|post|put|patch|delete|emit|dispatch|publish)\(.*\).*\n.*(getFlag|isEnabled|evaluate|variation)|error|FA-012|Feature flag evaluated after a side effect has already executed|Evaluate feature flags before performing side effects to prevent partial execution'

  # FA-013: No flag dependency graph
  '([Ff]lag|[Ff]eature|[Tt]oggle)[[:alnum:]_]*[[:space:]]*(requires|dependsOn|needs|after)[[:space:]]*[=:][[:space:]]*["\x27]([Ff]lag|[Ff]eature|[Tt]oggle)|warning|FA-013|Flag dependencies declared without a dependency graph or validation|Build a flag dependency graph and validate it during initialization for cycles'

  # FA-014: Client-side flag without server validation
  'if[[:space:]]*\([[:space:]]*(window|document|navigator|client|browser).*([Ff]lag|[Ff]eature|[Tt]oggle)|warning|FA-014|Client-side flag evaluation without server-side validation|Validate flag state server-side to prevent client-side manipulation'

  # FA-015: Flag evaluation result not logged
  '(const|let|var)[[:space:]]+[[:alnum:]_]*[[:space:]]*=[[:space:]]*(getFlag|evaluate|variation|isEnabled)[[:space:]]*\([^)]*\)[[:space:]]*;[[:space:]]*$|info|FA-015|Flag evaluation result not logged or recorded for observability|Log the flag evaluation result for debugging and operational visibility'
)

# ==============================================================================
# Tier Gating Configuration
# Free:  SF + FC  (30 patterns)
# Pro:   SF + FC + FS + SM  (60 patterns)
# Team:  SF + FC + FS + SM + FL + FA  (90 patterns)
# ==============================================================================
featurelint_get_tier_patterns() {
    local tier="${1:-free}"
    case "${tier}" in
        free)
            echo "SF FC"
            ;;
        pro)
            echo "SF FC FS SM"
            ;;
        team)
            echo "SF FC FS SM FL FA"
            ;;
        *)
            echo "SF FC"
            ;;
    esac
}

# Return the pattern array name for a given category code
featurelint_get_pattern_array() {
    local category="$1"
    case "${category}" in
        SF) echo "FEATURELINT_SF_PATTERNS" ;;
        FC) echo "FEATURELINT_FC_PATTERNS" ;;
        FS) echo "FEATURELINT_FS_PATTERNS" ;;
        SM) echo "FEATURELINT_SM_PATTERNS" ;;
        FL) echo "FEATURELINT_FL_PATTERNS" ;;
        FA) echo "FEATURELINT_FA_PATTERNS" ;;
        *)  echo "" ;;
    esac
}

# Count total patterns available for a given tier
featurelint_count_tier_patterns() {
    local tier="${1:-free}"
    local categories
    categories="$(featurelint_get_tier_patterns "$tier")"
    local count=0
    for cat in $categories; do
        local array_name
        array_name="$(featurelint_get_pattern_array "$cat")"
        if [[ -n "$array_name" ]]; then
            local -n arr="$array_name"
            count=$(( count + ${#arr[@]} ))
        fi
    done
    echo "$count"
}

# Validate that all patterns have the required trailing fields
# Format: REGEX|SEVERITY|CHECK_ID|DESCRIPTION|RECOMMENDATION
# The regex field may contain pipe characters, so we validate by
# extracting the last 4 fields (severity, check_id, description, rec)
featurelint_validate_patterns() {
    local errors=0
    local all_categories="SF FC FS SM FL FA"
    for cat in $all_categories; do
        local array_name
        array_name="$(featurelint_get_pattern_array "$cat")"
        if [[ -n "$array_name" ]]; then
            local -n arr="$array_name"
            for i in "${!arr[@]}"; do
                local entry="${arr[$i]}"
                local total_fields
                total_fields=$(echo "$entry" | awk -F'|' '{print NF}')
                # Extract severity (4th field from end) and check_id (3rd from end)
                local severity check_id
                severity=$(echo "$entry" | awk -F'|' "{print \$(NF-3)}")
                check_id=$(echo "$entry" | awk -F'|' "{print \$(NF-2)}")

                # Validate severity is a known value
                case "$severity" in
                    error|warning|info) ;;
                    *)
                        echo "ERROR: ${cat}-$(printf '%03d' $((i+1))): invalid severity '${severity}'" >&2
                        errors=$((errors + 1))
                        continue
                        ;;
                esac

                # Validate check_id matches expected pattern
                if ! echo "$check_id" | grep -qE "^${cat}-[0-9]{3}$"; then
                    echo "ERROR: ${cat}-$(printf '%03d' $((i+1))): invalid check_id '${check_id}'" >&2
                    errors=$((errors + 1))
                fi
            done
        fi
    done
    return "$errors"
}
