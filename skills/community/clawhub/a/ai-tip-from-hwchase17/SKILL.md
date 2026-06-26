# AI Tip from @hwchase17

## Description
Automatically generated AI learning skill from curated web and social media sources.

## Steps

1. New in LangChain: You can now easily create custom agents with structured outputs!
2. from langchain_core.pydantic_v1 import BaseModel, Field
3. class Joke(BaseModel):
4. setup: str = Field(description="question to set up a joke")
5. punchline: str = Field(description="answer to resolve the joke")
6. llm.with_structured_output(Joke)

## Code Examples

```python
from langchain_core.pydantic_v1 import BaseModel, Field

class Joke(BaseModel):
    setup: str = Field(description="question to set up a joke")
    punchline: str = Field(description="answer to resolve the joke")

llm.with_structured_output(Joke)
```

## Dependencies
- Python 3.8+
- Relevant libraries (see code examples)
