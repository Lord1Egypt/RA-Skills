# 中国大陆 (China Mainland) Deployment Guide

Shipping a mobile app inside China is a different track from the international one. The differences are not cosmetic — many international defaults (FCM push, Google Maps, Google OAuth, Expo's default OTA relay) are either blocked, slow, or non-compliant. This file is the practical checklist.

Before reading: confirm the user actually plans to distribute in mainland China. If the user is only targeting 港澳台 (Hong Kong / Macau / Taiwan) or worldwide-minus-China, treat as international.

---

## Regulatory checklist (do these first — they have long lead times)

### 1. ICP 备案 (工信部备案)

Required to legally distribute an Android app in domestic stores. Some stores (华为, 小米, OPPO, vivo) now refuse submissions without it.

- **What**: A filing with 工信部 (Ministry of Industry and Information Technology) tying your app to a company entity and domain.
- **Who can file**: A Chinese-registered company (营业执照). Foreign individuals/companies cannot file directly — you need a Chinese subsidiary, a partner, or a service.
- **Time**: 7-20 business days, sometimes longer in Q4.
- **Cost**: The filing itself is free; service providers charge 1000-5000 RMB.
- **Where to start**: 火山引擎 (Volcano Engine) and 阿里云 (Alibaba Cloud) both offer ICP 备案 assistance bundled with hosting — see [backend.md](backend.md) for cloud-choice rationale.

### 2. 软件著作权 (Software Copyright)

Required by most Chinese app stores as proof of ownership.

- **What**: A registered copyright certificate for your app's source code, issued by 中国版权保护中心.
- **Time**: 30-90 days for normal track; expedited services (加急) can do 1-15 days for extra fee.
- **Cost**: 300 RMB normal, 1000-3000 RMB expedited.

### 3. 版号 (only for specific categories)

Required for: games (mandatory), and increasingly some content categories.

- **What**: A 版号 (publication number) from 国家新闻出版署. Without it, paid features and in-app purchases for games are illegal.
- **Time**: Highly variable — can be months. There have been freezes in past years.
- **Don't ship a game without this.** It's the #1 reason indie game studios get pulled from stores.

### 4. 实名认证 (Real-name verification)

If the app has user-generated content, social features, or accounts: users must verify with their real name + national ID. Plan the integration with 火山引擎 / 阿里云实名认证 from the start.

---

## App stores

There is no single Android store. Plan to publish to multiple.

| Store | Owner | Notes |
|---|---|---|
| 华为应用市场 (Huawei AppGallery) | Huawei | Strictest review. Required if you want HMS users. |
| 小米应用商店 | Xiaomi | Large user base, moderate review. |
| OPPO 软件商店 | OPPO | Required for OPPO/OnePlus phones. |
| vivo 应用商店 | vivo | Required for vivo phones. |
| 应用宝 | Tencent | Most cross-device coverage. WeChat integration helps. |
| 360 手机助手 | Qihoo 360 | Declining share but still relevant. |
| 百度手机助手 | Baidu | Smaller now. Optional. |

**iOS**: Apple App Store, China region. The app review is the same Apple review you know, but content rules around politically sensitive topics are stricter. Cloud functions / VPN / news categories get scrutinized.

**Tooling**: There's no "one click deploy to all stores" like EAS Submit. Two practical options:
1. Manual upload to each store's developer portal (sometimes the only option for first submission)
2. 蒲公英 (PgyER) or 七鱼 multi-channel packaging tools for staged rollouts

EAS Build still works perfectly fine — it produces the .apk you upload. Just don't expect `eas submit` to handle non-Google Play Android stores.

**Store listing content (titles, descriptions, screenshots, metadata)**: EAS Metadata covers App Store Connect (including the China region) but **does not cover Chinese Android stores** — each one has its own dashboard with its own metadata schema. See [store-presence.md](store-presence.md) for the full picture, including the source-of-truth-file pattern for keeping the listing in sync across 华为 / 小米 / OPPO / vivo / 应用宝, plus the China-specific fields (ICP 备案号, 软著, 版号, 营业执照) each store requires.

---

## Push notifications

`expo-notifications` defaults to FCM on Android. **FCM is blocked in mainland China.** Devices without Google Play Services (most domestic phones) cannot receive FCM messages at all, and even devices with GMS see severe delays.

### Options (pick one, integrate early)

1. **极光推送 (JPush) — recommended default**
   - Most widely-used third-party push in China
   - Aggregates vendor channels (Huawei, Xiaomi, OPPO, vivo) — one SDK, all vendors
   - Has a React Native SDK; needs `expo prebuild` to integrate, or use a community config plugin
   - Pricing: free tier covers most apps until significant scale

2. **个推 (GeTui)**
   - Similar feature set to JPush, sometimes preferred for enterprise apps

3. **Vendor-specific (HMS Push, MiPush, OPPO Push, vivo Push)**
   - Each vendor has their own push system; using them directly avoids aggregator fees
   - Significantly more integration work — you ship multiple SDKs and route by manufacturer
   - Only worth it at scale

4. **iOS**: Use APNs normally via `expo-notifications`. APNs is not blocked in China.

### Implication for your code

Don't write code assuming a single push channel. Abstract the registration call so you can swap providers per platform / per build:

```ts
// lib/push/index.ts
export async function registerForPush() {
  if (Platform.OS === 'ios') return registerAPNs();
  return registerJPush();  // or vendor-specific
}
```

---

## Authentication / Social login

`better-auth` ships providers for Google, GitHub, Apple, etc. For China:

- **Apple** — works fine, often required by Apple's policy if you offer other social logins
- **Google** — works for users with VPN but unusable for most mainland users; don't make it the primary path
- **WeChat (微信)** — the dominant social login. Implementation: there's no first-party Expo module; use a community config plugin or `expo prebuild` with `react-native-wechat-lib`. Requires registering as a 开放平台 developer with WeChat (need a verified company + 300 RMB/year fee).
- **QQ** — second most common after WeChat
- **微博 (Weibo)** — relevant for content/social apps
- **手机号验证码 (SMS code)** — this is actually the PRIMARY login method for mainland consumer apps, not a fallback. See [auth.md](auth.md) for full implementation via better-auth's `phoneNumber` plugin. Use 火山引擎 SMS (primary) or 阿里云 SMS (fallback).

Integration with better-auth: WeChat etc. are not in better-auth's stock provider list. Either:
1. Use better-auth's custom OAuth provider hook to wire WeChat's OAuth flow
2. Use a Chinese-native auth library (e.g., 友盟+ 一键登录) alongside better-auth for non-WeChat flows

The cleaner architecture is option 1 — keep better-auth as the single session source of truth.

---

## Maps

`react-native-maps` defaults to Google Maps on Android (blocked) and Apple Maps on iOS (sparse data in mainland China — many roads/POIs missing).

### Choose one:

- **高德地图 (AMap)** — the standard choice. Most accurate POI data, best routing.
- **百度地图** — second choice; preferred if your data already lives in Baidu's ecosystem.

None have first-party Expo modules. Integration paths:
1. Community config plugin if one exists for your chosen provider
2. `expo prebuild` + manual SDK integration (most reliable)

Budget 1-2 days for first integration including the developer-portal registration and key provisioning.

---

## Analytics & error tracking

- **友盟 (Umeng)** — the de facto Chinese analytics standard. Free, comprehensive, mandatory for many apps that want growth marketing data.
- **神策 (Sensors Data)** — heavier, enterprise-style product analytics. Self-hosted available.
- **PostHog (self-hosted)** — works if you host on a China-accessible domain (Alibaba Cloud, etc.). Cloud PostHog (US/EU) is too slow.
- **Sentry (self-hosted)** — same logic; cloud Sentry has reliability issues from mainland.

If the app is dual-region, integrate two analytics SDKs and route at build time — don't try to send Chinese traffic to a Western SaaS.

---

## OTA / 热更新 (`react-native-update` + Pushy)

**The default Expo update CDN is slow and occasionally blocked in mainland China. Don't use `expo-updates` for China builds.**

The de facto standard for React Native OTA in China is **`react-native-update`** (the JS library) backed by **Pushy** (the hosted update service from reactnative.cn).

- **Library**: `react-native-update` — https://github.com/reactnativecn/react-native-update
- **Service**: Pushy — https://pushy.reactnative.cn/ (sign up, create an app, get an app key)
- **Skill**: `npx skills add reactnativecn/react-native-update-skill --skill react-native-update` — installs the Claude skill that knows the Pushy CLI, version semantics, and rollout commands.
- **Always check the official docs first** — Pushy's CLI flags, version-channel model, and config schema change between releases: https://pushy.reactnative.cn/

### Trade-off you must accept

`react-native-update` is not a first-party Expo module. To integrate it, you need to run `pnpm expo prebuild` once. This commits the project to the **bare workflow** for native configuration — the `ios/` and `android/` folders are now in the repo, and changes to native config go through those files rather than `app.config.ts` plugins alone.

For a China-only build this is the right trade-off: working OTA beats managed-workflow purity. For a dual-region build that needs to also serve international users with `expo-updates`, the cleanest architecture is two build profiles where only the China profile prebuilds and adds `react-native-update`, while the international profile stays in the managed workflow with `expo-updates`. The `APP_REGION` env-var pattern in the build-time configuration section below makes this possible.

### Workflow once installed

1. Sign up at https://pushy.reactnative.cn/ and create an app (one per platform per environment is the common pattern).
2. Save the app key to EAS Secrets (`eas secret:create`) — never commit it.
3. Use the Pushy CLI (`pushy bundle`, `pushy publish`) to ship updates; the `react-native-update` skill walks through the specific commands.
4. Test on a real domestic network before relying on it — Pushy is fast in China but you want to verify your specific carrier + region combination.

### Why not just self-host?

You can self-host an `expo-updates`-compatible server on Alibaba Cloud OSS — `expo-updates` is open about its protocol. But: you lose the rollout/staging features Pushy provides for free, you pay for CDN bandwidth yourself, and you maintain the update server. For 95% of teams shipping in China, Pushy is the correct choice. Self-host only if you have specific compliance or scale reasons.

---

## Backend hosting

See [backend.md](backend.md) for the full architecture story. Short version for China:

- **Don't host on Cloudflare Workers, Vercel us-east-1, or anywhere outside mainland for production.** China mainland → US round trips are 200-400ms even when not blocked, and CF has intermittent reachability issues.
- **Use a Chinese cloud, in this preference order**:
  1. **火山引擎 (Volcano Engine, ByteDance)** — **primary.** Best price-to-perf, fastest-improving Chinese cloud over the last 18 months, strong if your app touches the TikTok / Douyin / 抖音 ecosystem.
  2. **阿里云 (Alibaba Cloud)** — fallback. Most mature service catalog and the safest default; pick when 火山引擎 lacks a specific service or when you need the broadest ICP 备案 / domain registration bundle.

  Both bundle ICP 备案 assistance and offer Hong Kong regions if you want one region serving China + SEA. (Other clouds — 腾讯云, 华为云 — are out of scope for Tenshow's stack; see [backend.md](backend.md).)
- **Repo structure**: separate `apps/api/` directory in a pnpm monorepo (see [backend.md](backend.md) for the layout) — don't try to colocate inside Expo API Routes the way international builds do.

---

## Build-time configuration pattern

Use `app.config.ts` to switch between international and China builds without forking the codebase:

```ts
const region = process.env.APP_REGION ?? 'intl';
const isCN = region === 'cn';

export default ({ config }) => ({
  ...config,
  name: isCN ? 'MyApp 中国版' : 'MyApp',
  ios: {
    bundleIdentifier: isCN ? 'com.example.myapp.cn' : 'com.example.myapp',
    // ...
  },
  android: {
    package: isCN ? 'com.example.myapp.cn' : 'com.example.myapp',
    // ...
  },
  plugins: [
    'expo-router',
    isCN && 'react-native-wechat-lib',
    !isCN && 'expo-notifications',  // FCM-backed
    // ...
  ].filter(Boolean),
  extra: {
    region,
    apiUrl: isCN ? 'https://api.example.cn' : 'https://api.example.com',
  },
});
```

Then build with:

```bash
APP_REGION=cn eas build --profile production --platform all
APP_REGION=intl eas build --profile production --platform all
```

---

## What to budget time-wise for a first China launch

Rough order-of-magnitude for an indie / small team launching in China for the first time:

- ICP 备案: **2-3 weeks elapsed** (mostly waiting)
- 软著: **1-3 months elapsed** (mostly waiting, can be parallelized)
- WeChat OAuth setup: **1-2 days**
- AMap integration: **1-2 days**
- Push notification integration (JPush): **1-3 days**
- Per-store submission and review: **3-14 days per store**, total elapsed **2-4 weeks** if submitting to top 5 stores

So: do not promise "launch in 2 weeks" for a first-time China release. **6-10 weeks** is realistic for compliance + integration + reviews, even with a small competent team.
