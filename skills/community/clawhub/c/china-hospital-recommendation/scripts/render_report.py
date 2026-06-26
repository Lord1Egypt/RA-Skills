#!/usr/bin/env python3
"""Render premium hospital recommendation reports as Markdown and PDF."""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import tempfile
from html import escape as html_escape
from pathlib import Path

try:
    from reportlab.lib import colors
    from reportlab.lib.enums import TA_LEFT
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
    from reportlab.lib.units import mm
    from reportlab.pdfbase.cidfonts import UnicodeCIDFont
    from reportlab.pdfbase.pdfmetrics import registerFont
    from reportlab.platypus import (
        HRFlowable,
        PageBreak,
        Paragraph,
        SimpleDocTemplate,
        Spacer,
        Table,
        TableStyle,
    )

    REPORTLAB_AVAILABLE = True
except ImportError:
    REPORTLAB_AVAILABLE = False


LOCALES = {
    "en": {
        "title": "Personalized Hospital Recommendation Report",
        "subtitle": "Premium medical travel planning brief",
        "top_takeaway_section": "Top Takeaway",
        "patient_snapshot": "Your Situation at a Glance",
        "recommendation_logic": "Why These Hospitals Were Chosen",
        "quick_comparison": "Quick Comparison",
        "recommended_hospitals": "Recommended Hospitals",
        "specialist_directions": "Recommended Specialist Directions",
        "estimated_costs": "Expected Costs",
        "travel_logistics": "Travel and Visa Planning",
        "next_steps": "What You Should Do Next",
        "evidence_notes": "Evidence Notes",
        "important_disclaimer": "Important Disclaimer",
        "current_limitations_section": "What Could Change the Recommendation",
        "report_id": "Report ID",
        "created_at": "Created At",
        "patient_name": "Patient Name",
        "country": "Country",
        "condition_summary": "Condition Summary",
        "preferred_city": "Preferred City",
        "travel_time": "Travel Time",
        "budget_range": "Budget Range",
        "clinical_focus": "Clinical Focus",
        "recommendation_rule": "Selection Logic",
        "recommended_length_of_stay": "Recommended Length of Stay",
        "top_takeaway": "Top Takeaway",
        "uncertainty_note": "How Missing Details Could Change the Recommendation",
        "fit_summary": "Why This May Fit You in One Line",
        "chinese_name": "Chinese Name",
        "city": "City",
        "department": "Recommended Department",
        "international_services": "International Services",
        "international_access": "International Access",
        "admin_intake_status": "Administrative Intake",
        "record_review_status": "Record Review Before Travel",
        "doctor_teleconsult_status": "Doctor-Led Remote Consultation",
        "access_evidence_level": "Access Evidence Level",
        "remote_consultation_note": "Remote Consultation Note",
        "estimated_cost": "Estimated Cost",
        "contact": "Contact Channel",
        "why_recommended": "Why This May Fit You",
        "best_for": "Best For",
        "potential_limitation": "Potential Limitation",
        "current_checks": "Before You Book",
        "jci_status": "JCI Status",
        "jci_last_verified": "JCI Last Checked",
        "jci_note": "JCI Note",
        "comparison_hospital": "Hospital",
        "comparison_support": "International Access Evidence",
        "comparison_budget": "Cost Positioning",
        "specialist_focus": "Focus",
        "specialist_hospital": "Hospital",
        "specialist_summary": "Recommendation",
        "specialist_evidence": "Evidence Level",
        "specialist_intent_gate": "When To Use This Route",
        "scenario": "Scenario",
        "planning_estimate": "Planning Estimate",
        "uncertainty": "Uncertainty",
        "high_uncertainty_heading": "High-Uncertainty Planning Estimate",
        "consultation_range": "Consultation and Workup",
        "surgery_range": "Surgery-Centered Treatment",
        "treatment_range": "Treatment Range",
        "non_medical_range": "Travel and Stay Range",
        "notes": "Notes",
        "visa": "Visa",
        "accommodation": "Accommodation",
        "transportation": "Transportation",
        "not_provided": "Not provided",
        "confidentiality": "Prepared for your hospital selection planning.",
    }
}

FONT_CANDIDATES = [
    "PingFang SC",
    "Songti SC",
    "Hiragino Sans GB",
    "Arial Unicode MS",
    "STHeiti",
    "Noto Sans CJK SC",
]
_WORKING_FONT: str | None = None
_REPORTLAB_FONT_READY = False
REPORTLAB_CJK_FONT = "STSong-Light"
CONSULT_SERVICE_SENTENCE = (
    "If you need consult service, please contact ChinaMed Select "
    "(https://www.chinamed.cc, info@chinamed.cc)."
)
BRAND_COLORS = {
    "primary": "#3B82F6",
    "primary_dark": "#1E40AF",
    "primary_light": "#DBEAFE",
    "success": "#10B981",
    "warning": "#F59E0B",
    "text": "#1F2937",
    "text_secondary": "#4B5563",
    "text_muted": "#6B7280",
    "border": "#D1D5DB",
    "surface": "#F3F4F6",
    "white": "#FFFFFF",
}


def resolve_language(payload: dict) -> str:
    return (payload.get("output_language") or payload.get("language") or "en").lower()


def locale_for(payload: dict) -> dict[str, str]:
    return LOCALES.get(resolve_language(payload), LOCALES["en"])


def normalize_list(value: object) -> list[str]:
    if value is None:
        return []
    if isinstance(value, list):
        return [str(item).strip() for item in value if str(item).strip()]
    text = str(value).strip()
    return [text] if text else []


def markdown_escape(value: object) -> str:
    text = str(value).strip()
    return text.replace("\n", "<br>")


def normalize_text(value: object) -> str:
    return str(value).strip() if value is not None else ""


def first_non_empty(*values: object) -> str:
    for value in values:
        text = normalize_text(value)
        if text:
            return text
    return ""


def pdf_escape(value: object) -> str:
    text = html_escape(normalize_text(value))
    return text.replace("\n", "<br/>")


def bullet_list(items: list[str]) -> str:
    return "\n".join(f"- {item}" for item in items if item)


def numbered_list(items: list[str], fallback: str) -> str:
    rows = [f"{index}. {item}" for index, item in enumerate(items, start=1) if item]
    if not rows:
        rows = [f"1. {fallback}"]
    return "\n".join(rows)


def brand_color(name: str):
    return colors.HexColor(BRAND_COLORS[name])


def final_disclaimer_text(payload: dict) -> str:
    base = normalize_text(
        payload.get(
            "disclaimer",
            "This report is for informational purposes only and does not replace medical advice.",
        )
    )
    if CONSULT_SERVICE_SENTENCE in base:
        return base
    separator = " " if base else ""
    return f"{base}{separator}{CONSULT_SERVICE_SENTENCE}".strip()


def build_front_matter(payload: dict, labels: dict[str, str]) -> str:
    report_id = payload.get("report_id", labels["not_provided"])
    created_at = payload.get("created_at", labels["not_provided"])
    return "\n".join(
        [
            "---",
            f'title: "{labels["title"]}"',
            f'subtitle: "{labels["subtitle"]}"',
            f'date: "{created_at}"',
            f'author: "{report_id}"',
            "toc: true",
            "toc-depth: 2",
            "fontsize: 11pt",
            "---",
            "",
        ]
    )


def build_metadata_block(payload: dict, labels: dict[str, str]) -> str:
    patient = payload.get("patient", {})
    return "\n".join(
        [
            f"# {labels['title']}",
            "",
            f"> {labels['confidentiality']}",
            "",
            f"- **{labels['report_id']}:** {markdown_escape(payload.get('report_id', labels['not_provided']))}",
            f"- **{labels['created_at']}:** {markdown_escape(payload.get('created_at', labels['not_provided']))}",
            f"- **Patient:** {markdown_escape(patient.get('name', labels['not_provided']))}",
            f"- **{labels['country']}:** {markdown_escape(patient.get('country', labels['not_provided']))}",
            "",
        ]
    )


def build_patient_snapshot(payload: dict, labels: dict[str, str]) -> str:
    patient = payload.get("patient", {})
    return "\n".join(
        [
            f"- **{labels['condition_summary']}:** {patient.get('condition_summary', labels['not_provided'])}",
            f"- **{labels['preferred_city']}:** {patient.get('preferred_city', labels['not_provided'])}",
            f"- **{labels['travel_time']}:** {patient.get('travel_time', labels['not_provided'])}",
            f"- **{labels['budget_range']}:** {patient.get('budget_range', labels['not_provided'])}",
        ]
    )


def sentence_case(text: str) -> str:
    cleaned = text.strip().rstrip(".")
    if not cleaned:
        return cleaned
    return cleaned[0].lower() + cleaned[1:]


def format_title_case(value: str) -> str:
    return value.replace("_", " ").replace("-", " ").title()


def has_verified_doctor_teleconsult(hospital: dict) -> bool:
    access = hospital.get("international_access") or {}
    status = first_non_empty(
        access.get("doctor_teleconsult_status"),
        hospital.get("doctor_teleconsult_status"),
    ).lower()
    return status == "verified"


def payload_has_verified_doctor_teleconsult(payload: dict) -> bool:
    return any(has_verified_doctor_teleconsult(hospital) for hospital in payload.get("hospitals", []))


def sanitize_remote_claims(text: object, payload: dict) -> str:
    normalized = normalize_text(text)
    if not normalized:
        return ""
    if payload_has_verified_doctor_teleconsult(payload):
        return normalized

    replacements = {
        "may support remote consultation": "remote consultation still needs direct confirmation",
        "supports remote consultation": "remote consultation still needs direct confirmation",
        "remote consultation is available": "remote consultation still needs direct confirmation",
        "remote consultation may be available": "remote consultation still needs direct confirmation",
    }
    lowered = normalized.lower()
    for target, replacement in replacements.items():
        if target in lowered:
            start = lowered.index(target)
            end = start + len(target)
            normalized = normalized[:start] + replacement + normalized[end:]
            lowered = normalized.lower()
    return normalized


def build_current_limitations(summary: dict, labels: dict[str, str]) -> str:
    items = normalize_list(summary.get("current_limitations"))
    if not items:
        return f"- {labels['not_provided']}"
    return bullet_list(items)


def access_status_value(hospital: dict, key: str, default: str) -> str:
    access = hospital.get("international_access") or {}
    return first_non_empty(access.get(key), hospital.get(key), default)


def derive_access_evidence_level(hospital: dict, labels: dict[str, str]) -> str:
    explicit = first_non_empty(
        hospital.get("access_evidence_level"),
        hospital.get("international_access_evidence"),
        hospital.get("international_support"),
        hospital.get("support_level"),
    )
    if explicit:
        return explicit
    return "Needs manual confirmation"


def comparison_cost_position(item: dict, labels: dict[str, str]) -> str:
    explicit = first_non_empty(item.get("cost_positioning"), item.get("budget_level"))
    if explicit:
        return explicit
    return labels["high_uncertainty_heading"]


def derive_hospital_cost_summary(hospital: dict, labels: dict[str, str]) -> str:
    scenarios = hospital.get("cost_scenarios") or {}
    if scenarios:
        return labels["high_uncertainty_heading"]
    return first_non_empty(hospital.get("estimated_cost"), labels["high_uncertainty_heading"])


def derive_best_for_from_reason(reason: str) -> str:
    text = normalize_text(reason)
    lowered = text.lower()
    direct_patterns = [
        ("strong option when the patient wants ", "You want "),
        ("strong option when the patient needs ", "You need "),
        ("strong fit if the patient may need ", "You may need "),
        ("strong fit if the patient needs ", "You need "),
        ("valuable when the patient needs ", "You need "),
        ("useful as an alternative pathway if ", "You want an alternative pathway if "),
        ("can work well for patients who value ", "You value "),
    ]
    for marker, prefix in direct_patterns:
        if marker in lowered:
            tail = text[lowered.index(marker) + len(marker) :].strip().rstrip(".")
            if tail:
                return f"{prefix}{tail}."

    if "improves practical readiness for a patient traveling from" in lowered:
        return "You want clearer international-patient communication and intake support before you travel."
    if "making it the strongest baseline choice for a breast-cancer case that may require" in lowered:
        marker = "making it the strongest baseline choice for a breast-cancer case that may require"
        tail = text[lowered.index(marker) + len(marker) :]
        tail = tail.strip().rstrip(".")
        if tail:
            return f"You may need {sentence_case(tail)}."
    if "high-authority first opinion" in lowered:
        return "You want a high-authority first opinion, pathology review, and multidisciplinary planning before treatment decisions."
    if "detailed breast-surgery planning" in lowered:
        return "You may need detailed breast-surgery planning and coordinated postoperative oncology follow-up."
    return ""


def derive_best_for(hospital: dict, labels: dict[str, str]) -> str:
    explicit = normalize_text(hospital.get("best_for"))
    if explicit:
        return explicit

    reasons = normalize_list(hospital.get("why_recommended"))
    if reasons:
        for reason in reasons:
            candidate = derive_best_for_from_reason(reason)
            if candidate:
                return candidate
        return reasons[0]

    department = normalize_text(hospital.get("department"))
    city = normalize_text(hospital.get("city"))
    if department and city:
        return f"You want {department} support in {city}."
    if department:
        return f"You want a specialist review in {department}."
    return labels["not_provided"]


def derive_patient_facing_summary(hospital: dict, labels: dict[str, str]) -> str:
    explicit = normalize_text(hospital.get("patient_facing_summary"))
    if explicit:
        return explicit

    best_for = derive_best_for(hospital, labels)
    if best_for != labels["not_provided"]:
        lowered = best_for.lower()
        if lowered.startswith("you may need "):
            return f"This hospital may fit you if you need {best_for[13:].rstrip('.')}."
        if lowered.startswith("you need "):
            return f"This hospital may fit you if you need {best_for[9:].rstrip('.')}."
        if lowered.startswith("you want "):
            return f"This hospital may fit you if you want {best_for[9:].rstrip('.')}."
        if "may fit you" in best_for.lower():
            return best_for
        return f"This hospital may fit you if {best_for.rstrip('.')}."

    return "This hospital may fit you if you want a strong specialist review before making travel decisions."


def derive_potential_limitation(hospital: dict) -> str:
    explicit = normalize_text(hospital.get("potential_limitation"))
    if explicit:
        return explicit

    service_text = normalize_text(hospital.get("international_services")).lower()
    if any(token in service_text for token in ["reconfirm", "confirm", "checked directly", "should be checked directly"]):
        return "You should confirm the exact intake route and language support directly before you commit."

    checks = normalize_list(hospital.get("current_checks")) or normalize_list(hospital.get("booking_guidance"))
    if checks:
        return "You still need to confirm department routing, document review steps, and booking workflow before travel."

    return ""


def derive_international_support(hospital: dict, labels: dict[str, str]) -> str:
    return derive_access_evidence_level(hospital, labels)


def derive_budget_level(item: dict, labels: dict[str, str]) -> str:
    return comparison_cost_position(item, labels)


def derive_comparison_summary(payload: dict, hospitals: list[dict], labels: dict[str, str]) -> list[dict]:
    comparison_rows = payload.get("comparison_summary") or []
    if comparison_rows:
        return comparison_rows

    derived_rows = []
    for hospital in hospitals:
        derived_rows.append(
            {
                "hospital": first_non_empty(hospital.get("name_en"), hospital.get("name_zh"), labels["not_provided"]),
                "city": first_non_empty(hospital.get("city"), labels["not_provided"]),
                "best_for": derive_best_for(hospital, labels),
                "jci_status": first_non_empty(hospital.get("jci_status"), "Not currently verified"),
                "international_access_evidence": derive_international_support(hospital, labels),
                "cost_positioning": derive_budget_level(hospital, labels),
            }
        )
    return derived_rows


def build_quick_comparison(payload: dict, hospitals: list[dict], labels: dict[str, str]) -> str:
    rows = [
        f"| {labels['comparison_hospital']} | {labels['city']} | {labels['best_for']} | {labels['jci_status']} | {labels['comparison_support']} | {labels['comparison_budget']} |",
        "|---|---|---|---|---|---|",
    ]
    comparison_rows = derive_comparison_summary(payload, hospitals, labels)
    for item in comparison_rows:
        rows.append(
            "| "
            + " | ".join(
                [
                    markdown_escape(item.get("hospital", labels["not_provided"])),
                    markdown_escape(item.get("city", labels["not_provided"])),
                    markdown_escape(item.get("best_for", labels["not_provided"])),
                    markdown_escape(item.get("jci_status", "Not currently verified")),
                    markdown_escape(item.get("international_access_evidence", labels["not_provided"])),
                    markdown_escape(item.get("cost_positioning", labels["not_provided"])),
                ]
            )
            + " |"
        )
    return "\n".join(rows)


def resolve_hospital_limit(payload: dict) -> int:
    preferences = payload.get("report_preferences", {})
    requested = preferences.get("hospital_count")
    if requested is None:
        return 3
    try:
        requested_count = int(requested)
    except (TypeError, ValueError):
        return 3
    requested_count = max(1, min(requested_count, 5))
    if requested_count <= 3:
        return requested_count
    if payload.get("hospital_count_reason"):
        return requested_count
    return 3


def build_hospital_section(hospital: dict, labels: dict[str, str]) -> str:
    fit_summary = derive_patient_facing_summary(hospital, labels)
    best_for = derive_best_for(hospital, labels)
    potential_limitation = derive_potential_limitation(hospital)
    access_evidence = derive_access_evidence_level(hospital, labels)
    admin_intake = access_status_value(hospital, "admin_intake_status", "Needs manual confirmation")
    record_review = access_status_value(hospital, "record_review_status", "Needs manual confirmation")
    doctor_teleconsult = access_status_value(hospital, "doctor_teleconsult_status", "Not currently verified")
    remote_note = first_non_empty(
        hospital.get("remote_consultation_note"),
        "Doctor-led remote consultation still needs direct confirmation.",
    )
    parts = [
        f"### {hospital.get('rank', '?')}. {hospital.get('name_en', labels['not_provided'])}",
        f"- **{labels['fit_summary']}:** {fit_summary}",
        f"- **{labels['chinese_name']}:** {hospital.get('name_zh', labels['not_provided'])}",
        f"- **{labels['city']}:** {hospital.get('city', labels['not_provided'])}",
        f"- **{labels['best_for']}:** {best_for}",
        f"- **{labels['department']}:** {hospital.get('department', labels['not_provided'])}",
        f"- **{labels['international_services']}:** {hospital.get('international_services', labels['not_provided'])}",
        f"- **{labels['international_access']}:** {access_evidence}",
        f"- **{labels['admin_intake_status']}:** {admin_intake}",
        f"- **{labels['record_review_status']}:** {record_review}",
        f"- **{labels['doctor_teleconsult_status']}:** {doctor_teleconsult}",
        f"- **{labels['jci_status']}:** {hospital.get('jci_status', 'Not currently verified')}",
        f"- **{labels['estimated_cost']}:** {derive_hospital_cost_summary(hospital, labels)}",
        f"- **{labels['contact']}:** {hospital.get('contact', labels['not_provided'])}",
        "",
        f"**{labels['why_recommended']}**",
        bullet_list(normalize_list(hospital.get("why_recommended"))) or f"- {labels['not_provided']}",
    ]
    if remote_note:
        parts.extend(["", f"**{labels['remote_consultation_note']}**", f"- {remote_note}"])
    if potential_limitation:
        parts.extend(["", f"**{labels['potential_limitation']}**", f"- {potential_limitation}"])
    if hospital.get("jci_note"):
        parts.extend(
            [
                "",
                f"**{labels['jci_note']}**",
                f"- {hospital['jci_note']}",
            ]
        )
        if hospital.get("jci_last_verified"):
            parts.append(f"- **{labels['jci_last_verified']}:** {hospital['jci_last_verified']}")
    checks = normalize_list(hospital.get("current_checks"))
    booking_guidance = normalize_list(hospital.get("booking_guidance"))
    if booking_guidance:
        checks = booking_guidance
    if checks:
        parts.extend(["", f"**{labels['current_checks']}**", bullet_list(checks)])
    return "\n".join(parts)


def build_specialist_section(specialist: dict, labels: dict[str, str]) -> str:
    parts = [
        f"### {specialist.get('focus', labels['not_provided'])}",
        f"- **{labels['specialist_hospital']}:** {specialist.get('hospital_name', labels['not_provided'])}",
        f"- **{labels['specialist_summary']}:** {specialist.get('summary', labels['not_provided'])}",
        f"- **{labels['specialist_evidence']}:** {specialist.get('evidence_level', labels['not_provided'])}",
    ]
    if specialist.get("intent_gate"):
        parts.append(f"- **{labels['specialist_intent_gate']}:** {specialist.get('intent_gate')}")
    return "\n".join(parts)


def build_cost_scenario_rows(costs: dict) -> list[tuple[str, str, str]]:
    scenario_map = {
        "consult_only": "Consultation Only",
        "consult_plus_repeat_workup": "Consultation Plus Repeat Workup",
        "procedure_or_admission_path": "Procedure or Admission Path",
        "systemic_treatment_path": "Systemic Treatment Path",
    }
    rows: list[tuple[str, str, str]] = []
    for key, label in scenario_map.items():
        value = costs.get(key)
        if not isinstance(value, dict):
            continue
        rows.append(
            (
                label,
                first_non_empty(value.get("estimate_text"), "Not provided"),
                first_non_empty(value.get("uncertainty_level"), "High uncertainty"),
            )
        )
    return rows


def build_cost_section(costs: dict, labels: dict[str, str]) -> str:
    scenario_rows = build_cost_scenario_rows(costs)
    if scenario_rows:
        lines = [
            f"| {labels['scenario']} | {labels['planning_estimate']} | {labels['uncertainty']} |",
            "|---|---|---|",
        ]
        for scenario, estimate, uncertainty in scenario_rows:
            lines.append(
                f"| {markdown_escape(scenario)} | {markdown_escape(estimate)} | {markdown_escape(uncertainty)} |"
            )
    else:
        lines = [
            f"**{labels['high_uncertainty_heading']}**",
            "",
            "| Item | Estimate |",
            "|---|---|",
            f"| {labels['consultation_range']} | {markdown_escape(costs.get('consultation_range', labels['not_provided']))} |",
            f"| {labels['surgery_range']} | {markdown_escape(costs.get('surgery_range', labels['not_provided']))} |",
            f"| {labels['treatment_range']} | {markdown_escape(costs.get('treatment_range', labels['not_provided']))} |",
            f"| {labels['non_medical_range']} | {markdown_escape(costs.get('non_medical_range', labels['not_provided']))} |",
        ]
    notes = normalize_list(costs.get("notes"))
    if notes:
        lines.extend(["", f"**{labels['notes']}**", bullet_list(notes)])
    return "\n".join(lines)


def build_summary_text(summary: dict, labels: dict[str, str], payload: dict) -> str:
    return sanitize_remote_claims(
        first_non_empty(summary.get("top_takeaway"), summary.get("executive_summary"), labels["not_provided"]),
        payload,
    )


def build_recommendation_logic(summary: dict, labels: dict[str, str], payload: dict) -> str:
    lines = [
        f"- **{labels['clinical_focus']}:** {summary.get('clinical_focus', labels['not_provided'])}",
        f"- **{labels['recommendation_rule']}:** {sanitize_remote_claims(summary.get('recommendation_logic', labels['not_provided']), payload)}",
        f"- **{labels['recommended_length_of_stay']}:** {summary.get('recommended_length_of_stay', labels['not_provided'])}",
    ]
    if summary.get("top_takeaway"):
        lines.insert(0, f"- **{labels['top_takeaway']}:** {sanitize_remote_claims(summary['top_takeaway'], payload)}")
    if summary.get("uncertainty_note"):
        lines.append(f"- **{labels['uncertainty_note']}:** {summary['uncertainty_note']}")
    return "\n".join(lines)


def build_travel_section(travel: dict, labels: dict[str, str]) -> str:
    return "\n".join(
        [
            f"- **{labels['visa']}:** {travel.get('visa', labels['not_provided'])}",
            f"- **{labels['accommodation']}:** {travel.get('accommodation', labels['not_provided'])}",
            f"- **{labels['transportation']}:** {travel.get('transportation', labels['not_provided'])}",
        ]
    )


def build_markdown_report(payload: dict) -> str:
    labels = locale_for(payload)
    summary = payload.get("summary", {})
    hospitals = payload.get("hospitals", [])[: resolve_hospital_limit(payload)]
    specialist_blocks = payload.get("specialists", [])
    evidence_notes = normalize_list(payload.get("evidence_notes"))

    sections = [
        build_front_matter(payload, labels),
        build_metadata_block(payload, labels),
        f"## {labels['top_takeaway_section']}",
        "",
        build_summary_text(summary, labels, payload),
        "",
        f"## {labels['patient_snapshot']}",
        "",
        build_patient_snapshot(payload, labels),
        "",
        f"## {labels['recommendation_logic']}",
        "",
        build_recommendation_logic(summary, labels, payload),
        "",
        f"## {labels['current_limitations_section']}",
        "",
        build_current_limitations(summary, labels),
        "",
        f"## {labels['quick_comparison']}",
        "",
        build_quick_comparison(payload, hospitals, labels),
        "",
        f"## {labels['recommended_hospitals']}",
        "",
    ]

    if hospitals:
        for hospital in hospitals:
            sections.extend([build_hospital_section(hospital, labels), ""])
    else:
        sections.extend([f"- {labels['not_provided']}", ""])

    sections.extend([f"## {labels['specialist_directions']}", ""])
    if specialist_blocks:
        for specialist in specialist_blocks:
            sections.extend([build_specialist_section(specialist, labels), ""])
    else:
        sections.extend([f"- {labels['not_provided']}", ""])

    sections.extend(
        [
            f"## {labels['estimated_costs']}",
            "",
            build_cost_section(payload.get("cost_estimate", {}), labels),
            "",
            f"## {labels['travel_logistics']}",
            "",
            build_travel_section(payload.get("travel", {}), labels),
            "",
            f"## {labels['next_steps']}",
            "",
            numbered_list(normalize_list(payload.get("next_steps")), labels["not_provided"]),
            "",
            f"## {labels['evidence_notes']}",
            "",
            bullet_list(evidence_notes) or f"- {labels['not_provided']}",
            "",
            f"## {labels['important_disclaimer']}",
            "",
            final_disclaimer_text(payload),
            "",
        ]
    )

    return "\n".join(sections).strip() + "\n"


def preferred_pdf_backend() -> str:
    return "reportlab" if REPORTLAB_AVAILABLE else "pandoc"


def ensure_reportlab_font() -> None:
    global _REPORTLAB_FONT_READY
    if _REPORTLAB_FONT_READY or not REPORTLAB_AVAILABLE:
        return
    registerFont(UnicodeCIDFont(REPORTLAB_CJK_FONT))
    _REPORTLAB_FONT_READY = True


def build_pdf_styles():
    ensure_reportlab_font()
    styles = getSampleStyleSheet()
    base = REPORTLAB_CJK_FONT
    styles.add(
        ParagraphStyle(
            name="BrandTitle",
            parent=styles["Title"],
            fontName=base,
            fontSize=26,
            leading=32,
            textColor=brand_color("primary_dark"),
            alignment=TA_LEFT,
            spaceAfter=6,
        )
    )
    styles.add(
        ParagraphStyle(
            name="BrandSubtitle",
            parent=styles["Normal"],
            fontName=base,
            fontSize=11.5,
            leading=16,
            textColor=brand_color("text_secondary"),
            spaceAfter=8,
        )
    )
    styles.add(
        ParagraphStyle(
            name="BrandEyebrow",
            parent=styles["Normal"],
            fontName=base,
            fontSize=9,
            leading=12,
            textColor=brand_color("primary_dark"),
            spaceAfter=4,
        )
    )
    styles.add(
        ParagraphStyle(
            name="SectionHeading",
            parent=styles["Heading1"],
            fontName=base,
            fontSize=16,
            leading=21,
            textColor=brand_color("primary_dark"),
            spaceBefore=12,
            spaceAfter=8,
        )
    )
    styles.add(
        ParagraphStyle(
            name="CardHeading",
            parent=styles["Heading2"],
            fontName=base,
            fontSize=13.5,
            leading=18,
            textColor=brand_color("primary_dark"),
            spaceBefore=8,
            spaceAfter=6,
        )
    )
    styles.add(
        ParagraphStyle(
            name="HospitalTitle",
            parent=styles["Heading2"],
            fontName=base,
            fontSize=15,
            leading=20,
            textColor=brand_color("primary_dark"),
            spaceBefore=0,
            spaceAfter=4,
        )
    )
    styles.add(
        ParagraphStyle(
            name="Body",
            parent=styles["Normal"],
            fontName=base,
            fontSize=10.5,
            leading=15,
            textColor=brand_color("text"),
            spaceAfter=4,
        )
    )
    styles.add(
        ParagraphStyle(
            name="BodySmall",
            parent=styles["Normal"],
            fontName=base,
            fontSize=9.2,
            leading=13,
            textColor=brand_color("text_secondary"),
            spaceAfter=3,
        )
    )
    styles.add(
        ParagraphStyle(
            name="Label",
            parent=styles["Normal"],
            fontName=base,
            fontSize=8.8,
            leading=11,
            textColor=brand_color("text_muted"),
            spaceAfter=1,
        )
    )
    styles.add(
        ParagraphStyle(
            name="CoverTakeaway",
            parent=styles["Normal"],
            fontName=base,
            fontSize=11.5,
            leading=18,
            textColor=brand_color("text"),
            backColor=brand_color("primary_light"),
            borderPadding=12,
            borderWidth=0.6,
            borderColor=brand_color("border"),
            spaceAfter=12,
        )
    )
    styles.add(
        ParagraphStyle(
            name="ContentsItem",
            parent=styles["Normal"],
            fontName=base,
            fontSize=10,
            leading=14,
            leftIndent=8,
            bulletIndent=0,
            textColor=brand_color("text"),
        )
    )
    styles.add(
        ParagraphStyle(
            name="ChecklistItem",
            parent=styles["Normal"],
            fontName=base,
            fontSize=10.2,
            leading=13.5,
            textColor=brand_color("text"),
            leftIndent=8,
            bulletIndent=0,
            spaceAfter=2,
        )
    )
    styles.add(
        ParagraphStyle(
            name="WarningBody",
            parent=styles["Normal"],
            fontName=base,
            fontSize=10.2,
            leading=14,
            textColor=brand_color("text"),
            backColor=brand_color("surface"),
            borderPadding=8,
            borderWidth=0.5,
            borderColor=brand_color("warning"),
            spaceAfter=4,
        )
    )
    return styles


def build_metadata_table(payload: dict, labels: dict[str, str], styles) -> Table:
    patient = payload.get("patient", {})
    rows = [
        [
            Paragraph(f"<b>{pdf_escape(labels['report_id'])}</b><br/>{pdf_escape(payload.get('report_id', labels['not_provided']))}", styles["Body"]),
            Paragraph(f"<b>{pdf_escape(labels['created_at'])}</b><br/>{pdf_escape(payload.get('created_at', labels['not_provided']))}", styles["Body"]),
        ],
        [
            Paragraph(f"<b>Patient</b><br/>{pdf_escape(patient.get('name', labels['not_provided']))}", styles["Body"]),
            Paragraph(f"<b>{pdf_escape(labels['country'])}</b><br/>{pdf_escape(patient.get('country', labels['not_provided']))}", styles["Body"]),
        ],
    ]
    table = Table(rows, colWidths=[85 * mm, 85 * mm], hAlign="LEFT")
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), brand_color("white")),
                ("BOX", (0, 0), (-1, -1), 0.8, brand_color("border")),
                ("INNERGRID", (0, 0), (-1, -1), 0.5, brand_color("border")),
                ("ROWBACKGROUNDS", (0, 0), (-1, -1), [brand_color("white"), brand_color("surface")]),
                ("LEFTPADDING", (0, 0), (-1, -1), 12),
                ("RIGHTPADDING", (0, 0), (-1, -1), 12),
                ("TOPPADDING", (0, 0), (-1, -1), 10),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ]
        )
    )
    return table


def paragraph_or_fallback(text: object, styles, style_name: str, fallback: str) -> Paragraph:
    return Paragraph(pdf_escape(first_non_empty(text, fallback)), styles[style_name])


def bullet_paragraphs(items: list[str], styles) -> list[Paragraph]:
    if not items:
        return [Paragraph("• Not provided", styles["Body"])]
    return [Paragraph(f"• {pdf_escape(item)}", styles["Body"]) for item in items]


def checklist_paragraphs(items: list[str], styles) -> list[Paragraph]:
    if not items:
        return [Paragraph("• Not provided", styles["ChecklistItem"])]
    return [Paragraph(f"• {pdf_escape(item)}", styles["ChecklistItem"]) for item in items]


def build_reportlab_story(payload: dict) -> list:
    labels = locale_for(payload)
    styles = build_pdf_styles()
    summary = payload.get("summary", {})
    hospitals = payload.get("hospitals", [])[: resolve_hospital_limit(payload)]
    specialists = payload.get("specialists", [])
    evidence_notes = normalize_list(payload.get("evidence_notes"))
    comparison_rows = derive_comparison_summary(payload, hospitals, labels)
    costs = payload.get("cost_estimate", {})
    travel = payload.get("travel", {})

    story = [
        Table(
            [[Paragraph("CHINAMED SELECT", styles["BrandEyebrow"])]],
            colWidths=[178 * mm],
            hAlign="LEFT",
            style=TableStyle(
                [
                    ("BACKGROUND", (0, 0), (-1, -1), brand_color("primary")),
                    ("LEFTPADDING", (0, 0), (-1, -1), 10),
                    ("RIGHTPADDING", (0, 0), (-1, -1), 10),
                    ("TOPPADDING", (0, 0), (-1, -1), 5),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
                    ("TEXTCOLOR", (0, 0), (-1, -1), brand_color("white")),
                ]
            ),
        ),
        Spacer(1, 10),
        Paragraph(pdf_escape(labels["title"]), styles["BrandTitle"]),
        Paragraph(pdf_escape(labels["subtitle"]), styles["BrandSubtitle"]),
        Paragraph(pdf_escape(labels["confidentiality"]), styles["BodySmall"]),
        Spacer(1, 8),
        build_metadata_table(payload, labels, styles),
        Spacer(1, 14),
        Paragraph("Top Takeaway", styles["SectionHeading"]),
        Paragraph(
            pdf_escape(build_summary_text(summary, labels, payload)),
            styles["CoverTakeaway"],
        ),
        Paragraph("Clinical Focus", styles["CardHeading"]),
        Paragraph(pdf_escape(summary.get("clinical_focus", labels["not_provided"])), styles["Body"]),
        Spacer(1, 12),
        PageBreak(),
        Paragraph("Contents", styles["SectionHeading"]),
    ]

    for item in [
        "Your Situation at a Glance",
        "Why These Hospitals Were Chosen",
        "Quick Comparison",
        "Detailed Hospital Recommendations",
        "Recommended Specialist Directions",
        "Expected Costs",
        "Travel and Visa Planning",
        "What You Should Do Next",
        "Evidence Notes",
        "Important Disclaimer",
    ]:
        story.append(Paragraph(f"• {pdf_escape(item)}", styles["ContentsItem"]))
    story.extend([Spacer(1, 8), HRFlowable(color=brand_color("border"), width="100%"), Spacer(1, 10)])

    story.extend(
        [
            Paragraph("Your Situation at a Glance", styles["SectionHeading"]),
            Paragraph(f"<b>{pdf_escape(labels['condition_summary'])}:</b> {pdf_escape(payload.get('patient', {}).get('condition_summary', labels['not_provided']))}", styles["Body"]),
            Paragraph(f"<b>{pdf_escape(labels['preferred_city'])}:</b> {pdf_escape(payload.get('patient', {}).get('preferred_city', labels['not_provided']))}", styles["Body"]),
            Paragraph(f"<b>{pdf_escape(labels['travel_time'])}:</b> {pdf_escape(payload.get('patient', {}).get('travel_time', labels['not_provided']))}", styles["Body"]),
            Paragraph(f"<b>{pdf_escape(labels['budget_range'])}:</b> {pdf_escape(payload.get('patient', {}).get('budget_range', labels['not_provided']))}", styles["Body"]),
            Paragraph("Why These Hospitals Were Chosen", styles["SectionHeading"]),
            Paragraph(f"<b>{pdf_escape(labels['recommendation_rule'])}:</b> {pdf_escape(sanitize_remote_claims(summary.get('recommendation_logic', labels['not_provided']), payload))}", styles["Body"]),
        ]
    )
    if summary.get("recommended_length_of_stay"):
        story.append(
            Paragraph(
                f"<b>{pdf_escape(labels['recommended_length_of_stay'])}:</b> {pdf_escape(summary.get('recommended_length_of_stay'))}",
                styles["Body"],
            )
        )
    if summary.get("uncertainty_note"):
        story.append(
            Paragraph(
                f"<b>{pdf_escape(labels['uncertainty_note'])}:</b> {pdf_escape(summary.get('uncertainty_note'))}",
                styles["Body"],
            )
        )
    current_limitations = normalize_list(summary.get("current_limitations"))
    if current_limitations:
        story.append(Paragraph(labels["current_limitations_section"], styles["SectionHeading"]))
        story.extend(bullet_paragraphs(current_limitations, styles))

    story.extend([Paragraph("Quick Comparison", styles["SectionHeading"])])
    comparison_table_rows = [
        [
            Paragraph("<b>Hospital</b>", styles["Body"]),
            Paragraph(f"<b>{pdf_escape(labels['city'])}</b>", styles["Body"]),
            Paragraph(f"<b>{pdf_escape(labels['best_for'])}</b>", styles["Body"]),
            Paragraph(f"<b>{pdf_escape(labels['jci_status'])}</b>", styles["Body"]),
            Paragraph(f"<b>{pdf_escape(labels['comparison_support'])}</b>", styles["Body"]),
            Paragraph(f"<b>{pdf_escape(labels['comparison_budget'])}</b>", styles["Body"]),
        ]
    ]
    for row in comparison_rows:
        comparison_table_rows.append(
            [
                Paragraph(pdf_escape(row.get("hospital", labels["not_provided"])), styles["Body"]),
                Paragraph(pdf_escape(row.get("city", labels["not_provided"])), styles["Body"]),
                Paragraph(pdf_escape(row.get("best_for", labels["not_provided"])), styles["Body"]),
                Paragraph(pdf_escape(row.get("jci_status", "Not currently verified")), styles["Body"]),
                Paragraph(pdf_escape(row.get("international_access_evidence", labels["not_provided"])), styles["Body"]),
                Paragraph(pdf_escape(row.get("cost_positioning", labels["not_provided"])), styles["Body"]),
            ]
        )
    comparison_table = Table(
        comparison_table_rows,
        colWidths=[42 * mm, 18 * mm, 52 * mm, 26 * mm, 26 * mm, 20 * mm],
        repeatRows=1,
        hAlign="LEFT",
    )
    comparison_table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), brand_color("primary_light")),
                ("TEXTCOLOR", (0, 0), (-1, 0), brand_color("primary_dark")),
                ("GRID", (0, 0), (-1, -1), 0.5, brand_color("border")),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("ROWBACKGROUNDS", (0, 1), (-1, -1), [brand_color("white"), brand_color("surface")]),
                ("LEFTPADDING", (0, 0), (-1, -1), 7),
                ("RIGHTPADDING", (0, 0), (-1, -1), 7),
                ("TOPPADDING", (0, 0), (-1, -1), 7),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
            ]
        )
    )
    story.extend([comparison_table, Spacer(1, 10), Paragraph("Detailed Hospital Recommendations", styles["SectionHeading"])])

    for hospital in hospitals:
        metadata_rows = [
            [
                Paragraph(f"<b>{pdf_escape(labels['best_for'])}</b><br/>{pdf_escape(derive_best_for(hospital, labels))}", styles["Body"]),
                Paragraph(
                    f"<b>{pdf_escape(labels['department'])}</b><br/>{pdf_escape(hospital.get('department', labels['not_provided']))}",
                    styles["Body"],
                ),
            ],
            [
                Paragraph(
                    f"<b>{pdf_escape(labels['international_services'])}</b><br/>{pdf_escape(hospital.get('international_services', labels['not_provided']))}",
                    styles["Body"],
                ),
                Paragraph(
                    f"<b>{pdf_escape(labels['international_access'])}</b><br/>{pdf_escape(derive_access_evidence_level(hospital, labels))}",
                    styles["Body"],
                ),
            ],
            [
                Paragraph(
                    f"<b>{pdf_escape(labels['doctor_teleconsult_status'])}</b><br/>{pdf_escape(access_status_value(hospital, 'doctor_teleconsult_status', 'Not currently verified'))}",
                    styles["Body"],
                ),
                Paragraph(
                    f"<b>{pdf_escape(labels['jci_status'])}</b><br/>{pdf_escape(hospital.get('jci_status', 'Not currently verified'))}",
                    styles["Body"],
                ),
            ],
            [
                Paragraph(
                    f"<b>{pdf_escape(labels['estimated_cost'])}</b><br/>{pdf_escape(derive_hospital_cost_summary(hospital, labels))}",
                    styles["Body"],
                ),
                Paragraph(
                    f"<b>{pdf_escape(labels['contact'])}</b><br/>{pdf_escape(hospital.get('contact', labels['not_provided']))}",
                    styles["Body"],
                ),
            ],
        ]
        metadata_table = Table(metadata_rows, colWidths=[87 * mm, 87 * mm], hAlign="LEFT")
        metadata_table.setStyle(
            TableStyle(
                [
                    ("BACKGROUND", (0, 0), (-1, -1), brand_color("surface")),
                    ("BOX", (0, 0), (-1, -1), 0.5, brand_color("border")),
                    ("INNERGRID", (0, 0), (-1, -1), 0.5, brand_color("border")),
                    ("VALIGN", (0, 0), (-1, -1), "TOP"),
                    ("LEFTPADDING", (0, 0), (-1, -1), 8),
                    ("RIGHTPADDING", (0, 0), (-1, -1), 8),
                    ("TOPPADDING", (0, 0), (-1, -1), 8),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
                ]
            )
        )
        card_items = [
            Paragraph(
                pdf_escape(f"{hospital.get('rank', '?')}. {hospital.get('name_en', labels['not_provided'])}"),
                styles["HospitalTitle"],
            ),
            Paragraph(
                f"{pdf_escape(hospital.get('name_zh', labels['not_provided']))}  |  {pdf_escape(hospital.get('city', labels['not_provided']))}",
                styles["BodySmall"],
            ),
            Paragraph(
                f"<b>{pdf_escape(labels['fit_summary'])}:</b> {pdf_escape(derive_patient_facing_summary(hospital, labels))}",
                styles["Body"],
            ),
            metadata_table,
        ]
        if hospital.get("jci_note"):
            card_items.append(
                Paragraph(
                    f"<b>{pdf_escape(labels['jci_note'])}:</b> {pdf_escape(hospital.get('jci_note'))}",
                    styles["Body"],
                )
            )
        if hospital.get("jci_last_verified"):
            card_items.append(
                Paragraph(
                    f"<b>{pdf_escape(labels['jci_last_verified'])}:</b> {pdf_escape(hospital.get('jci_last_verified'))}",
                    styles["BodySmall"],
                )
            )
        remote_note = first_non_empty(
            hospital.get("remote_consultation_note"),
            "Doctor-led remote consultation still needs direct confirmation.",
        )
        card_items.extend(
            [
                Paragraph(pdf_escape(labels["remote_consultation_note"]), styles["CardHeading"]),
                Paragraph(f"• {pdf_escape(remote_note)}", styles["Body"]),
            ]
        )
        card_items.append(Paragraph("Why This May Fit You", styles["CardHeading"]))
        card_items.extend(bullet_paragraphs(normalize_list(hospital.get("why_recommended")), styles))
        potential_limitation = derive_potential_limitation(hospital)
        if potential_limitation:
            card_items.extend(
                [
                    Paragraph("Potential Limitation", styles["CardHeading"]),
                    Paragraph(f"• {pdf_escape(potential_limitation)}", styles["WarningBody"]),
                ]
            )
        checks = normalize_list(hospital.get("booking_guidance")) or normalize_list(hospital.get("current_checks"))
        if checks:
            card_items.append(Paragraph("Before You Book", styles["CardHeading"]))
            card_items.extend(checklist_paragraphs(checks, styles))
        hospital_table = Table([[item] for item in card_items], colWidths=[178 * mm], hAlign="LEFT")
        hospital_table.setStyle(
            TableStyle(
                [
                    ("BACKGROUND", (0, 0), (-1, -1), brand_color("white")),
                    ("BOX", (0, 0), (-1, -1), 0.9, brand_color("border")),
                    ("LINEABOVE", (0, 0), (-1, 0), 2.0, brand_color("primary")),
                    ("LEFTPADDING", (0, 0), (-1, -1), 12),
                    ("RIGHTPADDING", (0, 0), (-1, -1), 12),
                    ("TOPPADDING", (0, 0), (-1, -1), 6),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
                ]
            )
        )
        story.extend([hospital_table, Spacer(1, 12)])

    story.append(Paragraph("Recommended Specialist Directions", styles["SectionHeading"]))
    for specialist in specialists:
        story.extend(
            [
                Paragraph(pdf_escape(specialist.get("focus", labels["not_provided"])), styles["CardHeading"]),
                Paragraph(
                    f"<b>{pdf_escape(labels['specialist_hospital'])}:</b> {pdf_escape(specialist.get('hospital_name', labels['not_provided']))}",
                    styles["Body"],
                ),
                Paragraph(
                    f"<b>{pdf_escape(labels['specialist_summary'])}:</b> {pdf_escape(specialist.get('summary', labels['not_provided']))}",
                    styles["Body"],
                ),
                Paragraph(
                    f"<b>{pdf_escape(labels['specialist_evidence'])}:</b> {pdf_escape(specialist.get('evidence_level', labels['not_provided']))}",
                    styles["BodySmall"],
                ),
            ]
        )
        if specialist.get("intent_gate"):
            story.append(
                Paragraph(
                    f"<b>{pdf_escape(labels['specialist_intent_gate'])}:</b> {pdf_escape(specialist.get('intent_gate'))}",
                    styles["BodySmall"],
                )
            )

    story.append(Paragraph("Expected Costs", styles["SectionHeading"]))
    scenario_rows = build_cost_scenario_rows(costs)
    if scenario_rows:
        cost_rows = [
            [
                Paragraph(f"<b>{pdf_escape(labels['scenario'])}</b>", styles["Body"]),
                Paragraph(f"<b>{pdf_escape(labels['planning_estimate'])}</b>", styles["Body"]),
                Paragraph(f"<b>{pdf_escape(labels['uncertainty'])}</b>", styles["Body"]),
            ]
        ]
        for scenario, estimate, uncertainty in scenario_rows:
            cost_rows.append(
                [
                    Paragraph(pdf_escape(scenario), styles["Body"]),
                    Paragraph(pdf_escape(estimate), styles["Body"]),
                    Paragraph(pdf_escape(uncertainty), styles["Body"]),
                ]
            )
        cost_col_widths = [44 * mm, 96 * mm, 38 * mm]
    else:
        cost_rows = [
            [Paragraph("<b>Item</b>", styles["Body"]), Paragraph("<b>Estimate</b>", styles["Body"])],
            [Paragraph(pdf_escape(labels["consultation_range"]), styles["Body"]), paragraph_or_fallback(costs.get("consultation_range"), styles, "Body", labels["not_provided"])],
            [Paragraph(pdf_escape(labels["surgery_range"]), styles["Body"]), paragraph_or_fallback(costs.get("surgery_range"), styles, "Body", labels["not_provided"])],
            [Paragraph(pdf_escape(labels["treatment_range"]), styles["Body"]), paragraph_or_fallback(costs.get("treatment_range"), styles, "Body", labels["not_provided"])],
            [Paragraph(pdf_escape(labels["non_medical_range"]), styles["Body"]), paragraph_or_fallback(costs.get("non_medical_range"), styles, "Body", labels["not_provided"])],
        ]
        story.append(Paragraph(pdf_escape(labels["high_uncertainty_heading"]), styles["BodySmall"]))
        cost_col_widths = [52 * mm, 126 * mm]
    cost_table = Table(cost_rows, colWidths=cost_col_widths, repeatRows=1, hAlign="LEFT")
    cost_table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), brand_color("primary_light")),
                ("TEXTCOLOR", (0, 0), (-1, 0), brand_color("primary_dark")),
                ("GRID", (0, 0), (-1, -1), 0.5, brand_color("border")),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("ROWBACKGROUNDS", (0, 1), (-1, -1), [brand_color("white"), brand_color("surface")]),
                ("LEFTPADDING", (0, 0), (-1, -1), 8),
                ("RIGHTPADDING", (0, 0), (-1, -1), 8),
                ("TOPPADDING", (0, 0), (-1, -1), 9),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 9),
            ]
        )
    )
    story.extend([cost_table, Spacer(1, 10)])
    for note in normalize_list(costs.get("notes")):
        story.append(Paragraph(f"• {pdf_escape(note)}", styles["BodySmall"]))

    story.extend(
        [
            Paragraph("Travel and Visa Planning", styles["SectionHeading"]),
            Paragraph(f"<b>{pdf_escape(labels['visa'])}:</b> {pdf_escape(travel.get('visa', labels['not_provided']))}", styles["Body"]),
            Paragraph(f"<b>{pdf_escape(labels['accommodation'])}:</b> {pdf_escape(travel.get('accommodation', labels['not_provided']))}", styles["Body"]),
            Paragraph(f"<b>{pdf_escape(labels['transportation'])}:</b> {pdf_escape(travel.get('transportation', labels['not_provided']))}", styles["Body"]),
            Paragraph("What You Should Do Next", styles["SectionHeading"]),
        ]
    )
    for index, step in enumerate(normalize_list(payload.get("next_steps")), start=1):
        story.append(Paragraph(f"{index}. {pdf_escape(step)}", styles["Body"]))
    story.extend([Paragraph("Evidence Notes", styles["SectionHeading"])])
    for item in evidence_notes:
        story.append(Paragraph(f"• {pdf_escape(item)}", styles["Body"]))
    story.extend(
        [
            Paragraph("Important Disclaimer", styles["SectionHeading"]),
            Paragraph(
                pdf_escape(final_disclaimer_text(payload)),
                styles["BodySmall"],
            ),
        ]
    )
    return story


def draw_pdf_chrome(canvas, doc) -> None:
    canvas.saveState()
    canvas.setFillColor(brand_color("primary"))
    canvas.rect(0, A4[1] - 8 * mm, A4[0], 8 * mm, stroke=0, fill=1)
    canvas.setStrokeColor(brand_color("border"))
    canvas.line(doc.leftMargin, 16 * mm, A4[0] - doc.rightMargin, 16 * mm)
    canvas.setFont(REPORTLAB_CJK_FONT, 8.5)
    canvas.setFillColor(brand_color("text_muted"))
    canvas.drawString(doc.leftMargin, 10 * mm, "ChinaMed Select | Hospital recommendation report")
    canvas.drawRightString(A4[0] - doc.rightMargin, 10 * mm, f"Page {doc.page}")
    canvas.restoreState()


def render_reportlab_pdf(payload: dict, pdf_path: Path) -> None:
    if not REPORTLAB_AVAILABLE:
        raise RuntimeError("reportlab is not installed")

    doc = SimpleDocTemplate(
        str(pdf_path),
        pagesize=A4,
        leftMargin=16 * mm,
        rightMargin=16 * mm,
        topMargin=18 * mm,
        bottomMargin=20 * mm,
        title=payload.get("report_id", "hospital-report"),
        author="hospital-recommendation-report",
    )
    story = build_reportlab_story(payload)
    doc.build(story, onFirstPage=draw_pdf_chrome, onLaterPages=draw_pdf_chrome)


def choose_main_font() -> str:
    global _WORKING_FONT
    if _WORKING_FONT is not None:
        return _WORKING_FONT

    for font_name in FONT_CANDIDATES:
        if font_supports_pdf(font_name):
            _WORKING_FONT = font_name
            return font_name

    raise RuntimeError(
        "Unable to find a usable CJK font for PDF generation. "
        f"Tried: {', '.join(FONT_CANDIDATES)}"
    )


def _pandoc_base_command(markdown_path: Path, pdf_path: Path, main_font: str) -> list[str]:
    return [
        "pandoc",
        str(markdown_path),
        "--from=gfm",
        "--standalone",
        "--toc",
        "--toc-depth=2",
        "--pdf-engine=xelatex",
        "-V",
        "geometry:margin=0.85in",
        "-V",
        "papersize:a4",
        "-V",
        f"mainfont={main_font}",
        "-V",
        f"sansfont={main_font}",
        "-V",
        "monofont=Menlo",
        "-V",
        "header-includes=\\usepackage{longtable}\\usepackage{array}\\setlength{\\emergencystretch}{3em}",
        "-V",
        "colorlinks=true",
        "-o",
        str(pdf_path),
    ]


def font_supports_pdf(font_name: str) -> bool:
    with tempfile.TemporaryDirectory(prefix="hospital-report-font-") as temp_dir:
        temp_path = Path(temp_dir)
        markdown_path = temp_path / "probe.md"
        pdf_path = temp_path / "probe.pdf"
        markdown_path.write_text("# Font Probe\n\n中文 English\n", encoding="utf-8")
        result = subprocess.run(
            _pandoc_base_command(markdown_path, pdf_path, font_name),
            capture_output=True,
            text=True,
        )
        return result.returncode == 0


def build_pandoc_command(markdown_path: Path, pdf_path: Path) -> list[str]:
    return _pandoc_base_command(markdown_path, pdf_path, choose_main_font())


def build_fallback_pandoc_command(markdown_path: Path, pdf_path: Path) -> list[str]:
    return _pandoc_base_command(markdown_path, pdf_path, "Arial Unicode MS")


def render_pandoc_pdf(markdown_path: Path, pdf_path: Path) -> None:
    primary = subprocess.run(build_pandoc_command(markdown_path, pdf_path), capture_output=True, text=True)
    if primary.returncode == 0:
        return

    fallback = subprocess.run(build_fallback_pandoc_command(markdown_path, pdf_path), capture_output=True, text=True)
    if fallback.returncode == 0:
        return

    message = fallback.stderr.strip() or primary.stderr.strip() or primary.stdout.strip() or "unknown pandoc error"
    raise RuntimeError(f"Error producing PDF.\n{message}")


def render_pdf(payload: dict, markdown_path: Path, pdf_path: Path) -> None:
    if preferred_pdf_backend() == "reportlab":
        try:
            render_reportlab_pdf(payload, pdf_path)
            return
        except Exception:
            pass
    render_pandoc_pdf(markdown_path, pdf_path)


def write_report_files(payload: dict, output_dir: Path, basename: str, skip_pdf: bool) -> tuple[Path, Path | None]:
    output_dir.mkdir(parents=True, exist_ok=True)
    markdown_path = output_dir / f"{basename}.md"
    pdf_path = output_dir / f"{basename}.pdf"

    markdown_path.write_text(build_markdown_report(payload), encoding="utf-8")
    if skip_pdf:
        return markdown_path, None

    render_pdf(payload, markdown_path, pdf_path)
    return markdown_path, pdf_path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate a premium hospital recommendation report in Markdown and PDF.",
    )
    parser.add_argument("input_json", help="Path to the structured report input JSON file.")
    parser.add_argument("--output-dir", default=".", help="Directory where report files will be written.")
    parser.add_argument(
        "--basename",
        default=None,
        help="Output file basename. Defaults to report_id or 'hospital-report'.",
    )
    parser.add_argument("--skip-pdf", action="store_true", help="Write Markdown only.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    input_path = Path(args.input_json).resolve()
    payload = json.loads(input_path.read_text(encoding="utf-8"))
    basename = args.basename or payload.get("report_id") or "hospital-report"
    markdown_path, pdf_path = write_report_files(
        payload,
        Path(args.output_dir).resolve(),
        basename,
        args.skip_pdf,
    )
    print(f"Markdown: {markdown_path}")
    if pdf_path:
        print(f"PDF: {pdf_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
