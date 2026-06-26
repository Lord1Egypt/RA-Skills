"""
Helper models and utilities for the geo-bulk-processor skill.

This module is intentionally lightweight. It is designed as a reference
for how to model content items, clusters, and bulk GEO pipelines in a
structured way, so human teams and automation scripts can implement
the plans produced by the skill.

You do not need to execute this file to use the skill. Treat it as
an optional helper and source of inspiration for data structures.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class ContentItem:
    """
    Represents a single page or document in a GEO bulk corpus.
    """

    id: str
    url: Optional[str] = None
    path: Optional[str] = None
    content_type: Optional[str] = None  # e.g., "blog", "product", "location"
    language: Optional[str] = None
    cluster: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class PipelineStep:
    """
    A single logical step in a GEO bulk pipeline.

    Examples:
      - 'normalize_fields'
      - 'generate_faqs_with_geo_skill'
      - 'add_schema_with_geo_schema_gen'
      - 'export_to_cms_import_format'
    """

    name: str
    description: str
    inputs: List[str] = field(default_factory=list)
    outputs: List[str] = field(default_factory=list)
    external_skills: List[str] = field(default_factory=list)


@dataclass
class PipelineDefinition:
    """
    A reusable pipeline definition for one cluster or page type.
    """

    id: str
    cluster: str
    description: str
    steps: List[PipelineStep] = field(default_factory=list)


def summarize_inventory(items: List[ContentItem]) -> Dict[str, Any]:
    """
    Produce a high-level summary of a bulk corpus.

    This is a reference implementation that shows what kind of
    aggregated view is useful when designing bulk GEO strategies.
    """

    summary: Dict[str, Any] = {
        "total_items": len(items),
        "by_content_type": {},
        "by_language": {},
        "by_cluster": {},
    }

    for item in items:
        if item.content_type:
            summary["by_content_type"].setdefault(item.content_type, 0)
            summary["by_content_type"][item.content_type] += 1
        if item.language:
            summary["by_language"].setdefault(item.language, 0)
            summary["by_language"][item.language] += 1
        if item.cluster:
            summary["by_cluster"].setdefault(item.cluster, 0)
            summary["by_cluster"][item.cluster] += 1

    return summary


def example_pipeline_for_cluster(cluster_name: str) -> PipelineDefinition:
    """
    Return an illustrative pipeline definition for a given cluster name.

    This is not meant to be exhaustive or final. It simply demonstrates
    how to structure pipeline steps so that different tools and geo-*
    skills can be composed together in a repeatable way.
    """

    steps = [
        PipelineStep(
            name="ingest_and_normalize",
            description="Ingest records for this cluster and normalize fields into a common schema.",
            inputs=["raw_export"],
            outputs=["normalized_records"],
            external_skills=[],
        ),
        PipelineStep(
            name="content_enrichment",
            description="Enrich or rewrite content fields with GEO-focused templates and patterns.",
            inputs=["normalized_records"],
            outputs=["geo_enriched_records"],
            external_skills=["geo-content-optimizer"],
        ),
        PipelineStep(
            name="schema_generation",
            description="Attach or update structured data/schema markup for this cluster.",
            inputs=["geo_enriched_records"],
            outputs=["records_with_schema"],
            external_skills=["geo-schema-gen"],
        ),
        PipelineStep(
            name="export_for_implementation",
            description="Export final records into a format that can be imported into the CMS or delivery pipeline.",
            inputs=["records_with_schema"],
            outputs=["implementation_export"],
            external_skills=[],
        ),
    ]

    return PipelineDefinition(
        id=f"{cluster_name}-default-pipeline",
        cluster=cluster_name,
        description=(
            f"Default illustrative GEO bulk pipeline for the '{cluster_name}' cluster. "
            "Adapt steps, inputs, outputs, and external skills to the user’s actual systems."
        ),
        steps=steps,
    )


__all__ = [
    "ContentItem",
    "PipelineStep",
    "PipelineDefinition",
    "summarize_inventory",
    "example_pipeline_for_cluster",
]

