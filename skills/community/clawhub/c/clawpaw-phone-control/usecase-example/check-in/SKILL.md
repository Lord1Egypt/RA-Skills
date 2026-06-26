---
name: check-in
description: Location check-in with auto photo, geocoding, weather, and a generated caption
metadata: { "openclaw": { "emoji": "📸" } }
---

# Check-In

One command to create a full check-in: take a photo, get location + address, fetch weather, and generate a caption.

## Steps

### 1. Take a Photo

Capture the current scene with the rear camera:

```
nodes({ action: "camera_snap", facing: "back" })
```

If the user wants a selfie or group shot, use the front camera:
```
nodes({ action: "camera_snap", facing: "front" })
```

### 2. Get Location Details

Call `clawpaw_get_context` for current location and time.

Call `clawpaw_reverse_geocode` (using context coordinates) to get:
- Province / City / District
- Street / Road name
- Nearby landmark name

### 3. Get Weather

Call `clawpaw_weather` (current coordinates, forecast=false) for real-time conditions.

### 4. Generate Check-In Card

Combine everything into a check-in record:

```
📸 Check-In

📍 [Place name]
   [Full address]

🕐 [YYYY-MM-DD HH:MM] [Weekday]
🌤️ [Weather] [Temperature]°C

✨ [AI-generated one-liner]

[Attached photo]
```

### Caption Generation Guide

Generate a short, fitting one-liner based on the scene:
- Nature/scenery → poetic ("Every path leads to a new horizon")
- City streets → observational ("The city hums with stories untold")
- Food/restaurant → warm ("Good food, good mood")
- Travel → adventurous ("Another pin on the map")
- Workplace → light humor ("Clocking in, one day at a time")

Adjust tone by weather:
- Sunny → bright, upbeat
- Rainy → reflective, cozy
- Overcast → calm, contemplative

## When to Use

- User says "check in", "mark this spot", "log this place"
- User says "take a photo for the record", "commemorate this"
- User arrives at a new place and wants to capture the moment

## When NOT to Use

- User just wants to take a photo (no check-in intent)
- User is talking about attendance/clock-in at work
- User asks to photograph a specific object (not a location check-in)
