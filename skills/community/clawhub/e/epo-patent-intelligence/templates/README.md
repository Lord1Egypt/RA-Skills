# Report Templates

Jinja2 templates for generating professional patent intelligence reports.

## Templates Directory Structure

```
templates/
├── base_report.html      # Main report template (use this)
└── README.md            # This file
```

## Using the Templates

### From Python

```python
from scripts.report_generator import PatentReportGenerator

# Create generator
generator = PatentReportGenerator()

# Generate report
result = generator.create_report(
    db_path='data/patents.db',
    client_name='DMG Mori',
    output_html='reports/weekly_report.html',
    output_pdf='reports/weekly_report.pdf'
)
```

### CLI Usage

```bash
# Generate HTML only
python3 scripts/report_generator.py --db data/patents.db --client "DMG Mori" --html reports/output.html --no-pdf

# Generate both HTML and PDF
python3 scripts/report_generator.py --db data/patents.db --client "DMG Mori" --html reports/output.html --pdf reports/output.pdf

# Look back 30 days
python3 scripts/report_generator.py --days 30
```

## Template Features

### 1. Tailwind CSS Styling
- Professional enterprise design
- Responsive layout
- Threat-level color coding
- Print-friendly styles

### 2. Interactive Charts (Chart.js)
- Threat distribution doughnut chart
- Competitor activity bar chart
- Technology focus breakdown

### 3. Alpine.js Interactivity
- Filter by threat level
- Search patents by title/company
- Smooth transitions

### 4. Print/PDF Support
- Optimized for print output
- Page headers and footers
- Page break control

## Customization

### Colors
Edit threat colors in `base_report.html`:
```css
<script>
  tailwind.config = {
    theme: {
      extend: {
        colors: {
          threat: {
            critical: '#dc2626',
            high: '#ea580c',
            medium: '#ca8a04',
            low: '#16a34a'
          }
        }
      }
    }
  }
</script>
```

### Sections
The template includes:
1. Executive Summary (stats, alerts)
2. Analytics Dashboard (charts)
3. Detailed Patent Analysis (cards)

### Adding New Fields
Patent data can include:
- `title`: Patent title
- `company`: Assignee organization
- `patent_id`: Patent number
- `publication_date`: Publication date
- `filing_date`: Filing date
- `abstract`: Patent abstract
- `technology_category`: Main tech category
- `technology_area`: Specific area
- `threat_level`: Critical/High/Medium/Low
- `strategic_analysis`: LLM-generated analysis
- `action_recommended`: Suggested action
- `affected_business_area`: Business unit
- `inventor`: Inventor names
- `epo_link`: Link to EPO database

## Report Output

### HTML Report Features
- ✅ Interactive filtering
- ✅ Charts and visualizations
- ✅ Search functionality
- ✅ Print-optimized CSS
- ✅ Professional styling
- ✅ Mobile responsive

### PDF Report Features
- ✅ Professional headers/footers
- ✅ Page numbers
- ✅ Consistent formatting
- ✅ Confidential marking
- ✅ Email-ready output

## Dependencies

Install required packages:
```bash
pip install jinja2 playwright
playwright install chromium
```

Or use requirements.txt:
```bash
pip install -r requirements.txt
```

## Examples

### Basic Report
```bash
python3 scripts/generate_demo_report.py
```

### Custom Client
```python
generator = PatentReportGenerator()
generator.create_report(
    db_path='data/patents.db',
    client_name='Trumpf GmbH',
    output_html='reports/trumpf_analysis.html',
    days=14
)
```

### Batch Reports
```python
clients = ['DMG Mori', 'Trumpf', 'Mazak']
for client in clients:
    generator.create_report(
        db_path='data/patents.db',
        client_name=client,
        output_html=f'reports/{client.lower().replace(" ", "_")}_report.html'
    )
```
