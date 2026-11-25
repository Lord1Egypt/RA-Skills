# Petstore API Reference

## Authentication

All requests require an `api_key` header.

## Endpoints

### List Pets

    GET /pets

Returns all pets.

### Get Pet by ID

    GET /pets/{petId}

Returns a single pet.

### Create Pet

    POST /pets

Creates a new pet. Request body:

```json
{"name": "Buddy", "status": "available"}
```

### Delete Pet

    DELETE /pets/{petId}

Deletes a pet by ID.

## Notes

The API rate limit is 100 requests per minute.
Contact support@example.com for access issues.
