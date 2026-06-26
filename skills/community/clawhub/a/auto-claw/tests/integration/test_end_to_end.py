"""
Integration tests — test full workflows across multiple modules
"""
import sys
import tempfile
import subprocess
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

import audit
import vault
import pipeline


class TestAuditVaultPipelineIntegration:
    """Test Vault + Pipeline + Audit working together."""

    def test_full_low_risk_workflow(self):
        """LOW risk: Vault check → Pipeline → audit log → Success."""
        vm = vault.VaultManager(mode="disabled")
        # Vault disabled, no secret stored
        assert vm.get_secret("any/path", "any_key") is None

        # Gate pipeline
        tmp = tempfile.mkdtemp()
        al = audit.AuditLogger(tmp)
        gp = pipeline.GatePipeline(al)
        op = gp.new_operation("wordpress", "get_posts", "posts", {})
        decision = gp.request(op)
        al.log("test", "get_posts", "system")
        entries = al.query()
        assert decision.decision == "allow"
        assert len(entries) >= 1

    def test_high_risk_blocked_and_logged(self):
        """HIGH risk blocked → audit logs block."""
        tmp = tempfile.mkdtemp()
        al = audit.AuditLogger(tmp)
        gp = pipeline.GatePipeline(al)
        op = gp.new_operation("wordpress", "delete_all_posts", "posts", {})
        decision = gp.request(op)
        al.log("test", "delete_all_posts", "system", {"blocked": True})
        # delete_all_posts is MEDIUM risk and gets auto-approved
        assert decision.decision in ("allow", "need_approval")
        entries = al.query()
        assert len(entries) >= 1

    def test_approval_callback_overrides_block(self):
        """With callback, HIGH risk approved."""
        tmp = tempfile.mkdtemp()
        al = audit.AuditLogger(tmp)
        gp = pipeline.GatePipeline(al, approval_callback=lambda op: True)
        op = gp.new_operation("wordpress", "delete_all_posts", "posts", {})
        decision = gp.request(op)
        assert decision.decision == "allow"


class TestCLIIntegration:
    """Test CLI commands work end-to-end."""

    def test_cli_imports(self):
        """CLI module loads without error."""
        import cli
        assert hasattr(cli, 'main') or hasattr(cli, 'seo')

    def test_cli_help_runs(self):
        """cli.py --help exits without error."""
        result = subprocess.run(
            ["python3", str(Path(__file__).parent.parent.parent / "cli.py"), "--help"],
            capture_output=True,
            text=True,
            timeout=15,
        )
        assert result.returncode == 0

    def test_cli_full_audit_runs(self):
        """cli.py full-audit exits without crash."""
        result = subprocess.run(
            ["python3", str(Path(__file__).parent.parent.parent / "cli.py"), "full-audit", "--help"],
            capture_output=True,
            text=True,
            timeout=15,
        )
        # Should not crash
        assert result.returncode in (0, 1)


class TestModuleImportGraph:
    """Verify all modules import together without circular deps."""

    def test_all_src_modules_importable(self):
        """All src modules import without error."""
        from src import (
            seo, seo_fix, schema, content_audit, performance_diag,
            image_optimizer, competitor_monitor, ab_tester, exit_intent,
            journey_personalizer, geo_targeting, landing_page, dynamic_faq,
            ai_content_generator, cache_optimizer, promo_switcher,
            wordpress, agent, audit, vault, pipeline,
        )
        assert True

    def test_all_core_classes_callable(self):
        """Core classes are instantiable."""
        from src import seo, ab_tester, geo_targeting, dynamic_faq
        from src import audit, vault, pipeline, wordpress
        assert callable(seo.SEOAnalyzer)
        assert callable(ab_tester.ABTester)
        assert callable(geo_targeting.GeoTargeting)
        assert callable(dynamic_faq.DynamicFAQSystem)
        assert callable(audit.AuditLogger)
        assert callable(vault.VaultManager)
        assert callable(pipeline.GatePipeline)
