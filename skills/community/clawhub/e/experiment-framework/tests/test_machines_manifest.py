from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from axiotic_experiments.machines import MachineRegistry
from axiotic_experiments.manifest import (
    ArtifactNode,
    ProvenanceGraph,
    validate_sealed_graph,
)
from axiotic_experiments.provenance import build_graph
from axiotic_experiments.spec import ExperimentSpec

from .fixtures import spec_mapping


class MachineRegistryTests(unittest.TestCase):
    def test_alias_resolves_to_canonical_machine(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "machines.toml"
            path.write_text(
                """
[machines.worker2]
transport = "ssh"
target = "worker-two"
workspace_root = "~/Work/repos"
aliases = ["worker-two"]
"""
            )
            registry = MachineRegistry.load(path)

        self.assertEqual(registry.resolve("worker-two").name, "worker2")
        self.assertEqual(
            registry.resolve("worker2").source_path_text("project"),
            "~/Work/repos/project",
        )


class ManifestTests(unittest.TestCase):
    def test_sealed_graph_links_every_peer(self) -> None:
        graph = ProvenanceGraph("run")
        graph.add(ArtifactNode("a", "one", "one://a"))
        graph.add(ArtifactNode("b", "two", "two://b"))
        graph.add(ArtifactNode("c", "three", "three://c"))

        sealed = graph.seal()
        validate_sealed_graph(sealed)

        self.assertEqual(len(sealed["nodes"]), 3)
        self.assertTrue(all(len(node["links"]) == 2 for node in sealed["nodes"]))

    def test_default_graph_has_eight_nodes_and_seven_links_each(self) -> None:
        spec = ExperimentSpec.from_mapping(spec_mapping())
        with tempfile.TemporaryDirectory() as directory:
            machines = Path(directory) / "machines.toml"
            machines.write_text(
                """
[machines.local]
transport = "local"
workspace_root = "/tmp"
"""
            )
            profile = MachineRegistry.load(machines).resolve("local")

        sealed = build_graph(spec, profile, core_sha256="abc").seal()
        validate_sealed_graph(sealed)

        self.assertEqual(len(sealed["nodes"]), 8)
        self.assertTrue(all(len(node["links"]) == 7 for node in sealed["nodes"]))

    def test_validation_rejects_missing_peer_link(self) -> None:
        graph = ProvenanceGraph("run")
        graph.add(ArtifactNode("a", "one", "one://a"))
        graph.add(ArtifactNode("b", "two", "two://b"))
        sealed = graph.seal()
        sealed["nodes"][0]["links"] = {}

        with self.assertRaisesRegex(ValueError, "complete peer map"):
            validate_sealed_graph(sealed)


if __name__ == "__main__":
    unittest.main()
