# Mobile App Analytics

## Tool Selection Guide (2025)

| Stage | Best Choice | Why |
|---|---|---|
| Early-stage / MVP | **Firebase** | Free, easy Google Ads + BigQuery integration, auto-events |
| Growth / Product-led | **Amplitude** | Deep behavioral cohorts, retention analysis, funnel exploration |
| Real-time / B2B SaaS | **Mixpanel** | Fast queries, flexible dashboards, account-level analytics |
| Marketing attribution | **AppsFlyer** or **Adjust** | Install attribution, paid channel ROI, fraud prevention |
| Subscription revenue | **RevenueCat** | IAP tracking, subscription churn, LTV modeling |
| Experimentation | **Statsig** | A/B testing + analytics unified; 50–80% cheaper than alternatives |

**Common stacks:**
- Small app: Firebase Analytics + RevenueCat
- Growth startup: Amplitude + AppsFlyer + RevenueCat
- Enterprise: Mixpanel + Adjust + custom data warehouse
- Note: Microsoft Visual Studio App Center was retired March 31, 2025 — migrate if still using it

---

## Event Schema Design

### Golden Rules for Mobile Events
1. Every event is independent (no shared context like web's dataLayer)
2. Each `logEvent()` call must carry all its own parameters
3. Name events as `object_action` — consistent with web
4. Firebase: max 500 unique event names per app, 25 parameters per event
5. Amplitude/Mixpanel: no hard limits but design taxonomy carefully

### Standard Event Taxonomy

**Installation & Onboarding**
```
app_installed         install_source, device, os_version, app_version
app_first_launched    install_date, attribution_channel
onboarding_started    
onboarding_step_completed   step_number, step_name
onboarding_completed  time_to_complete_seconds
permission_granted    permission_type (notifications/camera/location)
permission_denied     permission_type
```

**Session & Navigation**
```
app_opened            session_id, source (push/organic/deeplink), app_version
screen_viewed         screen_name, previous_screen, time_on_previous_screen
app_backgrounded      session_duration, screens_visited_count
app_crashed           error_type, screen_name, stack_trace_id
```

**Feature Usage**
```
feature_used          feature_name, feature_category, usage_count
feature_completed     feature_name, completion_time_seconds
feature_abandoned     feature_name, abandonment_point, time_spent
search_performed      query, results_count, result_clicked (bool)
content_consumed      content_id, content_type, percent_consumed
```

**Conversion Events**
```
purchase_initiated    product_id, price, currency
purchase_completed    product_id, price, currency, transaction_id, payment_method
subscription_started  plan_id, plan_name, price, billing_period
subscription_cancelled plan_id, cancellation_reason, days_active
subscription_renewed  plan_id, renewal_count
in_app_purchase       item_id, item_name, price, currency
```

**Retention Signals**
```
notification_received notification_id, notification_type
notification_tapped   notification_id, notification_type
deep_link_opened      deep_link_url, source
social_share          content_id, platform
rating_prompted       trigger_event, session_count
rating_submitted      rating (1-5), feedback_text
```

---

## Firebase Implementation

```swift
// iOS (Swift)
import FirebaseAnalytics

// Log a standard event
Analytics.logEvent("feature_used", parameters: [
    "feature_name": "photo_editor" as NSString,
    "session_id": sessionId as NSString,
    "user_tier": userTier as NSString,
])

// Set user properties (persistent across events)
Analytics.setUserProperty("premium", forName: "subscription_tier")
Analytics.setUserProperty(acquisitionSource, forName: "acquisition_source")

// Set user ID (for cross-device tracking)
Analytics.setUserID(hashedUserId)
```

```kotlin
// Android (Kotlin)
import com.google.firebase.analytics.ktx.analytics
import com.google.firebase.ktx.Firebase

val analytics = Firebase.analytics

val params = Bundle().apply {
    putString("feature_name", "photo_editor")
    putString("session_id", sessionId)
    putString("user_tier", userTier)
}
analytics.logEvent("feature_used", params)

// User properties
analytics.setUserProperty("subscription_tier", "premium")
```

**Firebase limits:**
- 500 distinct event names per app
- 25 parameters per event
- 500k events/day free on Spark plan
- DebugView: enable with `adb shell setprop debug.firebase.analytics.app YOUR_PACKAGE`

---

## Amplitude Implementation

```javascript
// React Native / JS SDK
import { init, track, identify, Identify } from '@amplitude/analytics-react-native';

// Initialize
init('YOUR_API_KEY', userId, {
  trackingOptions: {
    ipAddress: false,     // privacy
    carrier: true,
    deviceManufacturer: true,
  }
});

// Track event
track('feature_used', {
  feature_name: 'photo_editor',
  session_id: sessionId,
  user_tier: userTier,
  time_in_feature_seconds: 42,
});

// Set user properties
const identifyObj = new Identify();
identifyObj.set('subscription_tier', 'premium');
identifyObj.set('acquisition_source', 'instagram_ad');
identifyObj.increment('session_count', 1);
identify(identifyObj);
```

**Amplitude strengths:**
- Cohort analysis: group users by acquisition date, plan, behavior
- Pathfinder: visualize most common event sequences
- Compass: identifies events most correlated with retention
- Funnel analysis with configurable conversion windows (up to 90 days)
- Free tier: 10M user actions/month

---

## Mixpanel Implementation

```javascript
// React Native
import { Mixpanel } from 'mixpanel-react-native';

const mixpanel = new Mixpanel('YOUR_TOKEN', true); // true = track automatically
await mixpanel.init();

// Identify user
mixpanel.identify(userId);
mixpanel.getPeople().set({
  '$name': userName,
  'subscription_tier': 'premium',
  'acquisition_source': 'organic',
  'signup_date': signupDate,
});

// Track event
mixpanel.track('Feature Used', {
  'feature_name': 'photo_editor',
  'session_id': sessionId,
  'time_spent_seconds': 42,
});
```

**Mixpanel strengths:**
- Real-time data (no batching delay)
- Self-serve cohort analysis without SQL
- Account-level analytics (group features) — ideal for B2B
- Strong funnel analysis: visualize drop-off at each step
- Retention: N-day, unbounded, bracket retention charts

---

## AppsFlyer / Adjust Attribution

For paid user acquisition, you need a Mobile Measurement Partner (MMP):

```javascript
// AppsFlyer React Native SDK
import appsFlyer from 'react-native-appsflyer';

appsFlyer.initSdk({
  devKey: 'YOUR_DEV_KEY',
  isDebug: false,
  appId: 'YOUR_APP_ID',   // iOS App ID
  onInstallConversionDataListener: true,
  onDeepLinkListener: true,
  timeToWaitForATTUserAuthorization: 10,  // iOS ATT timeout
}, (result) => console.log(result));

// Log in-app events for attribution
appsFlyer.logEvent('af_purchase', {
  af_revenue: 29.99,
  af_currency: 'USD',
  af_content_id: 'premium_plan',
});
```

**AppsFlyer tracks:**
- Which ad → which install (Meta, Google, TikTok, etc.)
- Post-install events: purchase, subscription, level complete
- Re-engagement attribution
- Fraud detection (invalid traffic filtering)
- SKAdNetwork (iOS 14.5+ privacy-preserving attribution)

---

## Key Mobile Metrics & Analysis

### Retention Analysis
```
Day 1 retention:   % of users who return 1 day after install
Day 7 retention:   % who return after 7 days
Day 30 retention:  % who return after 30 days

Industry benchmarks (2025):
  D1:  20–40% (good), >40% (excellent)
  D7:  10–20% (good), >20% (excellent)
  D30: 5–10% (good), >10% (excellent)

80% of Android users drop within 3 days
90% of all users leave within 30 days without re-engagement
```

### Session & Feature Analysis
```python
# Identify "power users" — top 10% by engagement
def classify_user(user_events: list) -> str:
    sessions_30d = count_sessions(user_events, days=30)
    features_used = len(set(e["feature"] for e in user_events))
    purchases = count_event(user_events, "purchase_completed")
    
    if sessions_30d >= 20 and features_used >= 5:
        return "power_user"
    elif sessions_30d >= 7:
        return "engaged"
    elif sessions_30d >= 2:
        return "casual"
    else:
        return "at_risk_churn"
```

### Churn Prediction Signals
Watch for these churn precursors:
- Session frequency declining (was daily → now weekly)
- Feature usage narrowing (using fewer features)
- Notification opt-out
- App moved to last page of home screen (inferred from reduced opens)
- Support contact (negative interaction signal)
- Subscription cancellation started but not completed

**Churn intervention:** Trigger push notification or in-app message when session gap exceeds 7 days.

---

## Privacy Considerations (2025)

### iOS ATT (App Tracking Transparency)
- Show ATT prompt only after user has experienced value
- Opt-in rate: 30–40% globally
- Without IDFA: rely on SKAdNetwork (limited, delayed) + first-party ID
- Use AppsFlyer's aggregated attribution for non-consenting users

### Android Privacy Sandbox
- Google phasing out Advertising ID for non-consenting users
- Moving to Privacy Sandbox APIs (Topics, Protected Audience)
- Impact: similar to iOS ATT, plan for reduced signal

### Data Minimization Best Practices
- Hash user IDs before sending to any third-party analytics platform
- Don't send raw PII in event properties
- Implement data deletion APIs for GDPR/CCPA user rights requests
- Firebase: disable IP collection for GDPR markets
- Amplitude/Mixpanel: configure EU data residency if serving EU users
