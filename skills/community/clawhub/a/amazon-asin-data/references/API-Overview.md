# LinkFoxAgent API Overview

LinkFoxAgent is a specialized agent platform for cross-border e-commerce, providing tools for product selection, market analysis, operations, and competitive intelligence.

## Base Configuration

### API Endpoint
```
https://test-tool-gateway.linkfox.com/
```

### Authentication

All API requests require authentication via header:

```http
Authorization: {LINKFOXAGENT_API_KEY}
Content-Type: application/json
```

### Environment Setup

**Set API Key**
```bash
export LINKFOXAGENT_API_KEY="your_api_key_here"
```

**Verify Setup**
```bash
echo $LINKFOXAGENT_API_KEY
```

**Persistent Configuration** (add to `~/.bashrc`, `~/.zshrc`, or `~/.profile`):
```bash
# LinkFoxAgent API Configuration
export LINKFOXAGENT_API_KEY="your_api_key_here"
```

### Obtaining API Key

1. Visit the LinkFoxAgent dashboard
2. Navigate to API Settings or Developer Console
3. Generate or copy your API key
4. Store securely and never commit to version control

## Available Tools

LinkFoxAgent provides multiple specialized tools organized by category:

### Market Analysis Tools

**Jiimore (极目) - Amazon Niche Market Analysis**
- Endpoint: `/jiimore/getNicheInfoByKeyword`
- Purpose: Amazon marketplace data and niche analysis
- Markets: US, JP, DE
- Documentation: See `Jiimore.md`

### Data Processing Tools

**Python Sandbox (`@Python沙箱`)**
- Built-in LLM capabilities
- Process structured JSON data
- Export to CSV/Excel
- Image recognition from URLs
- Statistical calculations
- Markdown table generation

**Use cases:**
- Post-process API results
- Data transformation and filtering
- Custom metric calculations
- Export formatted reports

### Web Research Tools

**Web Search (`@网页检索`)**
- Powered by Tavily Search
- Use for all web research needs beyond specialized tools
- Includes WeChat public account information
- Real-time internet data

**Note:** For Amazon, Walmart, eBay use specialized tools; for everything else use web search.

### AI Tools

**AI Image Generation (`AI绘图`)**
- Top-tier image generation (Google Imagen model)
- Support for up to 3 reference images
- Text-to-image and image-to-image
- Product mockup generation
- Background replacement
- Object modification
- Style transfer

**Priority:** Use this tool for all image generation tasks.

## Request Patterns

### Synchronous Requests
For quick operations (<1 second response time):
```bash
curl -X POST https://test-tool-gateway.linkfox.com/endpoint \
  -H "Authorization: ${LINKFOXAGENT_API_KEY}" \
  -H "Content-Type: application/json" \
  -d '{"param": "value"}'
```

### Asynchronous Requests (Recommended)
For operations requiring 1-5 minutes:

1. Submit task (returns task ID)
2. Continue other work
3. Poll for completion or receive callback
4. Retrieve results with HTML report URL

**Benefits:**
- Non-blocking execution
- Continue conversation during processing
- Automatic result delivery
- HTML report generation

## Response Formats

### Standard JSON Response
```json
{
  "total": number,
  "data": array | object,
  "columns": array,
  "costToken": number,
  "type": "table" | "json" | "html",
  "title": string
}
```

### HTML Report Response
Some tools return HTML report URLs:
```json
{
  "reportUrl": "https://...",
  "data": {...}
}
```

**Important:** Always provide HTML report URLs to users when available.

## Error Handling

### Common Error Codes

**401 Unauthorized**
```json
{
  "error": "Unauthorized",
  "message": "Invalid or missing API key"
}
```
**Solution:** Verify `LINKFOXAGENT_API_KEY` is set correctly

**400 Bad Request**
```json
{
  "error": "Validation Failed",
  "message": "Invalid parameter: ..."
}
```
**Solution:** Check parameter types and constraints

**429 Rate Limit Exceeded**
```json
{
  "error": "Rate Limit Exceeded",
  "message": "Too many requests"
}
```
**Solution:** Implement backoff and retry logic

**500 Internal Server Error**
```json
{
  "error": "Internal Server Error",
  "message": "Processing failed"
}
```
**Solution:** Retry with exponential backoff, contact support if persistent

### Retry Strategy

Implement exponential backoff for transient failures:

```python
import time

def api_request_with_retry(url, data, max_retries=3):
    for attempt in range(max_retries):
        try:
            response = requests.post(url, json=data, headers=headers)
            if response.status_code == 200:
                return response.json()
            elif response.status_code == 429:
                wait_time = (2 ** attempt) * 1
                time.sleep(wait_time)
                continue
            else:
                response.raise_for_status()
        except requests.exceptions.RequestException as e:
            if attempt == max_retries - 1:
                raise
            time.sleep(2 ** attempt)
    return None
```

## Best Practices

### Security
1. **Never hardcode API keys** in source code
2. **Use environment variables** for configuration
3. **Rotate keys regularly** for security
4. **Restrict key permissions** to minimum required scope
5. **Monitor usage** for unauthorized access

### Performance
1. **Use async/background processing** for long operations
2. **Implement caching** for repeated queries
3. **Batch requests** when possible
4. **Optimize parameters** to reduce processing time
5. **Monitor rate limits** and implement backoff

### Data Handling
1. **Validate inputs** before API calls
2. **Parse responses carefully** (check for errors first)
3. **Handle missing fields** gracefully
4. **Convert decimals to percentages** for user display
5. **Provide context** when presenting data

### User Experience
1. **Progressive disclosure** - start simple, add complexity as needed
2. **Natural language processing** - convert user intent to API parameters
3. **Clear error messages** - explain what went wrong and how to fix
4. **Visual aids** - use tables, charts, images when available
5. **Export options** - provide CSV/Excel downloads for data analysis

## Integration Workflows

### Basic Analysis Workflow
```
User Query
  ↓
Convert to API Parameters
  ↓
Submit API Request (Background)
  ↓
Notify User Processing Started
  ↓
Continue Conversation
  ↓
Receive Results Callback
  ↓
Parse and Present Data
  ↓
Offer Export/Further Analysis
```

### Advanced Multi-Tool Workflow
```
1. Jiimore API → Get niche data
2. Python Sandbox → Process/filter results
3. Web Search → Research top competitors
4. AI Image Gen → Create product mockups
5. Python Sandbox → Export final report
```

### Polling Implementation
For async tasks without callbacks:

```python
import time

def poll_task_result(task_id, max_wait=300, poll_interval=10):
    start_time = time.time()
    while time.time() - start_time < max_wait:
        response = check_task_status(task_id)
        if response['status'] == 'completed':
            return response['data']
        elif response['status'] == 'failed':
            raise Exception(f"Task failed: {response['error']}")
        time.sleep(poll_interval)
    raise TimeoutError("Task exceeded maximum wait time")
```

## Rate Limits

Default rate limits (subject to subscription tier):
- **Per minute**: 10 requests
- **Per hour**: 100 requests
- **Per day**: 1000 requests

**Recommendations:**
- Implement request queuing for batch operations
- Use background processing to avoid user-facing delays
- Monitor usage via dashboard
- Upgrade tier for higher limits

## Support & Resources

### Documentation
- Tool-specific docs in `references/` directory
- API changelog and updates from LinkFoxAgent
- Example code and workflows

### Troubleshooting
1. Check environment variable configuration
2. Verify API key validity
3. Review request/response logs
4. Test with minimal parameters
5. Contact support with task IDs

### Updates
- API endpoint may change (update `BASE_URL`)
- New tools added regularly
- Breaking changes announced in advance
- Monitor changelog for updates

## Migration Notes

**From Internal Tools to Public API:**
- Internal restrictions removed from documentation
- Focus on public API contract only
- Implementation details abstracted
- User-facing features emphasized

**Backward Compatibility:**
- Existing integrations continue to work
- New parameters optional (defaults provided)
- Deprecated features marked clearly
- Migration guides provided for breaking changes

## Cost Considerations

API usage tracked via:
- `costToken` field in responses (internal metric)
- Per-request pricing based on complexity
- Subscription tier limits
- Export/download bandwidth

**Optimization:**
- Use filters to reduce result size
- Cache frequently accessed data
- Avoid redundant requests
- Choose appropriate `pageSize`

## Examples

### Python Example
```python
import os
import requests

BASE_URL = "https://test-tool-gateway.linkfox.com"
API_KEY = os.getenv("LINKFOXAGENT_API_KEY")

def query_niche(keyword, country="US"):
    url = f"{BASE_URL}/jiimore/getNicheInfoByKeyword"
    headers = {
        "Authorization": API_KEY,
        "Content-Type": "application/json"
    }
    payload = {
        "keyword": keyword,
        "countryCode": country,
        "pageSize": 50,
        "sortField": "demand",
        "sortType": "desc"
    }

    response = requests.post(url, json=payload, headers=headers)
    response.raise_for_status()
    return response.json()

# Usage
results = query_niche("wireless charger", "US")
print(f"Found {results['total']} niches")
for niche in results['data'][:5]:
    print(f"{niche['nicheTitle']}: Demand={niche['demand']}")
```

### Shell Example
```bash
#!/bin/bash

KEYWORD="bluetooth speaker"
COUNTRY="US"

curl -X POST "https://test-tool-gateway.linkfox.com/jiimore/getNicheInfoByKeyword" \
  -H "Authorization: ${LINKFOXAGENT_API_KEY}" \
  -H "Content-Type: application/json" \
  -d "{
    \"keyword\": \"${KEYWORD}\",
    \"countryCode\": \"${COUNTRY}\",
    \"pageSize\": 50,
    \"sortField\": \"demand\",
    \"sortType\": \"desc\"
  }" | jq '.data[].nicheTitle'
```

## Summary

LinkFoxAgent provides a comprehensive API for cross-border e-commerce intelligence:

- **Simple Setup**: Environment variable configuration
- **Rich Toolset**: Market analysis, AI generation, data processing
- **Async Processing**: Background execution for long operations
- **Clear Documentation**: Detailed parameter and response specs
- **Best Practices**: Security, performance, UX guidelines

Start with basic queries, iterate based on results, and leverage multi-tool workflows for comprehensive analysis.
