#!/usr/bin/env bash
# APIShield -- Security Check Patterns
# Each pattern: REGEX | SEVERITY | CHECK_ID | DESCRIPTION | RECOMMENDATION
#
# Severities: critical, high, medium, low
# Patterns are grep -E compatible (extended regex)

set -euo pipefail

# ─── Express.js Auth Patterns ────────────────────────────────────────────────
# Detect Express routes without authentication middleware

EXPRESS_AUTH_PATTERNS=(
  'app\.(get|post|put|delete|patch)\s*\(\s*["\x27/].*,\s*\(req|app\.(get|post|put|delete|patch)\s*\(\s*["\x27/].*,\s*async\s*\(req|critical|EXPRESS_NO_AUTH|Express route without auth middleware — handler directly receives req without auth check|Add authentication middleware: app.get("/path", authMiddleware, handler)'
  'router\.(get|post|put|delete|patch)\s*\(\s*["\x27/].*,\s*\(req|router\.(get|post|put|delete|patch)\s*\(\s*["\x27/].*,\s*async\s*\(req|critical|EXPRESS_ROUTER_NO_AUTH|Express router route without auth middleware|Add authentication middleware: router.get("/path", authMiddleware, handler)'
  'app\.all\s*\(|high|EXPRESS_WILDCARD_METHOD|app.all() exposes all HTTP methods on endpoint — overly permissive|Use specific HTTP methods: app.get(), app.post() instead of app.all()'
)

EXPRESS_RATELIMIT_PATTERNS=(
  'app\.(get|post|put|delete|patch)\s*\(|high|EXPRESS_NO_RATELIMIT|Express route without rate limiting middleware|Add rate limiting: app.use("/api", rateLimit({ windowMs: 15*60*1000, max: 100 }))'
)

EXPRESS_VALIDATION_PATTERNS=(
  'req\.body\b|high|EXPRESS_NO_VALIDATION|Direct use of req.body without input validation|Validate input with Joi, Zod, or express-validator before using req.body'
  'req\.params\b|medium|EXPRESS_PARAMS_NO_VALIDATION|Direct use of req.params without validation|Validate route params with a validation middleware'
  'req\.query\b|medium|EXPRESS_QUERY_NO_VALIDATION|Direct use of req.query without validation|Validate query parameters before use'
)

# ─── FastAPI Auth Patterns ───────────────────────────────────────────────────

FASTAPI_AUTH_PATTERNS=(
  '@app\.(get|post|put|delete|patch)\s*\(|critical|FASTAPI_NO_AUTH|FastAPI route without Depends() auth dependency|Add auth dependency: @app.get("/path", dependencies=[Depends(verify_token)])'
  '@router\.(get|post|put|delete|patch)\s*\(|critical|FASTAPI_ROUTER_NO_AUTH|FastAPI router route without auth dependency|Add Depends() auth to router endpoint'
)

FASTAPI_VALIDATION_PATTERNS=(
  'request\.json\(\)|high|FASTAPI_RAW_JSON|Using raw request.json() instead of Pydantic model validation|Use a Pydantic model as a parameter for automatic validation'
  'dict\s*\)|medium|FASTAPI_DICT_PARAM|Using plain dict instead of typed Pydantic model|Define a Pydantic model for structured request validation'
)

# ─── Flask Auth Patterns ─────────────────────────────────────────────────────

FLASK_AUTH_PATTERNS=(
  '@app\.route\s*\(|critical|FLASK_NO_AUTH|Flask route without @login_required or auth decorator|Add @login_required or custom auth decorator before route handler'
  '@.*\.route\s*\(|critical|FLASK_BP_NO_AUTH|Flask blueprint route without auth decorator|Add authentication decorator to blueprint route'
)

FLASK_VALIDATION_PATTERNS=(
  'request\.form\b|high|FLASK_NO_FORM_VALIDATION|Direct use of request.form without validation|Use WTForms or marshmallow to validate form data'
  'request\.get_json\(\)|high|FLASK_NO_JSON_VALIDATION|Direct use of request.get_json() without validation|Validate JSON data with marshmallow or a schema validator'
  'request\.args\b|medium|FLASK_NO_ARGS_VALIDATION|Direct use of request.args without validation|Validate query arguments before use'
)

# ─── Django Auth Patterns ────────────────────────────────────────────────────

DJANGO_AUTH_PATTERNS=(
  'def\s+(get|post|put|delete|patch)\s*\(self|critical|DJANGO_VIEW_NO_AUTH|Django view method without permission_classes or @login_required|Add @login_required decorator or permission_classes to view'
  'path\s*\(\s*["\x27]|critical|DJANGO_URL_NO_AUTH|Django URL pattern — verify corresponding view has authentication|Ensure the view referenced in this URL pattern has @login_required or permission_classes'
)

DJANGO_VALIDATION_PATTERNS=(
  'request\.data\b|high|DJANGO_NO_SERIALIZER|Direct use of request.data without serializer validation|Use a DRF serializer to validate input data'
  'request\.POST\b|high|DJANGO_NO_FORM_VALIDATION|Direct use of request.POST without form validation|Use Django Forms or serializers to validate POST data'
)

# ─── Rails Auth Patterns ─────────────────────────────────────────────────────

RAILS_AUTH_PATTERNS=(
  'def\s+(index|show|create|update|destroy)\b|critical|RAILS_NO_AUTH|Rails controller action without before_action :authenticate|Add before_action :authenticate_user! or equivalent auth filter'
  'skip_before_action\s*:authenticate|critical|RAILS_SKIP_AUTH|Authentication explicitly skipped on controller action|Review whether skipping authentication is intentional and safe'
)

RAILS_VALIDATION_PATTERNS=(
  'params\[|high|RAILS_NO_STRONG_PARAMS|Direct params[] access without strong parameters|Use params.require(:model).permit(:field1, :field2) for safe mass assignment'
  'params\.permit!|critical|RAILS_PERMIT_ALL|params.permit! allows all parameters — mass assignment vulnerability|Use explicit params.require(:model).permit(:allowed_fields) instead'
)

# ─── Next.js Auth Patterns ───────────────────────────────────────────────────

NEXTJS_AUTH_PATTERNS=(
  'export\s+(async\s+)?function\s+(GET|POST|PUT|DELETE|PATCH)\b|critical|NEXTJS_NO_AUTH|Next.js API route handler without auth check|Add getServerSession() or auth() check at the start of the handler'
  'NextResponse\.(json|redirect)|high|NEXTJS_RESPONSE_NO_AUTH|Next.js response without prior auth validation|Verify authentication before returning NextResponse'
)

NEXTJS_VALIDATION_PATTERNS=(
  'request\.json\(\)|high|NEXTJS_NO_VALIDATION|Next.js route using request.json() without schema validation|Validate request body with Zod or similar before processing'
  'searchParams\.get\(|medium|NEXTJS_NO_QUERY_VALIDATION|Direct use of searchParams without validation|Validate query parameters with Zod or manual checks'
)

# ─── Cross-Framework: CORS Patterns ──────────────────────────────────────────

CORS_PATTERNS=(
  "Access-Control-Allow-Origin.*\*|high|CORS_WILDCARD|CORS allows all origins (Access-Control-Allow-Origin: *)|Restrict CORS to specific trusted origins"
  "cors\(\s*\)|high|CORS_DEFAULT_OPEN|CORS enabled with default (open) configuration|Configure CORS with explicit origin whitelist: cors({ origin: ['https://app.example.com'] })"
  "origin:\s*['\"]?\*['\"]?|high|CORS_ORIGIN_STAR|CORS origin set to wildcard|Set specific origins: origin: ['https://yourdomain.com']"
  'allow_all_origins\s*=\s*True|high|CORS_DJANGO_ALL|Django CORS allows all origins|Set CORS_ALLOWED_ORIGINS to specific domains in settings.py'
  "Access-Control-Allow-Credentials.*true|medium|CORS_CREDENTIALS_WILDCARD|CORS credentials allowed — verify origin is not wildcard|Ensure Access-Control-Allow-Origin is not * when credentials are allowed"
  "Access-Control-Allow-Methods.*\*|medium|CORS_METHODS_WILDCARD|CORS allows all HTTP methods|Restrict to required methods: GET, POST, etc."
)

# ─── Cross-Framework: Debug/Admin Endpoints ──────────────────────────────────

DEBUG_PATTERNS=(
  '["\x27]/debug["\x27/]|critical|DEBUG_ENDPOINT|Debug endpoint exposed — likely leaks internal state|Remove debug endpoints or protect with authentication'
  '["\x27]/test["\x27/]|high|TEST_ENDPOINT|Test endpoint exposed in non-test code|Remove test endpoints from production code'
  '["\x27]/admin["\x27/]|critical|ADMIN_ENDPOINT|Admin endpoint — ensure strong authentication is applied|Protect admin endpoints with admin-level auth and IP restrictions'
  '["\x27]/internal["\x27/]|high|INTERNAL_ENDPOINT|Internal endpoint — should not be publicly accessible|Restrict access to internal network or add authentication'
  '["\x27]/health-full["\x27/]|medium|HEALTH_VERBOSE|Verbose health endpoint may expose system details|Use minimal /health endpoint; move detailed checks behind auth'
  'console\.log\(.*password|critical|LOG_PASSWORD|Password value written to console/log|Never log passwords or secrets — remove immediately'
  'console\.log\(.*secret|critical|LOG_SECRET|Secret value written to console/log|Never log secrets — remove immediately'
  'console\.log\(.*token|high|LOG_TOKEN|Token value written to console/log|Avoid logging tokens — use redaction if logging is necessary'
)

# ─── Cross-Framework: SQL Injection Patterns ─────────────────────────────────

INJECTION_PATTERNS=(
  '\$\{.*\}.*[Qq]uery|critical|SQL_INJECTION_TEMPLATE|Template literal string interpolation in SQL query|Use parameterized queries: db.query("SELECT * FROM users WHERE id = ?", [id])'
  "f['\"].*SELECT.*FROM|critical|SQL_INJECTION_FSTRING|Python f-string in SQL query — SQL injection risk|Use parameterized queries: cursor.execute(\"SELECT * FROM users WHERE id = %s\", (id,))"
  '\.format\(.*[Qq]uery|critical|SQL_INJECTION_FORMAT|String .format() in SQL query — SQL injection risk|Use parameterized queries instead of string formatting'
  'query\s*\(\s*["\x27].*\+\s*|critical|SQL_INJECTION_CONCAT|String concatenation in SQL query|Use parameterized queries instead of string concatenation'
  'execute\s*\(\s*f["\x27]|critical|SQL_INJECTION_EXECUTE|f-string used directly in execute() — SQL injection risk|Use parameterized queries: cursor.execute("... WHERE id = %s", (id,))'
  'raw\s*\(\s*f["\x27]|critical|SQL_INJECTION_RAW|Raw SQL with f-string interpolation|Use parameterized queries instead of raw SQL with interpolation'
  'exec\s*\(|high|CODE_EXEC|Dynamic code execution (exec) — potential code injection|Avoid exec() — use safe alternatives or sandboxed execution'
  'eval\s*\(|high|CODE_EVAL|Dynamic code evaluation (eval) — potential code injection|Avoid eval() — parse data with JSON.parse() or safe parsers'
)

# ─── Cross-Framework: Sensitive Data Exposure ────────────────────────────────

SENSITIVE_DATA_PATTERNS=(
  'password\s*[=:]|high|SENSITIVE_PASSWORD|Password field in API response or assignment|Never return password fields in API responses; use select/exclude'
  'secret\s*[=:]|high|SENSITIVE_SECRET|Secret value in API response or assignment|Never expose secret values in responses'
  'apiKey\s*[=:]|high|SENSITIVE_APIKEY|API key in response or hardcoded|Never expose API keys in responses; use environment variables'
  'api_key\s*[=:]|high|SENSITIVE_API_KEY|API key in response or hardcoded|Never expose API keys in responses; use environment variables'
  'creditCard|credit_card|cardNumber|card_number|high|SENSITIVE_CREDIT_CARD|Credit card data in API response|Never return credit card data; use tokenized references'
  'ssn|socialSecurity|social_security|critical|SENSITIVE_SSN|Social security number in API response|Never expose SSN in API responses'
  'token\s*[=:]\s*["\x27]|medium|SENSITIVE_TOKEN_HARDCODED|Token value appears to be hardcoded|Use environment variables for tokens; never hardcode'
  'Bearer\s+[A-Za-z0-9_-]+\.|high|SENSITIVE_BEARER_HARDCODED|Hardcoded Bearer token|Use environment variables for Bearer tokens'
)

# ─── Cross-Framework: CSRF Patterns ─────────────────────────────────────────

CSRF_PATTERNS=(
  'csrf_exempt|high|CSRF_EXEMPT|CSRF protection explicitly disabled|Remove @csrf_exempt unless endpoint is an API with token auth'
  'protect_from_forgery.*except|high|CSRF_RAILS_SKIP|Rails CSRF protection skipped|Do not skip CSRF protection on state-changing actions'
  'WTF_CSRF_ENABLED\s*=\s*False|high|CSRF_FLASK_DISABLED|Flask-WTF CSRF protection disabled|Enable CSRF protection: WTF_CSRF_ENABLED = True'
)

# ─── Cross-Framework: Error Handling / Info Leak ─────────────────────────────

ERROR_LEAK_PATTERNS=(
  'res\.(send|json)\s*\(\s*err|high|ERROR_LEAK_EXPRESS|Express error object sent directly to client — may leak stack trace|Send sanitized error: res.status(500).json({ error: "Internal server error" })'
  'return\s+str\(e\)|high|ERROR_LEAK_PYTHON|Python exception converted to string and returned — may leak stack trace|Return a generic error message; log the full exception server-side'
  'traceback\.print_exc|medium|ERROR_LEAK_TRACEBACK|Traceback printed — may be visible in response if stdout is captured|Log tracebacks server-side only; never expose to clients'
  'raise\s+.*from\s+None|medium|ERROR_SUPPRESSED|Exception chain suppressed — may hide root cause|Preserve exception chain for debugging; handle errors explicitly'
  'stack.*trace|medium|ERROR_STACK_EXPOSE|Stack trace may be exposed in response|Never send stack traces to clients; log them server-side'
  'e\.message|medium|ERROR_MESSAGE_EXPOSE|Raw error message sent to client|Send generic error messages to clients; log details server-side'
  'DEBUG\s*=\s*True|high|DEBUG_MODE_ON|Debug mode enabled — exposes detailed error pages|Set DEBUG = False in production'
  'NODE_ENV.*development|medium|NODE_ENV_DEV|NODE_ENV set to development — may enable verbose errors|Ensure NODE_ENV=production in deployed environments'
)

# ─── Generic Security Patterns ───────────────────────────────────────────────

GENERIC_SECURITY_PATTERNS=(
  'http://|medium|INSECURE_HTTP|Insecure HTTP URL — should use HTTPS|Use HTTPS for all external requests and API endpoints'
  'verify\s*=\s*False|critical|SSL_VERIFY_DISABLED|SSL certificate verification disabled|Enable SSL verification: verify=True or remove verify=False'
  'rejectUnauthorized\s*:\s*false|critical|SSL_REJECT_DISABLED|Node.js SSL certificate verification disabled|Remove rejectUnauthorized: false; fix certificate issues instead'
  'SECURITY_KEY.*=.*["\x27].{1,20}["\x27]|high|WEAK_SECRET_KEY|Security/secret key appears to be short or hardcoded|Use a strong random key from environment variables (min 32 chars)'
  'allowDiskUse\s*:\s*true|medium|MONGO_DISK_USE|MongoDB allowDiskUse enabled — potential DoS vector|Restrict allowDiskUse to admin-only operations'
  'helmet|low|HELMET_MISSING|Consider using helmet for HTTP security headers|Add helmet middleware: app.use(helmet()) for secure headers'
)
