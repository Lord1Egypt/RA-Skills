from __future__ import annotations


def decide(zone: dict, moisture_values: list[float], recent_rain_mm: float, forecast_rain_mm: float, recent_watering: list[dict]) -> dict:
    avg_moisture = sum(moisture_values) / len(moisture_values) if moisture_values else None
    if avg_moisture is None:
        return {
            'should_irrigate': False,
            'minutes': 0,
            'reason': 'No sensor data'
        }

    target_min = zone['target_moisture_min']
    target_max = zone['target_moisture_max']
    default_minutes = zone['default_minutes']
    max_minutes = zone['max_minutes']
    
    # Only irrigate when average moisture is below the target minimum
    if avg_moisture < target_min:
        deficit = target_min - avg_moisture
        # Add 1 extra minute per 5% moisture deficit
        minutes = default_minutes + round(deficit / 5)

        # Rain-sensitive zone adjustment
        if zone.get('rain_sensitive'):
            if recent_rain_mm >= 8 or forecast_rain_mm >= 5:
                minutes = max(0, minutes - 4)

        # Recent watering adjustment
        if recent_watering:
            minutes = max(0, minutes - 1)
        
        minutes = min(max_minutes, max(0, minutes))
        valve = zone.get('valve', {})
        return {
            'should_irrigate': minutes > 0,
            'minutes': minutes,
            'reason': f"avg moisture={avg_moisture:.1f}% < target_min={target_min}%, deficit={deficit:.1f}%, recent rain={recent_rain_mm:.1f}mm, forecast rain={forecast_rain_mm:.1f}mm",
            'valve_plan': {
                'device_id': valve.get('device_id'),
                'switch_code': valve.get('switch_code', 'switch_1'),
                'countdown_code': valve.get('countdown_code'),
                'supports_countdown': valve.get('supports_countdown', False)
            }
        }
    else:
        # Moisture is within or above target range — no irrigation needed
        status = "within target range" if avg_moisture <= target_max else "above target range"
        valve = zone.get('valve', {})
        return {
            'should_irrigate': False,
            'minutes': 0,
            'reason': f"avg moisture={avg_moisture:.1f}% {status} ({target_min}-{target_max}%), recent rain={recent_rain_mm:.1f}mm",
            'valve_plan': {
                'device_id': valve.get('device_id'),
                'switch_code': valve.get('switch_code', 'switch_1'),
                'countdown_code': valve.get('countdown_code'),
                'supports_countdown': valve.get('supports_countdown', False)
            }
        }
