# Cognito Setup Guide

Step-by-step guidance for creating Cognito resources from scratch.

## Table of Contents
1. [User Pool Setup](#user-pool-setup)
2. [App Client Configuration](#app-client-configuration)
3. [Domain Setup](#domain-setup)
4. [Identity Pool Setup](#identity-pool-setup)
5. [Federation (Social & Enterprise)](#federation)
6. [MFA Configuration](#mfa-configuration)

---

## User Pool Setup

### Minimum Viable User Pool

Every user pool needs at minimum:
- Sign-in aliases (how users identify themselves)
- A password policy
- At least one app client

**Sign-in alias options** — choose carefully, these can't change after creation:
- `email` — most common for B2C apps
- `phone` — common in regions where phone is primary
- `username` — custom username, often combined with email as a verified contact
- `preferredUsername` — user-changeable display name (not unique)

**Standard attributes** — mark required ones at creation time (immutable decision):
- Common required: `email`, `name`
- Common optional: `phone_number`, `picture`, `address`, `birthdate`
- Only mark as required what you truly need at sign-up time

**Custom attributes** — up to 50, always prefixed `custom:`:
- String, Number, DateTime, Boolean types
- Can be mutable or immutable
- Cannot be made required (only standard attributes can be required)
- Cannot be removed once created (can only add new ones)

### Password Policy

Recommended production defaults:
- Minimum length: 8 (Cognito minimum is 6, but 8+ is best practice)
- Require at least: lowercase, uppercase, digit
- Symbols: optional but recommended
- Temporary password validity: 7 days (for admin-created accounts)

### Account Recovery

Options (pick one or combine):
- `EMAIL_ONLY` — most common, sends code to verified email
- `PHONE_ONLY_WITHOUT_MFA` — sends code to verified phone
- `PHONE_AND_EMAIL` — tries phone first, falls back to email
- `NONE` — no self-service recovery (admin must reset)

### Verification

Auto-verify attributes that are used for sign-in. If email is a sign-in alias, auto-verify email. If phone, auto-verify phone.

**Email verification methods**:
- `CODE` — sends a numeric code, user enters it (default, recommended)
- `LINK` — sends a clickable verification link

**Email sending options**:
- Default (Cognito-managed): Limited to 50 emails/day. Fine for dev/testing.
- Amazon SES: Required for production. Configure a verified SES identity and connect it to the user pool. Allows custom From addresses, higher quotas, and delivery tracking.

---

## App Client Configuration

### Public vs Confidential Clients

**Public client** (no client secret):
- For SPAs (React, Vue, Angular) and mobile apps
- Cannot securely store a client secret
- Use Authorization Code flow with PKCE
- Enable: `ALLOW_USER_SRP_AUTH` for direct sign-in, `ALLOW_REFRESH_TOKEN_AUTH` for token refresh

**Confidential client** (with client secret):
- For server-side apps (Node.js, Python, Java backends)
- Client secret is stored securely on the server
- Can use Authorization Code flow (with or without PKCE) or Client Credentials (M2M)
- Enable: `ALLOW_USER_SRP_AUTH`, `ALLOW_REFRESH_TOKEN_AUTH`

### Auth Flows to Enable

- `ALLOW_USER_SRP_AUTH` — Secure Remote Password, the standard username/password flow. Almost always enabled.
- `ALLOW_REFRESH_TOKEN_AUTH` — Required for token refresh. Almost always enabled.
- `ALLOW_USER_PASSWORD_AUTH` — Sends password in plaintext (over HTTPS). Use only if SRP isn't feasible (e.g., migration triggers).
- `ALLOW_CUSTOM_AUTH` — For Lambda-based custom authentication (passwordless, etc.).
- `ALLOW_ADMIN_USER_PASSWORD_AUTH` — Server-side admin auth. Requires IAM credentials.

### Token Validity

Recommended defaults:
- ID token: 1 hour (range: 5 min to 1 day)
- Access token: 1 hour (range: 5 min to 1 day)
- Refresh token: 30 days (range: 1 hour to 10 years)

For high-security apps, shorten ID/access to 15-30 minutes.

### OAuth Configuration

**Scopes**:
- `openid` — required for OIDC, returns ID token
- `email` — includes email and email_verified in ID token
- `phone` — includes phone_number and phone_number_verified
- `profile` — includes name, family_name, etc.
- `aws.cognito.signin.user.admin` — allows user to manage their own profile via Cognito API
- Custom scopes — defined via resource servers

**Callback URLs**: Where Cognito redirects after login. Must be HTTPS in production (localhost allowed for dev).

**Logout URLs**: Where Cognito redirects after logout.

---

## Domain Setup

Required for hosted UI / managed login and OAuth endpoints.

**Cognito-managed domain**: `https://<prefix>.auth.<region>.amazoncognito.com`
- Quick to set up, no SSL cert needed
- Use for dev/staging

**Custom domain**: `https://auth.yourdomain.com`
- Requires an ACM certificate in us-east-1
- Requires a CNAME DNS record pointing to the Cognito CloudFront distribution
- Use for production (brand consistency)

---

## Identity Pool Setup

Only needed when users require temporary AWS credentials to access AWS services directly (S3, DynamoDB, etc.).

### Configuration Decisions

- **Guest access**: Enable only if unauthenticated users need AWS credentials. Keep permissions extremely minimal.
- **Authentication providers**: Connect your user pool, social providers, SAML providers, or OIDC providers.
- **Role resolution**: Choose between "Use default role" and "Choose role with rules" (for attribute-based access control).

### IAM Roles

**Authenticated role**: Permissions granted to signed-in users.
**Unauthenticated role** (if guest access enabled): Permissions for anonymous users.

Always include trust policy conditions:
- `cognito-identity.amazonaws.com:aud` must match your identity pool ID
- `cognito-identity.amazonaws.com:amr` must be `authenticated` or `unauthenticated`

### Per-User Resource Scoping

Common pattern — scope S3 access to a per-user folder:
```json
{
  "Effect": "Allow",
  "Action": ["s3:GetObject", "s3:PutObject"],
  "Resource": "arn:aws:s3:::my-bucket/${cognito-identity.amazonaws.com:sub}/*"
}
```

---

## Federation

### Social Identity Providers

**Google**:
1. Create OAuth 2.0 credentials in Google Cloud Console
2. Configure in Cognito: client ID, client secret, authorized scopes (`openid email profile`)
3. Attribute mapping: Google `sub` → Cognito `username`, `email` → `email`, `name` → `name`

**Facebook**:
1. Create a Facebook App in Meta Developer Portal
2. Configure: app ID, app secret, authorized scopes (`public_profile,email`)
3. Attribute mapping: `id` → `username`, `email` → `email`, `name` → `name`

**Apple**:
1. Configure Sign in with Apple in Apple Developer account
2. Need: Services ID, Team ID, Key ID, Private Key
3. Attribute mapping: `sub` → `username`, `email` → `email`, `name` → `name`

### SAML Federation

1. Get metadata XML or URL from your IdP (Okta, Azure AD, ADFS, etc.)
2. Create a SAML identity provider in the user pool
3. Map SAML attributes to Cognito attributes
4. Configure the IdP with Cognito's SP metadata (entity ID and ACS URL from the user pool)

### OIDC Federation

1. Get issuer URL, client ID, and client secret from the OIDC provider
2. Create an OIDC identity provider in the user pool
3. Map OIDC claims to Cognito attributes

---

## MFA Configuration

### Options

- **OFF**: No MFA (not recommended for production)
- **OPTIONAL**: Users can enable MFA but aren't required to
- **REQUIRED**: All users must set up MFA

### MFA Methods

- **SMS**: Sends code via text message. Requires an IAM role for SNS. Vulnerable to SIM swapping — use TOTP when possible.
- **TOTP**: Authenticator app (Google Authenticator, Authy, etc.). More secure than SMS. Recommended as primary MFA method.
- **Email**: Sends code via email. Available on Essentials and Plus plans.

### Adaptive Authentication (Plus plan only)

Cognito evaluates risk for each sign-in attempt and can:
- Allow (low risk)
- Require MFA (medium risk)
- Block (high risk)

Risk factors include: new device, unusual location, impossible travel, compromised credentials.

### Device Tracking

- **Always**: Remember all devices
- **User opt-in**: User chooses to remember a device
- **Off**: No device tracking

Remembered devices can skip MFA on subsequent sign-ins.
