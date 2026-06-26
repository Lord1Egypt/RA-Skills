"""
PDF Reporter - Generates analysis reports in PDF format.

Uses reportlab for direct PDF generation with styled tables and text.
Falls back to HTML-to-PDF conversion if weasyprint/pdfkit/xhtml2pdf is available.
"""

import logging
import os
from typing import Dict, List, Tuple

from src.reporters.base_reporter import BaseReporter

logger = logging.getLogger(__name__)


class PdfReporter(BaseReporter):
    """Generates PDF reports from analysis metrics."""

    def generate(self, metrics: Dict) -> str:
        """
        Generate report content (returns HTML for compatibility).
        Use generate_to_file() for actual PDF output.
        """
        from src.reporters.html_reporter import HtmlReporter
        return HtmlReporter().generate(metrics)

    def generate_to_file(self, metrics: Dict, output_path: str) -> str:
        """
        Generate a PDF report and write it to a file.

        Args:
            metrics: Analysis metrics dict.
            output_path: Path to write the PDF file.

        Returns:
            The output file path.
        """
        # Try HTML-to-PDF engines first for best visual quality
        html_content = self.generate(metrics)
        for method in [
            self._try_weasyprint,
            self._try_pdfkit,
            self._try_xhtml2pdf,
        ]:
            try:
                return method(html_content, output_path)
            except (ImportError, Exception) as e:
                logger.debug("PDF method failed: %s", e)
                continue

        # Fall back to reportlab (always available)
        logger.info("Using reportlab for PDF generation")
        return self._generate_with_reportlab(metrics, output_path)

    # ─── HTML-to-PDF methods ──────────────────────────────────────────────

    @staticmethod
    def _try_weasyprint(html_content: str, output_path: str) -> str:
        from weasyprint import HTML
        HTML(string=html_content).write_pdf(output_path)
        logger.info("PDF generated with weasyprint: %s", output_path)
        return output_path

    @staticmethod
    def _try_pdfkit(html_content: str, output_path: str) -> str:
        import pdfkit
        pdfkit.from_string(html_content, output_path, options={
            "encoding": "UTF-8", "page-size": "A4",
            "margin-top": "15mm", "margin-bottom": "15mm",
        })
        logger.info("PDF generated with pdfkit: %s", output_path)
        return output_path

    @staticmethod
    def _try_xhtml2pdf(html_content: str, output_path: str) -> str:
        from xhtml2pdf import pisa
        with open(output_path, "wb") as f:
            pisa.CreatePDF(html_content, dest=f)
        logger.info("PDF generated with xhtml2pdf: %s", output_path)
        return output_path

    # ─── reportlab PDF generation ─────────────────────────────────────────

    def _generate_with_reportlab(self, metrics: Dict, output_path: str) -> str:
        """Generate PDF using reportlab (always available)."""
        from reportlab.lib.pagesizes import A4
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        from reportlab.lib.units import mm
        from reportlab.lib.colors import HexColor
        from reportlab.platypus import (
            SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
            PageBreak, HRFlowable,
        )
        from reportlab.lib import colors

        doc = SimpleDocTemplate(
            output_path,
            pagesize=A4,
            rightMargin=15 * mm,
            leftMargin=15 * mm,
            topMargin=15 * mm,
            bottomMargin=15 * mm,
        )

        styles = getSampleStyleSheet()

        # Custom styles
        title_style = ParagraphStyle(
            "CustomTitle",
            parent=styles["Title"],
            fontSize=22,
            textColor=HexColor("#4f46e5"),
            spaceAfter=12,
        )
        h2_style = ParagraphStyle(
            "CustomH2",
            parent=styles["Heading2"],
            fontSize=16,
            textColor=HexColor("#4f46e5"),
            spaceBefore=16,
            spaceAfter=8,
        )
        h3_style = ParagraphStyle(
            "CustomH3",
            parent=styles["Heading3"],
            fontSize=13,
            textColor=HexColor("#1e293b"),
            spaceBefore=12,
            spaceAfter=6,
        )
        h4_style = ParagraphStyle(
            "CustomH4",
            parent=styles["Heading4"],
            fontSize=11,
            textColor=HexColor("#64748b"),
            spaceBefore=8,
            spaceAfter=4,
        )
        body_style = styles["Normal"]
        strength_style = ParagraphStyle(
            "Strength", parent=body_style, textColor=HexColor("#166534"),
            fontSize=9, spaceBefore=2,
        )
        weakness_style = ParagraphStyle(
            "Weakness", parent=body_style, textColor=HexColor("#991b1b"),
            fontSize=9, spaceBefore=2,
        )
        suggestion_style = ParagraphStyle(
            "Suggestion", parent=body_style, textColor=HexColor("#1e40af"),
            fontSize=9, spaceBefore=2,
        )
        verdict_style = ParagraphStyle(
            "Verdict", parent=body_style, textColor=HexColor("#64748b"),
            fontSize=10, fontName="Helvetica-Oblique", spaceBefore=4, spaceAfter=8,
            leftIndent=10, borderPadding=5,
        )
        score_style = ParagraphStyle(
            "Score", parent=body_style, fontSize=14, fontName="Helvetica-Bold",
            textColor=HexColor("#4f46e5"),
        )

        elements = []
        elements.append(Paragraph("📊 Code Analysis Report", title_style))
        elements.append(Spacer(1, 6))

        primary_color = HexColor("#4f46e5")
        header_bg = HexColor("#f1f5f9")

        def make_table(headers: List[str], rows: List[List[str]]) -> Table:
            """Build a styled table."""
            data = [headers] + rows
            t = Table(data, repeatRows=1)
            t.setStyle(TableStyle([
                ("BACKGROUND", (0, 0), (-1, 0), primary_color),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("FONTSIZE", (0, 0), (-1, 0), 9),
                ("FONTSIZE", (0, 1), (-1, -1), 8),
                ("ALIGN", (0, 0), (-1, -1), "LEFT"),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("GRID", (0, 0), (-1, -1), 0.5, HexColor("#e2e8f0")),
                ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, header_bg]),
                ("TOPPADDING", (0, 0), (-1, -1), 4),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
            ]))
            return t

        for repo_name, repo_metrics in metrics.items():
            elements.append(Paragraph(f"📁 Repository: {repo_name}", h2_style))

            all_authors = set()
            for key, analyzer_data in repo_metrics.items():
                if isinstance(analyzer_data, dict) and key != "evaluations":
                    all_authors.update(analyzer_data.keys())

            for author in sorted(all_authors):
                elements.append(Paragraph(f"👤 {author}", h3_style))

                # ── Evaluation ──
                ev = repo_metrics.get("evaluations", {}).get(author, {})
                if ev:
                    elements.append(Paragraph("🏆 Developer Evaluation", h4_style))
                    score = ev.get("overall_score", 0)
                    grade = ev.get("grade", "?")
                    elements.append(Paragraph(
                        f"Overall Score: {score}/100 (Grade: {grade})", score_style
                    ))
                    verdict = ev.get("verdict", "")
                    if verdict:
                        elements.append(Paragraph(verdict, verdict_style))

                    # Dimension scores table
                    dim_names = {
                        "commit_discipline": "📝 Commit Discipline",
                        "work_consistency": "⏰ Work Consistency",
                        "efficiency": "🚀 Efficiency",
                        "code_quality": "🔍 Code Quality",
                        "code_style": "🎨 Code Style",
                        "engagement": "💪 Engagement",
                    }
                    dim_rows = []
                    for dim, s in ev.get("dimension_scores", {}).items():
                        name = dim_names.get(dim, dim)
                        bar = "█" * int(s / 10) + "░" * (10 - int(s / 10))
                        dim_rows.append([name, f"{s:.0f}/100", bar])
                    if dim_rows:
                        elements.append(make_table(
                            ["Dimension", "Score", "Bar"], dim_rows
                        ))

                    # Strengths
                    for s in ev.get("strengths", []):
                        elements.append(Paragraph(f"✅ {s}", strength_style))

                    if ev.get("strengths"):
                        elements.append(Spacer(1, 4))

                    # Weaknesses
                    for w in ev.get("weaknesses", []):
                        elements.append(Paragraph(f"❌ {w}", weakness_style))

                    if ev.get("weaknesses"):
                        elements.append(Spacer(1, 4))

                    # Suggestions
                    for sg in ev.get("suggestions", []):
                        elements.append(Paragraph(f"💡 {sg}", suggestion_style))

                    elements.append(Spacer(1, 6))

                # ── Slacking Index ──
                sl = repo_metrics.get("slacking", {}).get(author, {})
                if sl:
                    elements.append(Paragraph("🐟 Slacking Index (摸鱼指数)", h4_style))
                    idx = sl.get("slacking_index", 0)
                    level = sl.get("slacking_level_cn", "")
                    elements.append(Paragraph(
                        f"Index: {idx}/100 — {level}", score_style
                    ))
                    sl_rows = [
                        ["Activity Ratio", f"{sl.get('activity_ratio', 0):.1%}"],
                        ["Trivial Commit Ratio", f"{sl.get('trivial_commit_ratio', 0):.1%}"],
                        ["Large Gap Ratio", f"{sl.get('large_gap_ratio', 0):.1%}"],
                        ["Lines/Active Day", str(sl.get("lines_per_active_day", 0))],
                        ["Non-code Commit Ratio", f"{sl.get('non_code_commit_ratio', 0):.1%}"],
                    ]
                    elements.append(make_table(["Signal", "Value"], sl_rows))

                # ── Commit Patterns ──
                cd = repo_metrics.get("commit_patterns", {}).get(author, {})
                if cd:
                    elements.append(Paragraph("📝 Commit Patterns", h4_style))
                    rows = [
                        ["Total Commits", str(cd.get("total_commits", 0))],
                        ["Merge Ratio", f"{cd.get('merge_ratio', 0):.1%}"],
                        ["Active Span", f"{cd.get('active_span_days', 0)} days"],
                        ["Avg Commits/Day", str(cd.get("avg_commits_per_active_day", 0))],
                        ["Avg Lines Added", str(cd.get("avg_lines_added", 0))],
                        ["Avg Lines Deleted", str(cd.get("avg_lines_deleted", 0))],
                        ["Total Lines Added", f"{cd.get('total_lines_added', 0):,}"],
                        ["Total Lines Deleted", f"{cd.get('total_lines_deleted', 0):,}"],
                    ]
                    elements.append(make_table(["Metric", "Value"], rows))

                # ── Work Habits ──
                hd = repo_metrics.get("work_habits", {}).get(author, {})
                if hd:
                    elements.append(Paragraph("⏰ Work Habits", h4_style))
                    rows = [
                        ["Peak Hour", f"{hd.get('peak_hour', 'N/A')}:00"],
                        ["Weekend Ratio", f"{hd.get('weekend_ratio', 0):.1%}"],
                        ["Late Night Ratio", f"{hd.get('late_night_ratio', 0):.1%}"],
                        ["Longest Streak", f"{hd.get('longest_streak_days', 0)} days"],
                        ["Avg Gap", f"{hd.get('avg_gap_between_commits_hours', 0)} hrs"],
                    ]
                    elements.append(make_table(["Metric", "Value"], rows))

                # ── Efficiency ──
                ed = repo_metrics.get("efficiency", {}).get(author, {})
                if ed:
                    elements.append(Paragraph("🚀 Efficiency", h4_style))
                    rows = [
                        ["Churn Rate", f"{ed.get('churn_rate', 0):.1%}"],
                        ["Rework Ratio", f"{ed.get('rework_ratio', 0):.1%}"],
                        ["Lines/Commit", str(ed.get("lines_per_commit", 0))],
                        ["Files Touched", str(ed.get("unique_files_touched", 0))],
                        ["Ownership Ratio", f"{ed.get('ownership_ratio', 0):.1%}"],
                        ["Bus Factor", str(ed.get("repo_avg_bus_factor", 0))],
                    ]
                    elements.append(make_table(["Metric", "Value"], rows))

                # ── Code Quality ──
                qd = repo_metrics.get("code_quality", {}).get(author, {})
                if qd:
                    elements.append(Paragraph("🔍 Code Quality", h4_style))
                    rows = [
                        ["Bug Fix Ratio", f"{qd.get('bug_fix_ratio', 0):.1%}"],
                        ["Revert Ratio", f"{qd.get('revert_ratio', 0):.1%}"],
                        ["Large Commit Ratio", f"{qd.get('large_commit_ratio', 0):.1%}"],
                        ["Test Modification Ratio", f"{qd.get('test_modification_ratio', 0):.1%}"],
                        ["Avg Commit Size", f"{qd.get('avg_commit_size', 0)} lines"],
                    ]
                    if qd.get("avg_python_complexity", 0) > 0:
                        rows.append(["Avg Python Complexity", str(qd["avg_python_complexity"])])
                    elements.append(make_table(["Metric", "Value"], rows))

                elements.append(HRFlowable(
                    width="100%", thickness=1, color=HexColor("#e2e8f0"),
                    spaceBefore=8, spaceAfter=8,
                ))

            # ── Leaderboard ──
            evals = repo_metrics.get("evaluations", {})
            if evals and len(evals) >= 1:
                elements.append(Paragraph("🏆 Developer Leaderboard", h2_style))
                ranked = sorted(evals.items(), key=lambda x: -x[1].get("overall_score", 0))
                lb_rows = []
                for i, (a, ev) in enumerate(ranked, 1):
                    medal = {1: "🥇", 2: "🥈", 3: "🥉"}.get(i, str(i))
                    lb_rows.append([
                        medal, a,
                        str(ev.get("overall_score", 0)),
                        ev.get("grade", "?"),
                        ev.get("verdict", "")[:60],
                    ])
                elements.append(make_table(
                    ["Rank", "Developer", "Score", "Grade", "Verdict"],
                    lb_rows,
                ))

            # ── Slacking Leaderboard ──
            slacking = repo_metrics.get("slacking", {})
            if slacking and len(slacking) >= 1:
                elements.append(Paragraph("🐟 Slacking Leaderboard (摸鱼排行榜)", h2_style))
                ranked = sorted(slacking.items(), key=lambda x: -x[1].get("slacking_index", 0))
                sl_rows = []
                for i, (a, sd) in enumerate(ranked, 1):
                    sl_rows.append([
                        str(i), a,
                        f"{sd.get('slacking_index', 0)}/100",
                        sd.get("slacking_level_cn", ""),
                        str(sd.get("lines_per_active_day", 0)),
                    ])
                elements.append(make_table(
                    ["Rank", "Developer", "Index", "Level", "Lines/Day"],
                    sl_rows,
                ))

        # Build PDF
        doc.build(elements)
        logger.info("PDF generated with reportlab: %s", output_path)
        return output_path