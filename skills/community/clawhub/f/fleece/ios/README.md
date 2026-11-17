# Fleece iOS App

Native SwiftUI iPhone app that:

1. Tracks your location with CoreLocation
2. Uses **Apple MapKit `MKLocalSearch`** (free, no API key) to identify the store you're in
3. Maps `MKPointOfInterestCategory` → **MCC category** (dining, groceries, gas, hotels, etc.)
4. Ranks all cards by effective reward rate for that category
5. Fires a **local push notification**: *"Use Amex Gold · 4x Dining = 7.2% back (Amex MR)"*

**Zero per-request cost.** All place lookups stay on-device via Apple's MapKit framework.

---

## Setup

No API keys needed. Just:

1. Open Xcode → create a new **iOS App** project
   - Product Name: `FleeceApp`
   - Interface: **SwiftUI** / Language: **Swift**
   - Bundle ID: `io.getfleece.app`

2. Drag all `.swift` files from this directory into the Project Navigator (preserving folder groups)

3. Replace the generated `Info.plist` with the one in this directory

4. Under **Signing & Capabilities**, add:
   - **Background Modes → Location updates** (optional, for background detection)

5. Build and run on a physical device (CoreLocation requires real hardware)

---

## Architecture

```
FleeceApp/
├── FleeceApp.swift          — App entry; requests location + notification permissions
├── ContentView.swift        — TabView: Home / Wallet / Settings
├── AppState.swift           — Central @ObservableObject: orchestrates search + wallet
├── Config.swift             — Detection radius, notification cooldown constants
│
├── Views/
│   ├── HomeView.swift               — MapKit map + current place banner + card scroll
│   ├── RecommendationCardView.swift — Horizontal card chips + full recommendations sheet
│   ├── WalletView.swift             — Add/remove cards from wallet
│   └── SettingsView.swift           — App info (no API key needed)
│
├── Managers/
│   ├── LocationManager.swift     — CLLocationManager wrapper (@MainActor)
│   ├── PlacesService.swift       — MKLocalSearch wrapper (free, actor)
│   └── NotificationManager.swift — UNUserNotificationCenter, 5-min cooldown
│
├── Models/
│   ├── MCCCategory.swift   — MKPointOfInterestCategory → MCC mapping
│   ├── CreditCard.swift    — Card model + Color(hex:) extension
│   ├── NearbyPlace.swift   — Place model + MKMapItem conversion
│   └── Recommendation.swift — Ranked recommendation result
│
└── Services/
    ├── CardDatabase.swift   — 9 hard-coded US cards (Chase, Amex, Citi, CapOne, Bilt)
    └── CardRecommender.swift — Sorts cards by effective rate, wallet cards first
```

## MKPointOfInterestCategory → MCCCategory Mapping

| MCCCategory | MKPointOfInterestCategory values |
|---|---|
| Dining | restaurant, cafe, bakery, brewery, winery, nightlife |
| Groceries | foodMarket |
| Gas | gasStation |
| Hotels | hotel |
| Flights | airport |
| Transit | publicTransport |
| Drugstore | pharmacy |
| Entertainment | movieTheater, stadium, musicVenue, amusementPark, bowling, zoo, aquarium |
| Shopping | store, clothing |

## Card Database (9 cards)

| Card | Top Category | Effective Rate |
|---|---|---|
| Amex Gold | Dining / Groceries | 4x → 7.2% |
| Amex Platinum | Flights / Hotels | 5x → 10% |
| Chase Sapphire Reserve | Dining / Travel | 3x → 4.5% |
| Chase Sapphire Preferred | Dining / Groceries | 3x → 3.75% |
| Chase Freedom Unlimited | Dining / Drugstore | 3x → 3% + 1.5x base |
| Amex Blue Cash Preferred | Groceries / Streaming | 6x → 6% cash |
| Bilt Mastercard | Dining | 3x → 4.5% |
| Capital One Venture X | Hotels / Flights | 10x → 17% |
| Citi Double Cash | Everything | 2x → 2% cash |

## Notification Example

```
Title:  🍽️ Ippudo Ramen NYC
Body:   Use Gold Card · 4x Dining = 7.2% back (Amex MR)
Action: View All Cards  →  opens RecommendationsSheetView
```
