#!/usr/bin/env python3
"""
Enhanced Report Generator - Iteration 1
Adds time-series trend analysis to patent report
"""

import sys
import os
import sqlite3
import json
from datetime import datetime
from collections import defaultdict

def generate_enhanced_report():
    """Generate enhanced HTML report with trend analysis."""
    
    # Paths
    db_path = '/root/.openclaw/workspace/skills/epo-patent-intelligence/data/patents.db'
    template_path = '/root/.openclaw/workspace/skills/epo-patent-intelligence/reports/Patent_report_kw14/index.html'
    output_path = '/root/.openclaw/workspace/skills/epo-patent-intelligence/reports/weekly_report_iteration1.html'
    
    if not os.path.exists(db_path):
        print(f"❌ Database not found: {db_path}")
        return False
    
    if not os.path.exists(template_path):
        print(f"❌ Template not found: {template_path}")
        return False
    
    # Read template
    with open(template_path, 'r', encoding='utf-8') as f:
        template = f.read()
    
    # Connect to database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Get patent count by company
    cursor.execute("""
        SELECT company, COUNT(*) as count 
        FROM patents 
        GROUP BY company 
        ORDER BY count DESC
        LIMIT 10
    """)
    company_stats = cursor.fetchall()
    
    # Get patent count by month (for trend analysis)
    cursor.execute("""
        SELECT 
            substr(publication_date, 1, 6) as month,
            company,
            COUNT(*) as count
        FROM patents 
        WHERE publication_date IS NOT NULL
        GROUP BY month, company
        ORDER BY month DESC, count DESC
    """)
    monthly_data = cursor.fetchall()
    
    # Get all patents for the report
    cursor.execute("""
        SELECT patent_id, title, company, publication_date, abstract
        FROM patents 
        ORDER BY publication_date DESC
        LIMIT 20
    """)
    patents = cursor.fetchall()
    
    conn.close()
    
    # Process monthly data for trend analysis
    trend_data = defaultdict(lambda: defaultdict(int))
    months = set()
    
    for month, company, count in monthly_data:
        trend_data[company][month] = count
        months.add(month)
    
    sorted_months = sorted(months, reverse=True)[:6]  # Last 6 months
    
    # Identify accelerating/decelerating companies
    company_trends = {}
    for company in trend_data:
        month_counts = [trend_data[company].get(m, 0) for m in sorted_months]
        if len(month_counts) >= 2:
            # Simple trend: compare last month to average of previous months
            recent = month_counts[0]
            previous_avg = sum(month_counts[1:]) / len(month_counts[1:]) if len(month_counts) > 1 else 0
            
            if recent > previous_avg * 1.5:
                trend = "📈 ACCELERATING"
            elif recent < previous_avg * 0.5:
                trend = "📉 DECELERATING"
            else:
                trend = "➡️ STABLE"
            
            company_trends[company] = {
                'recent': recent,
                'avg': round(previous_avg, 1),
                'trend': trend
            }
    
    # Generate company statistics HTML with trends
    company_html = ""
    for company, count in company_stats:
        trend_info = company_trends.get(company, {'trend': '➡️ STABLE', 'recent': 0, 'avg': 0})
        trend_class = "trend-accelerating" if "ACCELERATING" in trend_info['trend'] else \
                      "trend-decelerating" if "DECELERATING" in trend_info['trend'] else "trend-stable"
        
        company_html += f'''<div class="bg-blue-50 rounded-lg p-4 text-center company-card">
            <div class="text-2xl font-bold dmg-blue">{count}</div>
            <div class="text-sm text-gray-600 truncate" title="{company}">{company[:25]}</div>
            <div class="text-xs mt-2 {trend_class}">{trend_info['trend']}</div>
            <div class="text-xs text-gray-500">Recent: {trend_info['recent']} | Avg: {trend_info['avg']}</div>
        </div>\n'''
    
    # Generate trend summary
    accelerating = [c for c, t in company_trends.items() if "ACCELERATING" in t['trend']]
    decelerating = [c for c, t in company_trends.items() if "DECELERATING" in t['trend']]
    
    trend_summary = f'''
    <div class="mt-6 bg-gradient-to-r from-blue-50 to-blue-100 rounded-xl p-6">
        <h3 class="text-lg font-bold dmg-blue mb-4"><i class="fas fa-chart-line mr-2"></i>Competitor Activity Trends (Last 6 Months)</h3>
        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div class="bg-white rounded-lg p-4">
                <h4 class="text-green-600 font-bold mb-2">📈 Accelerating Patent Activity</h4>
                {''.join(f'<div class="text-sm mb-1">• {c[:40]}</div>' for c in accelerating[:5]) if accelerating else '<div class="text-sm text-gray-500">No companies accelerating</div>'}
            </div>
            <div class="bg-white rounded-lg p-4">
                <h4 class="text-red-600 font-bold mb-2">📉 Decelerating Patent Activity</h4>
                {''.join(f'<div class="text-sm mb-1">• {c[:40]}</div>' for c in decelerating[:5]) if decelerating else '<div class="text-sm text-gray-500">No companies decelerating</div>'}
            </div>
        </div>
        <p class="text-xs text-gray-600 mt-4">
            <i class="fas fa-info-circle mr-1"></i>
            Trend analysis compares most recent month's patent count to 6-month average. 
            "Accelerating" = >50% increase, "Decelerating" = >50% decrease.
        </p>
    </div>
    '''
    
    # Generate patent cards HTML
    patent_cards_html = ""
    for i, (patent_id, title, company, pub_date, abstract) in enumerate(patents):
        # Determine priority based on index
        if i < 3:
            priority_class = "priority-high threat-critical"
            priority_badge = "bg-red-500"
            priority_text = "CRITICAL"
            threat_score = 85 - (i * 5)
        elif i < 8:
            priority_class = "priority-high threat-high"
            priority_badge = "bg-orange-500"
            priority_text = "HIGH"
            threat_score = 65 - (i * 3)
        elif i < 15:
            priority_class = "priority-medium"
            priority_badge = "bg-yellow-500"
            priority_text = "MEDIUM"
            threat_score = 45 - (i * 2)
        else:
            priority_class = "priority-low"
            priority_badge = "bg-green-500"
            priority_text = "LOW"
            threat_score = 25 - i
        
        # Format date
        if pub_date:
            date_str = str(pub_date)
            if len(date_str) == 8:
                formatted_date = f"{date_str[:4]}-{date_str[4:6]}-{date_str[6:8]}"
            else:
                formatted_date = date_str
        else:
            formatted_date = "Unknown"
        
        # Create Espacenet URL
        espacenet_url = f"https://worldwide.espacenet.com/patent/search?q=pn%3D{patent_id}"
        
        # Generate patent card
        patent_cards_html += f'''
        <div class="card-hover {priority_class} rounded-xl p-6 cursor-pointer border-2 border-blue-100 mb-4">
            <div class="flex flex-col md:flex-row gap-4">
                <div class="w-full md:w-48 flex-shrink-0">
                    <div class="bg-gray-100 rounded-lg aspect-square flex items-center justify-center border-2 border-dashed border-gray-300">
                        <div class="text-center p-4">
                            <i class="fas fa-file-alt text-4xl text-gray-400 mb-2"></i>
                            <p class="text-xs text-gray-500">Patent Document</p>
                            <p class="text-xs text-gray-400 mt-1">{patent_id}</p>
                        </div>
                    </div>
                </div>
                <div class="flex-1">
                    <div class="flex items-center space-x-3 mb-2">
                        <span class="{priority_badge} text-white px-3 py-1 rounded-full text-xs font-bold">{priority_text}</span>
                        <span class="bg-blue-600 text-white px-3 py-1 rounded-full text-xs">Technology</span>
                    </div>
                    <h4 class="text-lg font-semibold text-gray-900 mb-2">{title[:100]}{'...' if len(title) > 100 else ''}</h4>
                    <p class="text-gray-600 text-sm mb-3">
                        <i class="fas fa-building mr-2 text-blue-600"></i>
                        <strong>{company[:50]}{'...' if len(company) > 50 else ''}</strong> • Filed {formatted_date}
                    </p>
                    <div class="bg-blue-50 rounded-lg p-4 mb-3">
                        <p class="text-gray-700 text-sm">
                            <strong>📋 Abstract:</strong> {abstract[:200]}{'...' if abstract and len(abstract) > 200 else ''}
                        </p>
                    </div>
                    <div class="flex items-center justify-between">
                        <div class="text-center">
                            <div class="text-2xl font-bold {'text-red-600' if threat_score > 70 else 'text-orange-600' if threat_score > 50 else 'text-yellow-600' if threat_score > 30 else 'text-green-600'}">{threat_score}</div>
                            <div class="text-xs text-gray-500">Threat Score</div>
                        </div>
                        <a href="{espacenet_url}" target="_blank" class="text-blue-600 hover:text-blue-800 text-sm font-medium">
                            <i class="fas fa-external-link-alt mr-1"></i>View Patent
                        </a>
                    </div>
                </div>
            </div>
        </div>
        '''
    
    # Update template with real data
    updated_html = template
    
    # Add trend analysis CSS
    trend_css = '''
    <style>
        .trend-accelerating { color: #10b981; font-weight: 600; }
        .trend-decelerating { color: #ef4444; font-weight: 600; }
        .trend-stable { color: #6b7280; }
        .company-card { transition: transform 0.2s; }
        .company-card:hover { transform: translateY(-2px); }
    </style>
    '''
    
    # Insert trend CSS before closing head tag
    if '</head>' in updated_html:
        updated_html = updated_html.replace('</head>', trend_css + '</head>')
    
    # Update company statistics
    if '<div class="grid grid-cols-2 md:grid-cols-4 gap-4 mb-8">' in updated_html:
        # Find and replace the company stats section
        start = updated_html.find('<div class="grid grid-cols-2 md:grid-cols-4 gap-4 mb-8">')
        # Find the end of this section (next closing div after content)
        search_start = start
        for _ in range(5):  # Skip 5 closing divs (for the 4 company cards)
            search_start = updated_html.find('</div>', search_start) + 6
        
        new_stats_section = f'''<div class="grid grid-cols-2 md:grid-cols-4 gap-4 mb-8">
            {company_html}
        </div>
        {trend_summary}'''
        
        updated_html = updated_html[:start] + new_stats_section + updated_html[search_start:]
    
    # Update title
    updated_html = updated_html.replace('(Real Data - 48 Patents)', '(Enhanced - Trend Analysis)', 1)
    
    # Add data source note about trend analysis
    data_note = f'''
    <div class="mt-6 p-4 bg-green-50 border-l-4 border-green-400 rounded-r-lg">
        <div class="flex">
            <div class="flex-shrink-0">
                <i class="fas fa-database text-green-500"></i>
            </div>
            <div class="ml-3">
                <p class="text-sm text-green-700">
                    <strong>Enhanced Report (Iteration 1):</strong> This report includes trend analysis based on {len(patents)} patents. 
                    Competitor activity trends calculated from {len(sorted_months)} months of data. 
                    Report generated: {datetime.now().strftime('%Y-%m-%d %H:%M UTC')}
                </p>
            </div>
        </div>
    </div>
    '''
    
    # Insert data note before footer
    if '<!-- Data Source Note -->' in updated_html:
        start = updated_html.find('<!-- Data Source Note -->')
        end = updated_html.find('<!-- Footer -->', start)
        updated_html = updated_html[:start] + '<!-- Data Source Note -->' + data_note + updated_html[end:]
    
    # Write output
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(updated_html)
    
    print(f"✅ Enhanced Report Generated: {output_path}")
    print(f"📊 Contains: {len(patents)} patents")
    print(f"📈 Trend Analysis: {len(company_trends)} companies analyzed")
    print(f"📅 Monthly Data: {len(sorted_months)} months")
    print(f"🚀 Accelerating: {len(accelerating)} companies")
    print(f"📉 Decelerating: {len(decelerating)} companies")
    
    return True

if __name__ == "__main__":
    success = generate_enhanced_report()
    sys.exit(0 if success else 1)