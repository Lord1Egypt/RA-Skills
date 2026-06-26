import pytest
from argparse import Namespace
from ghostclaw.cli.commands.test import TestCommand

@pytest.mark.asyncio
async def test_test_command_execute_llm(mocker):
    cmd = TestCommand()
    args = Namespace(llm=True, ai_provider=None, ai_model=None)

    mock_config_load = mocker.patch("ghostclaw.cli.commands.test.GhostclawConfig.load")
    mock_config = mock_config_load.return_value
    mock_config.ai_provider = "dummy"

    mock_client_cls = mocker.patch("ghostclaw.cli.commands.test.LLMClient")
    mock_client = mock_client_cls.return_value
    mock_client.test_connection = mocker.AsyncMock(return_value=True)
    mock_client.list_models = mocker.AsyncMock(return_value=["dummy_model"])

    result = await cmd.execute(args)
    assert result == 0

@pytest.mark.asyncio
async def test_test_command_execute_help(capsys):
    cmd = TestCommand()
    args = Namespace(llm=False, ai_provider=None, ai_model=None)

    result = await cmd.execute(args)
    assert result == 1
    captured = capsys.readouterr()
    assert "Usage: ghostclaw test --llm" in captured.err
