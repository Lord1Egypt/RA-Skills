---
name: find-phone
description: Make the phone ring, vibrate, and flash to help locate it
metadata: { "openclaw": { "emoji": "📱" } }
---

# Find My Phone

When the user can't find their phone, trigger sound, vibration, and flashlight simultaneously to help locate it.

## Steps

### 1. Save Current State

Query current volume levels so they can be restored later:

```
nodes({ action: "invoke", invokeCommand: "hardware.volume" })
```

Remember the returned values for each stream.

### 2. Activate All Signals

Execute these in quick succession:

**Wake screen**:
```
nodes({ action: "invoke", invokeCommand: "hardware.screenOn" })
```

**Max volume**:
```
nodes({ action: "invoke", invokeCommand: "hardware.volume", invokeParamsJson: '{"stream": "ring", "level": 100}' })
nodes({ action: "invoke", invokeCommand: "hardware.volume", invokeParamsJson: '{"stream": "media", "level": 100}' })
```

**Flashlight on**:
```
nodes({ action: "invoke", invokeCommand: "hardware.flashlight", invokeParamsJson: '{"on": true}' })
```

**Sustained vibration**:
```
nodes({ action: "invoke", invokeCommand: "hardware.vibrate", invokeParamsJson: '{"pattern": [0, 1000, 500, 1000, 500, 1000, 500, 1000]}' })
```

### 3. Report Location

Call `clawpaw_get_context` to get the last known location, and tell the user:
- Where the phone was last detected (e.g. "Home", "Office", or a street address)
- When the location was last updated

### 4. Restore Settings

After the user confirms they found the phone, restore previous settings:

**Flashlight off**:
```
nodes({ action: "invoke", invokeCommand: "hardware.flashlight", invokeParamsJson: '{"on": false}' })
```

**Restore volume** (use values from step 1):
```
nodes({ action: "invoke", invokeCommand: "hardware.volume", invokeParamsJson: '{"stream": "ring", "level": ORIGINAL}' })
nodes({ action: "invoke", invokeCommand: "hardware.volume", invokeParamsJson: '{"stream": "media", "level": ORIGINAL}' })
```

## Output Format

```
📱 Helping you find your phone!

Activated: vibration + max volume + flashlight

📍 Last known location: [place] ([X] minutes ago)

Let me know when you've found it and I'll restore the volume settings.
```

## When to Use

- User says "find my phone", "where's my phone", "I lost my phone"
- User says "make my phone ring", "ring my phone"

## When NOT to Use

- User is asking about phone specs or models
- User is discussing buying a phone
- User says "found it" (restore settings instead)
