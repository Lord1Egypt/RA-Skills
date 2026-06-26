#!/usr/bin/env python3
import argparse
import html
import json
import mimetypes
import os
import signal
import socket
import struct
import threading
import time
import uuid
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import quote, urlparse
from xml.etree import ElementTree as ET

AUDIO_EXTS = {'.mp3', '.m4a', '.aac', '.wav', '.flac', '.aiff', '.ogg'}
STATE_DIR = Path.home() / '.openclaw' / 'state'
STATE_FILE = STATE_DIR / 'simple-dlna-server.json'
URN_DEVICE = 'urn:schemas-upnp-org:device:MediaServer:1'
URN_CONTENT = 'urn:schemas-upnp-org:service:ContentDirectory:1'
URN_CONN = 'urn:schemas-upnp-org:service:ConnectionManager:1'


def save_state(data):
    STATE_DIR.mkdir(parents=True, exist_ok=True)
    STATE_FILE.write_text(json.dumps(data, ensure_ascii=False, indent=2))


def load_state():
    if not STATE_FILE.exists():
        return {}
    try:
        return json.loads(STATE_FILE.read_text())
    except Exception:
        return {}


def local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('8.8.8.8', 80))
        return s.getsockname()[0]
    finally:
        s.close()


def resolve_roots(root_args):
    roots = []
    for raw in root_args or []:
        root = Path(os.path.expanduser(raw)).resolve()
        if not root.exists() or not root.is_dir():
            raise FileNotFoundError(root)
        roots.append(root)
    if not roots:
        raise ValueError('At least one --root path is required')
    return roots


def scan_library(roots):
    items = []
    seen = set()
    for root in roots:
        for p in root.rglob('*'):
            if not (p.is_file() and p.suffix.lower() in AUDIO_EXTS):
                continue
            rp = str(p.resolve())
            if rp in seen:
                continue
            seen.add(rp)
            rel = p.relative_to(root)
            items.append({
                'id': str(len(items) + 1),
                'name': p.stem,
                'path': rp,
                'root': str(root),
                'rel': str(rel).replace('\\', '/'),
                'size': p.stat().st_size,
                'mime': mimetypes.guess_type(str(p))[0] or 'application/octet-stream',
            })
    return items


def xml_text(tag, text):
    return f'<{tag}>{html.escape(str(text))}</{tag}>'


def didl_for_items(base_url: str, items):
    out = [
        '<DIDL-Lite xmlns="urn:schemas-upnp-org:metadata-1-0/DIDL-Lite/" '
        'xmlns:dc="http://purl.org/dc/elements/1.1/" '
        'xmlns:upnp="urn:schemas-upnp-org:metadata-1-0/upnp/">'
    ]
    for item in items:
        url = f'{base_url}/media/{quote(item["id"])}'
        out.append(
            f'<item id="{html.escape(item["id"])}" parentID="0" restricted="1">'
            f'{xml_text("dc:title", item["name"])}'
            '<upnp:class>object.item.audioItem.musicTrack</upnp:class>'
            f'<res protocolInfo="http-get:*:{html.escape(item["mime"])}:*" size="{item["size"]}">{html.escape(url)}</res>'
            '</item>'
        )
    out.append('</DIDL-Lite>')
    return ''.join(out)


def browse_response(base_url: str, items, object_id: str, start_index: int, count: int):
    if object_id != '0':
        selected = [x for x in items if x['id'] == object_id]
    else:
        selected = items
    total = len(selected)
    if count == 0:
        page = selected[start_index:]
    else:
        page = selected[start_index:start_index + count]
    didl = didl_for_items(base_url, page)
    return (
        '<u:BrowseResponse xmlns:u="urn:schemas-upnp-org:service:ContentDirectory:1">'
        f'{xml_text("Result", didl)}'
        f'{xml_text("NumberReturned", len(page))}'
        f'{xml_text("TotalMatches", total)}'
        f'{xml_text("UpdateID", 1)}'
        '</u:BrowseResponse>'
    )


def soap_envelope(body: str):
    return (
        '<?xml version="1.0" encoding="utf-8"?>'
        '<s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/" '
        's:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/">'
        f'<s:Body>{body}</s:Body>'
        '</s:Envelope>'
    ).encode('utf-8')


class DlnaHandler(BaseHTTPRequestHandler):
    server_version = 'OpenClawDLNA/0.1'

    def log_message(self, fmt, *args):
        print('HTTP', self.address_string(), fmt % args, flush=True)

    @property
    def state(self):
        return self.server.state

    def do_GET(self):
        parsed = urlparse(self.path)
        if parsed.path == '/description.xml':
            self.send_xml(self.device_description())
            return
        if parsed.path == '/scpd/content_directory.xml':
            self.send_xml(self.content_scpd())
            return
        if parsed.path == '/scpd/connection_manager.xml':
            self.send_xml(self.conn_scpd())
            return
        if parsed.path.startswith('/media/'):
            media_id = parsed.path.split('/')[-1]
            item = next((x for x in self.state['items'] if x['id'] == media_id), None)
            if not item:
                self.send_error(404, 'Not found')
                return
            path = Path(item['path'])
            if not path.exists():
                self.send_error(404, 'File missing')
                return
            self.send_response(200)
            self.send_header('Content-Type', item['mime'])
            self.send_header('Content-Length', str(item['size']))
            self.send_header('Accept-Ranges', 'bytes')
            self.end_headers()
            with path.open('rb') as f:
                while True:
                    chunk = f.read(1024 * 64)
                    if not chunk:
                        break
                    self.wfile.write(chunk)
            return
        self.send_error(404, 'Not found')

    def do_POST(self):
        parsed = urlparse(self.path)
        length = int(self.headers.get('Content-Length', '0'))
        body = self.rfile.read(length)
        if parsed.path == '/upnp/control/content_directory':
            self.handle_content_directory(body)
            return
        if parsed.path == '/upnp/control/connection_manager':
            self.handle_connection_manager(body)
            return
        self.send_error(404, 'Not found')

    def send_xml(self, text: str):
        data = text.encode('utf-8')
        self.send_response(200)
        self.send_header('Content-Type', 'text/xml; charset="utf-8"')
        self.send_header('Content-Length', str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def device_description(self):
        base = self.state['base_url']
        udn = self.state['udn']
        name = self.state['name']
        return f'''<?xml version="1.0"?>
<root xmlns="urn:schemas-upnp-org:device-1-0">
  <specVersion><major>1</major><minor>0</minor></specVersion>
  <URLBase>{html.escape(base)}/</URLBase>
  <device>
    <deviceType>{URN_DEVICE}</deviceType>
    <friendlyName>{html.escape(name)}</friendlyName>
    <manufacturer>OpenClaw</manufacturer>
    <manufacturerURL>https://docs.openclaw.ai</manufacturerURL>
    <modelDescription>OpenClaw simple audio DLNA server</modelDescription>
    <modelName>OpenClaw DLNA</modelName>
    <modelNumber>0.1</modelNumber>
    <UDN>{html.escape(udn)}</UDN>
    <serviceList>
      <service>
        <serviceType>{URN_CONTENT}</serviceType>
        <serviceId>urn:upnp-org:serviceId:ContentDirectory</serviceId>
        <SCPDURL>/scpd/content_directory.xml</SCPDURL>
        <controlURL>/upnp/control/content_directory</controlURL>
        <eventSubURL>/upnp/event/content_directory</eventSubURL>
      </service>
      <service>
        <serviceType>{URN_CONN}</serviceType>
        <serviceId>urn:upnp-org:serviceId:ConnectionManager</serviceId>
        <SCPDURL>/scpd/connection_manager.xml</SCPDURL>
        <controlURL>/upnp/control/connection_manager</controlURL>
        <eventSubURL>/upnp/event/connection_manager</eventSubURL>
      </service>
    </serviceList>
  </device>
</root>'''

    def content_scpd(self):
        return '''<?xml version="1.0"?>
<scpd xmlns="urn:schemas-upnp-org:service-1-0">
  <specVersion><major>1</major><minor>0</minor></specVersion>
  <actionList>
    <action><name>Browse</name><argumentList>
      <argument><name>ObjectID</name><direction>in</direction><relatedStateVariable>A_ARG_TYPE_ObjectID</relatedStateVariable></argument>
      <argument><name>BrowseFlag</name><direction>in</direction><relatedStateVariable>A_ARG_TYPE_BrowseFlag</relatedStateVariable></argument>
      <argument><name>Filter</name><direction>in</direction><relatedStateVariable>A_ARG_TYPE_Filter</relatedStateVariable></argument>
      <argument><name>StartingIndex</name><direction>in</direction><relatedStateVariable>A_ARG_TYPE_Index</relatedStateVariable></argument>
      <argument><name>RequestedCount</name><direction>in</direction><relatedStateVariable>A_ARG_TYPE_Count</relatedStateVariable></argument>
      <argument><name>SortCriteria</name><direction>in</direction><relatedStateVariable>A_ARG_TYPE_SortCriteria</relatedStateVariable></argument>
      <argument><name>Result</name><direction>out</direction><relatedStateVariable>A_ARG_TYPE_Result</relatedStateVariable></argument>
      <argument><name>NumberReturned</name><direction>out</direction><relatedStateVariable>A_ARG_TYPE_Count</relatedStateVariable></argument>
      <argument><name>TotalMatches</name><direction>out</direction><relatedStateVariable>A_ARG_TYPE_Count</relatedStateVariable></argument>
      <argument><name>UpdateID</name><direction>out</direction><relatedStateVariable>A_ARG_TYPE_UpdateID</relatedStateVariable></argument>
    </argumentList></action>
    <action><name>GetSearchCapabilities</name><argumentList><argument><name>SearchCaps</name><direction>out</direction><relatedStateVariable>SearchCapabilities</relatedStateVariable></argument></argumentList></action>
    <action><name>GetSortCapabilities</name><argumentList><argument><name>SortCaps</name><direction>out</direction><relatedStateVariable>SortCapabilities</relatedStateVariable></argument></argumentList></action>
    <action><name>GetSystemUpdateID</name><argumentList><argument><name>Id</name><direction>out</direction><relatedStateVariable>SystemUpdateID</relatedStateVariable></argument></argumentList></action>
  </actionList>
  <serviceStateTable>
    <stateVariable sendEvents="no"><name>A_ARG_TYPE_ObjectID</name><dataType>string</dataType></stateVariable>
    <stateVariable sendEvents="no"><name>A_ARG_TYPE_BrowseFlag</name><dataType>string</dataType></stateVariable>
    <stateVariable sendEvents="no"><name>A_ARG_TYPE_Filter</name><dataType>string</dataType></stateVariable>
    <stateVariable sendEvents="no"><name>A_ARG_TYPE_Index</name><dataType>ui4</dataType></stateVariable>
    <stateVariable sendEvents="no"><name>A_ARG_TYPE_Count</name><dataType>ui4</dataType></stateVariable>
    <stateVariable sendEvents="no"><name>A_ARG_TYPE_SortCriteria</name><dataType>string</dataType></stateVariable>
    <stateVariable sendEvents="no"><name>A_ARG_TYPE_Result</name><dataType>string</dataType></stateVariable>
    <stateVariable sendEvents="no"><name>A_ARG_TYPE_UpdateID</name><dataType>ui4</dataType></stateVariable>
    <stateVariable sendEvents="no"><name>SearchCapabilities</name><dataType>string</dataType></stateVariable>
    <stateVariable sendEvents="no"><name>SortCapabilities</name><dataType>string</dataType></stateVariable>
    <stateVariable sendEvents="no"><name>SystemUpdateID</name><dataType>ui4</dataType></stateVariable>
  </serviceStateTable>
</scpd>'''

    def conn_scpd(self):
        return '''<?xml version="1.0"?>
<scpd xmlns="urn:schemas-upnp-org:service-1-0">
  <specVersion><major>1</major><minor>0</minor></specVersion>
  <actionList>
    <action><name>GetProtocolInfo</name><argumentList>
      <argument><name>Source</name><direction>out</direction><relatedStateVariable>SourceProtocolInfo</relatedStateVariable></argument>
      <argument><name>Sink</name><direction>out</direction><relatedStateVariable>SinkProtocolInfo</relatedStateVariable></argument>
    </argumentList></action>
    <action><name>GetCurrentConnectionIDs</name><argumentList>
      <argument><name>ConnectionIDs</name><direction>out</direction><relatedStateVariable>CurrentConnectionIDs</relatedStateVariable></argument>
    </argumentList></action>
  </actionList>
  <serviceStateTable>
    <stateVariable sendEvents="no"><name>SourceProtocolInfo</name><dataType>string</dataType></stateVariable>
    <stateVariable sendEvents="no"><name>SinkProtocolInfo</name><dataType>string</dataType></stateVariable>
    <stateVariable sendEvents="no"><name>CurrentConnectionIDs</name><dataType>string</dataType></stateVariable>
  </serviceStateTable>
</scpd>'''

    def handle_content_directory(self, body: bytes):
        try:
            root = ET.fromstring(body)
        except Exception:
            self.send_error(400, 'Bad XML')
            return
        for elem in root.iter():
            if elem.tag.endswith('Browse'):
                vals = {child.tag.split('}')[-1]: (child.text or '') for child in elem}
                xml = browse_response(
                    self.state['base_url'],
                    self.state['items'],
                    vals.get('ObjectID', '0'),
                    int(vals.get('StartingIndex', '0') or 0),
                    int(vals.get('RequestedCount', '0') or 0),
                )
                self.send_xml(soap_envelope(xml).decode('utf-8'))
                return
            if elem.tag.endswith('GetSearchCapabilities'):
                self.send_xml(soap_envelope('<u:GetSearchCapabilitiesResponse xmlns:u="urn:schemas-upnp-org:service:ContentDirectory:1"><SearchCaps></SearchCaps></u:GetSearchCapabilitiesResponse>').decode('utf-8'))
                return
            if elem.tag.endswith('GetSortCapabilities'):
                self.send_xml(soap_envelope('<u:GetSortCapabilitiesResponse xmlns:u="urn:schemas-upnp-org:service:ContentDirectory:1"><SortCaps></SortCaps></u:GetSortCapabilitiesResponse>').decode('utf-8'))
                return
            if elem.tag.endswith('GetSystemUpdateID'):
                self.send_xml(soap_envelope('<u:GetSystemUpdateIDResponse xmlns:u="urn:schemas-upnp-org:service:ContentDirectory:1"><Id>1</Id></u:GetSystemUpdateIDResponse>').decode('utf-8'))
                return
        self.send_error(400, 'Unsupported action')

    def handle_connection_manager(self, body: bytes):
        text = body.decode('utf-8', 'ignore')
        if 'GetProtocolInfo' in text:
            src = ','.join(sorted({f'http-get:*:{x["mime"]}:*' for x in self.state['items']}))
            xml = f'<u:GetProtocolInfoResponse xmlns:u="urn:schemas-upnp-org:service:ConnectionManager:1"><Source>{html.escape(src)}</Source><Sink></Sink></u:GetProtocolInfoResponse>'
            self.send_xml(soap_envelope(xml).decode('utf-8'))
            return
        if 'GetCurrentConnectionIDs' in text:
            xml = '<u:GetCurrentConnectionIDsResponse xmlns:u="urn:schemas-upnp-org:service:ConnectionManager:1"><ConnectionIDs></ConnectionIDs></u:GetCurrentConnectionIDsResponse>'
            self.send_xml(soap_envelope(xml).decode('utf-8'))
            return
        self.send_error(400, 'Unsupported action')


class SsdpResponder(threading.Thread):
    daemon = True

    def __init__(self, host: str, port: int, udn: str):
        super().__init__()
        self.host = host
        self.port = port
        self.udn = udn
        self.stop_event = threading.Event()

    def run(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        try:
            sock.bind(('', 1900))
        except Exception:
            return
        mreq = struct.pack('4sl', socket.inet_aton('239.255.255.250'), socket.INADDR_ANY)
        sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)
        sock.settimeout(1)
        location = f'http://{self.host}:{self.port}/description.xml'
        while not self.stop_event.is_set():
            try:
                data, addr = sock.recvfrom(2048)
            except socket.timeout:
                continue
            text = data.decode('utf-8', 'ignore')
            if 'M-SEARCH' not in text or 'ssdp:discover' not in text.lower():
                continue
            if 'upnp:rootdevice' in text or 'ssdp:all' in text.lower() or 'MediaServer:1' in text:
                for st in ['upnp:rootdevice', URN_DEVICE, self.udn]:
                    resp = (
                        'HTTP/1.1 200 OK\r\n'
                        'CACHE-CONTROL: max-age=1800\r\n'
                        'EXT:\r\n'
                        f'LOCATION: {location}\r\n'
                        'SERVER: OpenClaw/1.0 UPnP/1.0 OpenClawDLNA/0.1\r\n'
                        f'ST: {st}\r\n'
                        f'USN: {self.udn}::{st}\r\n\r\n'
                    )
                    sock.sendto(resp.encode('utf-8'), addr)
        sock.close()

    def stop(self):
        self.stop_event.set()


def cmd_scan(args):
    roots = resolve_roots(args.root)
    items = scan_library(roots)
    print(json.dumps({'roots': [str(r) for r in roots], 'count': len(items), 'sample': items[:args.limit]}, ensure_ascii=False, indent=2))
    return 0


def cmd_serve(args):
    roots = resolve_roots(args.root)
    host = args.host or local_ip()
    port = args.port
    items = scan_library(roots)
    udn = f'uuid:{uuid.uuid4()}'
    default_name = roots[0].name if len(roots) == 1 else f'{roots[0].name} + {len(roots)-1} more'
    name = args.name or f'OpenClaw DLNA ({default_name})'
    state = {
        'roots': [str(r) for r in roots],
        'items': items,
        'host': host,
        'port': port,
        'udn': udn,
        'name': name,
        'base_url': f'http://{host}:{port}',
        'pid': os.getpid(),
        'startedAt': int(time.time()),
    }
    save_state(state)
    httpd = ThreadingHTTPServer((host, port), DlnaHandler)
    httpd.state = state
    ssdp = SsdpResponder(host, port, udn)
    ssdp.start()
    print(json.dumps({'status': 'serving', 'description': f'http://{host}:{port}/description.xml', 'items': len(items), 'friendlyName': name}, ensure_ascii=False, indent=2), flush=True)

    def shutdown(*_):
        ssdp.stop()
        threading.Thread(target=httpd.shutdown, daemon=True).start()

    signal.signal(signal.SIGTERM, shutdown)
    signal.signal(signal.SIGINT, shutdown)
    try:
        httpd.serve_forever()
    finally:
        ssdp.stop()
    return 0


def cmd_status(args):
    print(json.dumps(load_state(), ensure_ascii=False, indent=2))
    return 0


def cmd_stop(args):
    st = load_state()
    pid = st.get('pid')
    if not pid:
        print(json.dumps({'stopped': False, 'reason': 'no recorded pid'}, ensure_ascii=False, indent=2))
        return 0
    try:
        os.kill(pid, signal.SIGTERM)
        print(json.dumps({'stopped': True, 'pid': pid}, ensure_ascii=False, indent=2))
    except ProcessLookupError:
        print(json.dumps({'stopped': False, 'reason': 'process not found', 'pid': pid}, ensure_ascii=False, indent=2))
    return 0


def main():
    parser = argparse.ArgumentParser(description='Minimal DLNA/UPnP audio MediaServer for local folders.')
    sub = parser.add_subparsers(dest='cmd', required=True)

    p = sub.add_parser('scan')
    p.add_argument('--root', action='append', required=True, help='Music directory to include. Repeat for multiple roots.')
    p.add_argument('--limit', type=int, default=20)
    p.set_defaults(func=cmd_scan)

    p = sub.add_parser('serve')
    p.add_argument('--root', action='append', required=True, help='Music directory to include. Repeat for multiple roots.')
    p.add_argument('--host', help='LAN IP to bind to; auto-detected by default')
    p.add_argument('--port', type=int, default=8200)
    p.add_argument('--name', help='DLNA friendly name')
    p.set_defaults(func=cmd_serve)

    p = sub.add_parser('status')
    p.set_defaults(func=cmd_status)

    p = sub.add_parser('stop')
    p.set_defaults(func=cmd_stop)

    args = parser.parse_args()
    return args.func(args)


if __name__ == '__main__':
    raise SystemExit(main())
