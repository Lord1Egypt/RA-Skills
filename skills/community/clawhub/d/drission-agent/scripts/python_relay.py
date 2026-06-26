import socket
import threading
import time
import os
import sys

# v2.1.0 SOTA Fortress: HARDENED GLOBAL GATE
if os.environ.get('SOTA_NUCLEAR_CONFIRMED') != 'true':
    print("!!! [SECURITY ABORT] RELAY BLOCKED. Use secure_wrapper.py.")
    sys.exit(1)

IDLE_TIMEOUT = 300 
MAX_LIFESPAN = 3600 

class SecureRelay:
    def __init__(self):
        self.last_activity = time.time()
        self.running = True
        self.connection_count = 0
        self.lock = threading.Lock()

    def pipe(self, source, destination):
        with self.lock: self.connection_count += 1
        try:
            source.settimeout(10)
            while self.running:
                try:
                    data = source.recv(4096)
                    if not data: break
                    destination.sendall(data)
                    self.last_activity = time.time()
                except socket.timeout: continue
        except: pass
        finally:
            source.close()
            destination.close()
            with self.lock: self.connection_count -= 1

    def monitor(self, start_time):
        while self.running:
            time.sleep(10)
            if time.time() - start_time > MAX_LIFESPAN or (self.connection_count <= 0 and time.time() - self.last_activity > IDLE_TIMEOUT):
                self.running = False
                try: socket.create_connection(('127.0.0.1', 9223), timeout=1)
                except: pass

    def start(self, local_port, remote_port):
        print(f"--- [SOTA SECURE TUNNEL] 127.0.0.1:{local_port} -> {remote_port} ---")
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.settimeout(5.0)
        try:
            server.bind(('127.0.0.1', local_port))
            server.listen(5)
            start_time = time.time()
            threading.Thread(target=self.monitor, args=(start_time,), daemon=True).start()
            while self.running:
                try:
                    client_sock, _ = server.accept()
                    target_sock = socket.create_connection(('127.0.0.1', remote_port), timeout=5)
                    threading.Thread(target=self.pipe, args=(client_sock, target_sock), daemon=True).start()
                    threading.Thread(target=self.pipe, args=(target_sock, client_sock), daemon=True).start()
                except socket.timeout: continue
            server.close()
            print("Relay service cleanly terminated.")
        except Exception as e: print(f"Error: {e}")

if __name__ == "__main__":
    SecureRelay().start(9223, 9222)
