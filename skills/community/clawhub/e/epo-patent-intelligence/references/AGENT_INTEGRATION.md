# OpenClaw Agent Integration Guide

## Overview

This document explains how OpenClaw agents should interact with the EPO Patent Intelligence skill.

## Agent Workflow

When an OpenClaw agent detects an analysis request marker file, it should:

### Step 1: Load Analysis Request
```python
import json
import sqlite3

# Read analysis request
with open('/path/to/analysis_request_YYYYMMDD.json', 'r') as f:
    request = json.load(f)

database_path = request['database_path']
client_context = request['client_context']
output_report = request['output_report']
```

### Step 2: Load Patents from Database
```python
def load_patents_from_db(db_path):
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    # Get recent patents (last 30 days)
    cursor.execute('''
    SELECT * FROM patents 
    WHERE publication_date >= date('now', '-30 days')
    ORDER BY publication_date DESC
    ''')
    
    patents = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return patents

patents = load_patents_from_db(database_path)
```

### Step 3: Analyze Each Patent (LLM Intelligence)

For each patent, use the LLM to analyze:

**Analysis Template:**
```
Analyze this patent for {client_context}:

PATENT: {patent_title}
COMPANY: {patent_company}
ABSTRACT: {patent_abstract}

Questions:
1. What is the competitive threat level? (None/Low/Medium/High/Critical)
2. Which technology category does this belong to? (CNC_Machining/Additive_Manufacturing/Automation/Digital_Manufacturing/Laser_Technology/Tooling_Systems)
3. What strategic action should {client_context} take? (Immediate_review/Weekly_review/Monthly_review/Monitor)
4. Why does this patent specifically matter to {client_context}'s business?
```

**Example LLM Prompt:**
```
You are a patent intelligence analyst for DMG Mori, a leading manufacturer of CNC machine tools.

Analyze this patent for competitive threat:

PATENT: "Spindle Lubricator System for High-Speed CNC Machines"
COMPANY: "YAMAZAKI MAZAK CORP"
ABSTRACT: "A spindle lubrication system for CNC machining centers that reduces heat generation and extends tool life..."

Questions:
1. Competitive threat level? (Mazak is DMG's primary competitor, this is core CNC technology)
2. Technology category? (CNC_Machining - spindle technology)
3. Strategic action? (Weekly_review - monitor Mazak's spindle technology developments)
4. Business impact? (This could affect DMG's competitive positioning in high-speed machining)
```

### Step 4: Generate HTML Report

Use the LLM to generate an HTML report with:

**Report Structure:**
```html
<!DOCTYPE html>
<html>
<head>
    <title>Weekly Patent Intelligence Report - {client_context}</title>
    <style>
        /* CSS for professional report */
    </style>
</head>
<body>
    <h1>Weekly Patent Intelligence Report</h1>
    <p>Client: {client_context}</p>
    <p>Date: {report_date}</p>
    <p>Total Patents Analyzed: {patent_count}</p>
    
    <h2>Executive Summary</h2>
    <p>[LLM-generated summary of key findings]</p>
    
    <h2>Competitor Activity</h2>
    <table>
        <tr><th>Competitor</th><th>Patents</th><th>Threat Level</th></tr>
        <!-- LLM-generated table rows -->
    </table>
    
    <h2>Detailed Patent Analysis</h2>
    <div class="patent-card">
        <h3>{patent_title}</h3>
        <p><strong>Company:</strong> {company}</p>
        <p><strong>Threat:</strong> {threat_level}</p>
        <p><strong>Action:</strong> {strategic_action}</p>
        <div class="analysis">
            {llm_analysis_text}
        </div>
    </div>
</body>
</html>
```

### Step 5: Save Report and Clean Up

```python
# Save HTML report
with open(output_report, 'w') as f:
    f.write(html_report)

# Mark analysis as complete
os.remove(analysis_request_path)
```

## Agent Configuration

### Required Tools
- `read` - Read analysis request and database
- `write` - Generate HTML report
- `exec` - Run database queries if needed
- LLM capabilities for analysis

### Skill Integration
The agent should:
1. Monitor the `logs/` directory for new analysis requests
2. Load the skill's `references/ANALYSIS_PATTERNS.md` for analysis templates
3. Use the skill's database schema
4. Follow the client context from the request

### Example Agent Prompt
```
You are an OpenClaw agent for the EPO Patent Intelligence skill.

TASK: Analyze patents for competitive intelligence.

INSTRUCTIONS:
1. Check for analysis request files in /path/to/skills/epo-patent-intelligence/logs/
2. If found, load the request JSON
3. Connect to the SQLite database at the specified path
4. Load recent patents (last 30 days)
5. For each patent, analyze using the template in references/ANALYSIS_PATTERNS.md
6. Generate an HTML report with executive summary and detailed analysis
7. Save report to the specified output path
8. Delete the analysis request file when complete

Use the LLM to provide strategic insights, not just data summarization.
```

## Testing the Integration

### Manual Test
```bash
# 1. Create test analysis request
cd /path/to/skill
python3 -c "
import json
request = {
    'request_type': 'test_analysis',
    'timestamp': '2026-04-04T10:00:00Z',
    'database_path': 'data/patents.db',
    'client_context': 'Test_Client',
    'output_report': 'reports/test_report.html'
}
with open('logs/test_request.json', 'w') as f:
    json.dump(request, f, indent=2)
"

# 2. Trigger OpenClaw agent manually
# (This depends on your OpenClaw setup)
```

### Automated Test
The `scripts/weekly_automation.sh` script automatically creates analysis requests every Monday at 9:00 AM.

## Error Handling

**No Analysis Request:** Agent should exit gracefully
**Database Not Found:** Log error and exit
**Empty Patent List:** Generate "No new patents" report
**LLM Analysis Failure:** Fall back to basic categorization
**Report Generation Failure:** Save error log and retry

## Performance Considerations

- Process patents in batches (e.g., 10 at a time)
- Cache competitor names for faster lookups
- Use streaming for large HTML reports
- Clean up temporary files after completion