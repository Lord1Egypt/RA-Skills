from findskills import load_registry, validate_registry, REGISTRY_PATH


def test_registry_file_exists():
    assert REGISTRY_PATH.exists()


def test_registry_valid():
    entries = load_registry()
    assert isinstance(entries, list) and len(entries) > 0
    problems = validate_registry(entries)
    assert problems == [], f"registry 校验问题: {problems}"


def test_registry_reputation_range():
    for e in load_registry():
        rep = e.get("reputation")
        assert rep is None or 0.0 <= float(rep) <= 1.0
