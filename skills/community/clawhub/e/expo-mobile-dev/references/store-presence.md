# Store Presence & Metadata

"Store presence" = everything that appears alongside the binary in an app store listing: title, subtitle, description, keywords, screenshots, icons, video previews, categories, age rating, privacy declarations, support URL, marketing URL, pricing tier, and localized versions of each. This is content, not code — but it's load-bearing for discoverability, conversion, and submission approval.

This reference covers managing that content in a maintainable way, with the **right path per region**.

---

## Schema source of truth

For the international stores (App Store Connect + Google Play), Expo provides **EAS Metadata** — a code-first way to manage store listings via a single `store.config.json` (or `.js` / `.ts`) file.

**The schema for that file is documented at https://docs.expo.dev/eas/metadata/schema/ — always treat that page as the source of truth.** EAS Metadata is still evolving; the schema gains and renames fields between Expo releases. Do not memorize field names from past projects or training data — fetch the current schema before writing or editing `store.config.json`.

When asked to populate a field, the workflow is:

1. Open https://docs.expo.dev/eas/metadata/schema/ (or fetch via `WebFetch` / `context7`).
2. Find the field name, its type, validation rules, and which platform(s) it applies to.
3. Write the value into `store.config.json` at the documented path.
4. Validate: `eas metadata:lint`.

---

## EAS Metadata (international path)

### What it covers

- **App Store Connect (iOS)**: extensive coverage — name, subtitle, description, keywords, promotional text, what's new, support/marketing URLs, primary/secondary category, age rating questionnaire, copyright, screenshots references, review info (contact, demo account, notes), build selection, version release type.
- **Google Play Console (Android)**: partial coverage at present — Expo's docs note ongoing expansion. Verify per-field support against the schema URL above before assuming a field round-trips through `metadata:push`.
- **Localization**: full — each field can be specified per locale (e.g., `en-US`, `zh-Hans`, `ja`).

### File layout

```
my-app/
├── store.config.json        # the EAS Metadata config (or .ts for typed editing)
├── assets/store/
│   ├── ios/
│   │   ├── icon-1024.png
│   │   ├── screenshots/
│   │   │   ├── 6.7-inch/
│   │   │   ├── 6.5-inch/
│   │   │   └── 5.5-inch/
│   │   └── preview-videos/
│   └── android/
│       ├── icon-512.png
│       ├── feature-graphic.png
│       └── screenshots/
│           ├── phone/
│           ├── tablet-7/
│           └── tablet-10/
└── eas.json
```

Screenshots and icons are referenced from `store.config.json` by relative path — keep them under `assets/store/` so they ship as part of the repo (or under a `.gitignored` directory that's populated by a build step if you generate them).

### Core commands

Verify these against the EAS CLI docs (the command surface has shifted between releases):

```bash
# Pull existing metadata from App Store Connect / Play Console into local config
eas metadata:pull

# Push local config up to the stores
eas metadata:push

# Validate the local config against the schema before pushing
eas metadata:lint
```

The pull/push round-trip lets you onboard an existing app: pull current store content, version it in git, then make all future edits through the config file.

### Credentials

EAS Metadata needs API credentials for each store:

- **App Store Connect**: App Store Connect API key (.p8 file from https://appstoreconnect.apple.com/access/api). Configure once via `eas credentials` or by referencing it in `eas.json`.
- **Google Play**: service account JSON with the right Play Console permissions. Same file you use for `eas submit`.

Both files are private keys — gitignore them, and store production copies in EAS Secrets or your team's secret manager.

### Localization pattern

In `store.config.json`, each text field is a map from locale to string. Skeleton:

```json
{
  "configVersion": 0,
  "apple": {
    "info": {
      "en-US": {
        "title": "MyApp",
        "subtitle": "Short tagline",
        "description": "Long description...",
        "keywords": ["word1", "word2"]
      },
      "zh-Hans": {
        "title": "我的应用",
        "subtitle": "副标题",
        "description": "应用详细介绍...",
        "keywords": ["关键词一", "关键词二"]
      }
    }
  }
}
```

Field names are illustrative — **check the schema page before writing this for real**.

App Store Connect requires metadata in every locale you've enabled for the app; don't enable a locale without populating it.

---

## Asset requirements (international)

These dimensions are the moving targets in store presence — Apple in particular has changed required device sizes multiple times. Cross-check against the schema URL and Apple/Google's own docs before generating assets.

| Asset | Where | Typical sizes |
|---|---|---|
| iOS app icon | App Store Connect | 1024 × 1024, PNG, no alpha |
| iOS screenshots | App Store Connect | 6.7", 6.5", 5.5" iPhone; 12.9" / 11" iPad — at the resolutions Apple currently mandates |
| iOS preview video | App Store Connect | 15-30 sec, per device size, max 500 MB |
| Android app icon | Play Console | 512 × 512, PNG |
| Android feature graphic | Play Console | 1024 × 500, PNG/JPG |
| Android screenshots | Play Console | Phone (min 2, max 8); 7" tablet, 10" tablet (optional) |
| Android promo video | Play Console | YouTube URL (not uploaded directly) |

**Apple is strict about screenshot dimensions** — the "required device sizes" list changes with each iPhone generation. If submission fails on "missing screenshots for 6.9-inch display," it means Apple added a device size and you need to regenerate at the new resolution.

For automated screenshot generation, tools like Fastlane Snapshot, Maestro screenshots, or Detox + custom scripts work. Worth investing in once you ship to ≥5 locales — manual screenshot capture across locales × devices × screens does not scale.

---

## Privacy & compliance declarations

Both Apple and Google require explicit disclosures about what data the app collects. These are NOT auto-generated; you fill in questionnaires that must match what the app actually does, or risk rejection or store removal.

### Apple — Privacy Nutrition Labels / App Privacy Details

In App Store Connect: per data type collected, declare:
- Whether it's collected
- Whether it's linked to the user's identity
- Whether it's used for tracking
- The purpose (analytics, app functionality, etc.)

Cross-reference the actual SDKs the app embeds (analytics, push, crash reporting, auth providers, ad networks). Each SDK's own privacy manifest (`PrivacyInfo.xcprivacy`) feeds into this.

### Google — Data Safety form

In Play Console → "App content" → "Data safety": similar questionnaire to Apple's. The Play Console links to a CSV import format if you have lots of data types — useful if the app touches many.

### Privacy URL

Both stores require a hosted privacy policy URL. Don't ship without one — a real policy on a real domain.

---

## 中国大陆 (China mainland) — separate path

EAS Metadata **does not cover Chinese Android app stores**. Each store has its own dashboard, metadata format, and review process. Workflow becomes a parallel manual one:

| Store | Where to manage listing | Notes |
|---|---|---|
| **App Store China region (iOS)** | App Store Connect (same dashboard, `zh-Hans` locale) | EAS Metadata works here. Just enable `zh-Hans` and populate. |
| **华为 AppGallery** | https://developer.huawei.com/consumer/cn/console | Strictest review. Long-form 应用介绍 + 应用截图 required. |
| **小米应用商店** | https://dev.mi.com/console/ | Requires 软著 number, ICP 备案 number. |
| **OPPO 软件商店** | https://open.oppomobile.com/ | Similar metadata fields to Xiaomi. |
| **vivo 应用商店** | https://dev.vivo.com.cn/ | Similar to OPPO. |
| **应用宝** | https://wikinew.open.qq.com/ | Tencent. WeChat-integrated promotion options. |

### Keeping metadata in sync across Chinese stores

Recommended pattern: maintain a single **source-of-truth YAML or markdown file** in the repo (e.g., `store-presence/cn.yaml`) with localized name, subtitle, description, keywords, screenshots, and a per-store override map for any field that differs. Then either:

1. **Manual upload per store** — copy-paste from the SOT file into each console. Tedious but reliable, fine for ≤5 updates per year.
2. **Use a third-party Chinese multi-channel tool** — e.g., 蒲公英 (PgyER), Bugly, or 友盟分发. These offer aggregated upload to multiple Chinese stores, with varying coverage.

EAS Metadata is not in this picture for Chinese Android stores. Don't try to force-fit it.

### China-specific metadata fields

Most Chinese stores require, on top of the international fields:

- **ICP 备案号** — your filed ICP number (see [china-deployment.md](china-deployment.md))
- **软著证书** — software copyright certificate number + scan
- **公司营业执照** — business license scan
- **版号** — only for games (mandatory) and some content categories
- **隐私政策 URL** — hosted on an ICP-filed domain
- **联系电话** — Chinese phone number for the developer contact
- **应用分类** — each store has its own category taxonomy; map to the closest match

Budget time for the initial submission: every store wants a slightly different declaration of permissions, SDKs used, and content compliance. This is mostly form-filling, not code.

---

## Pre-submission checklist

Before clicking "Submit for Review" on any store:

- [ ] App name, subtitle/short description, long description populated in every supported locale
- [ ] Keywords / search terms tuned (App Store Connect allows up to 100 chars total for iOS keywords)
- [ ] Screenshots present for every required device size, every locale
- [ ] App icon at all required dimensions, no transparency where prohibited (iOS)
- [ ] Preview video uploaded if applicable
- [ ] Category (primary + secondary) selected
- [ ] Age rating questionnaire completed
- [ ] Privacy URL hosted and reachable
- [ ] Apple Privacy Nutrition Labels / Google Data Safety form filled and matches the app's actual SDK behavior
- [ ] Support URL + marketing URL hosted and reachable
- [ ] Pricing tier set
- [ ] Build selected and processed (not "still processing")
- [ ] Review notes include demo account credentials if any feature requires login
- [ ] For China: ICP 备案号, 软著, 营业执照, 版号 (if applicable) all uploaded to each Android store
- [ ] `eas metadata:lint` passes (international) and the file is committed

Run `eas metadata:push` (international) or upload to each Chinese store dashboard as the final step.

---

## Reference URLs

- **EAS Metadata schema (the source of truth)** — https://docs.expo.dev/eas/metadata/schema/
- **EAS Metadata getting started** — https://docs.expo.dev/eas/metadata/
- **App Store Connect API keys** — https://appstoreconnect.apple.com/access/api
- **Apple Privacy Manifest spec** — https://developer.apple.com/documentation/bundleresources/privacy_manifest_files
- **Google Play Data Safety guide** — https://support.google.com/googleplay/android-developer/answer/10787469
- **华为 AppGallery dev console** — https://developer.huawei.com/consumer/cn/console
- **小米应用商店 dev console** — https://dev.mi.com/console/
- **OPPO 开放平台** — https://open.oppomobile.com/
- **vivo 开放平台** — https://dev.vivo.com.cn/
- **腾讯应用宝 (开放平台)** — https://wikinew.open.qq.com/
