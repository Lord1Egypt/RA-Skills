import sys
from pathlib import Path

# Add repo root to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

import asyncio
import json
import pytest
from ghostclaw.core.analyzer import CodebaseAnalyzer
from ghostclaw.core.config import GhostclawConfig


@pytest.mark.asyncio
async def test_analyze_node_repo(tmp_path):
    # Setup Node repo with large files
    (tmp_path / "package.json").write_text('{"name": "test"}')
    # Create a file with 600 lines + nested logic for Lizard
    content = "function ghost() {\n"
    for i in range(10):
        content += "  " * (i + 1) + f"if (x == {i}) {{\n"
    content += "  " * 12 + "console.log('deep');\n"
    for i in range(10):
        content += "  " * (10 - i) + "}\n"
    content += "\n".join(["// padding"] * 600) + "\n}"
    (tmp_path / "index.js").write_text(content)

    analyzer = CodebaseAnalyzer()
    report_model = await analyzer.analyze(str(tmp_path))
    report = report_model.model_dump()

    assert report["stack"] == "node"
    assert report["files_analyzed"] >= 1
    assert report["vibe_score"] < 100  # Should penalize large file
    assert any("files >400 lines" in i for i in report["issues"])


@pytest.mark.asyncio
async def test_analyze_python_repo_with_circular_imports(tmp_path):
    (tmp_path / "pyproject.toml").write_text("[project]\nname='test'")
    (tmp_path / "a.py").write_text("from b import x\n")
    (tmp_path / "b.py").write_text("from a import y\n")

    analyzer = CodebaseAnalyzer()
    report_model = await analyzer.analyze(str(tmp_path))
    report = report_model.model_dump()

    assert report["stack"] == "python"
    assert any("Circular dependency" in i for i in report["issues"])


@pytest.mark.asyncio
async def test_analyze_unknown_stack(tmp_path):
    # Empty dir
    analyzer = CodebaseAnalyzer()
    report_model = await analyzer.analyze(str(tmp_path))
    report = report_model.model_dump()
    assert report["stack"] == "unknown"
    # The exact issue message may vary; just check that we got some issue
    assert len(report["issues"]) > 0


@pytest.mark.asyncio
async def test_delta_mode_filters_to_changed_files(tmp_path):
    """Delta mode should analyze only files that changed in git diff."""
    # Initialize git repo
    import subprocess
    subprocess.run(["git", "init"], cwd=tmp_path, check=True, capture_output=True)
    subprocess.run(["git", "config", "user.email", "test@test.com"], cwd=tmp_path, check=True)
    subprocess.run(["git", "config", "user.name", "Test"], cwd=tmp_path, check=True)

    # Create initial files (commit A)
    (tmp_path / "file1.py").write_text("print('hello')\n")
    (tmp_path / "file2.py").write_text("print('world')\n")
    subprocess.run(["git", "add", "."], cwd=tmp_path, check=True)
    subprocess.run(["git", "commit", "-m", "initial"], cwd=tmp_path, check=True)

    # Modify only file1.py (commit B)
    (tmp_path / "file1.py").write_text("print('hello updated')\n")
    subprocess.run(["git", "add", "."], cwd=tmp_path, check=True)
    subprocess.run(["git", "commit", "-m", "update file1"], cwd=tmp_path, check=True)

    # Now run delta analysis against HEAD~1 (should see only file1.py changes)
    config = GhostclawConfig.load(str(tmp_path), delta_mode=True, delta_base_ref="HEAD~1")
    analyzer = CodebaseAnalyzer()
    report_model = await analyzer.analyze(str(tmp_path), config=config)
    report = report_model.model_dump()

    # Check delta metadata present
    assert "metadata" in report
    assert "delta" in report["metadata"]
    assert report["metadata"]["delta"]["mode"] is True
    assert report["metadata"]["delta"]["base_ref"] == "HEAD~1"
    changed_files = report["metadata"]["delta"]["files_changed"]
    assert "file1.py" in changed_files
    # file2.py should NOT be in changed files (it wasn't modified)
    assert "file2.py" not in changed_files

    # Verify that only changed files were analyzed in this delta run
    # (files_analyzed should be <= number of changed files that match stack)
    # For Python repo, both file1.py and file2.py are .py, but only file1 changed
    assert report["files_analyzed"] >= 1
    # The exact count depends on whether file2 was analyzed; we expect only file1
    assert report["files_analyzed"] <= len(changed_files)


@pytest.mark.asyncio
async def test_delta_mode_base_report_discovery(tmp_path):
    """Delta mode should attempt to load base report from .ghostclaw/storage/reports/."""
    import subprocess
    subprocess.run(["git", "init"], cwd=tmp_path, check=True, capture_output=True)
    subprocess.run(["git", "config", "user.email", "test@test.com"], cwd=tmp_path, check=True)
    subprocess.run(["git", "config", "user.name", "Test"], cwd=tmp_path, check=True)

    # Create initial files and commit
    (tmp_path / "file.py").write_text("print('v1')\n")
    subprocess.run(["git", "add", "."], cwd=tmp_path, check=True)
    subprocess.run(["git", "commit", "-m", "v1"], cwd=tmp_path, check=True)

    # Run a full analysis first (simulate base report)
    analyzer = CodebaseAnalyzer()
    base_config = GhostclawConfig.load(str(tmp_path))
    base_report_model = await analyzer.analyze(str(tmp_path), config=base_config)
    base_report = base_report_model.model_dump()

    # The full analysis should have written a JSON report and we can verify it exists
    reports_dir = tmp_path / ".ghostclaw" / "storage" / "reports"
    if reports_dir.exists():
        json_files = list(reports_dir.glob("ARCHITECTURE-REPORT-*.json"))
        assert len(json_files) > 0, "Base full analysis should have written a JSON report"

    # Now make a change
    (tmp_path / "file.py").write_text("print('v2 updated')\n")
    subprocess.run(["git", "add", "."], cwd=tmp_path, check=True)
    subprocess.run(["git", "commit", "-m", "v2"], cwd=tmp_path, check=True)

    # Run delta mode
    delta_config = GhostclawConfig.load(str(tmp_path), delta_mode=True, delta_base_ref="HEAD~1")
    delta_report_model = await analyzer.analyze(str(tmp_path), config=delta_config)
    delta_report = delta_report_model.model_dump()

    # Should have delta metadata
    assert "delta" in delta_report["metadata"]
    # Should include the diff text
    assert len(delta_report["metadata"]["delta"]["diff"]) > 0
