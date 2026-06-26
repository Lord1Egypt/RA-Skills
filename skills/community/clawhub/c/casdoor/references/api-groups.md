# API Groups

Use this file when the user describes a business task but does not know which endpoint family fits it.

## Account API

- Endpoint count: 12
- Typical paths: /api/add-ldap, /api/delete-ldap, /api/get-account
- Use this group when the request matches the `Account API` feature family.

## Adapter API

- Endpoint count: 5
- Typical paths: /api/add-adapter, /api/delete-adapter, /api/get-adapter
- Use this group when the request matches the `Adapter API` feature family.

## Application API

- Endpoint count: 7
- Typical paths: /api/add-application, /api/delete-application, /api/get-application
- Use this group when the request matches application settings, OIDC app behavior, and client-specific configuration.

## CLI API

- Endpoint count: 1
- Typical paths: /api/refresh-engines
- Use this group when the request matches the `CLI API` feature family.

## Callback API

- Endpoint count: 1
- Typical paths: /api/Callback
- Use this group when the request matches the `Callback API` feature family.

## Cert API

- Endpoint count: 6
- Typical paths: /api/add-cert, /api/delete-cert, /api/get-cert
- Use this group when the request matches the `Cert API` feature family.

## Device Authorization Endpoint

- Endpoint count: 1
- Typical paths: /api/device-auth
- Use this group when the request matches the `Device Authorization Endpoint` feature family.

## Enforcer API

- Endpoint count: 16
- Typical paths: /api/add-enforcer, /api/add-policy, /api/batch-enforce
- Use this group when the request matches the `Enforcer API` feature family.

## Form API

- Endpoint count: 6
- Typical paths: /api/add-form, /api/delete-form, /api/get-form
- Use this group when the request matches the `Form API` feature family.

## Group API

- Endpoint count: 5
- Typical paths: /api/add-group, /api/delete-group, /api/get-group
- Use this group when the request matches the `Group API` feature family.

## Invitation API

- Endpoint count: 8
- Typical paths: /api/add-invitation, /api/delete-invitation, /api/get-invitation
- Use this group when the request matches the `Invitation API` feature family.

## Login API

- Endpoint count: 12
- Typical paths: /api/faceid-signin-begin, /api/get-app-login, /api/get-captcha
- Use this group when the request matches the `Login API` feature family.

## MFA API

- Endpoint count: 5
- Typical paths: /api/delete-mfa/, /api/mfa/setup/enable, /api/mfa/setup/initiate
- Use this group when the request matches the `MFA API` feature family.

## Model API

- Endpoint count: 5
- Typical paths: /api/add-model, /api/delete-model, /api/get-model
- Use this group when the request matches the `Model API` feature family.

## OIDC API

- Endpoint count: 6
- Typical paths: /.well-known/jwks, /.well-known/openid-configuration, /.well-known/webfinger
- Use this group when the request matches OIDC discovery, JWKS, issuer metadata, and related identity bootstrap tasks.

## Order API

- Endpoint count: 9
- Typical paths: /api/add-order, /api/cancel-order, /api/delete-order
- Use this group when the request matches the `Order API` feature family.

## Organization API

- Endpoint count: 7
- Typical paths: /api/add-organization, /api/delete-organization, /api/get-default-application
- Use this group when the request matches organization scope, tenants, and ownership boundaries.

## Payment API

- Endpoint count: 5
- Typical paths: /api/add-payment, /api/delete-payment, /api/invoice-payment
- Use this group when the request matches the `Payment API` feature family.

## Permission API

- Endpoint count: 7
- Typical paths: /api/add-permission, /api/delete-permission, /api/get-permission
- Use this group when the request matches the `Permission API` feature family.

## Plan API

- Endpoint count: 5
- Typical paths: /api/add-plan, /api/delete-plan, /api/get-plan
- Use this group when the request matches the `Plan API` feature family.

## Pricing API

- Endpoint count: 5
- Typical paths: /api/add-pricing, /api/delete-pricing, /api/get-pricing
- Use this group when the request matches the `Pricing API` feature family.

## Product API

- Endpoint count: 5
- Typical paths: /api/add-product, /api/delete-product, /api/get-product
- Use this group when the request matches the `Product API` feature family.

## Provider API

- Endpoint count: 6
- Typical paths: /api/add-provider, /api/delete-provider, /api/get-global-providers
- Use this group when the request matches external identity providers or federation integration tasks.

## Record API

- Endpoint count: 3
- Typical paths: /api/add-record, /api/get-records, /api/get-records-filter
- Use this group when the request matches the `Record API` feature family.

## Resource API

- Endpoint count: 6
- Typical paths: /api/add-resource, /api/delete-resource, /api/get-resource
- Use this group when the request matches the `Resource API` feature family.

## Role API

- Endpoint count: 5
- Typical paths: /api/add-role, /api/delete-role, /api/get-role
- Use this group when the request matches the `Role API` feature family.

## Service API

- Endpoint count: 3
- Typical paths: /api/send-email, /api/send-notification, /api/send-sms
- Use this group when the request matches the `Service API` feature family.

## Session API

- Endpoint count: 6
- Typical paths: /api/add-session, /api/delete-session, /api/get-session
- Use this group when the request matches the `Session API` feature family.

## Subscription API

- Endpoint count: 5
- Typical paths: /api/add-subscription, /api/delete-subscription, /api/get-subscription
- Use this group when the request matches the `Subscription API` feature family.

## Syncer API

- Endpoint count: 6
- Typical paths: /api/add-syncer, /api/delete-syncer, /api/get-syncer
- Use this group when the request matches the `Syncer API` feature family.

## System API

- Endpoint count: 9
- Typical paths: /api/get-dashboard, /api/get-prometheus-info, /api/get-qrcode
- Use this group when the request matches the `System API` feature family.

## Ticket API

- Endpoint count: 6
- Typical paths: /api/add-ticket, /api/add-ticket-message, /api/delete-ticket
- Use this group when the request matches the `Ticket API` feature family.

## Token API

- Endpoint count: 8
- Typical paths: /api/add-token, /api/delete-token, /api/get-captcha-status
- Use this group when the request matches the `Token API` feature family.

## Transaction API

- Endpoint count: 5
- Typical paths: /api/add-transaction, /api/delete-transaction, /api/get-transaction
- Use this group when the request matches the `Transaction API` feature family.

## User API

- Endpoint count: 16
- Typical paths: /api/add-user, /api/add-user-keys, /api/check-user-password
- Use this group when the request matches user lookup, lifecycle management, and account-related operations.

## Verification API

- Endpoint count: 6
- Typical paths: /api/get-payment, /api/get-payments, /api/get-user-payments
- Use this group when the request matches the `Verification API` feature family.

## Webhook API

- Endpoint count: 5
- Typical paths: /api/add-webhook, /api/delete-webhook, /api/get-webhook
- Use this group when the request matches the `Webhook API` feature family.
