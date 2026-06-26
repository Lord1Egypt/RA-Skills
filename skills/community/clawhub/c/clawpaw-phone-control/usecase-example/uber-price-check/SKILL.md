---
name: uber-price-check
description: Check Uber ride prices for a destination. Use when user says "how much is an Uber to...", "check ride prices", "Uber price check", etc.
disable-model-invocation: true
---

# Uber Price Check

Check ride prices on Uber for a given destination. Uber has no consumer API — pricing can only be seen through the app.

Use `snapshot` throughout. Avoid `screenshot` unless snapshot returns no useful elements.

## Package

`com.ubercab` (Uber) or `com.ubercab.eats` (Uber Eats)

**Note:** If Uber is not installed, inform the user. Check with `list_apps` first.

## Step 1 — Launch Uber

```
shell → monkey -p com.ubercab -c android.intent.category.LAUNCHER 1
```

`snapshot` — confirm Uber is open and logged in. If a login/signup screen appears, inform the user and stop.

## Step 2 — Enter destination

1. `snapshot` — the home screen typically shows "Where to?" / "去哪里？" input field
2. `tap` the destination input field
3. `type_text` with the destination from `$ARGUMENTS` or as specified by the user
4. `snapshot` — wait for autocomplete suggestions to appear
5. `tap` the most relevant suggestion from the list

## Step 3 — Read ride options

After selecting a destination, Uber shows available ride types with prices.

1. `snapshot` — read the ride options panel. Look for:
   - Ride type names: "UberX", "Uber Comfort", "UberXL", "Uber Black", etc.
   - Price estimates for each option
   - Estimated arrival time (ETA)
   - Estimated trip duration
2. If not all options are visible, `swipe up` on the ride options panel to see more
3. Collect all ride types, prices, and ETAs

## Step 4 — Report to user

Present a clear price comparison:

```
Uber prices to [Destination]:

| Ride Type     | Price      | Arrival | Trip Time |
|---------------|------------|---------|-----------|
| UberX         | $12-15     | 3 min   | 18 min    |
| Uber Comfort  | $16-20     | 5 min   | 18 min    |
| UberXL        | $20-25     | 8 min   | 18 min    |
| Uber Black    | $30-38     | 6 min   | 18 min    |
```

Ask if the user wants to book a ride.

## Step 5 — Book ride (if requested)

1. `snapshot` — find the desired ride type and `tap` to select it
2. Look for the "Confirm" / "确认" button
3. **Confirm with the user** before tapping: "Book UberX for $12-15? This will request a ride."
4. After user confirms, `tap` Confirm
5. `snapshot` — verify the ride is confirmed (shows driver matching screen)

## Important Notes

1. **Always confirm before booking** — this commits real money and requests a real ride
2. **Surge pricing:** Uber may show surge multipliers during busy times. Alert the user if prices seem unusually high
3. **Uber UI varies by region** — element labels may be in different languages. Common identifiers include "fare_estimate", "vehicle_view", "product_name"
4. **Payment method:** The default payment method will be used. If the user wants to change it, look for the payment icon (usually bottom of ride options)
5. **Pickup location:** Uber uses the phone's GPS for pickup. If the user wants a different pickup point, they need to adjust it on the map before entering a destination
6. **If Uber is not installed** but user wants ride prices, suggest checking Lyft (`com.lyft.android`) or other ride-hailing apps available on the device
