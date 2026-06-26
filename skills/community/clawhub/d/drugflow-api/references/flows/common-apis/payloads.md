# DrugFlow Common APIs Payload Rules

## Sign In
1. Request
```json
{
  "email": "user@example.com",
  "password": "your-password",
  "phone": "0"
}
```
2. Success
```json
{
  "detail": "ok"
}
```

## Sign Up
1. Request
```json
{
  "email": "new-user@example.com",
  "name": "new-user",
  "organization": "org",
  "password1": "YourPassword123",
  "password2": "YourPassword123"
}
```
2. Success
```json
{
  "detail": "ok"
}
```
3. Common error (already exists)
```json
{
  "detail": {
    "email": [
      "A user with that email already exists."
    ]
  }
}
```

## Workspace List
1. Success shape
```json
{
  "count": 3,
  "available_count": 3,
  "next": null,
  "previous": null,
  "results": [
    {
      "ws_id": "abcdefghijklmnop",
      "name": "Default Workspace",
      "status": 1
    }
  ]
}
```

## Workspace Create
1. Request
```json
{
  "ws_name": "codex-common-api-workspace",
  "is_default": true
}
```
2. Success
```json
{
  "status": "ok",
  "ws_id": "abcdefghijklmnop"
}
```

## Balance
1. Success
```json
{
  "is_avaliable": true,
  "tokens": 123456,
  "licence_time": 1711111111
}
```

## Jobs List
1. Success shape
```json
{
  "count": 10,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 123,
      "name": "job-name",
      "state": "finished"
    }
  ]
}
```
