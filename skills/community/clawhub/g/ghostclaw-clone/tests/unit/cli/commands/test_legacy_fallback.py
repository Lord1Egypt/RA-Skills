import pytest
import sys
import argparse
from unittest.mock import patch
from ghostclaw.cli.ghostclaw import main

def test_legacy_fallback(mocker, capsys):
    test_args = ["ghostclaw.py", "invalid_command"]
    with patch.object(sys, 'argv', test_args):
        mock_exit = mocker.patch("ghostclaw.cli.ghostclaw.sys.exit")

        main()

        captured = capsys.readouterr()
        assert "Warning: Using legacy CLI mode..." in captured.err
        mock_exit.assert_called_with(1)
