# Azure Bing Grounding Skill for OpenClaw

This skill enables OpenClaw (and its AI agents) to perform real-time web search and grounding using **Azure AI Agent Service** and the **Bing Grounding Search Tool**. It searches the web, synthesizes an answer using your deployed Azure OpenAI model, and provides URL citations for factual accuracy.

## Prerequisites

1. An **Azure AI Foundry** project.
2. An **Azure OpenAI** model deployment (e.g., `gpt-4o`).
3. A **Bing Grounding Search** resource connected to your AI Foundry project.
4. Python 3 installed.

## Installation

Install the required Python dependencies:

```bash
pip install azure-identity azure-ai-agents
```

## Configuration

You must provide your Azure endpoint, connection ID, and credentials. Add the following to your OpenClaw environment configuration (usually located at `~/.openclaw/.env`):

```bash
# ==========================================
# REQUIRED: Azure AI Foundry Configuration
# ==========================================

# Your Azure AI Foundry project endpoint
# e.g., "https://<your-resource>.services.ai.azure.com/api/projects/<your-project>"
FOUNDRY_PROJECT_ENDPOINT="<your-project-endpoint>"

# The ID of the Bing Grounding connection in your Azure AI Foundry Project
# e.g., "/subscriptions/.../connections/GroundingBingSearch"
BING_PROJECT_CONNECTION_ID="<your-connection-id>"

# ==========================================
# OPTIONAL: Model Configuration
# ==========================================

# Default model deployment name (Defaults to gpt-4o if not set)
FOUNDRY_MODEL_DEPLOYMENT_NAME="gpt-4o"

# ==========================================
# AUTHENTICATION
# ==========================================
# By default, the script will attempt to use `DefaultAzureCredential` (e.g., via `az login` or Managed Identity).
# If you are using a Service Principal, configure the following variables:

AZURE_TENANT_ID="<your-tenant-id>"
AZURE_CLIENT_ID="<your-client-id>"
AZURE_CLIENT_SECRET="<your-client-secret>"
```

## Usage

The skill includes a Python script located at `scripts/bing_grounding.py` that can be invoked via the CLI or by the OpenClaw agent.

### Basic Query (Markdown format)

```bash
python3 scripts/bing_grounding.py --query "What is the weather in Seattle today?" --format md
```

### Basic Query (Raw JSON format)

```bash
python3 scripts/bing_grounding.py --query "Latest news on AI" --format raw
```

### Specify a different model dynamically

```bash
python3 scripts/bing_grounding.py --query "Tell me a joke" --model "gpt-4o-mini" --format md
```

## Output Example

When using `--format md`, the output will look like this:

```markdown
根据天气预报，明天（3月24日）北京的天气以晴天为主，最高气温约为18℃，最低气温为5℃，天空晴朗，适合户外活动【3:0†source】【3:1†source】。

**Citations:**
- https://www.weather.com.cn/weather40d/101010100.shtml
- https://beijing.tianqi.com/beijing/mingtian/
```
