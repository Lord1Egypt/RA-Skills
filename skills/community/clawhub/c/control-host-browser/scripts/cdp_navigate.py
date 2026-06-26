#!/usr/bin/env python3
"""
Send CDP Page.navigate command via WebSocket to a Chrome DevTools endpoint.

Usage: python3 cdp_navigate.py <port> <page_id> <url>

This script:
1. Connects to the Chrome DevTools WebSocket endpoint
2. Performs the WebSocket handshake
3. Sends a CDP Page.navigate command
4. Waits for confirmation and closes
"""

import sys
import json
import time
import socket
import base64

def send_cdp_command(port, page_id, url):
    """Send CDP Page.navigate command to Chrome DevTools endpoint."""
    host = '172.17.0.1'
    path = f'/devtools/page/{page_id}'
    
    # Create socket connection
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.connect((host, int(port)))
    except Exception as e:
        print(f"ERROR: Failed to connect to {host}:{port}: {e}")
        return False
    
    # WebSocket handshake
    key = base64.b64encode(b'OpenClawControlBrowser').decode()
    request = (
        f"GET {path} HTTP/1.1\r\n"
        f"Host: {host}:{port}\r\n"
        "Upgrade: websocket\r\n"
        "Connection: Upgrade\r\n"
        f"Sec-WebSocket-Key: {key}\r\n"
        "Sec-WebSocket-Version: 13\r\n"
        "\r\n"
    )
    sock.send(request.encode())
    
    # Read handshake response
    response = b''
    while b'\r\n\r\n' not in response:
        chunk = sock.recv(1024)
        if not chunk:
            print("ERROR: Connection closed during handshake")
            sock.close()
            return False
        response += chunk
    
    if b'101' not in response:
        print(f"ERROR: Handshake failed: {response.decode()[:200]}")
        sock.close()
        return False
    
    print(f"  WebSocket connected to {page_id}")
    
    # Send CDP command
    command = json.dumps({
        'id': 1,
        'method': 'Page.navigate',
        'params': {'url': url}
    })
    payload = command.encode()
    
    # WebSocket frame: 0x81 (text, masked) + length + mask + masked payload
    mask = b'\x00\x00\x00\x00'  # Simple zero mask
    frame = bytearray()
    frame.append(0x81)  # FIN + text opcode
    frame.append(0x80 | len(payload))  # Masked flag + length
    frame.extend(mask)
    for i, byte in enumerate(payload):
        frame.append(byte ^ mask[i % 4])
    
    sock.send(frame)
    print(f"  Sent navigate command for {url}")
    
    # Wait for response
    time.sleep(0.5)
    try:
        sock.settimeout(2.0)
        response = sock.recv(4096)
        if response:
            # Parse WebSocket frame to get payload
            if len(response) > 2 and (response[0] & 0x80):
                length = response[1] & 0x7F
                if length == 126:
                    length = int.from_bytes(response[2:4], 'big')
                    mask_offset = 4
                elif length == 127:
                    length = int.from_bytes(response[2:10], 'big')
                    mask_offset = 10
                else:
                    mask_offset = 2
                
                if len(response) > mask_offset + 4:
                    mask = response[mask_offset:mask_offset+4]
                    data_start = mask_offset + 4
                    payload_bytes = bytearray(response[data_start:data_start+length])
                    for i in range(len(payload_bytes)):
                        payload_bytes[i] ^= mask[i % 4]
                    
                    try:
                        result = json.loads(payload_bytes.decode())
                        if 'result' in result:
                            print(f"  Navigation confirmed: frameId={result['result'].get('frameId', 'N/A')}")
                        elif 'error' in result:
                            print(f"  Navigation error: {result['error']}")
                    except json.JSONDecodeError:
                        pass
    except socket.timeout:
        print("  Response timeout (navigation may still be in progress)")
    except Exception as e:
        print(f"  Error reading response: {e}")
    
    sock.close()
    print("  Done")
    return True

if __name__ == '__main__':
    if len(sys.argv) != 4:
        print(f"Usage: {sys.argv[0]} <port> <pageId> <url>")
        sys.exit(1)
    
    port = sys.argv[1]
    page_id = sys.argv[2]
    url = sys.argv[3]
    
    success = send_cdp_command(port, page_id, url)
    sys.exit(0 if success else 1)
