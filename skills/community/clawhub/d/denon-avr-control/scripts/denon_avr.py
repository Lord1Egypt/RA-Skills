#!/usr/bin/env python3
import argparse
import socket
import sys
import urllib.parse
import urllib.request

DEFAULT_PORT = 23
DEFAULT_HTTP_PORT = 80

INPUT_MAP = {
    'tv': 'SITV',
    'cd': 'SICD',
    'dvd': 'SIDVD',
    'bluray': 'SIBD',
    'bd': 'SIBD',
    'game': 'SIGAME',
    'media-player': 'SIMPLAY',
    'mplay': 'SIMPLAY',
    'cbl-sat': 'SISAT/CBL',
    'sat-cbl': 'SISAT/CBL',
    'aux1': 'SIAUX1',
    'aux2': 'SIAUX2',
    'tuner': 'SITUNER',
    'heos': 'SINET',
    'net': 'SINET',
    'bluetooth': 'SIBLUETOOTH',
    'phono': 'SIPHONO',
}

SOUND_MODE_MAP = {
    'stereo': 'MSSTEREO',
    'direct': 'MSDIRECT',
    'pure-direct': 'MSPURE DIRECT',
    'dolby-audio': 'MSDOLBY AUDIO - DOLBY SURROUND',
    'movie': 'MSMOVIE',
    'music': 'MSMUSIC',
    'game': 'MSGAME',
    'auto': 'MSAUTO',
}


def send_tcp(host: str, port: int, command: str, timeout: float) -> str:
    data = (command + '\r').encode('ascii')
    with socket.create_connection((host, port), timeout=timeout) as sock:
        sock.settimeout(timeout)
        sock.sendall(data)
        try:
            return sock.recv(4096).decode('utf-8', 'ignore').strip()
        except socket.timeout:
            return ''


def send_http(host: str, port: int, command: str, timeout: float) -> str:
    encoded = urllib.parse.quote(command, safe='')
    url = f'http://{host}:{port}/goform/formiPhoneAppDirect.xml?{encoded}'
    req = urllib.request.Request(url, method='GET')
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return resp.read().decode('utf-8', 'ignore').strip()


def format_volume(value: float) -> str:
    if value < 0 or value > 98:
        raise ValueError('Volume must be between 0 and 98 dB steps in Denon absolute scale.')
    whole = int(value)
    frac = round(value - whole, 1)
    if frac == 0:
        return f'{whole:02d}'
    if frac == 0.5:
        return f'{whole:02d}5'
    raise ValueError('Volume must be in 0.5 increments, e.g. 35 or 35.5')


def build_commands(args: argparse.Namespace) -> list[str]:
    commands: list[str] = []

    if args.raw:
        commands.extend(args.raw)

    if args.power:
        if args.power == 'on':
            commands.append('PWON')
        elif args.power == 'off':
            commands.append('PWSTANDBY')
        elif args.power == 'status':
            commands.append('PW?')

    if args.mute:
        commands.append({'on': 'MUON', 'off': 'MUOFF', 'toggle': 'MUTOGGLE', 'status': 'MU?'}[args.mute])

    if args.volume is not None:
        commands.append('MV' + format_volume(args.volume))
    if args.volume_up:
        commands.extend(['MVUP'] * args.volume_up)
    if args.volume_down:
        commands.extend(['MVDOWN'] * args.volume_down)
    if args.volume_status:
        commands.append('MV?')

    if args.input:
        key = args.input.strip().lower()
        if key not in INPUT_MAP:
            raise ValueError(f'Unknown input: {args.input}')
        commands.append(INPUT_MAP[key])
    if args.input_status:
        commands.append('SI?')

    if args.sound_mode:
        key = args.sound_mode.strip().lower()
        if key not in SOUND_MODE_MAP:
            raise ValueError(f'Unknown sound mode: {args.sound_mode}')
        commands.append(SOUND_MODE_MAP[key])
    if args.sound_mode_status:
        commands.append('MS?')

    if args.zone:
        zone = args.zone.upper()
        zone_cmd = zone + '?'
        commands.append(zone_cmd)

    if args.status:
        commands.extend(['PW?', 'MU?', 'MV?', 'SI?', 'MS?'])

    if not commands:
        raise ValueError('No command requested. Use --status, --power, --volume, --input, or --raw.')

    return commands


def main() -> int:
    parser = argparse.ArgumentParser(description='Control a Denon AVR over TCP or HTTP IP control.')
    parser.add_argument('--host', required=True, help='Receiver hostname or IP address')
    parser.add_argument('--transport', choices=['tcp', 'http'], default='tcp')
    parser.add_argument('--port', type=int, help='Override port (default: 23 for tcp, 80 for http)')
    parser.add_argument('--timeout', type=float, default=3.0)

    parser.add_argument('--status', action='store_true', help='Query common status values')
    parser.add_argument('--power', choices=['on', 'off', 'status'])
    parser.add_argument('--mute', choices=['on', 'off', 'toggle', 'status'])
    parser.add_argument('--volume', type=float, help='Set absolute volume in 0.5 steps, e.g. 35.5')
    parser.add_argument('--volume-up', type=int, default=0, help='Increment volume N steps')
    parser.add_argument('--volume-down', type=int, default=0, help='Decrement volume N steps')
    parser.add_argument('--volume-status', action='store_true')
    parser.add_argument('--input', help='Select input: tv, bluray, game, heos, cd, dvd, tuner, aux1, aux2, bluetooth, phono, cbl-sat')
    parser.add_argument('--input-status', action='store_true')
    parser.add_argument('--sound-mode', help='Set sound mode: stereo, direct, pure-direct, movie, music, game, auto, dolby-audio')
    parser.add_argument('--sound-mode-status', action='store_true')
    parser.add_argument('--zone', choices=['ZM', 'Z2', 'Z3'], help='Query a raw zone status token')
    parser.add_argument('--raw', action='append', help='Send a raw Denon command. Repeat for multiple commands.')

    args = parser.parse_args()

    try:
        commands = build_commands(args)
    except ValueError as e:
        print(f'error: {e}', file=sys.stderr)
        return 2

    port = args.port or (DEFAULT_PORT if args.transport == 'tcp' else DEFAULT_HTTP_PORT)
    sender = send_tcp if args.transport == 'tcp' else send_http

    exit_code = 0
    for command in commands:
        try:
            response = sender(args.host, port, command, args.timeout)
            print(f'> {command}')
            if response:
                print(response)
        except Exception as e:
            exit_code = 1
            print(f'> {command}', file=sys.stderr)
            print(f'error: {e}', file=sys.stderr)
            break

    return exit_code


if __name__ == '__main__':
    raise SystemExit(main())
