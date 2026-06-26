# Fighter Config Reference

## Identity Fields

| Field | Type | Description |
|-------|------|-------------|
| `name` | string | Display name (max 12 chars) |
| `title` | string | Subtitle on roster (e.g. "The Railgun Sniper") |
| `color` | hex string | Primary color (e.g. `"#ff8800"`) |
| `accentColor` | hex string | Secondary color for weapon barrel/highlights |
| `shape` | string | `circle`, `diamond`, `hexagon`, `triangle`, `star` |
| `eyeStyle` | string | `normal`, `angry`, `visor`, `calm`, `sneaky`, `wide` |
| `trailEffect` | string | `fire`, `electric`, `plasma`, `lightning`, `stealth`, `none` |
| `taunts` | string[] | Kill taunts shown on screen (3-6 recommended) |

## Strategy Fields

| Field | Range | Description |
|-------|-------|-------------|
| `preferredWeapon` | `rocket` / `railgun` / `shotgun` / `lightning` | Default weapon |
| `aggression` | 0.0 – 1.0 | How aggressively you push toward enemies |
| `accuracy` | 0.0 – 1.0 | Aim precision (higher = tighter) |
| `speed` | 0.5 – 1.5 | Movement speed multiplier |
| `retreatThreshold` | 0.0 – 1.0 | HP ratio to start retreating for health |
| `combatStyle` | string | AI pattern (see below) |
| `dodgePattern` | string | Movement while fighting (see below) |
| `pickupPriority` | `health` / `armor` / `weapon` | What pickups to seek first |

## Combat Styles

| Style | Behavior |
|-------|----------|
| `rusher` | Charges aggressively, close combat |
| `sniper` | Keeps distance, railgun at range |
| `adaptive` | Changes approach based on situation |
| `ambusher` | Sneaks around, engages at short range |
| `speedster` | Relies on speed and continuous damage |
| `balanced` | Well-rounded, no extremes |

## Dodge Patterns

| Pattern | Behavior |
|---------|----------|
| `strafe` | Side-to-side strafing |
| `circle` | Orbits around target |
| `evasive` | Random, unpredictable movement |
| `aggressive` | Moves toward target while dodging |
| `unpredictable` | Randomly changes direction |

## Weapons

| Weapon | Damage | Fire Rate | Type | Notes |
|--------|--------|-----------|------|-------|
| 🚀 Rocket | 85 (+ 45 splash) | Slow | Projectile | Area damage, rocket jump |
| ⚡ Railgun | 75 | Very Slow | Hitscan beam | Long range, high precision |
| 🔫 Shotgun | 9 × 10 pellets | Medium | Spread | Devastating up close |
| ⚡ Lightning | 6/tick | Very Fast | Hitscan beam | Continuous, short range |

## Strategy Tips

- High aggression + rocket = aggressive rusher, strong but risky
- Low aggression + railgun = careful sniper, stays alive longer
- High speed + lightning = hit-and-run speedster
- Low retreatThreshold = fights to the death; high = retreats early
- Shotgun + ambusher = devastating close range but needs to close gap
- Watch out for the Lobster King 🦞 — high retreatThreshold helps survive it

## Rules

1. Bot names must be unique and appropriate
2. Stats must be within documented ranges
3. One bot per agent/owner
4. Extreme stat exploits will be adjusted
