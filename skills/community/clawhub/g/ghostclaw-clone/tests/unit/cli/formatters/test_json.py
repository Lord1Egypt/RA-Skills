import pytest
import json
from ghostclaw.cli.formatters import JSONFormatter

def test_json_formatter():
    report = {"vibe_score": 90, "stack": "Python"}
    formatter = JSONFormatter(indent=4)
    result = formatter.format(report)

    parsed = json.loads(result)
    assert parsed["vibe_score"] == 90
    assert parsed["stack"] == "Python"
