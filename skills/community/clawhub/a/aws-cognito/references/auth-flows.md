# Cognito Authentication Flows

SDK code patterns for implementing authentication in your application.

## Table of Contents
1. [Flow Selection Guide](#flow-selection-guide)
2. [Amplify v6 (React / Next.js)](#amplify-v6)
3. [AWS SDK v3 (Node.js Backend)](#aws-sdk-v3-nodejs)
4. [AWS SDK v3 (Python / Boto3)](#boto3-python)
5. [Token Handling](#token-handling)
6. [Custom Auth (Passwordless)](#custom-auth-passwordless)
7. [Machine-to-Machine](#machine-to-machine)

---

## Flow Selection Guide

| Scenario | Flow | Client Type |
|----------|------|-------------|
| SPA or mobile app | Authorization Code + PKCE | Public (no secret) |
| Server-rendered web app | Authorization Code | Confidential (with secret) |
| Direct username/password (SPA) | USER_SRP_AUTH via SDK | Public |
| Admin creates/authenticates users | ADMIN_USER_PASSWORD_AUTH | Server-side only |
| Passwordless (magic link, OTP) | CUSTOM_AUTH with Lambda triggers | Either |
| Service-to-service | Client Credentials | Confidential |
| Migration from legacy auth | USER_PASSWORD_AUTH + migration trigger | Temporary |

**General rules**:
- Always prefer SRP over plaintext password flows
- Always use PKCE for public clients
- Never use Implicit flow (legacy, insecure)
- Always implement token refresh

---

## Amplify v6

### Installation

```bash
npm install aws-amplify
```

### Configuration

```typescript
// amplifyconfiguration.ts
import { Amplify } from 'aws-amplify';

Amplify.configure({
  Auth: {
    Cognito: {
      userPoolId: 'us-east-1_XXXXXXXXX',
      userPoolClientId: 'xxxxxxxxxxxxxxxxxxxxxxxxxx',
      loginWith: {
        oauth: {
          domain: 'your-domain.auth.us-east-1.amazoncognito.com',
          scopes: ['openid', 'email', 'profile'],
          redirectSignIn: ['http://localhost:3000/'],
          redirectSignOut: ['http://localhost:3000/'],
          responseType: 'code',
        },
      },
    },
  },
});
```

### Sign Up

```typescript
import { signUp } from 'aws-amplify/auth';

async function handleSignUp(email: string, password: string) {
  try {
    const { isSignUpComplete, userId, nextStep } = await signUp({
      username: email,
      password,
      options: {
        userAttributes: {
          email,
          name: 'Jane Doe',
        },
      },
    });

    if (nextStep.signUpStep === 'CONFIRM_SIGN_UP') {
      // User needs to enter verification code
      console.log('Verification code sent to:', email);
    }
  } catch (error) {
    console.error('Sign up error:', error);
  }
}
```

### Confirm Sign Up

```typescript
import { confirmSignUp } from 'aws-amplify/auth';

async function handleConfirmation(email: string, code: string) {
  try {
    const { isSignUpComplete } = await confirmSignUp({
      username: email,
      confirmationCode: code,
    });
    console.log('Sign up confirmed:', isSignUpComplete);
  } catch (error) {
    console.error('Confirmation error:', error);
  }
}
```

### Sign In

```typescript
import { signIn } from 'aws-amplify/auth';

async function handleSignIn(email: string, password: string) {
  try {
    const { isSignedIn, nextStep } = await signIn({
      username: email,
      password,
    });

    switch (nextStep.signInStep) {
      case 'DONE':
        console.log('Signed in successfully');
        break;
      case 'CONFIRM_SIGN_IN_WITH_TOTP_CODE':
        // User needs to enter TOTP code
        break;
      case 'CONFIRM_SIGN_IN_WITH_SMS_CODE':
        // User needs to enter SMS code
        break;
      case 'CONFIRM_SIGN_IN_WITH_NEW_PASSWORD_REQUIRED':
        // Admin-created user needs to set password
        break;
    }
  } catch (error) {
    console.error('Sign in error:', error);
  }
}
```

### Social / Federated Sign In

```typescript
import { signInWithRedirect } from 'aws-amplify/auth';

// Google
await signInWithRedirect({ provider: 'Google' });

// Facebook
await signInWithRedirect({ provider: 'Facebook' });

// Apple
await signInWithRedirect({ provider: 'Apple' });

// SAML
await signInWithRedirect({
  provider: { custom: 'YourSAMLProviderName' },
});
```

### Get Current Session / Tokens

```typescript
import { fetchAuthSession, getCurrentUser } from 'aws-amplify/auth';

// Get the current user
const user = await getCurrentUser();
console.log('User ID:', user.userId);
console.log('Username:', user.username);

// Get tokens (automatically refreshes if expired)
const session = await fetchAuthSession();
const idToken = session.tokens?.idToken?.toString();
const accessToken = session.tokens?.accessToken?.toString();

// Get AWS credentials (if Identity Pool is configured)
const credentials = session.credentials;
```

### Sign Out

```typescript
import { signOut } from 'aws-amplify/auth';

// Local sign out
await signOut();

// Global sign out (invalidates all sessions)
await signOut({ global: true });
```

### Password Reset

```typescript
import { resetPassword, confirmResetPassword } from 'aws-amplify/auth';

// Step 1: Initiate reset
const { nextStep } = await resetPassword({ username: email });
// nextStep.resetPasswordStep === 'CONFIRM_RESET_PASSWORD_WITH_CODE'

// Step 2: Confirm with code and new password
await confirmResetPassword({
  username: email,
  confirmationCode: code,
  newPassword: newPassword,
});
```

### MFA Setup

```typescript
import { setUpTOTP, verifyTOTPSetup, updateMFAPreference } from 'aws-amplify/auth';

// Set up TOTP
const totpSetup = await setUpTOTP();
const setupUri = totpSetup.getSetupUri('YourApp', email);
// Display setupUri as QR code for user to scan

// Verify TOTP with code from authenticator app
await verifyTOTPSetup({ code: '123456' });

// Set TOTP as preferred MFA
await updateMFAPreference({ totp: 'PREFERRED' });
```

---

## AWS SDK v3 (Node.js)

### Installation

```bash
npm install @aws-sdk/client-cognito-identity-provider
```

### Admin: Create User

```typescript
import {
  CognitoIdentityProviderClient,
  AdminCreateUserCommand,
} from '@aws-sdk/client-cognito-identity-provider';

const client = new CognitoIdentityProviderClient({ region: 'us-east-1' });

async function createUser(email: string) {
  const command = new AdminCreateUserCommand({
    UserPoolId: process.env.USER_POOL_ID,
    Username: email,
    UserAttributes: [
      { Name: 'email', Value: email },
      { Name: 'email_verified', Value: 'true' },
      { Name: 'name', Value: 'Jane Doe' },
    ],
    DesiredDeliveryMediums: ['EMAIL'],
  });
  return client.send(command);
}
```

### Admin: Authenticate User (Server-Side)

```typescript
import { AdminInitiateAuthCommand } from '@aws-sdk/client-cognito-identity-provider';

async function adminSignIn(email: string, password: string) {
  const command = new AdminInitiateAuthCommand({
    UserPoolId: process.env.USER_POOL_ID,
    ClientId: process.env.CLIENT_ID,
    AuthFlow: 'ADMIN_USER_PASSWORD_AUTH',
    AuthParameters: {
      USERNAME: email,
      PASSWORD: password,
    },
  });
  const response = await client.send(command);
  return response.AuthenticationResult; // { IdToken, AccessToken, RefreshToken }
}
```

### Verify Token (Backend Middleware)

```typescript
import { CognitoJwtVerifier } from 'aws-jwt-verify';

// Create verifier (reuse this — it caches JWKS)
const verifier = CognitoJwtVerifier.create({
  userPoolId: process.env.USER_POOL_ID!,
  tokenUse: 'access', // or 'id'
  clientId: process.env.CLIENT_ID!,
});

async function verifyToken(token: string) {
  try {
    const payload = await verifier.verify(token);
    return payload; // { sub, email, cognito:groups, ... }
  } catch {
    throw new Error('Invalid token');
  }
}
```

Install the JWT verifier: `npm install aws-jwt-verify`

### Admin: Add User to Group

```typescript
import { AdminAddUserToGroupCommand } from '@aws-sdk/client-cognito-identity-provider';

async function addToGroup(username: string, groupName: string) {
  const command = new AdminAddUserToGroupCommand({
    UserPoolId: process.env.USER_POOL_ID,
    Username: username,
    GroupName: groupName,
  });
  return client.send(command);
}
```

### Refresh Tokens

```typescript
import { InitiateAuthCommand } from '@aws-sdk/client-cognito-identity-provider';

async function refreshTokens(refreshToken: string) {
  const command = new InitiateAuthCommand({
    ClientId: process.env.CLIENT_ID,
    AuthFlow: 'REFRESH_TOKEN_AUTH',
    AuthParameters: {
      REFRESH_TOKEN: refreshToken,
    },
  });
  const response = await client.send(command);
  return response.AuthenticationResult; // New IdToken and AccessToken
}
```

---

## Boto3 (Python)

### Admin: Create User

```python
import boto3

client = boto3.client('cognito-idp', region_name='us-east-1')

def create_user(email: str, user_pool_id: str):
    return client.admin_create_user(
        UserPoolId=user_pool_id,
        Username=email,
        UserAttributes=[
            {'Name': 'email', 'Value': email},
            {'Name': 'email_verified', 'Value': 'true'},
            {'Name': 'name', 'Value': 'Jane Doe'},
        ],
        DesiredDeliveryMediums=['EMAIL'],
    )
```

### Admin: Authenticate User

```python
def admin_sign_in(email: str, password: str, user_pool_id: str, client_id: str):
    return client.admin_initiate_auth(
        UserPoolId=user_pool_id,
        ClientId=client_id,
        AuthFlow='ADMIN_USER_PASSWORD_AUTH',
        AuthParameters={
            'USERNAME': email,
            'PASSWORD': password,
        },
    )
```

### User: Sign Up (Self-Service)

```python
def sign_up(email: str, password: str, client_id: str):
    return client.sign_up(
        ClientId=client_id,
        Username=email,
        Password=password,
        UserAttributes=[
            {'Name': 'email', 'Value': email},
            {'Name': 'name', 'Value': 'Jane Doe'},
        ],
    )
```

---

## Token Handling

### Token Structure

**ID Token claims** (JWT):
- `sub` — unique user identifier (UUID)
- `email` — user's email
- `email_verified` — boolean
- `cognito:username` — the username
- `cognito:groups` — array of group names
- `custom:*` — any custom attributes
- `iss` — issuer (user pool URL)
- `aud` — audience (client ID)
- `exp` — expiration timestamp

**Access Token claims**:
- `sub` — same as ID token
- `scope` — OAuth scopes
- `cognito:groups` — group names
- `client_id` — the app client ID
- `token_use` — always "access"

### Best Practices

- Store tokens securely: HttpOnly cookies for web, Keychain/Keystore for mobile
- Never store tokens in localStorage (XSS vulnerable)
- Always validate tokens on your backend — don't trust client-side validation alone
- Use the `aws-jwt-verify` library (not manual JWT parsing) for Node.js
- Check `token_use` claim to ensure you're validating the right token type
- Implement automatic token refresh before expiration

---

## Custom Auth (Passwordless)

### Architecture

Uses three Lambda triggers working together:
1. **Define Auth Challenge**: Decides which challenge to present next
2. **Create Auth Challenge**: Generates the challenge (e.g., sends OTP)
3. **Verify Auth Challenge**: Validates the user's response

### Example: Email OTP Flow

**Define Auth Challenge Lambda**:
```typescript
export const handler = async (event: any) => {
  const session = event.request.session;

  if (session.length === 0) {
    // First attempt — issue custom challenge
    event.response.challengeName = 'CUSTOM_CHALLENGE';
    event.response.issueTokens = false;
    event.response.failAuthentication = false;
  } else if (
    session.length === 1 &&
    session[0].challengeResult === true
  ) {
    // Challenge answered correctly — issue tokens
    event.response.issueTokens = true;
    event.response.failAuthentication = false;
  } else {
    // Wrong answer — fail
    event.response.issueTokens = false;
    event.response.failAuthentication = true;
  }

  return event;
};
```

**Create Auth Challenge Lambda**:
```typescript
import { SESClient, SendEmailCommand } from '@aws-sdk/client-ses';

const ses = new SESClient({});

export const handler = async (event: any) => {
  const otp = Math.floor(100000 + Math.random() * 900000).toString();

  // Send OTP via email
  await ses.send(new SendEmailCommand({
    Destination: { ToAddresses: [event.request.userAttributes.email] },
    Message: {
      Subject: { Data: 'Your verification code' },
      Body: { Text: { Data: `Your code is: ${otp}` } },
    },
    Source: 'noreply@yourdomain.com',
  }));

  event.response.publicChallengeParameters = {
    email: event.request.userAttributes.email,
  };
  event.response.privateChallengeParameters = { otp };
  event.response.challengeMetadata = 'EMAIL_OTP';

  return event;
};
```

**Verify Auth Challenge Lambda**:
```typescript
export const handler = async (event: any) => {
  const expected = event.request.privateChallengeParameters.otp;
  const answer = event.request.challengeAnswer;

  event.response.answerCorrect = expected === answer;
  return event;
};
```

---

## Machine-to-Machine

### Getting M2M Tokens

M2M uses the Client Credentials flow — no user interaction involved.

```typescript
async function getM2MToken(
  domain: string,
  clientId: string,
  clientSecret: string,
  scopes: string[]
) {
  const credentials = Buffer.from(`${clientId}:${clientSecret}`).toString('base64');

  const response = await fetch(`https://${domain}/oauth2/token`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/x-www-form-urlencoded',
      Authorization: `Basic ${credentials}`,
    },
    body: new URLSearchParams({
      grant_type: 'client_credentials',
      scope: scopes.join(' '),
    }),
  });

  const data = await response.json();
  return data.access_token; // Only access token — no ID or refresh token
}
```

### Python M2M

```python
import requests
import base64

def get_m2m_token(domain: str, client_id: str, client_secret: str, scopes: list[str]):
    credentials = base64.b64encode(f"{client_id}:{client_secret}".encode()).decode()
    response = requests.post(
        f"https://{domain}/oauth2/token",
        headers={
            "Content-Type": "application/x-www-form-urlencoded",
            "Authorization": f"Basic {credentials}",
        },
        data={
            "grant_type": "client_credentials",
            "scope": " ".join(scopes),
        },
    )
    return response.json()["access_token"]
```
