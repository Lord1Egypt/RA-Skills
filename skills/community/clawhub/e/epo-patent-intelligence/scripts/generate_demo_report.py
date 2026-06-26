"""
Example: Generate a sample patent report from existing database.

This script demonstrates the report generation workflow.
"""

import sys
from pathlib import Path

# Add parent to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from report_generator import PatentReportGenerator

def generate_demo_report():
    """Generate a demo report using existing patent data."""
    
    # Initialize generator
    generator = PatentReportGenerator()
    
    # Database path
    db_path = Path(__file__).parent.parent / 'data' / 'patents.db'
    
    if not db_path.exists():
        print("❌ No database found. Please run patent collection first:")
        print("   python3 epo_data_mapper.py 'pa=DMG Mori' 1 50")
        return False
    
    # Generate report
    result = generator.create_report(
        db_path=str(db_path),
        client_name='DMG Mori',
        output_html='reports/weekly_report_demo.html',
        output_pdf='reports/weekly_report_demo.pdf',
        days=30  # Look back 30 days
    )
    
    print("\n" + "="*60)
    print("✅ DEMO REPORT GENERATED")
    print("="*60)
    print(f"\n📄 HTML Report: {result['html_path']}")
    print(f"📕 PDF Report:  {result.get('pdf_path', 'Not generated')}")
    print(f"📊 Total Patents: {result['patent_count']}")
    print(f"\n📈 Breakdown:")
    print(f"   Critical: {result['stats']['critical']}")
    print(f"   High:     {result['stats']['high']}")
    print(f"   Medium:   {result['stats']['medium']}")
    print(f"   Low:      {result['stats']['low']}")
    
    if result['stats']['by_company']:
        print(f"\n🏢 Top Competitors:")
        for company, count in list(result['stats']['by_company'].items())[:5]:
            print(f"   {company}: {count} patents")
    
    print("\n" + "="*60)
    print("🌐 Open the HTML file in a browser to view the interactive report")
    print("📧 The PDF can be emailed directly to stakeholders")
    print("="*60)
    
    return True

if __name__ == '__main__':
    generate_demo_report()
