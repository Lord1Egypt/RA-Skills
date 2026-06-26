import os
import requests
import json
import sys
import argparse

class FireflyClient:
    def __init__(self):
        # Allow override via environment variables
        self.url = os.environ.get("FIREFLY_URL")
        self.token = os.environ.get("FIREFLY_TOKEN")
        
        # Validate configuration
        if not self.url or not self.token:
            print("Error: FIREFLY_URL and FIREFLY_TOKEN must be set.", file=sys.stderr)
            sys.exit(1)
            
        self.headers = {
            "Authorization": f"Bearer {self.token}",
            "Accept": "application/vnd.api+json",
            "Content-Type": "application/json"
        }

    def request(self, method, endpoint, data=None):
        """Generic request method with error handling."""
        url = f"{self.url.rstrip('/')}/{endpoint.lstrip('/')}"
        
        # Safely handle JSON data
        try:
            json_data = json.loads(data) if isinstance(data, str) else data
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON data: {e}", file=sys.stderr)
            sys.exit(1)
            
        try:
            response = requests.request(method, url, headers=self.headers, json=json_data)
            # Raise exception for 4xx/5xx errors
            response.raise_for_status()
            # Handle empty responses
            return response.json() if response.text.strip() else {}
        except requests.exceptions.HTTPError as e:
            # Provide detailed error info from API
            try:
                error_detail = response.json()
                print(f"API Error ({response.status_code}): {json.dumps(error_detail, indent=2)}", file=sys.stderr)
            except:
                print(f"HTTP Error: {e}", file=sys.stderr)
            sys.exit(1)
        except Exception as e:
            print(f"Request Error: {e}", file=sys.stderr)
            sys.exit(1)

if __name__ == "__main__":
    client = FireflyClient()
    parser = argparse.ArgumentParser(description="Firefly III Generic API Client")
    subparsers = parser.add_subparsers(dest="command")

    # Request command
    req_parser = subparsers.add_parser("request")
    req_parser.add_argument("method", choices=["GET", "POST", "PUT", "PATCH", "DELETE"])
    req_parser.add_argument("endpoint", help="API endpoint (e.g., api/v1/accounts)")
    req_parser.add_argument("-d", "--data", help="JSON data for POST/PUT/PATCH requests")

    args = parser.parse_args()

    if args.command == "request":
        result = client.request(args.method, args.endpoint, args.data)
        print(json.dumps(result, indent=2))
    else:
        parser.print_help()