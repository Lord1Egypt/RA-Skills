# Store submission and release checks

[简体中文](stores.zh-CN.md). Public-source check date: **2026-10-22**.
This guide expands **P4, P8, P9, W4 and X6**, preserving the checklist IDs.
Use it for a new listing, update, ownership transfer or distribution change.
Read only the selected channels; do not require an app to join every store.

## Scope and evidence

Record `store / package model × OS / architecture × territory × app type`
before deciding applicability. Include the publisher account, package / app
ID, release version, artifact hash, review track, intended audience and
features (accounts, UGC, ads, payments, regulated services). macOS App Store
and Developer ID downloads are different channels; so are Microsoft Store
MSIX and hosted MSI/EXE. A vendor's Android, HarmonyOS and quick-app offerings
are not interchangeable targets.

In the channel sections, **R** means a stated requirement for that path;
**C** means required when the stated trigger applies; **A** means advice or
an optional programme. This is separate from **verified / to do / needs
device / not applicable**. A recommendation is not a rejection rule.
For each applicable rule, retain its direct official source, check date,
trigger, evidence and owner. If a portal-only rule cannot be read, record
`to do` for the account owner, rather than treating it as absent.

These are submission checks, not permission to publish, alter a developer
account, accept agreements, buy certificates or contact reviewers. Complete
the artifacts within the user's authorization; leave any unapproved external
action at a concrete reviewable state.

## Common release evidence

This table is the skill's review procedure. The channel sections determine
which checks are store mandates; the table does not impose one store's rules
on another.

| Review gate | Evidence to collect / applicability | Existing IDs |
|---|---|---|
| Publisher and rights | Account owner, verified identity / organization where required, authorized app ownership, trademarks / content / redistribution rights, accepted current agreements and appropriate submitter role. Check trader / merchant / tax details when the selected territory or monetization triggers them. Use redacted console evidence; keep credentials out of reports. | P9, W4 |
| Package and update identity | Compare the uploaded artifact's ID, signing identity, version / build number, architectures and deployment minimum with the store record and prior release. Test the actual update, including app transfers, renamed IDs and Store vs direct-download coexistence where affected; a reinstall is not an upgrade. | B7, W4, X6 |
| Privacy and permissions | Inventory app and SDK collection / sharing / retention, match policy URLs and console disclosures, and inspect final manifests / entitlements / sandbox access. Test fresh consent, refusal, revocation and deletion. A no-collection declaration needs evidence too; it is not permission to omit a required form. | P1–P6, P9 |
| Audience and conditional features | Re-evaluate age / content ratings, children, ads, UGC moderation, account creation / deletion, third-party login, games, generative AI and regulated services. Attach the applicable category / territory rule and test it. No account creation can make an account-deletion rule inapplicable, not all privacy checks. | P4, P9 |
| Payment and regional conditions | Classify digital vs physical goods, app vs game, storefront and any enrolled alternative-billing programme. Prove allowed purchase, restoration, renewal, refund and cancellation flows. An app with no payments may mark P8 inapplicable; do not copy one global payment / external-link policy. | P8 |
| Listing and accessibility claims | Validate current required fields / asset sizes in the channel, separate app and listing locales, rights to screenshots / logos, support and privacy URLs, accurate features / device requirements and any accessibility claims. Preview each selected listing locale; an accessibility label needs functional evidence, not a screenshot. | D2, D5, I5, P9 |
| Review access | For restricted features, supply a dedicated working review account or permitted demo mode, entitlement / sample data / hardware instructions and a reachable backend. Test the route from a clean install, including region, network and OTP / MFA dependencies. Put access instructions in the secure review field, not the public listing or repository. | P9, X6, X8 |
| Installed release | Archive the exact artifact and validation reports, then test clean install, launch, protected features, upgrade and uninstall as an ordinary user. Exercise the store sandbox / signing identity and supported hardware / OS boundaries. Record automated counts separately from physical-device and human-console checks. | W4, X4, X6, X9 |
| Release and recovery | Record review approval vs published status, track / branch, countries, pricing, release operator and stop criteria. Rehearse available staged-release / pause controls and a forward-fix plan. Halting rollout or unlisting does not remove installed builds or reverse a data migration; a binary downgrade must pass B7. | B7, W4, X6 |

Use [permissions.md](permissions.md) for existing privacy, deletion, UGC,
children and payment acceptance tests; [desktop.md](desktop.md) for signing
and installers; [testing.md](testing.md) for device and release evidence.

## Apple App Store: iOS, iPadOS and macOS

- **R — record and review.** Match the team, bundle ID and app record;
  check current [app-record requirements](https://developer.apple.com/help/app-store-connect/create-an-app-record/add-a-new-app/)
  and [submission SDK requirements](https://developer.apple.com/news/upcoming-requirements/).
  Supply complete metadata, test access and live services under
  [App Review's submission checklist](https://developer.apple.com/app-store/review/guidelines/#before-you-submit).
- **C — Mac App Store.** Guideline **2.4.5** requires appropriate sandboxing,
  self-contained Xcode packaging and Store-delivered updates; a third-party
  installer / updater is not this path. Inspect the signed sandbox and test
  file / device access. [Mac requirements](https://developer.apple.com/app-store/review/guidelines/#hardware-compatibility)
  differ from [outside-Store Developer ID / notarization](desktop.md#w4-packaging-and-distribution--p0-for-release),
  which is not App Review approval. Do not apply macOS notarization steps
  as a substitute for iOS / iPadOS Store submission.
- **C — features and territory.** Apply P4 / P8 / P9 to the shipped features;
  complete [encryption export answers](https://developer.apple.com/help/app-store-connect/manage-app-information/overview-of-export-compliance/)
  and required territory / category documentation. Record compatible-iPad
  availability on Macs / Vision Pro as well as native platforms (W4).
- **A / C — listing claims.** Apple's [accessibility-label guidance](https://developer.apple.com/help/app-store-connect/manage-app-accessibility/overview-of-accessibility-nutrition-labels/)
  currently describes voluntary participation transitioning toward required
  disclosure. Check the current console requirement; substantiate any claim.
- **A — controlled release.** TestFlight and [phased updates](https://developer.apple.com/help/app-store-connect/update-your-app/release-a-version-update-in-phases/)
  help validation; phased automatic updates do not prevent manual downloads.
  Record the selected release option and a forward-fix procedure.

**Evidence:** processed build / archive ID, final entitlement and privacy
report, app record / feature answers, review-access rehearsal, installed
test results and release-option capture. A local archive alone is not an
approved submission. New submissions and updates need their own check.

## Google Play

- **R — publisher and package.** Complete the applicable
  [developer-identity verification](https://support.google.com/googleplay/android-developer/answer/10841920?hl=en),
  then match the permanent package name, increasing version code and
  [app setup](https://support.google.com/googleplay/android-developer/answer/9859152?hl=en).
  Follow the selected [release format / track](https://support.google.com/googleplay/android-developer/answer/9859348?hl=en)
  and [Play App Signing](https://developer.android.com/studio/publish/app-signing);
  record upload and distribution certificate fingerprints separately.
- **R / C — content declarations.** Review [App content](https://support.google.com/googleplay/android-developer/answer/9859455?hl=en):
  app access, ads, audience, rating, privacy / Data safety and any sensitive
  permissions or category declarations. P4 / P8 / P9 supply the behavioral
  checks, including account deletion where triggered. Check current
  [target API policy](https://support.google.com/googleplay/android-developer/answer/11926878?hl=en)
  and [native page-size rules](https://developer.android.com/guide/practices/page-sizes)
  rather than copying an old deadline.
- **C — production access.** Newly created personal accounts have a
  [closed-testing / production-access process](https://support.google.com/googleplay/android-developer/answer/14151465?hl=en).
  Check the account's current tester / duration conditions and retain the
  production-access result. Internal testing does not satisfy this gate.
- **A — rollout.** Choose the intended testing / production track and
  rollout controls; distinguish [publishing status](https://support.google.com/googleplay/android-developer/answer/9859751?hl=en)
  from a successful upload. Confirm the release is available to the intended
  accounts, countries and devices.

**Evidence:** console setup / declaration snapshot, bundle and delivered-APK
inspection, signed update on a supported device, review credentials tested
and applicable test-track / production-access evidence. An emulator or
side-loaded debug APK cannot establish Play device availability.

## Microsoft Store: choose MSIX or hosted MSI/EXE

The [submission guide](https://learn.microsoft.com/en-us/windows/apps/publish/get-started)
separates the paths. Reserve the product identity in Partner Center and
check account / package identity, age rating, capability declarations and
certification notes. Store MSIX/AppX packages are re-signed by Microsoft;
submission does **not** require purchasing a CA-trusted certificate. This
does not apply to a package distributed outside the Store.

**C — non-gaming, PC-only hosted MSI/EXE:** current
[Store Policies 10.2.9](https://learn.microsoft.com/en-us/windows/apps/publish/store-policies#102-security)
require a versioned immutable HTTPS installer URL, a standalone offline
installer, silent installation (UAC allowed), and trusted-CA signatures on
the installer **and all included PE files**. Inspect every binary and test
install / upgrade / uninstall from that URL. These are not MSIX rules.
Policy **7.20**, published 2026-09-15 and effective **2026-10-22**, is the
dated basis here. The [MSI/EXE certification help](https://learn.microsoft.com/en-us/windows/apps/publish/publish-your-app/msi/app-certification-process)
still calls signing a recommendation; use the current formal policy for
this requirement and recheck any discrepancy before submission.

**C — behavior:** apply policy 10.3 test account / live backend, 10.5 personal
data, 10.8 commerce and 11 content / age / UGC rules when triggered. Games
and non-game PC apps have different payment conditions (P8). Do not copy
Apple's login or Play's deletion-URL form as a Microsoft requirement.

**Evidence:** package / installer identity and signature inventory, immutable
URL hash, standard-user lifecycle test, relevant WACK / certification
results, store metadata and reachable review account. WACK passing is
preflight evidence, not Store certification.

## Flathub

- **R — inclusion and packaging.** Check current
  [requirements](https://docs.flathub.org/docs/for-app-authors/requirements):
  app-ID authority, redistribution licensing, declared offline-build
  sources, validated AppStream metadata, desktop entry / icon and minimal
  sandbox permissions / applicable portals. Verify requested architectures
  and supported runtime; test without local permission overrides.
- **C — human submission boundary.** The current
  [generative-AI policy](https://docs.flathub.org/docs/for-app-authors/requirements#generative-ai-policy)
  requires disclosure of known AI-generated app / packaging material and
  forbids AI-generated or AI-assisted Flathub manifests. It also prohibits
  agents from creating / automating submission PRs or generating their
  commit messages, descriptions or review interactions, and prohibits
  requested AI-agent reviews. Actual Flathub submissions require a human
  to handle those steps; disclosure alone does not grant acceptance. This
  is a Flathub-specific boundary, not a ban on unrelated project work.
- **A — identity / presentation.** [Verification](https://docs.flathub.org/docs/for-app-authors/verification)
  and [listing quality checks](https://docs.flathub.org/docs/for-app-authors/metainfo-guidelines/quality-guidelines)
  affect trust / promotion; quality checks are explicitly not all required
  for initial submission. Keep them separate from inclusion requirements.

**Evidence:** human-confirmed provenance / rights, source / runtime / commit
identifiers, [submission build and lint results](https://docs.flathub.org/docs/for-app-authors/submission),
installed sandbox / portal tests, and reviewer disposition when submitted.
A local `.flatpak` or merged app-repository PR is not Flathub acceptance.

## Snap Store

- **R — publication identity.** Register the publisher and snap name, check
  package metadata / declared architectures, and review the store's
  [upload / automated review process](https://ubuntu.com/docs/snapcraft/9/how-to/publishing/publish-a-snap/).
- **C — confinement and permissions.** [Permission requests](https://snapcraft.io/docs/permission-requests)
  require approval for classic confinement and specified privileged access /
  auto-connections. `devmode` is not eligible for a stable-channel release.
  Test the declared [confinement](https://snapcraft.io/docs/explanation/security/snap-confinement/)
  and actual interface connections; local `--devmode`, `--dangerous` or
  manual connections do not establish Store-install behavior.
- **A — release control.** Use the intended
  [track / risk channel and progressive-release controls](https://ubuntu.com/docs/snapcraft/9/how-to/publishing/manage-revisions-and-releases/).
  Record the released revision separately from the display version. Prove
  a store install, refresh from the prior revision and data compatibility
  before changing production channels. Do not treat an upload as permission
  to promote to stable.

**Evidence:** publisher / name, revision / channel, automated review result,
manual grant links when required, installed `snap connections` and refresh
test. The [Store terms](https://ubuntu.com/legal/terms-and-policies/snap-store-terms)
include content, licensing and third-party privacy rights; do not invent
Play-style Data safety or IARC forms for this channel.

## Mainland China Android: selected channels

Select each actual channel and territory explicitly. The representative
routes below are not a claim that all Android stores have one policy, nor
an exhaustive legal determination. Keep APK vs HarmonyOS vs quick-app
records separate. Other selected stores need their own dated official
rules and portal evidence.

| Channel / source | Check before that channel's submission | Source access on 2026-10-22 |
|---|---|---|
| Huawei AppGallery [review-policy index](https://developer.huawei.com/consumer/cn/doc/doccenter-submission/50000) | Obtain the applicable application review guide, qualification / filing guide, age-rating and privacy-label instructions for the selected platform / territory. Record the developer entity and exact submitted package type. | Official indexed overview inspected; detailed portal pages were not fully readable. Owner must verify current detailed rules in the console; do not mark them verified from the index. |
| Xiaomi [current listing requirements](https://dev.mi.com/xiaomihyperos/documentation/detail?pId=1322) | Reconcile publisher / app identity, qualification and filing material; inspect first-run privacy accept / reject and pre-consent SDK behavior, matching in-app / web policy and actual account-deletion flow where applicable. Paid features need usable review access. | Full public requirement text inspected; dated 2025-09-02. Prefer it to older MIUI screenshot / submission guides, then check live console updates. |
| OPPO [publication entry](https://open.oppomobile.com/new/developmentDoc/info?id=10035) and [review-guide migration entry](https://open.oppomobile.com/new/developmentDoc/info?id=10071) | Follow the current migrated guide and selected app / qualification path, privacy review and test-access instructions. Confirm distribution territory and applicable payment / content requirements in the portal. | Official indexed excerpts inspected; public HTML requires JavaScript and review guide has moved. Detailed requirements remain an owner portal check. |

**C — territory / service:** the [MIIT APP filing notice](https://www.miit.gov.cn/jgsj/xgj/wjfb/art/2023/art_dd783a581c9644a4aee10afa582811db.html)
addresses providers of APP internet information services in mainland China;
record whether that scope applies, the filing / permit and displayed number
when required. Sector qualifications (for example news, games, health or
finance) depend on the actual service and channel. Software-copyright
evidence, internet-service filing, sector permission and privacy consent
are different checks. Do not infer universal filing / payment / deletion
rules from a Chinese-language UI or from one store's acceptance.

**Evidence:** current official guide / console capture, verified operator /
package correspondence, applicable qualification material, privacy / SDK
test report, device-specific install / signed update and review account.
Where requirements or applicability are unresolved, record `to do` with the
owner; an untested domestic channel is not `not applicable` merely because
the Play build passes.

## Other selected distribution channels

These are conditional routes, not extra mandatory stores:

- **WinGet community repository:** follow its
  [manifest / installer validation](https://learn.microsoft.com/en-us/windows/package-manager/package/winget-validation),
  publisher URLs and package policies. Manifest acceptance does not certify
  the app for Microsoft Store. Test install, upgrade and uninstall from the
  published manifest, including hashes / architecture / silent switches.
- **Homebrew Cask:** check [acceptance](https://docs.brew.sh/Acceptable-Casks)
  and the [cask recipe](https://docs.brew.sh/Cask-Cookbook), with upstream
  artifact version, URL, checksum / allowed exceptions and supported
  platforms. Cask distribution does not bypass macOS security checks (W4).
- **F-Droid main repository, when selected:** inspect its
  [inclusion / source and dependency requirements](https://f-droid.org/docs/Inclusion_Policy/)
  and plan the flavor / signing / update path. A proprietary-SDK Play build
  is not automatically eligible; do not silently remove product features.
- **Direct downloads and distro repositories:** maintain the selected
  repository / installer policy, signatures / update trust and recovery
  evidence under W4 / X6. A standalone `.deb`, `.rpm`, AppImage, DMG or MSI
  is not an approval from the desktop's graphical software center.

## Report record

Keep the common app / artifact information once, then split rows by store,
package model, territory or feature trigger when their outcomes differ.
For example (illustrative, **not** results of an actual submission):

| ID / channel | Rule level / trigger | Status | Evidence / next action |
|---|---|---|---|
| W4 / Microsoft hosted MSI | C; non-game PC URL path | to do | Source 10.2.9 checked 2026-10-22; sign installer and included PE inventory, retain immutable URL hash and standard-user install results. Owner: release engineer. |
| P9 / Apple / account deletion | C; no account creation | not applicable | Record that release has no guest, automatic, linked or in-app account creation; re-evaluate when accounts are added. Privacy checks remain applicable. |
| X6 / Snap / camera | C; camera feature shipped | needs device | Revision and channel recorded; owner tests store install, actual interface grant, capture / refusal / refresh on supported hardware. |

Record console / reviewer evidence separately from local tests. No real
store account, submission or approval was exercised while writing this
reference. Reopen the official sources and the selected console at release;
do not freeze SDK deadlines, tester counts, screenshot dimensions, fees or
review durations in project code from this guide.
