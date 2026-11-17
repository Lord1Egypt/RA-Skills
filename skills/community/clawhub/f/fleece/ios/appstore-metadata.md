# Fleece: Card Advisor — App Store Metadata

Copy-paste ready content for all App Store Connect fields.

---

## App Information

| Field | Value |
|---|---|
| **Name** | Fleece: Card Advisor |
| **Subtitle** | Best Card at Every Store |
| **Primary Category** | Finance |
| **Secondary Category** | Utilities |
| **Privacy Policy URL** | https://getfleece.io/privacy-policy |
| **Support URL** | https://getfleece.io |
| **Marketing URL** | https://getfleece.io/ios |
| **Age Rating** | 4+ |
| **Primary Language** | English (U.S.) |

---

## Version 1.0 — App Store Listing

### Promotional Text (170 chars max — changeable without resubmission)

```
Fleece finds your best credit card for every purchase — tap any store on the map for instant ranked recommendations from your wallet.
```

### Description (4000 chars max)

```
Fleece recommends the best credit card in your wallet for every purchase — automatically, as you move between stores.

How it works
Tap any business on the map to see instant card recommendations from your wallet. Fleece knows the reward rates for dining, groceries, gas, travel, transit, entertainment, and more — and ranks your cards by what you'll actually earn.

Set up your wallet once. Every tap on the map gives you a ranked list, best card first.

Ask Fleece — on-device AI
Chat with a card advisor powered by Apple Intelligence. Ask "Which card should I use at Whole Foods?" or "What earns the most on flights?" — processed privately on your device, nothing sent to any server.

Supported cards include:
• Chase Sapphire Preferred & Reserve
• American Express Gold & Platinum
• Citi Double Cash & Custom Cash
• Capital One Venture & Savor
• Bilt Mastercard

Privacy by design
• No account required
• No data leaves your device
• Location processed on-device via Apple MapKit
• AI powered by on-device Apple Intelligence
• No ads, no tracking, no telemetry

Spending profile
Enter your monthly spend in dining, groceries, travel, gas, and other categories. Fleece uses this to surface the card that earns the most for your actual habits.

Requires iOS 17.0 or later.
The Ask tab requires Apple Intelligence (iPhone 15 Pro or later with iOS 18.1+, or iPhone 16 with iOS 18.1+).
```

### Keywords (100 chars max, comma-separated — no spaces after commas)

```
credit card,rewards,cashback,wallet,best card,dining,travel,points,finance,card advisor
```

### What's New in This Version

```
Welcome to Fleece — the first release. Tap any store on the map to see your best card instantly.
```

---

## Screenshots

Upload from `ios/screenshots/framed/` — three framed 1290×2796 screenshots:

| File | Screen | Caption suggestion |
|---|---|---|
| `01_home_framed.png` | Map + card recommendations | Best card, detected automatically |
| `02_wallet_framed.png` | Wallet card management | Add the cards you carry once |
| `03_settings_framed.png` | Settings + spending profile | Personalize with your spend habits |

Upload all three to the **6.7-inch iPhone display** slot. App Store Connect will scale them for other sizes automatically.

---

## App Review Information

### Contact

| Field | Value |
|---|---|
| First Name | Yuan |
| Last Name | Chen |
| Phone | (your number) |
| Email | cysbc1999@gmail.com |

### Sign-in Required

No — the app does not require an account or login.

### Notes for Reviewer

```
Fleece detects nearby store categories via Apple MapKit and recommends the best credit card from the user's wallet.

To test:
1. Open the app and go to the Wallet tab — add 2–3 cards (e.g. Chase Sapphire Preferred, Amex Gold, Citi Double Cash).
2. Return to the Home tab — tap anywhere on the map to see ranked card recommendations for that location.
3. The Ask tab requires Apple Intelligence. On devices without Apple Intelligence enabled, the tab shows a setup prompt — this is expected behavior.

No internet connection is required for the core recommendation features. All place detection and card ranking runs on-device.
```

---

## Pricing and Availability

| Field | Value |
|---|---|
| Price | Free |
| Availability | All countries and regions |

---

## Submission Checklist

- [ ] App Information: Subtitle set to "Best Card at Every Store"
- [ ] App Information: Primary Category = Finance, Secondary = Utilities
- [ ] App Information: Privacy Policy URL = https://getfleece.io/privacy-policy
- [ ] Version 1.0: Description added
- [ ] Version 1.0: Keywords added
- [ ] Version 1.0: Promotional text added
- [ ] Version 1.0: Support URL = https://getfleece.io
- [ ] Version 1.0: What's New added
- [ ] Screenshots: 3 framed screenshots uploaded for 6.7" iPhone
- [ ] App Review: Contact info and notes filled in
- [ ] Pricing: Free, all regions
- [ ] Build uploaded via `ios/release.sh <TEAM_ID>` and selected in Version 1.0
- [ ] Digital Services Act: Complete trader/non-trader declaration
- [ ] Submit for Review

---

## Privacy Manifest

`ios/FleeceApp/PrivacyInfo.xcprivacy` is included in the bundle and declares:

- **NSPrivacyTracking**: false — no cross-app tracking
- **NSPrivacyCollectedDataTypes**: empty — no data collected
- **NSPrivacyAccessedAPITypes**: UserDefaults with reason `CA92.1` (user-facing wallet and profile storage)

This satisfies the App Store privacy manifest requirement in effect since May 2024.

---

## Build & Upload

Run from the `ios/` directory on a Mac with Xcode 16 and XCodeGen installed:

```bash
# Install XCodeGen if needed
brew install xcodegen

# Archive and upload to App Store Connect
./release.sh <YOUR_TEAM_ID>
```

Find your Team ID at [developer.apple.com/account](https://developer.apple.com/account) → Membership Details.

After upload, wait ~10 minutes for the build to process in App Store Connect, then select it in the Version 1.0 build field.
