# Cognito Lambda Triggers

Lambda triggers let you customize Cognito's behavior at key points in the authentication lifecycle.

## Table of Contents
1. [Trigger Overview](#trigger-overview)
2. [Pre Sign-Up](#pre-sign-up)
3. [Post Confirmation](#post-confirmation)
4. [Pre Authentication](#pre-authentication)
5. [Post Authentication](#post-authentication)
6. [Pre Token Generation](#pre-token-generation)
7. [Custom Message](#custom-message)
8. [User Migration](#user-migration)
9. [Custom Auth Triggers](#custom-auth-triggers)
10. [CDK Wiring](#cdk-wiring)

---

## Trigger Overview

| Trigger | When It Fires | Common Use Cases |
|---------|--------------|------------------|
| Pre Sign-Up | Before a new user is registered | Auto-confirm users, validate email domains, block disposable emails |
| Post Confirmation | After user confirms their account | Create user record in DynamoDB, send welcome email, add to default group |
| Pre Authentication | Before credentials are validated | Custom validation, rate limiting, block certain users |
| Post Authentication | After successful authentication | Log sign-in events, update last-login timestamp |
| Pre Token Generation | Before tokens are issued | Add custom claims, modify group claims, inject tenant info |
| Custom Message | Before Cognito sends an SMS/email | Customize verification emails, localize messages |
| User Migration | When user signs in but doesn't exist in pool | Migrate users from legacy auth system on-demand |
| Define Auth Challenge | During custom auth flow | Control challenge sequence |
| Create Auth Challenge | During custom auth flow | Generate OTP, magic link |
| Verify Auth Challenge | During custom auth flow | Validate user's challenge response |

**Critical constraints**:
- All triggers have a **5-second timeout**. Keep them fast.
- Triggers run **synchronously** — they block the auth flow until complete.
- The Lambda execution role needs `cognito-idp:*` only if the trigger calls Cognito APIs.

---

## Pre Sign-Up

Fires before Cognito creates the user. You can auto-confirm, auto-verify, or reject the sign-up.

```typescript
export const handler = async (event: any) => {
  const email = event.request.userAttributes.email;

  // Block disposable email domains
  const disposableDomains = ['tempmail.com', 'throwaway.email', 'guerrillamail.com'];
  const domain = email.split('@')[1];
  if (disposableDomains.includes(domain)) {
    throw new Error('Disposable email addresses are not allowed.');
  }

  // Auto-confirm users from your corporate domain
  if (domain === 'yourcompany.com') {
    event.response.autoConfirmUser = true;
    event.response.autoVerifyEmail = true;
  }

  return event;
};
```

### Auto-Confirm and Link Federated Users

When a social login user already has a native account with the same email:

```typescript
export const handler = async (event: any) => {
  // If this is a federated sign-up (external provider), auto-confirm
  if (event.triggerSource === 'PreSignUp_ExternalProvider') {
    event.response.autoConfirmUser = true;
    event.response.autoVerifyEmail = true;
  }
  return event;
};
```

---

## Post Confirmation

Fires after the user confirms their account (or is auto-confirmed). Safe place for side effects.

```typescript
import { DynamoDBClient, PutItemCommand } from '@aws-sdk/client-dynamodb';

const dynamo = new DynamoDBClient({});

export const handler = async (event: any) => {
  // Create user record in DynamoDB
  await dynamo.send(new PutItemCommand({
    TableName: process.env.USERS_TABLE!,
    Item: {
      pk: { S: `USER#${event.request.userAttributes.sub}` },
      sk: { S: 'PROFILE' },
      email: { S: event.request.userAttributes.email },
      name: { S: event.request.userAttributes.name || '' },
      createdAt: { S: new Date().toISOString() },
    },
    ConditionExpression: 'attribute_not_exists(pk)', // Idempotent
  }));

  return event;
};
```

---

## Pre Authentication

Fires before Cognito validates credentials. Use for custom blocklisting or rate limiting.

```typescript
export const handler = async (event: any) => {
  const email = event.request.userAttributes.email;

  // Block specific users
  const blockedUsers = await getBlockedUsers(); // Your logic
  if (blockedUsers.includes(email)) {
    throw new Error('Your account has been suspended. Contact support.');
  }

  return event;
};
```

---

## Post Authentication

Fires after successful authentication. Good for audit logging.

```typescript
export const handler = async (event: any) => {
  console.log(JSON.stringify({
    event: 'user_sign_in',
    userId: event.request.userAttributes.sub,
    email: event.request.userAttributes.email,
    source: event.triggerSource,
    timestamp: new Date().toISOString(),
  }));

  return event;
};
```

---

## Pre Token Generation

Fires before tokens are created. Add or modify claims in the ID and access tokens.

### V2 Trigger (Essentials/Plus plans — recommended)

```typescript
export const handler = async (event: any) => {
  // Add custom claims to the ID token
  event.response.claimsAndScopeOverrideDetails = {
    idTokenGeneration: {
      claimsToAddOrOverride: {
        'custom:tenant': 'acme-corp',
        'custom:permissions': JSON.stringify(['read', 'write']),
      },
      claimsToSuppress: ['email_verified'], // Remove claims you don't want exposed
    },
    accessTokenGeneration: {
      claimsToAddOrOverride: {
        'custom:role': 'admin',
      },
      scopesToAdd: ['custom-scope'],
      scopesToSuppress: [],
    },
  };

  return event;
};
```

### V1 Trigger (Lite plan)

```typescript
export const handler = async (event: any) => {
  // V1 can only modify ID token claims and group overrides
  event.response.claimsOverrideDetails = {
    claimsToAddOrOverride: {
      'custom:tenant': 'acme-corp',
    },
    groupsToOverride: ['admin', 'users'], // Override cognito:groups claim
  };

  return event;
};
```

---

## Custom Message

Customize the content of emails and SMS messages Cognito sends.

```typescript
export const handler = async (event: any) => {
  const { codeParameter, usernameParameter } = event.request;

  switch (event.triggerSource) {
    case 'CustomMessage_SignUp':
      event.response.emailSubject = 'Welcome! Confirm your account';
      event.response.emailMessage = `
        <h1>Welcome to Our App!</h1>
        <p>Your verification code is: <strong>${codeParameter}</strong></p>
      `;
      break;

    case 'CustomMessage_ForgotPassword':
      event.response.emailSubject = 'Reset your password';
      event.response.emailMessage = `
        <p>Your password reset code is: <strong>${codeParameter}</strong></p>
        <p>This code expires in 1 hour.</p>
      `;
      break;

    case 'CustomMessage_ResendCode':
      event.response.emailSubject = 'Your new verification code';
      event.response.emailMessage = `
        <p>Your new code is: <strong>${codeParameter}</strong></p>
      `;
      break;
  }

  return event;
};
```

---

## User Migration

Migrate users on-demand from a legacy auth system. Fires when a user tries to sign in but doesn't exist in the pool.

```typescript
export const handler = async (event: any) => {
  if (event.triggerSource === 'UserMigration_Authentication') {
    // Validate against your legacy system
    const legacyUser = await legacyAuth(
      event.userName,
      event.request.password
    );

    if (legacyUser) {
      event.response.userAttributes = {
        email: legacyUser.email,
        email_verified: 'true',
        name: legacyUser.name,
        'custom:legacyId': legacyUser.id,
      };
      event.response.finalUserStatus = 'CONFIRMED';
      event.response.messageAction = 'SUPPRESS'; // Don't send welcome email
    } else {
      throw new Error('Bad credentials');
    }
  }

  if (event.triggerSource === 'UserMigration_ForgotPassword') {
    const legacyUser = await legacyLookup(event.userName);
    if (legacyUser) {
      event.response.userAttributes = {
        email: legacyUser.email,
        email_verified: 'true',
      };
      event.response.messageAction = 'SUPPRESS';
    }
  }

  return event;
};
```

---

## CDK Wiring

### Attach Triggers to User Pool

```typescript
import * as lambda from 'aws-cdk-lib/aws-lambda-nodejs';
import * as cognito from 'aws-cdk-lib/aws-cognito';

// Create the Lambda
const preSignUpFn = new lambda.NodejsFunction(this, 'PreSignUp', {
  entry: 'src/triggers/pre-sign-up.ts',
  runtime: lambda.Runtime.NODEJS_20_X,
  timeout: cdk.Duration.seconds(5),
});

const postConfirmFn = new lambda.NodejsFunction(this, 'PostConfirm', {
  entry: 'src/triggers/post-confirmation.ts',
  runtime: lambda.Runtime.NODEJS_20_X,
  timeout: cdk.Duration.seconds(5),
  environment: {
    USERS_TABLE: usersTable.tableName,
  },
});

// Grant DynamoDB access
usersTable.grantWriteData(postConfirmFn);

// Attach to user pool
const userPool = new cognito.UserPool(this, 'UserPool', {
  // ... other config
  lambdaTriggers: {
    preSignUp: preSignUpFn,
    postConfirmation: postConfirmFn,
    preTokenGeneration: preTokenGenFn,
    customMessage: customMessageFn,
  },
});
```

### Pre Token Generation V2 Trigger (CDK)

The V2 trigger requires setting the trigger config explicitly:

```typescript
const cfnUserPool = userPool.node.defaultChild as cognito.CfnUserPool;
cfnUserPool.lambdaConfig = {
  ...cfnUserPool.lambdaConfig,
  preTokenGenerationConfig: {
    lambdaArn: preTokenGenFn.functionArn,
    lambdaVersion: 'V2_0',
  },
};

// Grant Cognito permission to invoke the Lambda
preTokenGenFn.addPermission('CognitoInvoke', {
  principal: new iam.ServicePrincipal('cognito-idp.amazonaws.com'),
  sourceArn: userPool.userPoolArn,
});
```
