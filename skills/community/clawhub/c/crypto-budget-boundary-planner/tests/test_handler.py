import builtins
import sys
from pathlib import Path
from unittest import mock

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from handler import handle

with mock.patch.object(
    builtins,
    "open",
    side_effect=AssertionError("handler must not read local files"),
):
    result = handle({
        "skill_name": "../../private-data",
        "input": "Explain the risk calmly.",
        "mode": "guide",
    })

assert result["result"] == "done"
assert result["mode"] == "guide"
assert "no local file" in result["note"].lower()
print("passed")
