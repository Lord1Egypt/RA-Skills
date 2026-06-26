---
name: cognito
description: >
  Use this skill for ANY task involving AWS Cognito — user pools, identity pools, authentication flows,
  token handling, social/enterprise federation, MFA, Lambda triggers, hosted UI, or Cognito integration
  with API Gateway, AppSync, S3, DynamoDB, Amplify, or any AWS service. Trigger whenever the user mentions
  "Cognito", "user pool", "identity pool", "auth flow", "social login with AWS", "JWT tokens from AWS",
  "hosted UI", "managed login", "Cognito triggers", "OAuth with Cognito", "SAML federation", "MFA setup",
  "sign-up/sign-in", "password policy", "Cognito CDK", "Cognito CloudFormation", "Cognito Terraform",
  "Cognito SDK", "aws-amplify auth", "token refresh", "Cognito groups", "RBAC with Cognito",
  or any authentication/authorization task that could involve AWS Cognito — even if they don't name
  Cognito explicitly but describe a pattern it solves (e.g. "I need user auth for my AWS app").
---

# AWS Cognito Skill

This skill helps you build, configure, debug, and manage AWS Cognito resources — user pools, identity pools, app clients, Lambda triggers, federation, and integrations with other AWS services.

## Quick Decision: What Does the User Need?

1. **New Cognito setup from scratch** → Read `references/setup-guide.md`, then follow the setup workflow
2. **CDK / CloudFormation / Terraform IaC** → Read `references/iac-patterns.md` for production-ready templates
3. **Authentication flow implementation** → Read `references/auth-flows.md` for SDK code and flow selection
4. **Debugging / troubleshooting** → Read `references/troubleshooting.md` for common issues and fixes
5. **Lambda triggers** → Read `references/lambda-triggers.md` for trigger patterns
6. **Security hardening** → Read `references/security.md` for best practices

Read the relevant reference file(s) before generating any code or configuration. Multiple files may apply — for example, a new CDK setup would benefit from both `setup-guide.md` and `iac-patterns.md`.

## Core Concepts (Always Keep in Mind)

### User Pools vs Identity Pools

These are the two main Cognito components and they serve different purposes:

- **User Pool**: A user directory and OIDC identity provider. Handles sign-up, sign-in, MFA, token issuance (ID token, access token, refresh token), and federation with external IdPs. Think of it as "who is this user?"
- **Identity Pool** (Federated Identities): Exchanges tokens (from a user pool, social provider, SAML, or OIDC) for temporary AWS credentials (STS). Think of it as "what AWS resources can this user access?"

A common architecture uses both: User Pool authenticates the user and issues tokens → Identity Pool exchanges those tokens for AWS credentials → User accesses S3, DynamoDB, etc.

### Feature Plans (Pricing Tiers)

As of late 2024, Cognito uses feature plans instead of the old "advanced security" toggle:

- **Lite**: Low-cost, basic auth features. Good for simple apps with fewer MAUs.
- **Essentials** (default for new pools): All latest auth features including access-token customization and managed login.
- **Plus**: Everything in Essentials plus threat protection (adaptive auth, compromised credential detection).

Always ask the user which plan they need, or default to Essentials for new setups.

### Token Types

- **ID Token**: Contains user identity claims (email, name, groups, custom attributes). Use for identity verification on your backend.
- **Access Token**: Contains scopes and authorized actions. Use for API authorization (e.g., API Gateway Cognito Authorizer).
- **Refresh Token**: Long-lived token to obtain new ID/access tokens without re-authentication. Default validity is 30 days.

## Workflow: Building a Cognito Solution

### Step 1: Clarify Requirements

Before writing any code, determine:

- **Auth methods**: Username/password? Email-only? Phone? Social login (Google, Apple, Facebook)? Enterprise SAML/OIDC?
- **MFA**: Required, optional, or off? SMS, TOTP authenticator app, or email?
- **Self-service sign-up**: Enabled or admin-only user creation?
- **Token usage**: Frontend-only (SPA/mobile)? Backend API authorization? Direct AWS resource access?
- **IaC preference**: CDK (TypeScript/Python), CloudFormation, Terraform, or console/CLI?
- **Frontend framework**: React/Amplify, Next.js, Vue, mobile (iOS/Android), or custom?

### Step 2: Design the Architecture

Based on requirements, determine:

- User Pool configuration (sign-in aliases, attributes, password policy, MFA)
- App client(s) — public (no secret, for SPAs/mobile) vs confidential (with secret, for server-side)
- OAuth flows — Authorization Code (with PKCE for public clients), Implicit (legacy, avoid), Client Credentials (M2M)
- Whether an Identity Pool is needed (only if users need direct AWS resource access)
- Lambda triggers needed (pre-sign-up, post-confirmation, pre-token-generation, custom auth, etc.)
- Domain — Cognito-hosted prefix domain or custom domain

### Step 3: Implement

Read the appropriate reference files and generate code. Always:

- Use the latest CDK v2 constructs (`aws-cdk-lib/aws-cognito`) — never CDK v1
- For SDK code, use AWS SDK v3 (`@aws-sdk/client-cognito-identity-provider`) — never v2
- For frontend, prefer Amplify v6 (`aws-amplify`) patterns
- Include proper error handling and token refresh logic
- Set `RemovalPolicy.RETAIN` on user pools in production (data loss prevention)
- Never hardcode secrets — use environment variables or AWS Secrets Manager

### Step 4: Security Review

Before declaring done, verify against `references/security.md`:

- MFA is enabled (at least optional) for production
- Password policy meets requirements (minimum 8 chars, complexity rules)
- Token validity periods are reasonable
- WAF is considered for public-facing auth endpoints
- Least-privilege IAM for any Identity Pool roles
- Client secrets are used for confidential clients
- HTTPS-only callback URLs

## Common Patterns Quick Reference

### Cognito + API Gateway
Use a Cognito User Pool Authorizer on API Gateway. The access token is validated automatically. Scopes in the token control which API methods are accessible.

### Cognito + AppSync
Configure `AMAZON_COGNITO_USER_POOLS` authorization on your GraphQL API. Use `@auth` directives in your schema for fine-grained access control.

### Cognito + S3 (via Identity Pool)
User Pool → Identity Pool → IAM role with S3 permissions scoped to `${cognito-identity.amazonaws.com:sub}/*` for per-user folders.

### Cognito + Lambda (Custom Auth)
Use `CUSTOM_AUTH` flow with Define, Create, and Verify Auth Challenge triggers for passwordless (magic link, OTP) or multi-step authentication.

### Machine-to-Machine (M2M)
Use Client Credentials grant with a resource server and custom scopes. No user interaction — one app authenticating to another.

## Important Reminders

- User pool attributes marked as required at creation CANNOT be changed later. Plan attributes carefully.
- Custom attributes are always prefixed with `custom:` (e.g., `custom:company`).
- The `sub` attribute is the unique, immutable user identifier. Use it as your primary key, not email or username.
- Email/phone verification is separate from sign-in aliases. Auto-verify what you use for sign-in.
- Cognito has service quotas (e.g., API request rate limits). For high-volume apps, request quota increases proactively.
- Lambda triggers execute synchronously and have a 5-second timeout. Keep them fast.
