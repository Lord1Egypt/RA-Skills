# delivery-queue — Delayed Segmented Delivery

Schedule and deliver messages in timed segments to simulate human-like sending patterns.

## Use Cases
- Break long product introductions into 3-5 digestible messages
- Schedule follow-ups at optimal times (e.g., prospect's local 9 AM)
- Drip campaigns: space out nurture messages over days
- Avoid WhatsApp spam detection by pacing outbound messages

## Commands
- `deliver:schedule` — Queue a message for future delivery
- `deliver:list` — View pending deliveries
- `deliver:cancel` — Cancel a scheduled delivery
- `deliver:flush` — Send all pending messages immediately

## Configuration
```yaml
default_delay_ms: 3000        # Delay between segments
max_segments: 10              # Max segments per delivery
timezone: "{{timezone}}"      # Owner's timezone
quiet_hours:                  # Don't send during these hours
  start: "22:00"
  end: "07:00"
```

## Usage Example
```
Schedule a 3-part product intro to +1234567890:
1. Company overview (send now)
2. Product highlights (send after 5 min)
3. Pricing inquiry (send after 15 min)
```

## How It Works
1. AI composes the full message sequence
2. Skill splits into segments with timing
3. Each segment is queued with a delivery timestamp
4. Background worker sends at scheduled times
5. Failed deliveries retry up to 3 times

## File Structure
```
delivery-queue/
├── SKILL.md          # This file
└── deliver.sh        # Queue management script
```
