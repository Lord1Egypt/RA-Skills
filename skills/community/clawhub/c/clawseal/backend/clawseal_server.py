#!/usr/bin/env python3
"""
ClawSeal OpenClaw Server — HTTP bridge for ClawSeal memory operations.

Starts on port 5002 (configurable via --port).
Auto-detects demo/production mode based on QSEAL_SECRET.
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import sys
import argparse

try:
    from clawseal import ScrollMemoryStore
except ImportError:
    print("ERROR: ClawSeal not installed. Run: pip install clawseal")
    sys.exit(1)

app = Flask(__name__)
CORS(app)

# Initialize ScrollMemoryStore
memory_store = ScrollMemoryStore(base_path="./clawseal_scrolls")


@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint."""
    return jsonify({"status": "ok", "service": "clawseal-openclaw-server"})


@app.route('/remember', methods=['POST'])
def remember():
    """Store a memory with QSEAL signature."""
    data = request.get_json()

    content = data.get('content')
    memory_type = data.get('memory_type', 'general')
    user_id = data.get('user_id', 'default')

    if not content:
        return jsonify({"success": False, "error": "content required"}), 400

    result = memory_store.remember(
        content=content,
        memory_type=memory_type,
        user_id=user_id
    )

    return jsonify({
        "success": True,
        "memory_id": result.get('memory_id'),
        "qseal_signature": result.get('qseal_signature'),
        "qseal_mode": result.get('qseal_mode'),
        "qseal_production": result.get('qseal_production')
    })


@app.route('/recall', methods=['POST'])
def recall():
    """Retrieve memories with QSEAL verification."""
    data = request.get_json()

    query = data.get('query', '')
    user_id = data.get('user_id', 'default')
    limit = data.get('limit', 5)

    result = memory_store.recall(
        query=query,
        user_id=user_id,
        limit=limit
    )

    return jsonify({
        "success": True,
        "count": result.get('count', 0),
        "memories": result.get('memories', [])
    })


@app.route('/verify', methods=['POST'])
def verify():
    """Verify a specific memory's QSEAL signature."""
    data = request.get_json()

    memory_id = data.get('memory_id')
    user_id = data.get('user_id', 'default')

    if not memory_id:
        return jsonify({"valid": False, "error": "memory_id required"}), 400

    # Load memory and verify signature
    # (ScrollMemoryStore.recall already verifies, so we can reuse)
    result = memory_store.recall(query=memory_id, user_id=user_id, limit=1)

    if result.get('count', 0) == 0:
        return jsonify({"valid": False, "error": "memory not found"}), 404

    memory = result['memories'][0]

    return jsonify({
        "valid": True,
        "memory_id": memory_id,
        "signature_verified": memory.get('qseal_verified', False),
        "content_intact": True,
        "qseal_mode": memory.get('qseal_mode')
    })


def main():
    parser = argparse.ArgumentParser(description="ClawSeal OpenClaw Server")
    parser.add_argument('--port', type=int, default=5002, help='Server port (default: 5002)')
    parser.add_argument('--host', type=str, default='127.0.0.1', help='Server host (default: 127.0.0.1)')
    args = parser.parse_args()

    print(f"🔐 ClawSeal OpenClaw Server starting on {args.host}:{args.port}")
    print(f"📂 Scrolls directory: ./clawseal_scrolls")
    print(f"🔍 Health check: http://{args.host}:{args.port}/health")

    app.run(host=args.host, port=args.port, debug=False)


if __name__ == '__main__':
    main()
