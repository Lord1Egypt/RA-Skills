# Example 3: Building a Content Creator Agent

This example demonstrates how to build an AI content creator for blogs, social media, and newsletters.

## Goal

Create an agent that can:
1. Research topics automatically
2. Generate high-quality content
3. Optimize for SEO
4. Publish to multiple platforms

## Step 1: Create the Agent

```bash
openclaw agent create content-creator \
  --name "创作小助手" \
  --role "内容创作者" \
  --tone "creative, engaging, informative" \
  --toolkit agent-dev-toolkit
```

## Step 2: Configure Content Guidelines

Edit `AGENTS.md`:

```markdown
## Content Guidelines

### Style Rules
- Use clear, conversational language
- Include examples and stories
- Break into scannable sections
- Add visuals when possible

### Quality Standards
- Minimum 1,500 words for articles
- Include 3-5 internal links
- Add meta description (150-160 chars)
- Optimize for target keywords

### Never Do
- Plagiarize content
- Make up facts or statistics
- Use clickbait headlines
- Ignore copyright

### Always
- Cite sources
- Fact-check claims
- Proofread before publishing
- Track performance metrics
```

## Step 3: Set Up Research Workflow

Use **Agent Browser** to research topics:

```javascript
// Research a topic
async function researchTopic(topic) {
  // Search for latest articles
  await browser.navigate(`https://www.google.com/search?q=${topic}`);
  const articles = await browser.extractMultiple('.search-result');
  
  // Gather key points
  const keyPoints = [];
  for (const article of articles) {
    await browser.click(article);
    const content = await browser.extract('article');
    keyPoints.push(extractKeyPoints(content));
    await browser.back();
  }
  
  return synthesizeResearch(keyPoints);
}

// Find statistics
async function findStatistics(topic) {
  await browser.navigate(`https://www.statista.com/search?q=${topic}`);
  const stats = await browser.extractMultiple('.statistic');
  return validateStatistics(stats);
}
```

## Step 4: Create Content Templates

Use **Agent Docs** to create templates:

```bash
# Create article template
openclaw docs create-template \
  --type article \
  --output ./templates/article.md

# Create social media template
openclaw docs create-template \
  --type social \
  --output ./templates/social.md
```

## Step 5: Implement SEO Optimization

```javascript
// Optimize content for SEO
async function optimizeForSEO(content, keyword) {
  // Check keyword density
  const density = calculateKeywordDensity(content, keyword);
  if (density < 0.5 || density > 2.5) {
    content = adjustKeywordDensity(content, keyword);
  }
  
  // Generate meta tags
  const meta = {
    title: generateTitle(content, keyword),
    description: generateDescription(content),
    tags: extractKeywords(content)
  };
  
  // Add internal links
  content = addInternalLinks(content);
  
  return { content, meta };
}
```

## Step 6: Set Up Publishing Pipeline

```bash
# Connect to WordPress
openclaw platform connect wordpress \
  --agent content-creator \
  --url "https://yourblog.com" \
  --credentials ./wordpress-credentials.json

# Connect to Medium
openclaw platform connect medium \
  --agent content-creator \
  --integration-token "your-token"

# Connect to Twitter/X
openclaw platform connect twitter \
  --agent content-creator \
  --api-key "your-key"
```

## Content Calendar

Create an automated content calendar:

```bash
# Create calendar
openclaw calendar create \
  --agent content-creator \
  --frequency "3 articles/week" \
  --topics "AI, productivity, technology"
```

Example schedule:
```
Monday: Research + Outline
Tuesday: Write Article 1
Wednesday: Edit + SEO
Thursday: Write Article 2
Friday: Schedule + Promote
Saturday: Research trends
Sunday: Plan next week
```

## Quality Assurance

### Automated Checks

```bash
# Run quality checks
openclaw qa check \
  --agent content-creator \
  --checks "grammar,plagiarism,seo,readability"
```

### Manual Review Workflow

```bash
# Submit for review
openclaw workflow start \
  --agent content-creator \
  --type review \
  --approvers "editor@company.com"
```

## Performance Tracking

```bash
# Track article performance
openclaw analytics track \
  --agent content-creator \
  --metrics "views,shares,comments,conversion"

# Generate performance report
openclaw report generate content-creator \
  --type monthly \
  --output ./reports/content-performance.md
```

## Monetization Strategies

### 1. Subscription Newsletter

```bash
# Set up newsletter
openclaw newsletter setup \
  --agent content-creator \
  --platform substack \
  --price 10/month
```

### 2. Sponsored Content

```bash
# Manage sponsorships
openclaw sponsorship manage \
  --agent content-creator \
  --rate 500/post
```

### 3. Affiliate Marketing

```javascript
// Add affiliate links automatically
async function addAffiliateLinks(content) {
  const products = extractProductMentions(content);
  for (const product of products) {
    const affiliateLink = await getAffiliateLink(product);
    content = replaceProductLink(content, product, affiliateLink);
  }
  return content;
}
```

## Advanced Features

### Multi-Language Support

```bash
# Enable translation
openclaw translation enable \
  --agent content-creator \
  --languages "en,zh,es,ja"
```

### Content Repurposing

```bash
# Repurpose article to social posts
openclaw content repurpose \
  --agent content-creator \
  --source article.md \
  --target "twitter,linkedin,instagram"
```

### A/B Testing Headlines

```javascript
// Test different headlines
async function testHeadlines(articleId) {
  const headlines = generateHeadlines(articleId);
  const results = await runABTest(headlines);
  return selectBestHeadline(results);
}
```

## Cost Analysis

**Initial costs:**
- Toolkit: $29
- Platform integrations: $0-50

**Monthly costs:**
- OpenClaw: $20-100
- Research tools: $50-200
- Publishing platforms: $0-100
- Total: $70-400/month

**Revenue potential:**
- Newsletter subscriptions: $500-5,000/month
- Sponsored content: $1,000-10,000/month
- Affiliate income: $200-2,000/month
- Total: $1,700-17,000/month

## Success Metrics

Track these KPIs:

1. **Content Volume**
   - Articles published per week
   - Word count
   - Social posts

2. **Engagement**
   - Page views
   - Time on page
   - Social shares
   - Comments

3. **SEO Performance**
   - Keyword rankings
   - Organic traffic
   - Backlinks

4. **Revenue**
   - Subscription revenue
   - Sponsor revenue
   - Affiliate revenue

## Tips for Success

1. **Consistency**: Publish regularly
2. **Quality**: Never sacrifice quality for quantity
3. **Engagement**: Respond to comments
4. **Analytics**: Track and optimize
5. **Diversification**: Multiple revenue streams
6. **Authenticity**: Build genuine audience relationships

## Next Steps

1. Set up your agent
2. Create content calendar
3. Connect publishing platforms
4. Start creating!
5. Monitor and optimize

Happy creating! 🚀
