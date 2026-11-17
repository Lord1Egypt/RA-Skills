# Auth — Users, Sessions, Permissions, Password Flows

Django ships a complete authentication system; the failures come from the seams — the user model chosen too late, permission checks that look enforced and are not, and session settings left at their defaults.

## The User Model Decision

- `AUTH_USER_MODEL = "accounts.User"` must be set before the first `migrate` (SKILL.md Core Rules 8). Start with `class User(AbstractUser): pass`; it costs nothing and is the difference between adding a field later and rebuilding migration history.
- `AbstractUser` keeps username, email, names, and the permission machinery — extend it. `AbstractBaseUser` gives you only the password and last-login plumbing; choose it when you genuinely want email-as-identifier with no username column, and then you also owe a `UserManager` with `create_user`/`create_superuser` and a `REQUIRED_FIELDS` list.
- Reference the user model as `settings.AUTH_USER_MODEL` in foreign keys and `get_user_model()` inside functions. `get_user_model()` at module import raises `AppRegistryNotReady` (Core Rules 9).
- A separate `Profile` model with a `OneToOneField` is the alternative when you cannot swap the user model. Accessing `user.profile` when the row is missing raises `RelatedObjectDoesNotExist` — create it in the same transaction as the user, not in a signal that can be skipped by `bulk_create`.
- Email uniqueness is **not** enforced by `AbstractUser`. If you log in by email, add a `UniqueConstraint` on `Lower("email")` — case-insensitive, or two accounts differ only by capitalization.

## Login, Logout, Sessions

- `authenticate(request, username=..., password=...)` checks credentials and returns a user or `None`. `login(request, user)` only writes the session. Calling `login()` without `authenticate()` logs anyone in — this is the single most dangerous mistake in the module.
- `login()` cycles the session key, which is the built-in defence against session fixation. Never reuse a session across an authentication boundary by hand.
- `request.user.is_authenticated` is a property. `is_authenticated()` with parentheses is always truthy on old code — it has not been callable for many major versions, so the parentheses now raise, which is the good outcome.
- Session backends: database (default, needs `clearsessions` on a schedule or the table grows forever), cache (fast, and sessions vanish when the cache is evicted or restarted), cached_db (read from cache, write through to the database), signed cookies (no server state, no revocation, and the whole payload is visible to the client).
- `SESSION_COOKIE_AGE` defaults to 1209600 seconds (14 days). `SESSION_EXPIRE_AT_BROWSER_CLOSE` and `request.session.set_expiry(0)` give per-session cookies; `set_expiry(n)` sets seconds for that user.
- The session is only saved when it is *modified*. Mutating a nested structure in place (`request.session["cart"]["x"] = 1`) does not mark it dirty — reassign the key, or set `request.session.modified = True`.
- Cookie flags belong in settings, not in code: `SESSION_COOKIE_SECURE`, `SESSION_COOKIE_HTTPONLY` (on by default), `SESSION_COOKIE_SAMESITE = "Lax"`.
- Rotating `SECRET_KEY` invalidates every session and every password-reset link. `SECRET_KEY_FALLBACKS` (Django >=4.1) lets old signatures verify during a rotation window.

## Passwords

- Hashing is configured by `PASSWORD_HASHERS`; the first entry is used for new passwords and Django upgrades a user's hash on their next successful login. Argon2 requires the `argon2-cffi` extra; the default PBKDF2 iteration count rises with each Django release, which is why upgrading Django re-hashes users gradually.
- `set_password()` hashes; assigning `user.password = "..."` stores plaintext and produces an account nobody can log into (or worse, one that matches a crafted hash). `check_password()` verifies.
- `AUTH_PASSWORD_VALIDATORS` runs in forms and `validate_password()` — not in `set_password()`. A script that creates users bypasses every policy unless it calls the validators itself.
- The password reset flow is `PasswordResetView` → email with a signed token → `PasswordResetConfirmView`. Tokens expire after `PASSWORD_RESET_TIMEOUT` (default 259200 seconds = 3 days) and are invalidated by a password change or a `last_login` update, because both feed the token hash.
- Django has **no** built-in login rate limiting. An unprotected login endpoint is an open credential-stuffing target; add throttling at the view, the proxy, or with a dedicated package.
- Never log or email a password, and never include one in a `ValidationError` message — form errors are frequently logged wholesale.

## Permissions

- Every model gets `add`, `change`, `delete`, `view` permissions, created by `migrate` from the content types. New permissions in `Meta.permissions` exist only after the migration runs — a fresh permission that "does not exist" usually means an unmigrated environment.
- `user.has_perm("shop.change_order")` returns `True` for any superuser regardless of your logic. Test custom rules with a normal user, always.
- Permissions are cached on the user object for the life of the request. After granting one in the same request, re-fetch the user or clear `user._perm_cache`-style state by reloading the object.
- Django's permission system is model-level, not object-level: `has_perm` with an object argument returns `False` from the default backend. Object-level rules need a custom authentication backend, a rules-style package, or — most often the right answer — a queryset filtered by owner.
- **Filtering is the enforcement.** `Order.objects.filter(user=request.user)` in `get_queryset()` protects list *and* detail *and* update in one line; a permission check in the template protects nothing.
- Groups carry permissions; assigning users to groups is what makes permissions administrable. Hard-coded per-user permissions become undebuggable within a year.

## Protecting Views

| Layer | Tool | Note |
|---|---|---|
| Function view | `@login_required`, `@permission_required("app.perm", raise_exception=True)` | Without `raise_exception` an authenticated but unauthorized user is redirected to login, producing a loop |
| Class-based view | `LoginRequiredMixin`, `PermissionRequiredMixin` first in the bases | A decorator on the class does nothing |
| Whole project | `LoginRequiredMiddleware` (Django >=5.1) with `@login_not_required` on the exceptions | Default-deny beats remembering a decorator on every new view |
| API | DRF permission classes | Redirecting an API client to an HTML login page is the 302 symptom in SKILL.md |
| Object | Queryset filtered by owner | The only layer that survives someone guessing an ID |

- `LOGIN_URL`, `LOGIN_REDIRECT_URL`, `LOGOUT_REDIRECT_URL` are settings; the `next` parameter must be validated before use, or the login page becomes an open redirect.
- Logout is POST-only: `LogoutView` stopped accepting GET in Django >=5.0, because a GET logout is trivially triggered by an `<img>` tag on any page.

## Custom Authentication Backends

```python
class EmailBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        user = User.objects.filter(email__iexact=username).first()
        if user and user.check_password(password) and self.user_can_authenticate(user):
            return user
        return None
```

- Backends in `AUTHENTICATION_BACKENDS` are tried in order until one returns a user; permission checks consult **all** of them, so a permissive `has_perm` in any backend grants the permission.
- Return `None`, never raise, for "not my kind of credential" — raising stops the chain.
- Call `user_can_authenticate()` (or check `is_active` yourself); skipping it lets deactivated users log in.
- Run `check_password` even when the user is absent, or response timing tells an attacker which emails exist. Django's own `ModelBackend` calls `UserModel().set_password(password)` for exactly this reason.
- Anything protocol-level — OAuth providers, SAML, OIDC, MFA enrolment flows — is a different skill (see Related Skills in SKILL.md); what belongs here is how the resulting identity becomes a Django user and session.
