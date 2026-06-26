from canvas_claw.tasks import build_video_request


def test_first_frame_switches_to_image_to_video() -> None:
    payload = build_video_request(
        prompt="slow camera push",
        capability="video-animate",
        provider="vg",
        model_id="seedance-1-5-pro",
        image_urls=["https://example.com/frame.png"],
        aspect_ratio="16:9",
        resolution="720p",
        duration=8,
        generate_audio=True,
    )
    assert payload["type"] == "image_to_video"
    assert payload["options"]["sound"] is True


def test_generate_video_script_bootstrap_adds_project_root() -> None:
    script_text = (
        __import__("pathlib")
        .Path(__file__)
        .resolve()
        .parents[1]
        .joinpath("scripts", "generate_video.py")
        .read_text()
    )
    assert "sys.path.insert" in script_text
