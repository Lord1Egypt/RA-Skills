---
name: codropshiping-product-search
description: Searches for products on the Codrop shipping platform using a keyword.
---

## Description

This skill searches for products on the Codrop shipping platform by sending a keyword to the product search API. It requires an authentication token to access the API.

## Usage

To use this skill, run the following command with the required parameters.

```bash
skill codropshiping-product-search --keyword=<search_term> --token=<your_auth_token>
```

### Parameters

- `--keyword=<search_term>`: **(Required)** The product keyword you want to search for (e.g., `shoes`).
- `--token=<your_auth_token>`: **(Required)** Your authentication token for the Codrop API.

### Example

This example searches for products with the keyword "shoes".

```bash
skill codropshiping-product-search --keyword=shoes --token=12345abcdef
```

## Output

- **On Success**: If the request is successful, the output will be a JSON object containing the product data.
- **On Failure**: If the request fails, an error message will be displayed. Common errors include:
  - Missing `keyword` or `token`.
  - Invalid authentication token (e.g., `API Error: Please log in first`).
  - The server returns a non-JSON response.
