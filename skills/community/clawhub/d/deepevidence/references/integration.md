# DeepEvidence Integration Examples

Use this reference when the user asks how to integrate DeepEvidence into an application or wants curl, Python, or Node examples. These examples use direct HTTP and do not require an SDK.

## Curl

```bash
curl https://deepevid.medsci.cn/api/v1/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $DEEPEVIDENCE_API_KEY" \
  -d '{
    "model": "DeepEvidence-V1",
    "messages": [
      {"role": "user", "content": "阿司匹林的适应症有哪些？"}
    ],
    "stream": false
  }'
```

## Python

```python
import json
import os
from urllib import request

payload = {
    "model": "DeepEvidence-V1",
    "messages": [
        {"role": "user", "content": "阿司匹林的适应症有哪些？"}
    ],
    "stream": False,
}

req = request.Request(
    "https://deepevid.medsci.cn/api/v1/chat/completions",
    data=json.dumps(payload, ensure_ascii=False).encode("utf-8"),
    headers={
        "Authorization": f"Bearer {os.environ['DEEPEVIDENCE_API_KEY']}",
        "Content-Type": "application/json",
    },
    method="POST",
)

with request.urlopen(req, timeout=60) as resp:
    data = json.loads(resp.read().decode("utf-8"))

print(data["choices"][0]["message"]["content"])
```

## Node.js

```javascript
const resp = await fetch("https://deepevid.medsci.cn/api/v1/chat/completions", {
  method: "POST",
  headers: {
    "Authorization": `Bearer ${process.env.DEEPEVIDENCE_API_KEY}`,
    "Content-Type": "application/json",
  },
  body: JSON.stringify({
    model: "DeepEvidence-V1",
    messages: [
      { role: "user", content: "阿司匹林的适应症有哪些？" },
    ],
    stream: false,
  }),
});

const data = await resp.json();
console.log(data.choices[0].message.content);
```

## Notes

- The server defaults `stream` to `true`; set `stream: false` when the caller expects a normal JSON response.
- Read API keys from environment variables only.
- Log only minimal operational metadata, such as status, latency, model, token usage, and request ID if returned.
