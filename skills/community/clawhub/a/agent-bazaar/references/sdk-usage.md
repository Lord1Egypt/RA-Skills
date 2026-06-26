# Agent Bazaar — Programmatic Integration

## Direct HTTP (Any Language)

Agent Bazaar skills are standard HTTP endpoints. No SDK required.

```python
import requests

# Step 1: Call without payment to discover requirements
r = requests.post('https://agent-bazaar.com/api/x402/code-review',
    json={'code': 'print("hello")', 'language': 'python'})

if r.status_code == 402:
    payment_intent = r.json()['payment']
    # Step 2: Delegate payment to lobster.cash wallet
    # lobster.cash handles: amount, currency, signing, broadcast
    # Step 3: Retry with payment proof from lobster.cash
    r = requests.post('https://agent-bazaar.com/api/x402/code-review',
        json={'code': 'print("hello")', 'language': 'python'},
        headers={'X-402-Payment': payment_proof})

result = r.json()
```

## @agentbazaar/x402-sdk

Official SDK for framework integrations.

```bash
npm install @agentbazaar/x402-sdk
```

### Basic Usage

```typescript
import { AgentBazaarClient } from '@agentbazaar/x402-sdk';

const client = new AgentBazaarClient({
  baseUrl: 'https://agent-bazaar.com',
});

// Search capabilities (free)
const skills = await client.search({ q: 'code review' });

// Call a skill — payment delegated to wallet
const result = await client.call('code-review', {
  code: 'function add(a,b) { return a+b }',
  language: 'javascript'
});
```

### Demo Mode

```typescript
const client = new AgentBazaarClient({
  baseUrl: 'https://agent-bazaar.com',
  paymentToken: 'demo', // free testing, sample responses
});
```

## Framework Integrations

### LangChain

```typescript
import { AgentBazaarTool } from '@agentbazaar/x402-sdk/integrations/langchain';

const codeReview = new AgentBazaarTool({ skill: 'code-review' });
const agent = new AgentExecutor({ tools: [codeReview], llm: model });
```

### CrewAI

```python
from agentbazaar import AgentBazaarTool

code_review = AgentBazaarTool(skill="code-review")
agent = Agent(role="Code Reviewer", tools=[code_review])
```

### AutoGen

```python
from agentbazaar import AgentBazaarFunction

functions = [
    AgentBazaarFunction("code-review"),
    AgentBazaarFunction("content-writer"),
]
```

## agentbazaar CLI

```bash
npm install -g agentbazaar

agentbazaar search "code review"    # Find skills
agentbazaar info code-review        # Get details + pricing
agentbazaar call code-review --code "console.log('hi')" --payment demo
agentbazaar list                    # All available skills
agentbazaar analytics               # Usage stats
```
