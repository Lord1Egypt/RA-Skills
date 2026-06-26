---
name: ezviz-open-safety-production-inspection
description: Ezviz safety production inspection skill. Captures device images and sends to Ezviz AI for workplace safety analysis.
metadata:
  openclaw:
    emoji: "⚠️"
    requires:
      env: ["EZVIZ_APP_KEY", "EZVIZ_APP_SECRET", "EZVIZ_DEVICE_SERIAL"]
      pip: ["requests"]
    primaryEnv: "EZVIZ_APP_KEY"
    warnings:
      - "Use dedicated Ezviz credentials (not main account)"
      - "Queries intelligent agent list"
      - "May create agent from template"
      - "Captures device images"
      - "Sends images to aidialoggw.ys7.com"
      - "Token cached in /tmp/ezviz_global_token_cache/ (600)"
    sideEffects:
      - "Query agent list"
      - "Create agent (template: 安全生产行业通用智能体)"
      - "Capture images"
      - "AI analysis (aidialoggw.ys7.com)"
    security:
      utf8Validated: true
      apiDomains: ["open.ys7.com", "aidialoggw.ys7.com"]
      tokenCachePerms: "0600"
---

# Ezviz Safety Production Inspection Skill

Captures images from Ezviz cameras and sends to Ezviz AI for workplace safety production inspection.

**Template**: 安全生产行业通用智能体 (`e15f061c13f349b1b2a3`)

**Detection Items**:
- Safety helmet detection (安全帽佩戴)
- Fall detection (人员跌倒)
- Cleanliness analysis (整洁度)
- Fire/smoke detection (烟火检测)

> **⚠️ Important**: This skill uses the **安全生产行业通用智能体** template.
> 
> - Template ID: `e15f061c13f349b1b2a3`
> - The skill will prioritize existing agents with '安全生产' in the name
> - If no matching agent exists, a new one will be created from the safety production template
> - Created agents will automatically have '安全生产' in the name

---

## User Confirmation Required

Running this skill means you accept these remote actions:

1. Query Ezviz agent list (open.ys7.com)
2. Create agent from template if needed (open.ys7.com)
3. Capture device images (open.ys7.com)
4. Send images for AI analysis (aidialoggw.ys7.com)

Data flow: Device -> open.ys7.com -> aidialoggw.ys7.com -> Local output

Privacy:
- Images stored on Ezviz (2 hours)
- Token cached in /tmp/ezviz_global_token_cache/ (perms 600)

---

## Security Requirements

1. Use dedicated Ezviz app credentials (not main account)
2. Minimal permissions: capture + agent APIs only
3. Prefer environment variables over config files
4. Test with non-production devices first
5. **Agent name must contain '安全生产'** (compliance requirement)

---

## Quick Start

### Environment Variables (Recommended)

```bash
export EZVIZ_APP_KEY="your_key"
export EZVIZ_APP_SECRET="your_secret"
export EZVIZ_DEVICE_SERIAL="dev1,dev2"
# Template ID is optional (default: e15f061c13f349b1b2a3)
export EZVIZ_SAFETY_TEMPLATE_ID="e15f061c13f349b1b2a3"
python3 scripts/safety_production_inspection.py
```

### Config File (Alternative)

Add to ~/.openclaw/channels.json:
```json
{
  "channels": {
    "ezviz": {
      "appId": "your_app_id",
      "appSecret": "your_app_secret",
      "devices": ["BF6985110"],
      "safetyTemplateId": "e15f061c13f349b1b2a3"  # 安全生产行业通用智能体模板 ID
    }
  }
}
```

Then run:
```bash
python3 scripts/safety_production_inspection.py
```

### Disable Token Cache (High Security)

```bash
export EZVIZ_TOKEN_CACHE=0
python3 scripts/safety_production_inspection.py
```

---

## Pre-Run Verification

Run these before first use:

```bash
# 1. Check for hidden characters
python3 -c "
import sys
for f in ['SKILL.md', 'scripts/safety_production_inspection.py', 'lib/token_manager.py']:
    with open(f, 'rb') as file:
        text = file.read().decode('utf-8')
        for i, c in enumerate(text):
            code = ord(c)
            if code < 32 and code not in [9, 10, 13]:
                print(f'{f}: Control char at {i}')
                sys.exit(1)
print('All files clean')
"

# 2. Verify API domains (should use open.ys7.com only)
grep -r "open.ys7.com" scripts/ lib/  # Should show endpoints

# 3. Verify domain connectivity
curl -I https://open.ys7.com/api/lapp/token/get  # Should return 200 OK

# 4. Check token cache permissions
ls -la /tmp/ezviz_global_token_cache/global_token_cache.json
# Should show: -rw------- (600)
```

---

## API Endpoints

| Domain | Purpose |
|--------|---------|
| open.ys7.com | Token, Capture, Agent Management |
| aidialoggw.ys7.com | AI Analysis |

Note: open.ys7.com is the official Ezviz Open API domain (openai = Open API, not AI).

---

## Safety Production Inspection Items

The AI agent will analyze images for:

1. **Personal Protective Equipment (PPE)** - Safety helmets, safety vests, goggles
2. **Fire Safety** - Fire extinguishers, emergency exits, no smoking signs
3. **Electrical Safety** - Proper wiring, no exposed wires, grounded equipment
4. **Workplace Organization** - Clear walkways, proper storage, no clutter
5. **Machinery Safety** - Guard rails, warning signs, proper operation
6. **Hazardous Materials** - Proper storage, labeling, containment

---

## Security Checklist

Before running:
- [ ] Reviewed scripts/safety_production_inspection.py
- [ ] Reviewed lib/token_manager.py
- [ ] Verified API domains (open.ys7.com, aidialoggw.ys7.com)
- [ ] Created dedicated Ezviz app (minimal permissions)
- [ ] Tested with non-production device
- [ ] Configured 安全生产 template ID

Before autonomous use:
- [ ] Accept remote side effects (agent creation, image capture, AI analysis)
- [ ] Understand data flow and privacy implications
- [ ] Configured token cache appropriately for your environment

---

## Update Log

| Date | Version | Changes |
|------|---------|---------|
| 2026-03-19 | 2.0.1 | Updated template ID to e15f061c13f349b1b2a3 (安全生产行业通用智能体) |
| 2026-03-19 | 2.0.0 | Renamed from restaurant-inspection to safety-production-inspection |
| 2026-03-19 | 1.0.9 | Agent name must contain '安全生产' (compliance requirement) |
| 2026-03-19 | 1.0.8 | Security hardened: unified domains, user confirmation, clean UTF-8 |
| 2026-03-19 | 1.0.7 | Global token cache support |
| 2026-03-19 | 1.0.6 | Config file support |

---

Author: EzvizOpenTeam
License: MIT-0
