"""
Patent Report Generator

Generates professional HTML and PDF reports from patent data stored in SQLite.
Uses Jinja2 for templating and Playwright for PDF generation.

Usage:
    generator = PatentReportGenerator()
    generator.create_report(
        db_path='data/patents.db',
        client_name='DMG Mori',
        output_html='reports/weekly_report.html',
        output_pdf='reports/weekly_report.pdf'
    )
"""

from jinja2 import Environment, FileSystemLoader, select_autoescape
from playwright.sync_api import sync_playwright
import sqlite3
import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional


class PatentReportGenerator:
    """Generate professional patent intelligence reports."""
    
    # Threat level color mapping
    THREAT_COLORS = {
        'Critical': '#dc2626',
        'High': '#ea580c',
        'Medium': '#ca8a04',
        'Low': '#16a34a',
        'None': '#6b7280',
        'Unknown': '#6b7280'
    }
    
    def __init__(self, template_dir: str = None):
        """
        Initialize report generator.
        
        Args:
            template_dir: Directory containing Jinja2 templates.
                         Defaults to 'templates' in skill directory.
        """
        if template_dir is None:
            # Default to templates directory in skill
            skill_dir = Path(__file__).parent.parent
            template_dir = skill_dir / 'templates'
        
        self.template_dir = Path(template_dir)
        
        # Setup Jinja2 environment
        self.env = Environment(
            loader=FileSystemLoader(self.template_dir),
            autoescape=select_autoescape(['html', 'xml'])
        )
        
        # Add custom filters
        self.env.filters['tojson'] = lambda x: json.dumps(x)
    
    def generate_html(self, patents: List[Dict], client_name: str, stats: Dict) -> str:
        """
        Generate HTML report from patent data.
        
        Args:
            patents: List of patent dictionaries
            client_name: Name of the client organization
            stats: Statistics dictionary with counts and breakdowns
            
        Returns:
            Rendered HTML string
        """
        template = self.env.get_template('base_report.html')
        
        return template.render(
            client_name=client_name,
            report_date=datetime.now().strftime('%B %d, %Y'),
            patents=patents,
            stats=stats,
            threat_colors=self.THREAT_COLORS
        )
    
    def generate_pdf(self, html_content: str, output_path: str) -> str:
        """
        Convert HTML to PDF using Playwright.
        
        Args:
            html_content: HTML string to convert
            output_path: Path for output PDF file
            
        Returns:
            Path to generated PDF
        """
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        with sync_playwright() as p:
            browser = p.chromium.launch()
            page = browser.new_page()
            
            # Set content and wait for fonts/charts to load
            page.set_content(html_content, wait_until='networkidle')
            
            # Wait a bit for charts to render
            page.wait_for_timeout(2000)
            
            # Generate PDF with professional settings
            page.pdf(
                path=str(output_path),
                format='A4',
                print_background=True,
                margin={
                    'top': '20mm',
                    'right': '20mm',
                    'bottom': '20mm',
                    'left': '20mm'
                },
                display_header_footer=True,
                header_template=f'''
                    <div style="font-size:9px;margin-left:20mm;margin-top:5mm;width:100%;color:#666;">
                        <span style="font-weight:bold;">Patent Intelligence Report</span>
                        <span style="margin-left:10mm;">{datetime.now().strftime('%B %d, %Y')}</span>
                    </div>
                ''',
                footer_template='''
                    <div style="font-size:9px;margin-left:20mm;margin-bottom:5mm;width:100%;color:#666;">
                        <span>Page <span class="pageNumber"></span> of <span class="totalPages"></span></span>
                        <span style="float:right;margin-right:20mm;">Confidential</span>
                    </div>
                '''
            )
            
            browser.close()
        
        return str(output_path)
    
    def create_report(
        self, 
        db_path: str, 
        client_name: str, 
        output_html: str,
        output_pdf: Optional[str] = None,
        days: int = 7
    ) -> Dict:
        """
        Full pipeline: database → HTML → PDF.
        
        Args:
            db_path: Path to SQLite database
            client_name: Client organization name
            output_html: Path for HTML output
            output_pdf: Optional path for PDF output
            days: Number of days to look back for patents
            
        Returns:
            Dictionary with paths and metadata
        """
        # Load patents from database
        patents = self._load_patents(db_path, days)
        
        # Calculate statistics
        stats = self._calculate_stats(patents)
        
        # Generate HTML
        html = self.generate_html(patents, client_name, stats)
        
        # Save HTML
        output_html = Path(output_html)
        output_html.parent.mkdir(parents=True, exist_ok=True)
        with open(output_html, 'w', encoding='utf-8') as f:
            f.write(html)
        
        result = {
            'html_path': str(output_html),
            'patent_count': len(patents),
            'stats': stats,
            'generated_at': datetime.now().isoformat()
        }
        
        # Generate PDF if requested
        if output_pdf:
            pdf_path = self.generate_pdf(html, output_pdf)
            result['pdf_path'] = pdf_path
        
        return result
    
    def _load_patents(self, db_path: str, days: int = 7) -> List[Dict]:
        """
        Load patents from SQLite database.
        
        Args:
            db_path: Path to SQLite database file
            days: Number of days to look back
            
        Returns:
            List of patent dictionaries
        """
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT 
                id,
                patent_id,
                title,
                inventor,
                company,
                filing_date,
                publication_date,
                abstract,
                category as technology_category,
                technology_area,
                secondary_effects,
                image_url,
                epo_link,
                threat_level,
                analysis as strategic_analysis,
                action_recommended,
                affected_business_area
            FROM patents 
            WHERE created_at >= datetime('now', '-{} days')
               OR publication_date >= date('now', '-{} days')
            ORDER BY 
                CASE threat_level
                    WHEN 'Critical' THEN 1
                    WHEN 'High' THEN 2
                    WHEN 'Medium' THEN 3
                    WHEN 'Low' THEN 4
                    ELSE 5
                END,
                publication_date DESC
        '''.format(days, days))
        
        patents = [dict(row) for row in cursor.fetchall()]
        conn.close()
        
        return patents
    
    def _calculate_stats(self, patents: List[Dict]) -> Dict:
        """
        Calculate report statistics from patent data.
        
        Args:
            patents: List of patent dictionaries
            
        Returns:
            Statistics dictionary
        """
        from collections import Counter
        
        # Count by threat level
        threat_counts = Counter(
            p.get('threat_level') or 'Unknown' 
            for p in patents
        )
        
        # Group by company
        company_counts = Counter(
            p.get('company', 'Unknown') 
            for p in patents
        )
        
        # Group by technology
        tech_counts = Counter(
            p.get('technology_category') or 'Unclassified' 
            for p in patents
        )
        
        return {
            'total': len(patents),
            'critical': threat_counts.get('Critical', 0),
            'high': threat_counts.get('High', 0),
            'medium': threat_counts.get('Medium', 0),
            'low': threat_counts.get('Low', 0) + threat_counts.get('None', 0),
            'by_company': dict(company_counts.most_common(10)),
            'by_technology': dict(tech_counts.most_common(10)),
            'threat_distribution': dict(threat_counts)
        }


def main():
    """CLI entry point for testing."""
    import sys
    import argparse
    
    parser = argparse.ArgumentParser(description='Generate patent intelligence reports')
    parser.add_argument('--db', default='data/patents.db', help='Database path')
    parser.add_argument('--client', default='DMG Mori', help='Client name')
    parser.add_argument('--html', default='reports/weekly_report.html', help='HTML output path')
    parser.add_argument('--pdf', default='reports/weekly_report.pdf', help='PDF output path')
    parser.add_argument('--days', type=int, default=7, help='Days to look back')
    parser.add_argument('--no-pdf', action='store_true', help='Skip PDF generation')
    
    args = parser.parse_args()
    
    # Check if database exists
    if not Path(args.db).exists():
        print(f"❌ Database not found: {args.db}")
        sys.exit(1)
    
    # Generate report
    generator = PatentReportGenerator()
    
    print(f"🔄 Generating report for {args.client}...")
    print(f"   Database: {args.db}")
    print(f"   Looking back: {args.days} days")
    
    result = generator.create_report(
        db_path=args.db,
        client_name=args.client,
        output_html=args.html,
        output_pdf=None if args.no_pdf else args.pdf,
        days=args.days
    )
    
    print(f"\n✅ Report generated successfully!")
    print(f"   📄 HTML: {result['html_path']}")
    print(f"   📊 Patents: {result['patent_count']}")
    print(f"   📈 Stats: {result['stats']['critical']} critical, {result['stats']['high']} high, {result['stats']['medium']} medium")
    
    if 'pdf_path' in result:
        print(f"   📕 PDF: {result['pdf_path']}")


if __name__ == '__main__':
    main()
