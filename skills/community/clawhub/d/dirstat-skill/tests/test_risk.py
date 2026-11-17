from dirstat_skill.risk import classify_path


def test_classify_path_marks_system_prefix_as_keep_protected() -> None:
    assert (
        classify_path(
            "/var/lib/docker",
            ["/etc", "/usr", "/var/lib"],
            ["/home", "/var/log"],
        )
        == "keep protected"
    )


def test_classify_path_marks_windows_system_paths_as_keep_protected() -> None:
    assert (
        classify_path(
            "C:\\Windows\\System32",
            ["C:\\Windows", "C:\\Program Files"],
            ["C:\\Users"],
        )
        == "keep protected"
    )


def test_classify_path_marks_windows_temp_as_review_first() -> None:
    assert (
        classify_path(
            "C:\\Users\\giova\\AppData\\Local\\Temp\\huge.tmp",
            ["C:\\Windows", "C:\\Program Files"],
            ["C:\\Users"],
        )
        == "review first"
    )


def test_classify_path_marks_windows_temp_directory_as_review_first() -> None:
    assert (
        classify_path(
            "C:\\Users\\giova\\AppData\\Local\\Temp",
            ["C:\\Windows", "C:\\Program Files"],
            ["C:\\Users"],
        )
        == "review first"
    )


def test_classify_path_marks_home_assets_as_review_carefully() -> None:
    assert (
        classify_path(
            "/home/jagones/ComfyUI/models/checkpoints/model.safetensors",
            ["/etc", "/usr", "/var/lib"],
            ["/home", "/var/log"],
        )
        == "review carefully"
    )


def test_classify_path_marks_linux_cache_directory_as_review_first() -> None:
    assert (
        classify_path(
            "/home/jagones/.cache",
            ["/etc", "/usr", "/var/lib"],
            ["/home", "/var/log"],
        )
        == "review first"
    )


def test_classify_path_marks_huggingface_cache_directory_as_review_first() -> None:
    assert (
        classify_path(
            "F:\\huggingface_cache\\models--wan2.2",
            ["C:\\Windows", "C:\\Program Files", "F:\\docker"],
            ["C:\\Users", "F:\\"],
        )
        == "review first"
    )

