# Competitor Finder Skill

## Purpose
Identifies 3-5 competitors for a given brand by searching the web via SerpAPI and, as a last resort, falling back to a minimal OpenAI call. Returns competitor names, websites, and optionally the reason they are considered competitors. This collector feeds into the Marketing Audit Pipeline to populate the Competitor Landscape section of the final report.

## Input Schema
```typescript
// Function signature
collectCompetitors(brandName: string, domain?: string): Promise<CompetitorData>

// brandName: The brand name to find competitors for (e.g. "Gymshark")
// domain: Optional domain for additional context (e.g. "gymshark.com").
// Helps refine competitor search and filter out the brand itself from results.
```

## Output Schema
```typescript
interface CompetitorData {
 competitors: CompetitorEntry[]; // 3-5 competitor entries
 error?: string; // Present only when collector fails
}

interface CompetitorEntry {
 name: string; // e.g. "Nike"
 website: string; // e.g. "nike.com"
 reason?: string; // e.g. "Direct competitor in activewear market"
}
```

## API Dependencies

### Primary: SerpAPI
- **API Name:** SerpAPI (Google Search)
- **Endpoint:** `https://serpapi.com/search.json`
- **Auth:** `SERPAPI_KEY` environment variable
- **Cost estimate:** ~$0.005 per search
- **Rate limits:** Depends on plan; free tier allows 100 searches/month

### Secondary: DataForSEO
- **API Name:** DataForSEO Competitor Domain API
- **Endpoint:** `https://api.dataforseo.com/v3/dataforseo_labs/google/competitors_domain/live`
- **Auth:** `DATAFORSEO_LOGIN` + `DATAFORSEO_PASSWORD` environment variables
- **Cost estimate:** ~$0.01 per request
- **Rate limits:** Depends on plan; free tier allows 100 requests/month

### Fallback: OpenAI (minimal call)
- **API Name:** OpenAI API
- **Model:** `gpt-4.1-mini`
- **Auth:** `OPENAI_API_KEY` environment variable
- **Cost estimate:** ~$0.001 per call (minimal prompt)
- **Usage:** Only used when both SerpAPI and DataForSEO fail or return no results

## Implementation Pattern

### Data Flow
1. Receive `brandName` and optional `domain` from the pipeline
2. Attempt Method 1: SerpAPI search
3. If Method 1 fails or returns insufficient results, attempt Method 2: DataForSEO
4. If both fail, attempt Method 3: OpenAI fallback (minimal prompt)
5. Deduplicate and filter results (remove the brand itself)
6. Return 3-5 competitors mapped to `CompetitorData`

### Method 1: SerpAPI Search
```typescript
// Query: "top competitors of {brandName}"
{
 api_key: process.env.SERPAPI_KEY,
 engine: "google",
 q: `top competitors of ${brandName}`,
 num: 10
}
```
- Parse organic results to extract competitor brand names and domains
- Look for listicle-style results ("Top 10 Gymshark competitors...")
- Extract domain names from result URLs
- Filter out non-competitor results (news articles, the brand's own site)

### Method 2: DataForSEO Competitor Domain
```typescript
[{
 target: domain, // e.g. "gymshark.com"
 language_code: "en",
 location_code: 2840, // United States
 limit: 5
}]
```
- Returns domains that compete for the same keywords
- More accurate than SERP search but requires the domain parameter

### Method 3: OpenAI Fallback (Minimal)
```typescript
// ONLY used when Methods 1 and 2 both fail
// This is a MINIMAL prompt -- keep token usage as low as possible
const response = await openai.chat.completions.create({
 model: 'gpt-4.1-mini',
 max_tokens: 200,
 temperature: 0.3,
 messages: [
 {
 role: 'system',
 content: 'You are a marketing analyst. Return only a JSON array of competitor objects.'
 },
 {
 role: 'user',
 content: `List 5 direct competitors of "${brandName}"${domain ? ` (${domain})` : ''}. Return JSON: [{"name":"...","website":"...","reason":"..."}]`
 }
 ]
});
```
- Parse the JSON response
- This call costs ~$0.001 and should only happen when SERP/DataForSEO APIs are unavailable
- Log a warning when this fallback is used so it can be monitored

### Result Filtering
- Remove entries where the name or website matches the input brand
- Deduplicate by website domain (normalize: strip www, trailing slashes)
- Ensure each entry has both `name` and `website` populated
- Limit to 5 results maximum; aim for at least 3

## Error Handling
- Entire function wrapped in `try/catch`
- On failure of all three methods, return `EMPTY_COMPETITOR_DATA` with `error` field set:
 ```typescript
 return { ...EMPTY_COMPETITOR_DATA, error: 'Competitor data unavailable: <reason>' };
 ```
- Never throw -- always return a valid `CompetitorData` object
- Log errors with Winston logger including brandName and method that failed:
 ```typescript
 logger.error('Competitor collector failed', { brandName, domain, method, err });
 ```
- Log warnings when falling back to secondary/tertiary methods:
 ```typescript
 logger.warn('Competitor finder: SerpAPI failed, falling back to DataForSEO', { brandName });
 logger.warn('Competitor finder: DataForSEO failed, falling back to OpenAI', { brandName });
 ```
- Common failure scenarios:
 - SerpAPI key invalid or quota exhausted
 - DataForSEO credentials invalid or out of credits
 - OpenAI API key invalid
 - No competitors found for niche or unknown brand
 - Network timeout on any API

## Example Usage
```typescript
import { collectCompetitors } from '../collectors/competitorCollector';

// Successful collection (via SerpAPI)
const data = await collectCompetitors('Gymshark', 'gymshark.com');
// Returns:
// {
// competitors: [
// { name: "Nike", website: "nike.com", reason: "Global leader in athletic apparel" },
// { name: "Lululemon", website: "lululemon.com", reason: "Premium activewear competitor" },
// { name: "Under Armour", website: "underarmour.com", reason: "Direct competitor in gym wear" },
// { name: "Alphalete", website: "alphalete.com", reason: "DTC fitness apparel brand" },
// { name: "Fabletics", website: "fabletics.com", reason: "Subscription-based activewear" },
// ],
// }

// Partial result (only OpenAI fallback worked)
const partial = await collectCompetitors('ObscureBrand');
// Returns:
// {
// competitors: [
// { name: "CompetitorA", website: "competitora.com", reason: "Similar product category" },
// { name: "CompetitorB", website: "competitorb.com", reason: "Same target market" },
// { name: "CompetitorC", website: "competitorc.com" },
// ],
// }

// Failed collection (graceful degradation)
const failedData = await collectCompetitors('UnknownBrand');
// Returns:
// {
// competitors: [],
// error: "Competitor data unavailable: All methods failed"
// }
```

## Notes
- This collector uses a three-tier fallback strategy to maximize data availability. SerpAPI is preferred because it provides real SERP data. DataForSEO provides keyword-overlap-based competitors. OpenAI is a last resort.
- The OpenAI fallback is the ONLY place outside of `reportGenerator.ts` where an AI model call is permitted. It must be minimal (max 200 tokens) and should be logged as a warning for cost monitoring.
- When the input type is `'instagram'` (no domain available), skip Method 2 (DataForSEO requires a domain) and rely on Methods 1 and 3.
- The `EMPTY_COMPETITOR_DATA` constant is defined in `src/types/audit.types.ts` and should be imported for fallback returns.
- Competitor data is inherently subjective. The report generator (GPT-4.1-mini) will contextualize the raw competitor list into strategic analysis.
- This collector must never block the pipeline. Even a complete failure returns valid typed data with an error flag.
