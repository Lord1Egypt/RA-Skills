from __future__ import annotations

import unittest

from axiotic_experiments.spec import ExperimentSpec, SpecError

from .fixtures import spec_mapping


class ExperimentSpecTests(unittest.TestCase):
    def test_loads_portable_spec_and_metadata(self) -> None:
        spec = ExperimentSpec.from_mapping(spec_mapping())

        self.assertEqual(spec.run.id, "phase-model_seed0")
        self.assertEqual(spec.run.tags[-1], "seed:0")
        self.assertEqual(
            spec.source.commit_url,
            "https://github.com/org/repo/commit/0123456789abcdef0123456789abcdef01234567",
        )
        self.assertEqual(spec.core_manifest()["wandb"]["resume"], "allow")

    def test_parses_butler_reservation_dimensions(self) -> None:
        raw = spec_mapping()
        raw["resources"].update(
            {"estimated_cost": 24.5, "currency": "gbp", "disk_gb": 200}
        )
        spec = ExperimentSpec.from_mapping(raw)

        self.assertEqual(spec.resources.estimated_cost, 24.5)
        self.assertEqual(spec.resources.currency, "GBP")
        self.assertEqual(spec.resources.disk_gb, 200)
        self.assertEqual(spec.core_manifest()["resources"]["disk_gb"], 200)

    def test_rejects_offline_wandb(self) -> None:
        raw = spec_mapping()
        raw["wandb"]["mode"] = "offline"

        with self.assertRaisesRegex(SpecError, "must be online"):
            ExperimentSpec.from_mapping(raw)

    def test_rejects_secret_key_in_public_env(self) -> None:
        raw = spec_mapping()
        raw["execution"]["env"] = {"SERVICE_API_KEY": "not-even-a-real-token"}

        with self.assertRaisesRegex(SpecError, "credential-like key"):
            ExperimentSpec.from_mapping(raw)

    def test_rejects_secret_value_in_public_env(self) -> None:
        raw = spec_mapping()
        raw["execution"]["env"] = {"PUBLIC": "hf_" + ("x" * 24)}

        with self.assertRaisesRegex(SpecError, "credential-like material"):
            ExperimentSpec.from_mapping(raw)

    def test_runpod_requires_provider_section(self) -> None:
        raw = spec_mapping(machine="runpod")
        del raw["runpod"]

        with self.assertRaisesRegex(SpecError, "requires a \\[runpod\\] section"):
            ExperimentSpec.from_mapping(raw)

    def test_parses_runpod_adapter_fields(self) -> None:
        spec = ExperimentSpec.from_mapping(spec_mapping(machine="runpod"))

        self.assertEqual(spec.resources.gpus, 1)
        self.assertEqual(spec.runpod.cloud_type, "SECURE")
        self.assertEqual(spec.runpod.max_cost_usd, 10)


if __name__ == "__main__":
    unittest.main()
