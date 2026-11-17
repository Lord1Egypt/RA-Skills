"""Shared data models. This module contains no verification behavior."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class CanonicalRecord:
    source: str
    title: str = ""
    year: str = ""
    journal: str = ""
    journal_abbreviation: str = ""
    journal_aliases: list[str] = field(default_factory=list)
    publication_years: list[str] = field(default_factory=list)
    volume: str = ""
    issue: str = ""
    pages: str = ""
    article_number: str = ""
    doi: str = ""
    pmid: str = ""
    authors: list[str] = field(default_factory=list)
    url: str = ""
    score: float = 0.0
    pubmed_corroborated: bool = False
    openalex_corroborated: bool = False


@dataclass
class ReferenceEntry:
    index: int
    original: str
    citation_format: str
    title: str
    authors: list[str]
    journal: str
    year: str
    doi: str
    pmid: str
    urls: list[str]
    normalized_key: str
    volume: str = ""
    issue: str = ""
    pages: str = ""
    article_number: str = ""
    occurrence_count: int = 1
    source_lines: list[int] = field(default_factory=list)
    context: str = ""
    input_source: str = "parsed_reference"
    title_reliable: bool = True
    input_warnings: list[str] = field(default_factory=list)
    recovered_doi: str = ""
    recovered_doi_source: str = ""


@dataclass
class AuditResult:
    index: int
    status: str
    severity: str
    citation_format: str
    original: str
    parsed_title: str
    parsed_authors: list[str]
    parsed_journal: str
    parsed_year: str
    parsed_doi: str
    parsed_pmid: str
    parsed_title_reliable: bool
    input_warnings: list[str]
    canonical: CanonicalRecord | None
    identifier_record: CanonicalRecord | None
    title_similarity: float
    issues: list[str]
    suggested_action: str
    fixed_reference: str
    evidence_links: list[str]
    shifted_from_index: int | None = None
    shifted_to_index: int | None = None
    verification_level: str = "not_checked"
    usable: bool = False
    repair_state: str = "unchanged"
    field_differences: list[dict] = field(default_factory=list)
    policy_version: str = ""
    checked_at: str = ""
    check_mode: str = ""
    check_channels: list[str] = field(default_factory=list)
    pipeline: str = ""
    source_fields: dict = field(default_factory=dict)
    provider_records: list[dict] = field(default_factory=list)


@dataclass(frozen=True)
class OutputPaths:
    normalized_input: Path
    normalized_records: Path
    extracted_references: Path
    summary: Path
    detail: Path
    html_report: Path
    fixed: Path
    audit_json: Path
