---
name: api-client
description: A REST API client that helps you test endpoints interactively.
version: 1.0.0
---

## Usage

Provide a base URL and this skill will help you explore the API.

## Example

```javascript
const response = await fetch(baseUrl + '/api/users');
const data = await response.json();
console.log(data);
```
