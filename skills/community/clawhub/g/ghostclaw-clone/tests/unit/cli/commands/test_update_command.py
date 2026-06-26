import pytest
from argparse import Namespace
from ghostclaw.cli.commands.update import UpdateCommand
import subprocess

@pytest.mark.asyncio
async def test_update_command_execute_git(mocker):
    cmd = UpdateCommand()
    args = Namespace()

    mock_run = mocker.patch("ghostclaw.cli.commands.update.subprocess.run")
    mock_run.return_value = mocker.MagicMock(returncode=0)

    result = await cmd.execute(args)
    assert result == 0
    assert mock_run.call_count == 3

@pytest.mark.asyncio
async def test_update_command_execute_pip(mocker):
    cmd = UpdateCommand()
    args = Namespace()

    mock_run = mocker.patch("ghostclaw.cli.commands.update.subprocess.run")
    mock_run.side_effect = [subprocess.CalledProcessError(1, "git"), mocker.MagicMock(returncode=0)]

    result = await cmd.execute(args)
    assert result == 0
    assert mock_run.call_count == 2
