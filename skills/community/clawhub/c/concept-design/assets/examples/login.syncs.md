# app ExternalLogin
include Web
include OAuthAuthentication [Credential]
include ExternalIdentity
include Profile [ExternalIdentity.Identity]
include Session [ExternalIdentity.Identity]

### Verify login credentials
sync VerifyLogin
when { Web/login: [credential: ?credential] => [request: ?request] }
then { OAuthAuthentication/verify: [credential: ?credential] }

### Record the verified external identity
sync RecordVerifiedIdentity
when {
  OAuthAuthentication/verify: []
    => [valid: true; namespace: ?namespace; subject: ?subject]
}
then { ExternalIdentity/record: [namespace: ?namespace; subject: ?subject] }

### Set the profile and create a session
sync PrepareLogin
when {
  OAuthAuthentication/verify: [] => [valid: true; displayName: ?displayName]
  ExternalIdentity/record: [] => [identity: ?identity]
}
then {
  Profile/set: [identity: ?identity; displayName: ?displayName]
  Session/open: [identity: ?identity]
}

### Join completions and read response data
sync CompleteLogin
when {
  Web/login: [] => [request: ?request]
  Profile/set: [identity: ?identity] => [identity: ?identity]
  Session/open: [identity: ?identity] => [session: ?session]
}
where {
  Profile: { ?identity displayName: ?displayName }
  Session: { ?session identity: ?identity; token: ?token }
}
then {
  Web/respond: [request: ?request; identity: ?identity; session: ?session;
                displayName: ?displayName; token: ?token]
}

### Refuse invalid credentials
sync RefuseLogin
when {
  Web/login: [] => [request: ?request]
  OAuthAuthentication/verify: [] => [valid: false]
}
then { Web/respond: [request: ?request; error: "InvalidCredentials"] }

### Return a verification error
sync ReportVerificationError
when {
  Web/login: [] => [request: ?request]
  OAuthAuthentication/verify: [] => [error: ?error]
}
then { Web/respond: [request: ?request; error: ?error] }

### Return a session error
sync ReportSessionError
when {
  Web/login: [] => [request: ?request]
  Session/open: [] => [error: ?error]
}
then { Web/respond: [request: ?request; error: ?error] }

## Execution constraints
- Flow/correlation: each Web/login starts its own flow with one verification attempt. Each other action is called at most once within that flow; repeated attempts need occurrence correlation.
- Reads/order: actions may execute synchronously or asynchronously; CompleteLogin matches completed Profile/set and Session/open actions. Successful completions require their declared state effects to be queryable. No other flow changes the queried profile or session between completion and response in this example.
- Outcomes: if actions complete with the listed cases and matched rules eventually execute, each request gets exactly one response. A session failure preserves completed identity/profile effects. The error response does not wait for the profile update or imply cancellation of that pending call.
- Timing/recovery: timing, retry, and restart recovery remain open.
