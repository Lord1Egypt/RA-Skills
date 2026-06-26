import pytest
from argparse import Namespace
from ghostclaw.cli.commands.analyze import AnalyzeCommand

@pytest.mark.asyncio
async def test_analyze_command_execute(mocker, tmp_path):
    repo_path = tmp_path / "test_repo"
    repo_path.mkdir()

    mock_service = mocker.patch("ghostclaw.cli.commands.analyze.AnalyzerService")
    mock_instance = mock_service.return_value
    mock_instance.run = mocker.AsyncMock(return_value={
        "vibe_score": 85,
        "stack": "Python",
        "files_analyzed": 10,
        "total_lines": 500,
        "metadata": {
            "timestamp": "2023-10-27T10:00:00Z",
            "delta": {"mode": False}  # Simulate non-delta report
        },
        "issues": [],
        "architectural_ghosts": [],
        "red_flags": []
    })

    cmd = AnalyzeCommand()
    args = Namespace(
        repo_path=str(repo_path),
        json=True,
        no_write_report=True,
        create_pr=False,
        no_cache=True,
        use_ai=False,
        no_ai=True,
        ai_provider=None,
        ai_model=None,
        dry_run=False,
        verbose=False,
        patch=False,
        pyscn=False,
        no_pyscn=True,
        ai_codeindex=False,
        no_ai_codeindex=True,
        # Orchestrator flags (new)
        orchestrate=False,
        no_orchestrate=False,
        no_parallel=True,
        concurrency_limit=None,
        strict=False,
        benchmark=False,
        cache_dir=None,
        cache_ttl=7,
        cache_stats=False,
        # Delta mode flags (v0.1.10)
        delta=False,
        delta_base_ref="HEAD~1",
        # QMD backend (v0.2.0)
        use_qmd=False,
        embedding_backend=None
    )

    result = await cmd.execute(args)
    assert result == 0

@pytest.mark.asyncio
async def test_analyze_command_invalid_path():
    cmd = AnalyzeCommand()
    args = Namespace(
        repo_path="invalid_path",
        delta=False,
        delta_base_ref="HEAD~1",
        # Add all expected flags to avoid attribute errors during validation
        orchestrate=False,
        no_orchestrate=False,
        use_qmd=False,
        embedding_backend=None,
        no_cache=True,
        use_ai=False,
        no_ai=True,
        ai_provider=None,
        ai_model=None,
        dry_run=False,
        verbose=False,
        patch=False,
        pyscn=False,
        no_pyscn=True,
        ai_codeindex=False,
        no_ai_codeindex=True,
        no_parallel=True,
        concurrency_limit=None,
        strict=False,
        benchmark=False,
        cache_dir=None,
        cache_ttl=7,
        cache_stats=False
    )
    with pytest.raises(SystemExit):
        await cmd.execute(args)
