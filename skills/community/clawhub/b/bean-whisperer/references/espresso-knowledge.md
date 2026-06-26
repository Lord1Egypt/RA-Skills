# Espresso Profile Knowledge Base

## Rancilio Silvia + GaggiMate Pro Specifics

### Temperature
- GaggiMate measures **boiler wall temperature** via M3 thermocouple
- Default temp offset for Silvia: **5°C** (configured in GaggiMate settings, NOT in profiles)
- Profile temperature = **desired brew water temperature** (offset applied automatically)
- PID values: 112.315, 0.658, 1436.887
- Boiler refill plugin recommended (heating element sits in water)

### Pressure System
- GaggiMate Pro has pressure transducer for closed-loop pressure control
- Stock Silvia vibratory pump; pressure profiling via PWM dimmer control
- Max practical pressure: ~12 bar (stock OPV)

## Temperature Guidelines by Roast Level

| Roast Level | Brew Temp (°C) | Notes |
|-------------|---------------|-------|
| Light | 94-96 | Higher temp extracts more from dense beans |
| Medium-Light | 92-94 | Sweet spot for specialty single origins |
| Medium | 90-93 | Most versatile range |
| Medium-Dark | 88-91 | Lower to avoid bitterness |
| Dark | 85-89 | Much lower; oils extract fast |

## Dose & Ratio Guidelines

### 18g Basket
- Dose: 17-18g
- Espresso (1:2): 34-36g out
- Ristretto (1:1.5): 25-27g out
- Lungo (1:2.5): 42-45g out
- Best for: Standard shots, most beans

### 20g Basket  
- Dose: 19-20g
- Espresso (1:2): 38-40g out
- Ristretto (1:1.5): 28-30g out
- Lungo (1:2.5): 47-50g out
- Best for: Lighter roasts needing more extraction, milk drinks

### Basket Recommendation Logic
- **Light roasts / fruity single origins** → 20g (more coffee = more extraction surface)
- **Medium roasts / balanced blends** → 18g (standard, forgiving)
- **Dark roasts / espresso blends** → 18g (less coffee = less over-extraction risk)
- **Milk drinks (latte/cap)** → 20g (needs punch to cut through milk)

## Pre-infusion Strategies

### Bloom Pre-infusion (light/medium roasts)
1. Fill phase: flow 5ml/s, 3-4s (wet the puck)
2. Soak/bloom: pump off (valve open), 5-8s (let CO2 degas)
3. Gentle ramp to brew pressure

### Pressure Pre-infusion (medium/dark roasts)
1. Fill at 2-3 bar, 3-5s
2. Brief pause or immediate ramp to 9 bar

### Long Pre-infusion (very light roasts)
1. Low flow 2ml/s, 5-8s
2. Extended soak 8-15s
3. Slow ramp to 6-7 bar (lower peak pressure)

## Pressure Profile Strategies

### Flat 9 Bar (classic, all roasts)
- Ramp to 9 bar → hold → cut at target weight
- Simple, predictable, good starting point

### Declining Pressure (medium-dark, dark)
- Ramp to 9 bar → hold briefly → decline to 5-6 bar
- Reduces channeling late in shot, smoother cup

### Blooming Espresso (light, medium-light)
- Pre-infuse → bloom (no pressure) → ramp to 6-7 bar
- Extended contact time, higher extraction without harshness

### Lever-style (all roasts, especially medium)
- Quick ramp to 8-9 bar → gradual natural decline
- Mimics spring lever machines (Cremina profile)
- Produces thick, syrupy body

### Turbo Shot (light roasts, experimental)
- Very high flow (4-5ml/s), lower pressure (4-6 bar)
- Grind coarser, 15-20s total shot time
- High extraction, tea-like clarity

## Processing Method Considerations

| Processing | Flavor Profile | Profile Approach |
|-----------|---------------|-----------------|
| Washed | Clean, bright, acidic | Higher temp, bloom PI, moderate pressure |
| Natural | Fruity, sweet, heavy body | Lower temp, shorter PI, flat or declining |
| Honey | Sweet, medium body | Medium temp, standard PI, declining |
| Anaerobic | Intense, funky, fruit-forward | Lower temp, gentle flow PI, avoid over-extraction |

## Origin Tendencies

| Region | Typical Character | Profile Lean |
|--------|------------------|-------------|
| Ethiopia | Floral, fruity, bright | Bloom PI, higher temp, lower pressure |
| Colombia | Balanced, caramel, nutty | Standard, medium temp |
| Brazil | Chocolatey, nutty, low acid | Flat 9 bar, lower temp |
| Kenya | Bright, berry, wine-like | Bloom PI, higher temp |
| Sumatra | Earthy, heavy, low acid | Short PI, lower temp, declining |
| Guatemala | Chocolate, spice, balanced | Standard to declining |
| Costa Rica | Honey, bright, clean | Bloom PI, medium-high temp |

## GaggiMate Profile Structure (Pro)

Typical phases for a well-structured Pro profile:
1. **Fill** (preinfusion): Flow target 4-5ml/s, 3-4s, valve open
2. **Pre-infuse/Bloom** (preinfusion): Low flow or pump off, 4-10s
3. **Ramp** (brew): Pressure target, 2-4s, transition linear/ease-in
4. **Main Brew** (brew): Pressure/flow hold, 15-30s
5. **Decline** (brew, optional): Lower pressure target, linear transition
6. **Final** (brew): Stop condition on weight (volumetric target)

### Transition Types
- `instant` — jump to new target immediately
- `linear` — straight-line ramp over duration
- `ease-in` — slow start, fast end
- `ease-out` — fast start, slow end  
- `ease-in-out` — smooth S-curve

### Stop Conditions (targets)
- `volumetric` + `gte` + value: Stop when scale reads ≥ Xg (most common final stop)
- `pressure` + `gte`/`lte`: Stop when pressure crosses threshold
- `flow` + `gte`/`lte`: Stop when flow crosses threshold
- `pumped` + `gte`: Stop when X ml pumped in this phase
