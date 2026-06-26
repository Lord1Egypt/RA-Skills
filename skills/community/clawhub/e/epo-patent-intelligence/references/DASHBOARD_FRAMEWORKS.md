# Enterprise Dashboard & Report Generation Research

**For:** EPO Patent Intelligence Skill  
**Date:** April 4, 2026  
**Purpose:** Research modern frameworks for professional patent intelligence reports

---

## Executive Summary

For the EPO Patent Intelligence skill, we need a **hybrid approach**:
- **HTML Reports:** Tailwind CSS + Vanilla JS for maximum portability
- **Data Visualization:** Chart.js (charts) + D3.js (complex visualizations)
- **PDF Generation:** Puppeteer (screenshot-to-PDF) or WeasyPrint (HTML-to-PDF)
- **Templates:** Jinja2 for HTML templating + custom CSS for patent report styling

**Recommendation:** Use a **single-file HTML approach** with embedded CSS/JS for maximum portability and zero dependencies.

---

## 1. Dashboard Framework Analysis

### 1.1 React-Based Solutions

#### Material-UI (MUI) + React
```javascript
// Material-UI Dashboard Component Example
import React from 'react';
import { Card, CardContent, Typography, Chip, Grid } from '@mui/material';
import { DataGrid } from '@mui/x-data-grid';

const PatentCard = ({ patent }) => (
  <Card variant="outlined" sx={{ mb: 2, borderLeft: 4, borderColor: 'warning.main' }}>
    <CardContent>
      <Typography variant="h6" component="h3">
        {patent.title}
      </Typography>
      <Typography color="text.secondary" gutterBottom>
        {patent.company} • {patent.filing_date}
      </Typography>
      <Chip 
        label={patent.threat_level} 
        color={patent.threat_level === 'Critical' ? 'error' : 'warning'}
        size="small"
        sx={{ mr: 1 }}
      />
      <Chip label={patent.technology_category} variant="outlined" size="small" />
    </CardContent>
  </Card>
);
```

**Pros:**
- Enterprise-grade component library
- Excellent TypeScript support
- Rich ecosystem (MUI X Data Grid for tables)
- Professional theming system

**Cons:**
- Requires build step (webpack/vite)
- Heavy for simple reports (200KB+ bundle)
- Overkill for static HTML generation

**Verdict:** ❌ **Not recommended** for patent reports (too heavy)

---

#### Ant Design (AntD)
```javascript
import { Card, Tag, Statistic, Row, Col } from 'antd';
import { AlertOutlined, FileTextOutlined } from '@ant-design/icons';

const PatentDashboard = ({ patents }) => (
  <Row gutter={[16, 16]}>
    <Col span={6}>
      <Card>
        <Statistic 
          title="Total Patents" 
          value={patents.length}
          prefix={<FileTextOutlined />}
        />
      </Card>
    </Col>
    <Col span={6}>
      <Card>
        <Statistic 
          title="Critical Threats" 
          value={patents.filter(p => p.threat === 'Critical').length}
          valueStyle={{ color: '#cf1322' }}
          prefix={<AlertOutlined />}
        />
      </Card>
    </Col>
  </Row>
);
```

**Pros:**
- Comprehensive enterprise components
- Excellent for data-heavy applications
- Chinese-friendly (if needed)

**Cons:**
- Large bundle size (~500KB)
- Complex theming
- Build step required

**Verdict:** ❌ **Not recommended** (too heavy for reports)

---

### 1.2 Vue-Based Solutions

#### Vuetify (Material Design for Vue)
```vue
<template>
  <v-card v-for="patent in patents" :key="patent.id" class="mb-4" outlined>
    <v-card-title>
      {{ patent.title }}
      <v-chip 
        :color="getThreatColor(patent.threat_level)" 
        small 
        class="ml-2"
      >
        {{ patent.threat_level }}
      </v-chip>
    </v-card-title>
    <v-card-subtitle>
      {{ patent.company }} • {{ patent.filing_date }}
    </v-card-subtitle>
    <v-card-text>
      <v-chip-group>
        <v-chip v-for="tech in patent.technologies" :key="tech" outlined small>
          {{ tech }}
        </v-chip>
      </v-chip-group>
    </v-card-text>
  </v-card>
</template>

<script>
export default {
  props: ['patents'],
  methods: {
    getThreatColor(level) {
      const colors = { Critical: 'red', High: 'orange', Medium: 'yellow', Low: 'green' };
      return colors[level] || 'grey';
    }
  }
}
</script>
```

**Pros:**
- Beautiful Material Design components
- Good for progressive web apps
- Responsive grid system

**Cons:**
- Requires Vue build toolchain
- Bundle size ~300KB
- Not suitable for static HTML

**Verdict:** ❌ **Not recommended** (build step required)

---

#### Element Plus
```vue
<template>
  <el-card v-for="patent in patents" :key="patent.id" class="patent-card">
    <template #header>
      <div class="card-header">
        <span>{{ patent.title }}</span>
        <el-tag :type="getTagType(patent.threat_level)">
          {{ patent.threat_level }}
        </el-tag>
      </div>
    </template>
    <p><strong>Company:</strong> {{ patent.company }}</p>
    <p><strong>Date:</strong> {{ patent.filing_date }}</p>
    <el-tag v-for="cat in patent.categories" :key="cat" effect="plain">
      {{ cat }}
    </el-tag>
  </el-card>
</template>
```

**Pros:**
- Clean, minimal design
- Good documentation
- Smaller than Vuetify

**Cons:**
- Still requires Vue build
- Limited customization

**Verdict:** ❌ **Not recommended** (build step required)

---

### 1.3 Vanilla JS Solutions ⭐ **RECOMMENDED**

#### Alpine.js (Lightweight Reactivity)
```html
<!DOCTYPE html>
<html>
<head>
  <script defer src="https://cdn.jsdelivr.net/npm/alpinejs@3.x.x/dist/cdn.min.js"></script>
  <script src="https://cdn.tailwindcss.com"></script>
</head>
<body>
  <div x-data="{ patents: [], threatFilter: 'all' }" x-init="fetchPatents()">
    <!-- Filter Controls -->
    <div class="mb-4">
      <select x-model="threatFilter" class="border p-2 rounded">
        <option value="all">All Threats</option>
        <option value="Critical">Critical</option>
        <option value="High">High</option>
        <option value="Medium">Medium</option>
      </select>
    </div>
    
    <!-- Patent Cards -->
    <template x-for="patent in patents.filter(p => threatFilter === 'all' || p.threat === threatFilter)" :key="patent.id">
      <div class="border-l-4 p-4 mb-4 rounded shadow"
           :class="{
             'border-red-500 bg-red-50': patent.threat === 'Critical',
             'border-orange-500 bg-orange-50': patent.threat === 'High',
             'border-yellow-500 bg-yellow-50': patent.threat === 'Medium'
           }">
        <h3 x-text="patent.title" class="text-lg font-bold"></h3>
        <p class="text-gray-600" x-text="patent.company + ' • ' + patent.date"></p>
        <span x-text="patent.threat" class="inline-block px-2 py-1 rounded text-sm"
              :class="{
                'bg-red-500 text-white': patent.threat === 'Critical',
                'bg-orange-500 text-white': patent.threat === 'High'
              }"></span>
      </div>
    </template>
  </div>
</body>
</html>
```

**Pros:**
- ✅ Zero build step required
- ✅ 15KB minified (Alpine.js)
- ✅ React-like syntax without build
- ✅ Perfect for static HTML reports
- ✅ Easy interactivity (filtering, sorting)

**Cons:**
- Less powerful than React/Vue
- Limited ecosystem

**Verdict:** ✅ **STRONG RECOMMENDATION** for patent reports

---

#### Petite-Vue (2KB Alpine Alternative)
```html
<script type="module">
  import { createApp } from 'https://unpkg.com/petite-vue?module'
  
  createApp({
    patents: [],
    filter: 'all',
    get filteredPatents() {
      return this.filter === 'all' 
        ? this.patents 
        : this.patents.filter(p => p.threat === this.filter)
    }
  }).mount()
</script>

<div v-scope="{ patents: patentData }">
  <select v-model="filter">
    <option value="all">All</option>
    <option value="Critical">Critical</option>
  </select>
  
  <div v-for="patent in filteredPatents" :key="patent.id">
    {{ patent.title }}
  </div>
</div>
```

**Pros:**
- ✅ Only 2KB!
- ✅ Vue-like syntax
- ✅ No build step
- ✅ Perfect for embedded reports

**Verdict:** ✅ **EXCELLENT** for ultra-lightweight reports

---

## 2. Data Visualization Libraries

### 2.1 Chart.js ⭐ **RECOMMENDED**
```html
<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>

<canvas id="threatChart" width="400" height="200"></canvas>

<script>
const ctx = document.getElementById('threatChart').getContext('2d');
new Chart(ctx, {
  type: 'doughnut',
  data: {
    labels: ['Critical', 'High', 'Medium', 'Low', 'None'],
    datasets: [{
      data: [5, 12, 25, 15, 8],
      backgroundColor: [
        '#dc2626', // red-600
        '#ea580c', // orange-600
        '#ca8a04', // yellow-600
        '#16a34a', // green-600
        '#6b7280'  // gray-500
      ]
    }]
  },
  options: {
    responsive: true,
    plugins: {
      title: { display: true, text: 'Patent Threat Distribution' },
      legend: { position: 'bottom' }
    }
  }
});
</script>
```

**Why Chart.js:**
- ✅ 60KB minified (with tree-shaking)
- ✅ CDN availability
- ✅ Excellent documentation
- ✅ Simple, clean API
- ✅ Perfect for patent metrics (pie charts, bar charts, time series)

---

### 2.2 D3.js (Complex Visualizations)
```javascript
// Patent Timeline Visualization
const svg = d3.select("#timeline")
  .append("svg")
  .attr("width", 800)
  .attr("height", 200);

const x = d3.scaleTime()
  .domain([new Date(2024, 0, 1), new Date()])
  .range([50, 750]);

svg.selectAll("circle")
  .data(patents)
  .enter()
  .append("circle")
  .attr("cx", d => x(new Date(d.filing_date)))
  .attr("cy", 100)
  .attr("r", d => Math.sqrt(d.citations) * 2)
  .attr("fill", d => threatColors[d.threat_level])
  .on("mouseover", showPatentTooltip);
```

**Why D3.js:**
- ✅ Infinite flexibility
- ✅ Network graphs, timelines, custom charts
- ✅ Patent citation networks
- ❌ Steep learning curve
- ❌ 300KB+ bundle

**Verdict:** Use D3 only for complex visualizations, not basic reports.

---

### 2.3 ApexCharts (Modern Alternative)
```html
<script src="https://cdn.jsdelivr.net/npm/apexcharts"></script>

<div id="chart"></div>

<script>
const options = {
  series: [{
    name: 'Patents Filed',
    data: [30, 40, 35, 50, 49, 60, 70]
  }],
  chart: { type: 'area', height: 350 },
  xaxis: { categories: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul'] },
  colors: ['#3b82f6'],
  fill: { type: 'gradient' }
};

const chart = new ApexCharts(document.querySelector("#chart"), options);
chart.render();
</script>
```

**Why ApexCharts:**
- ✅ Modern design
- ✅ Interactive features
- ✅ 80KB gzipped
- ✅ Good for dashboards

---

## 3. CSS Frameworks for Enterprise Styling

### 3.1 Tailwind CSS ⭐ **STRONG RECOMMENDATION**
```html
<!-- Patent Report Card with Tailwind -->
<div class="max-w-4xl mx-auto p-6">
  <!-- Executive Summary Header -->
  <div class="bg-gradient-to-r from-blue-600 to-blue-800 text-white p-6 rounded-lg shadow-lg mb-6">
    <h1 class="text-3xl font-bold mb-2">Weekly Patent Intelligence Report</h1>
    <p class="text-blue-100">Client: DMG Mori • Week of April 4, 2026</p>
  </div>
  
  <!-- Stats Grid -->
  <div class="grid grid-cols-4 gap-4 mb-6">
    <div class="bg-white p-4 rounded-lg shadow border-l-4 border-blue-500">
      <p class="text-gray-500 text-sm">Total Patents</p>
      <p class="text-2xl font-bold">65</p>
    </div>
    <div class="bg-white p-4 rounded-lg shadow border-l-4 border-red-500">
      <p class="text-gray-500 text-sm">Critical Threats</p>
      <p class="text-2xl font-bold text-red-600">5</p>
    </div>
    <div class="bg-white p-4 rounded-lg shadow border-l-4 border-orange-500">
      <p class="text-gray-500 text-sm">High Priority</p>
      <p class="text-2xl font-bold text-orange-600">12</p>
    </div>
    <div class="bg-white p-4 rounded-lg shadow border-l-4 border-yellow-500">
      <p class="text-gray-500 text-sm">New Technologies</p>
      <p class="text-2xl font-bold text-yellow-600">8</p>
    </div>
  </div>
  
  <!-- Patent Card -->
  <div class="bg-white rounded-lg shadow-md overflow-hidden mb-4 border-l-4 border-red-500">
    <div class="p-6">
      <div class="flex justify-between items-start mb-4">
        <div>
          <h3 class="text-xl font-semibold text-gray-900">Spindle Lubricator System</h3>
          <p class="text-gray-600">YAMAZAKI MAZAK CORP • Filed: 2026-03-15</p>
        </div>
        <span class="px-3 py-1 bg-red-100 text-red-800 rounded-full text-sm font-medium">
          Critical Threat
        </span>
      </div>
      
      <div class="prose max-w-none mb-4">
        <p class="text-gray-700">
          <strong>Abstract:</strong> A spindle lubrication system for CNC machining centers 
          that reduces heat generation and extends tool life through advanced cooling mechanisms...
        </p>
      </div>
      
      <div class="flex gap-2 mb-4">
        <span class="px-2 py-1 bg-blue-100 text-blue-800 rounded text-xs">CNC Machining</span>
        <span class="px-2 py-1 bg-purple-100 text-purple-800 rounded text-xs">Spindle Technology</span>
        <span class="px-2 py-1 bg-green-100 text-green-800 rounded text-xs">Thermal Management</span>
      </div>
      
      <div class="bg-gray-50 p-4 rounded-lg border-l-4 border-blue-400">
        <h4 class="font-semibold text-gray-900 mb-2">Strategic Analysis</h4>
        <p class="text-gray-700 text-sm">
          ⚠️ <strong>Competitive Threat:</strong> Mazak patenting spindle lubrication technology 
          directly competes with DMG Mori's core CNC offerings. This threatens DMG's competitive 
          advantage in high-precision machining...
        </p>
        <div class="mt-3 flex gap-2">
          <span class="text-xs px-2 py-1 bg-orange-100 text-orange-800 rounded">Weekly Review</span>
          <span class="text-xs px-2 py-1 bg-gray-200 text-gray-700 rounded">CNC Division</span>
        </div>
      </div>
    </div>
  </div>
</div>
```

**Tailwind Benefits:**
- ✅ Zero build step (CDN version)
- ✅ Utility-first = consistent styling
- ✅ Responsive by default
- ✅ Professional look out-of-box
- ✅ Easy to customize
- ✅ Small footprint with PurgeCSS

---

### 3.2 Bootstrap 5 (Classic Enterprise)
```html
<div class="container py-5">
  <div class="card border-danger mb-4">
    <div class="card-header bg-danger text-white d-flex justify-content-between">
      <span>Spindle Lubricator System</span>
      <span class="badge bg-light text-danger">Critical Threat</span>
    </div>
    <div class="card-body">
      <h6 class="card-subtitle mb-2 text-muted">YAMAZAKI MAZAK CORP • Filed: 2026-03-15</h6>
      <p class="card-text">
        <span class="badge bg-primary">CNC Machining</span>
        <span class="badge bg-secondary">Spindle Tech</span>
      </p>
      <div class="alert alert-warning">
        <strong>⚠️ Competitive Threat:</strong> Mazak patenting core technology...
      </div>
    </div>
  </div>
</div>
```

**Bootstrap Pros/Cons:**
- ✅ Familiar to most developers
- ✅ Good documentation
- ✅ Component library included
- ❌ "Bootstrap look" (generic)
- ❌ Requires build for customization

**Verdict:** Good for quick prototyping, but Tailwind is better for custom branding.

---

### 3.3 Custom CSS (For Ultimate Control)
```css
/* Patent Report Design System */
:root {
  --threat-critical: #dc2626;
  --threat-high: #ea580c;
  --threat-medium: #ca8a04;
  --threat-low: #16a34a;
  --primary-blue: #2563eb;
  --bg-light: #f8fafc;
}

.patent-card {
  background: white;
  border-radius: 8px;
  box-shadow: 0 1px 3px rgba(0,0,0,0.1);
  margin-bottom: 1rem;
  overflow: hidden;
}

.patent-card.critical { border-left: 4px solid var(--threat-critical); }
.patent-card.high { border-left: 4px solid var(--threat-high); }

.threat-badge {
  display: inline-block;
  padding: 0.25rem 0.75rem;
  border-radius: 9999px;
  font-size: 0.875rem;
  font-weight: 500;
}

.threat-badge.critical {
  background: var(--threat-critical);
  color: white;
}
```

---

## 4. Report Generation Libraries

### 4.1 Puppeteer (HTML to PDF) ⭐ **RECOMMENDED**
```javascript
const puppeteer = require('puppeteer');

async function generatePDF(htmlContent, outputPath) {
  const browser = await puppeteer.launch();
  const page = await browser.newPage();
  
  // Load HTML content
  await page.setContent(htmlContent, { waitUntil: 'networkidle0' });
  
  // Generate PDF with professional settings
  await page.pdf({
    path: outputPath,
    format: 'A4',
    printBackground: true,
    margin: {
      top: '20mm',
      right: '20mm',
      bottom: '20mm',
      left: '20mm'
    },
    displayHeaderFooter: true,
    headerTemplate: `
      <div style="font-size: 9px; margin-left: 20mm; margin-top: 5mm; width: 100%;">
        <span>Patent Intelligence Report • DMG Mori</span>
      </div>
    `,
    footerTemplate: `
      <div style="font-size: 9px; margin-left: 20mm; margin-bottom: 5mm; width: 100%;">
        <span>Page <span class="pageNumber"></span> of <span class="totalPages"></span></span>
        <span style="float: right; margin-right: 20mm;">Confidential</span>
      </div>
    `
  });
  
  await browser.close();
}
```

**Puppeteer Benefits:**
- ✅ Renders HTML exactly as browser displays
- ✅ Full CSS support (including Tailwind)
- ✅ JavaScript execution in PDF
- ✅ Charts rendered perfectly
- ✅ Header/footer support
- ✅ Professional quality

**Cons:**
- Requires Node.js
- ~100MB Chromium download
- Slower than alternatives

---

### 4.2 WeasyPrint (Python HTML to PDF)
```python
from weasyprint import HTML, CSS

def generate_patent_report(html_content, output_path):
    """Generate PDF from HTML using WeasyPrint"""
    html = HTML(string=html_content)
    
    # Custom CSS for print optimization
    css = CSS(string='''
        @page {
            size: A4;
            margin: 20mm;
            @top-center { content: "Patent Intelligence Report"; font-size: 9pt; }
            @bottom-center { content: "Page " counter(page) " of " counter(pages); }
        }
        .patent-card { break-inside: avoid; }
        h2 { break-after: avoid; }
    ''')
    
    html.write_pdf(output_path, stylesheets=[css])

# Usage
html_report = generate_html_report(patents)
generate_patent_report(html_report, 'reports/weekly_report.pdf')
```

**WeasyPrint Benefits:**
- ✅ Pure Python (no Node.js)
- ✅ Good CSS support
- ✅ Print-specific CSS features
- ✅ Page break control

**Cons:**
- Complex setup (GTK dependencies)
- Limited JavaScript support (no charts)
- Slower CSS processing

**Verdict:** Good for text-heavy reports, not for interactive charts.

---

### 4.3 Playwright (Modern Alternative)
```python
from playwright.sync_api import sync_playwright

def html_to_pdf(html_content, output_path):
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.set_content(html_content)
        page.pdf(
            path=output_path,
            format='A4',
            margin={'top': '20mm', 'right': '20mm', 'bottom': '20mm', 'left': '20mm'},
            display_header_footer=True,
            header_template='<div style="font-size:9px;margin-left:20mm;">Patent Report</div>',
            footer_template='<div style="font-size:9px;margin-left:20mm;">Page <span class="pageNumber"></span></div>'
        )
        browser.close()
```

**Playwright:** Modern replacement for Puppeteer, same API.

---

### 4.4 Jinja2 Templating (HTML Generation)
```python
from jinja2 import Environment, FileSystemLoader
import json

# Setup Jinja2
env = Environment(loader=FileSystemLoader('templates'))
template = env.get_template('patent_report.html')

# Render with data
html_output = template.render(
    client_name="DMG Mori",
    report_date="2026-04-04",
    patents=patent_data,
    stats={
        'total': 65,
        'critical': 5,
        'high': 12,
        'medium': 25
    },
    threat_colors={
        'Critical': '#dc2626',
        'High': '#ea580c',
        'Medium': '#ca8a04',
        'Low': '#16a34a'
    }
)

# Template (templates/patent_report.html)
"""
<!DOCTYPE html>
<html>
<head>
  <title>Patent Report - {{ client_name }}</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
</head>
<body class="bg-gray-100">
  <div class="max-w-4xl mx-auto p-6">
    <h1 class="text-3xl font-bold mb-2">Weekly Patent Intelligence Report</h1>
    <p class="text-gray-600 mb-6">{{ client_name }} • {{ report_date }}</p>
    
    <!-- Stats -->
    <div class="grid grid-cols-4 gap-4 mb-6">
      <div class="bg-white p-4 rounded shadow">
        <p class="text-gray-500">Total Patents</p>
        <p class="text-2xl font-bold">{{ stats.total }}</p>
      </div>
      <div class="bg-white p-4 rounded shadow border-l-4 border-red-500">
        <p class="text-gray-500">Critical</p>
        <p class="text-2xl font-bold text-red-600">{{ stats.critical }}</p>
      </div>
      <!-- ... -->
    </div>
    
    <!-- Patent Cards -->
    {% for patent in patents %}
    <div class="bg-white rounded-lg shadow mb-4 border-l-4" 
         style="border-color: {{ threat_colors[patent.threat_level] }}">
      <div class="p-6">
        <h3>{{ patent.title }}</h3>
        <p>{{ patent.company }} • {{ patent.filing_date }}</p>
        <span class="badge" style="background: {{ threat_colors[patent.threat_level] }}">
          {{ patent.threat_level }}
        </span>
      </div>
    </div>
    {% endfor %}
  </div>
</body>
</html>
"""
```

---

## 5. Patent/Intelligence Report Best Practices

### 5.1 Industry Examples

#### Example 1: Google Patents Dashboard
- Clean, minimal design
- Search-focused interface
- Patent cards with key metadata
- Citation visualization

#### Example 2: PatSnap Intelligence Reports
- Executive summary at top
- Technology trend charts
- Competitor comparison matrices
- Patent family trees

#### Example 3: Cipher Patent Intelligence
- Heat maps for technology areas
- Timeline visualizations
- Strength/score metrics
- Export to PowerPoint/PDF

### 5.2 Recommended Report Structure
```
1. EXECUTIVE SUMMARY
   - Key metrics (total patents, threats, trends)
   - Critical alerts (top 3 urgent items)
   - Strategic recommendations

2. COMPETITOR DASHBOARD
   - Competitor activity chart (timeline)
   - Patent count by company
   - Technology focus areas

3. THREAT ANALYSIS
   - Critical patents (red cards)
   - High priority patents (orange cards)
   - Technology category breakdown

4. TECHNOLOGY TRENDS
   - Emerging technologies chart
   - Filing trends over time
   - Geographic distribution

5. DETAILED PATENT CARDS
   - Individual patent analysis
   - Strategic implications
   - Recommended actions

6. APPENDIX
   - Full patent list
   - Methodology
   - Data sources
```

### 5.3 Visual Design Principles

**Color Coding for Threat Levels:**
```css
--threat-critical: #dc2626;  /* Red - immediate action */
--threat-high: #ea580c;      /* Orange - weekly review */
--threat-medium: #ca8a04;    /* Yellow - monthly review */
--threat-low: #16a34a;       /* Green - monitor only */
```

**Card Design Pattern:**
- Left border color = threat level
- Header = Title + threat badge
- Meta = Company + date + patent number
- Tags = Technology categories
- Analysis = Expandable strategic insight

**Typography Hierarchy:**
- H1: Report title (28px, bold)
- H2: Section headers (22px, semibold)
- H3: Patent titles (18px, semibold)
- Body: 14px, 1.5 line height
- Meta: 12px, gray-600

---

## 6. Implementation Recommendations

### 6.1 Recommended Stack for EPO Patent Reports

| Component | Tool | Reason |
|-----------|------|--------|
| **HTML Generation** | Jinja2 (Python) | Template inheritance, logic in templates |
| **CSS Framework** | Tailwind CSS (CDN) | Zero build, utility-first, professional |
| **Charts** | Chart.js (CDN) | Simple API, patent metrics visualization |
| **Interactivity** | Alpine.js (CDN) | Light filtering/sorting without build |
| **PDF Export** | Playwright (Python) | Modern Puppeteer alternative, great quality |

### 6.2 File Structure
```
epo-patent-intelligence/
├── templates/
│   ├── base_report.html      # Base template with CDN links
│   ├── patent_card.html      # Patent card component
│   ├── executive_summary.html
│   └── charts_section.html
├── static/
│   └── custom.css           # Patent-specific styles
├── scripts/
│   ├── report_generator.py  # Main generation script
│   └── pdf_exporter.py      # Playwright PDF export
└── reports/
    └── *.html, *.pdf
```

### 6.3 Sample Implementation

```python
# scripts/report_generator.py
from jinja2 import Environment, FileSystemLoader
from playwright.sync_api import sync_playwright
import sqlite3
import json
from datetime import datetime

class PatentReportGenerator:
    def __init__(self, template_dir='templates'):
        self.env = Environment(loader=FileSystemLoader(template_dir))
        self.threat_colors = {
            'Critical': '#dc2626',
            'High': '#ea580c',
            'Medium': '#ca8a04',
            'Low': '#16a34a',
            'None': '#6b7280'
        }
    
    def generate_html(self, patents, client_name, stats):
        """Generate HTML report from patent data"""
        template = self.env.get_template('base_report.html')
        
        return template.render(
            client_name=client_name,
            report_date=datetime.now().strftime('%Y-%m-%d'),
            patents=patents,
            stats=stats,
            threat_colors=self.threat_colors
        )
    
    def generate_pdf(self, html_content, output_path):
        """Convert HTML to PDF using Playwright"""
        with sync_playwright() as p:
            browser = p.chromium.launch()
            page = browser.new_page()
            page.set_content(html_content)
            page.pdf(
                path=output_path,
                format='A4',
                margin={'top': '20mm', 'right': '20mm', 'bottom': '20mm', 'left': '20mm'},
                display_header_footer=True,
                header_template=f'''
                    <div style="font-size:9px;margin-left:20mm;width:100%;">
                        Patent Intelligence Report • {datetime.now().strftime('%Y-%m-%d')}
                    </div>
                ''',
                footer_template='''
                    <div style="font-size:9px;margin-left:20mm;width:100%;">
                        Page <span class="pageNumber"></span> of <span class="totalPages"></span>
                        <span style="float:right;margin-right:20mm;">Confidential</span>
                    </div>
                '''
            )
            browser.close()
    
    def create_report(self, db_path, client_name, output_html, output_pdf=None):
        """Full pipeline: database → HTML → PDF"""
        # Load patents from database
        patents = self._load_patents(db_path)
        
        # Calculate stats
        stats = self._calculate_stats(patents)
        
        # Generate HTML
        html = self.generate_html(patents, client_name, stats)
        
        # Save HTML
        with open(output_html, 'w') as f:
            f.write(html)
        
        # Generate PDF if requested
        if output_pdf:
            self.generate_pdf(html, output_pdf)
        
        return output_html
    
    def _load_patents(self, db_path):
        """Load patents from SQLite database"""
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT * FROM patents 
            WHERE publication_date >= date('now', '-7 days')
            ORDER BY threat_level DESC, publication_date DESC
        ''')
        
        patents = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return patents
    
    def _calculate_stats(self, patents):
        """Calculate report statistics"""
        return {
            'total': len(patents),
            'critical': len([p for p in patents if p.get('threat_level') == 'Critical']),
            'high': len([p for p in patents if p.get('threat_level') == 'High']),
            'medium': len([p for p in patents if p.get('threat_level') == 'Medium']),
            'by_company': self._group_by_company(patents),
            'by_technology': self._group_by_technology(patents)
        }
    
    def _group_by_company(self, patents):
        from collections import Counter
        return dict(Counter(p['company'] for p in patents))
    
    def _group_by_technology(self, patents):
        from collections import Counter
        return dict(Counter(p.get('technology_category', 'Unknown') for p in patents))


# Usage example
if __name__ == '__main__':
    generator = PatentReportGenerator()
    generator.create_report(
        db_path='data/patents.db',
        client_name='DMG Mori',
        output_html='reports/weekly_report_20260404.html',
        output_pdf='reports/weekly_report_20260404.pdf'
    )
```

### 6.4 Base Template (templates/base_report.html)

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Patent Intelligence Report - {{ client_name }}</title>
  
  <!-- Tailwind CSS -->
  <script src="https://cdn.tailwindcss.com"></script>
  
  <!-- Chart.js -->
  <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
  
  <!-- Alpine.js for interactivity -->
  <script defer src="https://cdn.jsdelivr.net/npm/alpinejs@3.x.x/dist/cdn.min.js"></script>
  
  <!-- Custom Config -->
  <script>
    tailwind.config = {
      theme: {
        extend: {
          colors: {
            threat: {
              critical: '#dc2626',
              high: '#ea580c',
              medium: '#ca8a04',
              low: '#16a34a',
              none: '#6b7280'
            }
          }
        }
      }
    }
  </script>
  
  <style>
    @media print {
      .no-print { display: none !important; }
      .patent-card { break-inside: avoid; }
      .section-header { break-after: avoid; }
    }
    
    .patent-card {
      transition: transform 0.2s, box-shadow 0.2s;
    }
    
    .patent-card:hover {
      transform: translateY(-2px);
      box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.1);
    }
  </style>
</head>
<body class="bg-gray-100 min-h-screen">
  <!-- Print Button -->
  <div class="no-print fixed top-4 right-4 z-50">
    <button onclick="window.print()" 
            class="bg-blue-600 text-white px-4 py-2 rounded-lg shadow-lg hover:bg-blue-700 transition">
      🖨️ Print / Save PDF
    </button>
  </div>

  <div class="max-w-5xl mx-auto p-6">
    <!-- Header -->
    <header class="bg-gradient-to-r from-blue-700 to-blue-900 text-white p-8 rounded-xl shadow-lg mb-8">
      <div class="flex justify-between items-start">
        <div>
          <h1 class="text-4xl font-bold mb-2">Patent Intelligence Report</h1>
          <p class="text-blue-200 text-lg">{{ client_name }}</p>
          <p class="text-blue-300">Week of {{ report_date }}</p>
        </div>
        <div class="text-right">
          <div class="text-5xl font-bold">{{ stats.total }}</div>
          <div class="text-blue-200">Patents Analyzed</div>
        </div>
      </div>
    </header>

    <!-- Executive Summary -->
    {% include 'executive_summary.html' %}

    <!-- Charts Section -->
    {% include 'charts_section.html' %}

    <!-- Patent Cards -->
    <section class="mb-8" x-data="{ filter: 'all' }">
      <div class="flex justify-between items-center mb-6 section-header">
        <h2 class="text-2xl font-bold text-gray-800">Detailed Patent Analysis</h2>
        
        <!-- Filter Controls -->
        <div class="no-print">
          <select x-model="filter" 
                  class="border border-gray-300 rounded-lg px-4 py-2 focus:ring-2 focus:ring-blue-500">
            <option value="all">All Threats</option>
            <option value="Critical">Critical Only</option>
            <option value="High">High Only</option>
            <option value="Medium">Medium Only</option>
          </select>
        </div>
      </div>

      <!-- Patent Cards -->
      <div class="space-y-4">
        {% for patent in patents %}
        <article class="patent-card bg-white rounded-xl shadow-md overflow-hidden border-l-4"
                 :class="{ 'hidden': filter !== 'all' && filter !== '{{ patent.threat_level }}' }"
                 style="border-color: {{ threat_colors[patent.threat_level] }}">
          {% include 'patent_card.html' %}
        </article>
        {% endfor %}
      </div>
    </section>

    <!-- Footer -->
    <footer class="text-center text-gray-500 text-sm mt-12 pt-8 border-t">
      <p>Generated by EPO Patent Intelligence System</p>
      <p class="mt-1">{{ report_date }}</p>
    </footer>
  </div>

  <!-- Initialize Charts -->
  <script>
    // Threat Distribution Chart
    const threatCtx = document.getElementById('threatChart').getContext('2d');
    new Chart(threatCtx, {
      type: 'doughnut',
      data: {
        labels: ['Critical', 'High', 'Medium', 'Low'],
        datasets: [{
          data: [{{ stats.critical }}, {{ stats.high }}, {{ stats.medium }}, {{ stats.low }}],
          backgroundColor: ['#dc2626', '#ea580c', '#ca8a04', '#16a34a']
        }]
      },
      options: {
        responsive: true,
        plugins: {
          legend: { position: 'bottom' },
          title: { display: true, text: 'Threat Level Distribution' }
        }
      }
    });
    
    // Company Chart
    const companyCtx = document.getElementById('companyChart').getContext('2d');
    new Chart(companyCtx, {
      type: 'bar',
      data: {
        labels: {{ stats.by_company.keys() | list | tojson }},
        datasets: [{
          label: 'Patents Filed',
          data: {{ stats.by_company.values() | list | tojson }},
          backgroundColor: '#3b82f6'
        }]
      },
      options: {
        responsive: true,
        plugins: {
          title: { display: true, text: 'Patents by Competitor' }
        }
      }
    });
  </script>
</body>
</html>
```

---

## 7. Summary & Action Items

### 7.1 Recommended Technology Stack

| Purpose | Recommended Tool | Alternative |
|---------|-----------------|-------------|
| HTML Generation | Jinja2 (Python) | Handlebars, Mustache |
| Styling | Tailwind CSS (CDN) | Bootstrap 5 (CDN) |
| Charts | Chart.js (CDN) | ApexCharts |
| Interactivity | Alpine.js (CDN) | Petite-Vue |
| PDF Export | Playwright (Python) | Puppeteer (Node) |
| Icons | Heroicons (SVG) | Font Awesome |

### 7.2 Key Advantages of This Stack

1. **Zero Build Step** - All tools work via CDN, no webpack/vite needed
2. **Single-File Reports** - Portable HTML files with embedded logic
3. **Professional Output** - Enterprise-grade design out-of-box
4. **PDF Ready** - HTML renders perfectly to PDF
5. **Interactive** - Filtering/sorting without server
6. **Maintainable** - Jinja2 templates separate logic from presentation

### 7.3 Implementation Steps

1. ✅ Create `templates/` directory with base template
2. ✅ Set up Jinja2 environment in Python
3. ✅ Create patent card component template
4. ✅ Add Tailwind + Chart.js + Alpine.js CDN links
5. ✅ Implement report generator class
6. ✅ Add Playwright PDF export
7. ✅ Test with real patent data
8. ✅ Style for DMG Mori branding

### 7.4 Files to Create

```
templates/
├── base_report.html         # Main template with CDN links
├── patent_card.html         # Reusable patent card component
├── executive_summary.html   # Stats and key findings
├── charts_section.html      # Chart.js visualizations
└── competitor_section.html  # Competitor breakdown

scripts/
└── report_generator.py      # Main generation script

static/
└── custom.css               # Patent-specific custom styles
```

---

## 8. References & Resources

### 8.1 Official Documentation
- **Tailwind CSS:** https://tailwindcss.com/docs
- **Chart.js:** https://www.chartjs.org/docs/
- **Alpine.js:** https://alpinejs.dev/
- **Jinja2:** https://jinja.palletsprojects.com/
- **Playwright:** https://playwright.dev/python/

### 8.2 Design Inspiration
- **PatSnap:** https://www.patsnap.com/ (patent intelligence dashboards)
- **Google Patents:** https://patents.google.com/ (clean patent cards)
- **Cipher:** https://cipher.ai/ (patent analytics)

### 8.3 Color Palettes
```css
/* Enterprise Blue Theme */
--primary: #1e40af;
--secondary: #3b82f6;
--accent: #60a5fa;

/* Threat Level Colors */
--critical: #dc2626;
--high: #ea580c;
--medium: #ca8a04;
--low: #16a34a;

/* Neutral */
--bg: #f8fafc;
--text: #1f2937;
--muted: #6b7280;
```

---

**Document Version:** 1.0  
**Last Updated:** April 4, 2026  
**Author:** Subagent Research Team  
**Purpose:** EPO Patent Intelligence Skill - Report Generation Framework Selection
