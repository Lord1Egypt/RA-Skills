from pathlib import Path

from dirstat_skill.config import load_settings


def test_load_settings_reads_defaults_and_overrides(tmp_path: Path) -> None:
    config_path = tmp_path / "defaults.json"
    config_path.write_text(
        """
        {
          "top_n": 20,
          "min_bytes": 1048576,
          "one_file_system": true,
          "exclude_patterns": [".cache", "node_modules"],
          "risk_do_not_touch_prefixes": ["/etc", "/usr", "/var/lib"],
          "risk_needs_inspection_prefixes": ["/opt", "/srv", "/var/log"],
          "windows_do_not_touch_prefixes": ["C:\\\\Windows", "C:\\\\Program Files"],
          "default_engine_windows": "windows-native",
          "default_engine_linux": "ncdu"
        }
        """.strip(),
        encoding="utf-8",
    )

    settings = load_settings(
        config_path=config_path,
        env_overrides={"TOP_N": "50", "MIN_BYTES": "1073741824"},
    )

    assert settings.top_n == 50
    assert settings.min_bytes == 1073741824
    assert settings.one_file_system is True
    assert settings.exclude_patterns == [".cache", "node_modules"]
    assert settings.windows_do_not_touch_prefixes == ["C:\\Windows", "C:\\Program Files"]
    assert settings.default_engine_windows == "windows-native"
    assert settings.default_engine_linux == "ncdu"


def test_load_settings_reads_recursive_reporting_defaults(tmp_path: Path) -> None:
    config_path = tmp_path / "defaults.json"
    config_path.write_text(
        """
        {
          "top_n": 20,
          "min_bytes": 1048576,
          "one_file_system": true,
          "exclude_patterns": [".cache", "node_modules"],
          "risk_do_not_touch_prefixes": ["/etc", "/usr", "/var/lib"],
          "risk_needs_inspection_prefixes": ["/opt", "/srv", "/var/log"],
          "windows_do_not_touch_prefixes": ["C:\\\\Windows", "C:\\\\Program Files"],
          "default_engine_windows": "windows-native",
          "default_engine_linux": "ncdu",
          "dominant_percent": 0.8,
          "min_candidate_bytes": 2097152,
          "max_nearby_reference_files": 5,
          "nearby_reference_extensions": [".json", ".yaml", ".yml"]
        }
        """.strip(),
        encoding="utf-8",
    )

    settings = load_settings(config_path=config_path)

    assert settings.dominant_percent == 0.8
    assert settings.min_candidate_bytes == 2097152
    assert settings.max_nearby_reference_files == 5
    assert settings.nearby_reference_extensions == [".json", ".yaml", ".yml"]


def test_load_settings_reads_dominant_percent_override() -> None:
    settings = load_settings(
        Path("config/defaults.json"),
        env_overrides={"DOMINANT_PERCENT": "0.67"},
    )

    assert settings.dominant_percent == 0.67

