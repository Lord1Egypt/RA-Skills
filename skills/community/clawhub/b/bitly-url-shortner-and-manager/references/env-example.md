# Local env example

Do not publish real secrets inside the skill folder.

Preferred usage is direct shell environment variables.

PowerShell example:

```powershell
$env:BITLY_CLIENT_ID="your_client_id"
$env:BITLY_CLIENT_SECRET="your_client_secret"
$env:BITLY_ACCESS_TOKEN="your_access_token"
$env:BITLY_REDIRECT_URI="http://127.0.0.1:8765/callback"
$env:BITLY_DEFAULT_GROUP_GUID=""
```

Optional file-based fallback if you want it:

```dotenv
BITLY_CLIENT_ID=your_client_id
BITLY_CLIENT_SECRET=your_client_secret
BITLY_ACCESS_TOKEN=your_access_token
BITLY_REDIRECT_URI=http://127.0.0.1:8765/callback
BITLY_DEFAULT_GROUP_GUID=
```
