import pytest
from argparse import Namespace
from ghostclaw.cli.commands.bridge import BridgeCommand

@pytest.mark.asyncio
async def test_bridge_command_execute(mocker):
    cmd = BridgeCommand()
    args = Namespace(verbose=False)

    mock_bridge = mocker.patch("ghostclaw.cli.commands.bridge.GhostBridge")
    mock_instance = mock_bridge.return_value
    mock_instance.run = mocker.AsyncMock()

    result = await cmd.execute(args)
    assert result == 0
    mock_instance.run.assert_called_once()

@pytest.mark.asyncio
async def test_bridge_command_keyboard_interrupt(mocker):
    cmd = BridgeCommand()
    args = Namespace(verbose=False)

    mock_bridge = mocker.patch("ghostclaw.cli.commands.bridge.GhostBridge")
    mock_instance = mock_bridge.return_value
    mock_instance.run.side_effect = KeyboardInterrupt

    result = await cmd.execute(args)
    assert result == 130
