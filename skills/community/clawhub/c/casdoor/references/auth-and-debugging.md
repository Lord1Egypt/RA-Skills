# Auth And Debugging

Use this checklist when a Casdoor request fails or when authentication expectations are unclear.

## Debugging Flow

1. Verify the endpoint path and HTTP method from `references/endpoint-index.md`.
2. Verify every required path, query, and body parameter.
3. Verify whether the request should include an access token, cookie, or no auth at all.
4. Compare the caller's request shape with the generated curl or code example.
5. Inspect the response code and map it to the most likely root cause.

## Common Failure Patterns

- `400 Bad Request`: missing required query or body fields, malformed JSON, or wrong parameter type.
- `401 Unauthorized`: missing token, invalid token, wrong issuer, or expired login state.
- `403 Forbidden`: valid identity but insufficient permission or wrong tenant/application scope.
- `404 Not Found`: wrong path, wrong path parameter, or endpoint unavailable on that deployment version.
- `500 Internal Server Error`: server-side issue; confirm the request shape first, then inspect Casdoor logs.

## OIDC Checks

- Confirm the discovery endpoint for the correct application when app-specific OIDC is involved.
- Confirm JWKS and discovery URLs match the same host and deployment environment.
- For issuer validation errors, compare the issuer from discovery with the token's `iss` claim.

## Known Discovery Paths

- `/.well-known/jwks`
- `/.well-known/openid-configuration`
- `/.well-known/webfinger`
- `/.well-known/{application}/jwks`
- `/.well-known/{application}/openid-configuration`

## Reporting Pattern

- State the most likely root cause.
- State the exact parameter or header that should be checked next.
- If Swagger does not prove the auth mode, label that as a deployment-specific assumption.
