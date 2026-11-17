"""OpenClaw state paths and a bounded, read-only Gateway health probe."""
from __future__ import annotations
import json
import os
from pathlib import Path
import re
import shutil
import subprocess


def layout(env=None):
    env = os.environ if env is None else env
    system_home = Path(env.get('HOME') or str(Path.home())).expanduser().absolute()
    raw_home = (env.get('OPENCLAW_HOME') or '').strip()
    if raw_home in ('null', 'undefined', ''):
        raw_home = str(system_home)
    home = Path(raw_home.replace('~/', str(system_home) + '/', 1) if raw_home.startswith('~/') else str(system_home) if raw_home == '~' else raw_home).absolute()
    def path(value):
        value = str(value)
        if value == '~':
            return home
        if value.startswith('~/'):
            return home / value[2:]
        return Path(value).absolute()
    profile = (env.get('OPENCLAW_PROFILE') or 'default').strip()
    if not re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9_-]{0,63}', profile):
        raise ValueError('Invalid OPENCLAW_PROFILE')
    if profile.lower() == 'default':
        profile = 'default'
    state_override = (env.get('OPENCLAW_STATE_DIR') or '').strip()
    state = path(state_override) if state_override else home / ('.openclaw' if profile == 'default' else f'.openclaw-{profile}')
    if not state_override and profile == 'default' and not state.exists() and (home / '.clawdbot').is_dir():
        state = home / '.clawdbot'
    workspace_default = state / 'workspace' if state_override or profile != 'default' else home / '.openclaw/workspace'
    workspace = path(env.get('OPENCLAW_WORKSPACE_DIR') or workspace_default)
    return {
        'state': state,
        'workspace': workspace,
        'skills': path(env.get('OPENCLAW_SKILLS_DIR') or state / 'skills'),
        'quarantine': path(env.get('OPENCLAW_QUARANTINE_DIR') or state / 'skills-quarantine'),
        'stage': path(env.get('OPENCLAW_STAGE_DIR') or workspace / '.skill_stage'),
    }


def gateway_health(*, emit, profile=None, timeout=10000):
    """ok=true confirms RPC success, not clean channels, plugins or host state."""
    unknown = ['Gateway reachability does not prove channel health, skill safety, or an uncompromised host.']
    if not 1 <= timeout <= 120000:
        raise ValueError('--timeout must be between 1 and 120000 milliseconds')
    profile = profile or os.environ.get('OPENCLAW_PROFILE')
    if profile and not re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9_-]{0,63}', profile):
        raise ValueError('Invalid OpenClaw profile')
    executable = shutil.which(os.environ.get('OPENCLAW_BIN', 'openclaw'))
    if not executable:
        emit([], ['OpenClaw CLI is not available.'], unknown, 'Select a trusted OpenClaw executable with OPENCLAW_BIN and re-run.')
        return 2
    command = [executable]
    if profile:
        command += ['--profile', profile]
    command += ['health', '--json', '--timeout', str(timeout)]
    try:
        result = subprocess.run(command, capture_output=True, text=True, timeout=timeout / 1000 + 5)
        if result.returncode != 0:
            raise ValueError(f'OpenClaw health command exited {result.returncode}')
        data = json.loads(result.stdout)
        if not isinstance(data, dict) or data.get('ok') is not True:
            raise ValueError('OpenClaw did not return a successful health snapshot')
    except (OSError, ValueError, subprocess.TimeoutExpired) as exc:
        # Do not echo raw stdout/stderr, which can contain authentication data.
        reason = 'OpenClaw health probe timed out' if isinstance(exc, subprocess.TimeoutExpired) else 'OpenClaw health probe failed or returned invalid JSON'
        emit([], [reason], unknown, 'Inspect OpenClaw status and local Gateway logs before trusting this session.')
        return 2
    emit(['Gateway health RPC succeeded and returned an ok=true snapshot.'], [], unknown,
         'Review channel/plugin/queue details in openclaw health --json; use openclaw security audit for a separate security assessment.')
    return 0
