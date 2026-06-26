---
name: api-test-generator
description: Generates quick API test examples in various programming languages (Python, JavaScript, cURL, Go) based on user-provided API details. Use this when a user requests code snippets or examples for testing APIs.
---

# API Test Example Generator

This skill helps in quickly generating API test examples for various programming languages and tools. It's designed to provide ready-to-use code snippets for rapid API testing and development.

## Workflow

When a user requests an API test example, follow these steps:

### 1. Gather API Details

Ask the user for the following information:

- **API Endpoint URL**: The full URL of the API endpoint (e.g., `https://api.example.com/v1/users`).
- **HTTP Method**: The HTTP method to use (e.g., `GET`, `POST`, `PUT`, `DELETE`).
- **Headers (Optional)**: Any required headers, such as `Authorization` tokens or `Content-Type`.
- **Request Body (Optional)**: The data payload for `POST`, `PUT`, or `PATCH` requests, typically in JSON format.
- **Desired Language/Tool**: The programming language or tool for the example (e.g., `Python`, `JavaScript`, `cURL`, `Go`). If not specified, ask the user.

### 2. Select Appropriate Template

Based on the user's desired language/tool, select the corresponding template from `references/api_patterns.md`. If the requested language is not directly available, choose the closest alternative or inform the user about available options.

### 3. Generate Code Example

Populate the selected template with the API details provided by the user. Ensure that placeholders like `YOUR_TOKEN`, `https://api.example.com/v1/endpoint`, and `{"key":"value"}` are replaced with the actual values.

### 4. Present the Example

Provide the generated code example to the user, enclosed in a code block. Offer to make adjustments or generate examples in other languages if needed.

## Available Languages/Tools

This skill supports generating examples for the following:

- **Python** (using `requests` library)
- **JavaScript** (using `fetch` API)
- **cURL** (command-line tool)
- **Go** (using `net/http` package)

Refer to `references/api_patterns.md` for the base templates and syntax for each language.

## Example Usage

**User Request:** "Can you give me a Python example to POST data to `https://api.example.com/data` with a JSON body `{"name": "test"}` and an Authorization header `Bearer abc123`?"

**Agent Action (Conceptual):**
1. Identify language: Python.
2. Retrieve Python template from `api_patterns.md`.
3. Replace placeholders with provided URL, method, headers, and body.
4. Present the generated Python code.

```python
import requests

url = "https://api.example.com/data"
headers = {
    "Authorization": "Bearer abc123",
    "Content-Type": "application/json"
}
payload = {
    "name": "test"
}

response = requests.post(url, json=payload, headers=headers)
print(f"Status Code: {response.status_code}")
print(response.json())
```
