#!/usr/bin/env python3
"""
Run the irrigation system in an OpenClaw agent environment and send reports.
This script should be executed within an OpenClaw agent session.
"""

from __future__ import annotations

from pathlib import Path
import sys
import json

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / 'src'
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from garden_irrigation.utils.config import Config
from garden_irrigation.storage.files import JsonStore, iso_now
from garden_irrigation.integrations.tuya import TuyaClient
from garden_irrigation.integrations.weather import WeatherClient
from garden_irrigation.engine.decision import decide
from garden_irrigation.reporting.daily import build_report


def send_message_via_openclaw(to: str, account_id: str, message: str) -> bool:
    """Send a message in the OpenClaw agent environment.

    This function should be called within an OpenClaw agent session.
    """
    try:
        # In an OpenClaw agent, we can invoke the message tool directly.
        # Here we simulate the tool call.
        print(f"[Tool call] message.send(to={to}, accountId={account_id})")

        # In a real OpenClaw agent this would be:
        # from openclaw_tools import message
        # result = message.send(to=to, accountId=account_id, message=message)
        # return result.get('ok', False)

        # Since we are inside the OpenClaw agent, we can call the tool directly,
        # but we need to ensure we are in the correct context.

        # Output the tool call in the format expected by the OpenClaw runtime.
        tool_call = {
            "name": "message",
            "parameters": {
                "action": "send",
                "to": to,
                "accountId": account_id,
                "message": message
            }
        }
        
        print(f"[TOOL_CALL] {json.dumps(tool_call)}")
        return True

    except Exception as e:
        print(f"[Error] Failed to send message: {e}")
        return False


def main():
    """Main function: run the irrigation system and send the report."""
    config = Config(ROOT)
    store = JsonStore(config.data_dir)
    tuya = TuyaClient(ROOT.parent.parent)
    weather = WeatherClient()
    
    # fetch weather data
    wx = weather.history_and_forecast(
        config.system['location']['latitude'],
        config.system['location']['longitude'],
        config.system['timezone']
    )
    
    history_daily = wx['history']['daily']
    forecast_daily = wx['forecast']['daily']
    recent_rain_mm = sum(history_daily.get('precipitation_sum', [])[-7:])
    forecast_rain_mm = sum(forecast_daily.get('precipitation_sum', [])[:1])
    
    results = []
    device_statuses = []
    
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
        
        result = {
            'zone_id': zone['id'],
            'zone_name': zone['name'],
            'decision': decision,
            'sensors': zone_sensors
        }
        results.append(result)
        store.append_jsonl(f"irrigation/{zone['id']}.jsonl", {
            'ts': iso_now(),
            'planned': decision,
        })
    
    # generate report
    report = build_report(results, weather_data=wx)
    report_path = store.write_report(f"reports/daily-{iso_now().replace(':','-')}.md", report)
    print(f"Report saved: {report_path}")

    # check whether to send the report
    reporting_config = config.system.get('reporting', {})
    if reporting_config.get('enabled', False) and reporting_config.get('send_report_to_bot', False):
        print("[Notification] Checking whether to send report to bot...")

        # get the greenhouse zone decision
        greenhouse_decision = None
        for result in results:
            if result['zone_id'] == 'greenhouse':
                greenhouse_decision = result['decision']
                break
        
        if greenhouse_decision:
            # check send conditions
            should_send = False
            should_irrigate = greenhouse_decision.get('should_irrigate', False)
            
            if should_irrigate and reporting_config.get('send_on_irrigation', True):
                should_send = True
            elif not should_irrigate and reporting_config.get('send_on_no_irrigation', False):
                should_send = True
            
            if should_send:
                bot_account_id = reporting_config.get('bot_account_id')
                bot_target = reporting_config.get('bot_target')
                
                if bot_account_id and bot_target:
                    # format message
                    title = f"🌱 Garden Irrigation Report - {iso_now()[:10]}"
                    message_content = f"**{title}**\n\n{report}"

                    # truncate to platform length limit
                    max_length = 3500
                    if len(message_content) > max_length:
                        message_content = message_content[:max_length] + "\n\n... (report truncated)"

                    # send message
                    print(f"[Notification] Sending report to {bot_target}...")
                    success = send_message_via_openclaw(
                        to=bot_target,
                        account_id=bot_account_id,
                        message=message_content
                    )
                    
                    if success:
                        print("[Notification] Report sending process started")
                    else:
                        print("[Notification] Report sending failed")
                else:
                    print("[Notification error] Bot configuration incomplete")
            else:
                print("[Notification] Configuration says not to send report this time")
        else:
            print("[Notification warning] No greenhouse decision found, skipping send")
    else:
        print("[Notification] Report sending not enabled")

    print("\n" + "="*60)
    print(report)
    print("="*60)


if __name__ == '__main__':
    main()