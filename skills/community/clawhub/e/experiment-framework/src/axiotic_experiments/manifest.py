from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


def canonical_bytes(value: Any) -> bytes:
    return json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
    ).encode("utf-8")


def sha256_json(value: Any) -> str:
    return hashlib.sha256(canonical_bytes(value)).hexdigest()


@dataclass(frozen=True)
class ArtifactNode:
    id: str
    kind: str
    uri: str
    sha256: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)


class ProvenanceGraph:
    def __init__(self, run_id: str, core_sha256: str | None = None):
        self.run_id = run_id
        self.core_sha256 = core_sha256
        self._nodes: dict[str, ArtifactNode] = {}

    def add(self, node: ArtifactNode) -> None:
        if not node.id or not node.uri:
            raise ValueError("artifact nodes require non-empty id and uri")
        if node.id in self._nodes:
            raise ValueError(f"duplicate artifact node id: {node.id}")
        self._nodes[node.id] = node

    def upsert(self, node: ArtifactNode) -> None:
        if not node.id or not node.uri:
            raise ValueError("artifact nodes require non-empty id and uri")
        self._nodes[node.id] = node

    def seal(self) -> dict[str, Any]:
        nodes = []
        for node_id in sorted(self._nodes):
            node = self._nodes[node_id]
            links = {
                peer_id: self._nodes[peer_id].uri
                for peer_id in sorted(self._nodes)
                if peer_id != node_id
            }
            nodes.append(
                {
                    "id": node.id,
                    "kind": node.kind,
                    "uri": node.uri,
                    "sha256": node.sha256,
                    "metadata": node.metadata,
                    "links": links,
                }
            )
        return {
            "schema_version": "1.0",
            "run_id": self.run_id,
            "core_sha256": self.core_sha256,
            "connectivity": "complete-directed-graph",
            "nodes": nodes,
        }


@dataclass(frozen=True)
class BundleHashes:
    core_sha256: str
    index_sha256: str


def validate_sealed_graph(index: dict[str, Any]) -> None:
    nodes = index.get("nodes")
    if not isinstance(nodes, list) or not nodes:
        raise ValueError("artifact graph requires at least one node")
    by_id: dict[str, dict[str, Any]] = {}
    for node in nodes:
        if not isinstance(node, dict) or not isinstance(node.get("id"), str):
            raise TypeError("artifact graph contains an invalid node")
        if node["id"] in by_id:
            raise ValueError(f"duplicate artifact node id: {node['id']}")
        by_id[node["id"]] = node
    all_ids = set(by_id)
    for node_id, node in by_id.items():
        links = node.get("links")
        expected = all_ids - {node_id}
        if not isinstance(links, dict) or set(links) != expected:
            raise ValueError(
                f"artifact node {node_id!r} does not contain a complete peer map"
            )
        for peer_id, uri in links.items():
            if uri != by_id[peer_id].get("uri"):
                raise ValueError(
                    f"artifact node {node_id!r} has a stale URI for peer {peer_id!r}"
                )


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(canonical_bytes(value) + b"\n")


def write_bundle(
    directory: Path,
    core: dict[str, Any],
    graph: ProvenanceGraph,
    *,
    launch_plan: dict[str, Any],
) -> BundleHashes:
    directory.mkdir(parents=True, exist_ok=True)
    core_sha = sha256_json(core)
    graph.core_sha256 = core_sha
    index = graph.seal()
    validate_sealed_graph(index)
    index_sha = sha256_json(index)
    write_json(directory / "run-core.json", core)
    write_json(directory / "artifact-index.json", index)
    write_json(directory / "launch-plan.json", launch_plan)
    (directory / "metrics.jsonl").touch(exist_ok=True)
    return BundleHashes(core_sha256=core_sha, index_sha256=index_sha)
