import socket
import sys

def scan_port(host, port):
    """Attempts to connect to a given port on a host."""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)  # 1 second timeout
        result = sock.connect_ex((host, port))
        if result == 0:
            print(f"Port {port} is open on {host}")
            return True
        else:
            # print(f"Port {port} is closed on {host}")
            return False
        sock.close()
    except socket.gaierror:
        print("Hostname could not be resolved.")
        sys.exit(1)
    except socket.error:
        print("Couldn\'t connect to server.")
        sys.exit(1)
    return False

def main():
    if len(sys.argv) < 3:
        print("Usage: python3 port_scanner.py <host> <port1> [port2 ...]")
        sys.exit(1)

    host = sys.argv[1]
    ports = [int(p) for p in sys.argv[2:]]

    print(f"Scanning ports on {host}...")
    for port in ports:
        scan_port(host, port)

if __name__ == "__main__":
    main()
