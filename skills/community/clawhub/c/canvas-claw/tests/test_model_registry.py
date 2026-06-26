from canvas_claw.model_registry import resolve_model


def test_resolve_default_text_to_image_model() -> None:
    model = resolve_model(capability="image-create", catalog_key=None)
    assert model.catalog_key == "image-plus"
    assert model.provider == "vg"
    assert model.model_id == "qwen-image-2"
    assert model.task_type == "text_to_image"


def test_image_remix_uses_backend_text_to_image_model() -> None:
    model = resolve_model(capability="image-remix", catalog_key=None)
    assert model.catalog_key == "image-multi"
    assert model.model_id == "nano-banana-2"
    assert model.task_type == "text_to_image"
