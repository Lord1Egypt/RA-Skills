#!/usr/bin/env python3
"""
FRITZ!Box TR-064 API Client
Simple CLI tool to control AVM FRITZ!Box routers via TR-064 protocol.
"""

import argparse
import sys
import hashlib
import ipaddress
import socket
import requests
from requests.auth import HTTPDigestAuth
from xml.etree import ElementTree as ET
from urllib.parse import quote
import re
import os

# Try to load .env file
def load_env_file(path='.env'):
    """Load environment variables from .env file."""
    env_paths = [
        path,
        os.path.join(os.path.dirname(__file__), '..', '.env'),
        os.path.expanduser('~/.openclaw/workspace-main/skills/fritzbox/.env')
    ]
    
    for env_path in env_paths:
        if os.path.exists(env_path):
            with open(env_path, 'r') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#') and '=' in line:
                        key, value = line.split('=', 1)
                        if key not in os.environ:
                            os.environ[key] = value
            break

load_env_file()


class FritzBox:
    """Simple FRITZ!Box TR-064 API client."""
    
    COMMON_ACTIONS = {
        'wlan': {
            'service': 'urn:dslforum-org:service:WLANConfiguration:1',
            'control': '/upnp/control/wlanconfig1',
            'actions': {
                'info': 'GetInfo',
                'stats': 'GetStatistics',
            }
        },
        'wlan2': {
            'service': 'urn:dslforum-org:service:WLANConfiguration:2',
            'control': '/upnp/control/wlanconfig2',
        },
        'wlan3': {
            'service': 'urn:dslforum-org:service:WLANConfiguration:3',
            'control': '/upnp/control/wlanconfig3',
        },
        'hosts': {
            'service': 'urn:dslforum-org:service:Hosts:1',
            'control': '/upnp/control/hosts',
            'actions': {
                'list': 'GetHostNumberOfEntries',
                'info': 'GetGenericHostEntry',
            }
        },
        'device': {
            'service': 'urn:dslforum-org:service:DeviceInfo:1',
            'control': '/upnp/control/deviceinfo',
            'actions': {
                'info': 'GetInfo',
            }
        },
        'wan': {
            'service': 'urn:dslforum-org:service:WANIPConnection:1',
            'control': '/upnp/control/wanipconnection1',
        },
        'dect': {
            'service': 'urn:dslforum-org:service:X_AVM-DE_Dect:1',
            'control': '/upnp/control/x_dect',
        },
        'homeauto': {
            'service': 'urn:dslforum-org:service:X_AVM-DE_Homeauto:1',
            'control': '/upnp/control/x_homeauto',
        }
    }
    
    def __init__(self, host='fritz.box', user=None, password=None):
        validated_ip = self._validate_host(host)
        # Use the resolved IP (not the raw env string) so credentials are never
        # sent to an env-controlled hostname — the URL is derived from a
        # DNS-validated private IP only.
        self.host = validated_ip
        self.user = user or ''
        self.password = password or ''
        self.base_url = f'http://{validated_ip}:49000'
        # Pre-build the auth object so request methods don't reference env vars directly.
        self._auth = HTTPDigestAuth(self.user, self.password) if self.password else None
        self._sid = None
        self._challenge = None

    @staticmethod
    def _validate_host(host: str) -> str:
        """Resolve host and ensure it is a private or loopback address.

        Returns the resolved IP string so the caller can use the validated IP
        directly instead of the original (potentially env-supplied) hostname.
        Credentials must never be sent to a public internet host.
        Raises ValueError if the host is not local.
        """
        try:
            ip_str = socket.gethostbyname(host)
            addr = ipaddress.ip_address(ip_str)
        except socket.gaierror:
            raise ValueError(
                f"Cannot resolve host '{host}'. "
                "FRITZBOX_HOST must be a reachable local address."
            )
        if not (addr.is_private or addr.is_loopback or addr.is_link_local):
            raise ValueError(
                f"Host '{host}' resolves to public IP {ip_str}. "
                "FRITZBOX_HOST must be a private/local address to prevent "
                "credential exfiltration."
            )
        return ip_str
        
    def _get_challenge(self):
        """Get authentication challenge from FRITZ!Box."""
        try:
            # Try to get challenge via login_sid.lua
            resp = requests.get(f'http://{self.host}/login_sid.lua', timeout=10)
            resp.raise_for_status()
            
            # Parse challenge from XML response
            match = re.search(r'<Challenge>([^<]+)</Challenge>', resp.text)
            if match:
                return match.group(1)
        except Exception as e:
            print(f"Challenge fetch error: {e}", file=sys.stderr)
        return None
    
    def _create_response(self, challenge, password):
        """Create challenge-response hash for FRITZ!Box authentication."""
        # FRITZ!Box uses: challenge + "-" + md5(challenge + "-" + password)
        text = f"{challenge}-{password}"
        # Convert to UTF-16LE (Windows style)
        text_utf16 = text.encode('utf-16le')
        response_hash = hashlib.md5(text_utf16).hexdigest()
        return f"{challenge}-{response_hash}"
    
    def _login(self):
        """Login to FRITZ!Box and get session ID."""
        if self._sid:
            return self._sid
            
        challenge = self._get_challenge()
        if not challenge:
            return None
            
        response = self._create_response(challenge, self.password)
        
        try:
            login_url = f'http://{self.host}/login_sid.lua?username={quote(self.user)}&response={response}'
            resp = requests.get(login_url, timeout=10)
            resp.raise_for_status()
            
            # Parse SID from response
            match = re.search(r'<SID>([^<]+)</SID>', resp.text)
            if match:
                sid = match.group(1)
                if sid != '0000000000000000':
                    self._sid = sid
                    return sid
        except Exception as e:
            print(f"Login error: {e}", file=sys.stderr)
        return None
    
    def _build_soap(self, service, action, args=None):
        """Build SOAP envelope."""
        args = args or {}
        arg_str = ''.join([f'<{k}>{v}</{k}>' for k, v in args.items()])
        
        soap = f'''<?xml version="1.0" encoding="utf-8"?>
<s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/"
            s:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/">
  <s:Body>
    <u:{action} xmlns:u="{service}">
      {arg_str}
    </u:{action}>
  </s:Body>
</s:Envelope>'''
        return soap
    
    def _call(self, service, control_url, action, args=None):
        """Make SOAP call."""
        soap = self._build_soap(service, action, args)
        headers = {
            'Content-Type': 'text/xml; charset=utf-8',
            'SOAPAction': f'"{service}#{action}"'
        }
        
        try:
            # TR-064 uses HTTP Digest Authentication
            resp = requests.post(
                f'{self.base_url}{control_url}',
                data=soap,
                headers=headers,
                auth=self._auth,
                timeout=10
            )
            resp.raise_for_status()
            return resp.text
        except requests.exceptions.RequestException as e:
            print(f"Error: {e}", file=sys.stderr)
            return None
    
    def _parse_response(self, xml_text, action):
        """Parse SOAP response."""
        if not xml_text:
            return {}
        try:
            root = ET.fromstring(xml_text)
            # Extract response body
            body = root.find('.//{http://schemas.xmlsoap.org/soap/envelope/}Body')
            if body is not None:
                response = body[0]  # First child is the response
                result = {}
                for child in response:
                    tag = child.tag.split('}')[-1] if '}' in child.tag else child.tag
                    result[tag] = child.text
                return result
        except ET.ParseError as e:
            print(f"Parse error: {e}", file=sys.stderr)
        return {}
    
    def wlan_status(self, band=1):
        """Get WLAN status."""
        cfg = self.COMMON_ACTIONS[f'wlan{band}' if band > 1 else 'wlan']
        xml = self._call(cfg['service'], cfg['control'], 'GetInfo')
        return self._parse_response(xml, 'GetInfo')
    
    def wlan_on(self, band=1):
        """Turn WLAN on."""
        cfg = self.COMMON_ACTIONS[f'wlan{band}' if band > 1 else 'wlan']
        xml = self._call(cfg['service'], cfg['control'], 'SetEnable', {'NewEnable': '1'})
        return xml is not None
    
    def wlan_off(self, band=1):
        """Turn WLAN off."""
        cfg = self.COMMON_ACTIONS[f'wlan{band}' if band > 1 else 'wlan']
        xml = self._call(cfg['service'], cfg['control'], 'SetEnable', {'NewEnable': '0'})
        return xml is not None
    
    def get_hosts(self):
        """Get connected hosts."""
        cfg = self.COMMON_ACTIONS['hosts']
        # First get number of entries
        xml = self._call(cfg['service'], cfg['control'], 'GetHostNumberOfEntries')
        result = self._parse_response(xml, 'GetHostNumberOfEntries')
        count = int(result.get('NewHostNumberOfEntries', 0))
        
        hosts = []
        for i in range(count):
            xml = self._call(cfg['service'], cfg['control'], 'GetGenericHostEntry', {'NewIndex': str(i)})
            host = self._parse_response(xml, 'GetGenericHostEntry')
            if host:
                hosts.append(host)
        return hosts
    
    def device_info(self):
        """Get device info."""
        cfg = self.COMMON_ACTIONS['device']
        xml = self._call(cfg['service'], cfg['control'], 'GetInfo')
        return self._parse_response(xml, 'GetInfo')
    
    def reconnect(self):
        """Force WAN reconnect."""
        cfg = self.COMMON_ACTIONS['wan']
        xml = self._call(cfg['service'], cfg['control'], 'ForceTermination')
        return xml is not None
    
    def _webapi_login(self):
        """Login via web API and return SID."""
        try:
            # Get challenge
            resp = requests.get(f'http://{self.host}/login_sid.lua', timeout=10)
            match = re.search(r'<Challenge>([^<]+)</Challenge>', resp.text)
            if not match:
                return None
            challenge = match.group(1)
            
            # Create response
            text = f'{challenge}-{self.password}'
            text_utf16 = text.encode('utf-16le')
            response_hash = hashlib.md5(text_utf16).hexdigest()
            response = f'{challenge}-{response_hash}'
            
            # Login
            login_url = f'http://{self.host}/login_sid.lua?username={quote(self.user)}&response={response}'
            resp = requests.get(login_url, timeout=10)
            match = re.search(r'<SID>([^<]+)</SID>', resp.text)
            if match:
                sid = match.group(1)
                if sid != '0000000000000000':
                    return sid
        except Exception as e:
            print(f"Login error: {e}", file=sys.stderr)
        return None
    
    def get_smarthome_devices(self):
        """Get smarthome devices via web API."""
        sid = self._webapi_login()
        if not sid:
            return []
        
        try:
            url = f'http://{self.host}/webservices/homeautoswitch.lua?switchcmd=getdevicelistinfos&sid={sid}'
            resp = requests.get(url, timeout=10)
            root = ET.fromstring(resp.text)
            
            devices = []
            for device in root.findall('device'):
                d = {
                    'identifier': device.get('identifier', ''),
                    'id': device.get('id', ''),
                    'name': device.findtext('name', 'Unknown'),
                    'present': device.findtext('present', '0'),
                }
                
                # Switch state
                switch = device.find('switch')
                if switch is not None:
                    d['state'] = switch.findtext('state', '0')
                    d['mode'] = switch.findtext('mode', '')
                
                # Simple on/off state
                simpleonoff = device.find('simpleonoff')
                if simpleonoff is not None:
                    d['simple_state'] = simpleonoff.findtext('state', '0')
                
                # Power meter
                powermeter = device.find('powermeter')
                if powermeter is not None:
                    d['voltage'] = powermeter.findtext('voltage', '0')
                    d['power'] = powermeter.findtext('power', '0')
                    d['energy'] = powermeter.findtext('energy', '0')
                
                # Temperature
                temp = device.find('temperature')
                if temp is not None:
                    d['temperature'] = temp.findtext('celsius', '0')
                
                devices.append(d)
            return devices
        except Exception as e:
            print(f"Error getting devices: {e}", file=sys.stderr)
        return []
    
    def switch_smarthome_device(self, ain, on=True):
        """Switch smarthome device on/off via web API."""
        sid = self._webapi_login()
        if not sid:
            return False
        
        try:
            cmd = 'setswitchon' if on else 'setswitchoff'
            url = f'http://{self.host}/webservices/homeautoswitch.lua?switchcmd={cmd}&ain={quote(ain)}&sid={sid}'
            resp = requests.get(url, timeout=10)
            return resp.text.strip() == '1'
        except Exception as e:
            print(f"Error switching device: {e}", file=sys.stderr)
        return False
    
    def get_dect_devices(self):
        """Get DECT devices (Smarthome)."""
        cfg = self.COMMON_ACTIONS['dect']
        xml = self._call(cfg['service'], cfg['control'], 'GetNumberOfDectEntries')
        result = self._parse_response(xml, 'GetNumberOfDectEntries')
        count = int(result.get('NewNumberOfEntries', 0))
        
        devices = []
        for i in range(count):
            xml = self._call(cfg['service'], cfg['control'], 'GetGenericDectEntry', {'NewIndex': str(i)})
            device = self._parse_response(xml, 'GetGenericDectEntry')
            if device:
                # Get additional info for the device
                ain = device.get('NewAIN') or device.get('NewID')
                if ain:
                    try:
                        xml2 = self._call(cfg['service'], cfg['control'], 'GetSpecificDectEntry', {'NewAIN': ain})
                        extra = self._parse_response(xml2, 'GetSpecificDectEntry')
                        device.update(extra)
                    except:
                        pass
                devices.append(device)
        return devices
    
    def get_homeauto_devices(self):
        """Get Home Automation devices."""
        cfg = self.COMMON_ACTIONS['homeauto']
        xml = self._call(cfg['service'], cfg['control'], 'GetInfo')
        result = self._parse_response(xml, 'GetInfo')
        count = int(result.get('NewNumberOfDevices', 0))
        
        devices = []
        for i in range(count):
            xml = self._call(cfg['service'], cfg['control'], 'GetGenericDeviceInfo', {'NewIndex': str(i)})
            device = self._parse_response(xml, 'GetGenericDeviceInfo')
            if device:
                devices.append(device)
        return devices
    
    def switch_device(self, ain, on=True):
        """Switch a device on/off by AIN."""
        # Try homeauto first
        cfg = self.COMMON_ACTIONS['homeauto']
        action = 'SetSwitchON' if on else 'SetSwitchOFF'
        xml = self._call(cfg['service'], cfg['control'], action, {'NewAIN': ain})
        if xml:
            return True
        
        # Try DECT service as fallback
        cfg = self.COMMON_ACTIONS['dect']
        action = 'SetSwitch' if on else 'SetSwitch'
        xml = self._call(cfg['service'], cfg['control'], 'SetSwitch', {'NewAIN': ain, 'NewSwitchOn': '1' if on else '0'})
        return xml is not None


def main():
    parser = argparse.ArgumentParser(description='FRITZ!Box Control')
    parser.add_argument('--host', default=os.environ.get('FRITZBOX_HOST', 'fritz.box'), help='FRITZ!Box hostname/IP')
    parser.add_argument('--user', '-u', default=os.environ.get('FRITZBOX_USER', ''), help='Username (if configured)')
    parser.add_argument('--password', '-p', default=os.environ.get('FRITZBOX_PASSWORD', ''), help='Password')
    
    subparsers = parser.add_subparsers(dest='command', help='Commands')
    
    # WLAN commands
    wlan_parser = subparsers.add_parser('wlan', help='WLAN control')
    wlan_parser.add_argument('action', choices=['on', 'off', 'status'], help='Action')
    wlan_parser.add_argument('--band', '-b', type=int, default=1, choices=[1, 2, 3], 
                            help='WLAN band (1=2.4GHz, 2=5GHz, 3=guest)')
    
    # Hosts command
    subparsers.add_parser('hosts', help='List connected hosts')
    
    # Info command
    subparsers.add_parser('info', help='Device info')
    
    # Reconnect command
    subparsers.add_parser('reconnect', help='Force WAN reconnect')
    
    # Smarthome command
    smarthome_parser = subparsers.add_parser('smarthome', help='Smarthome devices')
    smarthome_subparsers = smarthome_parser.add_subparsers(dest='smarthome_cmd', help='Smarthome commands')
    
    # List devices
    smarthome_subparsers.add_parser('list', help='List smarthome devices')
    
    # Switch device
    switch_parser = smarthome_subparsers.add_parser('switch', help='Switch device on/off')
    switch_parser.add_argument('ain', help='Device AIN (identifier, use quotes if contains spaces)')
    switch_parser.add_argument('state', choices=['on', 'off'], help='Switch state')
    
    # Toggle device
    toggle_parser = smarthome_subparsers.add_parser('toggle', help='Toggle device on/off')
    toggle_parser.add_argument('ain', help='Device AIN (identifier, use quotes if contains spaces)')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(1)
    
    # Create client
    fb = FritzBox(args.host, args.user, args.password)
    
    if args.command == 'wlan':
        if args.action == 'status':
            status = fb.wlan_status(args.band)
            if status:
                enabled = status.get('NewEnable') == '1'
                ssid = status.get('NewSSID', 'Unknown')
                print(f"WLAN {args.band}: {'ON' if enabled else 'OFF'}")
                print(f"SSID: {ssid}")
            else:
                print("Failed to get status")
                sys.exit(1)
        elif args.action == 'on':
            if fb.wlan_on(args.band):
                print(f"WLAN {args.band} turned ON")
            else:
                print("Failed to turn on WLAN")
                sys.exit(1)
        elif args.action == 'off':
            if fb.wlan_off(args.band):
                print(f"WLAN {args.band} turned OFF")
            else:
                print("Failed to turn off WLAN")
                sys.exit(1)
    
    elif args.command == 'hosts':
        hosts = fb.get_hosts()
        print(f"Connected hosts: {len(hosts)}")
        print()
        for h in hosts:
            name = h.get('NewHostName') or 'Unknown'
            ip = h.get('NewIPAddress') or '-'
            mac = h.get('NewMACAddress') or '-'
            active = 'Yes' if h.get('NewActive') == '1' else 'No'
            print(f"  {name:20} {ip:15} {mac:17} Active: {active}")
    
    elif args.command == 'info':
        info = fb.device_info()
        if info:
            print(f"Model: {info.get('NewModelName', 'Unknown')}")
            print(f"Software: {info.get('NewSoftwareVersion', 'Unknown')}")
            print(f"Serial: {info.get('NewSerialNumber', 'Unknown')}")
        else:
            print("Failed to get info")
            sys.exit(1)
    
    elif args.command == 'reconnect':
        if fb.reconnect():
            print("WAN reconnect initiated")
        else:
            print("Failed to reconnect")
            sys.exit(1)
    
    elif args.command == 'smarthome':
        if args.smarthome_cmd == 'list':
            devices = fb.get_smarthome_devices()
            
            if devices:
                print(f"Smarthome devices: {len(devices)}")
                print()
                for d in devices:
                    name = d.get('name', 'Unknown')
                    ain = d.get('identifier', '-')
                    state = d.get('state', '-')
                    power = d.get('power', '0')
                    voltage = d.get('voltage', '0')
                    temp = d.get('temperature', '0')
                    
                    # Format values
                    state_str = 'ON' if state == '1' else 'OFF' if state == '0' else state
                    try:
                        power_w = f"{int(power) / 100:.1f}W" if power else '-'
                        voltage_v = f"{int(voltage) / 1000:.1f}V" if voltage else '-'
                        temp_c = f"{int(temp) / 10:.1f}°C" if temp else '-'
                    except:
                        power_w = voltage_v = temp_c = '-'
                    
                    print(f"  {name}")
                    print(f"    AIN: {ain}")
                    print(f"    State: {state_str}, Power: {power_w}, Voltage: {voltage_v}, Temp: {temp_c}")
                    print()
            else:
                print("No smarthome devices found")
                
        elif args.smarthome_cmd == 'switch':
            if fb.switch_smarthome_device(args.ain, args.state == 'on'):
                print(f"Device {args.ain} turned {args.state.upper()}")
            else:
                print(f"Failed to switch device {args.ain}")
                sys.exit(1)

        elif args.smarthome_cmd == 'toggle':
            devices = fb.get_smarthome_devices()
            device = next((d for d in devices if d.get('identifier') == args.ain), None)
            if device is None:
                print(f"Device {args.ain} not found")
                sys.exit(1)
            current_state = device.get('state', '0')
            turn_on = current_state != '1'
            if fb.switch_smarthome_device(args.ain, turn_on):
                print(f"Device {args.ain} toggled {'ON' if turn_on else 'OFF'}")
            else:
                print(f"Failed to toggle device {args.ain}")
                sys.exit(1)


if __name__ == '__main__':
    main()
