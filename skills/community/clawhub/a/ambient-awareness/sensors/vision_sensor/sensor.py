from __future__ import annotations

from sensor_api import BaseSensor, AwarenessEvent


class VisionSensor(BaseSensor):
    id = "vision.camera.stub"
    capabilities = ["vision", "motion_detection", "object_detection", "ocr"]
    permission_class = 2

    def setup(self, config):
        super().setup(config)
        self.enabled = bool(config.get("enabled", False))
        self.camera_index = config.get("camera_index", 0)

    def poll(self):
        if not self.enabled:
            return []
        # Stub only. Replace with OpenCV/local model logic.
        return [AwarenessEvent(
            sensor_id=self.id,
            event_type="sensor_error",
            summary="Vision sensor is enabled but only the stub implementation is installed.",
            confidence=1.0,
            importance_hint=0.8,
            payload={"camera_index": self.camera_index}
        )]
