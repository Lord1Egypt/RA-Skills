#!/usr/bin/env python3
"""
Redis Stream 广播脚本 - 资源更新通知
用法: python broadcast_redis.py --type TYPE --id RESOURCE_ID --version VERSION --action ACTION
"""

import argparse
import os
import sys
from datetime import datetime


def broadcast_resource_update(resource_type, resource_id, version, update_type):
    """
    广播资源更新到 Redis Stream

    Args:
        resource_type: 资源类型 (hotel/car/attraction/activity/spa/club/restaurant/tea)
        resource_id: 资源唯一标识
        version: 版本号 (如 v1, v2)
        update_type: 更新类型 (INSERT/UPDATE/DELETE)
    """
    try:
        import redis
    except ImportError:
        print("[SKIP] redis not installed, broadcast skipped")
        return True  # graceful degradation, not a failure

    # Redis 连接配置
    REDIS_HOST = os.environ.get("REDIS_HOST", "localhost")
    REDIS_PORT = int(os.environ.get("REDIS_PORT", 6379))
    REDIS_STREAM = "resource_stream"

    try:
        r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)
        r.ping()  # 测试连接
    except redis.ConnectionError:
        print(f"[ERROR] Cannot connect to Redis ({REDIS_HOST}:{REDIS_PORT})")
        print("[ERROR] Make sure Redis is running, or set REDIS_HOST / REDIS_PORT env vars")
        return False

    message = {
        "resource_type": resource_type,
        "resource_id": str(resource_id),
        "version": str(version),
        "update_type": update_type,
        "timestamp": datetime.now().isoformat(),
        "source": "xingyue_agent"
    }

    try:
        stream_id = r.xadd(REDIS_STREAM, message)
        print(f"[OK] Broadcast sent")
        print(f"   Stream: {REDIS_STREAM}")
        print(f"   ID: {stream_id}")
        print(f"   资源类型: {resource_type}")
        print(f"   资源ID: {resource_id}")
        print(f"   版本: {version}")
        print(f"   操作: {update_type}")
        print(f"   时间: {message['timestamp']}")
        return True
    except Exception as e:
        print(f"[ERROR] Broadcast failed: {e}")
        return False


def main():
    parser = argparse.ArgumentParser(description="Redis Stream 资源更新广播")
    parser.add_argument("--type", "-t", required=True,
                        choices=["hotel", "car", "attraction", "activity", "spa", "club", "restaurant", "tea"],
                        help="资源类型")
    parser.add_argument("--id", "-i", required=True,
                        help="资源唯一标识")
    parser.add_argument("--version", "-v", default="v1",
                        help="版本号 (默认: v1)")
    parser.add_argument("--action", "-a", required=True,
                        choices=["INSERT", "UPDATE", "DELETE"],
                        help="更新操作类型")

    args = parser.parse_args()

    success = broadcast_resource_update(
        resource_type=args.type,
        resource_id=args.id,
        version=args.version,
        update_type=args.action
    )

    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
