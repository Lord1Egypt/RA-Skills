import requests
import sys

def test_sql_injection(url, param_name):
    """Tests for basic SQL injection by appending a common payload to a URL parameter."""
    payload = "' OR 1=1 -- "
    test_url = f"{url}?{param_name}={payload}"
    
    print(f"Testing URL: {test_url}")
    
    try:
        response = requests.get(test_url, timeout=5)
        # A real SQL injection scanner would analyze the response content for specific error messages or changes.
        # For this basic example, we'll just check if the request was successful and print a generic message.
        if response.status_code == 200:
            print(f"Potential SQL Injection vulnerability detected on {url} with parameter {param_name}. Review the response manually.")
            # In a real scenario, you'd look for specific keywords like 'SQL error', 'syntax error', etc.
            # For example: if "SQL error" in response.text or "syntax error" in response.text:
            #    print("SQL error message found in response.")
        else:
            print(f"No obvious SQL Injection vulnerability detected on {url} with parameter {param_name}. Status code: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"Error during request to {url}: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python3 sql_injector.py <url> <parameter_name>")
        sys.exit(1)
    
    url = sys.argv[1]
    param_name = sys.argv[2]
    test_sql_injection(url, param_name)
