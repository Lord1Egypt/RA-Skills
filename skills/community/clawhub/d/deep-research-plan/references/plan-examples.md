# Research Plan Examples

These examples demonstrate the research plan format that defines WHAT to research without specifying HOW to search.

## Example 1: Technology Research

```json
{
  "topic": "AI agents in software development",
  "research_questions": [
    "What AI agent frameworks and tools are currently available?",
    "How are companies and developers using AI agents for coding?",
    "What are the main limitations and challenges of AI coding agents?",
    "What is the future outlook and roadmap for AI coding agents?"
  ],
  "scope": {
    "include": ["development tools", "productivity studies", "enterprise adoption"],
    "exclude": ["AI agents for non-coding tasks", "general AI research"]
  },
  "report_requirements": {
    "sections": ["executive_summary", "findings", "conclusion", "references"],
    "depth": "comprehensive",
    "min_sources": 10,
    "focus_areas": ["practical applications", "technical capabilities"]
  }
}
```

## Example 2: Market Research

```json
{
  "topic": "Electric vehicle market in China",
  "research_questions": [
    "What is the current market size and growth trajectory?",
    "Who are the major players and what are their market positions?",
    "What government policies and incentives affect the market?",
    "What are consumer adoption trends and preferences?"
  ],
  "scope": {
    "include": ["passenger EVs", "charging infrastructure", "policy analysis"],
    "exclude": ["commercial vehicles", "hybrid vehicles"]
  },
  "report_requirements": {
    "sections": ["executive_summary", "market_overview", "competitive_landscape", "policy_analysis", "conclusion", "references"],
    "depth": "detailed",
    "min_sources": 12,
    "focus_areas": ["market data", "policy impact"]
  }
}
```

## Example 3: Academic/Technical Research

```json
{
  "topic": "Large language model safety and alignment",
  "research_questions": [
    "What are the primary safety concerns with current LLMs?",
    "What alignment techniques are being researched and deployed?",
    "What evaluation methods and benchmarks exist for safety?",
    "What are the major open problems and research directions?"
  ],
  "scope": {
    "include": ["safety techniques", "evaluation frameworks", "recent research"],
    "exclude": ["general AI ethics", "non-LLM AI safety"]
  },
  "report_requirements": {
    "sections": ["executive_summary", "findings", "conclusion", "references"],
    "depth": "technical",
    "min_sources": 15,
    "focus_areas": ["technical approaches", "evaluation methods"]
  },
  "notes": "Focus on papers from 2023-2025 and major research labs"
}
```

## Example 4: Competitive Analysis

```json
{
  "topic": "Cloud storage services comparison",
  "research_questions": [
    "What are the major cloud storage providers and their offerings?",
    "How do pricing models compare across providers?",
    "What are the key differentiating features?",
    "What are user reviews and satisfaction ratings?"
  ],
  "scope": {
    "include": ["AWS S3", "Google Cloud Storage", "Azure Blob", "pricing analysis"],
    "exclude": ["consumer file sharing", "personal backup solutions"]
  },
  "report_requirements": {
    "sections": ["executive_summary", "provider_comparison", "pricing_analysis", "feature_matrix", "conclusion", "references"],
    "depth": "detailed",
    "min_sources": 8,
    "focus_areas": ["enterprise features", "cost comparison"]
  }
}
```

## Key Principles

**Research Questions**: Define what to investigate. Should be specific enough to guide research but open enough to allow discovery.

**Scope**: Boundaries of research. Include defines what must be covered. Exclude prevents drift into tangential topics.

**Report Requirements**: Expectations for output. Sections define structure. Depth guides analysis level. Focus areas indicate priorities.

**No Search Specification**: The plan does NOT include keywords, queries, sources, or number of searches. The Sub Agent determines search strategy based on research questions.
