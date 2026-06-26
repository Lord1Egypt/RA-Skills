# Audit Scope

Use this reference to understand what the static auditor can and cannot infer today.

## Supported analysis goals

The auditor is designed to answer questions like:
- Which frontend API calls do not map to any backend endpoint?
- Which calls use the wrong HTTP method?
- Which routes appear to differ only by prefix, pluralization, or dynamic path handling?
- Which frontend query/body/auth expectations appear inconsistent with backend contracts?
- Which backend routes look unused by the currently scanned frontend surfaces?

## Frontend extraction scope

Current best coverage:
- Axios method calls such as `axios.get(...)`, `client.post(...)`
- Axios `.request(...)` and object-config calls
- `fetch(...)`
- some Dart/Dio direct client calls and wrapper methods
- selected baseURL/default authorization header patterns

Current weak areas:
- heavily dynamic URL assembly
- request construction hidden behind multiple indirection layers
- generated SDKs without recognizable call patterns
- response field usage inferred through complex intermediate transforms

## Backend extraction scope

Current best coverage:
- Spring `@GetMapping/@PostMapping/...`
- selected `@RequestMapping(method=...)`
- Java/Kotlin DTO field extraction
- basic `@RequestBody`, `@RequestParam`, `@RequestPart` hints
- selected Spring Security matcher hints
- Express `app.get/post/...`, `router.get/post/...`
- Express `router.route('/x').get(...).post(...)`
- same-file `app.use('/prefix', router)` prefix mounting
- basic `req.params/query/body` and header/auth/multipart hints in Express handlers
- Laravel `Route::get/post/put/patch/delete`
- Laravel `Route::match`, `Route::any`
- Laravel `Route::resource`, `Route::apiResource`
- Laravel `Route::prefix(...)->group(...)` prefix inference
- basic controller-method request/query/body/auth/multipart hints in Laravel

Current weak areas:
- complex meta-annotations
- custom routing abstractions
- response DTO inference beyond straightforward signatures
- advanced validation rule semantics
- Express router mounting spread across many files or dynamic imports
- Laravel nested group composition and heavily dynamic route registration
- non-Spring/non-Express/non-Laravel backends

## How to interpret findings

- **high confidence**: direct literal route/method extraction, obvious endpoint absence, strong path match
- **medium confidence**: dynamic path normalization, partial body/query inference, route-prefix suspicion
- **low confidence**: auth-only hints, dynamic wrappers, backend-only endpoints that may be called indirectly

Treat findings as engineering review inputs.
Fixing a report item should usually involve checking the cited frontend call site and backend mapping together.

## Useful CLI controls

- `--exclude a,b,c`: ignore noisy path parts such as generated/build directories
- `--format json|md|both`: choose output mode
- `--summary-only`: print concise console summary while still writing report files
- `--fail-on high|medium|low`: return non-zero when findings meet a severity threshold

## Best use cases

- pre-release API drift review
- frontend/backend refactor regression checks
- multi-surface audits across web/admin/mobile
- code review support when runtime verification is expensive
