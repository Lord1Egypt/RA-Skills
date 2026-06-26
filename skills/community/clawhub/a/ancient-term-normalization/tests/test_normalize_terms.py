import json
import subprocess
from pathlib import Path


def test_normalize_terms(tmp_path):
    """
    Run the normalization script on a small input and verify the output JSON structure.
    """
    # Create sample input file
    input_data = {
        "recognized_chars": [
            {"text": "荆", "confidence": 0.5},
            {"text": "未知"}
        ]
    }
    input_path = tmp_path / "input.json"
    input_path.write_text(json.dumps(input_data, ensure_ascii=False, indent=2), encoding="utf-8")
    # Create workspace dir
    workspace = tmp_path / "ws"
    workspace.mkdir()
    # Run script
    script_path = Path(__file__).parent.parent / "scripts" / "normalize_terms.py"
    subprocess.check_call([
        "python", str(script_path), "--input", str(input_path), "--workspace", str(workspace)
    ])
    # Check output
    out_path = workspace / "term_normalisation" / "normalized_terms.json"
    assert out_path.exists()
    data = json.loads(out_path.read_text(encoding="utf-8"))
    assert "normalized_terms" in data
    assert len(data["normalized_terms"]) == 2
    # Check that unknown term has type unknown
    unknown = next(filter(lambda x: x["original"] == "未知", data["normalized_terms"]))
    assert unknown["type"] == "unknown"