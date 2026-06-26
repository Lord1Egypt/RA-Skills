import socket
import threading
import time
import os
import sys

# SOTA Integrity: Hardened Self-Destruct Mechanism
IDLE_TIMEOUT = 300  # 5 minutes of total silence
CHECK_INTERVAL = 10
MAX_LIFESPAN = 3600 # 1 hour hard limit for any single relay session

class SecureRelay:
    def __init__(self):
        self.last_activity = time.time()
        self.running = True
        self.connection_count = 0
        self.lock = threading.Lock()

    def pipe(self, source, destination):
        with self.lock:
            self.connection_count += 1
        
        try:
            # Set a timeout on the socket to allow checking self.running status
            source.settimeout(10)
            destination.settimeout(10)
            while self.running:
                try:
                    data = source.recv(4096)
                    if not data: break
                    destination.sendall(data)
                    self.last_activity = time.time()
                except socket.timeout:
                    continue
        except Exception:
            pass
        finally:
            source.close()
            destination.close()
            with self.lock:
                self.connection_count -= 1

    def monitor(self, start_time):
        """Monitor for idle timeout or max lifespan and kill server."""
        while self.running:
            time.sleep(CHECK_INTERVAL)
            idle_time = time.time() - self.last_activity
            total_age = time.time() - start_time
            
            # Condition 1: Total lifespan exceeded
            if total_age > MAX_LIFESPAN:
                print(f"!!! [SECURITY] MAX LIFESPAN ({MAX_LIFESPAN}s) REACHED. SHUTTING DOWN.")
                self.running = False
                break
            
            # Condition 2: Idle timeout reached with no active connections
            if self.connection_count <= 0 and idle_time > IDLE_TIMEOUT:
                print(f"!!! [SECURITY] IDLE TIMEOUT ({IDLE_TIMEOUT}s) EXCEEDED. SHUTTING DOWN.")
                self.running = False
                break

    def start(self, local_port, remote_port):
        print(f"--- [SOTA SECURE TUNNEL] 127.0.0.1:{local_port} -> 127.0.0.1:{remote_port} ---")
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
        # CRITICAL: Set timeout so accept() doesn't block forever
        server.settimeout(5.0)
        
        try:
            server.bind(('127.0.0.1', local_port))
            server.listen(5)
        except Exception as e:
            print(f"Failed to bind port {local_port}: {e}")
            return

        start_time = time.time()
        threading.Thread(target=self.monitor, args=(start_time,), daemon=True).start()
        
        while self.running:
            try:
                client_sock, addr = server.accept()
                self.last_activity = time.time()
                
                try:
                    target_sock = socket.create_connection(('127.0.0.1', remote_port), timeout=5)
                    threading.Thread(target=self.pipe, args=(client_sock, target_sock), daemon=True).start()
                    threading.Thread(target=self.pipe, args=(target_sock, client_sock), daemon=True).start()
                except Exception as e:
                    print(f"[Relay] Failed to connect to target: {e}")
                    client_sock.close()
            except socket.timeout:
                # This allows the loop to check self.running every 5 seconds
                continue
            except Exception as e:
                if self.running:
                    print(f"Server error: {e}")
                break
        
        server.close()
        print("Relay service cleanly terminated.")

if __name__ == "__main__":
    SecureRelay().start(9223, 9222)
