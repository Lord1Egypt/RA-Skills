from toolkit.smoke_e2e import run_smoke_test


class FakeClient:
    def __init__(self):
        self.video_task_id = "task-001"
        self.poll_count = 0

    def post(self, endpoint, json):
        if endpoint == "/images/generations":
            return {"data": [{"url": "https://example.com/image.jpg"}]}

        if endpoint == "/responses":
            return {
                "output": [
                    {
                        "type": "message",
                        "content": [
                            {
                                "type": "output_text",
                                "text": "mock vision summary",
                            }
                        ],
                    }
                ]
            }

        if endpoint == "/contents/generations/tasks":
            return {"id": self.video_task_id}

        raise AssertionError(f"unexpected endpoint: {endpoint}")

    def get(self, endpoint):
        if endpoint != f"/contents/generations/tasks/{self.video_task_id}":
            raise AssertionError(f"unexpected endpoint: {endpoint}")

        self.poll_count += 1
        if self.poll_count < 2:
            return {"status": "running", "content": {}}

        return {
            "status": "succeeded",
            "content": {"video_url": "https://example.com/video.mp4"},
        }


class FailingImageClient(FakeClient):
    def post(self, endpoint, json):
        if endpoint == "/images/generations":
            return {}
        return super().post(endpoint, json)


def test_run_smoke_test_success_path():
    result = run_smoke_test(client=FakeClient(), poll_interval=0.0, max_polls=3)

    assert result["ok"] is True
    assert result["image"]["url"] == "https://example.com/image.jpg"
    assert result["vision"]["summary"] == "mock vision summary"
    assert result["video"]["task_id"] == "task-001"
    assert result["video"]["status"] == "succeeded"
    assert result["video"]["url"] == "https://example.com/video.mp4"


def test_run_smoke_test_fails_when_image_missing_url():
    result = run_smoke_test(client=FailingImageClient(), poll_interval=0.0, max_polls=1)

    assert result["ok"] is False
    assert result["step"] == "image_generation"
