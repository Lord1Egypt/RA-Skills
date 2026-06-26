from canvas_claw.model_registry import list_models_for_capability


def test_image_models_are_filtered() -> None:
    models = list_models_for_capability("image-create")
    assert any(model.catalog_key == "image-plus" for model in models)
    assert all(model.task_type in {"text_to_image", "image_to_image"} for model in models)
