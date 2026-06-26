# Authentication (better-auth + International OAuth Providers)

How to wire up `better-auth` + `@better-auth/expo` with the OAuth providers commonly used outside mainland China: **Apple, Google, GitHub, and email/password**. For WeChat (微信), QQ, and Weibo, see [china-deployment.md](china-deployment.md) — those don't go through better-auth's stock provider list.

This reference is opinionated and pragmatic. better-auth is moving fast — **always cross-check the current docs at https://www.better-auth.com/docs before writing config**. Specific provider option names, redirect-URI formats, and the Expo bridge API have all changed across minor versions.

---

## Mental model

`better-auth` is a code-first auth library that runs on a server and exposes a typed client. The server framework and deployment target depend on region — see [backend.md](backend.md) for the architecture (Hono inside Expo API Routes → Cloudflare Workers for international, separate `apps/api/` Hono server → 火山引擎/阿里云 for 中国大陆). `@better-auth/expo` is the React Native bridge: it handles native OAuth flows, secure session storage (via `expo-secure-store`), and deep-link callbacks for you.

**Default login method by region** — pick the primary, layer the rest as supplemental:

| Region | Primary login | Required supplemental | Optional |
|---|---|---|---|
| International | Email + password | Apple Sign-In (App Store policy) | Google, GitHub, magic links |
| 中国大陆 | **Phone number + SMS code** | Apple Sign-In (App Store China policy) | WeChat (微信), QQ, 微博 |

Email-based login is the international norm and is uncommon in mainland China consumer apps. Don't ship email as the primary login for China — it creates UX friction (users have to remember another credential) and friction with 实名认证 (real-name verification) flows that already key off phone number.

Architecture:

```
┌───────────────────────────┐         ┌────────────────────────────┐
│  Expo app                 │         │  Auth server               │
│  • @better-auth/expo      │ HTTPS   │  • better-auth             │
│  • expo-secure-store      │ ◄─────► │  • Provider client_secrets │
│  • Deep-link scheme       │         │  • DB (users, sessions)    │
└───────────────────────────┘         └────────────────────────────┘
                                                │
                                                ▼
                                      Apple / Google / GitHub
                                       (OAuth providers)
```

The native app **never sees provider client_secrets**. They live on the server, which exchanges authorization codes for tokens.

---

## Apple Sign-In (required by App Store policy if you offer any other social login)

Apple OAuth is the most involved: instead of a static `client_secret`, Apple requires a **signed JWT** as the client secret. The JWT is valid for up to **180 days**, then you must regenerate it. The script under [`assets/generate-apple-client-secret.ts`](../assets/generate-apple-client-secret.ts) does this generation.

### Prerequisites

1. **Apple Developer account** (paid, $99/year)
2. **App ID** registered in Apple Developer portal with "Sign in with Apple" capability enabled
3. **Services ID** registered (this becomes your `APPLE_CLIENT_ID`)
4. **Sign in with Apple Key (.p8 file)** — created under **Keys** in the developer portal: **https://developer.apple.com/account/resources/authkeys/list** . **You can only download this file once.** Lose it and you have to revoke + reissue.

### Apple Developer Portal — where each value lives

Each value the script needs corresponds to a specific page in https://developer.apple.com/account/. Bookmark these — you'll come back every ~150 days for rotation.

| Env var / file | Source page | Direct URL |
|---|---|---|
| `APPLE_TEAM_ID` | Membership page (10-char string, top right of the portal too) | https://developer.apple.com/account |
| `APPLE_CLIENT_ID` | **Services IDs** (the identifier, looks like `com.example.app.signin`) | https://developer.apple.com/account/resources/identifiers/serviceId |
| App ID (prerequisite for Services ID + Key) | **App IDs** — enable "Sign in with Apple" capability | https://developer.apple.com/account/resources/identifiers/list |
| `APPLE_KEY_ID` + `AuthKey_<KEY_ID>.p8` | **Keys** — create a key with "Sign in with Apple" enabled, download the `.p8` (one chance only) | https://developer.apple.com/account/resources/authkeys/list |

### Setup flow in the portal (do these in order, once)

1. **App ID** — https://developer.apple.com/account/resources/identifiers/list → register an App ID (e.g., `com.example.myapp`) → check "Sign in with Apple" capability. This is the bundle ID your app ships with.
2. **Services ID** — https://developer.apple.com/account/resources/identifiers/serviceId → register a Services ID (e.g., `com.example.app.signin`, conventionally different from the App ID) → check "Sign in with Apple" → click "Configure" → set the **Primary App ID** to the one from step 1 → add return URLs (your auth server's callback, e.g., `https://api.example.com/api/auth/callback/apple`). **This Services ID identifier is the value of `APPLE_CLIENT_ID`** that the script reads from `.env`.
3. **Key** — https://developer.apple.com/account/resources/authkeys/list → "+" → name it → enable "Sign in with Apple" → click "Configure" → bind to the App ID from step 1 → "Save" → "Continue" → "Register" → **download the `.p8` file IMMEDIATELY** (you only get one chance). The 10-char Key ID shown next to it is `APPLE_KEY_ID`.
4. **Team ID** — visible top-right of https://developer.apple.com/account, or under Membership details. This is `APPLE_TEAM_ID`.

### File placement

Save the downloaded `.p8` next to the script as **exactly** `AuthKey_<APPLE_KEY_ID>.p8` — the script reads `./AuthKey_${keyId}.p8` literally. Example: if Key ID is `XYZ7890123`, the file must be `AuthKey_XYZ7890123.p8`.

Add the `.p8` filename pattern to `.gitignore` immediately:

```gitignore
# Apple Sign-In private key — never commit
AuthKey_*.p8
.env
```

### Generating the client_secret JWT

The script lives at [`assets/generate-apple-client-secret.ts`](../assets/generate-apple-client-secret.ts). Copy it to your project (e.g., `scripts/generate-apple-client-secret.ts`).

Install its dependencies (these are dev-only — they belong to the script, not the app):

```bash
pnpm add -D jose dotenv tsx
```

Create a `.env` at the project root (gitignored):

```env
APPLE_TEAM_ID=ABCD123456
APPLE_KEY_ID=XYZ7890123
APPLE_CLIENT_ID=com.example.app.signin
```

Place the `AuthKey_<APPLE_KEY_ID>.p8` file alongside the script (gitignored — `.p8` files are private keys, never commit).

Run:

```bash
pnpm tsx scripts/generate-apple-client-secret.ts
```

Output (a long JWT):

```
APPLE_CLIENT_SECRET:
eyJhbGciOiJFUzI1NiIsImtpZCI6IlhZWjc4OTAxMjMifQ.eyJpc3MiOi...
```

### Where the generated JWT goes

The JWT is the `clientSecret` value for better-auth's Apple provider on the **server**. Two places to put it:

1. **Local dev**: add to the server's `.env` as `APPLE_CLIENT_SECRET=<the JWT>`.
2. **Production**: store in EAS Secret (`eas secret:create --name APPLE_CLIENT_SECRET --value <the JWT>`) if the server runs on EAS, or in your hosting provider's secret store (Vercel env, Fly secrets, Alibaba/Tencent/AWS secret manager).

better-auth server config (cross-check current syntax in https://www.better-auth.com/docs):

```ts
// server/auth.ts
import { betterAuth } from "better-auth";

export const auth = betterAuth({
  socialProviders: {
    apple: {
      clientId: process.env.APPLE_CLIENT_ID!,
      clientSecret: process.env.APPLE_CLIENT_SECRET!, // the JWT from the script
      appBundleIdentifier: process.env.APPLE_BUNDLE_ID!, // your app's bundle ID
    },
  },
});
```

### 180-day rotation — set a calendar reminder NOW

The JWT expires. When it does, every Apple Sign-In attempt fails silently for users.

**On the day you generate a new client_secret, immediately set a calendar reminder for 150 days later** (gives you a 30-day cushion). Title it something obvious like "🔑 Rotate APPLE_CLIENT_SECRET for <app name>".

Rotation procedure:

1. Re-run `pnpm tsx scripts/generate-apple-client-secret.ts` (same `.p8`, same env vars — you don't need a new key unless the old one was leaked).
2. Update the secret in your production secret store.
3. Restart / redeploy the auth server.
4. Set the next reminder for 150 days out.

You can automate this with a GitHub Actions cron job, but for most teams a calendar reminder is enough — rotation isn't frequent enough to justify CI complexity.

### iOS native flow

On iOS, native Sign in with Apple goes through **`expo-apple-authentication`** rather than a web browser — it triggers the system-level Sign in with Apple sheet. `@better-auth/expo` integrates with this. The package is installed by Step 3 of [SKILL.md](../SKILL.md) (auth section); if you skipped that step, install with:

```bash
pnpm expo install expo-apple-authentication
```

Then add to `app.config.ts`:

```ts
ios: {
  usesAppleSignIn: true,
  // ...
},
```

Read https://docs.expo.dev/versions/latest/sdk/apple-authentication/ for the current button component and JS API.

### Troubleshooting

#### Filling the Services ID's two URL fields (the most common gotcha)

When you click "Configure" next to "Sign in with Apple" on a Services ID (step 2 of the setup flow above), Apple presents **two URL fields with different format requirements**. The form does not make the difference obvious, and putting the wrong format in either field causes either a save failure or silent OAuth rejection at sign-in time.

| Field | Format | Example |
|---|---|---|
| **Domains and Subdomains** (top field) | Bare domain — **NO `https://` scheme** | `example.com/` |
| **Return URLs** (bottom field) | Full URL **WITH `https://`** and the complete callback path | `https://example.com/api/auth/oauth2/callback/apple` |

Common mistakes:

- Pasting `https://example.com` into **Domains and Subdomains** → Apple rejects on save.
- Pasting `example.com/api/auth/oauth2/callback/apple` (no `https://`) into **Return URLs** → Apple rejects on save.
- Forgetting that both fields are required — leaving Return URLs empty makes Sign in with Apple silently fail at sign-in time, not at config save time.
- Trailing-slash mismatch between what's registered here and what the auth server actually serves (`.../apple` vs `.../apple/`). Apple does exact-string matching on the Return URL.

The callback path itself (`/api/auth/oauth2/callback/apple` in the example) is determined by **better-auth's current OAuth2 callback route**. Verify it against https://www.better-auth.com/docs before registering — the path has shifted between minor versions.

---

## Google OAuth

Significantly simpler than Apple — no JWT generation, just static credentials.

### Prerequisites

1. **Google Cloud project** with OAuth consent screen configured
2. **OAuth 2.0 Client IDs** created — you need **three separate client IDs**:
   - Web (used by the auth server)
   - iOS (used by the iOS native flow)
   - Android (used by the Android native flow)

### Values

```env
GOOGLE_CLIENT_ID=...apps.googleusercontent.com     # Web client ID
GOOGLE_CLIENT_SECRET=GOCSPX-...
GOOGLE_IOS_CLIENT_ID=...apps.googleusercontent.com
GOOGLE_ANDROID_CLIENT_ID=...apps.googleusercontent.com
```

Web client ID + secret go on the **server** (EAS Secret / hosting provider secrets).
iOS + Android client IDs are **safe to ship to the client** (they identify, not authorize — the actual auth happens server-side).

### Server config

```ts
// server/auth.ts
socialProviders: {
  google: {
    clientId: process.env.GOOGLE_CLIENT_ID!,
    clientSecret: process.env.GOOGLE_CLIENT_SECRET!,
  },
},
```

### Native client setup

International builds use **`@react-native-google-signin/google-signin`** for the native iOS and Android Google sign-in sheets — installed by Step 3 of [SKILL.md](../SKILL.md) (auth section). If you skipped that step:

```bash
pnpm expo install @react-native-google-signin/google-signin
```

Then:
1. Add the iOS and Android client IDs (from Google Cloud Console) to `app.config.ts` under `extra` (or wherever the library's config plugin expects them — verify against its current docs).
2. Register the library's config plugin in `app.config.ts` plugins array so iOS URL schemes and Android intent filters are set up automatically.
3. Cross-check the `@better-auth/expo` provider docs for how to hand the native token back to better-auth's server.

Library docs: https://react-native-google-signin.github.io/

**Do not ship this on 中国大陆 builds** — Google Sign-In silently fails on Android phones without Google Play Services (most domestic devices). For China, use WeChat/QQ/Weibo as documented in [china-deployment.md](china-deployment.md), and conditionally exclude the Google plugin via the `APP_REGION` env-var pattern in [app-config.md](app-config.md).

### Callback URL

Add to Google Cloud's OAuth client allowed redirect URIs:

```
https://<your-auth-server-domain>/api/auth/callback/google
```

(The exact path is set by better-auth — verify against https://www.better-auth.com/docs.)

---

## GitHub OAuth

The simplest of the three social providers.

### Prerequisites

1. Create an OAuth App at https://github.com/settings/developers
2. Set the **Authorization callback URL** to your server's callback path:
   ```
   https://<your-auth-server-domain>/api/auth/callback/github
   ```
3. Generate a client secret in the OAuth App settings.

### Values

```env
GITHUB_CLIENT_ID=Iv1.abc123def456
GITHUB_CLIENT_SECRET=...
```

### Server config

```ts
socialProviders: {
  github: {
    clientId: process.env.GITHUB_CLIENT_ID!,
    clientSecret: process.env.GITHUB_CLIENT_SECRET!,
  },
},
```

That's it — no native module, no platform-specific client IDs. GitHub OAuth always goes through the system browser via `expo-web-browser`.

---

## Email + Password (primarily for international)

better-auth ships with email/password built in. **For international builds this is typically the primary login method**; for 中国大陆 builds, prefer phone-number login (next section) — email is unusual for Chinese consumer apps and creates UX friction.

The setup work is in:

1. **Choosing an email sender** for verification + password reset emails. Pick one:
   - **Resend** — easiest API, modern, recommended for most teams
   - **Postmark** — fastest delivery for transactional email
   - **AWS SES / Alibaba Cloud DM** — cheapest at scale; more setup
2. **Wiring better-auth's email hook** to your sender:

   ```ts
   emailAndPassword: {
     enabled: true,
     requireEmailVerification: true,
   },
   emailVerification: {
     sendVerificationEmail: async ({ user, url }) => {
       await resend.emails.send({
         from: "noreply@example.com",
         to: user.email,
         subject: "Verify your email",
         html: `<a href="${url}">Verify</a>`,
       });
     },
   },
   ```

3. **Deep-link handling** — the verification link opens in the browser, then needs to redirect back into the app. See "Deep links" below.

---

## Phone number + SMS code (PRIMARY for 中国大陆)

For mainland China consumer apps, phone-number login is the default user expectation. It also aligns naturally with 实名认证 (real-name verification) regulations, which key off phone numbers tied to government-issued IDs.

better-auth provides this via the **`phoneNumber` plugin** in its core package — no separate npm install — but you must wire it to an SMS provider yourself.

### SMS provider choice

Match the cloud picked in [backend.md](backend.md). Both Chinese SMS providers we use require pre-approving the message template (短信模板) and the sender signature (短信签名) — budget ~1-3 business days for first-time approval before you can send a single SMS in production. Test environments have looser limits.

| Provider | Use when | SDK | Install |
|---|---|---|---|
| **火山引擎 SMS** (primary) | Default — pairs with the recommended primary cloud | `@volcengine/openapi` | `pnpm add @volcengine/openapi` |
| **阿里云 SMS (dysms)** (fallback) | On 阿里云 | `@alicloud/dysmsapi20170525` | `pnpm add @alicloud/dysmsapi20170525 @alicloud/openapi-client` |

For international builds that want phone-number login as a *supplemental* method (e.g., a US fintech that wants SMS-based MFA), Twilio / Vonage / AWS SNS are the standard choices.

**Create templates and signatures from the CLI, not the web console.** Both clouds expose template / signature management through their CLIs, so SMS infra becomes scriptable and reviewable in your repo instead of clicked through dashboards. Examples (verify against current docs — these CLIs evolve):

```bash
# 火山引擎 — via the volcengine CLI (`vctl` / `volcengine` depending on version)
volcengine sms CreateSmsTemplate \
  --SignName "腾秀" \
  --TemplateName "登录验证码" \
  --TemplateContent "您的验证码是 \${code}，5 分钟内有效。"
volcengine sms CreateSmsSign --SignName "腾秀" --SignSource 0  # 0 = self-owned brand

# 阿里云 — via aliyun CLI (after `aliyun configure`)
aliyun dysmsapi AddSmsTemplate \
  --SignName "腾秀" \
  --TemplateName "登录验证码" \
  --TemplateContent "您的验证码是\${code}，5分钟内有效。" \
  --TemplateType 0  # 0 = verification code
aliyun dysmsapi AddSmsSign --SignName "腾秀" --SignSource 0
```

Store template IDs and signature names in EAS Secrets (or your secret manager) and reference them from the auth server's env vars rather than hardcoding strings — that way rotating a template doesn't require a redeploy.

### Server config (cross-check current better-auth docs before copying)

```ts
// apps/api/src/auth.ts (or server/auth.ts)
import { betterAuth } from "better-auth";
import { phoneNumber } from "better-auth/plugins";
import { sendSmsViaVolcEngine } from "./sms";  // your provider wrapper

export const auth = betterAuth({
  plugins: [
    phoneNumber({
      sendOTP: async ({ phoneNumber, code }) => {
        await sendSmsViaVolcEngine({
          to: phoneNumber,
          templateCode: process.env.SMS_TEMPLATE_CODE!,
          templateParams: { code },
        });
      },
      // optional: rate-limit per phone number to prevent abuse
      otpLength: 6,
      expiresIn: 300, // 5 minutes
    }),
  ],
});
```

### SMS provider wrapper (火山引擎 example)

The exact SDK call shape changes between provider releases — **read the SDK's current docs before writing this**. The shape is roughly:

```ts
// apps/api/src/sms.ts (火山引擎 SMS)
import { VolcengineSigner /* etc — verify current import */ } from "@volcengine/openapi";

export async function sendSmsViaVolcEngine(params: {
  to: string;
  templateCode: string;
  templateParams: Record<string, string>;
}) {
  // construct the request per current 火山引擎 SMS API reference
  // POST to /sms_openapi/2020-01-01 with template + phone number + sign name
  // Auth: AK/SK signing via the SDK's signer helper
}
```

For 阿里云 dysms, the equivalent uses `@alicloud/dysmsapi20170525` Client's `sendSms` method. Both providers need: phone (with country code, `+86` for China), template code, template parameters, sign name (短信签名).

### Client-side (`@better-auth/expo`)

The Expo client side typically looks like:

```ts
const { sendOTP, verifyOTP } = authClient.phoneNumber;

// Step 1: request OTP
await sendOTP({ phoneNumber: "+8613800138000" });

// Step 2: user enters the 6-digit code from SMS, then:
const { data, error } = await verifyOTP({
  phoneNumber: "+8613800138000",
  code: "123456",
});
```

Cross-check the current `@better-auth/expo` client API before copying — method names and shapes have shifted between minor versions.

### Rate limiting + abuse prevention

SMS costs real money per send (火山引擎 charges ~¥0.04 per domestic SMS as of 2026). Without rate limiting, an attacker can drain your account or DDoS your users via SMS bombing. Minimum:

- Cap to 1 OTP per phone number per minute, 5 per hour, 10 per day
- Cap to N OTPs per IP per minute (~3-5)
- Require client-side CAPTCHA (火山引擎 / 阿里云 each ship a CAPTCHA product) before the first OTP request from any new IP

This is configured in the route handler in front of the `phoneNumber` plugin, not inside it.

---

## Localized error responses (`@better-auth/i18n`)

By default, better-auth returns error responses with English error codes and messages (`"INVALID_CREDENTIALS"`, `"INVALID_OTP"`). Two reasons that's not acceptable for production:

1. **Chinese-language UIs** can't render English error strings without rewriting them, and the constants leak through if you forget a translation.
2. **International apps with multi-language users** want errors in the user's language too.

`@better-auth/i18n` (installed in Step 3 of [SKILL.md](../SKILL.md)) wires translated error catalogs into better-auth's response shape. Configure with the locales you ship:

```ts
// apps/api/src/auth.ts
import { betterAuth } from "better-auth";
import { i18n } from "@better-auth/i18n";

export const auth = betterAuth({
  plugins: [
    i18n({
      defaultLocale: "zh-CN",   // or "en" for international
      supportedLocales: ["zh-CN", "en", "ja", "ko"],
      // Optional: resolve locale per-request from Accept-Language header
      resolveLocale: (req) =>
        req.headers.get("accept-language")?.split(",")[0] ?? "zh-CN",
    }),
    // ...other plugins
  ],
});
```

Cross-check the current `@better-auth/i18n` API — the option names (`defaultLocale` / `resolveLocale`) and the bundled translation catalogs evolve between minor versions.

---

## Deep links (callbacks back into the app)

OAuth callbacks and email verification links land in the browser, then need to reopen your app. Configure in `app.config.ts`:

```ts
export default ({ config }) => ({
  ...config,
  scheme: "myapp",  // custom URL scheme — `myapp://`
  ios: {
    bundleIdentifier: "com.example.myapp",
    // Universal Links (https URLs):
    associatedDomains: ["applinks:myapp.com"],
  },
  android: {
    package: "com.example.myapp",
    // App Links:
    intentFilters: [{
      action: "VIEW",
      autoVerify: true,
      data: [{ scheme: "https", host: "myapp.com" }],
      category: ["BROWSABLE", "DEFAULT"],
    }],
  },
});
```

Two approaches:
- **Custom scheme** (`myapp://auth/callback`) — simple, works without server config, but looks unpolished and can be hijacked by other apps using the same scheme.
- **Universal Links / App Links** (`https://myapp.com/auth/callback`) — requires hosting an `apple-app-site-association` file on iOS and `assetlinks.json` on Android, but is secure and indistinguishable from regular URLs.

For production, use Universal Links / App Links. For development/staging, custom schemes are fine.

`@better-auth/expo` reads the configured scheme automatically. Check the current package docs for exact callback URL formatting.

---

## Session storage

`@better-auth/expo` stores sessions in `expo-secure-store` (Keychain on iOS, EncryptedSharedPreferences on Android) by default. Don't override this — `AsyncStorage` is unencrypted and inappropriate for session tokens.

Install:

```bash
pnpm expo install expo-secure-store
```

The Expo bridge picks it up automatically. No additional config needed beyond what's in better-auth's Expo setup guide.

---

## Provider checklist

Before going live, verify each enabled provider:

- [ ] Server has each provider's client credentials (Web client_id + client_secret, or for Apple the generated JWT)
- [ ] Callback URLs match between provider console and server
- [ ] Native client IDs (Google iOS/Android) are in `app.config.ts`
- [ ] Deep-link scheme is configured and tested on both platforms
- [ ] For Apple: `expo-apple-authentication` installed, `usesAppleSignIn: true` in `app.config.ts`, calendar reminder set for client_secret rotation
- [ ] For 中国大陆 phone-number login: SMS template (短信模板) + sign name (短信签名) approved by the SMS provider, SMS provider AK/SK in EAS Secrets, rate-limiting + CAPTCHA wired in front of the OTP endpoint
- [ ] `@better-auth/i18n` configured with the locales you ship + locale resolver (Accept-Language header or stored preference)
- [ ] All client_secrets and SMS AK/SK are in EAS Secrets / hosting provider secrets, not in source code
- [ ] `.p8` Apple key file is gitignored
- [ ] Production OAuth apps are separate from development ones (different redirect URIs, different credentials)

---

## When something doesn't work

Most OAuth issues fall into a few buckets:

1. **Redirect URI mismatch** — the most common error. The provider console must list the *exact* callback URL the server uses. Check protocol (http vs https), trailing slash, path.
2. **Wrong client_id in the wrong place** — e.g., putting the web client_id in the iOS app config. Each platform needs its own.
3. **Apple client_secret expired** — silent failure ~180 days after generation. If Apple Sign-In suddenly breaks, regenerate the JWT first before debugging anything else.
4. **SMS OTP not arriving (China)** — check, in order: (a) is the phone number formatted with `+86` country code? (b) is your SMS template approved and currently active in the provider's console? (c) are you hitting a per-phone-per-minute rate limit on the provider side? (d) did the user opt out of marketing SMS at the carrier level (yes, this blocks transactional OTPs from some senders)? Provider dashboards show send + delivery status per message — start there.
5. **Error messages are in English when app is Chinese** — `@better-auth/i18n` plugin isn't installed, isn't registered in the `plugins` array, or its `resolveLocale` isn't returning the right locale for the request. Log the resolved locale from a middleware to confirm.

For better-auth-specific issues, the official docs (https://www.better-auth.com/docs) are the source of truth. The library is changing fast; stale Stack Overflow / blog posts will lead you astray.
