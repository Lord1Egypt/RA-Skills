# 🔍 Search Agent

AI-powered search agent that performs intelligent web searches, aggregates results from multiple sources, and provides summarized answers with source citations.

[![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)](https://github.com/clawhub/search-agent)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Node.js](https://img.shields.io/badge/node-%3E%3D16.0.0-brightgreen.svg)](https://nodejs.org/)

## ✨ Features

- **🔍 Multi-Source Search** - Web, news, academic, and code search
- **🤖 AI-Powered Analysis** - Smart summarization and fact verification
- **📊 Structured Output** - Clear, cited answers with confidence scores
- **⚡ Quick Answers** - Get fast responses to simple questions
- **✅ Fact Checking** - Verify claims with multiple sources
- **🌐 Multi-Language** - Support for various languages

## 🚀 Quick Start

### Installation

```bash
# Install via npm
npm install -g search-agent

# Or install as a project dependency
npm install search-agent
```

### Basic Usage

```javascript
const searchAgent = require('search-agent');

// General search
const result = await searchAgent.search('latest AI developments');
console.log(result.summary);

// Quick answer
const answer = await searchAgent.quickSearch('what is quantum computing');
console.log(answer);

// Fact check
const verification = await searchAgent.factCheck('Python is the most popular language');
console.log(verification.verdict);
```

### CLI Usage

```bash
# Search
search-agent search "quantum computing latest news"

# Quick answer
search-agent quick "what is machine learning"

# Fact check
search-agent factcheck "TypeScript is better than JavaScript"

# News search
search-agent news "artificial intelligence"

# Academic search
search-agent academic "climate change effects"

# Code search
search-agent code "react hooks tutorial"
```

## 📖 API Reference

### `search(query, options)`

Performs an intelligent web search with AI-powered summarization.

**Parameters:**
- `query` (string): Search query
- `options` (Object): Search options
  - `type` (string): Search type - 'general', 'news', 'academic', 'code'
  - `maxResults` (number): Maximum number of results (default: 10)
  - `timeRange` (string): Time filter - 'day', 'week', 'month', 'year'

**Returns:** Promise<Object> with summary, key findings, sources, and metadata

### `quickSearch(query)`

Gets a quick answer for simple queries.

**Parameters:**
- `query` (string): Search query

**Returns:** Promise<string> with concise answer

### `factCheck(claim)`

Verifies a claim or fact using multiple sources.

**Parameters:**
- `claim` (string): Claim to verify

**Returns:** Promise<Object> with verdict, confidence, and evidence

### `searchNews(topic, options)`

Searches for recent news on a topic.

**Parameters:**
- `topic` (string): News topic
- `options` (Object): Additional options

**Returns:** Promise<Object> with news results

### `searchAcademic(query)`

Searches academic sources and scholarly articles.

**Parameters:**
- `query` (string): Research query

**Returns:** Promise<Object> with academic results

### `searchCode(query)`

Searches for code solutions and programming resources.

**Parameters:**
- `query` (string): Code query

**Returns:** Promise<Object> with code results

## ⚙️ Configuration

### Environment Variables

```bash
# Required
SEARCH_API_KEY=your_search_api_key

# Optional
SEARCH_MAX_RESULTS=10      # Maximum results (default: 10)
SEARCH_TIMEOUT=30000       # Request timeout in ms (default: 30000)
SEARCH_LANGUAGE=zh-CN      # Language code (default: zh-CN)
AI_MODEL=gpt-4            # AI model for summarization
```

### Programmatic Configuration

```javascript
const { config } = require('search-agent');

// Update configuration
config.maxResults = 20;
config.timeout = 60000;
config.language = 'en';
```

## 📝 Output Format

Search Agent returns structured results:

```javascript
{
  query: "your search query",
  summary: "AI-generated summary of findings",
  keyFindings: [
    {
      point: "Key finding 1",
      source: "https://example.com",
      credibility: 85
    }
  ],
  confidence: 78,
  sources: [
    {
      index: 1,
      title: "Source Title",
      url: "https://example.com",
      credibility: 85,
      publishedAt: "2024-01-15"
    }
  ],
  relatedQueries: ["related topic 1", "related topic 2"],
  metadata: {
    totalSources: 5,
    searchTime: "2024-01-20T10:30:00Z",
    language: "zh-CN"
  }
}
```

## 🎯 Use Cases

### Research & Learning
- Academic research and citation finding
- Topic exploration and learning
- Fact verification and myth-busting
- Tutorial and documentation discovery

### Professional Work
- Market research and competitor analysis
- Technical documentation lookup
- Industry news monitoring
- Data and statistics gathering

### Daily Life
- Product research and comparison
- Travel planning and recommendations
- Health and wellness information
- Current events and news summaries

## 🔧 Advanced Search Operators

- `"exact phrase"` - Search for exact matches
- `site:example.com` - Search within specific domain
- `filetype:pdf` - Find specific file types
- `-exclude` - Exclude specific terms
- `OR` - Search for either term

## 🛡️ Privacy & Security

- No query logging - searches are not stored
- Secure HTTPS connections for all API calls
- Source verification and malicious domain filtering
- Data minimization - only fetches necessary content

## 🧪 Testing

```bash
# Run tests
npm test

# Run with coverage
npm run test:coverage

# Run linting
npm run lint

# Format code
npm run format
```

## 🤝 Contributing

Contributions are welcome! Please read our [Contributing Guide](CONTRIBUTING.md) for details.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Thanks to all contributors who have helped shape Search Agent
- Special thanks to the OpenClaw community for support and feedback

## 📞 Support

- 🐛 [Report Issues](https://github.com/clawhub/search-agent/issues)
- 📖 [Documentation](https://github.com/clawhub/search-agent/wiki)
- 💬 [Discussions](https://github.com/clawhub/search-agent/discussions)

---

**Made with ❤️ by the Search Agent Team**
