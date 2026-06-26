#!/usr/bin/env python3
"""
Technology Trend Analysis - Iteration 2
Adds technology-specific trend analysis to patent report
"""

import sys
import os
import sqlite3
import json
from datetime import datetime
from collections import defaultdict

def generate_tech_trend_report():
    """Generate HTML report with technology trend analysis."""
    
    # Paths
    db_path = '/root/.openclaw/workspace/skills/epo-patent-intelligence/data/patents.db'
    template_path = '/root/.openclaw/workspace/skills/epo-patent-intelligence/reports/Patent_report_kw14/index.html'
    output_path = '/root/.openclaw/workspace/skills/epo-patent-intelligence/reports/weekly_report_iteration2.html'
    
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
    
    # Get all patents
    cursor.execute("""
        SELECT patent_id, title, company, publication_date, abstract
        FROM patents 
        ORDER BY publication_date DESC
        LIMIT 20
    """)
    patents = cursor.fetchall()
    
    # Technology keywords
    tech_categories = {
        'CNC': ['cnc', 'computer numerical control', 'machining', 'tool', 'lathe', 'mill', 'milling'],
        'Laser': ['laser', 'lasercutting', 'laser cutting', 'laser machining', 'fiber laser'],
        'Additive': ['additive', '3d printing', 'additive manufacturing', 'powder bed', 'selective laser'],
        'AI': ['ai', 'artificial intelligence', 'machine learning', 'neural network', 'deep learning', 'generative'],
        'Robotics': ['robot', 'robotic', 'automation', 'automated', 'industrial robot'],
        'IoT': ['iot', 'internet of things', 'sensor', 'connected', 'smart factory'],
        'Software': ['software', 'application', 'interface', 'gui', 'user interface', 'algorithm'],
        'Materials': ['material', 'coating', 'surface', 'alloy', 'composite', 'ceramic']
    }
    
    # Analyze technology distribution
    tech_counts = {cat: 0 for cat in tech_categories}
    patent_tech_mapping = {}
    
    for patent_id, title, company, pub_date, abstract in patents:
        text = (title + ' ' + (abstract or '')).lower()
        categories = []
        
        for category, keywords in tech_categories.items():
            for keyword in keywords:
                if keyword in text:
                    categories.append(category)
                    break
        
        for cat in set(categories):
            tech_counts[cat] += 1
        
        patent_tech_mapping[patent_id] = categories
    
    # Analyze technology trends by month
    cursor.execute("""
        SELECT substr(publication_date, 1, 6) as month, title, abstract
        FROM patents 
        WHERE publication_date IS NOT NULL
        ORDER BY month DESC
    """)
    monthly_data = cursor.fetchall()
    
    monthly_tech_trends = defaultdict(lambda: defaultdict(int))
    months = set()
    
    for month, title, abstract in monthly_data:
        if not month:
            continue
        
        text = (title + ' ' + (abstract or '')).lower()
        months.add(month)
        
        for category, keywords in tech_categories.items():
            for keyword in keywords:
                if keyword in text:
                    monthly_tech_trends[month][category] += 1
                    break
    
    # Calculate technology growth trends
    sorted_months = sorted(months, reverse=True)[:6]  # Last 6 months
    tech_growth = {}
    
    if len(sorted_months) >= 6:
        recent_months = sorted_months[:3]
        previous_months = sorted_months[3:6]
        
        for category in tech_categories.keys():
            recent_count = sum(monthly_tech_trends[m].get(category, 0) for m in recent_months)
            previous_count = sum(monthly_tech_trends[m].get(category, 0) for m in previous_months)
            
            if previous_count > 0:
                growth = ((recent_count - previous_count) / previous_count) * 100
                trend = '📈 ACCELERATING' if growth > 20 else '📉 DECELERATING' if growth < -20 else '➡️ STABLE'
                tech_growth[category] = {
                    'recent': recent_count,
                    'previous': previous_count,
                    'growth': growth,
                    'trend': trend
                }
            elif recent_count > 0:
                tech_growth[category] = {
                    'recent': recent_count,
                    'previous': 0,
                    'growth': 100,
                    'trend': '🚀 EMERGING'
                }
    
    conn.close()
    
    # Generate technology insights HTML
    tech_insights_html = ""
    
    # Top technologies section
    top_techs = sorted([(cat, count) for cat, count in tech_counts.items() if count > 0], 
                      key=lambda x: x[1], reverse=True)[:5]
    
    tech_insights_html += f'''
    <div class="mt-8 bg-gradient-to-r from-indigo-50 to-blue-50 rounded-xl p-6">
        <h3 class="text-lg font-bold dmg-blue mb-4">
            <i class="fas fa-microchip mr-2"></i>Technology Focus Analysis
        </h3>
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4 mb-6">
    '''
    
    for category, count in top_techs:
        percentage = (count / len(patents)) * 100
        growth_info = tech_growth.get(category, {'trend': '➡️ STABLE', 'growth': 0})
        
        tech_insights_html += f'''
        <div class="bg-white rounded-lg p-4 shadow-sm border border-gray-200">
            <div class="flex items-center justify-between mb-2">
                <span class="font-bold text-gray-800">{category}</span>
                <span class="text-sm px-2 py-1 rounded-full bg-blue-100 text-blue-800">{count} patents</span>
            </div>
            <div class="text-sm text-gray-600 mb-2">{percentage:.1f}% of analyzed patents</div>
            <div class="text-xs { 'text-green-600' if 'ACCELERATING' in growth_info['trend'] or 'EMERGING' in growth_info['trend'] else 'text-red-600' if 'DECELERATING' in growth_info['trend'] else 'text-gray-600' }">
                {growth_info['trend']}
            </div>
        </div>
        '''
    
    tech_insights_html += '''
        </div>
    '''
    
    # Technology growth trends section
    if tech_growth:
        tech_insights_html += '''
        <div class="mt-6">
            <h4 class="text-md font-semibold text-gray-700 mb-3">
                <i class="fas fa-chart-line mr-2"></i>Technology Growth Trends (Last 3 Months)
            </h4>
            <div class="overflow-x-auto">
                <table class="min-w-full bg-white rounded-lg overflow-hidden">
                    <thead class="bg-gray-100">
                        <tr>
                            <th class="py-2 px-4 text-left text-sm font-medium text-gray-700">Technology</th>
                            <th class="py-2 px-4 text-left text-sm font-medium text-gray-700">Recent (3M)</th>
                            <th class="py-2 px-4 text-left text-sm font-medium text-gray-700">Previous (3M)</th>
                            <th class="py-2 px-4 text-left text-sm font-medium text-gray-700">Growth</th>
                            <th class="py-2 px-4 text-left text-sm font-medium text-gray-700">Trend</th>
                        </tr>
                    </thead>
                    <tbody>
        '''
        
        for category, info in sorted(tech_growth.items(), key=lambda x: abs(x[1]['growth']), reverse=True):
            growth_color = 'text-green-600' if info['growth'] > 0 else 'text-red-600' if info['growth'] < 0 else 'text-gray-600'
            trend_icon = '📈' if info['growth'] > 20 else '📉' if info['growth'] < -20 else '➡️'
            
            tech_insights_html += f'''
                        <tr class="border-t border-gray-200 hover:bg-gray-50">
                            <td class="py-2 px-4 text-sm font-medium text-gray-900">{category}</td>
                            <td class="py-2 px-4 text-sm text-gray-700">{info['recent']}</td>
                            <td class="py-2 px-4 text-sm text-gray-700">{info['previous']}</td>
                            <td class="py-2 px-4 text-sm {growth_color}">{info['growth']:+.1f}%</td>
                            <td class="py-2 px-4 text-sm">{trend_icon} {info['trend'].split()[0]}</td>
                        </tr>
            '''
        
        tech_insights_html += '''
                    </tbody>
                </table>
            </div>
        </div>
    '''
    
    tech_insights_html += '''
        <div class="mt-6 p-4 bg-yellow-50 border-l-4 border-yellow-400 rounded-r-lg">
            <div class="flex">
                <div class="flex-shrink-0">
                    <i class="fas fa-lightbulb text-yellow-500"></i>
                </div>
                <div class="ml-3">
                    <p class="text-sm text-yellow-700">
                        <strong>Strategic Insight:</strong> Technology trend analysis reveals where competitors are investing R&D resources. 
                        "Accelerating" technologies indicate strategic focus areas, while "Decelerating" may signal technology maturity or shifting priorities.
                    </p>
                </div>
            </div>
        </div>
    </div>
    '''
    
    # Update template with technology insights
    updated_html = template
    
    # Insert technology insights after company statistics
    if '<!-- Technology Insights -->' in updated_html:
        # Replace placeholder with actual insights
        updated_html = updated_html.replace('<!-- Technology Insights -->', tech_insights_html)
    else:
        # Find a good place to insert (after company stats section)
        insert_point = updated_html.find('<div class="grid grid-cols-2 md:grid-cols-4 gap-4 mb-8">')
        if insert_point != -1:
            # Find end of company stats section
            end_point = updated_html.find('</div>', insert_point)
            for _ in range(5):  # Skip nested divs
                end_point = updated_html.find('</div>', end_point + 1)
            
            updated_html = updated_html[:end_point] + tech_insights_html + updated_html[end_point:]
    
    # Update title
    updated_html = updated_html.replace('(Enhanced - Trend Analysis)', '(Technology Trends)', 1)
    
    # Add iteration note
    iteration_note = f'''
    <div class="mt-6 p-4 bg-blue-50 border-l-4 border-blue-400 rounded-r-lg">
        <div class="flex">
            <div class="flex-shrink-0">
                <i class="fas fa-flask text-blue-500"></i>
            </div>
            <div class="ml-3">
                <p class="text-sm text-blue-700">
                    <strong>Iteration 2 - Technology Trend Analysis:</strong> This report includes technology-specific trend analysis based on {len(patents)} patents. 
                    Identified {len([c for c in tech_counts.values() if c > 0])} technology categories with growth trends. 
                    Report generated: {datetime.now().strftime('%Y-%m-%d %H:%M UTC')}
                </p>
            </div>
        </div>
    </div>
    '''
    
    # Insert iteration note before footer
    if '<!-- Iteration Note -->' in updated_html:
        updated_html = updated_html.replace('<!-- Iteration Note -->', iteration_note)
    
    # Write output
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(updated_html)
    
    print(f"✅ Technology Trend Report Generated: {output_path}")
    print(f"📊 Contains: {len(patents)} patents")
    print(f"🔬 Technology Categories: {len([c for c in tech_counts.values() if c > 0])} identified")
    print(f"📈 Top Technologies: {', '.join([cat for cat, _ in top_techs])}")
    
    return True

if __name__ == "__main__":
    success = generate_tech_trend_report()
    sys.exit(0 if success else 1)