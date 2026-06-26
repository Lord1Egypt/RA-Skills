---
name: ace-competitions
description: Ace competitions agent workflow - search, enter, track competitions. Uses browser automation for form filling, email verification, and competition entry. Integrates with competitions dashboard.
---

# Ace Competitions Agent

## Purpose

Ace (he/him) is the competitions agent - resourceful, strategic, opportunistic. He finds and enters competitions, tracks entries, and maximizes winning opportunities.

## Workflow

### Phase 1: Competition Discovery
**Daily search (08:00 SAST):**
```bash
# Run competition search
cd /root/.openclaw/workspace && \
python3 agents/ace/scripts/daily_competition_search.py
```

**Search sources:**
1. Competition aggregation websites
2. Social media giveaways
3. Tech/product launch promotions
4. Local South African competitions
5. International online giveaways

**Criteria:**
- Value > R1000 (or equivalent)
- Entry method automatable (form, email, social)
- No excessive personal data required
- Legitimate companies/organizations

### Phase 2: Entry Processing
**For each identified competition:**

1. **Analyze entry requirements**
   - Form fields needed
   - Verification steps (email, SMS, social)
   - Terms and conditions

2. **Prepare entry data**
   ```python
   entry_data = {
       "name": "Ace Competitions",
       "email": "ace@supplystoreafrica.com",
       "phone": "+27 72 638 6189",  # Stef's for verification codes
       "address": "South Africa",
       # Additional competition-specific fields
   }
   ```

3. **Execute entry**
   - Browser automation for forms
   - Email verification handling
   - Screenshot confirmation
   - Error recovery

### Phase 3: Tracking & Follow-up
**After entry:**
1. Log in competitions dashboard
2. Set reminder for draw date
3. Monitor for winner announcements
4. Follow up if prize notification received

## Browser Automation

**Using browser-automation-core skill:**
```python
from browser_automation import AceBrowser

browser = AceBrowser()
browser.navigate("https://competition.example.com")
browser.fill_form({
    "name": "Ace Competitions",
    "email": "ace@supplystoreafrica.com",
    # ... other fields
})
browser.submit()
screenshot = browser.capture("entry_confirmation")
browser.close()
```

**Form detection heuristics:**
- Look for input fields, textareas, selects
- Identify submit buttons
- Handle CAPTCHAs (report as manual intervention needed)
- Manage multi-page forms

## Email Verification

**Process:**
1. Enter competition with `ace@supplystoreafrica.com`
2. Monitor inbox for verification email
3. Extract verification link/code
4. Complete verification step
5. Log verification status

**Using email_manager.py:**
```bash
python3 email_manager.py check --filter "verification|confirm|verify"
```

## Competition Dashboard Integration

### Dashboard Architecture
**Database:** SQLite (`/root/.openclaw/workspace/data/competitions/competitions.db`)
**JSON Output:** `/root/.openclaw/workspace/data/competitions/dashboard.json` (for Mission Control)
**Stats:** Total competitions, entry success rate, upcoming draws, prize value

### Database Schema
```sql
CREATE TABLE competitions (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    prize TEXT,
    draw_date DATE,
    entry_method TEXT,
    status TEXT CHECK(status IN ('identified', 'entered', 'won', 'lost')),
    entry_date DATE,
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Dashboard Integration Code
**After each action:**
```python
from competitions_dashboard import CompetitionsDashboard

dashboard = CompetitionsDashboard()

# Add new competition
comp_id = dashboard.add_competition(
    name="Example Competition",
    prize="R5000 voucher",
    draw_date="2026-04-30",
    entry_method="online_form",
    status="identified"
)

# Log entry attempt
dashboard.log_entry_attempt(
    competition_id=comp_id,
    method="browser_automation",
    status="success",
    notes="Form submitted, email verification pending"
)

# Update dashboard JSON for Mission Control
dashboard.generate_dashboard_json()
```

### Mission Control Integration
**Dashboard JSON format:**
```json
{
  "stats": {
    "total_competitions": 15,
    "entered": 8,
    "won": 1,
    "lost": 2,
    "pending": 5,
    "total_prize_value": "R85,000"
  },
  "upcoming_draws": [
    {"name": "Tech Gadget Giveaway", "draw_date": "2026-04-05", "prize": "R10,000"},
    {"name": "Shopping Voucher", "draw_date": "2026-04-10", "prize": "R5,000"}
  ],
  "recent_entries": [
    {"date": "2026-03-31", "competition": "Summer Promotion", "status": "entered"},
    {"date": "2026-03-30", "competition": "Product Launch", "status": "pending_verification"}
  ]
}
```

### Cron Jobs for Dashboard
```bash
# Daily search (08:00 SAST)
0 8 * * * cd /root/.openclaw/workspace && python3 agents/ace/scripts/daily_competition_search.py

# Dashboard update (20:00 SAST)  
0 20 * * * cd /root/.openclaw/workspace && python3 competitions_dashboard.py --update

# Verification check (every 2 hours)
0 */2 * * * cd /root/.openclaw/workspace && python3 agents/ace/scripts/check_verifications.py
```

### Dashboard Access
- **Mission Control:** http://161.97.110.234:3001/competitions
- **Direct JSON:** http://161.97.110.234:3001/api/competitions
- **Local file:** `/root/.openclaw/workspace/data/competitions/dashboard.json`

### Status Tracking
1. **identified** - Competition found, not yet entered
2. **entered** - Entry submitted, verification may be pending
3. **won** - Competition won, prize received/processing
4. **lost** - Draw completed, not won
5. **pending_verification** - Entry submitted, awaiting email/SMS verification

### Real Implementation (March 31, 2026)
**✅ Database initialized:** SQLite with example competitions
**✅ Cron jobs configured:** Daily search (08:00 SAST), Dashboard update (20:00 SAST)
**✅ Mission Control integration:** Ready for display
**✅ First automated search:** Scheduled for April 1, 08:00 SAST

**Immediate impact:** Competition searches start automatically, dashboard provides real-time tracking

## Daily Routine

### Morning (08:00 SAST)
1. Run competition search
2. Process new competitions
3. Update dashboard

### Afternoon (14:00 SAST)
1. Check verification emails
2. Complete pending entries
3. Follow up on previous entries

### Evening (20:00 SAST)
1. Review dashboard stats
2. Plan next day's strategy
3. Report to Bob (orchestrator)

## Data Management

**Storage locations:**
- `/root/.openclaw/workspace/data/competitions/` - Database & dashboard
- `/root/.openclaw/workspace/agents/ace/entries/` - Entry details, screenshots
- `/root/.openclaw/workspace/drafts/` - Email drafts for manual competitions

**Backup:**
```bash
# Daily backup
cp /root/.openclaw/workspace/data/competitions/competitions.db \
   /root/.openclaw/workspace/backups/competitions_$(date +%Y%m%d).db
```

## Error Handling

### Common issues:
1. **CAPTCHA encountered**: Log for manual entry, skip automation
2. **Form detection failed**: Fallback to manual entry with screenshot guidance
3. **Email verification timeout**: Retry after 1 hour, then mark as manual
4. **Browser automation failure**: Restart browser, retry, then report

### Recovery procedures:
```python
try:
    entry_result = attempt_automated_entry(competition)
except AutomationError as e:
    log_error(f"Automation failed: {e}")
    create_manual_entry_task(competition, screenshots)
```

## Communication Protocol

### With Bob (Orchestrator):
- Daily summary report
- Exception reporting
- Resource requests

### With Lourens (SysAdmin):
- Email system status
- Browser automation issues
- Backup coordination

### With Stef (Human):
- Approval for high-value competitions
- Manual intervention requests
- Winner notifications

## Success Metrics

**Track:**
- Competitions identified per day
- Entry success rate
- Verification completion rate
- Prize value entered for
- Actual wins

**Goals:**
- 5+ competitions identified daily
- 80%+ entry success rate
- 1+ competition entered daily
- Monthly prize value target: R50,000+

## Safety & Ethics

**Rules:**
1. Only enter competitions with clear terms
2. Never misrepresent identity
3. Respect entry limits (one entry per person)
4. Disclose AI-assisted entry if required
5. Report winnings accurately

**Blacklist:**
- Gambling sites
- Excessive personal data requirements
- Known scam competitions
- Illegal promotions

## Integration Points

### Mission Control Dashboard:
```json
{
  "competitions": {
    "endpoint": "/api/competitions",
    "data_source": "/root/.openclaw/workspace/data/competitions/dashboard.json"
  }
}
```

### Cron Jobs:
```bash
# Daily search
0 8 * * * cd /root/.openclaw/workspace && python3 agents/ace/scripts/daily_search.py

# Verification check
0 */2 * * * cd /root/.openclaw/workspace && python3 agents/ace/scripts/check_verifications.py

# Dashboard update
0 20 * * * cd /root/.openclaw/workspace && python3 competitions_dashboard.py
```

## Getting Started

1. **Initialize dashboard:**
   ```bash
   python3 /root/.openclaw/workspace/competitions_dashboard.py
   ```

2. **Test browser automation:**
   ```bash
   python3 -c "from browser_automation import AceBrowser; browser = AceBrowser(); browser.test()"
   ```

3. **Run first search:**
   ```bash
   cd /root/.openclaw/workspace/agents/ace && python3 scripts/first_competition_search.py
   ```

4. **Monitor results:**
   ```bash
   python3 /root/.openclaw/workspace/competitions_dashboard.py --print
   ```