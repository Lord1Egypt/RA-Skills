"""PDF Report Generator for CANSLIM Analysis.

This module generates professional PDF reports from the final CANSLIM analysis JSON data.
"""

import json
import logging
import os
from datetime import datetime
from typing import Any, Dict, List

from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    PageBreak,
    Image,
)
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("canslim_analysis.log"),
        logging.StreamHandler(),
    ],
)
logger = logging.getLogger(__name__)


class CANSLIMReportGenerator:
    """Generates PDF reports for CANSLIM stock analysis."""

    def __init__(self, output_dir: str):
        """Initialize the report generator.

        Args:
            output_dir: Directory to save PDF reports.
        """
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
        
        # Setup styles
        self.styles = getSampleStyleSheet()
        self._setup_custom_styles()

    def _setup_custom_styles(self) -> None:
        """Setup custom paragraph styles for the report."""
        self.styles.add(ParagraphStyle(
            name='ReportTitle',
            parent=self.styles['Heading1'],
            fontSize=24,
            spaceAfter=30,
            alignment=TA_CENTER,
            textColor=colors.HexColor('#1a365d'),
        ))
        
        self.styles.add(ParagraphStyle(
            name='SectionHeader',
            parent=self.styles['Heading2'],
            fontSize=16,
            spaceBefore=20,
            spaceAfter=10,
            textColor=colors.HexColor('#2c5282'),
        ))
        
        self.styles.add(ParagraphStyle(
            name='SubSection',
            parent=self.styles['Heading3'],
            fontSize=12,
            spaceBefore=10,
            spaceAfter=5,
            textColor=colors.HexColor('#2d3748'),
        ))
        
        self.styles.add(ParagraphStyle(
            name='ReportBody',
            parent=self.styles['Normal'],
            fontSize=10,
            spaceBefore=5,
            spaceAfter=5,
        ))
        
        self.styles.add(ParagraphStyle(
            name='GradeAPlus',
            parent=self.styles['Normal'],
            fontSize=14,
            textColor=colors.HexColor('#276749'),
            alignment=TA_CENTER,
        ))
        
        self.styles.add(ParagraphStyle(
            name='GradeA',
            parent=self.styles['Normal'],
            fontSize=14,
            textColor=colors.HexColor('#2f855a'),
            alignment=TA_CENTER,
        ))
        
        self.styles.add(ParagraphStyle(
            name='GradeB',
            parent=self.styles['Normal'],
            fontSize=14,
            textColor=colors.HexColor('#b7791f'),
            alignment=TA_CENTER,
        ))
        
        self.styles.add(ParagraphStyle(
            name='GradeC',
            parent=self.styles['Normal'],
            fontSize=14,
            textColor=colors.HexColor('#c53030'),
            alignment=TA_CENTER,
        ))

    def _get_grade_style(self, grade: str) -> ParagraphStyle:
        """Get the appropriate style for a grade.

        Args:
            grade: The grade string (A+, A, A-, B+, B, C, D).

        Returns:
            ParagraphStyle for the grade.
        """
        if grade in ('A+', 'A'):
            return self.styles['GradeAPlus']
        elif grade in ('A-', 'B+'):
            return self.styles['GradeA']
        elif grade == 'B':
            return self.styles['GradeB']
        else:
            return self.styles['GradeC']

    def _format_percentage(self, value: Any) -> str:
        """Format a value as percentage.

        Args:
            value: Numeric value to format.

        Returns:
            Formatted percentage string.
        """
        if value is None:
            return "N/A"
        try:
            return f"{float(value) * 100:.1f}%"
        except (TypeError, ValueError):
            return "N/A"

    def _format_number(self, value: Any, decimals: int = 2) -> str:
        """Format a numeric value.

        Args:
            value: Numeric value to format.
            decimals: Number of decimal places.

        Returns:
            Formatted number string.
        """
        if value is None:
            return "N/A"
        try:
            return f"{float(value):,.{decimals}f}"
        except (TypeError, ValueError):
            return "N/A"

    def _format_large_number(self, value: Any) -> str:
        """Format large numbers with M/B suffixes.

        Args:
            value: Numeric value to format.

        Returns:
            Formatted number string with suffix.
        """
        if value is None:
            return "N/A"
        try:
            num = float(value)
            if num >= 1_000_000_000:
                return f"{num / 1_000_000_000:.1f}B"
            elif num >= 1_000_000:
                return f"{num / 1_000_000:.1f}M"
            elif num >= 1_000:
                return f"{num / 1_000:.1f}K"
            else:
                return f"{num:.0f}"
        except (TypeError, ValueError):
            return "N/A"

    def _create_header_section(self, data: Dict[str, Any]) -> List:
        """Create the report header section.

        Args:
            data: The report data dictionary.

        Returns:
            List of reportlab flowables.
        """
        elements = []
        
        # Title
        elements.append(Paragraph("CANSLIM Stock Analysis Report", self.styles['ReportTitle']))
        elements.append(Spacer(1, 20))
        
        # Report metadata table
        meta_data = [
            ["Report Date", data.get("Report_Date", "N/A")],
            ["Report Time", data.get("Report_Time", "N/A")],
            ["Schema Version", data.get("Schema_Version", "N/A")],
            ["Market Environment", data.get("Market_Environment", "Unknown")],
            ["M Criterion Met", "Yes" if data.get("M_Criterion_Met", False) else "No"],
            ["Total Candidates", str(data.get("Total_Candidates_Evaluated", 0))],
        ]
        
        meta_table = Table(meta_data, colWidths=[2*inch, 3*inch])
        meta_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#e2e8f0')),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.HexColor('#2d3748')),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#cbd5e0')),
        ]))
        
        elements.append(meta_table)
        elements.append(Spacer(1, 20))
        
        # Score distribution
        score_dist = data.get("Score_Distribution", {})
        if score_dist:
            elements.append(Paragraph("Score Distribution", self.styles['SectionHeader']))
            
            dist_data = [["Score", "Count"]]
            for score, count in sorted(score_dist.items(), key=lambda x: int(x[0]), reverse=True):
                dist_data.append([score, str(count)])
            
            dist_table = Table(dist_data, colWidths=[1.5*inch, 1.5*inch])
            dist_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2c5282')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, -1), 10),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
                ('TOPPADDING', (0, 0), (-1, -1), 8),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#cbd5e0')),
                ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f7fafc')]),
            ]))
            
            elements.append(dist_table)
            elements.append(Spacer(1, 20))
        
        return elements

    def _create_stock_section(self, stock: Dict[str, Any], index: int) -> List:
        """Create a section for a single stock.

        Args:
            stock: Stock data dictionary.
            index: Stock index number.

        Returns:
            List of reportlab flowables.
        """
        elements = []
        
        # Stock header with ticker and company name
        ticker = stock.get("Ticker", "N/A")
        company_name = stock.get("Company_Name", "N/A")
        grade = stock.get("Grade", "N/A")
        score = stock.get("Final_Score", 0)
        
        elements.append(Paragraph(
            f"#{index}: {ticker} - {company_name}",
            self.styles['SectionHeader']
        ))
        
        # Grade and score display
        grade_style = self._get_grade_style(grade)
        elements.append(Paragraph(
            f"Grade: {grade} (Score: {score}/7)",
            grade_style
        ))
        elements.append(Spacer(1, 10))
        
        # Criteria met/missed
        met_criteria = stock.get("Met_Criteria", [])
        missed_criteria = stock.get("Missed_Criteria", [])
        
        criteria_data = [
            ["CANSLIM Criteria", "Status"],
        ]
        
        for letter in ["C", "A", "N", "S", "L", "I", "M"]:
            status = "✓ Met" if letter in met_criteria else "✗ Missed"
            criteria_data.append([letter, status])
        
        criteria_table = Table(criteria_data, colWidths=[1.5*inch, 1.5*inch])
        criteria_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2c5282')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
            ('TOPPADDING', (0, 0), (-1, -1), 6),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#cbd5e0')),
        ]))
        
        # Color code the status cells
        for i, letter in enumerate(["C", "A", "N", "S", "L", "I", "M"], start=1):
            if letter in met_criteria:
                criteria_table.setStyle(TableStyle([
                    ('BACKGROUND', (1, i), (1, i), colors.HexColor('#c6f6d5')),
                    ('TEXTCOLOR', (1, i), (1, i), colors.HexColor('#276749')),
                ]))
            else:
                criteria_table.setStyle(TableStyle([
                    ('BACKGROUND', (1, i), (1, i), colors.HexColor('#fed7d7')),
                    ('TEXTCOLOR', (1, i), (1, i), colors.HexColor('#c53030')),
                ]))
        
        elements.append(criteria_table)
        elements.append(Spacer(1, 10))
        
        # Key metrics table
        metrics = stock.get("Metrics", {})
        
        metrics_data = [
            ["Metric", "Value"],
            ["RS Rating", self._format_number(metrics.get("RS_Rating"), 1)],
            ["Current Price", f"${self._format_number(metrics.get('Current_Price'), 2)}"],
            ["Quarterly EPS Growth", self._format_percentage(metrics.get("Quarterly_EPS_Growth"))],
            ["Annual EPS Growth", self._format_percentage(metrics.get("Annual_EPS_Growth"))],
            ["EPS Accelerating", "Yes" if metrics.get("EPS_Accelerating") else "No"],
            ["S Score", str(metrics.get("S_Score", 0))],
            ["Float Shares", self._format_large_number(metrics.get("Float_Shares"))],
            ["Institutional Ownership", self._format_percentage(metrics.get("Institutional_Ownership"))],
        ]
        
        metrics_table = Table(metrics_data, colWidths=[2.5*inch, 2*inch])
        metrics_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#4a5568')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('ALIGN', (1, 0), (1, -1), 'RIGHT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
            ('TOPPADDING', (0, 0), (-1, -1), 6),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#cbd5e0')),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f7fafc')]),
        ]))
        
        elements.append(Paragraph("Key Metrics", self.styles['SubSection']))
        elements.append(metrics_table)
        elements.append(Spacer(1, 10))
        
        # Details section
        details = stock.get("Details", {})
        
        # C & A Details
        elements.append(Paragraph("Earnings Analysis (C & A)", self.styles['SubSection']))
        elements.append(Paragraph(
            f"<b>Current Earnings (C):</b> {details.get('C_Details', 'N/A')}",
            self.styles['ReportBody']
        ))
        elements.append(Paragraph(
            f"<b>Annual Earnings (A):</b> {details.get('A_Details', 'N/A')}",
            self.styles['ReportBody']
        ))
        elements.append(Spacer(1, 5))
        
        # N Details
        elements.append(Paragraph("New Highs & Catalyst (N)", self.styles['SubSection']))
        elements.append(Paragraph(
            f"<b>Technical:</b> {details.get('N_Technical_Details', 'N/A')}",
            self.styles['ReportBody']
        ))
        elements.append(Paragraph(
            f"<b>Catalyst:</b> {details.get('N_Catalyst_Details', 'N/A')}",
            self.styles['ReportBody']
        ))
        elements.append(Spacer(1, 5))
        
        # S Details
        elements.append(Paragraph("Supply & Demand (S)", self.styles['SubSection']))
        elements.append(Paragraph(
            f"<b>Quantitative:</b> {details.get('S_Quant_Details', 'N/A')}",
            self.styles['ReportBody']
        ))
        elements.append(Paragraph(
            f"<b>Float Analysis:</b> {details.get('S_Float_Details', 'N/A')}",
            self.styles['ReportBody']
        ))
        elements.append(Spacer(1, 5))
        
        # I Details
        elements.append(Paragraph("Institutional Sponsorship (I)", self.styles['SubSection']))
        elements.append(Paragraph(
            f"<b>Quantitative:</b> {details.get('I_Quant_Details', 'N/A')}",
            self.styles['ReportBody']
        ))
        elements.append(Paragraph(
            f"<b>Quality Assessment:</b> {details.get('I_Institutional_Details', 'N/A')}",
            self.styles['ReportBody']
        ))
        elements.append(Spacer(1, 5))
        
        # AI Catalyst Note
        ai_note = stock.get("AI_Catalyst_Note", "")
        if ai_note:
            elements.append(Paragraph("AI Catalyst Analysis", self.styles['SubSection']))
            elements.append(Paragraph(ai_note, self.styles['ReportBody']))
        
        # Page break after each stock (except the last one)
        elements.append(Spacer(1, 20))
        
        return elements

    def generate_report(self, json_path: str) -> str:
        """Generate a PDF report from JSON data.

        Args:
            json_path: Path to the JSON report file.

        Returns:
            Path to the generated PDF file.
        """
        logger.info("Loading JSON data from %s", json_path)
        
        with open(json_path, "r", encoding="utf-8") as handle:
            data = json.load(handle)
        
        # Generate output filename
        report_date = data.get("Report_Date", datetime.now().strftime("%Y-%m-%d"))
        pdf_filename = f"canslim_report_{report_date}.pdf"
        pdf_path = os.path.join(self.output_dir, pdf_filename)
        
        logger.info("Generating PDF report: %s", pdf_path)
        
        # Create the PDF document
        doc = SimpleDocTemplate(
            pdf_path,
            pagesize=letter,
            rightMargin=0.75*inch,
            leftMargin=0.75*inch,
            topMargin=0.75*inch,
            bottomMargin=0.75*inch,
        )
        
        # Build the document content
        elements = []
        
        # Add header section
        elements.extend(self._create_header_section(data))
        
        # Add page break before stocks
        elements.append(PageBreak())
        
        # Add each stock
        stocks = data.get("Top_Candidates", [])
        for index, stock in enumerate(stocks, start=1):
            elements.extend(self._create_stock_section(stock, index))
            # Add page break after each stock except the last
            if index < len(stocks):
                elements.append(PageBreak())
        
        # Build the PDF
        doc.build(elements)
        
        logger.info("PDF report generated successfully: %s", pdf_path)
        return pdf_path


def main() -> None:
    """Main entry point for PDF report generation."""
    logger.info("--- Starting CANSLIM PDF Report Generation ---")
    
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    output_dir = os.path.join(project_root, "out")
    
    # Find the JSON report
    json_path = os.path.join(script_dir, "final_canslim_report.json")
    
    if not os.path.exists(json_path):
        logger.error("JSON report not found: %s", json_path)
        logger.error("Please run final_process.py first to generate the JSON report.")
        return
    
    # Generate the PDF report
    generator = CANSLIMReportGenerator(output_dir)
    pdf_path = generator.generate_report(json_path)
    
    logger.info("PDF report saved to: %s", pdf_path)


if __name__ == "__main__":
    main()