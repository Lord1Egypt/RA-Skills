---
name: AWS Knowledge
description: >
  AWS expert powered by the AWS Knowledge MCP Server (via mcporter). Provides real-time access
  to AWS documentation, best practices, SOPs, and regional availability. Use when the user asks
  about AWS services (S3, EC2, Lambda, CDK, CloudFormation, ECS, EKS, RDS, DynamoDB, Bedrock,
  SageMaker, IAM, VPC, etc.), AWS architecture patterns, deployment guidance, troubleshooting,
  regional availability, cost optimization, security hardening, or any "how do I do X on AWS"
  question. Also activates for CDK/CloudFormation infrastructure-as-code questions and
  AWS Well-Architected guidance.
metadata: {"openclaw":{"emoji":"☁️","requires":{"bins":["mcporter"]},"install":[{"id":"npm","kind":"node","package":"mcporter","bins":["mcporter"],"label":"Install mcporter (npm)"}]}}
---

# AWS Knowledge Skill

Query the AWS Knowledge MCP Server via mcporter for real-time AWS expertise.

The MCP server is `aws-knowledge` (must be configured in mcporter).

## Query Routing

Route each question to the right tool:

| Question Type | Tool | Example |
|---|---|---|
| General "how to" / best practices | `search_documentation` | "How to secure an S3 bucket" |
| Read a specific doc page | `read_documentation` | "Show me the Lambda pricing page" |
| Explore related topics | `recommend` | "What else should I know about VPC peering" |
| Is a service available in a region | `get_regional_availability` | "Is Bedrock available in ap-southeast-1" |
| List all AWS regions | `list_regions` | "What regions does AWS have" |
| Step-by-step task walkthrough | `retrieve_agent_sops` | "Walk me through deploying to ECS" |

## Tool Calling

All calls go through mcporter:

```bash
# Search documentation (most common)
mcporter call aws-knowledge.search_documentation query="<search terms>"

# Optionally filter by topic
mcporter call aws-knowledge.search_documentation query="<search terms>" topic="<topic>"

# Read a specific documentation page
mcporter call aws-knowledge.read_documentation url="<full doc URL>"

# Get recommendations for related content
mcporter call aws-knowledge.recommend url="<doc URL>"

# List all AWS regions
mcporter call aws-knowledge.list_regions

# Check regional availability
mcporter call aws-knowledge.get_regional_availability service="<service name>" region="<region id>"

# Get step-by-step SOPs
mcporter call aws-knowledge.retrieve_agent_sops query="<task description>"
```

## Workflow

1. **Classify the question** — determine which tool to call (see routing table above)
2. **Call the tool** — use mcporter with appropriate parameters
3. **Read deeper if needed** — use `read_documentation` on URLs from search results
4. **Synthesize the answer** — combine findings into a clear response
5. **Include sources** — always cite doc URLs so the user can verify
6. **Offer follow-ups** — suggest related topics or deeper dives

## Tips

- **Search first, don't guess.** Even for common topics, search to get the latest guidance.
- **Use SOPs for procedures.** If the user wants to DO something (deploy, configure, troubleshoot), check `retrieve_agent_sops` first — these are tested step-by-step workflows.
- **Check regional availability before recommending.** Don't assume a service is available everywhere.
- **Combine tools.** A typical flow: `search_documentation` → pick best result → `read_documentation` for full content → `recommend` for related reading.
- **Topic filtering.** When searching, use the `topic` parameter to narrow results if the query is broad.

## Domain Patterns

For common query patterns organized by AWS domain, see `references/query-patterns.md`.
