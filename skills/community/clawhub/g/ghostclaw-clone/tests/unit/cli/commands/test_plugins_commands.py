import pytest
from argparse import Namespace
from pathlib import Path
from ghostclaw.cli.commands.plugins.list import PluginsListCommand
from ghostclaw.cli.commands.plugins.add import PluginsAddCommand
from ghostclaw.cli.commands.plugins.remove import PluginsRemoveCommand
from ghostclaw.cli.commands.plugins.info import PluginsInfoCommand
from ghostclaw.cli.commands.plugins.enable import PluginsEnableCommand
from ghostclaw.cli.commands.plugins.disable import PluginsDisableCommand
from ghostclaw.cli.commands.plugins.test import PluginsTestCommand
from ghostclaw.cli.commands.plugins.scaffold import PluginsScaffoldCommand

@pytest.mark.asyncio
async def test_plugins_list_command(mocker, capsys):
    mock_service = mocker.patch("ghostclaw.cli.commands.plugins.base.PluginService")
    mock_instance = mock_service.return_value
    mock_instance.list_plugins.return_value = [{"name": "test-plugin", "version": "1.0", "description": "A test plugin"}]

    cmd = PluginsListCommand()
    args = Namespace()
    result = await cmd.execute(args)

    assert result == 0
    captured = capsys.readouterr()
    assert "test-plugin" in captured.out

@pytest.mark.asyncio
async def test_plugins_add_command(mocker):
    mock_service = mocker.patch("ghostclaw.cli.commands.plugins.base.PluginService")
    mock_instance = mock_service.return_value
    mock_instance.add_plugin.return_value = "target_path"

    cmd = PluginsAddCommand()
    args = Namespace(source="source_path")
    result = await cmd.execute(args)
    assert result == 0

@pytest.mark.asyncio
async def test_plugins_remove_command(mocker):
    mock_service = mocker.patch("ghostclaw.cli.commands.plugins.base.PluginService")
    mock_instance = mock_service.return_value
    mock_instance.remove_plugin.return_value = "target_path"

    cmd = PluginsRemoveCommand()
    args = Namespace(name="test-plugin")
    result = await cmd.execute(args)
    assert result == 0

@pytest.mark.asyncio
async def test_plugins_info_command(mocker, capsys):
    mock_service = mocker.patch("ghostclaw.cli.commands.plugins.base.PluginService")
    mock_instance = mock_service.return_value
    mock_instance.get_plugin_info.return_value = {"name": "test-plugin", "version": "1.0", "description": "A test plugin"}

    cmd = PluginsInfoCommand()
    args = Namespace(name="test-plugin")
    result = await cmd.execute(args)
    assert result == 0
    captured = capsys.readouterr()
    assert "Plugin: test-plugin" in captured.out

@pytest.mark.asyncio
async def test_plugins_enable_command(mocker):
    mock_service = mocker.patch("ghostclaw.cli.commands.plugins.base.PluginService")
    mock_instance = mock_service.return_value

    cmd = PluginsEnableCommand()
    args = Namespace(name="test-plugin")
    result = await cmd.execute(args)
    assert result == 0

@pytest.mark.asyncio
async def test_plugins_disable_command(mocker):
    mock_service = mocker.patch("ghostclaw.cli.commands.plugins.base.PluginService")
    mock_instance = mock_service.return_value

    cmd = PluginsDisableCommand()
    args = Namespace(name="test-plugin")
    result = await cmd.execute(args)
    assert result == 0

@pytest.mark.asyncio
async def test_plugins_test_command(mocker, capsys):
    mock_service = mocker.patch("ghostclaw.cli.commands.plugins.base.PluginService")
    mock_instance = mock_service.return_value
    mock_instance.test_plugin.return_value = True

    cmd = PluginsTestCommand()
    args = Namespace(name="test-plugin")
    result = await cmd.execute(args)
    assert result == 0
    captured = capsys.readouterr()
    assert "✅ Plugin 'test-plugin' is registered." in captured.out

@pytest.mark.asyncio
async def test_plugins_scaffold_command(mocker):
    mock_service = mocker.patch("ghostclaw.cli.commands.plugins.base.PluginService")
    mock_instance = mock_service.return_value
    mock_instance.scaffold_plugin.return_value = Path("target_path")

    cmd = PluginsScaffoldCommand()
    args = Namespace(name="new-plugin")
    result = await cmd.execute(args)
    assert result == 0
