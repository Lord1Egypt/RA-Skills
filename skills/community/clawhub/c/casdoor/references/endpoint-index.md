# Endpoint Index

Use this file first when you need to find the closest Casdoor endpoint for a task.

## Account API

- `POST /api/add-ldap` — add ldap (params: body:body)
- `POST /api/delete-ldap` — delete ldap (params: body:body)
- `GET /api/get-account` — get the details of the current account
- `GET /api/get-ldap` — get ldap (params: id:query)
- `GET /api/get-ldap-users` — get ldap users
- `GET /api/get-ldaps` — get ldaps (params: owner:query)
- `POST /api/reset-email-or-phone` — ApiController.ResetEmailOrPhone
- `POST /api/set-password` — set password (params: userOwner:formData, userName:formData, oldPassword:formData, ...)
- `POST /api/sync-ldap-users` — sync ldap users (params: id:query)
- `POST /api/update-ldap` — update ldap (params: body:body)
- `GET /api/user` — return Laravel compatible user information according to OAuth 2.0
- `GET /api/userinfo` — return user information according to OIDC standards

## Adapter API

- `POST /api/add-adapter` — add adapter (params: body:body)
- `POST /api/delete-adapter` — delete adapter (params: body:body)
- `GET /api/get-adapter` — get adapter (params: id:query)
- `GET /api/get-adapters` — get adapters (params: owner:query)
- `POST /api/update-adapter` — update adapter (params: id:query, body:body)

## Application API

- `POST /api/add-application` — add an application (params: body:body)
- `POST /api/delete-application` — delete an application (params: body:body)
- `GET /api/get-application` — get the detail of an application (params: id:query)
- `GET /api/get-applications` — get all applications (params: owner:query)
- `GET /api/get-organization-applications` — get the detail of the organization's application (params: organization:query)
- `GET /api/get-user-application` — get the detail of the user's application (params: id:query)
- `POST /api/update-application` — update an application (params: id:query, body:body)

## CLI API

- `POST /api/refresh-engines` — Refresh all CLI engines (params: m:query, t:query)

## Callback API

- `POST /api/Callback` — Get Login Error Counts

## Cert API

- `POST /api/add-cert` — add cert (params: body:body)
- `POST /api/delete-cert` — delete cert (params: body:body)
- `GET /api/get-cert` — get cert (params: id:query)
- `GET /api/get-certs` — get certs (params: owner:query)
- `GET /api/get-global-certs` — get global certs
- `POST /api/update-cert` — update cert (params: id:query, body:body)

## Device Authorization Endpoint

- `POST /api/device-auth` — Endpoint for the device authorization flow

## Enforcer API

- `POST /api/add-enforcer` — add enforcer (params: enforcer:body)
- `POST /api/add-policy` — add policy (params: id:query, body:body)
- `POST /api/batch-enforce` — Call Casbin BatchEnforce API (params: body:body, permissionId:query, modelId:query, ...)
- `POST /api/delete-enforcer` — delete enforcer (params: body:body)
- `POST /api/enforce` — Call Casbin Enforce API (params: body:body, permissionId:query, modelId:query, ...)
- `GET /api/get-all-actions` — Get all actions for a user (Casbin API) (params: userId:query)
- `GET /api/get-all-objects` — Get all objects for a user (Casbin API) (params: userId:query)
- `GET /api/get-all-roles` — Get all roles for a user (Casbin API) (params: userId:query)
- `GET /api/get-enforcer` — get enforcer (params: id:query)
- `GET /api/get-enforcers` — get enforcers (params: owner:query)
- `POST /api/get-filtered-policies` — get filtered policies with support for multiple filters via POST body (params: id:query, body:body)
- `GET /api/get-policies` — get policies (params: id:query, adapterId:query)
- `POST /api/remove-policy` — remove policy (params: id:query, body:body)
- `GET /api/run-casbin-command` — Call Casbin CLI commands
- `POST /api/update-enforcer` — update enforcer (params: id:query, enforcer:body)
- `POST /api/update-policy` — update policy (params: id:query, body:body)

## Form API

- `POST /api/add-form` — add form (params: body:body)
- `POST /api/delete-form` — delete form (params: body:body)
- `GET /api/get-form` — get form (params: id:query)
- `GET /api/get-forms` — get forms (params: owner:query)
- `GET /api/get-global-forms` — get global forms
- `POST /api/update-form` — update form (params: id:query, body:body)

## Group API

- `POST /api/add-group` — add group (params: body:body)
- `POST /api/delete-group` — delete group (params: body:body)
- `GET /api/get-group` — get group (params: id:query)
- `GET /api/get-groups` — get groups (params: owner:query)
- `POST /api/update-group` — update group (params: id:query, body:body)

## Invitation API

- `POST /api/add-invitation` — add invitation (params: body:body)
- `POST /api/delete-invitation` — delete invitation (params: body:body)
- `GET /api/get-invitation` — get invitation (params: id:query)
- `GET /api/get-invitation-info` — get invitation code information (params: code:query)
- `GET /api/get-invitations` — get invitations (params: owner:query)
- `POST /api/send-invitation` — verify invitation (params: id:query, body:body)
- `POST /api/update-invitation` — update invitation (params: id:query, body:body)
- `GET /api/verify-invitation` — verify invitation (params: id:query)

## Login API

- `GET /api/faceid-signin-begin` — FaceId Login Flow 1st stage (params: owner:query, name:query)
- `GET /api/get-app-login` — get application login (params: clientId:query, responseType:query, redirectUri:query, ...)
- `GET /api/get-captcha` — ApiController.GetCaptcha
- `POST /api/login` — login (params: clientId:query, responseType:query, redirectUri:query, ...)
- `POST /api/login/oauth/introspect` — The introspection endpoint is an OAuth 2.0 endpoint that takes a (params: token:formData, token_type_hint:formData)
- `POST /api/logout` — logout the current user (params: id_token_hint:query, post_logout_redirect_uri:query, state:query)
- `POST /api/signup` — sign up a new user (params: username:formData, password:formData)
- `GET /api/sso-logout` — logout the current user from all applications or current session only (params: logoutAll:query)
- `POST /api/sso-logout` — logout the current user from all applications or current session only (params: logoutAll:query)
- `POST /api/unlink` — ApiController.Unlink
- `GET /api/webauthn/signin/begin` — WebAuthn Login Flow 1st stage (params: owner:query, name:query)
- `POST /api/webauthn/signin/finish` — WebAuthn Login Flow 2nd stage (params: body:body)

## MFA API

- `POST /api/delete-mfa/` — : Delete MFA
- `POST /api/mfa/setup/enable` — enable totp
- `POST /api/mfa/setup/initiate` — setup MFA
- `POST /api/mfa/setup/verify` — setup verify totp
- `POST /api/set-preferred-mfa` — : Set specific Mfa Preferred

## Model API

- `POST /api/add-model` — add model (params: body:body)
- `POST /api/delete-model` — delete model (params: body:body)
- `GET /api/get-model` — get model (params: id:query)
- `GET /api/get-models` — get models (params: owner:query)
- `POST /api/update-model` — update model (params: id:query, body:body)

## OIDC API

- `GET /.well-known/jwks` — RootController.GetJwks
- `GET /.well-known/openid-configuration` — Get Oidc Discovery
- `GET /.well-known/webfinger` — RootController.GetWebFinger (params: resource:query)
- `GET /.well-known/{application}/jwks` — RootController.GetJwksByApplication (params: application:path)
- `GET /.well-known/{application}/openid-configuration` — Get Oidc Discovery for specific application (params: application:path)
- `GET /.well-known/{application}/webfinger` — RootController.GetWebFingerByApplication (params: application:path, resource:query)

## Order API

- `POST /api/add-order` — add order (params: body:body)
- `POST /api/cancel-order` — cancel an order (params: id:query)
- `POST /api/delete-order` — delete order (params: body:body)
- `GET /api/get-order` — get order (params: id:query)
- `GET /api/get-orders` — get orders (params: owner:query)
- `GET /api/get-user-orders` — get orders for a user (params: owner:query, user:query)
- `POST /api/pay-order` — pay an existing order (params: id:query, providerName:query)
- `POST /api/place-order` — place an order for a product (params: productId:query, pricingName:query, planName:query, ...)
- `POST /api/update-order` — update order (params: id:query, body:body)

## Organization API

- `POST /api/add-organization` — add organization (params: body:body)
- `POST /api/delete-organization` — delete organization (params: body:body)
- `GET /api/get-default-application` — get default application (params: id:query)
- `GET /api/get-organization` — get organization (params: id:query)
- `GET /api/get-organization-names` — get all organization name and displayName (params: owner:query)
- `GET /api/get-organizations` — get organizations (params: owner:query)
- `POST /api/update-organization` — update organization (params: id:query, body:body)

## Payment API

- `POST /api/add-payment` — add payment (params: body:body)
- `POST /api/delete-payment` — delete payment (params: body:body)
- `POST /api/invoice-payment` — invoice payment (params: id:query)
- `POST /api/notify-payment` — notify payment (params: body:body)
- `POST /api/update-payment` — update payment (params: id:query, body:body)

## Permission API

- `POST /api/add-permission` — add permission (params: body:body)
- `POST /api/delete-permission` — delete permission (params: body:body)
- `GET /api/get-permission` — get permission (params: id:query)
- `GET /api/get-permissions` — get permissions (params: owner:query)
- `GET /api/get-permissions-by-role` — get permissions by role (params: id:query)
- `GET /api/get-permissions-by-submitter` — get permissions by submitter
- `POST /api/update-permission` — update permission (params: id:query, body:body)

## Plan API

- `POST /api/add-plan` — add plan (params: body:body)
- `POST /api/delete-plan` — delete plan (params: body:body)
- `GET /api/get-plan` — get plan (params: id:query, includeOption:query)
- `GET /api/get-plans` — get plans (params: owner:query)
- `POST /api/update-plan` — update plan (params: id:query, body:body)

## Pricing API

- `POST /api/add-pricing` — add pricing (params: body:body)
- `POST /api/delete-pricing` — delete pricing (params: body:body)
- `GET /api/get-pricing` — get pricing (params: id:query)
- `GET /api/get-pricings` — get pricings (params: owner:query)
- `POST /api/update-pricing` — update pricing (params: id:query, body:body)

## Product API

- `POST /api/add-product` — add product (params: body:body)
- `POST /api/delete-product` — delete product (params: body:body)
- `GET /api/get-product` — get product (params: id:query)
- `GET /api/get-products` — get products (params: owner:query)
- `POST /api/update-product` — update product (params: id:query, body:body)

## Provider API

- `POST /api/add-provider` — add provider (params: body:body)
- `POST /api/delete-provider` — delete provider (params: body:body)
- `GET /api/get-global-providers` — get Global providers
- `GET /api/get-provider` — get provider (params: id:query)
- `GET /api/get-providers` — get providers (params: owner:query)
- `POST /api/update-provider` — update provider (params: id:query, body:body)

## Record API

- `POST /api/add-record` — add a record (params: body:body)
- `GET /api/get-records` — get all records (params: pageSize:query, p:query)
- `POST /api/get-records-filter` — get records by filter (params: filter:body)

## Resource API

- `POST /api/add-resource` — ApiController.AddResource (params: resource:body)
- `POST /api/delete-resource` — ApiController.DeleteResource (params: resource:body)
- `GET /api/get-resource` — get resource (params: id:query)
- `GET /api/get-resources` — get resources (params: owner:query, user:query, pageSize:query, ...)
- `POST /api/update-resource` — get resource (params: id:query, resource:body)
- `POST /api/upload-resource` — ApiController.UploadResource (params: owner:query, user:query, application:query, ...)

## Role API

- `POST /api/add-role` — add role (params: body:body)
- `POST /api/delete-role` — delete role (params: body:body)
- `GET /api/get-role` — get role (params: id:query)
- `GET /api/get-roles` — get roles (params: owner:query)
- `POST /api/update-role` — update role (params: id:query, body:body)

## Service API

- `POST /api/send-email` — This API is not for Casdoor frontend to call, it is for Casdoor SDKs. (params: clientId:query, clientSecret:query, from:body)
- `POST /api/send-notification` — This API is not for Casdoor frontend to call, it is for Casdoor SDKs. (params: from:body)
- `POST /api/send-sms` — This API is not for Casdoor frontend to call, it is for Casdoor SDKs. (params: clientId:query, clientSecret:query, from:body)

## Session API

- `POST /api/add-session` — Add session for one user in one application. If there are other existing sessions, join the session into the list. (params: body:body)
- `POST /api/delete-session` — Delete session for one user in one application. (params: body:body)
- `GET /api/get-session` — Get session for one user in one application. (params: sessionPkId:query)
- `GET /api/get-sessions` — Get organization user sessions. (params: owner:query)
- `GET /api/is-session-duplicated` — Check if there are other different sessions for one user in one application. (params: sessionPkId:query, sessionId:query)
- `POST /api/update-session` — Update session for one user in one application. (params: body:body)

## Subscription API

- `POST /api/add-subscription` — add subscription (params: body:body)
- `POST /api/delete-subscription` — delete subscription (params: body:body)
- `GET /api/get-subscription` — get subscription (params: id:query)
- `GET /api/get-subscriptions` — get subscriptions (params: owner:query)
- `POST /api/update-subscription` — update subscription (params: id:query, body:body)

## Syncer API

- `POST /api/add-syncer` — add syncer (params: body:body)
- `POST /api/delete-syncer` — delete syncer (params: body:body)
- `GET /api/get-syncer` — get syncer (params: id:query)
- `GET /api/get-syncers` — get syncers (params: owner:query)
- `GET /api/run-syncer` — run syncer (params: body:body)
- `POST /api/update-syncer` — update syncer (params: id:query, body:body)

## System API

- `GET /api/get-dashboard` — get information of dashboard
- `GET /api/get-prometheus-info` — get Prometheus Info
- `GET /api/get-qrcode` — ApiController.GetWechatQRCode (params: id:query)
- `GET /api/get-system-info` — get system info like CPU and memory usage
- `GET /api/get-version-info` — get version info like Casdoor release version and commit ID
- `GET /api/get-webhook-event` — ApiController.GetWebhookEventType (params: ticket:query)
- `GET /api/health` — check if the system is live
- `GET /api/metrics` — get Prometheus metrics
- `POST /api/webhook` — ApiController.HandleOfficialAccountEvent

## Ticket API

- `POST /api/add-ticket` — add ticket (params: body:body)
- `POST /api/add-ticket-message` — add a message to a ticket (params: id:query, body:body)
- `POST /api/delete-ticket` — delete ticket (params: body:body)
- `GET /api/get-ticket` — get ticket (params: id:query)
- `GET /api/get-tickets` — get tickets (params: owner:query)
- `POST /api/update-ticket` — update ticket (params: id:query, body:body)

## Token API

- `POST /api/add-token` — add token (params: body:body)
- `POST /api/delete-token` — delete token (params: body:body)
- `GET /api/get-captcha-status` — Get Login Error Counts (params: id:query)
- `GET /api/get-token` — get token (params: id:query)
- `GET /api/get-tokens` — get tokens (params: owner:query, pageSize:query, p:query)
- `POST /api/login/oauth/access_token` — get OAuth access token (params: grant_type:query, client_id:query, client_secret:query, ...)
- `POST /api/login/oauth/refresh_token` — refresh OAuth access token (params: grant_type:query, refresh_token:query, scope:query, ...)
- `POST /api/update-token` — update token (params: id:query, body:body)

## Transaction API

- `POST /api/add-transaction` — add transaction (params: body:body, dryRun:query)
- `POST /api/delete-transaction` — delete transaction (params: body:body)
- `GET /api/get-transaction` — get transaction (params: id:query)
- `GET /api/get-transactions` — get transactions (params: owner:query)
- `POST /api/update-transaction` — update transaction (params: id:query, body:body)

## User API

- `POST /api/add-user` — add user (params: body:body)
- `POST /api/add-user-keys` — ApiController.AddUserKeys
- `POST /api/check-user-password` — ApiController.CheckUserPassword
- `POST /api/delete-user` — delete user (params: body:body)
- `POST /api/exit-impersonation-user` — clear impersonation info for current session
- `GET /api/get-email-and-phone` — get email and phone by username (params: username:formData, organization:formData)
- `GET /api/get-global-users` — get global users
- `GET /api/get-sorted-users` — ApiController.GetSortedUsers (params: owner:query, sorter:query, limit:query)
- `GET /api/get-user` — get user (params: id:query, owner:query, email:query, ...)
- `GET /api/get-user-count` — ApiController.GetUserCount (params: owner:query, isOnline:query)
- `GET /api/get-users` — ApiController.GetUsers (params: owner:query)
- `POST /api/impersonation-user` — set impersonation user for current admin session (params: username:formData)
- `POST /api/update-user` — update user (params: id:query, userId:query, owner:query, ...)
- `POST /api/verify-identification` — verify user's real identity using ID Verification provider (params: owner:query, name:query, provider:query)
- `GET /api/webauthn/signup/begin` — WebAuthn Registration Flow 1st stage
- `POST /api/webauthn/signup/finish` — WebAuthn Registration Flow 2nd stage (params: body:body)

## Verification API

- `GET /api/get-payment` — get payment (params: id:query)
- `GET /api/get-payments` — get payments (params: owner:query)
- `GET /api/get-user-payments` — get payments for a user (params: owner:query, organization:query, user:query)
- `POST /api/send-verification-code` — ApiController.SendVerificationCode
- `POST /api/verify-captcha` — ApiController.VerifyCaptcha
- `POST /api/verify-code` — ApiController.VerifyCode

## Webhook API

- `POST /api/add-webhook` — add webhook (params: body:body)
- `POST /api/delete-webhook` — delete webhook (params: body:body)
- `GET /api/get-webhook` — get webhook (params: id:query)
- `GET /api/get-webhooks` — get webhooks (params: owner:query)
- `POST /api/update-webhook` — update webhook (params: id:query, body:body)
