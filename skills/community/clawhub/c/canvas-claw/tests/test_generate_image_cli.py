from canvas_claw.tasks import build_image_request


def test_reference_images_switch_to_image_to_image() -> None:
    payload = build_image_request(
        prompt="portrait",
        capability="image-remix",
        task_type="text_to_image",
        provider="vg",
        model_id="nano-banana-2",
        image_urls=["https://example.com/ref.png"],
        aspect_ratio="3:4",
        resolution="2K",
    )
    assert payload["type"] == "text_to_image"
    assert payload["input"]["image_urls"] == ["https://example.com/ref.png"]


def test_generate_image_script_bootstrap_adds_project_root() -> None:
    script_text = (
        __import__("pathlib")
        .Path(__file__)
        .resolve()
        .parents[1]
        .joinpath("scripts", "generate_image.py")
        .read_text()
    )
    assert "sys.path.insert" in script_text
