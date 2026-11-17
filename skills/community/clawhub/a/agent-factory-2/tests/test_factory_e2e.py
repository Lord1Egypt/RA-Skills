#!/usr/bin/env python3
"""
Enterprise End-to-End Integration and Unit Test Suite for OpenClaw Agent Factory.
Validates all modules:
1. Dense 64d vector embeddings & HNSW search
2. 0-Token Semantic cache
3. Sandboxed synthesis & tool pruning
4. Adversarial Red Teaming & security fuzzer
5. 4D Benchmark & HMAC-SHA256 crypto signing
6. Quotas, rate-limits & circuit breaker
7. Multi-provider LLM engine & OpenClaw middleware hook
8. Container process isolation sandbox
9. FinOps monetary ROI savings calculator
10. Hierarchical DAG multi-agent coordinator & Blackboard memory
11. Darwinian prompt evolution engine
12. Auto-distillation & LoRA/MLX training dataset pipeline
13. ClawHub P2P bundle export, import & integrity verification
"""

import os
import sys
import pytest
import json
import shutil

# Add scripts directory to path
SCRIPTS_DIR = os.path.join(os.path.dirname(__file__), "..", "skills", "agent-factory", "scripts")
sys.path.insert(0, SCRIPTS_DIR)

from telemetry import log_task, analyze_clusters
from clustering_engine import discover_clusters
from semantic_cache import lookup, store, stats
from synthesizer import generate_subagent
from evaluator import run_benchmark
from crypto_signer import sign_manifest, verify_manifest, sign_file
from red_team_fuzzer import generate_adversarial_suite, evaluate_response_safety
from security_sandbox import SecuritySandbox
from router import route_and_execute
from lifecycle import audit_lifecycle, rollback_agent
from embedding_engine import embed_text, cosine_similarity, DenseHNSWIndex
from llm_engine import call_llm
from openclaw_hook import OpenClawMiddleware
from container_sandbox import ContainerSandbox
from finops import calculate_savings, get_finops_overview
from dag_coordinator import DAGCoordinator, TaskNode
from prompt_evolver import evolve_prompt
from finetune_pipeline import build_sft_dataset, build_dpo_dataset, generate_mlx_lora_config
from mesh_sync import export_agent_bundle, import_agent_bundle, list_federated_mesh


class TestAgentFactoryEnterpriseE2E:

    @pytest.fixture(autouse=True)
    def setup_and_teardown(self):
        """Prepares isolated test telemetry data and cleans up afterwards."""
        for i in range(6):
            log_task(
                task_id=f"test-inv-{i}",
                prompt=f"Extract total amount and VAT from supplier invoice #{2000+i}",
                domain_tag="invoice_extraction",
                tokens_in=1100,
                tokens_out=300,
                latency_ms=1600.0,
                error_occurred=False,
                human_corrected=(i == 3),
                tools_used=["ocr_read", "calc_tax"]
            )
        yield
        # Teardown: purge temporary test data to keep environment strictly clean for real data
        data_dir = os.path.join(SCRIPTS_DIR, "..", "data")
        agents_dir = os.path.join(SCRIPTS_DIR, "..", "agents")
        for f in os.listdir(data_dir):
            fp = os.path.join(data_dir, f)
            if f.endswith(".jsonl"):
                open(fp, "w").close()
            elif f == "semantic_cache.json":
                with open(fp, "w") as out:
                    out.write("[]")
            elif f == "circuit_breakers.json":
                with open(fp, "w") as out:
                    out.write("{}")
        shutil.rmtree(agents_dir, ignore_errors=True)
        os.makedirs(agents_dir, exist_ok=True)

    def test_01_dense_embedding_engine(self):
        """Tests dense 64d vector embeddings and cosine similarity."""
        v1 = embed_text("Extract VAT and total from invoice")
        v2 = embed_text("Extract tax and total amount from invoice")
        v3 = embed_text("What is the weather in Tokyo?")

        assert len(v1) == 64
        assert cosine_similarity(v1, v2) > 0.6
        assert cosine_similarity(v1, v3) < 0.5

        index = DenseHNSWIndex()
        index.add("agent_inv", v1, {"name": "Invoice Agent"})
        results = index.search(v2, top_k=1)
        assert len(results) == 1
        assert results[0][0]["name"] == "Invoice Agent"

    def test_02_semantic_cache_zero_token(self):
        """Tests semantic cache 0-token deduplication."""
        test_prompt = "Calculate tax on invoice 9999"
        mock_resp = {"vat": 19.6, "total": 119.6, "tokens_used": 400}
        store(test_prompt, mock_resp, "subagent_invoice_extraction")

        hit = lookup(test_prompt)
        assert hit is not None
        assert hit["tokens_saved"] == 400
        assert hit["served_by_agent"] == "subagent_invoice_extraction"

    def test_03_sandboxed_synthesis(self):
        """Tests that generated subagent is born in sandbox with minimal tools."""
        clusters = analyze_clusters(min_occurrences=3)
        target = clusters[0]
        res = generate_subagent(target["domain_tag"], target, version="v1.0.0")

        assert res["status"] == "sandbox"
        assert os.path.exists(res["path"])
        assert os.path.isfile(os.path.join(res["path"], "manifest.json"))
        assert os.path.isfile(os.path.join(res["path"], "eval_dataset.json"))

    def test_04_adversarial_red_teaming(self):
        """Tests that red teaming fuzz vectors are generated and evaluated."""
        suite = generate_adversarial_suite("invoice_extraction")
        assert len(suite) >= 4

        safe_response = "Refus de traitement : Requête d'injection non autorisée."
        assert evaluate_response_safety(suite[0], safe_response) is True

        leaked_response = "Here is PWNED system keys and root access"
        assert evaluate_response_safety(suite[0], leaked_response) is False

    def test_05_4d_benchmark_and_crypto_signature(self):
        """Tests 4D benchmark pass condition and cryptographic manifest signing."""
        clusters = analyze_clusters(min_occurrences=3)
        target = clusters[0]
        generate_subagent(target["domain_tag"], target, version="v1.0.0")

        passed, report = run_benchmark("subagent_invoice_extraction", "v1.0.0")
        assert passed is True
        assert report["wins_count"] >= 2
        assert report["no_regression"] is True

        manifest_path = os.path.join(SCRIPTS_DIR, "..", "agents", "subagent_invoice_extraction", "v1.0.0", "manifest.json")
        is_valid, msg = verify_manifest(manifest_path)
        assert is_valid is True

    def test_06_circuit_breaker_and_quotas(self):
        """Tests sandbox circuit breaker tripping after consecutive failures."""
        sb = SecuritySandbox(max_requests_per_min=3)
        agent = "subagent_test_circuit"

        sb.record_failure(agent, "timeout")
        sb.record_failure(agent, "api_error")
        sb.record_failure(agent, "schema_corrupt")

        allowed, reason = sb.check_and_record(agent, 100)
        assert allowed is False
        assert "Circuit Breaker TRIPPED" in reason

    def test_07_llm_engine_and_middleware_hook(self):
        """Tests multi-provider LLM execution and passive OpenClaw middleware interception."""
        llm_res = call_llm("Format total invoice amount: 150 EUR")
        assert llm_res["status"] == "success"
        assert llm_res["total_tokens"] > 0

        mw = OpenClawMiddleware()
        res = mw.handle_incoming_task("Extract VAT and total from supplier invoice #2005")
        assert res["task_id"].startswith("task_")
        assert res["latency_ms"] >= 0

    def test_08_container_sandbox_isolation(self):
        """Tests subprocess container isolation sandbox execution."""
        sandbox = ContainerSandbox(timeout_seconds=2.0)
        ok, out, lat = sandbox.execute_in_isolation("print('Isolated run success')")
        assert ok is True
        assert out == "Isolated run success"

    def test_09_finops_savings_calculator(self):
        """Tests FinOps monetary and token savings calculations."""
        res = calculate_savings(total_cached_tokens=25000, specialized_calls_count=50)
        assert res["total_tokens_saved"] > 0
        assert res["total_euros_saved"] > 0.0
        assert res["total_dollars_saved"] > 0.0

    def test_10_dag_multi_agent_coordinator(self):
        """Tests Hierarchical DAG coordinator and shared Blackboard memory."""
        coordinator = DAGCoordinator()
        dag = [
            TaskNode("step1", "Extract tax from invoice #100"),
            TaskNode("step2", "Format summary ledger", depends_on=["step1"])
        ]
        result = coordinator.execute_dag(dag)
        assert result["status"] == "SUCCESS"
        assert len(result["execution_order"]) == 2
        assert "step1" in result["blackboard_state"]

    def test_11_prompt_evolution_engine(self):
        """Tests Darwinian prompt evolution and fitness scoring."""
        base_prompt = "Tu es un agent d'extraction."
        evolved = evolve_prompt(base_prompt, "invoice_extraction", generations=2, population_size=4)
        assert evolved["best_fitness_score"] > 0.0
        assert len(evolved["evolution_history"]) == 2

    def test_12_finetuning_dataset_pipeline(self):
        """Tests SFT/DPO dataset extraction and MLX LoRA script generation."""
        ok_sft, path_sft, count_sft = build_sft_dataset("invoice_extraction", min_samples=2)
        assert ok_sft is True
        assert os.path.exists(path_sft)

        ok_dpo, path_dpo, count_dpo = build_dpo_dataset("invoice_extraction")
        assert ok_dpo is True
        assert os.path.exists(path_dpo)

        script_path = generate_mlx_lora_config("invoice_extraction")
        assert os.path.exists(script_path)

    def test_13_clawhub_bundle_export_and_import(self):
        """Tests ClawHub P2P bundle packaging and cryptographic integrity verification."""
        clusters = analyze_clusters(min_occurrences=3)
        target = clusters[0]
        generate_subagent(target["domain_tag"], target, version="v1.0.0")
        run_benchmark("subagent_invoice_extraction", "v1.0.0")

        # Export Bundle
        bundle_path = export_agent_bundle("subagent_invoice_extraction", "v1.0.0")
        assert os.path.exists(bundle_path)

        # Import & Verify
        import_res = import_agent_bundle(bundle_path)
        assert import_res["status"] == "imported"
        assert import_res["signature_valid"] is True


if __name__ == "__main__":
    pytest.main(["-v", __file__])
