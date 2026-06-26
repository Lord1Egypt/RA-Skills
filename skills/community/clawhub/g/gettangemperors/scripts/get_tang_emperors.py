#!/usr/bin/env python3
"""
Tang Emperors API Client
Calls local backend API to retrieve Tang Dynasty emperor information
"""

import requests
import json
import sys

# API Configuration
API_BASE_URL = "http://127.0.0.1:8080"
API_ENDPOINT = "/api/v1/test"


def get_tang_emperors():
    """
    Fetch Tang Dynasty emperor information from local API
    
    Returns:
        dict: JSON response containing emperor information
    """
    try:
        url = f"{API_BASE_URL}{API_ENDPOINT}"
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.ConnectionError:
        return {"error": "Failed to connect to API. Make sure the backend is running at http://127.0.0.1:8080"}
    except requests.exceptions.Timeout:
        return {"error": "API request timed out"}
    except requests.exceptions.HTTPError as e:
        return {"error": f"HTTP error occurred: {e}"}
    except json.JSONDecodeError:
        return {"error": "Invalid JSON response from API"}
    except Exception as e:
        return {"error": f"Unexpected error: {e}"}


def format_emperor_data(data):
    """
    Format emperor data for human-readable output
    
    Args:
        data: Raw API response
        
    Returns:
        str: Formatted string
    """
    if "error" in data:
        return f"Error: {data['error']}"
    
    # Check if data is a list
    if isinstance(data, list):
        emperors = data
    # Check if data has an 'emperors' key
    elif isinstance(data, dict) and 'emperors' in data:
        emperors = data['emperors']
    # Check if data has a 'data' key
    elif isinstance(data, dict) and 'data' in data:
        emperors = data['data']
    else:
        return f"Unexpected data format: {json.dumps(data, indent=2, ensure_ascii=False)}"
    
    if not emperors:
        return "No emperor data found in API response"
    
    output = []
    output.append("唐朝前3代皇帝信息\n" + "=" * 40)
    
    for i, emperor in enumerate(emperors[:3], 1):
        output.append(f"\n皇帝 #{i}")
        if isinstance(emperor, dict):
            for key, value in emperor.items():
                output.append(f"  {key}: {value}")
        else:
            output.append(f"  {emperor}")
    
    return "\n".join(output)


if __name__ == "__main__":
    # Fetch data
    result = get_tang_emperors()
    
    # Check if JSON output is requested
    if len(sys.argv) > 1 and sys.argv[1] == "--json":
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        # Print formatted output
        print(format_emperor_data(result))
