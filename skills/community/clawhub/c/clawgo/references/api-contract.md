# API Contract

## 1. Entitlement Check

Endpoint:

`POST /v1/entitlements/check`

Request:

```json
{
  "user_id": "u_123",
  "feature": "hd_image",
  "context": {
    "surface": "proactive_update",
    "timestamp": "2026-03-09T10:00:00Z"
  }
}
```

Response:

```json
{
  "allowed": false,
  "tier": "free",
  "reason": "feature_not_in_plan",
  "upgrade_url": "https://example.com/upgrade"
}
```

## 2. Usage Metering

Endpoint:

`POST /v1/usage/record`

Request:

```json
{
  "user_id": "u_123",
  "feature": "proactive_update",
  "units": 1,
  "metadata": {
    "destination": "Lisbon",
    "is_premium": false
  }
}
```

## 3. Memory Sync (Optional)

Endpoint:

`POST /v1/memory/tags`

Request:

```json
{
  "user_id": "u_123",
  "tags": ["food", "nature", "photography"],
  "source": "owner_interaction"
}
```

## 4. Failure Handling

If entitlement API fails:

1. Fallback to free tier behavior
2. Log `entitlement_degraded=true`
3. Continue gameplay without user-facing errors

## 5. Image Generation

Endpoint:

`POST /v1/media/image`

Request:

```json
{
  "user_id": "u_123",
  "chapter": "港口篇",
  "expression": "打卡虾",
  "destination": "Lisbon",
  "topic_angle": "coastal sunset walk",
  "image_prompt": "same mascot identity as 虾游记 icon, bright red cartoon crayfish, harbor light..."
}
```

Response:

```json
{
  "ok": true,
  "mode": "image_gen",
  "image_url": "https://example.com/media/lisbon-shrimp.png"
}
```

## 6. TTS Voice

Endpoint:

`POST /v1/media/tts`

Request:

```json
{
  "user_id": "u_123",
  "voice_style": "warm-smug-travel-companion",
  "script": "旅伴，我发来一张新明信片。"
}
```

Response:

```json
{
  "ok": true,
  "audio_url": "https://example.com/media/lisbon-shrimp.mp3",
  "duration_ms": 18400
}
```
