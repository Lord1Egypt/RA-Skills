import pytest
from argparse import Namespace
from ghostclaw.cli.commands.doctor import DoctorCommand

@pytest.mark.asyncio
async def test_doctor_command_execute(mocker, tmp_path):
    cmd = DoctorCommand()
    args = Namespace(ai_provider=None, ai_model=None)

    mock_config_load = mocker.patch("ghostclaw.cli.commands.doctor.GhostclawConfig.load")
    mock_config = mock_config_load.return_value
    mock_config.api_key = "dummy"
    mock_config.ai_provider = "dummy"

    mock_client_cls = mocker.patch("ghostclaw.cli.commands.doctor.LLMClient")
    mock_client = mock_client_cls.return_value
    mock_client.test_connection = mocker.AsyncMock(return_value=True)
    mock_client.model = "dummy_model"

    import os
    original_cwd = os.getcwd()
    os.chdir(tmp_path)

    try:
        result = await cmd.execute(args)
        assert result == 0
    finally:
        os.chdir(original_cwd)
