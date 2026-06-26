***

name: find-agents
version: 1.0.0
description: "AI-powered find agents that performs intelligent web searches, aggregates results, and provides summarized answers with source citations. Use when: user needs to find current information, research topics, verify facts, or gather data from multiple sources."
-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# Find Agents Skill

An intelligent AI-powered find agents that performs advanced web searches, aggregates results from multiple sources, and provides comprehensive, cited answers to user queries.

## Overview

Find Agent is a powerful research tool that combines web search capabilities with AI summarization. It helps users quickly find accurate, up-to-date information from across the internet without manually browsing multiple websites.

## Key Features

### 🔍 Multi-Source Search

- **Web Search**: Real-time search across major search engines
- **News Search**: Latest news and current events
- **Academic Search**: Scholarly articles and research papers
- **Image Search**: Visual content discovery
- **Code Search**: Programming solutions and documentation

### 🤖 AI-Powered Analysis

- **Smart Summarization**: Condenses multiple sources into coherent answers
- **Fact Verification**: Cross-references information across sources
- **Source Credibility**: Ranks sources by reliability and authority
- **Context Understanding**: Maintains conversation context for follow-up questions

### 📊 Result Organization

- **Structured Output**: Presents information in easy-to-read formats
- **Citation Tracking**: Every claim is backed by source links
- **Confidence Scoring**: Indicates reliability of information
- **Related Topics**: Suggests related queries for deeper exploration

## Use Cases

### 1. Research & Learning

- **Academic Research**: Find scholarly articles and citations
- **Topic Exploration**: Get comprehensive overviews of complex subjects
- **Fact Checking**: Verify claims with multiple authoritative sources
- **Learning New Skills**: Find tutorials, documentation, and best practices

### 2. Professional Work

- **Market Research**: Gather industry trends and competitor information
- **Technical Documentation**: Find official docs and community solutions
- **News Monitoring**: Stay updated on relevant industry news
- **Data Collection**: Aggregate statistics and reports

### 3. Daily Life

- **Product Research**: Compare features, prices, and reviews
- **Travel Planning**: Find destinations, hotels, and local information
- **Health Information**: Access reliable medical and wellness information
- **Current Events**: Get summaries of breaking news and developments

## Usage Examples

### Basic Search

```
User: "What are the latest developments in quantum computing?"
Search Agent: Performs web search → Aggregates results → Provides summary with citations
```

### Technical Query

```
User: "How to implement JWT authentication in Node.js?"
Search Agent: Searches code repositories → Finds tutorials → Provides code examples with sources
```

### Fact Verification

```
User: "Is it true that Python is the most popular programming language in 2024?"
Search Agent: Cross-references multiple sources → Provides verified answer with statistics
```

### News Search

```
User: "What happened in the tech industry this week?"
Search Agent: Searches recent news → Summarizes key events → Provides timeline
```

## Search Capabilities

### Supported Search Types

| Type       | Description          | Best For                         |
| ---------- | -------------------- | -------------------------------- |
| `general`  | Broad web search     | General knowledge, how-to guides |
| `news`     | Recent news articles | Current events, trending topics  |
| `academic` | Scholarly sources    | Research, citations, studies     |
| `code`     | Code repositories    | Programming solutions, libraries |
| `images`   | Visual content       | Reference images, diagrams       |

### Advanced Search Operators

- `"exact phrase"` - Search for exact matches
- `site:example.com` - Search within specific domain
- `filetype:pdf` - Find specific file types
- `-exclude` - Exclude specific terms
- `OR` - Search for either term

## Output Format

Search Agent provides structured responses:

```markdown
## Summary
[Concise answer to the query]

## Key Findings
- [Point 1 with citation]
- [Point 2 with citation]
- [Point 3 with citation]

## Sources
1. [Source Title](URL) - [Credibility Score]
2. [Source Title](URL) - [Credibility Score]

## Related Queries
- [Suggested follow-up 1]
- [Suggested follow-up 2]
```

## Technical Architecture

### Components

1. **Search Engine Interface**: Connects to multiple search APIs
2. **Content Fetcher**: Retrieves and parses web pages
3. **AI Analyzer**: Processes and summarizes content
4. **Citation Manager**: Tracks and formats source references
5. **Response Formatter**: Structures output for readability

### Data Flow

```
User Query → Search APIs → Content Extraction → AI Analysis → Citation Mapping → Formatted Response
```

## Configuration

### Environment Variables

```bash
SEARCH_API_KEY=your_search_api_key
AI_MODEL=gpt-4  # or other supported models
MAX_RESULTS=10  # number of sources to analyze
TIMEOUT=30000   # request timeout in milliseconds
```

### Customization Options

- **Result Count**: Adjust number of sources analyzed
- **Source Filters**: Whitelist/blacklist specific domains
- **Language Preferences**: Prioritize results in specific languages
- **Time Range**: Filter results by date (past day, week, month, year)

## Best Practices

### When to Use Search Agent

✅ Current information not in training data
✅ Verifying facts or claims
✅ Researching new or niche topics
✅ Finding specific technical solutions
✅ Gathering multiple perspectives

### When NOT to Use Search Agent

❌ Information already known to be in training data
❌ Personal or private information
❌ Highly sensitive queries
❌ When offline functionality is required

## Limitations

- **Search Dependency**: Requires internet connectivity
- **API Rate Limits**: Subject to search API quotas
- **Source Availability**: Limited by indexed web content
- **Real-time Lag**: News may have slight delays
- **Language Support**: Optimized for major languages

## Privacy & Security

- **No Query Logging**: User searches are not stored
- **Secure Connections**: All API calls use HTTPS
- **Source Verification**: Filters known malicious domains
- **Data Minimization**: Only fetches necessary content

## Integration

### With Other Skills

- **findskills**: Discover complementary skills
- **code-reviewer**: Verify code solutions found
- **translator**: Translate search results

### API Usage

```javascript
// Example: Using Search Agent programmatically
const searchAgent = require('search-agent');

const result = await searchAgent.search({
  query: "renewable energy trends 2024",
  type: "news",
  maxResults: 5
});
```

## Version History

- **v1.0.0** (Current)
  - Initial release
  - Multi-source search capability
  - AI-powered summarization
  - Citation tracking

## Support & Feedback

For issues, feature requests, or contributions:

- GitHub Issues: \[repository-url]
- Documentation: \[docs-url]
- Community: \[community-url]

## License

MIT License - See LICENSE file for details

***

**Keywords**: search, research, web search, AI search, information retrieval, fact checking, news aggregation, academic search, code search, intelligent agent, knowledge discovery, source citation, automated research
