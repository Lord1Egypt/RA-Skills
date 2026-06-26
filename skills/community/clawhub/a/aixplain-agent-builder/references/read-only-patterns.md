# Read-Only Patterns

Use these examples when the user wants a conservative aiXplain workflow.

## Search Existing Assets

```python
import os
from aixplain import Aixplain

aix = Aixplain(api_key=os.getenv("AIXPLAIN_API_KEY"))

web_tools = aix.Tool.search(query="web search").results
doc_tools = aix.Tool.search(query="document parser").results
drive_integrations = aix.Integration.search(query="google drive").results
```

## Build With an Existing Marketplace Tool

```python
import os
from aixplain import Aixplain

aix = Aixplain(api_key=os.getenv("AIXPLAIN_API_KEY"))

tool = aix.Tool.get("<PUBLIC_TOOL_ID>")

agent = aix.Agent(
    name="Research Assistant",
    description="Finds information using an existing marketplace search tool.",
    instructions="Use attached tools only. If a request needs missing permissions, explain the limitation.",
    tools=[tool],
    output_format="markdown",
    max_tokens=4000,
).save()
```

## Avoid by Default

Do not recommend these unless the user explicitly asks for them and approves the risk:

- remote file upload helpers when direct local configuration is supported
- authenticated integration setup flows
- direct low-level API calls that bypass standard SDK or platform flows
- runtime-execution tools
- custom script-backed tools
