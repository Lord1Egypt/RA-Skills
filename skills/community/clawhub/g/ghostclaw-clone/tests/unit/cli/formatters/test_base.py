import pytest
from ghostclaw.cli.formatters import BaseFormatter

class DummyFormatter(BaseFormatter):
    def format(self, report):
        return f"Vibe: {report['vibe_score']}"

def test_base_formatter():
    formatter = DummyFormatter()
    result = formatter.format({"vibe_score": 100})
    assert result == "Vibe: 100"
