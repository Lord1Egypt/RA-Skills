# Security Review Checklist

## Injection Vulnerabilities

### SQL Injection
- Are parameterized queries or an ORM used instead of string concatenation?
- Are dynamic table/column names validated against a whitelist?
- Are stored procedure calls secure?

### Command Injection
- Are `os.system` / `subprocess` / `exec` / `eval` called?
- Is user input concatenated into command-line arguments?
- Is `shell=True` used without filtering user input?

### LDAP / XPath / NoSQL Injection
- Are query parameters escaped or are secure APIs used?

## Cross-Site Scripting (XSS)

- Is user input output to HTML with context-aware escaping?
- Is `innerHTML` / `document.write` used to render user content?
- Is a CSP header configured?
- Is HTML sanitization performed for Markdown / rich text rendering?

## Path Traversal

- Are file paths concatenated with user input?
- Is `path.resolve` / `realpath` used for normalization followed by a prefix check?
- Is Zip Slip protection in place for archive extraction?

## Authentication and Authorization

- Do sensitive endpoints have authentication middleware?
- Are there risks of privilege escalation (horizontal / vertical access control issues)?
- Is JWT validation complete (signature, expiration, algorithm confusion)?
- Are passwords stored using secure hashing (bcrypt / argon2)?
- Is multi-factor authentication in place?

## Session Management

- Is the session token generated securely and randomly?
- Are cookies set with HttpOnly / Secure / SameSite attributes?
- Is the session invalidated on the server side upon logout?

## Keys and Sensitive Information

- Are API keys / tokens / passwords hardcoded?
- Are keys in configuration files encrypted or stored in environment variables?
- Is sensitive information (tokens, passwords, ID numbers) printed in logs?
- Are .env / key files listed in .gitignore?

## Insecure Deserialization

- Is data from untrusted sources deserialized (pickle, `yaml.unsafe_load`)?
- Is JSON Schema used to validate the deserialized structure?

## Log Security

- Do logs record the full request/response body including sensitive fields?
- Are user passwords or tokens logged?
- Is the log level appropriate (avoid DEBUG in production)?

## Encryption and Transport Security

- Are weak algorithms used (MD5, SHA1, DES, RC4)?
- Are the TLS version and cipher suites secure?
- Is certificate verification skipped (`verify=False`)?

## SSRF

- Is a user-controlled URL directly requested by the server?
- Is DNS rebinding protection in place?
- Is access to internal network addresses restricted?

## Dependencies and Supply Chain

- Are dependency versions with known CVEs used?
- Is the integrity of third-party packages verified (lockfile, checksum)?

## Business Logic

- Are there race conditions (concurrent ordering, repeated coupon usage)?
- Is there a second confirmation step for sensitive operations (transfers, deletions)?
- Are there timing attack risks (login enumeration, reset tokens)?