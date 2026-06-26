from canvas_claw.tasks import build_image_request


def test_build_text_to_image_request() -> None:
    payload = build_image_request(
        prompt="a red fox",
        capability="image-create",
        task_type="text_to_image",
        provider="vg",
        model_id="qwen-image-2",
        image_urls=[],
        aspect_ratio="1:1",
        resolution="2K",
    )
    assert payload["type"] == "text_to_image"
    assert payload["input"]["prompt"] == "a red fox"
    assert payload["input"]["image_urls"] == []
    assert payload["options"]["aspect_ratio"] == "1:1"


def test_build_reference_image_request_uses_explicit_task_type() -> None:
    payload = build_image_request(
        prompt="same character",
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
