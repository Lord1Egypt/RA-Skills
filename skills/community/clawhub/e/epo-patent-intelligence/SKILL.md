---
name: epo-patent-intelligence
description: European Patent Office (EPO) patent intelligence and competitive analysis system. Use when:
  - Client needs to monitor competitor patents in real-time
  - Weekly patent intelligence reports are required for strategic decision-making
  - Identifying technology trends and competitive threats in specific industries
  - DMG Mori or similar manufacturing companies need patent monitoring
  - Generating HTML reports with strategic patent analysis
  - Tracking 50+ patents per week from top 4+ competitors
  - Understanding why specific patents matter to a client's business
  - Any task involving EPO API data collection, patent analysis, or competitive intelligence reporting
---

# EPO Patent Intelligence System

Intelligent patent monitoring and competitive analysis using the European Patent Office (EPO) Open Patent Services (OPS) API.

## Quick Start

1. **Ensure EPO credentials are configured** in `.env` file:
   - `EPO_CONSUMER_KEY` - Your EPO API consumer key
   - `EPO_SECRET_KEY` - Your EPO API secret key

2. **Run patent intelligence collection** for a company:
   ```bash
   cd /path/to/skill
   source .env
   python3 scripts/epo_data_mapper.py "pa=IBM" 1 10
   ```

3. **Generate strategic analysis** using OpenClaw LLM:
   - Load collected patents from database
   - Use LLM to analyze patent relevance and strategic importance
   - Generate HTML report with competitive intelligence

## Architecture

This skill uses a **hybrid approach**:

### Deterministic Layer (Scripts)
- `scripts/epo_data_mapper.py` - EPO API authentication and data fetching
- `scripts/weekly_report.sh` - Automated weekly execution
- `scripts/database_manager.py` - Database operations

### LLM-Powered Layer (OpenClaw Agents)
- **Patent analysis** - Use LLM to understand why patents matter to the client
- **Strategic categorization** - Identify technology categories and competitive threats
- **Report generation** - Create professional HTML with business insights
- **Pattern identification** - Detect trends across patent collections

## Workflow

### Phase 1: Data Collection (Deterministic)

**Step 1: Configure EPO API credentials**
```bash
# Ensure .env file exists with EPO credentials
cat .env
EPO_CONSUMER_KEY=your_key_here
EPO_SECRET_KEY=your_secret_here
```

**Step 2: Fetch patents from EPO API**
```bash
source .env
python3 scripts/epo_data_mapper.py "pa=IBM" 1 5
```

This script:
1. Authenticates with EPO using OAuth2
2. Queries EPO OPS API for patents
3. Parses XML response into structured data
4. Saves to SQLite database

### Phase 2: Analysis (LLM-Powered)

**Step 3: Analyze collected patents with LLM**

Load patents from database and use OpenClaw's reasoning capabilities to:
1. **Identify technology categories** - Match patents to business-relevant categories
2. **Assess competitive threat** - Determine if competitor is encroaching on client's territory
3. **Evaluate strategic importance** - High, Medium, Low, Critical
4. **Generate recommendations** - Immediate action, weekly review, monthly review, monitor

**Example analysis prompt:**
```
Analyze these patents collected from EPO API for DMG Mori:
- Patent: "Spindle Lubricator System" by Mazak
- Abstract: [patent abstract text]
- Technology: CNC Machining

Questions:
1. Why does this patent matter to DMG Mori specifically?
2. What is the competitive threat level? (None/Low/Medium/High/Critical)
3. What strategic action should DMG Mori take?
4. Which DMG business area is affected? (CNC/Additive/Automation/Digital)
```

### Phase 3: Report Generation (LLM-Powered)

**Step 4: Generate professional HTML report**

Use LLM to create structured HTML with modern enterprise dashboard design:
- Executive summary with KPI cards and key metrics
- Interactive Chart.js visualizations
- Individual patent cards with threat scoring and strategic analysis
- Activity timeline with competitor events
- Export to PDF functionality
- Mobile-responsive design

**Modern Framework Stack (CDN-based, no build step):**
- Tailwind CSS - Professional utility-first styling
- Chart.js - Interactive data visualizations
- Font Awesome - Enterprise iconography
- Inter font (Google Fonts) - Modern typography

**Report structure:**
```html
<!-- Modern enterprise dashboard template -->
<nav class="gradient-bg text-white sticky top-0">
  <h1>Patent Intelligence - Week 14, 2026</h1>
  <span class="bg-white/20 px-4 py-2 rounded-full">
    <i class="fas fa-sync-alt mr-2"></i>Live Updates
  </span>
</nav>

<!-- Executive Summary Cards -->
<div class="grid grid-cols-1 md:grid-cols-4 gap-6">
  <div class="bg-gradient-to-br from-blue-500 to-blue-600 rounded-xl p-6 text-white">
    <p class="text-blue-100">Total Patents</p>
    <p class="text-3xl font-bold">47</p>
  </div>
  <!-- More KPI cards... -->
</div>

<!-- Charts Section -->
<div class="grid grid-cols-1 lg:grid-cols-2 gap-8">
  <canvas id="competitorChart"></canvas>
  <canvas id="techChart"></canvas>
</div>

<!-- Patent Cards with Priority Styling -->
<div class="card-hover priority-high threat-critical rounded-xl p-6">
  <span class="bg-red-500 text-white px-3 py-1 rounded-full">CRITICAL</span>
  <span class="bg-gray-800 text-white px-3 py-1 rounded-full">CNC Machining</span>
  <h4>Intelligent Spindle Control System</h4>
  <p><strong>⚠️ Competitive Threat:</strong> [Analysis text]</p>
  <div class="text-3xl font-bold text-red-600">85</div>
</div>
```

**Weekly Report Deployment:**
- Week 14: `https://hermes.sqncr.ai/Patent_report_kw14`
- Week 15: `https://hermes.sqncr.ai/Patent_report_kw15`
- Each week gets a new subdomain with fresh reports

## Key Scripts

### scripts/epo_data_mapper.py
**Purpose:** EPO API authentication and data fetching
**Deterministic** - Same input always produces same output
**Parameters:**
- Query (e.g., "pa=IBM", "ti=CNC")
- Range start (1-100)
- Range end (1-100)

**Usage:**
```bash
python3 scripts/epo_data_mapper.py "pa=Trumpf" 1 5
```

**Output:** Saves patents to SQLite database

### scripts/weekly_report.sh
**Purpose:** Automated weekly patent intelligence generation
**Deterministic** - Runs on schedule (Monday 9:00 AM via cron)
**Workflow:**
1. Source .env credentials
2. Fetch patents for all monitored competitors
3. Trigger LLM analysis
4. Generate HTML report
5. Send email notification

**Usage:**
```bash
# Manual run
./scripts/weekly_report.sh

# Cron setup (every Monday 9:00 AM)
crontab -e
0 9 * * 1 /path/to/skill/scripts/weekly_report.sh
```

### scripts/database_manager.py
**Purpose:** Database operations for patent storage
**Deterministic** - Reliable data persistence
**Functions:**
- `save_patent()` - Store patent with deduplication
- `get_patents_by_company()` - Retrieve patents by competitor
- `get_patents_by_date()` - Time-based queries
- `get_recent_patents()` - Last N days

**Usage:**
```python
from scripts.database_manager import DatabaseManager
db = DatabaseManager()
patents = db.get_recent_patents(days=7)
```

## LLM Analysis Guidelines

### When to Use LLM vs Scripts

**Use Scripts (Deterministic):**
- EPO API authentication
- Data fetching from EPO
- Database storage/retrieval
- Scheduled execution
- File operations

**Use LLM (Intelligent):**
- Patent relevance assessment
- Strategic importance scoring
- Competitive threat analysis
- Natural language report generation
- Pattern/trend identification
- Business impact evaluation

### Analysis Template

For each patent, analyze:

1. **Competitive Threat**
   - None: Unrelated to client's business
   - Low: Adjacent technology, low impact
   - Medium: Overlapping technology, potential threat
   - High: Direct competitor, core technology
   - Critical: Threatens key business area

2. **Technology Alignment**
   - CNC_Machining: Turning, milling, machining centers
   - Additive_Manufacturing: 3D printing, laser metal deposition
   - Automation: Robotic loading, Industry 4.0
   - Digital_Manufacturing: IoT, predictive maintenance
   - Other: Specify based on patent content

3. **Strategic Action**
   - **Immediate_review:** Patent requires urgent R&D attention
   - **Weekly_review:** Include in weekly technology meeting
   - **Monthly_review:** Standard monitoring, monthly assessment
   - **Monitor:** Track but no immediate action needed

4. **Business Impact**
   - Describe in 2-3 sentences why this patent matters
   - Connect to client's business strategy
   - Highlight risks and opportunities

### Example Analysis Output

```
Patent: "Spindle Lubricator System"
Company: YAMAZAKI MAZAK CORP

⚠️ COMPETITIVE THREAT: Mazak is patenting spindle lubrication technology that 
directly competes with DMG Mori's CNC machining center offerings. This indicates 
Mazak is investing in core CNC technology improvements that could erode DMG's 
competitive advantage in high-precision machining.

📊 TECHNOLOGY ALIGNMENT: CNC_Machining - This is DMG Mori's core business. The 
patent covers spindle lubrication systems which are critical for maintaining 
precision in high-speed machining operations.

⚡ ACTION: Weekly R&D review recommended. DMG Mori should evaluate if this 
technology represents a threat requiring defensive patenting, or if it's 
an opportunity for licensing or collaboration.

🎯 IMPACT: HIGH - Core technology area, direct competitor, potential to 
affect DMG's market position in CNC machining centers.
```

## Database Schema

**Table: patents**
- `id` (INTEGER PRIMARY KEY)
- `patent_id` (TEXT) - EPO patent ID
- `title` (TEXT) - Patent title
- `inventor` (TEXT) - Inventor names
- `company` (TEXT) - Patent assignee
- `filing_date` (DATE) - Filing date
- `publication_date` (DATE) - Publication date
- `abstract` (TEXT) - Patent abstract
- `category` (TEXT) - Technology category (assigned by LLM)
- `technology_area` (TEXT) - Specific technology area
- `secondary_effects` (TEXT) - Side effects/benefits
- `image_url` (TEXT) - Link to patent document images
- `created_at` (TIMESTAMP) - When stored

## Competitive Monitoring Setup

### Step 1: Define Competitors
For a manufacturing client like DMG Mori:
- Trumpf (laser, additive manufacturing)
- Mazak (CNC machining)
- Okuma (machine tools)
- Haas (CNC systems)

### Step 2: Define Technology Categories
Match to client's business:
- CNC_Machining
- Additive_Manufacturing
- Automation
- Digital_Manufacturing
- Laser_Technology
- Tooling_Systems

### Step 3: Configure Weekly Monitoring
Edit `scripts/weekly_report.sh`:
```bash
COMPETITORS="Trumpf Mazak Okuma Haas"
TECH_CATEGORIES="CNC Additive Automation Digital"
```

### Step 4: Set Up Cron
```bash
crontab -e
# Add: 0 9 * * 1 /path/to/skill/scripts/weekly_report.sh
```

## Security & Credentials

**EPO API Credentials:**
- Store in `.env` file (not in version control)
- Format: `EPO_CONSUMER_KEY=xxx`, `EPO_SECRET_KEY=xxx`
- Script loads via `source .env` before execution
- Never commit credentials to git

**Data Security:**
- Database stored locally: `data/patents.db`
- Reports generated locally: `reports/*.html`
- No data sent to external services (except EPO API)
- Logs kept locally: `logs/*.log`

## Troubleshooting

### EPO API Authentication Failed
**Check:** `.env` file exists and contains valid credentials
**Action:** Verify keys at https://developers.epo.org/

### No Patents Fetched
**Check:** Query syntax (e.g., `pa=IBM` works, `pn=EP*` may not)
**Action:** Test with simple query first: `pa=IBM`

### Report Not Generated
**Check:** Database has patents, LLM analysis completed
**Action:** Run weekly_report.sh with debug logging

### Cron Job Not Running
**Check:** Script permissions, cron syntax, paths
**Action:** Test script manually before adding to cron

## References

For detailed information, see:
- `references/EPO_API.md` - EPO OPS API documentation
- `references/ANALYSIS_PATTERNS.md` - LLM analysis templates
- `references/REPORT_TEMPLATES.md` - HTML report structure examples
- `references/COMPETITOR_SETUP.md` - Setting up competitor monitoring