# Data Extraction Template

This template handles the extraction of structured data from scraped content.

## Parameters

- `content`: Scraped content (markdown or HTML)
- `extraction_prompt`: Instructions for what data to extract
- `schema`: Expected data structure (optional)

## Process

### Option 1: AI-Powered Extraction

Use Bright Data's `extract` tool for intelligent extraction:

```json
{
  "tool": "extract",
  "parameters": {
    "url": "{{url}}",
    "extraction_prompt": "{{extraction_prompt}}"
  }
}
```

**Extraction Prompt Examples**:

**E-commerce Products**:
```
Extract: product name, price (as number, exclude currency symbol),
availability (in stock/out of stock), rating (0-5 scale),
number of reviews, seller name, main features (as array of strings),
product image URL
```

**Articles**:
```
Extract: article title, author name, publication date (YYYY-MM-DD),
article category, main topics (array of 3-5 keywords),
summary (max 200 words), key insights (array of bullet points)
```

**General**:
```
Extract the main heading, all subheadings with their levels,
the main content summary, all links with their anchor text,
and metadata like date, author, tags
```

### Option 2: Manual Extraction

Parse the scraped content directly:

```markdown
# From Markdown Content

1. Extract heading (first # heading)
2. Extract all subheadings (##, ###)
3. Extract lists and tables
4. Extract links: [text](url) format
5. Extract metadata (dates, authors, etc.)
```

## Data Validation

After extraction, validate:

### Type Validation
- Numbers: Ensure numeric fields are actual numbers
- Dates: Ensure dates are valid (YYYY-MM-DD format)
- URLs: Ensure URLs are well-formed
- Emails: Ensure email format is correct

### Completeness Check
- All required fields are present
- No null/empty values in required fields
- Arrays have at least one element
- Strings are not empty strings

### Range Validation
- Ratings: 0-5 or 0-10
- Prices: Greater than 0
- Percentages: 0-100
- Dates: Within reasonable range

### Consistency Check
- Related fields make sense together
- No contradictory information
- Units are consistent (currency, measurements)

## Common Extraction Schemas

### E-commerce Product

```json
{
  "product_name": "string",
  "price": "number",
  "currency": "string (USD, EUR, etc.)",
  "availability": "string (in_stock, out_of_stock, preorder)",
  "rating": "number (0-5)",
  "review_count": "number",
  "seller": {
    "name": "string",
    "rating": "number",
    "url": "string"
  },
  "features": ["string"],
  "images": ["string (URLs)"],
  "url": "string",
  "scraped_at": "ISO 8601 timestamp"
}
```

### Article/Blog Post

```json
{
  "title": "string",
  "author": "string",
  "publication_date": "YYYY-MM-DD",
  "category": "string",
  "tags": ["string"],
  "summary": "string",
  "key_points": ["string"],
  "word_count": "number",
  "reading_time_minutes": "number",
  "url": "string",
  "scraped_at": "ISO 8601 timestamp"
}
```

### Company/Organization

```json
{
  "name": "string",
  "industry": "string",
  "founded_year": "number",
  "headquarters": "string",
  "employee_count": "string (e.g., '10,000+')",
  "website": "string (URL)",
  "description": "string",
  "key_people": [{"name": "string", "title": "string"}],
  "products_services": ["string"],
  "url": "string",
  "scraped_at": "ISO 8601 timestamp"
}
```

## Handling Missing Data

When a field is missing:
1. **Use default values**: `null`, `0`, `""`, `[]`
2. **Mark as missing**: Add field like `"field_missing": true`
3. **Log the issue**: Track which fields are frequently missing
4. **Don't fail**: Continue with available data

## Handling Malformed Data

When data doesn't match expected format:
1. **Try to fix**: Common transformations
   - Currency: "$1,234.56" → 1234.56
   - Dates: "Jan 1, 2024" → "2024-01-01"
   - Ratings: "4.5 out of 5" → 4.5

2. **Flag for review**: Add `"validation_errors": ["..."]`
3. **Use best effort**: Extract what you can
4. **Document the issue**: Explain what was malformed

## Output Format

```json
{
  "extraction_method": "ai|manual",
  "total_items": {{count}},
  "successful": {{count}},
  "failed": {{count}},
  "data": [
    {
      "item_id": "unique_id",
      "source_url": "https://example.com",
      "extracted_data": { /* extracted fields */ },
      "validation": {
        "is_valid": true,
        "errors": [],
        "warnings": []
      },
      "extracted_at": "ISO 8601 timestamp"
    }
  ],
  "statistics": {
    "fields_extracted": {{count}},
    "avg_completeness": "0.85",
    "missing_fields": ["field1", "field2"]
  }
}
```

## Best Practices

1. **Be Specific**: The more specific your extraction prompt, the better the results
2. **Provide Examples**: Include examples of expected output in the prompt
3. **Iterate**: Test and refine extraction prompts based on results
4. **Validate**: Always validate extracted data
5. **Handle Edge Cases**: Plan for missing, malformed, or unexpected data
6. **Document**: Keep track of what works and what doesn't
