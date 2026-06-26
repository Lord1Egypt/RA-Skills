# API Documentation: AI Content Generator Pro

## Overview
This document provides technical details for developers extending or integrating with the AI Content Generator Pro skill.

## Architecture

### File Structure
```
ai-content-generator-pro/
├── index.js              # Main skill entry point
├── config/               # Configuration files
│   ├── config.json      # User configuration
│   ├── models.json      # AI model configurations
│   ├── templates.json   # Content templates
│   └── prompts.json     # AI prompt templates
├── lib/                  # Core libraries (planned)
│   ├── generators/      # Content type generators
│   ├── models/         # AI model integrations
│   ├── utils/          # Utility functions
│   └── storage/        # Data storage
├── scripts/             # Setup and maintenance
└── references/          # Documentation
```

## Core Functions

### Main Skill Handler
```javascript
export default async function aiContentGeneratorPro(args, context) {
  // args: Array of command arguments
  // context: OpenClaw execution context
  // Returns: String output or Promise
}
```

### Content Generation Flow
1. Parse command and arguments
2. Load configuration and templates
3. Select appropriate AI model
4. Generate content using prompts
5. Apply optimizations (SEO, tone)
6. Save and return results

## Configuration API

### Configuration Structure
```json
{
  "openai": {
    "apiKey": "string",
    "model": "string"
  },
  "anthropic": {
    "apiKey": "string", 
    "model": "string"
  },
  "xai": {
    "apiKey": "string",
    "model": "string"
  },
  "defaultModel": "string",
  "tone": "string",
  "seo": {
    "enabled": "boolean",
    "keywords": ["array"]
  }
}
```

### Configuration Methods
```javascript
// Load configuration
const config = loadConfig();

// Save configuration
saveConfig(config);

// Update configuration
updateConfig(key, value);
```

## Content Generation API

### Available Generators
```javascript
// Blog posts
async function generateBlogPost(topic, config) {}

// Social media content
async function generateSocialMedia(topic, config) {}

// Email content  
async function generateEmail(topic, config) {}

// Product descriptions
async function generateProductDescription(topic, config) {}

// Ad copy
async function generateAdCopy(topic, config) {}

// Video scripts
async function generateVideoScript(topic, config) {}
```

### Generator Parameters
Each generator accepts:
- `topic`: String - Main topic or subject
- `config`: Object - User configuration
- `options`: Object (optional) - Additional parameters

## AI Model Integration

### Model Interface
```javascript
class AIModel {
  constructor(provider, config) {}
  
  async generate(prompt, options) {
    // Returns: { content: string, metadata: object }
  }
  
  async optimize(content, options) {}
  
  async analyze(content, options) {}
}
```

### Available Providers
1. **OpenAI**: GPT-4, GPT-4 Turbo, GPT-3.5
2. **Anthropic**: Claude 3 Opus, Sonnet, Haiku
3. **xAI**: Grok Beta, Grok 2

### Model Selection Logic
```javascript
function selectModel(contentType, config) {
  const recommendations = config.models.recommendations[contentType];
  const available = recommendations.filter(model => 
    config[model] && config[model].apiKey
  );
  return available[0] || config.defaultModel;
}
```

## Storage API

### Content Storage
```javascript
// Save generated content
function saveContent(content, metadata) {
  // Saves to SQLite database
  // Returns: contentId
}

// Load content
function loadContent(contentId) {
  // Returns: { content, metadata }
}

// List content
function listContent(options) {
  // Returns: Array of content items
}

// Delete content
function deleteContent(contentId) {}
```

### Database Schema
```sql
CREATE TABLE content (
  id TEXT PRIMARY KEY,
  type TEXT,
  topic TEXT,
  content TEXT,
  model TEXT,
  tone TEXT,
  seo_score INTEGER,
  created_at TIMESTAMP,
  updated_at TIMESTAMP
);

CREATE TABLE exports (
  id TEXT PRIMARY KEY,
  content_id TEXT,
  format TEXT,
  path TEXT,
  created_at TIMESTAMP
);
```

## Extension Points

### Adding New Content Types
1. Add template to `config/templates.json`
2. Add prompts to `config/prompts.json`
3. Create generator in `lib/generators/`
4. Register in main handler

### Adding New AI Models
1. Add model configuration to `config/models.json`
2. Create model class in `lib/models/`
3. Update model selection logic

### Custom Optimizations
```javascript
// Register custom optimizer
function registerOptimizer(name, optimizer) {
  // optimizer: function(content, config) -> optimizedContent
}

// Available optimization hooks
- preGeneration(content, config)
- postGeneration(content, config)  
- preExport(content, config)
- postExport(content, config)
```

## Error Handling

### Common Errors
```javascript
const ERRORS = {
  NO_API_KEY: 'API key not configured',
  MODEL_UNAVAILABLE: 'AI model not available',
  RATE_LIMITED: 'Rate limit exceeded',
  INVALID_CONTENT_TYPE: 'Unsupported content type',
  STORAGE_ERROR: 'Failed to save content'
};
```

### Error Response Format
```javascript
{
  success: false,
  error: {
    code: 'ERROR_CODE',
    message: 'Human readable message',
    details: {} // Additional context
  }
}
```

## Performance Considerations

### Caching Strategy
1. **Prompt Caching**: Cache common prompt responses
2. **Model Caching**: Cache model instances
3. **Content Caching**: Cache generated content

### Rate Limiting
- Implement per-user rate limits
- Respect API provider limits
- Queue system for high volume

### Memory Management
- Stream large content generation
- Clean up temporary files
- Monitor memory usage

## Security

### API Key Management
- Never log API keys
- Encrypt stored keys
- Validate key format

### Content Safety
- Validate generated content
- Implement content filters
- Log generation attempts

### Data Privacy
- Local storage option
- Data encryption
- User data isolation

## Testing

### Unit Tests
```javascript
// Test content generation
test('generate blog post', async () => {
  const content = await generateBlogPost('test', config);
  expect(content).toContain('test');
});

// Test model selection
test('select model for blog', () => {
  const model = selectModel('blog', config);
  expect(['openai', 'anthropic']).toContain(model);
});
```

### Integration Tests
- API connectivity tests
- End-to-end generation tests
- Performance tests

### Mock Data
```javascript
// Mock AI responses
const mockAI = {
  generate: async (prompt) => `Mock: ${prompt.substring(0, 50)}`
};
```

## Deployment

### Build Process
```bash
# Install dependencies
npm install

# Run tests
npm test

# Package for distribution
npm run package
```

### Installation
```bash
# OpenClaw installation
openclaw skill install ./ai-content-generator-pro

# Manual installation
cp -r ai-content-generator-pro /path/to/openclaw/skills/
```

### Updates
1. Backup configuration
2. Update skill files
3. Run migration scripts if needed
4. Verify functionality

## Support & Troubleshooting

### Common Issues
1. **API Key Errors**: Verify key format and permissions
2. **Rate Limiting**: Implement exponential backoff
3. **Content Quality**: Adjust temperature and prompts
4. **Performance Issues**: Check caching and optimization

### Debug Mode
```bash
# Enable debug logging
DEBUG=ai-content-generator-pro node index.js generate blog test
```

### Log Files
- `logs/error.log`: Error messages
- `logs/access.log`: Generation requests
- `logs/performance.log`: Timing metrics

## Version History

### v1.0.0 (Initial Release)
- Basic content generation
- Multi-model support
- SEO optimization
- Content calendar

### Planned Features
- v1.1: Brand voice training
- v1.2: Team collaboration
- v1.3: Advanced analytics
- v2.0: Enterprise features

## Contributing
See CONTRIBUTING.md for guidelines on contributing to the skill development.