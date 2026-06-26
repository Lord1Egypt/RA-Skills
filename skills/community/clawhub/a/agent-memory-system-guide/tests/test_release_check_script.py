from pathlib import Path
import os
import subprocess
import sys
import pytest


def test_release_check_script_passes_on_repo_state():
    if os.environ.get('AGENT_MEMORY_RELEASE_CHECK') == '1':
        pytest.skip('Avoid recursive invocation while check_release.py is already running pytest.')

    repo_root = Path(__file__).resolve().parents[1]
    result = subprocess.run(
        [sys.executable, str(repo_root / 'scripts' / 'check_release.py')],
        cwd=repo_root,
        text=True,
        capture_output=True,
        check=False,
    )

    assert result.returncode == 0
    assert 'Release checks passed.' in result.stdout
    assert 'pytest -q' in result.stdout
    assert 'Version:' in result.stdout
