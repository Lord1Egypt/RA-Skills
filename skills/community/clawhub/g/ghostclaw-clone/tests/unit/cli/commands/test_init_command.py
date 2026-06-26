import pytest
import json
from pathlib import Path
from argparse import Namespace
from ghostclaw.cli.commands.init import InitCommand
from ghostclaw.cli.services import ConfigService

@pytest.mark.asyncio
async def test_init_command_execute(mocker, tmp_path):
    cmd = InitCommand()
    args = Namespace()

    mock_init_project = mocker.patch("ghostclaw.cli.commands.init.ConfigService.init_project")

    result = await cmd.execute(args)
    assert result == 0
    mock_init_project.assert_called_once_with(".")

@pytest.mark.asyncio
async def test_init_command_execute_failure(mocker, capsys):
    cmd = InitCommand()
    args = Namespace()

    mock_init_project = mocker.patch("ghostclaw.cli.commands.init.ConfigService.init_project")
    mock_init_project.side_effect = Exception("Failed")

    result = await cmd.execute(args)
    assert result == 1
    captured = capsys.readouterr()
    assert "Failed" in captured.err


@pytest.mark.asyncio
async def test_init_project_creates_config_with_delta_fields(tmp_path):
    """Test that ghostclaw init creates a config file containing delta_mode and delta_base_ref."""
    ConfigService.init_project(str(tmp_path))

    config_file = tmp_path / ".ghostclaw" / "ghostclaw.json"
    assert config_file.exists()

    with open(config_file, "r", encoding="utf-8") as f:
        config = json.load(f)

    # Check all expected keys exist (including delta fields)
    expected_keys = [
        "use_ai", "ai_provider", "ai_model", "use_pyscn", "use_ai_codeindex",
        "delta_mode", "delta_base_ref"
    ]
    for key in expected_keys:
        assert key in config, f"Missing key: {key}"

    # Check delta defaults
    assert config["delta_mode"] is False
    assert config["delta_base_ref"] == "HEAD~1"
