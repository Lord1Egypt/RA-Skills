---
name: expo-mobile-dev
description: Opinionated, step-by-step workflow for starting a new React Native + Expo mobile app — gathers the app's name, purpose, and target region (China mainland vs international), scaffolds with `pnpm create expo-app --template default@sdk-55`, installs a hand-picked stack (better-auth, sonner-native, TanStack Query, TanStack Form, Zustand), and installs the official Expo + TanStack AI development skills so future work has expert guidance loaded. Use whenever the user mentions building, scaffolding, starting, or bootstrapping a React Native, Expo, iOS, Android, or "mobile app" — even casually ("我想做一个 app", "make me an app", "start a mobile project"). Also use when the user references files like `app.json`, `app.config.ts`, `eas.json`, the `app/` router directory, or Expo-specific imports. Default to this skill for mobile work unless the user explicitly asks for native Swift, Kotlin, or Flutter.
license: MIT
compatibility: Designed for Claude Code and compatible agents. Requires Node.js 20+, pnpm, and network access to the npm registry, Expo/EAS, and the agent-skill registries (github.com/expo/skills, tanstack-skills, reactnativecn). macOS recommended for iOS builds.
metadata:
  author: "北京腾秀创智技术有限公司 (Tenshow Innovation)"
  organization: tenshowinnovation.com
  version: "0.1.0"
---

# Expo Mobile Development

A workflow for taking an idea to a working Expo project with the right tools and AI-development skills loaded. Five steps, in order. Don't skip the first one — the region question changes everything downstream.

## Why this is structured as a workflow

Mobile is unforgiving: choices made on day one (bundle ID, target region, auth provider, push provider) are hard to undo. This skill exists to make those decisions deliberately, once, before any code gets written. Each step has a clear input, a clear output, and a reason it comes where it does.

Don't run the steps out of order. Step 2 (scaffold) is non-destructive but locks in SDK version. Step 5 (region config) depends on knowing the answers from Step 1.

---

## Step 1: Capture intent (ALWAYS ASK FIRST)

Before any tool calls, get three answers from the user. If the user hasn't told you yet, ask them explicitly — preferably with `AskUserQuestion` so they're easy to answer.

1. **App name** — short product name. This becomes the project folder, the `name` in `app.config.ts`, and the basis for bundle IDs. Sanitize to lowercase-hyphenated for the folder (`MyApp` → `my-app`); keep the human-readable form for the display name.
2. **Purpose** — one sentence about what the app does and who uses it. This is not optional — it informs every later decision (do we need camera? maps? auth at all? offline?). If the user gives you a vague answer like "social app", push for one more level of specificity.
3. **Target region** — **中国大陆 (China mainland) vs 海外/国际 (international)**. This is the single most consequential question because it determines:

   | Concern | International | 中国大陆 |
   |---|---|---|
   | App stores | Apple App Store, Google Play | Apple App Store (China region) + 华为 / 小米 / OPPO / vivo / 应用宝 (Google Play is blocked) |
   | Regulatory filing | None | ICP 备案 (工信部) + 软著 (software copyright) for most stores; some categories need 版号 |
   | Push notifications | APNs (iOS) + FCM (Android) via `expo-notifications` | APNs works; FCM is blocked — need 极光推送 (JPush), 个推 (GeTui), or vendor SDKs (HMS Push for Huawei, MiPush for Xiaomi) |
   | Social login | Google, Apple, GitHub, etc. via better-auth | WeChat (微信), QQ, 微博, Apple; Google won't work for most users |
   | Maps | Google Maps, Mapbox | 高德 (AMap) or 百度地图 |
   | Analytics / crash | Sentry, PostHog, Mixpanel | 友盟 (Umeng), 神策 (Sensors); Sentry self-hosted is OK |
   | OTA / 热更新 | `expo-updates` + EAS Update | `react-native-update` + Pushy (https://pushy.reactnative.cn/) — requires `expo prebuild` |
   | Backend region | Anywhere | Prefer 火山引擎 (Volcano Engine) / 阿里云 (Alibaba Cloud) — domestic for latency + compliance |

   If the app is launching in **both** regions, plan to ship two builds with different bundle IDs and conditional providers — don't try to make one binary serve both. (Section: "Step 5".)

Save these three answers somewhere visible (e.g., the top of `app.config.ts` as comments, or a `README.md`). Re-confirm with the user before scaffolding.

---

## Step 2: Scaffold the project

Use **pnpm** and pin the SDK explicitly to `sdk-55`. Do not run interactively — pass the template flag.

```bash
pnpm create expo-app <app-name> --template default@sdk-55
cd <app-name>
```

The `default@sdk-55` template ships with: TypeScript (strict), Expo Router v5 (file-based, under `app/`), ESLint, an example tabs route, and the New Architecture (Fabric/TurboModules) enabled.

If the user wants a clean slate without the tabs example:

```bash
pnpm run reset-project
```

Verify it boots before installing anything else:

```bash
pnpm start
# Press 'i' for iOS simulator, 'a' for Android, 'w' for web
```

A working baseline is your safety net — if Step 3 breaks something, you know it's the package not the scaffold.

---

## Step 3: Install the opinionated stack

This is the high-quality, hand-picked default. The combination is coherent: TanStack Query + TanStack Form share the TanStack mental model, Zustand is the lightest possible global state, better-auth is the modern code-first auth library, sonner-native is the React Native port of the popular sonner toast UI.

### CRITICAL: Read docs before installing

These libraries are **young and evolving**. Installation steps, peer-dependency requirements, and provider setup change between minor versions. Before you install any of them, fetch the latest official docs:

- **Preferred**: Use the `context7` MCP if available — `mcp__plugin_context7_context7__resolve-library-id` then `mcp__plugin_context7_context7__query-docs` to pull current install instructions.
- **Fallback**: `WebFetch` against the package's official docs URL.
- **Don't** rely on memorized install snippets from training data. They will be stale.

### The packages

| Package | Purpose | Where to read first |
|---|---|---|
| `better-auth` + `@better-auth/expo` | Auth (email/password, OAuth, sessions) | https://www.better-auth.com/docs/integrations/expo |
| `sonner` + `sonner-native` | Toast notifications | https://github.com/gunnartorfis/sonner-native |
| `@tanstack/react-query` | Server state, caching, refetching | https://tanstack.com/query/latest/docs/framework/react/installation |
| `@tanstack/react-form` + `zod` + `@tanstack/zod-form-adapter` | Forms with schema-based validation | https://tanstack.com/form/latest/docs/framework/react/quick-start + https://zod.dev/ |
| `zustand` | Client/global state | https://zustand.docs.pmnd.rs/ |

### Install order

Install one at a time so you can verify each. For anything Expo-aware (better-auth's expo bridge, sonner-native), use `pnpm expo install` so the version matches SDK 55. For pure JS libraries, plain `pnpm add` is fine.

```bash
# 1. Auth — read docs FIRST, then install + run any setup commands the docs specify
pnpm add better-auth
pnpm expo install @better-auth/expo

# Localized error codes — BOTH regions. Without this, better-auth's error
# responses ship English-only ("INVALID_CREDENTIALS" etc.) which neither
# renders well in a Chinese app UI nor matches the UX bar for an international
# app with non-English users. Configure the locale per-request from the
# client's Accept-Language header (or a stored user preference).
pnpm add @better-auth/i18n

# Native Sign in with Apple (iOS) — required by App Store policy whenever
# you offer any other social login. Used for BOTH regions (international
# and 中国大陆), since both ship to the iOS App Store.
pnpm expo install expo-apple-authentication

# Native Google Sign-In — INTERNATIONAL ONLY.
# Skip this for 中国大陆 builds: Google Sign-In does not work for users
# without Google Play Services (most domestic Android phones), and Google
# is not a viable primary login path in mainland. Use WeChat/QQ/Weibo
# instead — see references/china-deployment.md.
pnpm expo install @react-native-google-signin/google-signin

# Phone-number + SMS-code login — PRIMARY login method for 中国大陆 builds.
# Chinese consumer users rarely use email; phone-number login (with SMS OTP)
# is the expected UX and is also required by 实名认证 regulations for many
# content/social app categories. better-auth's phoneNumber plugin lives in
# the core package (no extra install) — but it needs an SMS provider to
# actually send the OTP. Install ONE that matches the cloud you picked in
# references/backend.md:
#   - 火山引擎 SMS (primary):  pnpm add @volcengine/openapi
#   - 阿里云 SMS (fallback):   pnpm add @alicloud/dysmsapi20170525 @alicloud/openapi-client
# For INTERNATIONAL builds, phone+SMS is optional (email/password +
# Apple/Google is the standard); if you want it, Twilio / Vonage / AWS SNS
# are the common SMS providers.
#
# Tip: each cloud's CLI can create the SMS template (短信模板) and signature
# (短信签名) — scriptable infra instead of clicking through the web console.
# 火山引擎: the volcengine CLI; 阿里云: `aliyun dysmsapi AddSmsTemplate` etc.
# Full phone-flow walkthrough lives in references/auth.md.

# Dev-only deps for the Apple client_secret generation script
# (assets/generate-apple-client-secret.ts). Install these now so the script
# is runnable when you set up Apple Sign-In. Use `tsx` or Node 24+'s native
# TS stripping to execute the script.
pnpm add -D jose dotenv
# Then follow current docs for: server config, expo plugin in app.config.ts,
# client setup, and any required secure-store / deep-link configuration.
# For provider wiring (Apple / Google / GitHub / email+password / phone+SMS)
# including the Apple client_secret JWT generation script, see references/auth.md.
# For WeChat / QQ / Weibo (China), see references/china-deployment.md.

# 2. Toast
pnpm add sonner sonner-native
# Wrap the app in <Toaster /> per current sonner-native docs.

# 3. Server state
pnpm add @tanstack/react-query
# Wrap app in <QueryClientProvider> in app/_layout.tsx.

# 4. Forms — install form library, schema validator, and adapter together
pnpm add @tanstack/react-form zod @tanstack/zod-form-adapter
# Zod defines the schema once; the adapter wires it into TanStack Form's
# validators (onChange / onBlur / onSubmit) so you don't write validation
# logic twice. Check the TanStack Form docs for the current adapter API —
# the validators API has evolved between minor versions.

# 5. Client state
pnpm add zustand
# Create stores under lib/stores/.
```

### OTA / 热更新 (region-conditional)

Install the matching OTA library based on the answer from Step 1. **Pick one — they don't coexist.**

**If international:**

```bash
pnpm expo install expo-updates
```

Then configure with EAS (handled by the `eas-update-insights` skill installed in Step 4):

```bash
eas update:configure
```

Docs: https://docs.expo.dev/eas-update/introduction/

**If 中国大陆:**

```bash
pnpm add react-native-update
```

Important: `react-native-update` is not a first-party Expo module. You will need to run `pnpm expo prebuild` once before the native code links — this commits you to the bare workflow for native config (`ios/` and `android/` directories live in the repo from then on). Decide this consciously; the trade-off is OTA that actually works in mainland China.

Service: **Pushy** (the OTA backend service). Sign up and create an app at https://pushy.reactnative.cn/ to get your app key. The full SDK guide, build commands (`pushy bundle`, `pushy publish`), and rollout strategies live there — **always check the official docs before configuring**, the CLI flags and config schema change between versions.

Official docs URL (record this for the agent): **https://pushy.reactnative.cn/**

After installing the OTA library, restart Metro with cache cleared:

```bash
pnpm start --clear
```

---

## Step 4: Install AI development skills

These skills load expert guidance into future Claude sessions so subsequent work (deployment, native UI, OTA updates, etc.) gets specialized help automatically. Install them once per project.

### Expo official skills (all regions)

```bash
npx skills add https://github.com/expo/skills expo-tailwind-setup
npx skills add https://github.com/expo/skills expo-cicd-workflows
npx skills add https://github.com/expo/skills expo-deployment
npx skills add https://github.com/expo/skills expo-dev-client
npx skills add https://github.com/expo/skills expo-api-routes
npx skills add https://github.com/expo/skills building-native-ui
npx skills add https://github.com/expo/skills native-data-fetching
npx skills add https://github.com/expo/skills upgrading-expo
npx skills add https://github.com/expo/skills use-dom
npx skills add https://github.com/expo/skills expo-module
npx skills add https://github.com/expo/skills expo-ui-swiftui
```

### TanStack skills (all regions)

```bash
npx skills add https://github.com/tanstack-skills/tanstack-skills --skill tanstack-query
npx skills add https://github.com/tanstack-skills/tanstack-skills --skill tanstack-form
```

### Vercel skills (all regions)

```bash
npx skills add https://github.com/vercel-labs/agent-skills --skill vercel-react-native-skills
```

### OTA skill (region-conditional — install ONE)

Pick the one that matches the OTA library installed in Step 3.

**If international (`expo-updates`):**

```bash
npx skills add https://github.com/expo/skills eas-update-insights
```

**If 中国大陆 (`react-native-update` + Pushy):**

```bash
npx skills add reactnativecn/react-native-update-skill --skill react-native-update
```

This skill knows the Pushy CLI, version semantics, rollout strategies, and points at the official docs (https://pushy.reactnative.cn/) for anything not in its prompt.

If any single skill fails to install, continue with the rest — they're independent. Note which ones failed so the user can retry later. Don't block the workflow on one missing skill.

### Pacing tip

Don't run all 14 in one long blocking shell command. Run them in batches of 3-4 so failures are easy to see and retry. After all are installed, restart the Claude session if needed so the new skills are picked up.

---

## Step 5: Region-specific configuration

Apply this based on the answer from Step 1. Don't try to configure both regions in one project unless you've decided that's necessary — having two clean projects with shared code is usually simpler than one project with conditional everything.

### If international:

You're on the well-trodden path. Standard config:

- Apple Developer + App Store Connect account
- Google Play Console account
- EAS Build for both platforms
- `expo-notifications` for push (FCM + APNs)
- better-auth with Google/Apple/GitHub OAuth providers
- Sentry or PostHog for monitoring
- **Backend**: Hono inside Expo API Routes (`app/api/`), deployed to Cloudflare Workers. See [references/backend.md](references/backend.md) for the architecture and skeleton.

See [references/eas-recipes.md](references/eas-recipes.md) for build/submit details. The `expo-deployment` skill (installed in Step 4) handles the rest.

### If 中国大陆 (China mainland):

The path is substantially different and **must be planned before launch**, not bolted on later. Read [references/china-deployment.md](references/china-deployment.md) for the full picture. Highlights:

- **ICP 备案** is required before the app can be distributed in domestic Android stores. This takes 7-20 business days. Start the application now if launch is in the next 2 months.
- **Apple App Store China region** requires the app's content to comply with Chinese regulations; some categories (games, news, financial) need additional 版号/license.
- **Push notifications**: do NOT use Expo's default push relay for Android (it routes through FCM). Use 极光推送 (JPush) or vendor-specific push (HMS for Huawei, MiPush for Xiaomi). iOS APNs works as normal.
- **Primary login**: phone-number + SMS code via better-auth's `phoneNumber` plugin. Email-based login is uncommon in mainland consumer apps and creates UX friction. SMS provider: 火山引擎 SMS (primary) or 阿里云 SMS (fallback). See [references/auth.md](references/auth.md).
- **Social login**: WeChat (微信) login via `react-native-wechat-lib` or a dedicated config plugin. QQ login similarly. Don't ship Google login as the primary path.
- **Maps**: 高德 (AMap) is the default choice. There's no first-party Expo module — use the community config plugin or `expo prebuild` and add the SDK manually.
- **Analytics**: 友盟 (Umeng) is most common. If you prefer Western tooling, self-hosted PostHog or Sentry behind a China-accessible domain can work.
- **App stores**: budget time for each store's review process — 华为 (Huawei AppGallery) is the strictest, 应用宝 (Tencent MyApp) the most widely-used.
- **OTA / 热更新**: `react-native-update` + Pushy (https://pushy.reactnative.cn/). Already installed in Step 3; the `react-native-update` skill (Step 4) handles version + rollout commands.
- **Backend**: separate `apps/api/` directory in a pnpm monorepo, Hono server deployed to 火山引擎 (primary) or 阿里云 (fallback) — NOT Cloudflare Workers. See [references/backend.md](references/backend.md) for the monorepo layout, skeleton, and deploy targets.

---

## After all steps complete

You now have:
- A scaffolded Expo SDK 55 project with TypeScript and Expo Router
- The opinionated stack installed (auth, toast, server state, forms, client state)
- 14 AI development skills loaded for specialized future work
- A region-appropriate deployment plan

From here, default to the installed skills for specialized work:
- Styling → `expo-tailwind-setup` skill
- Server data → `tanstack-query` + `native-data-fetching` skills
- Forms → `tanstack-form` skill
- CI/CD → `expo-cicd-workflows` skill
- Store submission → `expo-deployment` skill; for store **listing content** (titles, descriptions, screenshots, metadata), see [references/store-presence.md](references/store-presence.md)
- OTA updates (international) → `eas-update-insights` skill
- OTA updates / 热更新 (中国大陆) → `react-native-update` skill (docs: https://pushy.reactnative.cn/)
- Custom native code → `expo-module` + `building-native-ui` skills

This skill stops being the primary guide once those specialized skills have something more concrete to say. Hand off cleanly.

---

## Reference files

- [references/backend.md](references/backend.md) — API server architecture. Hono is the framework for both regions. International: Hono inside Expo API Routes → Cloudflare Workers. 中国大陆: separate `apps/api/` directory in a pnpm monorepo → 火山引擎 (primary) / 阿里云 (fallback). Includes monorepo layout, skeletons, type-safe `hc` client, validation with `@hono/zod-validator`, auth integration, deploy commands.
- [references/auth.md](references/auth.md) — better-auth + international OAuth providers (Apple, Google, GitHub, email/password): provider setup, deep links, session storage, 180-day Apple client_secret rotation. References the Apple JWT generation script in `assets/`.
- [references/china-deployment.md](references/china-deployment.md) — Full China mainland deployment guide: ICP 备案, app stores, push, WeChat/QQ login, maps, analytics, Pushy OTA
- [references/store-presence.md](references/store-presence.md) — Store listing content & metadata: EAS Metadata for App Store Connect + Google Play (schema source of truth: https://docs.expo.dev/eas/metadata/schema/), Apple Privacy Nutrition Labels, Google Data Safety, screenshots & asset specs, plus the separate manual path for 华为 / 小米 / OPPO / vivo / 应用宝.
- [references/app-config.md](references/app-config.md) — `app.config.ts` patterns for env vars, build variants, plugins
- [references/eas-recipes.md](references/eas-recipes.md) — EAS Build/Submit/Update commands and `eas.json` templates

## Bundled assets

- [assets/generate-apple-client-secret.ts](assets/generate-apple-client-secret.ts) — Generates the 180-day-valid JWT used as Apple's OAuth client_secret. Copy to the user's project (typically `scripts/`) and run with `pnpm tsx`. Setup instructions live in [references/auth.md](references/auth.md).
