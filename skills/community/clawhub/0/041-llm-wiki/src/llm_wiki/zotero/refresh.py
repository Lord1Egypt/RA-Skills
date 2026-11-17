"""One-shot Zotero DOI, citation, and publication freshness worker."""

from __future__ import annotations

import asyncio
import re
from collections.abc import Awaitable, Callable, Mapping, Sequence
from dataclasses import dataclass, field
from datetime import UTC, date, datetime, timedelta
from difflib import SequenceMatcher
from pathlib import Path
from typing import (
    Any,
)
from urllib.parse import urlparse

import httpx

from .cache import EnrichmentCache
from .local import LocalZoteroWriter
from .mcp_client import ZoteroMCPClient
from .plan import ACADEMIC_ITEM_TYPES, extract_doi_from_text, normalize_doi
from .providers import CrossrefProvider, OpenAlexProvider, ProviderError

MANAGED_PREFIX = "llm-wiki:"
DOI_MISSING_TAG = "llm-wiki:doi-missing"
PUBLICATION_REVIEW_TAG = "llm-wiki:publication-review"


@dataclass(frozen=True)
class RefreshSettings:
    request_timeout_seconds: float = 20.0
    max_concurrency: int = 3
    doi_verified_days: int = 365
    doi_missing_days: int = 30
    citation_days: int = 90
    publication_days: int = 30
    journal_metric_days: int = 365
    candidate_threshold: float = 0.92
    candidate_margin: float = 0.05
    verification_threshold: float = 0.72
    crossref_mailto: str = ""
    openalex_api_key: str = ""
    openalex_mailto: str = ""
    add_status_tags: bool = True
    normalize_doi_url: bool = True


@dataclass(frozen=True)
class RefreshItem:
    item_key: str
    title: str
    item_type: str
    date: str
    doi: str
    arxiv: str
    url: str
    tags: frozenset[str]
    creators: tuple[str, ...]
    publication_title: str
    issn: str
    extra: str

    @classmethod
    def from_zotero(cls, data: Mapping[str, Any]) -> RefreshItem:
        tags = frozenset(
            str(raw.get("tag") if isinstance(raw, Mapping) else raw).strip()
            for raw in data.get("tags") or []
            if str(raw.get("tag") if isinstance(raw, Mapping) else raw).strip()
        )
        creators = tuple(
            str(raw.get("lastName") or raw.get("name") or "").strip()
            for raw in data.get("creators") or []
            if isinstance(raw, Mapping)
            and str(raw.get("lastName") or raw.get("name") or "").strip()
        )
        extra = str(data.get("extra") or "")
        url = str(data.get("url") or "").strip()
        return cls(
            item_key=str(data.get("key") or "").strip(),
            title=str(data.get("title") or "").strip(),
            item_type=str(data.get("itemType") or "").strip(),
            date=str(data.get("date") or "").strip(),
            doi=normalize_doi(data.get("DOI")),
            arxiv=_extract_arxiv(extra, url),
            url=url,
            tags=tags,
            creators=creators,
            publication_title=str(data.get("publicationTitle") or "").strip(),
            issn=str(data.get("ISSN") or "").strip(),
            extra=extra,
        )


@dataclass
class RefreshMutation:
    item_key: str
    title: str
    doi_status: str = "unknown"
    citation_provider: str = ""
    citation_count: int | None = None
    safe_set_keys: dict[str, str] = field(default_factory=dict)
    add_tags: set[str] = field(default_factory=set)
    remove_tags: set[str] = field(default_factory=set)
    safe_fields: dict[str, str] = field(default_factory=dict)
    metadata_review: dict[str, Any] = field(default_factory=dict)
    errors: list[str] = field(default_factory=list)
    applied: bool = False

    @property
    def has_safe_changes(self) -> bool:
        return bool(
            self.safe_set_keys or self.add_tags or self.remove_tags or self.safe_fields
        )


@dataclass
class RefreshReport:
    collection_key: str
    collection_name: str
    items: list[RefreshMutation]
    applied_count: int = 0


def settings_from_config(config: Mapping[str, Any]) -> RefreshSettings:
    section = config.get("zotero_enrichment") or {}
    stale = section.get("stale_after_days") or {}
    crossref = section.get("crossref") or {}
    openalex = section.get("openalex") or {}
    apply = section.get("apply") or {}
    return RefreshSettings(
        request_timeout_seconds=float(section.get("request_timeout_seconds", 20.0)),
        max_concurrency=max(1, int(section.get("max_concurrency", 3))),
        doi_verified_days=max(1, int(stale.get("verified_doi", 365))),
        doi_missing_days=max(1, int(stale.get("missing_doi", 30))),
        citation_days=max(1, int(stale.get("citations", 90))),
        publication_days=max(1, int(stale.get("preprint_publication", 30))),
        journal_metric_days=max(1, int(stale.get("journal_metrics", 365))),
        candidate_threshold=float(section.get("candidate_threshold", 0.92)),
        candidate_margin=float(section.get("candidate_margin", 0.05)),
        verification_threshold=float(section.get("verification_threshold", 0.72)),
        crossref_mailto=str(crossref.get("mailto") or ""),
        openalex_api_key=str(openalex.get("api_key") or ""),
        openalex_mailto=str(openalex.get("mailto") or ""),
        add_status_tags=bool(apply.get("add_status_tags", True)),
        normalize_doi_url=bool(apply.get("normalize_doi_url", True)),
    )


def parse_extra_keys(extra: str) -> dict[str, str]:
    values: dict[str, str] = {}
    for line in str(extra or "").splitlines():
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        key = key.strip()
        if key:
            values[key] = value.strip()
    return values


def _extract_arxiv(extra: str, url: str) -> str:
    text = f"{extra}\n{url}"
    match = re.search(
        r"(?:arXiv:\s*|arxiv\.org/(?:abs|pdf)/)(\d{4}\.\d{4,5})(?:v\d+)?",
        text,
        re.IGNORECASE,
    )
    return match.group(1) if match else ""


def _normalize_title(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "", value.casefold())


def title_similarity(left: str, right: str) -> float:
    a = _normalize_title(left)
    b = _normalize_title(right)
    if not a or not b:
        return 0.0
    ratio = SequenceMatcher(None, a, b).ratio()
    shorter, longer = sorted((a, b), key=len)
    if shorter in longer and len(shorter) / len(longer) >= 0.55:
        ratio = max(ratio, 0.94)
    return ratio


def _year(value: Any) -> int | None:
    match = re.search(r"(?:19|20)\d{2}", str(value or ""))
    return int(match.group(0)) if match else None


def _crossref_year(work: Mapping[str, Any]) -> int | None:
    for key in (
        "published-print",
        "published-online",
        "published",
        "issued",
        "created",
    ):
        value = work.get(key)
        if not isinstance(value, Mapping):
            continue
        parts = value.get("date-parts")
        if (
            isinstance(parts, list)
            and parts
            and isinstance(parts[0], list)
            and parts[0]
        ):
            try:
                return int(parts[0][0])
            except (TypeError, ValueError):
                continue
    return None


def _crossref_title(work: Mapping[str, Any]) -> str:
    titles = work.get("title") or []
    return str(titles[0]).strip() if titles else ""


def _crossref_author(work: Mapping[str, Any]) -> str:
    authors = work.get("author") or []
    if authors and isinstance(authors[0], Mapping):
        return str(authors[0].get("family") or "").strip()
    return ""


def _crossref_doi(work: Mapping[str, Any]) -> str:
    return normalize_doi(work.get("DOI"))


def _openalex_id(work: Mapping[str, Any]) -> str:
    return str(work.get("id") or "").rstrip("/").rsplit("/", 1)[-1]


def _openalex_source_id(work: Mapping[str, Any]) -> str:
    location = work.get("primary_location")
    source = location.get("source") if isinstance(location, Mapping) else None
    return str(source.get("id") or "") if isinstance(source, Mapping) else ""


def _identity_score(
    item: RefreshItem, work: Mapping[str, Any]
) -> tuple[float, dict[str, Any]]:
    candidate_title = _crossref_title(work)
    title_score = title_similarity(item.title, candidate_title)
    scores: list[tuple[float, float]] = [(0.70, title_score)]

    author_match: bool | None = None
    candidate_author = _crossref_author(work)
    if item.creators and candidate_author:
        author_match = item.creators[0].casefold() == candidate_author.casefold()
        scores.append((0.20, 1.0 if author_match else 0.0))

    item_year = _year(item.date)
    candidate_year = _crossref_year(work)
    year_delta: int | None = None
    if item_year and candidate_year:
        year_delta = abs(item_year - candidate_year)
        year_score = (
            1.0
            if year_delta == 0
            else 0.7
            if year_delta == 1
            else 0.3
            if year_delta == 2
            else 0.0
        )
        scores.append((0.10, year_score))

    weight = sum(part[0] for part in scores)
    score = sum(part_weight * value for part_weight, value in scores) / weight
    evidence = {
        "title": candidate_title,
        "title_similarity": round(title_score, 4),
        "first_author_match": author_match,
        "year_delta": year_delta,
    }
    return score, evidence


def _select_crossref_candidate(
    item: RefreshItem,
    works: Sequence[Mapping[str, Any]],
    settings: RefreshSettings,
) -> dict[str, Any] | None:
    ranked: list[tuple[float, Mapping[str, Any], dict[str, Any]]] = []
    for work in works:
        doi = _crossref_doi(work)
        if not doi:
            continue
        score, evidence = _identity_score(item, work)
        ranked.append((score, work, evidence))
    ranked.sort(key=lambda entry: entry[0], reverse=True)
    if not ranked:
        return None
    best_score, best_work, evidence = ranked[0]
    next_score = ranked[1][0] if len(ranked) > 1 else 0.0
    if best_score < settings.candidate_threshold:
        return None
    if len(ranked) > 1 and best_score - next_score < settings.candidate_margin:
        return None
    return {
        "doi": _crossref_doi(best_work),
        "score": round(best_score, 4),
        "next_score": round(next_score, 4),
        "evidence": evidence,
        "work": dict(best_work),
    }


def _parse_checked_date(value: str) -> date | None:
    try:
        return date.fromisoformat(value[:10])
    except (TypeError, ValueError):
        return None


def _is_due(
    extra: Mapping[str, str], key: str, days: int, today: date, force: bool
) -> bool:
    if force:
        return True
    checked = _parse_checked_date(extra.get(key, ""))
    return checked is None or today - checked >= timedelta(days=days)


def _changed_keys(
    current: Mapping[str, str], desired: Mapping[str, Any]
) -> dict[str, str]:
    return {
        str(key): str(value)
        for key, value in desired.items()
        if value is not None and current.get(str(key)) != str(value)
    }


class RefreshWorker:
    def __init__(
        self,
        crossref: CrossrefProvider,
        openalex: OpenAlexProvider,
        cache: EnrichmentCache,
        settings: RefreshSettings,
        *,
        today: date | None = None,
        force: bool = False,
    ) -> None:
        self.crossref = crossref
        self.openalex = openalex
        self.cache = cache
        self.settings = settings
        self.today = today or datetime.now(UTC).date()
        self.force = force

    async def _cached(
        self,
        item_key: str,
        provider: str,
        operation: str,
        max_age_days: int,
        fetch: Callable[[], Awaitable[Any]],
    ) -> tuple[Any | None, str | None]:
        if not self.force:
            cached = self.cache.get_json(
                item_key,
                provider,
                operation,
                max_age_days=max_age_days,
            )
            if cached is not None:
                return cached, None
        try:
            value = await fetch()
        except ProviderError as exc:
            self.cache.put_error(item_key, provider, operation, str(exc))
            return None, str(exc)
        self.cache.put_json(item_key, provider, operation, value)
        return value, None

    async def _crossref_work(
        self, item: RefreshItem, doi: str
    ) -> tuple[dict[str, Any] | None, str | None]:
        value, error = await self._cached(
            item.item_key,
            "crossref",
            f"doi:{doi.casefold()}",
            self.settings.doi_verified_days,
            lambda: self.crossref.get_work(doi),
        )
        return (dict(value) if isinstance(value, Mapping) else None), error

    async def _crossref_search(
        self, item: RefreshItem
    ) -> tuple[list[dict[str, Any]], str | None]:
        signature = _normalize_title(item.title)[:80]
        value, error = await self._cached(
            item.item_key,
            "crossref",
            f"search:{signature}",
            self.settings.doi_missing_days,
            lambda: self.crossref.search_works(
                item.title,
                author=item.creators[0] if item.creators else "",
            ),
        )
        return ([dict(raw) for raw in value] if isinstance(value, list) else []), error

    async def _openalex_work(
        self, item: RefreshItem, doi: str
    ) -> tuple[dict[str, Any] | None, str | None]:
        value, error = await self._cached(
            item.item_key,
            "openalex",
            f"doi:{doi.casefold()}",
            self.settings.citation_days,
            lambda: self.openalex.get_work_by_doi(doi),
        )
        return (dict(value) if isinstance(value, Mapping) else None), error

    async def _openalex_source(
        self, item: RefreshItem, source_id: str
    ) -> tuple[dict[str, Any] | None, str | None]:
        value, error = await self._cached(
            item.item_key,
            "openalex",
            f"source:{source_id.rsplit('/', 1)[-1]}",
            self.settings.journal_metric_days,
            lambda: self.openalex.get_source(source_id),
        )
        return (dict(value) if isinstance(value, Mapping) else None), error

    async def refresh_item(self, item: RefreshItem) -> RefreshMutation:
        mutation = RefreshMutation(item_key=item.item_key, title=item.title)
        if item.item_type not in ACADEMIC_ITEM_TYPES:
            mutation.errors.append(
                f"unsupported item type: {item.item_type or 'unknown'}"
            )
            return mutation

        extra = parse_extra_keys(item.extra)
        today_text = self.today.isoformat()
        current_doi = item.doi
        crossref_work: dict[str, Any] | None = None
        doi_candidate: dict[str, Any] | None = None
        desired_keys: dict[str, Any] = {}

        doi_days = (
            self.settings.doi_verified_days
            if current_doi
            else self.settings.doi_missing_days
        )
        doi_due = _is_due(
            extra, "LLM-Wiki DOI Checked", doi_days, self.today, self.force
        )
        publication_due = item.item_type == "preprint" and _is_due(
            extra,
            "LLM-Wiki Publication Checked",
            self.settings.publication_days,
            self.today,
            self.force,
        )

        if current_doi and doi_due:
            crossref_work, error = await self._crossref_work(item, current_doi)
            if error:
                mutation.errors.append(f"Crossref DOI lookup: {error}")
            if crossref_work:
                score, evidence = _identity_score(item, crossref_work)
                author_year_match = (
                    evidence.get("first_author_match") is True
                    and evidence.get("year_delta") is not None
                    and int(evidence["year_delta"]) <= 1
                )
                if score >= self.settings.verification_threshold or author_year_match:
                    mutation.doi_status = "verified"
                    desired_keys.update(
                        {
                            "LLM-Wiki DOI Status": "verified",
                            "LLM-Wiki DOI Checked": today_text,
                            "LLM-Wiki DOI Check Provider": "Crossref",
                        }
                    )
                else:
                    mutation.doi_status = "review"
                    desired_keys.update(
                        {
                            "LLM-Wiki DOI Status": "review",
                            "LLM-Wiki DOI Checked": today_text,
                            "LLM-Wiki DOI Check Provider": "Crossref",
                        }
                    )
                    mutation.metadata_review["doi_identity_conflict"] = {
                        "doi": current_doi,
                        "score": round(score, 4),
                        "evidence": evidence,
                    }
            elif not error:
                mutation.doi_status = "review"
                desired_keys.update(
                    {
                        "LLM-Wiki DOI Status": "review",
                        "LLM-Wiki DOI Checked": today_text,
                        "LLM-Wiki DOI Check Provider": "Crossref",
                    }
                )
                mutation.metadata_review["doi_unresolved"] = {"doi": current_doi}
        elif current_doi:
            mutation.doi_status = extra.get("LLM-Wiki DOI Status", "recorded")

        if not current_doi and (doi_due or publication_due):
            candidates, error = await self._crossref_search(item)
            if error:
                mutation.errors.append(f"Crossref title search: {error}")
            doi_candidate = _select_crossref_candidate(item, candidates, self.settings)
            if doi_candidate:
                mutation.doi_status = "review"
                desired_keys.update(
                    {
                        "LLM-Wiki DOI Status": "review",
                        "LLM-Wiki DOI Checked": today_text,
                        "LLM-Wiki DOI Check Provider": "Crossref",
                        "LLM-Wiki DOI Candidate": doi_candidate["doi"],
                    }
                )
                mutation.metadata_review["doi_candidate"] = {
                    key: value for key, value in doi_candidate.items() if key != "work"
                }
                if item.item_type == "preprint":
                    mutation.metadata_review["published_version_candidate"] = {
                        key: value
                        for key, value in doi_candidate.items()
                        if key != "work"
                    }
            elif not error:
                mutation.doi_status = "missing"
                desired_keys.update(
                    {
                        "LLM-Wiki DOI Status": "missing",
                        "LLM-Wiki DOI Checked": today_text,
                        "LLM-Wiki DOI Check Provider": "Crossref",
                    }
                )
        elif not current_doi:
            mutation.doi_status = extra.get("LLM-Wiki DOI Status", "missing")
            stored_candidate = extra.get("LLM-Wiki DOI Candidate") or extra.get(
                "LLM-Wiki Published DOI Candidate"
            )
            if mutation.doi_status == "review" and stored_candidate:
                mutation.metadata_review["doi_candidate"] = {
                    "doi": stored_candidate,
                    "source": "Zotero Extra",
                }
                if item.item_type == "preprint":
                    mutation.metadata_review["published_version_candidate"] = {
                        "doi": stored_candidate,
                        "source": "Zotero Extra",
                    }

        if item.item_type == "preprint" and publication_due:
            if doi_candidate:
                desired_keys.update(
                    {
                        "LLM-Wiki Publication Status": "candidate-found",
                        "LLM-Wiki Published DOI Candidate": doi_candidate["doi"],
                        "LLM-Wiki Publication Checked": today_text,
                    }
                )
            elif not any(
                message.startswith("Crossref title search")
                for message in mutation.errors
            ):
                desired_keys.update(
                    {
                        "LLM-Wiki Publication Status": "preprint",
                        "LLM-Wiki Publication Checked": today_text,
                    }
                )

        citation_due = bool(current_doi) and _is_due(
            extra,
            "LLM-Wiki Citations Checked",
            self.settings.citation_days,
            self.today,
            self.force,
        )
        journal_due = bool(current_doi) and _is_due(
            extra,
            "LLM-Wiki Journal Metric Checked",
            self.settings.journal_metric_days,
            self.today,
            self.force,
        )
        if current_doi and (citation_due or journal_due):
            openalex_work, error = await self._openalex_work(item, current_doi)
            if error:
                mutation.errors.append(f"OpenAlex DOI lookup: {error}")
            if openalex_work:
                if citation_due:
                    count = openalex_work.get("cited_by_count")
                    if isinstance(count, int):
                        mutation.citation_provider = "OpenAlex"
                        mutation.citation_count = count
                        desired_keys.update(
                            {
                                "LLM-Wiki OpenAlex ID": _openalex_id(openalex_work),
                                "LLM-Wiki Citations OpenAlex": count,
                                "LLM-Wiki Citations Checked": today_text,
                            }
                        )
                if journal_due:
                    source_id = _openalex_source_id(openalex_work)
                    if source_id:
                        source, source_error = await self._openalex_source(
                            item, source_id
                        )
                        if source_error:
                            mutation.errors.append(
                                f"OpenAlex source lookup: {source_error}"
                            )
                        if source:
                            summary = source.get("summary_stats")
                            if isinstance(summary, Mapping):
                                desired_keys.update(
                                    {
                                        "LLM-Wiki Journal Metric Provider": "OpenAlex",
                                        "LLM-Wiki Journal Metric Checked": today_text,
                                        "LLM-Wiki Journal 2yr Citedness": (
                                            round(
                                                float(summary["2yr_mean_citedness"]), 4
                                            )
                                            if summary.get("2yr_mean_citedness")
                                            is not None
                                            else None
                                        ),
                                        "LLM-Wiki Journal H-Index": summary.get(
                                            "h_index"
                                        ),
                                    }
                                )
            elif citation_due and crossref_work:
                count = crossref_work.get("is-referenced-by-count")
                if isinstance(count, int):
                    mutation.citation_provider = "Crossref"
                    mutation.citation_count = count
                    desired_keys.update(
                        {
                            "LLM-Wiki Citations Crossref": count,
                            "LLM-Wiki Citations Checked": today_text,
                        }
                    )

        if self.settings.add_status_tags:
            if mutation.doi_status == "missing":
                mutation.add_tags.add(DOI_MISSING_TAG)
            elif mutation.doi_status == "verified":
                mutation.remove_tags.add(DOI_MISSING_TAG)
            if "published_version_candidate" in mutation.metadata_review:
                mutation.add_tags.add(PUBLICATION_REVIEW_TAG)
            elif item.item_type == "preprint" and publication_due:
                mutation.remove_tags.add(PUBLICATION_REVIEW_TAG)

        mutation.add_tags.difference_update(item.tags)
        mutation.remove_tags.intersection_update(item.tags)

        if (
            self.settings.normalize_doi_url
            and current_doi
            and mutation.doi_status == "verified"
        ):
            canonical_url = f"https://doi.org/{current_doi}"
            parsed = urlparse(item.url)
            is_doi_url = parsed.hostname in {"doi.org", "dx.doi.org"}
            if not item.url or (
                is_doi_url
                and extract_doi_from_text(item.url).casefold() != current_doi.casefold()
            ):
                mutation.safe_fields["url"] = canonical_url

        mutation.safe_set_keys = _changed_keys(extra, desired_keys)
        return mutation


async def build_refresh_report(
    items: Sequence[RefreshItem],
    worker: RefreshWorker,
    *,
    collection_key: str,
    collection_name: str,
    concurrency: int,
) -> RefreshReport:
    semaphore = asyncio.Semaphore(max(1, concurrency))

    async def refresh(item: RefreshItem) -> RefreshMutation:
        async with semaphore:
            return await worker.refresh_item(item)

    mutations = list(await asyncio.gather(*(refresh(item) for item in items)))
    return RefreshReport(
        collection_key=collection_key,
        collection_name=collection_name,
        items=mutations,
    )


def failed_item_mutations(failures: Sequence[tuple[str, str]]) -> list[RefreshMutation]:
    """把元数据加载失败的条目降级为待修复记录(不产生任何安全写入)。"""
    return [
        RefreshMutation(
            item_key=key,
            title="(metadata unavailable)",
            errors=[f"metadata load failed; pending heal: {message}"],
        )
        for key, message in failures
    ]


def report_to_manifest(report: RefreshReport) -> dict[str, Any]:
    items: list[dict[str, Any]] = []
    for mutation in report.items:
        entry: dict[str, Any] = {
            "item_key": mutation.item_key,
            "title": mutation.title,
            "doi_status": mutation.doi_status,
        }
        if (
            mutation.safe_set_keys
            or mutation.add_tags
            or mutation.remove_tags
            or mutation.safe_fields
        ):
            entry["safe_updates"] = {}
            if mutation.safe_set_keys:
                entry["safe_updates"]["set_keys"] = dict(
                    sorted(mutation.safe_set_keys.items())
                )
            if mutation.add_tags:
                entry["safe_updates"]["add_tags"] = sorted(mutation.add_tags)
            if mutation.remove_tags:
                entry["safe_updates"]["remove_tags"] = sorted(mutation.remove_tags)
            if mutation.safe_fields:
                entry["safe_updates"]["fields"] = dict(
                    sorted(mutation.safe_fields.items())
                )
        if mutation.metadata_review:
            entry["metadata_review"] = mutation.metadata_review
        if mutation.errors:
            entry["errors"] = list(mutation.errors)
        items.append(entry)
    return {
        "version": 1,
        "mode": "review-only",
        "collection": {"name": report.collection_name, "key": report.collection_key},
        "items": items,
    }


def _verify_applied_mutation(
    mutation: RefreshMutation, metadata: Mapping[str, Any]
) -> None:
    extra = parse_extra_keys(str(metadata.get("extra") or ""))
    for key, value in mutation.safe_set_keys.items():
        if extra.get(key) != str(value):
            raise RuntimeError(
                f"Write verification failed for {mutation.item_key}: Extra key {key}"
            )
    tags = {
        str(raw.get("tag") if isinstance(raw, Mapping) else raw).strip()
        for raw in metadata.get("tags") or []
    }
    if not mutation.add_tags.issubset(tags):
        raise RuntimeError(
            f"Write verification failed for {mutation.item_key}: added tags"
        )
    if mutation.remove_tags.intersection(tags):
        raise RuntimeError(
            f"Write verification failed for {mutation.item_key}: removed tags"
        )
    for key, value in mutation.safe_fields.items():
        raw_key = "DOI" if key == "doi" else key
        if str(metadata.get(raw_key) or "") != str(value):
            raise RuntimeError(
                f"Write verification failed for {mutation.item_key}: field {key}"
            )


async def run_live_refresh(
    project_root: Path,
    *,
    collection_key: str,
    settings: RefreshSettings,
    cache_path: Path,
    mcp_config_path: Path,
    mcp_server_name: str = "zotero",
    item_keys: set[str] | None = None,
    limit: int | None = None,
    force: bool = False,
    apply_safe: bool = False,
    write_backend: str = "web",
    local_store_path: Path | None = None,
    local_base_url: str | None = None,
) -> RefreshReport:
    async with ZoteroMCPClient(mcp_config_path, server_name=mcp_server_name) as zotero:
        collection_name, keys = await zotero.get_collection_item_keys(collection_key)
        if item_keys:
            keys = [key for key in keys if key in item_keys]
        if limit is not None:
            keys = keys[: max(0, limit)]
        metadata, load_failures = await zotero.get_items_tolerant(
            keys, concurrency=settings.max_concurrency
        )
        items = [RefreshItem.from_zotero(data) for data in metadata]

        timeout = httpx.Timeout(settings.request_timeout_seconds)
        limits = httpx.Limits(max_connections=max(4, settings.max_concurrency * 2))
        with EnrichmentCache(cache_path) as cache:
            async with httpx.AsyncClient(
                timeout=timeout, limits=limits, follow_redirects=True
            ) as http:
                worker = RefreshWorker(
                    CrossrefProvider(http, mailto=settings.crossref_mailto),
                    OpenAlexProvider(
                        http,
                        api_key=settings.openalex_api_key,
                        mailto=settings.openalex_mailto,
                    ),
                    cache,
                    settings,
                    force=force,
                )
                report = await build_refresh_report(
                    items,
                    worker,
                    collection_key=collection_key,
                    collection_name=collection_name,
                    concurrency=settings.max_concurrency,
                )
        if load_failures:
            report.items.extend(failed_item_mutations(load_failures))

        if apply_safe:
            writer: Any = zotero
            local_writer: LocalZoteroWriter | None = None
            if write_backend == "local":
                if local_store_path is None:
                    raise ValueError("write_backend='local' requires local_store_path")
                _writer_kwargs: dict[str, Any] = {}
                if local_base_url:
                    _writer_kwargs["base_url"] = local_base_url
                local_writer = LocalZoteroWriter.from_store(
                    local_store_path, **_writer_kwargs
                )
                writer = local_writer
            pending: dict[str, RefreshMutation] = {}
            try:
                for mutation in report.items:
                    if not mutation.has_safe_changes:
                        continue
                    try:
                        await writer.write_safe_mutation(
                            mutation.item_key,
                            set_keys=mutation.safe_set_keys,
                            add_tags=mutation.add_tags,
                            remove_tags=mutation.remove_tags,
                            fields=mutation.safe_fields,
                        )
                    except (OSError, RuntimeError, TypeError, ValueError) as exc:
                        mutation.errors.append(f"safe apply failed: {exc}")
                        continue
                    pending[mutation.item_key] = mutation

                for attempt, delay in enumerate((1.0, 2.0, 4.0, 0.0)):
                    if not pending:
                        break
                    if delay:
                        await asyncio.sleep(delay)
                    try:
                        (
                            metadata_batch,
                            _verify_load_failures,
                        ) = await zotero.get_items_tolerant(
                            list(pending),
                            concurrency=settings.max_concurrency,
                        )
                    except (OSError, RuntimeError, TypeError, ValueError) as exc:
                        if attempt == 3:
                            for mutation in pending.values():
                                mutation.errors.append(
                                    f"safe apply verification failed: {exc}"
                                )
                            pending.clear()
                        continue

                    metadata_by_key = {
                        str(metadata.get("key") or ""): metadata
                        for metadata in metadata_batch
                    }
                    failed: dict[str, RefreshMutation] = {}
                    for item_key, mutation in pending.items():
                        metadata = metadata_by_key.get(item_key)
                        if metadata is None:
                            failed[item_key] = mutation
                            continue
                        try:
                            _verify_applied_mutation(mutation, metadata)
                        except RuntimeError:
                            failed[item_key] = mutation
                            continue
                        mutation.applied = True
                        report.applied_count += 1
                    pending = failed
            finally:
                if local_writer is not None:
                    await local_writer.aclose()

            for mutation in pending.values():
                mutation.errors.append(
                    "safe apply verification failed after bounded retries"
                )
        return report
