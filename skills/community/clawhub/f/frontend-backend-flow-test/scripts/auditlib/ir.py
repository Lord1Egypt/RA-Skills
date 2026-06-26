from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Optional


@dataclass
class RequestHints:
    path_params: List[str] = field(default_factory=list)
    query_params: List[str] = field(default_factory=list)
    body_kind: Optional[str] = None
    body_keys: List[str] = field(default_factory=list)
    response_keys: List[str] = field(default_factory=list)
    auth: List[str] = field(default_factory=list)
    consumes: Optional[str] = None


@dataclass
class EndpointIR:
    side: str
    method: str
    path: str
    raw_path: str
    file: str
    line: int
    source: str
    locator: str
    framework: str
    ambiguous: bool = False
    confidence: str = 'high'
    hints: RequestHints = field(default_factory=RequestHints)


@dataclass
class Finding:
    id: str
    category: str
    severity: str
    summary: str
    frontend_source: Optional[Dict]
    backend_source: Optional[Dict]
    evidence: Dict[str, object]
    recommendation: str


def hints_to_dict(hints: RequestHints) -> Dict[str, object]:
    return {
        'path_params': hints.path_params,
        'query_params': hints.query_params,
        'body_kind': hints.body_kind,
        'body_keys': hints.body_keys,
        'response_keys': hints.response_keys,
        'auth': hints.auth,
        'consumes': hints.consumes,
    }
