import os
import sys
import time

# Standardized SOTA Security Lock
def verify_access_control():
    """
    Mandatory physical lock check for high-risk scripts.
    """
    token_path = os.path.join(os.path.expanduser("~"), ".openclaw/tmp/sota_active.lock")
    if not os.path.exists(token_path):
        print("!!! Access denied. Mandatory human authorization required via secure_wrapper.py.")
        sys.exit(1)
        
    # Check for token expiration (60 seconds)
    if time.time() - os.path.getmtime(token_path) > 60:
        print("!!! Security token expired. Please re-authorize.")
        sys.exit(1)
