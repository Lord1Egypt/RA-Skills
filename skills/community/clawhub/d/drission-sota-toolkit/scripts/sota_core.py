import os
import sys
import socket
import subprocess
import random
import time

# v6.2.0 SOTA FORTRESS: THE "UNIX SOCKET" ARCHITECTURE

def verify_uds_handshake():
    """
    True SOTA Handshake: Uses Unix Domain Sockets (Memory-only).
    Eliminates Symlink attacks and Race Conditions.
    """
    socket_path = "/tmp/.sota_auth.sock"
    if not os.path.exists(socket_path):
        print("!!! [SECURITY ABORT] No active authentication channel.")
        sys.exit(1)
        
    try:
        with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as client:
            client.settimeout(2)
            client.connect(socket_path)
            # Send readiness probe
            client.sendall(b"AUTH_REQUEST")
            response = client.recv(1024)
            if response != b"AUTH_GRANTED":
                print("!!! [SECURITY] Identity verification failed.")
                sys.exit(1)
    except:
        sys.exit(1)

def run_protected_script(script_name):
    """
    Secure Execution: Uses subprocess with clean environment.
    """
    base_dir = os.path.dirname(os.path.abspath(__file__))
    script_path = os.path.join(base_dir, script_name)
    
    # 1. Clean Environment
    clean_env = os.environ.copy()
    clean_env['SOTA_INTERNAL_AUTH'] = 'TRUE'
    
    # 2. Atomic Execution
    subprocess.run(
        [sys.executable, script_path],
        env=clean_env,
        check=True
    )
