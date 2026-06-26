from __future__ import annotations

from sensor_api import BaseSensor, AwarenessEvent


class AudioSensor(BaseSensor):
    id = "audio.microphone.stub"
    capabilities = ["audio", "speech_detection", "asr"]
    permission_class = 2

    def setup(self, config):
        super().setup(config)
        self.enabled = bool(config.get("enabled", False))
        self.device_index = config.get("device_index", None)

    def poll(self):
        if not self.enabled:
            return []
        # Stub only. Replace with local VAD/ASR logic.
        return [AwarenessEvent(
            sensor_id=self.id,
            event_type="sensor_error",
            summary="Audio sensor is enabled but only the stub implementation is installed.",
            confidence=1.0,
            importance_hint=0.8,
            payload={"device_index": self.device_index}
        )]
