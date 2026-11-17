"""Tests for generate_harness.py."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))
from generate_harness import main


def test_generate_harness_writes_file(tmp_path):
    agent = tmp_path / "fake_agent.py"
    agent.write_text("def build_agent(): pass\n", encoding="utf-8")
    out = tmp_path / "test_harness.py"
    main()
    # main uses sys.argv internally; call via script instead
    import subprocess
    subprocess.run([sys.executable, str(Path(__file__).parent.parent / "scripts" / "generate_harness.py"), "--agent", str(agent), "--output", str(out)], check=True)
    assert out.exists()
    assert "FakeModel" in out.read_text(encoding="utf-8")
