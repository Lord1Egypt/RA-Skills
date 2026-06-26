# Markdown for Agents Examples

## cURL Examples

### Basic Request

```bash
curl https://developers.cloudflare.com/agents/ \
  -H "Accept: text/markdown"
```

### With Fallback

```bash
curl https://developers.cloudflare.com/agents/ \
  -H "Accept: text/markdown, text/html"
```

### Show Response Headers

```bash
curl -I https://developers.cloudflare.com/agents/ \
  -H "Accept: text/markdown"
```

Output:
```
HTTP/2 200
date: Wed, 11 Feb 2026 11:44:48 GMT
content-type: text/markdown; charset=utf-8
content-length: 2899
vary: accept
x-markdown-tokens: 725
content-signal: ai-train=yes, search=yes, ai-input=yes
```

## JavaScript/TypeScript Examples

### Fetch with Headers

```typescript
const response = await fetch(
  "https://developers.cloudflare.com/agents/",
  {
    headers: {
      Accept: "text/markdown, text/html",
    },
  }
);

const tokenCount = response.headers.get("x-markdown-tokens");
const markdown = await response.text();

console.log(`Tokens: ${tokenCount}`);
console.log(markdown);
```

### Cloudflare Workers

```typescript
export default {
  async fetch(request: Request): Promise<Response> {
    const url = new URL(request.url);
    const targetUrl = url.searchParams.get("url");
    
    if (!targetUrl) {
      return new Response("Missing url parameter", { status: 400 });
    }
    
    const response = await fetch(targetUrl, {
      headers: {
        Accept: "text/markdown, text/html",
      },
    });
    
    const markdown = await response.text();
    const tokens = response.headers.get("x-markdown-tokens");
    
    return new Response(markdown, {
      headers: {
        "Content-Type": "text/markdown",
        "X-Markdown-Tokens": tokens || "unknown",
      },
    });
  },
};
```

### Using in an AI Agent

```typescript
import { Agent, callable } from "agents";

export class WebResearchAgent extends Agent {
  @callable()
  async fetchPage(url: string): Promise<{ markdown: string; tokens: number }> {
    const response = await fetch(url, {
      headers: {
        Accept: "text/markdown, text/html",
      },
    });
    
    const markdown = await response.text();
    const tokens = parseInt(
      response.headers.get("x-markdown-tokens") || "0",
      10
    );
    
    return { markdown, tokens };
  }
}
```

## Python Examples

### Using requests

```python
import requests

def fetch_markdown(url: str) -> dict:
    headers = {
        "Accept": "text/markdown, text/html"
    }
    
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    
    return {
        "markdown": response.text,
        "tokens": response.headers.get("x-markdown-tokens"),
        "content_signal": response.headers.get("content-signal"),
    }

# Usage
result = fetch_markdown("https://developers.cloudflare.com/agents/")
print(f"Tokens: {result['tokens']}")
print(result["markdown"][:500])
```

### Using aiohttp (Async)

```python
import aiohttp
import asyncio

async def fetch_markdown(url: str) -> dict:
    headers = {
        "Accept": "text/markdown, text/html"
    }
    
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as response:
            return {
                "markdown": await response.text(),
                "tokens": response.headers.get("x-markdown-tokens"),
                "status": response.status,
            }

# Usage
async def main():
    result = await fetch_markdown("https://developers.cloudflare.com/agents/")
    print(f"Tokens: {result['tokens']}")

asyncio.run(main())
```

## Testing if a Site Supports Markdown for Agents

```bash
#!/bin/bash

URL="$1"

if [ -z "$URL" ]; then
    echo "Usage: $0 <URL>"
    exit 1
fi

echo "Testing: $URL"
echo "---"

response=$(curl -s -o /dev/null -w "%{content_type}" \
    -H "Accept: text/markdown" "$URL")

if [[ "$response" == *"text/markdown"* ]]; then
    echo "✅ Markdown for Agents is supported!"
    echo "Content-Type: $response"
else
    echo "❌ Markdown for Agents is NOT supported"
    echo "Content-Type: $response"
fi
```

## Comparing HTML vs Markdown Token Count

```typescript
async function compareTokenUsage(url: string) {
  // Fetch HTML
  const htmlResponse = await fetch(url);
  const html = await htmlResponse.text();
  const htmlTokens = estimateTokens(html);
  
  // Fetch Markdown
  const mdResponse = await fetch(url, {
    headers: { Accept: "text/markdown" },
  });
  const markdown = await mdResponse.text();
  const mdTokens = parseInt(
    mdResponse.headers.get("x-markdown-tokens") || "0",
    10
  );
  
  console.log(`HTML tokens: ${htmlTokens}`);
  console.log(`Markdown tokens: ${mdTokens}`);
  console.log(`Savings: ${((1 - mdTokens/htmlTokens) * 100).toFixed(1)}%`);
}

function estimateTokens(text: string): number {
  // Rough estimate: ~4 characters per token
  return Math.ceil(text.length / 4);
}
```

## Integration with LLM Applications

### LangChain Document Loader

```typescript
import { BaseDocumentLoader } from "langchain/document_loaders/base";
import { Document } from "langchain/document";

class MarkdownForAgentsLoader extends BaseDocumentLoader {
  constructor(private url: string) {
    super();
  }

  async load(): Promise<Document[]> {
    const response = await fetch(this.url, {
      headers: { Accept: "text/markdown" },
    });

    const markdown = await response.text();
    const tokens = response.headers.get("x-markdown-tokens");

    return [
      new Document({
        pageContent: markdown,
        metadata: {
          source: this.url,
          tokens: parseInt(tokens || "0", 10),
        },
      }),
    ];
  }
}
```

### RAG Pipeline Example

```typescript
async function buildKnowledgeBase(urls: string[]) {
  const documents = [];
  
  for (const url of urls) {
    const response = await fetch(url, {
      headers: { Accept: "text/markdown" },
    });
    
    const markdown = await response.text();
    const tokens = parseInt(
      response.headers.get("x-markdown-tokens") || "0",
      10
    );
    
    // Chunk if too large for context window
    if (tokens > 4000) {
      const chunks = chunkMarkdown(markdown);
      documents.push(...chunks);
    } else {
      documents.push(markdown);
    }
  }
  
  return documents;
}
```
