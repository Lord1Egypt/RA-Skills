# GaggiMate WebSocket API — Profile Operations

Connect to `ws://gaggimate.local/ws`. Messages are JSON with a `tp` field.

## List Profiles
```json
→ {"tp": "req:profiles:list", "rid": "unique-id"}
← {"tp": "res:profiles:list", "rid": "...", "profiles": [...]}
```

## Load Profile
```json
→ {"tp": "req:profiles:load", "rid": "...", "id": "profile-uuid"}
← {"tp": "res:profiles:load", "rid": "...", "profile": {...}}
```

## Save Profile (create or update)
```json
→ {"tp": "req:profiles:save", "rid": "...", "profile": {<full profile object>}}
← {"tp": "res:profiles:save", "rid": "...", "profile": {<saved profile>}}
```

## Delete Profile
```json
→ {"tp": "req:profiles:delete", "rid": "...", "id": "profile-uuid"}
← {"tp": "res:profiles:delete", "rid": "..."}
```

## Select Profile (set active on machine)
```json
→ {"tp": "req:profiles:select", "rid": "...", "id": "profile-uuid"}
← {"tp": "res:profiles:select", "rid": "..."}
```

## Favorite Profile (show on machine display)
```json
→ {"tp": "req:profiles:favorite", "rid": "...", "id": "profile-uuid"}
← {"tp": "res:profiles:favorite", "rid": "..."}
```

## Unfavorite Profile
```json
→ {"tp": "req:profiles:unfavorite", "rid": "...", "id": "profile-uuid"}
← {"tp": "res:profiles:unfavorite", "rid": "..."}
```

## Status Events (continuous)
```json
← {"tp": "evt:status", "ct": 93.2, "tt": 93, "pr": 8.5, "fl": 2.1, "pt": 9, "m": 1, "p": "My Profile", "cp": true, "cd": true}
```
Fields: ct=current temp, tt=target temp, pr=pressure, fl=flow, pt=target pressure, m=mode, p=profile label, cp=pressure capable, cd=dimming capable
