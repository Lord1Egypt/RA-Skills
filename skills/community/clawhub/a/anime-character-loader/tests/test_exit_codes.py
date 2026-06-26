from anime_character_loader.errors import ExitCode


def test_exit_codes_are_stable():
    assert ExitCode.SUCCESS == 0
    assert ExitCode.NETWORK_ERROR == 10
    assert ExitCode.DATA_ERROR == 20
    assert ExitCode.VALIDATION_ERROR == 30
    assert ExitCode.FILE_ERROR == 40
