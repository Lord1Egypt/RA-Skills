#!/usr/bin/env bash
# AuthAudit -- Security Check Patterns
# 90 patterns organized into 6 categories (15 patterns each)
#
# Format: REGEX|SEVERITY|CHECK_ID|DESCRIPTION|RECOMMENDATION
#
# Categories:
#   AC  Authentication Checks       (15 patterns)
#   SM  Session Management           (15 patterns)
#   AZ  Authorization/Access Control (15 patterns)
#   TK  Token Handling               (15 patterns)
#   CS  CSRF Protection              (15 patterns)
#   PW  Password & Credential Mgmt  (15 patterns)
#
# Severities: critical, high, medium, low
# All patterns are POSIX ERE compatible (grep -E)
#
# Tier gating:
#   free       = patterns 1-5 per category   (30 total)
#   pro        = patterns 1-10 per category  (60 total)
#   team/ent   = patterns 1-15 per category  (90 total)

set -euo pipefail

# ═══════════════════════════════════════════════════════════════════════════════
# CATEGORY 1: AC -- Authentication Checks (15 patterns)
# Detects missing authentication middleware, unprotected routes, bypassed
# login checks, missing auth decorators, and unauthenticated endpoints.
# ═══════════════════════════════════════════════════════════════════════════════

AC_PATTERNS=(
  # --- FREE TIER (patterns 1-5) ---

  # AC-001: Express/Fastify route without auth middleware (handler directly receives req)
  'app\.(get|post|put|delete|patch)\([[:space:]]*["/'"'"'][^)]*,[[:space:]]*(async[[:space:]]+)?\(req[[:space:]]*,|critical|AC-001|Route handler without authentication middleware -- request goes directly to handler|Add authentication middleware before the handler: app.get("/path", authMiddleware, handler)'

  # AC-002: Flask route without login_required decorator
  '@app\.route\([^)]*\)[[:space:]]*$|critical|AC-002|Flask route without @login_required or auth decorator on next line|Add @login_required decorator: @login_required before def handler()'

  # AC-003: Django view without permission_classes or login_required
  'class[[:space:]]+[A-Z][a-zA-Z]*View[^:]*:[[:space:]]*$|critical|AC-003|Django view class without permission_classes -- may allow unauthenticated access|Add permission_classes = [IsAuthenticated] to the view class'

  # AC-004: skip_before_action :authenticate or skip_authorization
  'skip_before_action[[:space:]]*:authenticate|critical|AC-004|Authentication explicitly skipped on controller action|Review whether skipping authentication is intentional and restrict to specific actions only'

  # AC-005: FastAPI endpoint without Depends() auth dependency
  '@(app|router)\.(get|post|put|delete|patch)\([^)]*\)[[:space:]]*$|critical|AC-005|FastAPI route without Depends() authentication dependency|Add auth dependency: @app.get("/path", dependencies=[Depends(verify_token)])'

  # --- PRO TIER (patterns 6-10) ---

  # AC-006: AllowAnonymous or allow_unauthenticated on sensitive endpoints
  '(AllowAnonymous|allow_unauthenticated|authentication_classes[[:space:]]*=[[:space:]]*\[\])|high|AC-006|Anonymous access allowed -- verify this endpoint should be public|Remove AllowAnonymous or empty authentication_classes if endpoint handles sensitive data'

  # AC-007: Next.js API route without getServerSession or auth() check
  'export[[:space:]]+(async[[:space:]]+)?function[[:space:]]+(GET|POST|PUT|DELETE|PATCH)[[:space:]]*\(|high|AC-007|Next.js API route handler without apparent auth check|Add getServerSession() or auth() check at the start of the handler'

  # AC-008: Express router without any auth middleware reference
  'router\.(get|post|put|delete|patch)\([[:space:]]*["/'"'"'][^)]*,[[:space:]]*(async[[:space:]]+)?\(req|high|AC-008|Express router route without auth middleware|Add authentication middleware: router.get("/path", authMiddleware, handler)'

  # AC-009: Public file upload endpoint (multer/formidable without auth)
  '(multer|formidable|busboy|multipart)\(|high|AC-009|File upload handler detected -- ensure authentication is applied|Protect file upload endpoints with authentication middleware'

  # AC-010: Go http handler without auth check
  'func[[:space:]]+[a-zA-Z]*Handler\(w[[:space:]]+http\.ResponseWriter|high|AC-010|Go HTTP handler without visible authentication check|Add authentication middleware or check credentials at the start of the handler'

  # --- TEAM/ENTERPRISE TIER (patterns 11-15) ---

  # AC-011: Spring Controller without @PreAuthorize or security annotation
  '@(GetMapping|PostMapping|PutMapping|DeleteMapping|RequestMapping)\(|medium|AC-011|Spring endpoint without @PreAuthorize or security annotation|Add @PreAuthorize("isAuthenticated()") or Spring Security configuration'

  # AC-012: PHP route without auth middleware
  'Route::(get|post|put|delete|patch)\([[:space:]]*["/'"'"']|medium|AC-012|Laravel/PHP route without auth middleware|Add auth middleware: Route::get("/path", [Controller::class, "method"])->middleware("auth")'

  # AC-013: GraphQL resolver without auth context check
  '(resolve|Query|Mutation)[[:space:]]*[:=][[:space:]]*(async[[:space:]]+)?\(|medium|AC-013|GraphQL resolver without visible authentication context check|Verify authentication from context in every resolver: if (!context.user) throw new AuthError()'

  # AC-014: Catch-all wildcard route that may bypass auth
  'app\.(use|all)\([[:space:]]*["/'"'"']\*|low|AC-014|Catch-all wildcard route -- verify auth middleware is applied|Ensure wildcard routes have authentication middleware applied'

  # AC-015: Websocket handler without auth verification
  '(on\([[:space:]]*['"'"'"]connection['"'"'"]|ws\.on|socket\.on\([[:space:]]*['"'"'"]message)|low|AC-015|WebSocket handler without visible authentication check|Verify authentication during WebSocket handshake or on first message'
)

# ═══════════════════════════════════════════════════════════════════════════════
# CATEGORY 2: SM -- Session Management (15 patterns)
# Detects insecure session configuration, missing session expiry, absent
# session rotation, predictable IDs, and session fixation vulnerabilities.
# ═══════════════════════════════════════════════════════════════════════════════

SM_PATTERNS=(
  # --- FREE TIER (patterns 1-5) ---

  # SM-001: Session cookie missing Secure flag
  'cookie.*secure[[:space:]]*:[[:space:]]*false|high|SM-001|Session cookie Secure flag explicitly set to false -- cookies sent over HTTP|Set secure: true to ensure cookies are only sent over HTTPS'

  # SM-002: Session cookie missing HttpOnly flag
  'httpOnly[[:space:]]*:[[:space:]]*false|httponly[[:space:]]*=[[:space:]]*False|high|SM-002|Session cookie HttpOnly flag disabled -- cookie accessible via JavaScript|Set httpOnly: true to prevent client-side script access to session cookie'

  # SM-003: Session without expiry or maxAge
  'session\([[:space:]]*\{[^}]*(secret|name)[^}]*\}[[:space:]]*\)|critical|SM-003|Session configuration without maxAge or expires -- sessions may never expire|Add maxAge or cookie.expires to session configuration'

  # SM-004: No session regeneration on login/privilege change
  '(req\.login|login_user|sign_in|authenticate!)[[:space:]]*\(|high|SM-004|Login without session regeneration -- vulnerable to session fixation|Regenerate session ID after login: req.session.regenerate() or session.cycle()'

  # SM-005: Math.random used for session/token generation
  'Math\.random\(\)|critical|SM-005|Math.random() used -- predictable values unsuitable for session IDs or tokens|Use crypto.randomBytes() or crypto.randomUUID() for secure random generation'

  # --- PRO TIER (patterns 6-10) ---

  # SM-006: Session data stored in localStorage
  'localStorage\.(setItem|getItem)\([[:space:]]*['"'"'"](session|sess_|sid|JSESSIONID|PHPSESSID)|high|SM-006|Session identifier stored in localStorage -- vulnerable to XSS exfiltration|Store session identifiers in HttpOnly cookies instead of localStorage'

  # SM-007: express-session with default MemoryStore (session fixation risk)
  'session\([[:space:]]*\{|critical|SM-007|express-session may use default MemoryStore -- unsuitable for production and leaks memory|Configure a persistent session store: MongoStore, RedisStore, or connect-pg-simple'

  # SM-008: Session maxAge/lifetime set to very long value (> 24h in ms)
  'maxAge[[:space:]]*:[[:space:]]*(8640000[0-9]|[0-9]{9,})|medium|SM-008|Session lifetime exceeds 24 hours -- overly long session increases hijack window|Set maxAge to a reasonable duration (e.g., 3600000 for 1 hour, 86400000 for 24 hours)'

  # SM-009: Missing session invalidation on logout
  'logout['"'"'"]|sign_out|signout|log_out|high|SM-009|Logout handler detected -- ensure session is fully invalidated|Call req.session.destroy(), session.invalidate(), or equivalent on logout'

  # SM-010: Session ID passed in URL parameter
  '(sid|session_id|sessionId|JSESSIONID|PHPSESSID)[[:space:]]*=[[:space:]]*req\.(query|params)|critical|SM-010|Session ID read from URL parameter -- exposed in browser history and server logs|Transmit session IDs only via HttpOnly cookies, never in URL parameters'

  # --- TEAM/ENTERPRISE TIER (patterns 11-15) ---

  # SM-011: SESSION_COOKIE_AGE or session.gc_maxlifetime set very high
  '(SESSION_COOKIE_AGE|gc_maxlifetime)[[:space:]]*=[[:space:]]*[0-9]{6,}|medium|SM-011|Session cookie age or garbage collection lifetime set very high|Set session lifetime to a reasonable value (e.g., 86400 for 24 hours)'

  # SM-012: Session secret too short or hardcoded
  'secret[[:space:]]*:[[:space:]]*['"'"'"][a-zA-Z0-9 ]{1,15}['"'"'"]|high|SM-012|Session secret appears too short (under 16 chars) or hardcoded|Use a strong random secret (32+ chars) from environment variables'

  # SM-013: No idle timeout for sessions
  'rolling[[:space:]]*:[[:space:]]*false|low|SM-013|Session rolling disabled -- idle sessions do not get extended but verify idle timeout exists|Implement idle session timeout to invalidate sessions after period of inactivity'

  # SM-014: SameSite cookie attribute missing or set to None
  'sameSite[[:space:]]*:[[:space:]]*['"'"'"]?(None|none)['"'"'"]?|medium|SM-014|Session cookie SameSite set to None -- vulnerable to cross-site request attacks|Set sameSite to Strict or Lax unless cross-site cookies are required'

  # SM-015: Session cookie domain set overly broad
  'domain[[:space:]]*:[[:space:]]*['"'"'"]\.[a-zA-Z]+\.[a-zA-Z]+['"'"'"]|low|SM-015|Session cookie domain set broadly -- may be accessible by sibling subdomains|Set cookie domain as narrowly as possible to limit scope'
)

# ═══════════════════════════════════════════════════════════════════════════════
# CATEGORY 3: AZ -- Authorization / Access Control (15 patterns)
# Detects missing role checks, IDOR patterns, broken object-level auth,
# missing permission verification, and privilege escalation paths.
# ═══════════════════════════════════════════════════════════════════════════════

AZ_PATTERNS=(
  # --- FREE TIER (patterns 1-5) ---

  # AZ-001: Hardcoded admin/role string comparison
  'role[[:space:]]*===?[[:space:]]*['"'"'"](admin|root|superuser|superadmin)['"'"'"]|critical|AZ-001|Hardcoded admin role check -- brittle and may miss role hierarchy|Use a role hierarchy system or RBAC library instead of string comparison'

  # AZ-002: IDOR -- user-controlled ID used directly in database query
  '(findById|findOne|find_by_id|findByPk|get_object_or_404)\([[:space:]]*(req\.(params|query|body)|request\.(args|data|POST|GET))|critical|AZ-002|User-controlled ID passed directly to database lookup -- IDOR vulnerability|Verify the requesting user owns or has permission to access the referenced object'

  # AZ-003: Missing permission check -- params.id used in DB operations
  '\.(update|delete|destroy|remove)\([[:space:]]*\{[^}]*(id|_id)[[:space:]]*:|critical|AZ-003|Database mutation uses ID without visible ownership check -- potential IDOR|Verify the authenticated user owns the resource before update/delete operations'

  # AZ-004: isAdmin or is_admin flag checked client-side
  '(isAdmin|is_admin|isRoot|is_superuser)[[:space:]]*===?[[:space:]]*(true|false|1|0)|high|AZ-004|Admin flag checked with simple boolean -- ensure this is server-side and from trusted source|Derive admin status from session/token server-side, never from client-supplied data'

  # AZ-005: User role assigned from request body without validation
  '(role|userRole|user_role|permission)[[:space:]]*=[[:space:]]*(req\.body|request\.data|params)\[|high|AZ-005|User role assigned from request body -- privilege escalation risk|Never allow users to set their own role; assign roles server-side through admin flows'

  # --- PRO TIER (patterns 6-10) ---

  # AZ-006: Missing function-level authorization (all users can access admin functions)
  '(\/admin|\/manage|\/dashboard|\/internal)['"'"'"][[:space:]]*,|high|AZ-006|Admin/management endpoint without visible authorization check|Add role-based access control to restrict admin routes to authorized users'

  # AZ-007: Object access without ownership verification
  'getById|get_by_id|find_by_pk|high|AZ-007|Object retrieved by ID without ownership verification in same function|Add ownership check: verify requesting user ID matches resource owner ID'

  # AZ-008: Wildcard or overly permissive permission grant
  '(permissions?|scopes?)[[:space:]]*[:=][[:space:]]*\[[[:space:]]*['"'"'"]\*['"'"'"]|medium|AZ-008|Wildcard permission grant -- overly permissive access|Use specific granular permissions instead of wildcard grants'

  # AZ-009: Authorization check only on frontend (v-if, ng-if, conditional render)
  '(v-if|ng-if|\{[[:space:]]*isAdmin|&&[[:space:]]*isAdmin|role[[:space:]]*===)[[:space:]]|critical|AZ-009|Authorization check appears to be client-side only -- easily bypassed|Always enforce authorization on the server side regardless of client-side checks'

  # AZ-010: Missing ownership check in update/delete handler
  'async[[:space:]]+function[[:space:]]+(update|delete|remove|destroy)|high|AZ-010|Update/delete handler without visible ownership check|Verify the authenticated user owns the resource before allowing modification'

  # --- TEAM/ENTERPRISE TIER (patterns 11-15) ---

  # AZ-011: Role assigned during user creation from untrusted input
  '(new[[:space:]]+User|User\.create|create_user)\([[:space:]]*\{[^}]*role|medium|AZ-011|Role set during user creation -- ensure role value is not from untrusted input|Default new users to lowest privilege role; require admin action for role elevation'

  # AZ-012: Authorization middleware disabled or commented
  '#.*authorize|//.*authorize|/\*.*authorize|critical|AZ-012|Authorization middleware appears commented out or disabled|Re-enable authorization middleware -- do not leave it commented in production code'

  # AZ-013: Mass assignment -- params.permit! or accepting all fields
  '(permit!|attr_accessible[[:space:]]*:all|params\.to_unsafe_h|\.assign\(target,[[:space:]]*req\.body)|medium|AZ-013|Mass assignment -- all request parameters accepted without filtering|Use explicit field allowlists: permit(:name, :email) or pick specific fields'

  # AZ-014: Path traversal in authorized resource access
  '(path\.join|os\.path\.join|File\.join)\([^)]*req\.(params|query|body)|medium|AZ-014|Path construction from user input -- potential path traversal bypass|Sanitize and validate paths; use path.resolve and verify result is within allowed directory'

  # AZ-015: Default-open access policy (allow all, deny specific)
  '(default[[:space:]]*:[[:space:]]*['"'"'"]allow|access[[:space:]]*:[[:space:]]*['"'"'"]public|policy[[:space:]]*:[[:space:]]*['"'"'"]permissive)|low|AZ-015|Default-open access policy detected -- prefer deny-by-default|Use a deny-by-default policy and explicitly grant access to specific routes'
)

# ═══════════════════════════════════════════════════════════════════════════════
# CATEGORY 4: TK -- Token Handling (15 patterns)
# Detects insecure token storage, weak signing, missing expiry, token leakage,
# and improper token validation.
# ═══════════════════════════════════════════════════════════════════════════════

TK_PATTERNS=(
  # --- FREE TIER (patterns 1-5) ---

  # TK-001: JWT stored in localStorage
  'localStorage\.(setItem|getItem)\([[:space:]]*['"'"'"](token|jwt|access_token|auth_token|id_token)|high|TK-001|JWT/token stored in localStorage -- vulnerable to XSS exfiltration|Store tokens in HttpOnly cookies or use in-memory storage with refresh tokens'

  # TK-002: Token passed in URL query parameter
  '(token|jwt|api_key|apiKey|access_token|auth)[[:space:]]*=[[:space:]]*req\.(query|params)\[|critical|TK-002|Token read from URL parameter -- exposed in browser history, logs, and referrer headers|Transmit tokens via Authorization header or HttpOnly cookies'

  # TK-003: JWT with algorithm set to "none"
  'algorithm[[:space:]]*[:=][[:space:]]*['"'"'"]none['"'"'"]|critical|TK-003|JWT algorithm set to none -- signature verification completely disabled|Use a strong signing algorithm: RS256, ES256, or HS256 with a strong secret'

  # TK-004: Weak JWT signing secret (short string)
  '(jwt_secret|JWT_SECRET|secretOrKey|secret_key)[[:space:]]*[:=][[:space:]]*['"'"'"][a-zA-Z0-9]{1,20}['"'"'"]|high|TK-004|JWT signing secret appears weak or hardcoded (under 20 chars)|Use a strong random secret (64+ chars) from environment variables'

  # TK-005: JWT sign without expiresIn/exp option
  'jwt\.sign\([^)]*\{[^}]*\}[[:space:]]*,[[:space:]]*[^,)]+[[:space:]]*\)|high|TK-005|JWT signed without expiresIn option -- token may never expire|Add expiresIn option: jwt.sign(payload, secret, { expiresIn: "1h" })'

  # --- PRO TIER (patterns 6-10) ---

  # TK-006: Token refresh without rotation (reusing same refresh token)
  'refreshToken[[:space:]]*=[[:space:]]*req\.(body|cookies)|medium|TK-006|Refresh token accepted without apparent rotation -- reuse enables theft persistence|Rotate refresh tokens on every use: issue new refresh token and invalidate the old one'

  # TK-007: Token or secret logged to console or file
  'console\.(log|info|debug|warn)\([^)]*([Tt]oken|[Ss]ecret|[Kk]ey|jwt|JWT)|high|TK-007|Token or secret value logged to console -- may appear in log files|Remove token logging; use redaction if logging context is necessary'

  # TK-008: Missing JWT audience (aud) validation
  'jwt\.verify\([^)]*\{[^}]*\}[[:space:]]*\)|medium|TK-008|JWT verification without audience (aud) claim validation|Add audience validation: jwt.verify(token, secret, { audience: "your-app" })'

  # TK-009: Missing JWT issuer (iss) validation
  'verify[[:space:]]*\([^)]*token[^)]*\)|medium|TK-009|Token verification without visible issuer validation|Validate the issuer claim to ensure token was issued by your auth server'

  # TK-010: Hardcoded JWT secret in source code
  '(JWT_SECRET|jwt_secret|TOKEN_SECRET|token_secret)[[:space:]]*=[[:space:]]*['"'"'"][^'"'"'"]{5,}['"'"'"]|critical|TK-010|JWT secret hardcoded in source code|Move JWT secret to environment variables: process.env.JWT_SECRET'

  # --- TEAM/ENTERPRISE TIER (patterns 11-15) ---

  # TK-011: Token sent over plain HTTP
  'http://[^/]*\.(com|org|net|io|dev|app)[^'"'"'"]*[Tt]oken|high|TK-011|Token transmitted over insecure HTTP connection|Always use HTTPS for endpoints that transmit or receive tokens'

  # TK-012: Symmetric signing (HS256) in distributed/microservice context
  'HS256|hs256|high|TK-012|Symmetric JWT signing (HS256) -- secret must be shared with all verifiers|Use asymmetric signing (RS256, ES256) for distributed systems where multiple services verify tokens'

  # TK-013: No token revocation check (no blacklist/blocklist)
  'jwt\.verify\([[:space:]]*token[[:space:]]*,|low|TK-013|JWT verification without apparent revocation check|Implement token revocation: check a blocklist/database before accepting tokens'

  # TK-014: Refresh token stored in localStorage or sessionStorage
  '(localStorage|sessionStorage)\.(setItem|getItem)\([[:space:]]*['"'"'"]refresh|high|TK-014|Refresh token stored in browser storage -- vulnerable to XSS|Store refresh tokens in HttpOnly Secure cookies only'

  # TK-015: Token scope or permission not validated
  'decode[dD]?\([[:space:]]*token|low|TK-015|Token decoded without visible scope or permission validation|Validate token scopes/permissions against the requested action'
)

# ═══════════════════════════════════════════════════════════════════════════════
# CATEGORY 5: CS -- CSRF Protection (15 patterns)
# Detects missing CSRF tokens, absent SameSite flag, GET requests with side
# effects, missing Origin/Referer validation, and CORS misconfigurations.
# ═══════════════════════════════════════════════════════════════════════════════

CS_PATTERNS=(
  # --- FREE TIER (patterns 1-5) ---

  # CS-001: CSRF protection explicitly disabled
  '(csrf_exempt|@csrf_exempt|WTF_CSRF_ENABLED[[:space:]]*=[[:space:]]*False|CSRF_ENABLED[[:space:]]*=[[:space:]]*False)|critical|CS-001|CSRF protection explicitly disabled -- state-changing requests unprotected|Re-enable CSRF protection or use token-based auth (JWT) for API endpoints'

  # CS-002: Rails CSRF protection skipped
  '(protect_from_forgery[[:space:]]*except|skip_before_action[[:space:]]*:verify_authenticity_token)|high|CS-002|Rails CSRF verification skipped -- forms vulnerable to cross-site forgery|Do not skip CSRF verification on state-changing actions unless using API token auth'

  # CS-003: State-changing operation in GET handler
  'app\.get\([^)]*\{[^}]*(save|create|update|delete|destroy|insert|remove|drop)|high|CS-003|GET endpoint performs state-changing operation -- vulnerable to CSRF via links/images|Use POST/PUT/DELETE for state-changing operations; GET should be read-only'

  # CS-004: Cookie SameSite attribute set to None
  '([Ss]ame[Ss]ite[[:space:]]*[:=][[:space:]]*['"'"'"]?[Nn]one)|medium|CS-004|Cookie SameSite set to None -- cookies sent on cross-site requests|Set SameSite to Strict or Lax to prevent cross-site cookie transmission'

  # CS-005: Missing Origin or Referer header validation
  'Access-Control-Allow-Origin[[:space:]]*:[[:space:]]*\*|high|CS-005|CORS allows all origins -- combined with credentials enables CSRF|Restrict Access-Control-Allow-Origin to specific trusted domains'

  # --- PRO TIER (patterns 6-10) ---

  # CS-006: CORS with credentials and wildcard origin
  'credentials[[:space:]]*:[[:space:]]*true|critical|CS-006|CORS credentials enabled -- verify origin is not wildcard or overly permissive|Ensure Access-Control-Allow-Origin is set to specific domains when credentials are true'

  # CS-007: GET handler with database write operation
  '\.(get|GET)\([^)]*\)[^{]*\{[[:space:]]*(.*\.)?(save|insert|update|delete|destroy)\(|high|CS-007|GET endpoint appears to perform database writes|Move write operations to POST/PUT/DELETE handlers'

  # CS-008: No CSRF middleware in Express/Django/Rails app
  'app\.use\([[:space:]]*cors\(|high|CS-008|CORS middleware enabled -- verify CSRF protection is also configured|Add CSRF middleware alongside CORS: csurf, django.middleware.csrf, or protect_from_forgery'

  # CS-009: CSRF token transmitted in URL parameter
  '(csrf|_csrf|csrftoken|csrf_token)[[:space:]]*=[[:space:]]*req\.(query|params)|medium|CS-009|CSRF token in URL parameter -- leaked in browser history and server logs|Transmit CSRF tokens via request headers or hidden form fields only'

  # CS-010: Missing X-Requested-With header check for AJAX
  'XMLHttpRequest|x-requested-with|medium|CS-010|Custom header check detected -- verify it is required for all state-changing requests|Require X-Requested-With or custom header on state-changing AJAX requests'

  # --- TEAM/ENTERPRISE TIER (patterns 11-15) ---

  # CS-011: SameSite=None without Secure flag
  'sameSite[[:space:]]*:[[:space:]]*['"'"'"]?[Nn]one['"'"'"]?[^}]*secure[[:space:]]*:[[:space:]]*false|high|CS-011|SameSite=None without Secure flag -- cookie rejected by modern browsers|When SameSite=None, the Secure flag must also be set to true'

  # CS-012: Form action pointing to external domain
  'action[[:space:]]*=[[:space:]]*['"'"'"]https?://|medium|CS-012|Form action points to external URL -- potential data exfiltration or phishing|Verify form action URL is your own domain; use relative paths for internal forms'

  # CS-013: AJAX requests without anti-CSRF header
  'fetch\([[:space:]]*['"'"'"]|axios\.(post|put|delete|patch)\(|low|CS-013|AJAX request without visible CSRF token or custom header|Include CSRF token in request headers: X-CSRF-Token or X-XSRF-TOKEN'

  # CS-014: Django CORS_ALLOW_ALL_ORIGINS or CORS_ORIGIN_ALLOW_ALL
  '(CORS_ALLOW_ALL_ORIGINS|CORS_ORIGIN_ALLOW_ALL)[[:space:]]*=[[:space:]]*True|high|CS-014|Django CORS allows all origins -- effectively disables same-origin protections|Set CORS_ALLOWED_ORIGINS to a list of specific trusted domains'

  # CS-015: Access-Control-Allow-Methods with wildcard
  'Access-Control-Allow-Methods[[:space:]]*:[[:space:]]*\*|low|CS-015|CORS allows all HTTP methods -- overly permissive preflight response|Restrict Access-Control-Allow-Methods to only required methods: GET, POST'
)

# ═══════════════════════════════════════════════════════════════════════════════
# CATEGORY 6: PW -- Password & Credential Management (15 patterns)
# Detects weak password requirements, plaintext comparison, missing hashing,
# absent rate limiting on login, and credentials in query strings.
# ═══════════════════════════════════════════════════════════════════════════════

PW_PATTERNS=(
  # --- FREE TIER (patterns 1-5) ---

  # PW-001: Password compared with equality operator instead of timing-safe compare
  'password[[:space:]]*===?[[:space:]]*(req\.|request\.|params|args|body|data)|critical|PW-001|Password compared with equality operator -- vulnerable to timing attacks|Use bcrypt.compare(), crypto.timingSafeEqual(), or equivalent timing-safe comparison'

  # PW-002: Plaintext password stored or assigned directly
  '(password|passwd|pwd)[[:space:]]*=[[:space:]]*(req\.|request\.)(body|data|POST|form)|critical|PW-002|Password value assigned from request without hashing|Hash passwords before storage: await bcrypt.hash(password, 12) or Argon2'

  # PW-003: Missing bcrypt/argon2/scrypt -- using MD5 or SHA for passwords
  '(md5|MD5|sha1|SHA1|sha256|SHA256)\([[:space:]]*(password|passwd|pwd)|high|PW-003|Weak hash (MD5/SHA) used for password -- easily cracked with rainbow tables|Use bcrypt, argon2, or scrypt for password hashing'

  # PW-004: Password in URL query string
  '(password|passwd|pwd|secret)[[:space:]]*=[[:space:]]*req\.(query|params\.get|GET)|critical|PW-004|Password read from URL query parameter -- exposed in logs and browser history|Accept passwords only via POST request body, never in URL parameters'

  # PW-005: Hardcoded password or credential in source code
  '(password|passwd|secret|credential)[[:space:]]*[:=][[:space:]]*['"'"'"][a-zA-Z0-9!@#$%^&*]{4,}['"'"'"]|critical|PW-005|Hardcoded password or credential in source code|Move credentials to environment variables or a secrets manager'

  # --- PRO TIER (patterns 6-10) ---

  # PW-006: Weak minimum password length (less than 8 characters)
  '(minlength|min_length|minimumLength|minimum_length)[[:space:]]*[:=][[:space:]]*[1-7][^0-9]|high|PW-006|Minimum password length is less than 8 characters|Enforce minimum password length of at least 8 characters (12+ recommended)'

  # PW-007: Login/signin endpoint without rate limiting
  '(\/login|\/signin|\/sign-in|\/authenticate)['"'"'"]|high|PW-007|Login endpoint detected -- ensure rate limiting is applied|Add rate limiting to login endpoint: express-rate-limit, django-ratelimit, or rack-attack'

  # PW-008: Password logged to console or file
  'console\.(log|info|debug|warn|error)\([^)]*([Pp]assword|[Pp]asswd|[Cc]redential)|critical|PW-008|Password or credential value logged to console -- appears in log files|Never log passwords or credentials; remove logging statement immediately'

  # PW-009: Credentials in .env file checked into source
  '(PASSWORD|SECRET|CREDENTIAL|API_KEY|PRIVATE_KEY)[[:space:]]*=[[:space:]]*[a-zA-Z0-9+/=]{8,}|high|PW-009|Credential value in environment/config file -- ensure this file is not committed|Add .env files to .gitignore and use a secrets manager in production'

  # PW-010: Missing password complexity validation
  '(password|passwd).*\.length[[:space:]]*(>=?|<)[[:space:]]*[0-9]|medium|PW-010|Password validation checks only length -- missing complexity requirements|Add complexity rules: uppercase, lowercase, number, special character requirements'

  # --- TEAM/ENTERPRISE TIER (patterns 11-15) ---

  # PW-011: Password reset token without expiry
  '(reset_token|resetToken|password_reset)[[:space:]]*=[[:space:]]*(crypto|uuid|Math|random)|high|PW-011|Password reset token generated without visible expiry mechanism|Set reset token expiry to 15-60 minutes; store expiry timestamp with the token'

  # PW-012: Password reset link without time-based expiration
  '(resetUrl|reset_url|reset_link)[[:space:]]*=|medium|PW-012|Password reset URL constructed -- ensure token has time-based expiration|Include expiry timestamp in reset token and validate it on the reset page'

  # PW-013: Credential in source code comment
  '(\/\/|#|\/\*)[[:space:]]*password[[:space:]]*[:=][[:space:]]*[a-zA-Z0-9]|medium|PW-013|Credential appears in source code comment|Remove credentials from comments; never leave passwords in code comments'

  # PW-014: createHash with MD5 or SHA1 for password
  'createHash\([[:space:]]*['"'"'"](md5|sha1)['"'"'"]\)|high|PW-014|Node.js createHash with MD5 or SHA1 -- unsuitable for password hashing|Use bcrypt or argon2 for password hashing: await bcrypt.hash(password, 12)'

  # PW-015: Password returned in API response
  '(res\.(json|send)|JsonResponse|Response)\([^)]*password|low|PW-015|Password field may be included in API response|Exclude password from API responses: use .select("-password") or serializer exclude'
)

# ═══════════════════════════════════════════════════════════════════════════════
# Pattern Registry
# Maps category codes to their pattern arrays for iteration
# ═══════════════════════════════════════════════════════════════════════════════

AUTHAUDIT_CATEGORIES=("AC" "SM" "AZ" "TK" "CS" "PW")

AUTHAUDIT_CATEGORY_NAMES=(
  "Authentication Checks"
  "Session Management"
  "Authorization / Access Control"
  "Token Handling"
  "CSRF Protection"
  "Password & Credential Management"
)

# Map category code to pattern array name
get_pattern_array_name() {
  local category="$1"
  echo "${category}_PATTERNS"
}

# Get all pattern entries for a category, optionally limited by tier
# Usage: get_category_patterns "AC" [limit]
get_category_patterns() {
  local category="$1"
  local limit="${2:-15}"
  local arr_name="${category}_PATTERNS"

  # Get array by nameref
  local -n patterns_ref="$arr_name" 2>/dev/null || return 1

  local count=0
  local entry
  for entry in "${patterns_ref[@]}"; do
    if [[ $count -ge $limit ]]; then
      break
    fi
    echo "$entry"
    count=$((count + 1))
  done
}

# Get total pattern count across all categories for a given limit
get_total_pattern_count() {
  local limit="${1:-15}"
  local total=0
  local cat
  for cat in "${AUTHAUDIT_CATEGORIES[@]}"; do
    local arr_name="${cat}_PATTERNS"
    local -n ref="$arr_name" 2>/dev/null || continue
    local arr_len=${#ref[@]}
    if [[ $arr_len -lt $limit ]]; then
      total=$((total + arr_len))
    else
      total=$((total + limit))
    fi
  done
  echo "$total"
}
