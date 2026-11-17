# iOS Integration — Apple Search Ads

Complete guide for integrating Apple Search Ads attribution in your iOS app. Reading and reconciling the resulting numbers is the analysis side — `measurement.md`.

Contents: Overview · AdServices Framework · SKAdNetwork · MMP Integration · Testing Attribution · Best Practices

## Overview

Two complementary systems:
1. **AdServices** (iOS 14.3+) — Direct attribution with campaign details
2. **SKAdNetwork** — Privacy-focused conversion tracking

Mechanics that shape the integration:
- The AdServices attribution token is valid for 24 hours after generation — fetch and resolve it on first launch; there is no second chance after the window.
- Attribution works **without** ATT consent: it returns campaign-level IDs, no user identifiers.
- Apple's endpoint can return 404 before attribution data is ready. Apple's documented guidance: retry up to 3 times at 5-second intervals before treating the install as organic. Skipping the retry silently undercounts paid installs.
- The old iAd attribution API is dead (shut down 2023) — AdServices is the only direct path.

## AdServices Framework

### Setup

Add AdServices framework to your Xcode project:
1. Select your target → General → Frameworks
2. Add `AdServices.framework`

### Basic Implementation

```swift
import AdServices

class AttributionManager {
    
    static let shared = AttributionManager()
    
    /// Call this on app launch or first open
    func fetchAttribution() async {
        // Only fetch once per install
        guard !UserDefaults.standard.bool(forKey: "asa_attribution_fetched") else {
            return
        }
        
        do {
            // Get token from device
            let token = try AAAttribution.attributionToken()
            
            // Send to Apple's attribution endpoint
            let attribution = try await fetchAttributionData(token: token)
            
            // Process attribution
            await handleAttribution(attribution)
            
            // Mark as fetched
            UserDefaults.standard.set(true, forKey: "asa_attribution_fetched")
            
        } catch {
            // Not from ASA or network error
            print("Attribution error: \(error)")
        }
    }
    
    private func fetchAttributionData(token: String) async throws -> AttributionResponse {
        var request = URLRequest(url: URL(string: "https://api-adservices.apple.com/api/v1/")!)
        request.httpMethod = "POST"
        request.setValue("text/plain", forHTTPHeaderField: "Content-Type")
        request.httpBody = token.data(using: .utf8)
        
        // Apple's guidance: data may not be ready yet — on 404, retry up to 3x, 5s apart
        for attempt in 1...3 {
            let (data, response) = try await URLSession.shared.data(for: request)
            guard let httpResponse = response as? HTTPURLResponse else {
                throw AttributionError.invalidResponse
            }
            if httpResponse.statusCode == 200 {
                return try JSONDecoder().decode(AttributionResponse.self, from: data)
            }
            if httpResponse.statusCode == 404 && attempt < 3 {
                try await Task.sleep(nanoseconds: 5_000_000_000)
                continue
            }
            throw AttributionError.serverError
        }
        throw AttributionError.serverError
    }
    
    private func handleAttribution(_ response: AttributionResponse) async {
        guard response.attribution else {
            // Not attributed to Apple Search Ads
            return
        }
        
        // Send to your analytics backend
        await sendToAnalytics(
            campaignId: response.campaignId,
            adGroupId: response.adGroupId,
            keywordId: response.keywordId,
            clickDate: response.clickDate
        )
        
        // Store locally for reference
        UserDefaults.standard.set(response.campaignId, forKey: "asa_campaign_id")
    }
    
    private func sendToAnalytics(campaignId: Int?, adGroupId: Int?, 
                                  keywordId: Int?, clickDate: String?) async {
        // Your analytics implementation
        // Example: Mixpanel, Amplitude, Firebase, or your own backend
    }
}

struct AttributionResponse: Codable {
    let attribution: Bool
    let orgId: Int?
    let campaignId: Int?
    let adGroupId: Int?
    let keywordId: Int?
    let creativeSetId: Int?
    let conversionType: String?
    let clickDate: String?
    let countryOrRegion: String?
}

enum AttributionError: Error {
    case serverError
    case invalidResponse
}
```

### Call on App Launch

```swift
// In your AppDelegate or App struct
import SwiftUI

@main
struct MyApp: App {
    init() {
        Task {
            await AttributionManager.shared.fetchAttribution()
        }
    }
    
    var body: some Scene {
        WindowGroup {
            ContentView()
        }
    }
}
```

### With App Tracking Transparency

If you also request ATT permission, coordinate the timing:

```swift
import AppTrackingTransparency

func requestTrackingAndAttribution() async {
    // First, try to get attribution (works regardless of ATT)
    await AttributionManager.shared.fetchAttribution()
    
    // Then request ATT for other tracking (Facebook, etc.)
    if #available(iOS 14, *) {
        await ATTrackingManager.requestTrackingAuthorization()
    }
}
```

**Note:** AdServices works WITHOUT ATT permission. You can get campaign-level attribution even if the user denies tracking.

## SKAdNetwork

Facts that shape the conversion strategy:
- Conversion value is 6 bits (0-63). Design the full mapping **before launch** — installs measured under an old mapping cannot be reinterpreted.
- SKAN 4 sends up to three postbacks per install, over windows of 0-2, 3-7, and 8-35 days. The fine-grained value (0-63) arrives only in the first postback; the second and third carry only the coarse value (low/medium/high).
- Under SKAN 3, every conversion update resets a 24-hour timer; the postback fires with a randomized delay after it expires. Consequence: never expect same-day install counts, and never daypart on SKAN install data.
- Fine-grained values are withheld below Apple's crowd-anonymity thresholds — low-volume campaigns receive coarse or null values by design, not by bug.

### Info.plist Setup

Add Apple's network ID to your Info.plist:

```xml
<key>SKAdNetworkItems</key>
<array>
    <dict>
        <key>SKAdNetworkIdentifier</key>
        <string>cstr6suwn9.skadnetwork</string>
    </dict>
    <!-- Add other ad network IDs as needed -->
</array>
```

### Basic Implementation

```swift
import StoreKit

class SKAdNetworkManager {
    
    static let shared = SKAdNetworkManager()
    
    /// Call on app install/first launch
    func registerInstall() {
        if #available(iOS 16.1, *) {
            // SKAN 4: coarseValue is available from iOS 16.1 only
            SKAdNetwork.updatePostbackConversionValue(0, coarseValue: .low) { error in
                if let error = error {
                    print("SKAdNetwork register error: \(error)")
                }
            }
        } else if #available(iOS 15.4, *) {
            // iOS 15.4–16.0: fine-only completion-handler variant
            SKAdNetwork.updatePostbackConversionValue(0) { error in
                if let error = error {
                    print("SKAdNetwork register error: \(error)")
                }
            }
        } else if #available(iOS 14.0, *) {
            SKAdNetwork.updateConversionValue(0)
        }
    }
    
    /// Update conversion value when user completes valuable actions
    func updateConversion(value: Int, coarse: SKAdNetwork.CoarseConversionValue? = nil) {
        guard value >= 0 && value <= 63 else { return }
        
        if #available(iOS 16.1, *) {
            SKAdNetwork.updatePostbackConversionValue(value, coarseValue: coarse ?? .medium) { error in
                if let error = error {
                    print("SKAdNetwork update error: \(error)")
                }
            }
        } else if #available(iOS 15.4, *) {
            // Fine-only variant — coarseValue does not exist before 16.1
            SKAdNetwork.updatePostbackConversionValue(value) { error in
                if let error = error {
                    print("SKAdNetwork update error: \(error)")
                }
            }
        } else if #available(iOS 14.0, *) {
            SKAdNetwork.updateConversionValue(value)
        }
    }
}
```

### Conversion Value Strategy

Map user actions to conversion values (0-63):

```swift
enum ConversionEvent: Int {
    // Engagement (1-10)
    case appOpen = 1
    case session5Minutes = 3
    case session15Minutes = 5
    case returnDay2 = 8
    case returnDay7 = 10
    
    // Feature Usage (11-30)
    case completedOnboarding = 15
    case usedCoreFeature = 20
    case createdContent = 25
    case invitedFriend = 30
    
    // Monetization Signals (31-50)
    case viewedPaywall = 32
    case startedTrial = 40
    case addedPaymentMethod = 45
    case viewedPremiumFeature = 48
    
    // Revenue (51-63)
    case purchaseTier1 = 51  // $0.99 - $4.99
    case purchaseTier2 = 55  // $5 - $19.99
    case purchaseTier3 = 58  // $20 - $49.99
    case purchaseTier4 = 61  // $50 - $99.99
    case purchaseTier5 = 63  // $100+
}

extension SKAdNetworkManager {
    
    func trackEvent(_ event: ConversionEvent) {
        // Only update if new value is higher
        let currentValue = UserDefaults.standard.integer(forKey: "skan_conversion_value")
        
        if event.rawValue > currentValue {
            updateConversion(value: event.rawValue)
            UserDefaults.standard.set(event.rawValue, forKey: "skan_conversion_value")
        }
    }
    
    func trackPurchase(revenue: Decimal) {
        let event: ConversionEvent
        
        switch revenue {
        case ..<5: event = .purchaseTier1
        case 5..<20: event = .purchaseTier2
        case 20..<50: event = .purchaseTier3
        case 50..<100: event = .purchaseTier4
        default: event = .purchaseTier5
        }
        
        trackEvent(event)
    }
}
```

### Usage Throughout App

```swift
// On onboarding complete
SKAdNetworkManager.shared.trackEvent(.completedOnboarding)

// On purchase
SKAdNetworkManager.shared.trackPurchase(revenue: 9.99)

// On feature use
SKAdNetworkManager.shared.trackEvent(.usedCoreFeature)
```

## MMP Integration

If using a Mobile Measurement Partner (AppsFlyer, Adjust, Singular, Kochava, Branch), they handle most of this automatically.

### AppsFlyer Example

```swift
import AppsFlyerLib

// In AppDelegate
func application(_ application: UIApplication, 
                 didFinishLaunchingWithOptions launchOptions: [UIApplication.LaunchOptionsKey: Any]?) -> Bool {
    
    AppsFlyerLib.shared().appsFlyerDevKey = "YOUR_DEV_KEY"
    AppsFlyerLib.shared().appleAppID = "YOUR_APP_ID"
    AppsFlyerLib.shared().delegate = self
    
    // Enable Apple Search Ads attribution
    AppsFlyerLib.shared().waitForATTUserAuthorization(timeoutInterval: 60)
    
    return true
}

func applicationDidBecomeActive(_ application: UIApplication) {
    AppsFlyerLib.shared().start()
}

// Delegate method for attribution data
extension AppDelegate: AppsFlyerLibDelegate {
    func onConversionDataSuccess(_ data: [AnyHashable: Any]) {
        if let source = data["media_source"] as? String,
           source == "Apple Search Ads" {
            // Attributed to ASA
            let campaign = data["campaign"] as? String
            let adGroup = data["adgroup"] as? String
        }
    }
}
```

### Adjust Example

```swift
import Adjust

// In AppDelegate
func application(_ application: UIApplication, 
                 didFinishLaunchingWithOptions launchOptions: [UIApplication.LaunchOptionsKey: Any]?) -> Bool {
    
    let config = ADJConfig(appToken: "YOUR_TOKEN", environment: ADJEnvironmentProduction)
    
    // Enable Apple Search Ads attribution
    config?.allowAdServicesInfoReading = true
    config?.allowIdfaReading = true
    
    Adjust.appDidLaunch(config)
    
    return true
}
```

## Testing Attribution

### Sandbox Testing

1. Build app with Debug configuration
2. Install on test device (not simulator)
3. Search for your app in App Store
4. Tap ad if visible, or search and tap result
5. Install app
6. Attribution should fire on first launch

### Debugging

```swift
// Add debug logging
func fetchAttribution() async {
    do {
        let token = try AAAttribution.attributionToken()
        print("[ASA] Token: \(token.prefix(50))...")
        
        let attribution = try await fetchAttributionData(token: token)
        print("[ASA] Attribution: \(attribution)")
        
    } catch {
        print("[ASA] Error: \(error)")
    }
}
```

### Common Issues

| Issue | Cause | Solution |
|-------|-------|----------|
| Token error | Simulator | Use real device — the simulator has no attribution token |
| 404 from endpoint | Attribution data not ready yet | Retry up to 3x at 5s intervals (Apple's guidance), then treat as organic |
| `attribution: false` | Organic install | Expected — most installs are not from ads; not an error |
| No attribution despite ad tap | Token fetched later than 24h after generation | Fetch and resolve on first launch, within the token window |
| Server error | Apple API down | Retry with backoff |

## Best Practices

1. **Fetch on first launch, off the main thread** — the token window is 24h and you get one shot per install; retry 404s (→ Overview)
2. **Persist the attribution result immediately** — token and window expire; re-fetching later returns nothing
3. **`attribution: false` is the normal case** — most installs are organic; log it, don't alert on it
4. **Design the 0-63 mapping around your paywall funnel** — updates only move the value upward, so order events by revenue proximity, not by chronology
5. **If an MMP is installed, let it own both AdServices and SKAN** — a second direct integration double-counts and can clobber the MMP's conversion values
6. **Use both systems** — AdServices gives campaign/keyword detail for optimization; SKAN gives the privacy-safe install counts Apple's ecosystem reports against
