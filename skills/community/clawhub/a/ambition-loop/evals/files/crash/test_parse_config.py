from parse_config import parse

def test_basic():
    assert parse("a = 1\nb=2") == {"a": "1", "b": "2"}
