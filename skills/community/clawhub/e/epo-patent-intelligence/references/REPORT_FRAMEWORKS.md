# Modern Dashboard & Report Framework Guidelines

## Overview

This document provides comprehensive guidelines for creating enterprise-grade, beautiful patent intelligence reports.

## Recommended Tech Stack

### 1. CSS Framework: Tailwind CSS
**Why:** Utility-first, highly customizable, professional appearance
**Usage:** Via CDN for zero-setup
```html
<script src="https://cdn.tailwindcss.com"></script>
```

### 2. Icons: Font Awesome 6
**Why:** Professional iconography, extensive library
**Usage:** Via CDN
```html
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
```

### 3. Fonts: Inter (Google Fonts)
**Why:** Modern, highly readable, enterprise standard
**Usage:** Via CDN
```html
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
```

### 4. Charts: Chart.js
**Why:** Interactive, responsive, beautiful visualizations
**Usage:** Via CDN
```html
<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
```

## Design Principles

### 1. Color Scheme
- **Primary:** Indigo/Purple gradients (`#667eea` to `#764ba2`)
- **Success:** Green (`#10b981`)
- **Warning:** Amber (`#f59e0b`)
- **Danger:** Red (`#ef4444`)
- **Neutral:** Gray scale for text and backgrounds

### 2. Layout Structure
```html
<!-- Navigation Bar -->
<nav class="gradient-bg text-white sticky top-0 z-50">
    <!-- Brand, Date, Status -->
</nav>

<!-- Executive Summary Cards -->
<div class="grid grid-cols-1 md:grid-cols-4 gap-6">
    <!-- KPI Cards with gradients -->
</div>

<!-- Charts Section -->
<div class="grid grid-cols-1 lg:grid-cols-2 gap-8">
    <!-- Interactive charts -->
</div>

<!-- Patent Cards -->
<div class="space-y-4">
    <!-- Individual patent analysis cards -->
</div>

<!-- Timeline -->
<div class="relative">
    <!-- Activity timeline -->
</div>
```

### 3. Patent Card Structure
```html
<div class="card-hover priority-high threat-critical rounded-xl p-6">
    <!-- Priority Badge -->
    <span class="bg-red-500 text-white px-3 py-1 rounded-full">CRITICAL</span>
    
    <!-- Technology Tag -->
    <span class="bg-gray-800 text-white px-3 py-1 rounded-full">CNC Machining</span>
    
    <!-- Patent Title -->
    <h4 class="text-lg font-semibold">Intelligent Spindle Control System...</h4>
    
    <!-- Company & Date -->
    <p><i class="fas fa-building"></i> <strong>YAMAZAKI MAZAK CORP</strong></p>
    
    <!-- Threat Analysis -->
    <div class="bg-white/50 rounded-lg p-4">
        <p><strong>⚠️ Competitive Threat:</strong> [Analysis text]</p>
    </div>
    
    <!-- Action & Link -->
    <div class="flex items-center space-x-4">
        <span><i class="fas fa-exclamation-circle"></i> Immediate Review</span>
        <a href="[patent-url]" target="_blank">View Patent</a>
    </div>
    
    <!-- Threat Score -->
    <div class="text-3xl font-bold text-red-600">85</div>
</div>
```

### 4. Priority Styling
- **Critical:** Red border + red gradient background
- **High:** Orange border + orange gradient background
- **Medium:** Yellow/amber styling
- **Low:** Green styling

## Implementation Template

**File:** `reports/modern_report_template.html`

This template includes:
- ✅ Responsive navigation bar
- ✅ Executive summary with KPI cards
- ✅ Interactive Chart.js visualizations
- ✅ Professional patent cards with threat analysis
- ✅ Activity timeline
- ✅ Print/export functionality
- ✅ Mobile-responsive design

## Weekly Rotation System

### Subdomain Naming Convention
- **Week 14:** `hermes.sqncr.ai/Patent_report_kw14`
- **Week 15:** `hermes.sqncr.ai/Patent_report_kw15`
- **Week 16:** `hermes.sqncr.ai/Patent_report_kw16`

### Deployment Process
1. Generate report with modern template
2. Copy to reports directory
3. Start HTTP server on port 8080
4. Start Cloudflare tunnel
5. Verify subdomain accessibility
6. Previous week's subdomain is shut down

## Report Generation Workflow

### For LLM Agents
```python
# 1. Load template
template_path = "reports/modern_report_template.html"

# 2. Customize with data
# - Update executive summary numbers
# - Replace chart data with real patent counts
# - Generate patent cards for each analyzed patent
# - Update timeline with recent activity

# 3. Save as weekly report
output_path = f"reports/weekly_report_{date}.html"
```

### Key Sections to Populate
1. **Executive Summary Cards:**
   - Total patents analyzed
   - High priority count
   - Active competitors
   - Technology coverage %

2. **Charts:**
   - Patents by competitor (bar chart)
   - Technology categories (doughnut chart)

3. **Patent Cards:**
   - Critical patents first
   - Include threat scores
   - Link to EPO/Espacenet
   - Action recommendations

4. **Timeline:**
   - Recent patent filings
   - Competitor activity
   - Strategic events

## CDN Resources (No Build Step Required)

```html
<!-- Tailwind CSS -->
<script src="https://cdn.tailwindcss.com"></script>

<!-- Chart.js -->
<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>

<!-- Font Awesome -->
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">

<!-- Google Fonts: Inter -->
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
```

## Example: Threat Score Visualization

```javascript
// Add to Chart.js configuration
const threatChart = new Chart(ctx, {
    type: 'bar',
    data: {
        labels: ['Mazak', 'Trumpf', 'Okuma', 'Haas'],
        datasets: [{
            label: 'Threat Score',
            data: [85, 62, 45, 38],
            backgroundColor: [
                '#ef4444',  // High - Red
                '#f59e0b',  // Medium - Orange
                '#3b82f6',  // Low - Blue
                '#10b981'   // Monitor - Green
            ]
        }]
    }
});
```

## Best Practices

1. **Mobile First:** Test reports on mobile devices
2. **Print Styles:** Ensure reports print well (`@media print`)
3. **Loading States:** Show skeleton screens while data loads
4. **Accessibility:** Use proper ARIA labels and contrast ratios
5. **Performance:** Lazy load charts, optimize images
6. **Branding:** Consistent colors matching client brand

## Next Steps for Future Reports

1. **Week 15:** Copy template, update data, deploy to `kw15` subdomain
2. **Enhancements:** Add more interactive filters, search functionality
3. **PDF Export:** Implement WeasyPrint or Puppeteer for PDF generation
4. **Email Integration:** Embed report links in email notifications
5. **Historical Comparison:** Add week-over-week trend charts

---

**Status:** Template ready for Week 14 deployment
