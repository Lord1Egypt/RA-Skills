# Cognito Security Best Practices

A security checklist and patterns for hardening your Cognito setup.

## Table of Contents
1. [Pre-Launch Checklist](#pre-launch-checklist)
2. [User Pool Security](#user-pool-security)
3. [Identity Pool Security](#identity-pool-security)
4. [Token Security](#token-security)
5. [Network & Infrastructure](#network-and-infrastructure)
6. [Monitoring & Incident Response](#monitoring-and-incident-response)

---

## Pre-Launch Checklist

Run through this before going to production:

- [ ] MFA enabled (at minimum OPTIONAL, ideally REQUIRED for admin users)
- [ ] Password policy: 8+ chars, mixed case, digits required
- [ ] `preventUserExistenceErrors` enabled on all app clients
- [ ] Client secrets set on all confidential (server-side) clients
- [ ] No client secrets on public (SPA/mobile) clients
- [ ] Token validity periods reviewed (default 1hr ID/access, 30d refresh)
- [ ] Callback and logout URLs are HTTPS (no HTTP except localhost for dev)
- [ ] Unused auth flows disabled on each app client
- [ ] User pool has `RemovalPolicy.RETAIN` and deletion protection enabled
- [ ] Identity pool (if used) has minimal IAM permissions
- [ ] Guest access disabled unless explicitly needed
- [ ] WAF web ACL associated with user pool
- [ ] SES configured for email (not default Cognito email)
- [ ] CloudTrail logging enabled for Cognito API calls
- [ ] Lambda triggers have 5-second timeout and proper error handling

---

## User Pool Security

### Prevent User Enumeration

Enable `preventUserExistenceErrors` on every app client. Without this, Cognito returns different error messages for "user not found" vs "wrong password," letting attackers enumerate valid accounts.

### Block Disposable Emails

Use a Pre Sign-Up Lambda trigger to reject sign-ups from disposable email domains. Maintain a blocklist or use a third-party API.

### SMS Pumping Prevention

If SMS verification or MFA is enabled:
- Set up AWS WAF rate limiting on the user pool
- Monitor SNS spending with billing alerts
- Consider requiring email verification first, then phone as a second step
- Use TOTP MFA instead of SMS when possible (more secure and cheaper)

### Attribute Immutability

- Mark sensitive attributes as immutable (e.g., `tenantId`, `role` if set by admins)
- Use Pre Token Generation trigger to inject computed claims rather than trusting user-editable attributes
- Remember: users can modify their own mutable attributes via the `UpdateUserAttributes` API

### Account Takeover Protection (Plus Plan)

Enable adaptive authentication to automatically detect:
- Compromised credentials (checks against known breach databases)
- Unusual sign-in activity (new device, new location, impossible travel)
- Automated sign-in attempts

Configure risk-based responses:
- Low risk → Allow
- Medium risk → Require MFA
- High risk → Block

---

## Identity Pool Security

### Least Privilege IAM Roles

The #1 rule: give identity pool roles the absolute minimum permissions needed.

**Bad** — overly broad:
```json
{
  "Effect": "Allow",
  "Action": "s3:*",
  "Resource": "*"
}
```

**Good** — scoped to user's own data:
```json
{
  "Effect": "Allow",
  "Action": ["s3:GetObject", "s3:PutObject"],
  "Resource": "arn:aws:s3:::my-bucket/${cognito-identity.amazonaws.com:sub}/*"
}
```

### Trust Policy Conditions

Always include both conditions in the IAM role trust policy:

```json
{
  "Condition": {
    "StringEquals": {
      "cognito-identity.amazonaws.com:aud": "us-east-1:xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
    },
    "ForAnyValue:StringLike": {
      "cognito-identity.amazonaws.com:amr": "authenticated"
    }
  }
}
```

This ensures:
- `aud` matches your specific identity pool ID (not any identity pool)
- `amr` restricts to authenticated users only (or unauthenticated for guest role)

### Disable Guest Access

Only enable unauthenticated (guest) access if absolutely required. If enabled:
- Grant read-only access to truly public resources
- Monitor unauthenticated usage patterns
- Set aggressive rate limits

### Use Enhanced Flow (Not Basic)

Enhanced (simplified) flow handles role selection server-side. Basic (classic) flow delegates role selection to the client, which can be manipulated. Always prefer enhanced flow.

---

## Token Security

### Storage

| Platform | ID/Access Tokens | Refresh Token |
|----------|-----------------|---------------|
| Web (SPA) | In-memory (JS variable) | HttpOnly Secure cookie |
| Web (SSR) | HttpOnly Secure cookie | HttpOnly Secure cookie |
| iOS | Keychain | Keychain |
| Android | EncryptedSharedPreferences | EncryptedSharedPreferences |

**Never** store tokens in:
- localStorage (XSS vulnerable)
- sessionStorage (XSS vulnerable)
- Plain cookies without HttpOnly + Secure flags
- URL parameters

### Validation

Always validate tokens server-side:
1. Verify the JWT signature against the JWKS endpoint (`https://cognito-idp.{region}.amazonaws.com/{userPoolId}/.well-known/jwks.json`)
2. Check `exp` claim (expiration)
3. Check `iss` claim matches your user pool
4. Check `aud` (ID token) or `client_id` (access token) matches your app client
5. Check `token_use` is the expected type (`id` or `access`)

Use `aws-jwt-verify` for Node.js — it handles all of this correctly and caches JWKS.

### Token Revocation

- `signOut({ global: true })` in Amplify revokes refresh tokens
- `AdminUserGlobalSignOut` API revokes all sessions for a user
- `RevokeToken` API revokes a specific refresh token
- ID and access tokens remain valid until expiration even after revocation (short validity periods mitigate this)

---

## Network & Infrastructure

### AWS WAF

Associate a WAF web ACL with your user pool to:
- Rate limit authentication requests per IP
- Block known malicious IPs
- Add CAPTCHA for suspicious requests
- Geo-restrict if your app is region-specific

Recommended rules:
- Rate limit: 100-1000 requests per 5 minutes per IP (tune to your traffic)
- AWS Managed Rules: `AWSManagedRulesCommonRuleSet` for common attack patterns
- IP reputation: `AWSManagedRulesAmazonIpReputationList`

### VPC & Private Endpoints

If your backend runs in a VPC and calls Cognito APIs:
- Use VPC endpoints for `cognito-idp` to keep traffic off the public internet
- This doesn't apply to user-facing auth (managed login, OAuth endpoints are always public)

### Custom Domain SSL

When using a custom domain:
- ACM certificate must be in `us-east-1`
- Use TLS 1.2+ (Cognito enforces this)
- Set up a CNAME from your domain to the Cognito CloudFront distribution

---

## Monitoring & Incident Response

### CloudTrail

Enable CloudTrail logging to capture all Cognito API calls:
- `AdminCreateUser`, `AdminDeleteUser` — admin operations
- `InitiateAuth`, `RespondToAuthChallenge` — authentication attempts
- `ForgotPassword`, `ConfirmForgotPassword` — password resets
- `UpdateUserAttributes` — profile changes

### CloudWatch Metrics

Monitor these Cognito metrics:
- `SignUpSuccesses` / `SignUpThrottles`
- `SignInSuccesses` / `SignInThrottles`
- `TokenRefreshSuccesses` / `TokenRefreshThrottles`
- `FederationSuccesses` / `FederationThrottles`

Set alarms for:
- Spike in failed sign-in attempts (brute force)
- Spike in sign-up rate (bot registration)
- Throttling errors (quota exhaustion)

### Advanced Security Logging (Plus Plan)

With the Plus plan, Cognito logs detailed user activity including:
- Risk scores for each authentication attempt
- Device fingerprints
- IP addresses and locations
- Event types (sign-in, sign-up, password change)

Export to S3, CloudWatch Logs, or Data Firehose for analysis.

### Incident Response Playbook

**Compromised user account**:
1. `AdminUserGlobalSignOut` — revoke all sessions
2. `AdminResetUserPassword` — force password reset
3. `AdminSetUserMFAPreference` — enable MFA if not already
4. Review CloudTrail logs for unauthorized actions
5. If Identity Pool is used, the IAM credentials expire automatically (1 hour default)

**Suspected credential stuffing attack**:
1. Check CloudWatch for spike in failed `InitiateAuth` calls
2. Enable WAF rate limiting if not already active
3. Consider temporarily enabling CAPTCHA via WAF
4. Review source IPs in CloudTrail and block via WAF if patterns emerge
5. Enable adaptive authentication (Plus plan) for automatic risk-based responses

**SMS pumping detected**:
1. Monitor SNS spend in AWS Billing
2. Disable SMS as MFA/verification method temporarily
3. Switch to TOTP or email-based MFA
4. Add WAF rules to block traffic from suspicious regions
5. File an AWS Support case for help identifying the attack vector
