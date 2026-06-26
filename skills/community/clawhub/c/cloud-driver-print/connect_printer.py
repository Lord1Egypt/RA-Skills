from __future__ import annotations

import argparse
import socket
import time


def test_connection(host: str, port: int, timeout: float) -> tuple[bool, float, str]:
    """测试指定打印机地址是否可以建立 TCP 连接。"""
    start = time.perf_counter()
    try:
        with socket.create_connection((host, port), timeout=timeout):
            latency_ms = (time.perf_counter() - start) * 1000
            return True, latency_ms, "连接成功"
    except OSError as exc:
        latency_ms = (time.perf_counter() - start) * 1000
        return False, latency_ms, str(exc)


def main() -> None:
    parser = argparse.ArgumentParser(description="测试打印机 TCP 端口是否可访问。")
    parser.add_argument("ip", help="打印机 IP 地址。")
    parser.add_argument("--port", type=int, default=9100, help="打印机端口，默认 9100。")
    parser.add_argument("--timeout", type=float, default=3.0, help="连接超时时间，单位秒。")
    args = parser.parse_args()

    ok, latency_ms, message = test_connection(args.ip, args.port, args.timeout)
    status = "OK" if ok else "FAILED"
    print(f"{status} {args.ip}:{args.port} {latency_ms:.1f}ms {message}")
    if not ok:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
