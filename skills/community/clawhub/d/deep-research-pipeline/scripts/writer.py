"""Writer Agent — Publication-quality research report generation.

Takes analyst output (themes, contradictions, gaps, merged findings) and
produces polished research reports in multiple formats.

Supports:
- Full markdown report (default)
- Executive summary (concise)
- Bullet-point brief (quick scan)
- JSON structured output

Section structure:
  1. Executive Summary
  2. Key Findings (with confidence indicators)
  3. Detailed Analysis (one section per theme)
  4. Contradictions (where sources disagree)
  5. Knowledge Gaps
  6. Sources
  7. Methodology

Usage:
    # As module
    from writer import WriterAgent
    agent = WriterAgent()
    report = agent.write_report(analyst_output, question="...")

    # As CLI
    python writer.py --input analyst_output.json --question "..." --format report --output report.md
    python writer.py --input analyst_output.json --question "..." --format summary
    python writer.py --input analyst_output.json --question "..." --format brief
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import time
import urllib.request
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Optional

from llm_client import call_llm as _call_glm


class OutputFormat(Enum):
    REPORT = "report"           # Full markdown report
    SUMMARY = "summary"         # Executive summary only
    BRIEF = "brief"             # Bullet-point brief
    JSON = "json"               # Structured JSON output


class ConfidenceLevel(Enum):
    HIGH = "high"               # >= 0.8
    MEDIUM = "medium"           # >= 0.6
    LOW = "low"                 # >= 0.4
    UNCERTAIN = "uncertain"     # < 0.4


def _confidence_level(score: float) -> ConfidenceLevel:
    """Map numeric confidence to a level."""
    try:
        score = float(score)
    except (TypeError, ValueError):
        return ConfidenceLevel.UNCERTAIN
    if score >= 0.8:
        return ConfidenceLevel.HIGH
    if score >= 0.6:
        return ConfidenceLevel.MEDIUM
    if score >= 0.4:
        return ConfidenceLevel.LOW
    return ConfidenceLevel.UNCERTAIN


def _confidence_badge(level: ConfidenceLevel) -> str:
    """Emoji badge for confidence level."""
    badges = {
        ConfidenceLevel.HIGH: "🟢",
        ConfidenceLevel.MEDIUM: "🟡",
        ConfidenceLevel.LOW: "🟠",
        ConfidenceLevel.UNCERTAIN: "🔴",
    }
    return badges.get(level, "⚪")


def _parse_json_response(text: str) -> Any:
    """Parse JSON from LLM, stripping markdown fences."""
    text = text.strip()
    if text.startswith("```"):
        text = text.split("\n", 1)[1].rsplit("```", 1)[0].strip()
    return json.loads(text)


class WriterAgent:
    """Produces publication-quality research reports from analyst output.

    Args:
        use_llm: If True, uses GLM for section generation.
                 If False, uses template-based generation (no API calls).
        api_key: Optional ZAI_API_KEY override.
    """

    MAX_INPUT_CHARS = 15000

    def __init__(self, use_llm: bool = True, api_key: Optional[str] = None):
        self.use_llm = use_llm
        self.api_key = api_key

    def write_report(
        self,
        analyst_output: dict,
        question: str,
        fmt: OutputFormat = OutputFormat.REPORT,
        metadata: Optional[dict] = None,
    ) -> dict:
        """Generate a research report from analyst output.

        Args:
            analyst_output: Dict with themes, contradictions, gaps, merged_findings.
            question: The original research question.
            fmt: Output format (report, summary, brief, json).
            metadata: Optional metadata to include (cycles, sources count, etc.)

        Returns:
            Dict with 'status', 'report' (markdown string), 'question', 'metadata'.
        """
        themes = analyst_output.get("themes", [])
        contradictions = analyst_output.get("contradictions", [])
        gaps = analyst_output.get("gaps", [])
        merged = analyst_output.get("merged_findings", [])

        if fmt == OutputFormat.JSON:
            return self._write_json(analyst_output, question, metadata)
        elif fmt == OutputFormat.SUMMARY:
            report = self._write_summary(analyst_output, question, metadata)
        elif fmt == OutputFormat.BRIEF:
            report = self._write_brief(analyst_output, question, metadata)
        else:
            report = self._write_full_report(analyst_output, question, metadata)

        return {
            "status": "complete",
            "report": report.strip(),
            "question": question,
            "format": fmt.value,
            "metadata": {
                "themes_count": len(themes),
                "contradictions_count": len(contradictions),
                "gaps_count": len(gaps),
                "total_findings": len(merged),
                **(metadata or {}),
                "generated_at": datetime.now(timezone.utc).isoformat(),
            },
        }

    # ─── Full Report ─────────────────────────────────────────────────────

    def _write_full_report(
        self, analyst_output: dict, question: str, metadata: Optional[dict]
    ) -> str:
        """Write a full markdown report with all sections."""
        themes = analyst_output.get("themes", [])
        contradictions = analyst_output.get("contradictions", [])
        gaps = analyst_output.get("gaps", [])
        merged = analyst_output.get("merged_findings", [])

        sections = []

        # ── Title ──
        sections.append(f"# Research Report: {question}\n")
        sections.append(f"*Generated: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}*")

        if metadata:
            cycles = metadata.get("cycles_completed", "")
            coverage = metadata.get("final_coverage", "")
            if cycles:
                sections[0] += f" | Cycles: {cycles}"
            if coverage:
                sections[0] += f" | Coverage: {coverage:.0%}"

        sections.append("")

        # ── Executive Summary ──
        sections.append("## Executive Summary\n")
        summary = self._generate_executive_summary(analyst_output, question)
        sections.append(summary)
        sections.append("")

        # ── Key Findings ──
        if merged:
            sections.append("## Key Findings\n")
            key_findings = self._format_key_findings(merged)
            sections.append(key_findings)
            sections.append("")

        # ── Detailed Analysis ──
        if themes:
            sections.append("## Detailed Analysis\n")
            for theme in themes:
                theme_section = self._generate_theme_section(theme, merged, question)
                sections.append(theme_section)
                sections.append("")
        elif merged:
            # No themes — write findings directly
            sections.append("## Findings\n")
            findings_text = self._format_findings_as_text(merged, question)
            sections.append(findings_text)
            sections.append("")

        # ── Contradictions ──
        if contradictions:
            sections.append("## Contradictions\n")
            sections.append("> ⚠️ The following areas show disagreement between sources.\n")
            for i, c in enumerate(contradictions, 1):
                sections.append(self._format_contradiction(c, i))
            sections.append("")

        # ── Knowledge Gaps ──
        if gaps:
            sections.append("## Knowledge Gaps\n")
            for g in gaps:
                importance = g.get("importance", "medium")
                icon = {"high": "🔴", "medium": "🟡", "low": "🟢"}.get(importance, "⚪")
                q = g.get("question", "?")
                suggested = g.get("suggested_search", "")
                sections.append(f"- {icon} **{q}** ({importance} importance)")
                if suggested:
                    sections.append(f"  - *Suggested search: {suggested}*")
            sections.append("")

        # ── Sources ──
        all_sources = self._collect_sources(merged, analyst_output)
        if all_sources:
            sections.append("## Sources\n")
            for i, src in enumerate(all_sources, 1):
                title = src.get("title", src.get("url", "?"))
                url = src.get("url", "#")
                score = src.get("score", src.get("relevance_score", ""))
                score_str = f" (relevance: {score})" if score else ""
                sections.append(f"{i}. [{title}]({url}){score_str}")
            sections.append("")

        # ── Methodology ──
        sections.append("## Methodology\n")
        sections.append(self._generate_methodology(analyst_output, metadata))

        return "\n".join(sections)

    # ─── Executive Summary ───────────────────────────────────────────────

    def _generate_executive_summary(
        self, analyst_output: dict, question: str
    ) -> str:
        """Generate executive summary (2-3 paragraphs)."""
        themes = analyst_output.get("themes", [])
        merged = analyst_output.get("merged_findings", [])
        contradictions = analyst_output.get("contradictions", [])
        gaps = analyst_output.get("gaps", [])

        if not self.use_llm:
            return self._template_executive_summary(
                question, themes, merged, contradictions, gaps
            )

        system = (
            "You are a research report writer. Write a concise executive summary "
            "(2-3 paragraphs) for this research report.\n\n"
            "Rules:\n"
            "- Start with the most important finding\n"
            "- Mention key themes covered\n"
            "- Note any contradictions or significant gaps\n"
            "- Be precise — no vague language\n"
            "- Output markdown only, no JSON"
        )

        summary_input = json.dumps(
            {
                "question": question,
                "themes": [t.get("name", "") for t in themes],
                "findings_count": len(merged),
                "top_claims": [f.get("claim", "")[:200] for f in merged[:10]],
                "contradictions_count": len(contradictions),
                "gaps": [g.get("question", "") for g in gaps[:5]],
            },
            ensure_ascii=False,
        )

        prompt = (
            f"Research summary data:\n{summary_input}\n\n"
            "Write an executive summary."
        )

        try:
            return _call_glm(prompt, system, max_tokens=800, temperature=0.4, api_key=self.api_key).strip()
        except Exception as e:
            return self._template_executive_summary(
                question, themes, merged, contradictions, gaps
            )

    def _template_executive_summary(
        self, question, themes, merged, contradictions, gaps
    ) -> str:
        """Template-based executive summary (no LLM needed)."""
        lines = []
        lines.append(
            f"This report investigates: **{question}**. "
            f"Research identified {len(merged)} key findings across "
            f"{len(themes)} thematic area{'s' if len(themes) != 1 else ''}."
        )

        if themes:
            theme_names = [t.get("name", "") for t in themes[:5]]
            lines.append(f"Key areas examined: {', '.join(theme_names)}.")

        if contradictions:
            lines.append(
                f"⚠️ {len(contradictions)} "
                f"area{'s' if len(contradictions) != 1 else ''} of disagreement "
                f"between sources were identified."
            )

        if gaps:
            high_gaps = [g for g in gaps if g.get("importance") == "high"]
            if high_gaps:
                lines.append(
                    f"Significant gaps remain in: "
                    f"{', '.join(g.get('question', '?') for g in high_gaps[:3])}."
                )

        return "\n\n".join(lines)

    # ─── Key Findings ────────────────────────────────────────────────────

    def _format_key_findings(self, merged: list[dict]) -> str:
        """Format merged findings as a bulleted list with confidence indicators."""
        lines = []
        for i, f in enumerate(merged[:15], 1):
            claim = f.get("claim", str(f))
            confidence = f.get("confidence", 0.5)
            level = _confidence_level(confidence)
            badge = _confidence_badge(level)

            # Build citation
            sources = f.get("sources", [])
            if not sources:
                url = f.get("source_url", f.get("url", ""))
                if url:
                    sources = [url]

            citation = ""
            if sources:
                source_strs = []
                for s in sources[:2]:
                    if s.startswith("http"):
                        source_strs.append(f"[source]({s})")
                    else:
                        source_strs.append(s)
                citation = f" — {', '.join(source_strs)}"

            lines.append(f"{i}. {badge} {claim}{citation}")

        if len(merged) > 15:
            lines.append(f"\n*...and {len(merged) - 15} additional findings*")

        return "\n".join(lines)

    # ─── Theme Sections ──────────────────────────────────────────────────

    def _generate_theme_section(
        self, theme: dict, merged: list[dict], question: str
    ) -> str:
        """Generate a detailed section for a single theme."""
        theme_name = theme.get("name", "Unknown")
        theme_confidence = theme.get("confidence", 0)

        # Gather findings for this theme
        theme_findings = [
            f for f in merged
            if f.get("theme") == theme_name or f.get("dimension") == theme_name
        ]
        if not theme_findings:
            theme_findings = theme.get("findings", [])

        level = _confidence_level(theme_confidence)
        badge = _confidence_badge(level)
        header = f"### {theme_name} {badge}"

        if not self.use_llm or not theme_findings:
            return self._template_theme_section(
                header, theme_name, theme_findings, theme_confidence
            )

        section_data = json.dumps(
            {
                "theme": theme_name,
                "confidence": theme_confidence,
                "key_claims": theme.get("key_claims", []),
                "findings": theme_findings,
            },
            indent=2,
            ensure_ascii=False,
        )

        # Truncate if too large
        if len(section_data) > self.MAX_INPUT_CHARS:
            truncated = theme_findings[:5]
            section_data = (
                f"[TRUNCATED — showing top 5 of {len(theme_findings)} findings]\n\n"
                + json.dumps(
                    {"theme": theme_name, "findings": truncated},
                    indent=2,
                    ensure_ascii=False,
                )
            )

        system = (
            "You are a research report writer. Write a detailed markdown section "
            "based on the provided research findings.\n\n"
            "Rules:\n"
            "- Every factual claim MUST have an inline citation: [source URL]\n"
            "- Include confidence indicators for key claims\n"
            "- Use sub-headers, bullet points, and clear structure\n"
            "- Never fabricate — only use provided findings\n"
            "- Output markdown only, no JSON wrapping\n"
            "- Start with a brief overview paragraph, then detailed points"
        )

        prompt = (
            f"Research question: {question}\n"
            f"Theme: {theme_name}\n"
            f"Theme confidence: {theme_confidence}\n\n"
            f"Findings:\n{section_data}\n\n"
            f"Write a detailed markdown section for this theme."
        )

        try:
            section_md = _call_glm(
                prompt, system, max_tokens=8000, temperature=0.4, api_key=self.api_key
            )
            return f"{header}\n\n{section_md.strip()}"
        except Exception as e:
            return self._template_theme_section(
                header, theme_name, theme_findings, theme_confidence
            )

    def _template_theme_section(
        self, header: str, theme_name: str, findings: list[dict], confidence: float
    ) -> str:
        """Template-based theme section (no LLM needed)."""
        lines = [header, ""]
        level = _confidence_level(confidence)
        lines.append(f"*Section confidence: {level.value} ({confidence:.0%})*\n")

        for i, f in enumerate(findings[:10], 1):
            claim = f.get("claim", str(f))
            conf = f.get("confidence", 0.5)
            clevel = _confidence_level(conf)
            cbadge = _confidence_badge(clevel)

            sources = f.get("sources", [])
            if not sources:
                url = f.get("source_url", f.get("url", ""))
                if url:
                    sources = [url]

            citation = ""
            if sources:
                source_strs = []
                for s in sources[:2]:
                    if s.startswith("http"):
                        source_strs.append(f"[source]({s})")
                    else:
                        source_strs.append(s)
                citation = f" {cbadge} — {', '.join(source_strs)}"

            lines.append(f"- {claim}{citation}")

        return "\n".join(lines)

    # ─── Contradiction Formatting ────────────────────────────────────────

    def _format_contradiction(self, c: dict, index: int) -> str:
        """Format a single contradiction as a callout box."""
        claim_a = c.get("claim_a", "?")
        claim_b = c.get("claim_b", "?")
        source_a = c.get("source_a", "")
        source_b = c.get("source_b", "?")
        resolution = c.get("resolution", "Unresolved")
        reason = c.get("reason", "")

        lines = [
            f"**Contradiction {index}**",
        ]
        if reason:
            lines.append(f"*{reason}*")
        lines.append("")
        lines.append(f"- **Source A:** {claim_a}")
        if source_a:
            lines.append(f"  ({source_a})")
        lines.append(f"- **Source B:** {claim_b}")
        if source_b:
            lines.append(f"  ({source_b})")
        lines.append(f"- **Resolution:** {resolution}")

        return "\n".join(lines)

    # ─── Source Collection ───────────────────────────────────────────────

    def _collect_sources(
        self, merged: list[dict], analyst_output: dict
    ) -> list[dict]:
        """Collect unique sources from findings."""
        seen_urls = set()
        sources = []

        # From merged findings
        for f in merged:
            urls = f.get("sources", [])
            if not urls:
                url = f.get("source_url", f.get("url", ""))
                if url:
                    urls = [url]

            for url in urls:
                if url and url not in seen_urls and url != "https://example.com/mock":
                    seen_urls.add(url)
                    sources.append({
                        "url": url,
                        "title": f.get("source_title", url),
                        "score": f.get("confidence", ""),
                    })

        # From analyst_output sources
        for s in analyst_output.get("sources", []):
            url = s.get("url", "")
            if url and url not in seen_urls:
                seen_urls.add(url)
                sources.append(s)

        return sources[:50]

    # ─── Methodology ─────────────────────────────────────────────────────

    def _generate_methodology(
        self, analyst_output: dict, metadata: Optional[dict]
    ) -> str:
        """Generate methodology section."""
        lines = []
        lines.append(
            "This report was generated using the Deep Research v2 pipeline, "
            "which follows a multi-stage research architecture:"
        )
        lines.append("")
        lines.append("1. **Planning** — Research question decomposed into dimensions")
        lines.append("2. **Research** — Multi-query search across web, GitHub, and documentation sources")
        lines.append("3. **Analysis** — Deduplication, theme extraction, contradiction detection")
        lines.append("4. **Reflection** — Coverage assessment and gap analysis")
        lines.append("5. **Writing** — Report generation with inline citations and confidence scoring")

        if metadata:
            lines.append("")
            lines.append("**Research parameters:**")
            if "cycles_completed" in metadata:
                lines.append(f"- Research cycles: {metadata['cycles_completed']}")
            if "total_findings" in metadata:
                lines.append(f"- Total findings: {metadata['total_findings']}")
            if "dimensions" in metadata:
                lines.append(f"- Dimensions: {', '.join(metadata['dimensions'])}")

        lines.append("")
        lines.append(
            "All findings are directly sourced and cited. "
            "Confidence scores reflect source quality and corroboration across multiple sources."
        )

        return "\n".join(lines)

    # ─── Summary Format ──────────────────────────────────────────────────

    def _write_summary(
        self, analyst_output: dict, question: str, metadata: Optional[dict]
    ) -> str:
        """Write executive summary format (concise)."""
        themes = analyst_output.get("themes", [])
        merged = analyst_output.get("merged_findings", [])
        contradictions = analyst_output.get("contradictions", [])
        gaps = analyst_output.get("gaps", [])

        lines = [f"# Executive Summary: {question}\n"]

        # Summary paragraph
        summary = self._generate_executive_summary(analyst_output, question)
        lines.append(summary)
        lines.append("")

        # Top 5 findings
        if merged:
            lines.append("## Top Findings\n")
            for i, f in enumerate(merged[:5], 1):
                claim = f.get("claim", str(f))
                conf = f.get("confidence", 0.5)
                level = _confidence_level(conf)
                badge = _confidence_badge(level)
                lines.append(f"{i}. {badge} {claim}")
            lines.append("")

        # Contradictions count
        if contradictions:
            lines.append(f"⚠️ **{len(contradictions)} contradiction(s)** identified between sources.")

        # High-priority gaps
        high_gaps = [g for g in gaps if g.get("importance") == "high"]
        if high_gaps:
            lines.append("")
            lines.append("## Key Gaps\n")
            for g in high_gaps:
                lines.append(f"- {g.get('question', '?')}")

        return "\n".join(lines)

    # ─── Brief Format ────────────────────────────────────────────────────

    def _write_brief(
        self, analyst_output: dict, question: str, metadata: Optional[dict]
    ) -> str:
        """Write bullet-point brief format."""
        themes = analyst_output.get("themes", [])
        merged = analyst_output.get("merged_findings", [])
        contradictions = analyst_output.get("contradictions", [])
        gaps = analyst_output.get("gaps", [])

        lines = [f"📋 **Research Brief:** {question}\n"]

        # One-liner
        lines.append(f"**Findings:** {len(merged)} | **Themes:** {len(themes)} | "
                     f"**Contradictions:** {len(contradictions)} | **Gaps:** {len(gaps)}\n")

        # Bullet findings
        if merged:
            lines.append("**Key Points:**\n")
            for f in merged[:10]:
                claim = f.get("claim", str(f))
                conf = f.get("confidence", 0.5)
                level = _confidence_level(conf)
                badge = _confidence_badge(level)
                lines.append(f"- {badge} {claim}")

        # Contradictions
        if contradictions:
            lines.append("\n**⚠️ Conflicts:**\n")
            for c in contradictions[:3]:
                lines.append(
                    f"- {c.get('claim_a', '?')[:80]} ↔ {c.get('claim_b', '?')[:80]}"
                )

        # Gaps
        if gaps:
            lines.append("\n**Gaps:**\n")
            for g in gaps[:5]:
                importance = g.get("importance", "medium")
                icon = {"high": "🔴", "medium": "🟡", "low": "🟢"}.get(importance, "⚪")
                lines.append(f"- {icon} {g.get('question', '?')}")

        return "\n".join(lines)

    # ─── JSON Output ─────────────────────────────────────────────────────

    def _write_json(
        self, analyst_output: dict, question: str, metadata: Optional[dict]
    ) -> dict:
        """Write structured JSON output."""
        merged = analyst_output.get("merged_findings", [])
        themes = analyst_output.get("themes", [])
        contradictions = analyst_output.get("contradictions", [])
        gaps = analyst_output.get("gaps", [])

        # Annotate findings with confidence levels
        annotated_findings = []
        for f in merged:
            af = dict(f)
            conf = f.get("confidence", 0.5)
            af["confidence_level"] = _confidence_level(conf).value
            af["confidence_badge"] = _confidence_badge(_confidence_level(conf))
            annotated_findings.append(af)

        return {
            "status": "complete",
            "question": question,
            "format": "json",
            "summary": {
                "total_findings": len(merged),
                "themes": len(themes),
                "contradictions": len(contradictions),
                "gaps": len(gaps),
            },
            "themes": themes,
            "findings": annotated_findings,
            "contradictions": contradictions,
            "gaps": gaps,
            "sources": self._collect_sources(merged, analyst_output),
            "metadata": {
                "generated_at": datetime.now(timezone.utc).isoformat(),
                **(metadata or {}),
            },
        }

    # ─── Helper: format findings as plain text (no LLM) ──────────────────

    def _format_findings_as_text(
        self, findings: list[dict], question: str
    ) -> str:
        """Format findings as structured text without LLM."""
        lines = []
        for i, f in enumerate(findings[:15], 1):
            claim = f.get("claim", str(f))
            conf = f.get("confidence", 0.5)
            level = _confidence_level(conf)
            badge = _confidence_badge(level)

            sources = f.get("sources", [])
            if not sources:
                url = f.get("source_url", f.get("url", ""))
                if url:
                    sources = [url]

            citation = ""
            if sources:
                source_strs = []
                for s in sources[:2]:
                    if s.startswith("http"):
                        source_strs.append(f"[source]({s})")
                    else:
                        source_strs.append(s)
                citation = f" — {', '.join(source_strs)}"

            lines.append(f"{i}. {badge} {claim}{citation}")

        if len(findings) > 15:
            lines.append(f"\n*...and {len(findings) - 15} additional findings*")

        return "\n".join(lines)


# ─── Convenience functions ────────────────────────────────────────────────────


def write_report(
    analyst_output: dict,
    question: str,
    fmt: str = "report",
    use_llm: bool = True,
    metadata: Optional[dict] = None,
) -> dict:
    """Convenience function: generate a research report.

    Args:
        analyst_output: Dict from analyst (themes, contradictions, gaps, merged_findings).
        question: The original research question.
        fmt: Output format — "report", "summary", "brief", or "json".
        use_llm: Use GLM for section generation (default True).
        metadata: Optional metadata dict.

    Returns:
        Dict with 'status', 'report', 'question', 'metadata'.
    """
    try:
        output_fmt = OutputFormat(fmt)
    except ValueError:
        output_fmt = OutputFormat.REPORT

    agent = WriterAgent(use_llm=use_llm)
    return agent.write_report(analyst_output, question, output_fmt, metadata)


def save_report(result: dict, output_path: str) -> str:
    """Save report to a file.

    Args:
        result: Output from write_report().
        output_path: File path to save to.

    Returns:
        The output path.
    """
    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)

    if result.get("format") == "json":
        content = json.dumps(result, indent=2, ensure_ascii=False)
    else:
        content = result.get("report", "")

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(content)

    return output_path


# ─── CLI ──────────────────────────────────────────────────────────────────────


def main():
    parser = argparse.ArgumentParser(
        description="Writer Agent — generate research reports"
    )
    parser.add_argument("--input", "-i", required=True, help="Analyst output JSON file (or - for stdin)")
    parser.add_argument("--question", "-q", required=True, help="Research question")
    parser.add_argument(
        "--format", "-f",
        choices=["report", "summary", "brief", "json"],
        default="report",
        help="Output format (default: report)",
    )
    parser.add_argument("--output", "-o", help="Output file path (default: stdout)")
    parser.add_argument("--no-llm", action="store_true", help="Use template mode (no API calls)")
    parser.add_argument("--metadata", help="JSON file with additional metadata")
    args = parser.parse_args()

    # Load analyst output
    if args.input == "-":
        analyst_output = json.load(sys.stdin)
    else:
        with open(args.input, encoding="utf-8") as f:
            analyst_output = json.load(f)

    # Load optional metadata
    metadata = None
    if args.metadata:
        with open(args.metadata, encoding="utf-8") as f:
            metadata = json.load(f)

    # Generate report
    result = write_report(
        analyst_output=analyst_output,
        question=args.question,
        fmt=args.format,
        use_llm=not args.no_llm,
        metadata=metadata,
    )

    # Output
    if args.format == "json":
        output_text = json.dumps(result, indent=2, ensure_ascii=False)
    else:
        output_text = result.get("report", "")

    if args.output:
        save_report(result, args.output)
        print(f"Report saved to {args.output}", file=sys.stderr)
    else:
        print(output_text)


if __name__ == "__main__":
    main()
