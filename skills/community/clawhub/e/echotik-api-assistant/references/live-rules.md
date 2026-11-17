# Live Module Rules

## 1. Module Scope

All live-room or livestream-detail questions should be routed through this module first.

## 2. Live Detail - Realtime

- Documentation: `https://opendocs.echotik.live/realtime/live/detail.md`
- Purpose: retrieve live-room detail through `room_id + user_id`

### Rules

- This endpoint only works while the livestream is currently active.
- If the livestream has already ended, the endpoint may not return data.

## 3. Module Routing

- For historical creator live sessions rather than an active room, use the creator live-history module instead of realtime live detail.
