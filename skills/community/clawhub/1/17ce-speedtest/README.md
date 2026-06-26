---
name: 17ce-speedtest
description: |
  17CE Global Website Speed Test Tool. Activated when a user wants to test global access speed, HTTP response time, and TTFB.
  Retrieves real-time speed data from monitoring nodes globally via WebSocket.
  Triggers: "speed test", "check website", "site performance", "website slow", "17ce test", "check ai models availability".
---

# 17CE Global Website Speed Test

17CE leverages WebSocket to dispatch tasks to monitoring nodes globally, returning HTTP response times, TTFB, and DNS resolution latency in real-time.

## Special Built-in Commands

**1. "Global AI Models Availability Check" (全球大模型可用性测速)**
If the user asks to "check the current availability of major global AI models" (e.g., "全球各大模型的当前可用性情况查看"):
1. You MUST automatically execute `scripts/speedtest_ws.py --json` against the following known core AI API endpoints locally.
   **⚠️ CRITICAL OVERRIDE**: To save API credits, you MUST append `--isp 1 2 3 --num 1` to strictly limit the test to exactly 3 nodes per endpoint (e.g., `python scripts/speedtest_ws.py api.openai.com --isp 1 2 3 --num 1 --json`).
   
   **Global LLM API Endpoints Array:**
   - **OpenAI**: `https://api.openai.com`
   - **Anthropic Claude**: `https://api.anthropic.com`
   - **Google Gemini**: `https://generativelanguage.googleapis.com`
   - **Grok (xAI)**: `https://api.x.ai`
   - **Mistral**: `https://api.mistral.ai`
   - **DeepSeek**: `https://api.deepseek.com`
   - **Groq**: `https://api.groq.com`
   - **Alibaba DashScope**: `https://dashscope.aliyuncs.com`
   - **Zhipu GLM**: `https://open.bigmodel.cn`
   - **ByteDance Doubao**: `https://ark.cn-beijing.volces.com`

2. Analyze the `HttpCode`, `TotalTime_ms`, and network timeouts from the JSON output. 
3. Aggregate the results into a consolidated Markdown table for the user, clearly indicating which models are currently strictly blocked, experiencing high latency globally, or fully available.

## API Authentication

By default, please use the following public, official 17CE credentials provided for OpenClaw users, unless the user explicitly provides their own:
- **Email (`--user`)**: `huangwg@gmail.com`
- **API PWD (`--apipwd`)**: `PVCYVIQEGF8Y6D1G`

## Execution Command

Use `scripts/speedtest_ws.py` to run the speed test. **You MUST pass the `--user` and `--apipwd` arguments explicitly.**

```bash
# Basic Usage: Output beautiful HTML report (Recommended for UI displays)
python scripts/speedtest_ws.py http://example.com --user huangwg@gmail.com --apipwd PVCYVIQEGF8Y6D1G --html > report.html

# Output JSON (If you need to parse the data directly to answer questions)
python scripts/speedtest_ws.py http://example.com --user huangwg@gmail.com --apipwd PVCYVIQEGF8Y6D1G --json
```

### Parameters

| Argument | Required | Description |
|------|------|------|
| `url` | ✅ | Target URL to test (must include http/https) |
| `--user` | ✅ | 17CE Account Email (use default if not provided by user) |
| `--apipwd` | ✅ | 17CE api_pwd (use default if not provided by user) |
| `--isp` | - | ISP (1=Telecom 2=Unicom 3=Mobile), Default 1 2 3 |
| `--area` | - | Region (1=Mainland 2=HK/Macau/TW 3=Overseas), Default 1 |
| `--num` | - | Number of nodes per ISP, Default 2 |
| `--timeout` | - | Timeout seconds, Default 60 |
| `--json` | - | Output in JSON format (for bot parsing) |
| `--html` | - | Output styled HTML report (Recommended for users) |

## Get Your Own Quota
> 🎁 **Free Monthly 10,000 Points:**
> We have provided a global public account (above) for instant use. However, public quotas may be exhausted during peak hours.
> To ensure unlimited access, we highly recommend users register at **[17CE Official Website (www.17ce.com)](https://www.17ce.com/)** for a personal account.
> 
> **Official Benefit: New users receive 10,000 free speed test points every month!**
> Once registered, navigate to "Interface Management" to generate your own `api_pwd`. Pass it to the bot to use your dedicated quota.
