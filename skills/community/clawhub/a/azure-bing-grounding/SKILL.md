---
name: azure-bing-grounding
slug: azure-bing-grounding
version: 1.0.0
description: "Web search grounding via Azure Foundry and Bing Grounding Search tool. Use when the user needs up-to-date information searched from the web via Azure AI Agents. Returns the synthesized answer and URL citations."
---

# Azure Bing Grounding

Use the bundled Python script to perform grounded searches using Azure Foundry's Agent Service and the Bing Grounding Search Tool.

## Requirements

1. Required Python packages:
   ```bash
   pip install azure-identity azure-ai-agents
   ```

2. Authentication:
   - Ensure Azure CLI is logged in (`az login`), OR 
   - Set Azure Service Principal / Managed Identity credentials compatible with `DefaultAzureCredential` or `ClientSecretCredential`.

3. Environment Variables:
   Add the following to your `~/.openclaw/.env` file or export them in your shell:
   ```bash
   # Your Azure AI Foundry project endpoint
   FOUNDRY_PROJECT_ENDPOINT="https://<your-resource>.ai.azure.com/api/projects/<your-project>"
   
   # The ID of the Bing Grounding connection in your Azure AI Foundry Project
   BING_PROJECT_CONNECTION_ID="<your-connection-id>"

   # Default model deployment name (optional, defaults to gpt-4o)
   FOUNDRY_MODEL_DEPLOYMENT_NAME="gpt-4o"
   
   # (Optional) Service Principal Credentials if not using DefaultAzureCredential
   AZURE_TENANT_ID="<tenant-id>"
   AZURE_CLIENT_ID="<client-id>"
   AZURE_CLIENT_SECRET="<client-secret>"
   ```

## Commands

Run from the OpenClaw workspace:

```bash
# Raw JSON output (default)
python3 {baseDir}/scripts/bing_grounding.py --query "What is the latest AI news today?"

# Markdown human-readable output
python3 {baseDir}/scripts/bing_grounding.py --query "What is the latest AI news today?" --format md

# Use a specific model deployment (default is gpt-4o)
python3 {baseDir}/scripts/bing_grounding.py --query "Weather in Seattle?" --model "gpt-4o-mini"
```

## Output

Returns a generated response synthesized by the Azure AI Agent based on Bing Search results, along with the source URL citations.
