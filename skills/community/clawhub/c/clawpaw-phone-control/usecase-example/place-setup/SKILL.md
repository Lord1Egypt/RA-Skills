---
name: place-setup
description: Register and manage known places (home, office, gym, etc.) for location-aware features
metadata: { "openclaw": { "emoji": "📍" } }
---

# Place Setup

Help the user register, view, and manage their known places. These places power all location-aware features — arrival/departure detection, trajectory tracking, commute stats, overwork alerts, and context injection.

## When to Use

- User says "save this place", "register home", "add my office", "set up places"
- User asks "what places do I have", "show my places", "where is my home set"
- User wants to remove or update a place
- User just installed the plugin and needs initial setup
- First-time setup: guide the user to register at least HOME and COMPANY

## When NOT to Use

- User is asking about their current location (use `clawpaw_get_context` directly)
- User is asking for nearby places to visit (use food-finder or clawpaw_nearby)

## Workflow: Register a New Place

### Option A: User is currently at the place

1. Call `clawpaw_get_context` to get current coordinates
2. Call `clawpaw_reverse_geocode` with the coordinates to get a human-readable address
3. Confirm with the user: "You're currently at [address]. Save this as [label]?"
4. Call `clawpaw_save_place` with:
   - `tag`: HOME, COMPANY, or OTHER
   - `label`: user-provided name (e.g. "Home", "Office", "Gym")
   - `latitude` / `longitude`: from current location
   - `radiusKm`: 0.3 for precise places (apartment, office building), 0.5 for general areas

### Option B: User provides an address

1. Call `clawpaw_geocode` with the address to get coordinates
2. Confirm coordinates and resolved address with the user
3. Call `clawpaw_save_place` with the resolved coordinates

### Option C: User provides coordinates directly

1. Call `clawpaw_save_place` directly with the provided lat/lng

## Workflow: View Places

1. Call `clawpaw_get_places`
2. Format output:

```
📍 Your registered places:

1. 🏠 Home — (lat, lng) r=0.3km
2. 🏢 Office — (lat, lng) r=0.5km
3. 🏋️ Gym — (lat, lng) r=0.3km
```

Use icons based on tag: 🏠 HOME, 🏢 COMPANY, 📌 OTHER

## Workflow: Remove a Place

1. Call `clawpaw_get_places` to show the list
2. Ask the user which one to remove
3. Call `clawpaw_remove_place` with the place ID
4. Confirm removal

## Tag Selection Guide

| Tag | When to use | Examples |
|-----|-------------|---------|
| HOME | User's residence | Home, Apartment, Parents' house |
| COMPANY | Workplace | Office, Co-working space, Studio |
| OTHER | Everything else | Gym, School, Favorite café, Supermarket |

## Radius Guide

| Place type | Recommended radius |
|------------|-------------------|
| Apartment / House | 0.2 - 0.3 km |
| Office building | 0.3 - 0.5 km |
| Campus / Park | 0.5 - 1.0 km |
| General area | 1.0 km |

## First-Time Setup

If the user has no places registered, proactively guide them:

```
Looks like you haven't set up any places yet. Location-aware features (trajectory tracking, overwork alerts, commute stats) work best with at least a Home and Office registered.

Want to set them up now? You can:
1. Save your current location as a place
2. Tell me an address to register
```
