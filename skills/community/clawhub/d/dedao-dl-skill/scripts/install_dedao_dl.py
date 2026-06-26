import os
import sys
import platform
import json
import urllib.request
import stat

def main():
    system = platform.system().lower()
    machine = platform.machine().lower()
    
    arch = "amd64"
    if machine in ["x86_64", "amd64"]:
        arch = "amd64"
    elif machine in ["arm64", "aarch64"]:
        arch = "arm64"
    elif "386" in machine:
        arch = "386"
    
    print(f"Target OS: {system}, Architecture: {arch}")
    
    target_exe = "dedao-dl.exe" if system == "windows" else "dedao-dl"
    if os.path.exists(target_exe):
        print(f"'{target_exe}' already exists in current directory. Setup complete.")
        return

    api_url = "https://api.github.com/repos/yann0917/dedao-dl/releases/latest"
    try:
        req = urllib.request.Request(api_url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode())
    except Exception as e:
        print(f"Failed to fetch release info from GitHub API: {e}")
        return

    assets = data.get("assets", [])
    download_asset = None
    
    for asset in assets:
        name = asset["name"].lower()
        if system == "darwin" and "darwin" in name:
            # Match darwin build
            if arch in name or "all" in name:
                download_asset = asset
                break
        elif system in name and arch in name:
            if system == "windows" and name.endswith(".exe"):
                 download_asset = asset
                 break
            elif system != "windows" and not name.endswith(".zip") and not name.endswith(".tar.gz"):
                 # direct binary preferred
                 download_asset = asset
                 break
            # Fallback
            download_asset = asset

    if not download_asset:
        print("Could not find a suitable release asset. Available:")
        for a in assets:
            print("- " + a["name"])
        sys.exit(1)

    download_url = download_asset["browser_download_url"]
    file_name = download_asset["name"]
    print(f"Downloading {file_name} from {download_url}...")
    
    try:
        urllib.request.urlretrieve(download_url, target_exe)
        print("Download complete.")
        
        # Make script executable on Unix systems
        if system != "windows":
            st = os.stat(target_exe)
            os.chmod(target_exe, st.st_mode | stat.S_IEXEC)
            
        print(f"Setup successful. You can now use ./{target_exe} (or .\\{target_exe} on Windows)")
        
    except Exception as e:
        print(f"Error during installation: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
