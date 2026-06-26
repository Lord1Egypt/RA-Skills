import os
import httpx
from dotenv import load_dotenv

# Load ENV
load_dotenv()

API_URL = os.getenv("EMERGENCE_API_URL", "http://localhost:8000")
API_KEY = os.getenv("EMERGENCE_API_KEY", "local_test_key")

def test_rendering():
    print(f"--- Testing Rendering via {API_URL} ---")
    
    payload = {
        "engine": "mermaid",
        "code": "graph TD\n    A[User] -->|Input| B[Agent]\n    B -->|Code| C[Render Agent]\n    C -->|Image| B",
        "format": "png"
    }
    
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    
    try:
        response = httpx.post(f"{API_URL}/tools/render", json=payload, headers=headers)
        if response.status_code == 200:
            print("✅ Success: Rendering API is online and functional.")
            data = response.json()
            if "status" in data:
                print(f"Render Status: {data['status']}")
        else:
            print(f"❌ Error: {response.status_code}")
            print(response.text)
    except Exception as e:
        print(f"❌ Connection Error: {e}")

if __name__ == "__main__":
    test_rendering()
