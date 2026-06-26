# -*- coding: utf-8 -*-
"""
Web UI Module - Public API
===========================

Provides web server startup for the Web UI interface.
"""

import sys
from pathlib import Path


def start_web_ui(
    host: str = '0.0.0.0',
    port: int = 5000,
    debug: bool = False,
):
    """
    Start the Web UI server.
    
    Args:
        host: Host to bind to (default: 0.0.0.0)
        port: Port to listen on (default: 5000)
        debug: Enable debug mode
    """
    try:
        import flask
        from flask_socketio import SocketIO
        
        # Import Web UI app
        web_ui_dir = Path(__file__).parent.parent / 'web-ui'
        if not web_ui_dir.exists():
            raise ImportError("Web UI directory not found")
        
        # Add web-ui to path and import app
        sys.path.insert(0, str(web_ui_dir.parent))
        
        from web_ui.app import app as flask_app, socketio
        
        print(f"\n🚀 Starting Auto Video Generator Web UI...")
        print(f"   URL: http://{host}:{port}")
        print(f"   Debug: {debug}\n")
        
        socketio.run(flask_app, host=host, port=port, debug=debug)
        
    except ImportError as e:
        print(f"\n❌ Error starting Web UI:")
        print(f"   Missing dependency: {e}")
        print(f"\n   Install with: pip install auto-video-generator[web]")
        sys.exit(1)


__all__ = ['start_web_ui']
