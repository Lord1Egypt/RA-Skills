#!/usr/bin/env python3
"""
Irrigation runner with user confirmation.
Sends a confirmation request before executing watering.
"""

from __future__ import annotations

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / 'src'
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from garden_irrigation.utils.config import Config
from garden_irrigation.storage.files import JsonStore, iso_now
from garden_irrigation.integrations.tuya import TuyaClient
from garden_irrigation.integrations.weather import WeatherClient
from garden_irrigation.integrations.notifications import send_report_if_needed
from garden_irrigation.engine.decision import decide
from garden_irrigation.reporting.daily import build_report


def send_confirmation_request(zone_name: str, minutes: int, reason: str, config: dict) -> bool:
    """Send a watering confirmation request to the user."""
    print(f"\n{'=' * 60}")
    print(f"🚰 Watering confirmation request")
    print(f"{'=' * 60}")
    print(f"Zone: {zone_name}")
    print(f"Suggested duration: {minutes} minutes")
    print(f"Reason: {reason}")
    print(f"{'=' * 60}")

    # In a real system this would send a message via Telegram or another channel.
    # For now we use a console prompt.

    response = input("Execute watering? (y/n): ")
    return response.lower() == 'y'


def main():
    config = Config(ROOT)
    store = JsonStore(config.data_dir)
    tuya = TuyaClient(ROOT.parent.parent)
    weather = WeatherClient()

    wx = weather.history_and_forecast(
        config.system['location']['latitude'],
        config.system['location']['longitude'],
        config.system['timezone'],
    )
    history_daily = wx['history']['daily']
    forecast_daily = wx['forecast']['daily']
    recent_rain_mm = sum(history_daily.get('precipitation_sum', [])[-7:])
    forecast_rain_mm = sum(forecast_daily.get('precipitation_sum', [])[:1])

    results = []
    device_statuses = []  # collect status for all devices
    irrigation_executed = False  # track whether any watering was executed

    for zone in config.zones:
        moisture_values = []
        avg_24h_values = []
        zone_sensors = []

        for sensor_id in zone.get('soil_sensor_ids', []):
            if str(sensor_id).startswith('REPLACE_'):
                continue
            try:
                sensor = tuya.read_sensor(sensor_id)

                # extract device status info
                device_info = {
                    'device_id': sensor_id,
                    'name': sensor.get('name', 'Unknown'),
                    'online': sensor.get('online', False),
                    'moisture': None,
                    'temperature': None,
                    'battery': None,
                    'last_updated': sensor.get('parsed_data', {}).get('last_updated', '')
                }

                # current reading
                current_moisture = sensor.get('parsed_data', {}).get('humidity_percent') or sensor.get('va_humidity')
                device_info['moisture_current'] = float(current_moisture) if current_moisture is not None else None

                # 24h average
                avg_24h, avg_24h_count = None, 0
                try:
                    avg_data = tuya.read_sensor_last_n_avg(sensor_id)
                    if avg_data.get('count', 0) >= 1:
                        avg_24h = avg_data['avg_humidity']
                        avg_24h_count = avg_data['count']
                except Exception:
                    pass
                device_info['moisture_24h_avg'] = avg_24h
                device_info['moisture_24h_count'] = avg_24h_count

                if avg_24h is not None:
                    avg_24h_values.append(float(avg_24h))
                if current_moisture is not None:
                    moisture_values.append(float(current_moisture))
                device_info['moisture'] = avg_24h if avg_24h is not None else current_moisture

                # extract temperature
                temp = (
                        sensor.get('temperature') or
                        sensor.get('va_temperature') or
                        (sensor.get('parsed_data', {}).get('temperature_celsius'))
                )
                if temp is not None:
                    device_info['temperature'] = float(temp)

                # extract battery
                battery = (
                        sensor.get('battery_percentage') or
                        sensor.get('battery_percent') or
                        (sensor.get('parsed_data', {}).get('battery_percent'))
                )
                if battery is not None:
                    device_info['battery'] = int(battery)

                zone_sensors.append(device_info)
                device_statuses.append(device_info)

                store.append_jsonl(f"soil/{zone['id']}.jsonl", {
                    'ts': iso_now(), 'sensor_id': sensor_id, 'raw': sensor
                })
            except Exception as e:
                device_statuses.append({
                    'device_id': sensor_id,
                    'name': 'Error',
                    'online': False,
                    'error': str(e)
                })
                store.append_jsonl(f"soil/{zone['id']}.jsonl", {
                    'ts': iso_now(), 'sensor_id': sensor_id, 'error': str(e)
                })

        recent_watering = store.read_jsonl(f"irrigation/{zone['id']}.jsonl")[-3:]
        zone_moisture = avg_24h_values if avg_24h_values else moisture_values
        decision = decide(zone, zone_moisture, recent_rain_mm, forecast_rain_mm, recent_watering)

        # execution logic with confirmation
        executed_result = None
        if decision['should_irrigate'] and decision['minutes'] > 0:
            valve_config = zone.get('valve', {})

            if valve_config.get('device_id') and not str(valve_config['device_id']).startswith('REPLACE_'):
                # request user confirmation
                confirmed = send_confirmation_request(
                    zone_name=zone['name'],
                    minutes=decision['minutes'],
                    reason=decision['reason'],
                    config=config.system
                )

                if confirmed:
                    try:
                        print(f"\n🚰 Executing watering: {zone['name']} - {decision['minutes']} minutes")

                        # open valve
                        executed_result = tuya.open_valve_for_minutes(
                            valve_config,
                            decision['minutes']
                        )

                        success = executed_result.get('success', False)
                        if success:
                            print(f"✅ Watering executed successfully")
                            irrigation_executed = True
                        else:
                            print(f"❌ Watering failed: {executed_result.get('error', 'unknown error')}")

                    except Exception as e:
                        print(f"❌ Valve control failed: {e}")
                        executed_result = {'error': str(e), 'success': False}
                else:
                    print(f"⏸️  Watering cancelled by user")
                    executed_result = {'cancelled': True, 'success': False}
            else:
                print(f"⚠️  Valve not configured or is a placeholder")

        result = {
            'zone_id': zone['id'],
            'zone_name': zone['name'],
            'decision': decision,
            'sensors': zone_sensors,
            'executed': executed_result
        }
        results.append(result)

        # record irrigation history (including execution result)
        irrigation_record = {
            'ts': iso_now(),
            'planned': decision,
        }
        if executed_result:
            irrigation_record['executed'] = executed_result
        store.append_jsonl(f"irrigation/{zone['id']}.jsonl", irrigation_record)

    # Build report with language support
    report = build_report(
        results,
        weather_data=wx,
        config=config.system,
        query_text=None
    )
    report_path = store.write_report(f"reports/daily-{iso_now().replace(':', '-')}.md", report)
    print(f"\n📄 Report saved: {report_path}")

    if irrigation_executed:
        print(f"🚰 Watering was executed this run")

    # Send report to bot (if enabled)
    reporting_config = config.system.get('reporting', {})
    if reporting_config.get('enabled', False) and reporting_config.get('send_report_to_bot', False):
        print("\n[Notification] Checking if report should be sent to bot...")

        # Get greenhouse decision
        greenhouse_decision = None
        for result in results:
            if result['zone_id'] == 'greenhouse':
                greenhouse_decision = result['decision']
                break

        if greenhouse_decision:
            sent = send_report_if_needed(
                reporting_config=reporting_config,
                irrigation_decision=greenhouse_decision,
                report_content=report,
                report_title=f"🌱 Garden Irrigation Report - {iso_now()[:10]}"
            )
            if sent:
                print("[Notification] Report sending process started")
            else:
                print("[Notification] According to configuration, report not sent this time")
        else:
            print("[Notification Warning] No greenhouse decision found, skipping send")
    else:
        print("[Notification] Report sending not enabled")


if __name__ == '__main__':
    print("🌱 Garden irrigation system with confirmation")
    print("=" * 60)
    print("Mode: request user confirmation before watering")
    print("=" * 60)
    main()
