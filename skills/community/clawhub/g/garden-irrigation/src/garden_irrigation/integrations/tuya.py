from __future__ import annotations

from pathlib import Path
import json
import os
import shutil
import subprocess


class TuyaClient:
    def __init__(self, workspace_root: Path):
        # folder is tuya_cloud (underscore); fall back to tuya-cloud (hyphen) for compatibility
        skill_dir = workspace_root / 'skills' / 'tuya_cloud'
        if not skill_dir.exists():
            skill_dir = workspace_root / 'skills' / 'tuya-cloud'
        self.skill_dir = skill_dir
        self.script = self.skill_dir / 'scripts' / 'tuya_controller.py'
        self.python = self._resolve_python()

    def _resolve_python(self) -> str:
        env_python = os.getenv('TUYA_CLOUD_PYTHON')
        if env_python:
            return env_python

        candidates = [
            self.skill_dir / '.venv' / 'bin' / 'python',
            self.skill_dir / 'venv' / 'bin' / 'python',
        ]
        for candidate in candidates:
            if candidate.exists():
                return str(candidate)

        system_python = shutil.which('python3') or shutil.which('python')
        if system_python:
            return system_python

        raise FileNotFoundError('No usable Python interpreter found for tuya-cloud')

    def _run(self, args: list[str]) -> str:
        if not self.script.exists():
            raise FileNotFoundError(f'tuya_controller.py not found at {self.script}')
        cmd = [self.python, str(self.script), *args]
        result = subprocess.run(cmd, cwd=self.skill_dir, capture_output=True, text=True)
        if result.returncode != 0:
            stderr = (result.stderr or '').strip()
            stdout = (result.stdout or '').strip()
            msg = stderr or stdout or f'Command failed with exit code {result.returncode}'
            if 'ModuleNotFoundError' in msg:
                msg += ' | Hint: set TUYA_CLOUD_PYTHON to a Python environment with tinytuya and python-dotenv installed.'
            raise RuntimeError(msg)
        return result.stdout

    def read_sensor(self, device_id: str) -> dict:
        out = self._run(['read_sensor', device_id, '--output_format', 'json'])
        return json.loads(out)

    def read_sensor_24h_avg(self, device_id: str) -> dict:
        """Return avg/count/min/max humidity over the last 24 hours from device logs."""
        out = self._run(['read_24h_avg', device_id])
        return json.loads(out)

    def read_sensor_last_n_avg(self, device_id: str, n: int = 50) -> dict:
        """Return avg/count/min/max humidity from the last N readings (looks back up to 7 days)."""
        out = self._run(['read_last_n', device_id, '--n', str(n)])
        return json.loads(out)

    def control(self, device_id: str, commands: list[dict]) -> dict:
        self._run(['control_device', device_id, json.dumps(commands)])
        return {'success': True}

    def open_valve_for_minutes(self, valve: dict, minutes: int) -> dict:
        if not valve.get('device_id'):
            raise ValueError('Missing valve device_id')
        switch_code = valve.get('switch_code', 'switch_1')
        countdown_code = valve.get('countdown_code')
        supports_countdown = valve.get('supports_countdown', False)

        commands = [{"code": switch_code, "value": True}]
        if supports_countdown and countdown_code and minutes > 0:
            commands.append({"code": countdown_code, "value": int(minutes)})
        return self.control(valve['device_id'], commands)

    def close_valve(self, valve: dict) -> dict:
        if not valve.get('device_id'):
            raise ValueError('Missing valve device_id')
        switch_code = valve.get('switch_code', 'switch_1')
        return self.control(valve['device_id'], [{"code": switch_code, "value": False}])
