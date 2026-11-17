"""
LLM-Wiki Zotero Subsystem

Layered architecture:
- Backends & MCP: local, mcp_client
- Providers & Cache: providers, cache
- Domain Services: plan, refresh, relocate, heal, ingest_verify, writeback
"""

from .cache import EnrichmentCache
from .heal import apply_heal_plan, match_stale_binding, plan_heal, plan_to_heal_manifest
from .ingest_verify import (
    IngestVerificationError,
    IngestVerificationReport,
    ingest_report_to_manifest,
    load_allocation_ledger,
    verify_collection_ingest,
)
from .local import LocalZoteroWriter, authorize_local
from .mcp_client import ZoteroMCPClient
from .plan import (
    SnapshotItem,
    ZoteroBinding,
    ZoteroPlan,
    build_retired_binding_removal_plan,
    build_zotero_plan,
    collect_zotero_bindings,
    load_snapshot,
    normalize_doi,
    plan_to_manifest,
)
from .providers import CrossrefProvider, OpenAlexProvider
from .refresh import (
    RefreshItem,
    RefreshMutation,
    RefreshReport,
    RefreshSettings,
    build_refresh_report,
    parse_extra_keys,
    run_live_refresh,
)
from .refresh import (
    report_to_manifest as refresh_report_to_manifest,
)
from .refresh import (
    settings_from_config as refresh_settings_from_config,
)
from .relocate import relocate
from .writeback import apply_write_plan, audit_write_plan, verify_write_plan

__all__ = [
    "CrossrefProvider",
    "EnrichmentCache",
    "IngestVerificationError",
    "IngestVerificationReport",
    "LocalZoteroWriter",
    "OpenAlexProvider",
    "RefreshItem",
    "RefreshMutation",
    "RefreshReport",
    "RefreshSettings",
    "SnapshotItem",
    "ZoteroBinding",
    "ZoteroMCPClient",
    "ZoteroPlan",
    "apply_heal_plan",
    "apply_write_plan",
    "audit_write_plan",
    "authorize_local",
    "build_refresh_report",
    "build_retired_binding_removal_plan",
    "build_zotero_plan",
    "collect_zotero_bindings",
    "ingest_report_to_manifest",
    "load_allocation_ledger",
    "load_snapshot",
    "match_stale_binding",
    "normalize_doi",
    "parse_extra_keys",
    "plan_heal",
    "plan_to_heal_manifest",
    "plan_to_manifest",
    "refresh_report_to_manifest",
    "refresh_settings_from_config",
    "relocate",
    "run_live_refresh",
    "verify_collection_ingest",
    "verify_write_plan",
]
