# sso module

This module contains `10` endpoints in the `sso` domain.

## Endpoints

| Method | Path | Operation ID | Auth | Input | Required fields | Description |
|---|---|---|---|---|---|---|
| POST | `/sso.addTrustedOrigin` | `sso-addTrustedOrigin` | `apiKey` | `json` | body.origin | - |
| POST | `/sso.deleteProvider` | `sso-deleteProvider` | `apiKey` | `json` | body.providerId | - |
| GET | `/sso.getTrustedOrigins` | `sso-getTrustedOrigins` | `apiKey` | `none` | - | - |
| GET | `/sso.listProviders` | `sso-listProviders` | `apiKey` | `none` | - | - |
| GET | `/sso.one` | `sso-one` | `apiKey` | `params` | query.providerId | - |
| POST | `/sso.register` | `sso-register` | `apiKey` | `json` | body.providerId, body.issuer, body.domains | - |
| POST | `/sso.removeTrustedOrigin` | `sso-removeTrustedOrigin` | `apiKey` | `json` | body.origin | - |
| GET | `/sso.showSignInWithSSO` | `sso-showSignInWithSSO` | `apiKey` | `none` | - | - |
| POST | `/sso.update` | `sso-update` | `apiKey` | `json` | body.providerId, body.issuer, body.domains | - |
| POST | `/sso.updateTrustedOrigin` | `sso-updateTrustedOrigin` | `apiKey` | `json` | body.oldOrigin, body.newOrigin | - |

## Endpoint details

This section lists parameter and request-body fields for each operation.

### `sso-addTrustedOrigin`

- Method: `POST`
- Path: `/sso.addTrustedOrigin`
- Auth: `apiKey`
- Input: `json`

| Body field | Required | Type | Notes |
|---|---|---|---|
| `body.origin` | `required` | `string` | minLength=1 |

### `sso-deleteProvider`

- Method: `POST`
- Path: `/sso.deleteProvider`
- Auth: `apiKey`
- Input: `json`

| Body field | Required | Type | Notes |
|---|---|---|---|
| `body.providerId` | `required` | `string` | minLength=1 |

### `sso-getTrustedOrigins`

- Method: `GET`
- Path: `/sso.getTrustedOrigins`
- Auth: `apiKey`
- Input: `none`

No parameters or request body fields.

### `sso-listProviders`

- Method: `GET`
- Path: `/sso.listProviders`
- Auth: `apiKey`
- Input: `none`

No parameters or request body fields.

### `sso-one`

- Method: `GET`
- Path: `/sso.one`
- Auth: `apiKey`
- Input: `params`

| Param | In | Required | Type | Notes |
|---|---|---|---|---|
| `providerId` | `query` | yes | `string` | minLength=1 |

### `sso-register`

- Method: `POST`
- Path: `/sso.register`
- Auth: `apiKey`
- Input: `json`

| Body field | Required | Type | Notes |
|---|---|---|---|
| `body.providerId` | `required` | `string` | - |
| `body.issuer` | `required` | `string` | - |
| `body.domains` | `required` | `array<string>` | - |
| `body.domains[]` | `required` | `string` | - |
| `body.oidcConfig` | `optional` | `object` | - |
| `body.oidcConfig.clientId` | `required-if-body-present` | `string` | - |
| `body.oidcConfig.clientSecret` | `required-if-body-present` | `string` | - |
| `body.oidcConfig.authorizationEndpoint` | `optional` | `string` | - |
| `body.oidcConfig.tokenEndpoint` | `optional` | `string` | - |
| `body.oidcConfig.userInfoEndpoint` | `optional` | `string` | - |
| `body.oidcConfig.tokenEndpointAuthentication` | `optional` | `enum(client_secret_post, client_secret_basic)` | - |
| `body.oidcConfig.jwksEndpoint` | `optional` | `string` | - |
| `body.oidcConfig.discoveryEndpoint` | `optional` | `string` | - |
| `body.oidcConfig.skipDiscovery` | `optional` | `boolean` | - |
| `body.oidcConfig.scopes` | `optional` | `array<string>` | - |
| `body.oidcConfig.scopes[]` | `optional` | `string` | - |
| `body.oidcConfig.pkce` | `optional` | `boolean` | default=True |
| `body.oidcConfig.mapping` | `optional` | `object` | - |
| `body.oidcConfig.mapping.id` | `required-if-body-present` | `string` | - |
| `body.oidcConfig.mapping.email` | `required-if-body-present` | `string` | - |
| `body.oidcConfig.mapping.emailVerified` | `optional` | `string` | - |
| `body.oidcConfig.mapping.name` | `required-if-body-present` | `string` | - |
| `body.oidcConfig.mapping.image` | `optional` | `string` | - |
| `body.oidcConfig.mapping.extraFields` | `optional` | `object` | - |
| `body.samlConfig` | `optional` | `object` | - |
| `body.samlConfig.entryPoint` | `required-if-body-present` | `string` | - |
| `body.samlConfig.cert` | `required-if-body-present` | `string` | - |
| `body.samlConfig.callbackUrl` | `required-if-body-present` | `string` | - |
| `body.samlConfig.audience` | `optional` | `string` | - |
| `body.samlConfig.idpMetadata` | `optional` | `object` | - |
| `body.samlConfig.idpMetadata.metadata` | `optional` | `string` | - |
| `body.samlConfig.idpMetadata.entityID` | `optional` | `string` | - |
| `body.samlConfig.idpMetadata.cert` | `optional` | `string` | - |
| `body.samlConfig.idpMetadata.privateKey` | `optional` | `string` | - |
| `body.samlConfig.idpMetadata.privateKeyPass` | `optional` | `string` | - |
| `body.samlConfig.idpMetadata.isAssertionEncrypted` | `optional` | `boolean` | - |
| `body.samlConfig.idpMetadata.encPrivateKey` | `optional` | `string` | - |
| `body.samlConfig.idpMetadata.encPrivateKeyPass` | `optional` | `string` | - |
| `body.samlConfig.idpMetadata.singleSignOnService` | `optional` | `array<object>` | - |
| `body.samlConfig.idpMetadata.singleSignOnService[].Binding` | `required-if-body-present` | `string` | - |
| `body.samlConfig.idpMetadata.singleSignOnService[].Location` | `required-if-body-present` | `string` | - |
| `body.samlConfig.spMetadata` | `required-if-body-present` | `object` | - |
| `body.samlConfig.spMetadata.metadata` | `optional` | `string` | - |
| `body.samlConfig.spMetadata.entityID` | `optional` | `string` | - |
| `body.samlConfig.spMetadata.binding` | `optional` | `string` | - |
| `body.samlConfig.spMetadata.privateKey` | `optional` | `string` | - |
| `body.samlConfig.spMetadata.privateKeyPass` | `optional` | `string` | - |
| `body.samlConfig.spMetadata.isAssertionEncrypted` | `optional` | `boolean` | - |
| `body.samlConfig.spMetadata.encPrivateKey` | `optional` | `string` | - |
| `body.samlConfig.spMetadata.encPrivateKeyPass` | `optional` | `string` | - |
| `body.samlConfig.wantAssertionsSigned` | `optional` | `boolean` | - |
| `body.samlConfig.authnRequestsSigned` | `optional` | `boolean` | - |
| `body.samlConfig.signatureAlgorithm` | `optional` | `string` | - |
| `body.samlConfig.digestAlgorithm` | `optional` | `string` | - |
| `body.samlConfig.identifierFormat` | `optional` | `string` | - |
| `body.samlConfig.privateKey` | `optional` | `string` | - |
| `body.samlConfig.decryptionPvk` | `optional` | `string` | - |
| `body.samlConfig.additionalParams` | `optional` | `object` | - |
| `body.samlConfig.mapping` | `optional` | `object` | - |
| `body.samlConfig.mapping.id` | `required-if-body-present` | `string` | - |
| `body.samlConfig.mapping.email` | `required-if-body-present` | `string` | - |
| `body.samlConfig.mapping.emailVerified` | `optional` | `string` | - |
| `body.samlConfig.mapping.name` | `required-if-body-present` | `string` | - |
| `body.samlConfig.mapping.firstName` | `optional` | `string` | - |
| `body.samlConfig.mapping.lastName` | `optional` | `string` | - |
| `body.samlConfig.mapping.extraFields` | `optional` | `object` | - |
| `body.organizationId` | `optional` | `string` | - |
| `body.overrideUserInfo` | `optional` | `boolean` | default=False |

### `sso-removeTrustedOrigin`

- Method: `POST`
- Path: `/sso.removeTrustedOrigin`
- Auth: `apiKey`
- Input: `json`

| Body field | Required | Type | Notes |
|---|---|---|---|
| `body.origin` | `required` | `string` | minLength=1 |

### `sso-showSignInWithSSO`

- Method: `GET`
- Path: `/sso.showSignInWithSSO`
- Auth: `apiKey`
- Input: `none`

No parameters or request body fields.

### `sso-update`

- Method: `POST`
- Path: `/sso.update`
- Auth: `apiKey`
- Input: `json`

| Body field | Required | Type | Notes |
|---|---|---|---|
| `body.providerId` | `required` | `string` | - |
| `body.issuer` | `required` | `string` | - |
| `body.domains` | `required` | `array<string>` | - |
| `body.domains[]` | `required` | `string` | - |
| `body.oidcConfig` | `optional` | `object` | - |
| `body.oidcConfig.clientId` | `required-if-body-present` | `string` | - |
| `body.oidcConfig.clientSecret` | `required-if-body-present` | `string` | - |
| `body.oidcConfig.authorizationEndpoint` | `optional` | `string` | - |
| `body.oidcConfig.tokenEndpoint` | `optional` | `string` | - |
| `body.oidcConfig.userInfoEndpoint` | `optional` | `string` | - |
| `body.oidcConfig.tokenEndpointAuthentication` | `optional` | `enum(client_secret_post, client_secret_basic)` | - |
| `body.oidcConfig.jwksEndpoint` | `optional` | `string` | - |
| `body.oidcConfig.discoveryEndpoint` | `optional` | `string` | - |
| `body.oidcConfig.skipDiscovery` | `optional` | `boolean` | - |
| `body.oidcConfig.scopes` | `optional` | `array<string>` | - |
| `body.oidcConfig.scopes[]` | `optional` | `string` | - |
| `body.oidcConfig.pkce` | `optional` | `boolean` | default=True |
| `body.oidcConfig.mapping` | `optional` | `object` | - |
| `body.oidcConfig.mapping.id` | `required-if-body-present` | `string` | - |
| `body.oidcConfig.mapping.email` | `required-if-body-present` | `string` | - |
| `body.oidcConfig.mapping.emailVerified` | `optional` | `string` | - |
| `body.oidcConfig.mapping.name` | `required-if-body-present` | `string` | - |
| `body.oidcConfig.mapping.image` | `optional` | `string` | - |
| `body.oidcConfig.mapping.extraFields` | `optional` | `object` | - |
| `body.samlConfig` | `optional` | `object` | - |
| `body.samlConfig.entryPoint` | `required-if-body-present` | `string` | - |
| `body.samlConfig.cert` | `required-if-body-present` | `string` | - |
| `body.samlConfig.callbackUrl` | `required-if-body-present` | `string` | - |
| `body.samlConfig.audience` | `optional` | `string` | - |
| `body.samlConfig.idpMetadata` | `optional` | `object` | - |
| `body.samlConfig.idpMetadata.metadata` | `optional` | `string` | - |
| `body.samlConfig.idpMetadata.entityID` | `optional` | `string` | - |
| `body.samlConfig.idpMetadata.cert` | `optional` | `string` | - |
| `body.samlConfig.idpMetadata.privateKey` | `optional` | `string` | - |
| `body.samlConfig.idpMetadata.privateKeyPass` | `optional` | `string` | - |
| `body.samlConfig.idpMetadata.isAssertionEncrypted` | `optional` | `boolean` | - |
| `body.samlConfig.idpMetadata.encPrivateKey` | `optional` | `string` | - |
| `body.samlConfig.idpMetadata.encPrivateKeyPass` | `optional` | `string` | - |
| `body.samlConfig.idpMetadata.singleSignOnService` | `optional` | `array<object>` | - |
| `body.samlConfig.idpMetadata.singleSignOnService[].Binding` | `required-if-body-present` | `string` | - |
| `body.samlConfig.idpMetadata.singleSignOnService[].Location` | `required-if-body-present` | `string` | - |
| `body.samlConfig.spMetadata` | `required-if-body-present` | `object` | - |
| `body.samlConfig.spMetadata.metadata` | `optional` | `string` | - |
| `body.samlConfig.spMetadata.entityID` | `optional` | `string` | - |
| `body.samlConfig.spMetadata.binding` | `optional` | `string` | - |
| `body.samlConfig.spMetadata.privateKey` | `optional` | `string` | - |
| `body.samlConfig.spMetadata.privateKeyPass` | `optional` | `string` | - |
| `body.samlConfig.spMetadata.isAssertionEncrypted` | `optional` | `boolean` | - |
| `body.samlConfig.spMetadata.encPrivateKey` | `optional` | `string` | - |
| `body.samlConfig.spMetadata.encPrivateKeyPass` | `optional` | `string` | - |
| `body.samlConfig.wantAssertionsSigned` | `optional` | `boolean` | - |
| `body.samlConfig.authnRequestsSigned` | `optional` | `boolean` | - |
| `body.samlConfig.signatureAlgorithm` | `optional` | `string` | - |
| `body.samlConfig.digestAlgorithm` | `optional` | `string` | - |
| `body.samlConfig.identifierFormat` | `optional` | `string` | - |
| `body.samlConfig.privateKey` | `optional` | `string` | - |
| `body.samlConfig.decryptionPvk` | `optional` | `string` | - |
| `body.samlConfig.additionalParams` | `optional` | `object` | - |
| `body.samlConfig.mapping` | `optional` | `object` | - |
| `body.samlConfig.mapping.id` | `required-if-body-present` | `string` | - |
| `body.samlConfig.mapping.email` | `required-if-body-present` | `string` | - |
| `body.samlConfig.mapping.emailVerified` | `optional` | `string` | - |
| `body.samlConfig.mapping.name` | `required-if-body-present` | `string` | - |
| `body.samlConfig.mapping.firstName` | `optional` | `string` | - |
| `body.samlConfig.mapping.lastName` | `optional` | `string` | - |
| `body.samlConfig.mapping.extraFields` | `optional` | `object` | - |
| `body.organizationId` | `optional` | `string` | - |
| `body.overrideUserInfo` | `optional` | `boolean` | default=False |

### `sso-updateTrustedOrigin`

- Method: `POST`
- Path: `/sso.updateTrustedOrigin`
- Auth: `apiKey`
- Input: `json`

| Body field | Required | Type | Notes |
|---|---|---|---|
| `body.oldOrigin` | `required` | `string` | minLength=1 |
| `body.newOrigin` | `required` | `string` | minLength=1 |

## Invocation template

```bash
curl -X POST \
  "https://dokploy.example.com/api<endpoint>" \
  -H "Content-Type: application/json" \
  -H "x-api-key: $DOKPLOY_API_KEY" \
  -d '{"key":"value"}'
```
