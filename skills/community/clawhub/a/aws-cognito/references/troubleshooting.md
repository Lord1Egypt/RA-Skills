# Cognito Troubleshooting Guide

Common issues, error messages, and how to fix them.

## Table of Contents
1. [Authentication Errors](#authentication-errors)
2. [Token Issues](#token-issues)
3. [Federation Problems](#federation-problems)
4. [Lambda Trigger Failures](#lambda-trigger-failures)
5. [SDK & Amplify Issues](#sdk-and-amplify-issues)
6. [Quota & Throttling](#quota-and-throttling)
7. [CDK / IaC Deployment Issues](#deployment-issues)

---

## Authentication Errors

### `NotAuthorizedException: Incorrect username or password`

**Causes**:
- Wrong credentials (obvious)
- User exists but is in `FORCE_CHANGE_PASSWORD` status (admin-created, hasn't set own password)
- User pool has case-sensitive usernames and the case doesn't match
- App client doesn't have `ALLOW_USER_SRP_AUTH` enabled

**Fixes**:
- Check user status in Cognito console → Users
- If `FORCE_CHANGE_PASSWORD`: use `AdminSetUserPassword` with `Permanent: true`, or handle the `NEW_PASSWORD_REQUIRED` challenge in your app
- Verify `signInCaseSensitive` setting on the user pool

### `UserNotConfirmedException`

User signed up but hasn't verified their email/phone.

**Fix**: Call `ResendConfirmationCode` to send a new code, or `AdminConfirmSignUp` to confirm manually.

### `UserNotFoundException`

**If `preventUserExistenceErrors` is ON**: You won't see this error — Cognito returns a generic error instead. This is correct behavior.

**If OFF**: The user doesn't exist. Check username spelling and whether the user pool is the right one.

### `InvalidParameterException: USER_SRP_AUTH is not enabled`

The app client doesn't have the SRP auth flow enabled.

**Fix**: Update the app client to include `ALLOW_USER_SRP_AUTH` in `ExplicitAuthFlows`.

### `PasswordResetRequiredException`

Admin called `AdminResetUserPassword`. The user must complete the forgot-password flow before they can sign in.

### `UserLambdaValidationException`

A Lambda trigger threw an error. The error message from the Lambda is included.

**Debug**: Check CloudWatch Logs for the Lambda function. The trigger name is in the error details.

---

## Token Issues

### `Token is expired`

ID and access tokens have a default 1-hour validity.

**Fix**: Implement token refresh logic. With Amplify, `fetchAuthSession()` auto-refreshes. With SDK, call `InitiateAuth` with `REFRESH_TOKEN_AUTH` flow.

### `Invalid token` / Signature verification fails

**Causes**:
- Using the wrong JWKS endpoint (wrong region or user pool ID)
- Token was issued by a different user pool
- Token was tampered with
- Clock skew between your server and Cognito

**Fix**: Verify you're using the correct JWKS URL: `https://cognito-idp.{region}.amazonaws.com/{userPoolId}/.well-known/jwks.json`. Check server clock with NTP.

### `Token use doesn't match`

You're validating an ID token where an access token is expected, or vice versa.

**Fix**: Check the `token_use` claim. ID tokens have `"token_use": "id"`, access tokens have `"token_use": "access"`.

### Refresh token expired

Default refresh token validity is 30 days. After that, the user must re-authenticate.

**Fix**: Increase `RefreshTokenValidity` if needed (max 10 years). Redirect user to sign-in when refresh fails.

---

## Federation Problems

### `Invalid identity provider` / Provider not found

**Causes**:
- The identity provider name in the sign-in request doesn't match what's configured in Cognito
- The provider hasn't been added to the app client's `SupportedIdentityProviders`

**Fix**: Check the provider name exactly matches (case-sensitive). Ensure the provider is listed in the app client's supported providers.

### SAML: `Invalid saml response received`

**Common causes**:
- Metadata is stale (IdP rotated certificates)
- ACS URL in IdP config doesn't match Cognito's endpoint
- Clock skew between IdP and Cognito (SAML assertions have a validity window)
- Attribute mapping mismatch

**Fix**: Re-upload metadata from IdP. Verify ACS URL is `https://{domain}/saml2/idpresponse`. Check IdP logs for the outgoing assertion.

### Social login: Redirect loop or blank page

**Causes**:
- Callback URL in Cognito doesn't match the actual redirect URL
- Scopes mismatch between what's configured in Cognito and the social provider
- Social provider app isn't in "production" mode (e.g., Facebook app in development mode only works for test users)

**Fix**: Verify callback URLs match exactly (including trailing slashes). Check social provider's developer console for app status.

### `Already found an entry for username` (linking accounts)

A user tried to sign in with a social provider but an account with the same email already exists.

**Fix**: Implement account linking in a Pre Sign-Up trigger. When `triggerSource` is `PreSignUp_ExternalProvider`, call `AdminLinkProviderForUser` to link the social identity to the existing account.

---

## Lambda Trigger Failures

### `UserLambdaValidationException` with no useful message

**Debug steps**:
1. Go to CloudWatch Logs → find the log group for your Lambda
2. Check for runtime errors, timeouts, or unhandled exceptions
3. If no logs exist, the Lambda may not have permission to write to CloudWatch

### Lambda times out (5-second limit)

Cognito trigger Lambdas have a hard 5-second timeout.

**Fix**:
- Minimize cold starts: use provisioned concurrency or keep Lambdas warm
- Move slow operations (sending emails, complex DB queries) to async processes (SQS, EventBridge)
- Keep the trigger minimal — return quickly, process asynchronously

### `AccessDeniedException` when trigger calls Cognito API

The Lambda's execution role doesn't have permission to call Cognito APIs.

**Fix**: Add `cognito-idp:Admin*` permissions (scoped to your user pool ARN) to the Lambda's IAM role.

### Trigger not firing

**Causes**:
- Lambda isn't attached to the user pool (check Cognito console → User pool properties → Lambda triggers)
- Cognito doesn't have permission to invoke the Lambda
- The trigger source doesn't match (e.g., `PreSignUp_SignUp` vs `PreSignUp_ExternalProvider`)

**Fix**: Verify the Lambda trigger is configured. Add a resource-based policy on the Lambda allowing `cognito-idp.amazonaws.com` to invoke it.

---

## SDK & Amplify Issues

### Amplify: `No Cognito User Pool configuration`

Amplify isn't configured or the config is missing.

**Fix**: Ensure `Amplify.configure()` is called before any auth operations, typically in your app's entry point (`main.ts`, `App.tsx`, `_app.tsx`).

### Amplify: CORS errors

Cognito's hosted endpoints don't have CORS issues themselves, but your app might.

**Causes**:
- Calling Cognito APIs directly from the browser instead of using the SDK
- API Gateway behind Cognito doesn't have CORS configured
- OAuth redirect issues with different origins

**Fix**: Always use the Amplify SDK (never call Cognito endpoints directly from the browser). Configure CORS on API Gateway.

### SDK v3: `Missing credentials in config`

For admin operations (like `AdminInitiateAuth`), the SDK needs AWS credentials.

**Fix**: Ensure your server has valid AWS credentials (environment variables, IAM role, or credentials file). Client-side code should use Cognito's unauthenticated operations (`SignUp`, `InitiateAuth`) which don't require AWS credentials.

### `CredentialProviderError` in local development

**Fix**: Run `aws configure` or set `AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY` environment variables. For local Lambda development, use `aws-sdk-client-mock` for testing.

---

## Quota & Throttling

### `TooManyRequestsException` / `LimitExceededException`

Cognito has rate limits on API operations.

**Default quotas** (vary by operation and region):
- `UserCreation` (sign-up): 50/sec
- `UserAuthentication` (sign-in): 120/sec
- `UserRead` (get user): 120/sec
- `UserToken` (token refresh): 120/sec
- `UserResourceRead` (list users, etc.): 30/sec

**Fix**:
- Implement exponential backoff with jitter
- Request quota increases via Service Quotas console
- Cache user data instead of re-fetching from Cognito
- Use CloudWatch to identify which operations are being throttled

### Email sending quota

Default Cognito email: 50 emails/day.

**Fix**: Switch to SES. Even SES sandbox is limited to verified addresses — request production access for real usage.

---

## Deployment Issues

### CDK: `User pool already has a domain configured`

You can't have two domains on one user pool.

**Fix**: Delete the existing domain first (`aws cognito-idp delete-user-pool-domain`) or import it into your CDK stack.

### CDK: Circular dependency between user pool and Lambda trigger

**Fix**: Use `addTrigger` method after both resources are created, or break into separate stacks with cross-stack references.

### CloudFormation: User pool replacement (data loss!)

Certain property changes cause CloudFormation to replace the user pool (deleting all users).

**Dangerous changes** (trigger replacement):
- Changing `UsernameAttributes`
- Changing `AliasAttributes`
- Changing schema (adding/removing required attributes)

**Safe changes** (in-place update):
- Password policy
- MFA configuration
- Lambda triggers
- Email configuration
- App client changes

**Protection**: Always set `DeletionPolicy: Retain` and `UpdateReplacePolicy: Retain` on user pool resources.

### Terraform: `SchemaAttribute cannot be modified`

Cognito doesn't allow removing or modifying existing schema attributes.

**Fix**: Add new attributes, don't modify existing ones. If you must change a required attribute, you need a new user pool (and user migration).

### Custom domain: `One or more parameter values are not valid`

**Common cause**: ACM certificate is not in `us-east-1`, or the certificate isn't validated yet.

**Fix**: Create the ACM certificate in `us-east-1` (regardless of where the user pool is). Wait for DNS validation to complete before deploying.
