# Cognito Infrastructure as Code Patterns

Production-ready templates for CDK, CloudFormation, and Terraform.

## Table of Contents
1. [CDK (TypeScript)](#cdk-typescript)
2. [CDK (Python)](#cdk-python)
3. [CloudFormation](#cloudformation)
4. [Terraform](#terraform)
5. [Common Add-ons](#common-add-ons)

---

## CDK (TypeScript)

### Full User Pool + App Client + Domain

```typescript
import * as cdk from 'aws-cdk-lib';
import * as cognito from 'aws-cdk-lib/aws-cognito';
import { Construct } from 'constructs';

interface CognitoStackProps extends cdk.StackProps {
  stage: string;
  callbackUrls: string[];
  logoutUrls: string[];
  domainPrefix: string;
}

export class CognitoStack extends cdk.Stack {
  public readonly userPool: cognito.UserPool;
  public readonly userPoolClient: cognito.UserPoolClient;

  constructor(scope: Construct, id: string, props: CognitoStackProps) {
    super(scope, id, props);

    // User Pool
    this.userPool = new cognito.UserPool(this, 'UserPool', {
      userPoolName: `${props.stage}-user-pool`,
      selfSignUpEnabled: true,
      signInCaseSensitive: false,

      // Sign-in configuration
      signInAliases: {
        email: true,
      },

      // Auto-verify email since it's a sign-in alias
      autoVerify: {
        email: true,
      },

      // Keep original email/phone until new one is verified
      keepOriginal: {
        email: true,
      },

      // Password requirements
      passwordPolicy: {
        minLength: 8,
        requireLowercase: true,
        requireUppercase: true,
        requireDigits: true,
        requireSymbols: false,
        tempPasswordValidity: cdk.Duration.days(7),
      },

      // MFA
      mfa: cognito.Mfa.OPTIONAL,
      mfaSecondFactor: {
        sms: true,
        otp: true,
      },

      // Account recovery
      accountRecovery: cognito.AccountRecovery.EMAIL_ONLY,

      // Standard attributes
      standardAttributes: {
        email: { required: true, mutable: true },
        fullname: { required: false, mutable: true },
      },

      // Custom attributes
      customAttributes: {
        tenantId: new cognito.StringAttribute({ mutable: false }),
        role: new cognito.StringAttribute({ mutable: true }),
      },

      // Email configuration — switch to SES for production
      email: cognito.UserPoolEmail.withCognito('noreply@yourdomain.com'),

      // Feature plan
      featurePlan: cognito.FeaturePlan.ESSENTIALS,

      // IMPORTANT: Retain user data on stack deletion in production
      removalPolicy: props.stage === 'prod'
        ? cdk.RemovalPolicy.RETAIN
        : cdk.RemovalPolicy.DESTROY,

      // Deletion protection for production
      deletionProtection: props.stage === 'prod',
    });

    // User Pool Domain (for hosted UI / managed login)
    this.userPool.addDomain('CognitoDomain', {
      cognitoDomain: {
        domainPrefix: props.domainPrefix,
      },
    });

    // App Client (public — for SPA/mobile)
    this.userPoolClient = this.userPool.addClient('AppClient', {
      userPoolClientName: `${props.stage}-app-client`,
      generateSecret: false, // No secret for public clients

      // Auth flows
      authFlows: {
        userSrp: true,
        custom: true,
      },

      // OAuth configuration
      oAuth: {
        flows: {
          authorizationCodeGrant: true,
        },
        scopes: [
          cognito.OAuthScope.OPENID,
          cognito.OAuthScope.EMAIL,
          cognito.OAuthScope.PROFILE,
        ],
        callbackUrls: props.callbackUrls,
        logoutUrls: props.logoutUrls,
      },

      // Token validity
      idTokenValidity: cdk.Duration.hours(1),
      accessTokenValidity: cdk.Duration.hours(1),
      refreshTokenValidity: cdk.Duration.days(30),

      // Prevent user existence errors from leaking info
      preventUserExistenceErrors: true,
    });

    // Outputs
    new cdk.CfnOutput(this, 'UserPoolId', {
      value: this.userPool.userPoolId,
    });
    new cdk.CfnOutput(this, 'UserPoolClientId', {
      value: this.userPoolClient.userPoolClientId,
    });
  }
}
```

### Adding a Confidential (Server-Side) Client

```typescript
const serverClient = userPool.addClient('ServerClient', {
  userPoolClientName: `${stage}-server-client`,
  generateSecret: true, // Confidential client
  authFlows: {
    userSrp: true,
    adminUserPassword: true,
  },
  oAuth: {
    flows: {
      authorizationCodeGrant: true,
    },
    scopes: [
      cognito.OAuthScope.OPENID,
      cognito.OAuthScope.EMAIL,
    ],
    callbackUrls: ['https://api.yourdomain.com/auth/callback'],
    logoutUrls: ['https://api.yourdomain.com/auth/logout'],
  },
  preventUserExistenceErrors: true,
});
```

### Adding an Identity Pool (CDK v2 L2 Construct)

```typescript
import { IdentityPool, UserPoolAuthenticationProvider } from 'aws-cdk-lib/aws-cognito-identitypool';
import * as iam from 'aws-cdk-lib/aws-iam';
import * as s3 from 'aws-cdk-lib/aws-s3';

const identityPool = new IdentityPool(this, 'IdentityPool', {
  identityPoolName: `${stage}-identity-pool`,
  allowUnauthenticatedIdentities: false, // No guest access
  authenticationProviders: {
    userPools: [
      new UserPoolAuthenticationProvider({ userPool, userPoolClient }),
    ],
  },
});

// Grant authenticated users access to an S3 bucket (per-user prefix)
const dataBucket = new s3.Bucket(this, 'UserDataBucket');
identityPool.authenticatedRole.addToPrincipalPolicy(
  new iam.PolicyStatement({
    actions: ['s3:GetObject', 's3:PutObject', 's3:DeleteObject'],
    resources: [
      dataBucket.arnForObjects('${cognito-identity.amazonaws.com:sub}/*'),
    ],
  }),
);
```

### Adding Social Federation (Google Example)

```typescript
const googleProvider = new cognito.UserPoolIdentityProviderGoogle(this, 'Google', {
  userPool,
  clientId: 'your-google-client-id',
  clientSecretValue: cdk.SecretValue.secretsManager('google-client-secret'),
  scopes: ['openid', 'email', 'profile'],
  attributeMapping: {
    email: cognito.ProviderAttribute.GOOGLE_EMAIL,
    fullname: cognito.ProviderAttribute.GOOGLE_NAME,
    profilePicture: cognito.ProviderAttribute.GOOGLE_PICTURE,
  },
});

// Make sure the client depends on the provider
userPoolClient.node.addDependency(googleProvider);
```

### M2M (Client Credentials) Setup

```typescript
// Resource server with custom scopes
const resourceServer = userPool.addResourceServer('ResourceServer', {
  identifier: 'https://api.yourdomain.com',
  scopes: [
    { scopeName: 'read', scopeDescription: 'Read access' },
    { scopeName: 'write', scopeDescription: 'Write access' },
  ],
});

// M2M client
const m2mClient = userPool.addClient('M2MClient', {
  generateSecret: true,
  oAuth: {
    flows: { clientCredentials: true },
    scopes: [
      cognito.OAuthScope.resourceServer(resourceServer, {
        scopeName: 'read',
        scopeDescription: 'Read access',
      }),
    ],
  },
});
```

---

## CDK (Python)

### Full User Pool + App Client

```python
from aws_cdk import (
    Stack, Duration, RemovalPolicy, CfnOutput,
    aws_cognito as cognito,
)
from constructs import Construct


class CognitoStack(Stack):
    def __init__(self, scope: Construct, id: str, stage: str, **kwargs):
        super().__init__(scope, id, **kwargs)

        self.user_pool = cognito.UserPool(
            self, "UserPool",
            user_pool_name=f"{stage}-user-pool",
            self_sign_up_enabled=True,
            sign_in_case_sensitive=False,
            sign_in_aliases=cognito.SignInAliases(email=True),
            auto_verify=cognito.AutoVerifiedAttrs(email=True),
            keep_original=cognito.KeepOriginalAttrs(email=True),
            password_policy=cognito.PasswordPolicy(
                min_length=8,
                require_lowercase=True,
                require_uppercase=True,
                require_digits=True,
                require_symbols=False,
                temp_password_validity=Duration.days(7),
            ),
            mfa=cognito.Mfa.OPTIONAL,
            mfa_second_factor=cognito.MfaSecondFactor(sms=True, otp=True),
            account_recovery=cognito.AccountRecovery.EMAIL_ONLY,
            standard_attributes=cognito.StandardAttributes(
                email=cognito.StandardAttribute(required=True, mutable=True),
                fullname=cognito.StandardAttribute(required=False, mutable=True),
            ),
            feature_plan=cognito.FeaturePlan.ESSENTIALS,
            removal_policy=RemovalPolicy.RETAIN if stage == "prod" else RemovalPolicy.DESTROY,
            deletion_protection=True if stage == "prod" else False,
        )

        self.user_pool_client = self.user_pool.add_client(
            "AppClient",
            user_pool_client_name=f"{stage}-app-client",
            generate_secret=False,
            auth_flows=cognito.AuthFlow(user_srp=True, custom=True),
            o_auth=cognito.OAuthSettings(
                flows=cognito.OAuthFlows(authorization_code_grant=True),
                scopes=[
                    cognito.OAuthScope.OPENID,
                    cognito.OAuthScope.EMAIL,
                    cognito.OAuthScope.PROFILE,
                ],
                callback_urls=["https://yourdomain.com/callback"],
                logout_urls=["https://yourdomain.com/logout"],
            ),
            id_token_validity=Duration.hours(1),
            access_token_validity=Duration.hours(1),
            refresh_token_validity=Duration.days(30),
            prevent_user_existence_errors=True,
        )

        CfnOutput(self, "UserPoolId", value=self.user_pool.user_pool_id)
        CfnOutput(self, "ClientId", value=self.user_pool_client.user_pool_client_id)
```

---

## CloudFormation

### User Pool + Client (YAML)

```yaml
AWSTemplateFormatVersion: '2010-09-09'
Description: Cognito User Pool with App Client

Parameters:
  Stage:
    Type: String
    Default: dev
    AllowedValues: [dev, staging, prod]

Resources:
  UserPool:
    Type: AWS::Cognito::UserPool
    DeletionPolicy: Retain
    UpdateReplacePolicy: Retain
    Properties:
      UserPoolName: !Sub '${Stage}-user-pool'
      UsernameAttributes:
        - email
      AutoVerifiedAttributes:
        - email
      UsernameConfiguration:
        CaseSensitive: false
      Policies:
        PasswordPolicy:
          MinimumLength: 8
          RequireLowercase: true
          RequireUppercase: true
          RequireNumbers: true
          RequireSymbols: false
          TemporaryPasswordValidityDays: 7
      MfaConfiguration: OPTIONAL
      EnabledMfas:
        - SOFTWARE_TOKEN_MFA
        - SMS_MFA
      AccountRecoverySetting:
        RecoveryMechanisms:
          - Name: verified_email
            Priority: 1
      Schema:
        - Name: email
          AttributeDataType: String
          Required: true
          Mutable: true
        - Name: name
          AttributeDataType: String
          Required: false
          Mutable: true
        - Name: tenantId
          AttributeDataType: String
          Required: false
          Mutable: false
      UserPoolAddOns:
        AdvancedSecurityMode: ENFORCED  # For Plus plan

  UserPoolClient:
    Type: AWS::Cognito::UserPoolClient
    Properties:
      ClientName: !Sub '${Stage}-app-client'
      UserPoolId: !Ref UserPool
      GenerateSecret: false
      ExplicitAuthFlows:
        - ALLOW_USER_SRP_AUTH
        - ALLOW_REFRESH_TOKEN_AUTH
        - ALLOW_CUSTOM_AUTH
      AllowedOAuthFlows:
        - code
      AllowedOAuthScopes:
        - openid
        - email
        - profile
      AllowedOAuthFlowsUserPoolClient: true
      CallbackURLs:
        - https://yourdomain.com/callback
      LogoutURLs:
        - https://yourdomain.com/logout
      SupportedIdentityProviders:
        - COGNITO
      PreventUserExistenceErrors: ENABLED
      IdTokenValidity: 60       # minutes
      AccessTokenValidity: 60   # minutes
      RefreshTokenValidity: 43200  # minutes (30 days)
      TokenValidityUnits:
        IdToken: minutes
        AccessToken: minutes
        RefreshToken: minutes

  UserPoolDomain:
    Type: AWS::Cognito::UserPoolDomain
    Properties:
      Domain: !Sub '${Stage}-myapp'
      UserPoolId: !Ref UserPool

Outputs:
  UserPoolId:
    Value: !Ref UserPool
  UserPoolClientId:
    Value: !Ref UserPoolClient
  UserPoolDomain:
    Value: !Sub 'https://${Stage}-myapp.auth.${AWS::Region}.amazoncognito.com'
```

---

## Terraform

### User Pool + Client

```hcl
variable "stage" {
  type    = string
  default = "dev"
}

resource "aws_cognito_user_pool" "main" {
  name = "${var.stage}-user-pool"

  username_attributes      = ["email"]
  auto_verified_attributes = ["email"]

  username_configuration {
    case_sensitive = false
  }

  password_policy {
    minimum_length                   = 8
    require_lowercase                = true
    require_uppercase                = true
    require_numbers                  = true
    require_symbols                  = false
    temporary_password_validity_days = 7
  }

  mfa_configuration = "OPTIONAL"

  software_token_mfa_configuration {
    enabled = true
  }

  account_recovery_setting {
    recovery_mechanism {
      name     = "verified_email"
      priority = 1
    }
  }

  schema {
    name                = "email"
    attribute_data_type = "String"
    required            = true
    mutable             = true
  }

  schema {
    name                = "tenantId"
    attribute_data_type = "String"
    required            = false
    mutable             = false

    string_attribute_constraints {
      min_length = 1
      max_length = 256
    }
  }

  lifecycle {
    prevent_destroy = true  # Production safety
  }

  tags = {
    Environment = var.stage
  }
}

resource "aws_cognito_user_pool_client" "app" {
  name         = "${var.stage}-app-client"
  user_pool_id = aws_cognito_user_pool.main.id

  generate_secret = false

  explicit_auth_flows = [
    "ALLOW_USER_SRP_AUTH",
    "ALLOW_REFRESH_TOKEN_AUTH",
    "ALLOW_CUSTOM_AUTH",
  ]

  allowed_oauth_flows                  = ["code"]
  allowed_oauth_scopes                 = ["openid", "email", "profile"]
  allowed_oauth_flows_user_pool_client = true
  supported_identity_providers         = ["COGNITO"]

  callback_urls = ["https://yourdomain.com/callback"]
  logout_urls   = ["https://yourdomain.com/logout"]

  prevent_user_existence_errors = "ENABLED"

  id_token_validity      = 60  # minutes
  access_token_validity  = 60  # minutes
  refresh_token_validity = 30  # days

  token_validity_units {
    id_token      = "minutes"
    access_token  = "minutes"
    refresh_token = "days"
  }
}

resource "aws_cognito_user_pool_domain" "main" {
  domain       = "${var.stage}-myapp"
  user_pool_id = aws_cognito_user_pool.main.id
}

output "user_pool_id" {
  value = aws_cognito_user_pool.main.id
}

output "user_pool_client_id" {
  value = aws_cognito_user_pool_client.app.id
}
```

---

## Common Add-ons

### SES Email Configuration (CDK)

For production, replace Cognito's default email with SES:

```typescript
import * as ses from 'aws-cdk-lib/aws-ses';

const userPool = new cognito.UserPool(this, 'UserPool', {
  // ... other config
  email: cognito.UserPoolEmail.withSES({
    fromEmail: 'noreply@yourdomain.com',
    fromName: 'Your App',
    sesRegion: 'us-east-1', // SES must be in a supported region
    sesVerifiedDomain: 'yourdomain.com',
  }),
});
```

### Custom Domain with ACM Certificate (CDK)

```typescript
import * as acm from 'aws-cdk-lib/aws-certificatemanager';

// Certificate must be in us-east-1
const cert = acm.Certificate.fromCertificateArn(
  this, 'Cert',
  'arn:aws:acm:us-east-1:123456789:certificate/abc-123'
);

userPool.addDomain('CustomDomain', {
  customDomain: {
    domainName: 'auth.yourdomain.com',
    certificate: cert,
  },
});
```

### WAF Integration (CDK)

```typescript
import * as wafv2 from 'aws-cdk-lib/aws-wafv2';

const webAcl = new wafv2.CfnWebACL(this, 'CognitoWaf', {
  scope: 'REGIONAL',
  defaultAction: { allow: {} },
  rules: [
    {
      name: 'RateLimit',
      priority: 1,
      action: { block: {} },
      statement: {
        rateBasedStatement: {
          limit: 1000,
          aggregateKeyType: 'IP',
        },
      },
      visibilityConfig: {
        cloudWatchMetricsEnabled: true,
        metricName: 'CognitoRateLimit',
        sampledRequestsEnabled: true,
      },
    },
  ],
  visibilityConfig: {
    cloudWatchMetricsEnabled: true,
    metricName: 'CognitoWaf',
    sampledRequestsEnabled: true,
  },
});

new wafv2.CfnWebACLAssociation(this, 'WafAssociation', {
  resourceArn: userPool.userPoolArn,
  webAclArn: webAcl.attrArn,
});
```

### Cognito + API Gateway Authorizer (CDK)

```typescript
import * as apigateway from 'aws-cdk-lib/aws-apigateway';

const api = new apigateway.RestApi(this, 'Api');

const cognitoAuthorizer = new apigateway.CognitoUserPoolsAuthorizer(this, 'Authorizer', {
  cognitoUserPools: [userPool],
  identitySource: 'method.request.header.Authorization',
});

api.root.addResource('protected').addMethod('GET', integration, {
  authorizer: cognitoAuthorizer,
  authorizationType: apigateway.AuthorizationType.COGNITO,
  authorizationScopes: ['openid'], // Optional: require specific scopes
});
```
