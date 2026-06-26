"""Sensor layer — aggregates signals from multiple information sources."""

from .base import BaseSensor, Signal
from ..utils.logger import log

# Registry of available sensors
SENSOR_REGISTRY: dict[str, type[BaseSensor]] = {}


def _register_sensors():
    """Lazily register all built-in sensors."""
    if SENSOR_REGISTRY:
        return
    from .crypto import CryptoSensor
    from .news import NewsSensor
    from .google_trends import GoogleTrendsSensor
    SENSOR_REGISTRY["crypto"] = CryptoSensor
    SENSOR_REGISTRY["news"] = NewsSensor
    SENSOR_REGISTRY["google_trends"] = GoogleTrendsSensor


class SensorManager:
    """Aggregates signals from configured information sources."""

    def __init__(self, source_names: list[str]):
        _register_sensors()
        self.sensors: list[BaseSensor] = []
        for name in source_names:
            cls = SENSOR_REGISTRY.get(name)
            if cls:
                self.sensors.append(cls())
            else:
                log.warning(f"Unknown sensor: {name}")

    def scan_all(self) -> list[Signal]:
        """Scan all sensors and return aggregated, sorted signals."""
        all_signals = []
        for sensor in self.sensors:
            try:
                signals = sensor.scan()
                log.info(f"  [{sensor.name}] {len(signals)} signals")
                all_signals.extend(signals)
            except Exception as e:
                log.warning(f"  [{sensor.name}] error: {e}")

        # Sort by score descending
        all_signals.sort(key=lambda s: s.score, reverse=True)
        return all_signals
