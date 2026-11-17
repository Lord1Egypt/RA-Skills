from dedupe import dedupe

def test_order_and_uniqueness():
    ev = [{"a": 1}, {"a": 2}, {"a": 1}, {"a": 3}, {"a": 2}]
    assert dedupe(ev) == [{"a": 1}, {"a": 2}, {"a": 3}]

def test_empty():
    assert dedupe([]) == []
