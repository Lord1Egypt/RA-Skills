from toolkit.model_list import ModelList


class TestModelList:
    def test_get_all_models_contains_expected_groups(self):
        model_list = ModelList()

        result = model_list.get_all_models()

        assert "image_generation" in result
        assert "video_generation" in result
        assert "vision_understanding" in result
        assert len(result["image_generation"]) > 0
        assert len(result["video_generation"]) > 0
        assert len(result["vision_understanding"]) > 0

    def test_expandable_services_use_bearer_key_auth(self):
        model_list = ModelList()

        services = model_list.list_expandable_ark_services()

        assert len(services) >= 5
        for service in services:
            assert service["auth"] == "Bearer API Key"
            assert service["endpoint"].startswith("/")
