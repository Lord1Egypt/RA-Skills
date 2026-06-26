#!/usr/bin/env python3
"""Build FastEdge Rust app and optionally deploy."""
import subprocess
import sys
import os
import requests

def build():
    """Build the Wasm binary."""
    # Check for wasm32-wasip1 target
    result = subprocess.run(
        ["rustup", "target", "add", "wasm32-wasip1"],
        capture_output=True,
        text=True
    )
    
    # Build
    result = subprocess.run(
        ["cargo", "build", "--release"],
        capture_output=True,
        text=True
    )
    
    if result.returncode != 0:
        print(f"Build failed:\n{result.stderr}")
        sys.exit(1)
    
    # Find the wasm file
    name = os.path.basename(os.getcwd())
    wasm_path = f"target/wasm32-wasip1/release/{name.replace('-', '_')}.wasm"
    
    if not os.path.exists(wasm_path):
        # Try with original name
        import glob
        wasm_files = glob.glob("target/wasm32-wasip1/release/*.wasm")
        if wasm_files:
            wasm_path = wasm_files[0]
        else:
            print("No wasm file found in target/wasm32-wasip1/release/")
            sys.exit(1)
    
    size = os.path.getsize(wasm_path)
    print(f"✓ Built: {wasm_path} ({size:,} bytes)")
    return wasm_path

def deploy(binary_id: int = None, app_name: str = None, app_id: int = None):
    """Deploy or update a FastEdge app."""
    api_key = os.environ.get("GCORE_API_KEY")
    if not api_key:
        print("Error: GCORE_API_KEY environment variable not set")
        sys.exit(1)
    
    headers = {
        "Authorization": f"APIKey {api_key}",
        "Content-Type": "application/json",
        "accept": "application/json"
    }
    
    if app_id:
        # Update existing app
        url = f"https://api.gcore.com/fastedge/v1/apps/{app_id}"
        resp = requests.put(
            url,
            headers=headers,
            json={"binary": binary_id, "status": 1, "name": app_name}
        )
    else:
        # Create new app
        url = "https://api.gcore.com/fastedge/v1/apps"
        resp = requests.post(
            url,
            headers=headers,
            json={
                "name": app_name,
                "binary": binary_id,
                "status": 1
            }
        )
    
    if resp.status_code in (200, 201):
        data = resp.json()
        print(f"✓ Deployed: {data.get('url')}")
        print(f"  App ID: {data.get('id')}")
    else:
        print(f"Error: {resp.status_code} - {resp.text}")
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: build_rust.py build|deploy [OPTIONS]")
        print("  build                    - Build the Wasm binary")
        print("  deploy --app-name NAME   - Create new app")
        print("  deploy --app-id ID --binary-id ID - Update existing app")
        sys.exit(1)
    
    cmd = sys.argv[1]
    
    if cmd == "build":
        build()
    elif cmd == "deploy":
        # Parse simple args
        app_name = None
        app_id = None
        binary_id = None
        
        i = 2
        while i < len(sys.argv):
            if sys.argv[i] == "--app-name":
                app_name = sys.argv[i+1]
                i += 2
            elif sys.argv[i] == "--app-id":
                app_id = int(sys.argv[i+1])
                i += 2
            elif sys.argv[i] == "--binary-id":
                binary_id = int(sys.argv[i+1])
                i += 2
            else:
                i += 1
        
        if not binary_id:
            print("Error: --binary-id required for deploy")
            sys.exit(1)
        
        deploy(binary_id, app_name, app_id)
    else:
        print(f"Unknown command: {cmd}")
        sys.exit(1)
