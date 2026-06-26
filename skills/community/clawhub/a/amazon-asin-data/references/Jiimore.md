# Jiimore API Reference

Complete API documentation for the Jiimore Amazon Niche Market Analysis tool.

## Endpoint

```
POST https://test-tool-gateway.linkfox.com/jiimore/getNicheInfoByKeyword
```

## Authentication

Include API key in request headers:

```http
Authorization: {LINKFOXAGENT_API_KEY}
Content-Type: application/json
```

## Request Parameters

### Required Parameters

#### `keyword`
- **Type**: `string`
- **Required**: Yes
- **Max Length**: 1000
- **Description**: Search keyword for niche market. Translate to target country language when appropriate.
- **Example**: `"bluetooth charger"`, `"コーヒーグラインダー"`, `"Kabellose Kopfhörer"`

### Common Parameters

#### `countryCode`
- **Type**: `string`
- **Default**: `"US"`
- **Pattern**: `^(US|JP|DE)$`
- **Options**:
  - `US` - United States
  - `JP` - Japan
  - `DE` - Germany

#### `page`
- **Type**: `integer`
- **Default**: `1`
- **Minimum**: `1`
- **Description**: Page number for pagination (1-indexed)

#### `pageSize`
- **Type**: `integer`
- **Default**: `50`
- **Minimum**: `10`
- **Maximum**: `100`
- **Description**: Number of results per page

#### `sortType`
- **Type**: `string`
- **Default**: `"desc"`
- **Pattern**: `^(desc|asc)$`
- **Options**:
  - `desc` - Descending order
  - `asc` - Ascending order

#### `sortField`
- **Type**: `string`
- **Default**: `"unitsSoldT7"`
- **Description**: Field to sort results by
- **Options**:
  - `clickConversionRateT7` - 7-day click conversion rate
  - `demand` - Demand score
  - `avgPrice` - Average price
  - `maximumPrice` - Maximum price
  - `minimumPrice` - Minimum price
  - `productCount` - Product count
  - `searchConversionRateT7` - 7-day search conversion rate
  - `searchVolumeT7` - 7-day search volume
  - `unitsSoldT7` - 7-day sales volume (default)
  - `searchVolumeGrowthT7` - 7-day search growth rate
  - `clickCountT90` - 90-day click count
  - `clickCountT7` - 7-day click count
  - `brandCount` - Brand count
  - `top5BrandsClickShare` - TOP5 brand click share
  - `newProductsLaunchedT180` - 180-day new products launched
  - `successfulLaunchesT180` - 180-day successful launches
  - `launchRateT180` - 180-day launch success rate
  - `top5ProductsClickShare` - TOP5 product click share
  - `returnRateT360` - Annual return rate
  - `clickConversionRateT90` - 90-day click conversion rate
  - `searchConversionRateT90` - 90-day search conversion rate
  - `searchVolumeT90` - 90-day search volume
  - `unitsSoldT90` - 90-day sales volume
  - `unitsSoldGrowthT90` - 90-day sales growth rate
  - `searchVolumeGrowthT90` - 90-day search growth rate
  - `acos` - Advertising Cost of Sales
  - `profitRate50` - 50% natural order profit rate

### Optional Filter Parameters

#### Product & Price Filters

**`productCountMin` / `productCountMax`**
- **Type**: `integer`
- **Description**: Filter by product count range
- **Use Case**: Find niches with specific competition levels

**`avgPriceMin` / `avgPriceMax`**
- **Type**: `number`
- **Description**: Filter by average price range (in local currency)
- **Use Case**: Target specific price segments

**`cpcMediumMin` / `cpcMediumMax`**
- **Type**: `number`
- **Description**: Filter by median CPC (Cost Per Click) range
- **Use Case**: Evaluate advertising costs

#### Brand Filters

**`brandCountMin` / `brandCountMax`**
- **Type**: `integer`
- **Description**: Filter by brand count range
- **Use Case**: Find niches with low/high brand competition

**`avgBrandAgeMin` / `avgBrandAgeMax`**
- **Type**: `number`
- **Description**: Filter by current average brand age (years)
- **Use Case**: Target established or emerging markets

**`avgBrandAgeQoqMin` / `avgBrandAgeQoqMax`**
- **Type**: `number`
- **Description**: Filter by 90-day average brand age
- **Use Case**: Track brand maturity trends

**`avgBrandAgeYoyMin` / `avgBrandAgeYoyMax`**
- **Type**: `number`
- **Description**: Filter by 360-day average brand age
- **Use Case**: Annual brand maturity analysis

#### Seller Filters

**`avgSellingPartnerAgeMin` / `avgSellingPartnerAgeMax`**
- **Type**: `number`
- **Description**: Filter by current average seller age

**`avgSellingPartnerAgeQoqMin` / `avgSellingPartnerAgeQoqMax`**
- **Type**: `number`
- **Description**: Filter by 90-day average seller age

**`avgSellingPartnerAgeYoyMin` / `avgSellingPartnerAgeYoyMax`**
- **Type**: `number`
- **Description**: Filter by 360-day average seller age

#### Traffic & Sales Filters

**`unitsSoldT7Min` / `unitsSoldT7Max`**
- **Type**: `integer`
- **Description**: Filter by 7-day sales volume range
- **Use Case**: Target niches with specific sales levels

**`searchVolumeT7Min` / `searchVolumeT7Max`**
- **Type**: `integer`
- **Description**: Filter by 7-day search volume range
- **Use Case**: Find high-traffic niches

**`clickCountT7Min` / `clickCountT7Max`**
- **Type**: `integer`
- **Description**: Filter by 7-day click count range

**`clickConversionRateT7Min` / `clickConversionRateT7Max`**
- **Type**: `number` (0-1 range, represents percentage)
- **Description**: Filter by 7-day click conversion rate
- **Example**: `0.1` = 10% conversion rate
- **Use Case**: Find high-converting niches

**`top5BrandsClickShareMin` / `top5BrandsClickShareMax`**
- **Type**: `number` (0-1 range)
- **Description**: Filter by TOP5 brand click share
- **Example**: `0.3` = 30% market share
- **Use Case**: Avoid dominated markets (set max <0.3 for low concentration)

**`top5ProductsClickShareMin` / `top5ProductsClickShareMax`**
- **Type**: `number` (0-1 range)
- **Description**: Filter by TOP5 product click share
- **Use Case**: Find less concentrated product markets

#### Conversion & Risk Filters

**`launchRateT180Min` / `launchRateT180Max`**
- **Type**: `number` (0-1 range)
- **Description**: Filter by 180-day product launch success rate
- **Example**: `0.2` = 20% success rate
- **Use Case**: Assess market entry difficulty

**`returnRateT360Min` / `returnRateT360Max`**
- **Type**: `number` (0-1 range)
- **Description**: Filter by annual return rate
- **Example**: `0.1` = 10% return rate
- **Use Case**: Avoid high-return niches (set max <0.1 for quality products)

**`sponsoredProductsPercentageMin` / `sponsoredProductsPercentageMax`**
- **Type**: `number` (0-1 range)
- **Description**: Filter by percentage of sponsored products
- **Use Case**: Evaluate advertising saturation

**`newProductRateT180`**
- **Type**: `number` (0-1 range)
- **Description**: Minimum ratio of new products (180-day window)
- **Use Case**: Find markets with product innovation

## Response Structure

### Top-Level Fields

```json
{
  "total": 1234,
  "data": [...],
  "columns": [...],
  "costToken": 456,
  "type": "table",
  "title": "Niche Market Information"
}
```

- `total`: Total number of matching niches
- `data`: Array of niche market objects
- `columns`: Display column configuration
- `costToken`: API token cost (internal metric)
- `type`: Response format type
- `title`: Response title

### Data Object Fields

Each object in the `data` array contains:

#### Identification
- `nicheTitle` (string): Niche market title (English)
- `translationZh` (string): Chinese translation of title
- `nicheId` (string): Unique niche identifier

#### Market Metrics
- `demand` (number): Market demand score (0-100)
- `productCount` (integer): Total number of products
- `brandCount` (integer): Number of brands
- `categorieList` (array): Product category list

#### Pricing
- `avgPrice` (number): Average product price
- `minimumPrice` (number): Lowest price
- `maximumPrice` (number): Highest price
- `profitMarginGt50PctSkuRatio` (number, 0-1): Ratio of products with >50% profit margin
- `breakEvenRatio` (number, 0-1): Break-even ratio

#### Sales (Weekly - T7)
- `unitsSoldWeekly` (integer): 7-day sales volume
- `searchVolumeWeekly` (integer): 7-day search volume
- `searchVolumeGrowthWeekly` (number, 0-1): 7-day search growth rate
- `clickCountWeekly` (integer): 7-day click count

#### Sales (Quarterly - T90)
- `unitsSoldQuarterly` (integer): 90-day sales volume
- `searchVolumeQuarterly` (integer): 90-day search volume
- `searchVolumeGrowthQuarterly` (number, 0-1): 90-day search growth rate
- `clickCountQuarterly` (integer): 90-day click count

#### Conversion Metrics
- `searchConversionRateWeekly` (number, 0-1): 7-day search-to-sale conversion
- `searchConversionRateQuarterly` (number, 0-1): 90-day search-to-sale conversion
- `clickToSaleConversionWeekly` (number, 0-1): 7-day click-to-sale conversion
- `clickConversionRateQuarterly` (number, 0-1): 90-day click-to-sale conversion

#### Competition
- `top5BrandsClickShare` (number, 0-1): TOP5 brand market share
- `top5ProductsClickShare` (number, 0-1): TOP5 product market share
- `avgBrandAgeNow` (number): Current average brand age (years)
- `avgBrandAgeQuarterly` (number): 90-day average brand age

#### Product Lifecycle
- `launchRateSemiannual` (number, 0-1): 180-day launch success rate
- `newProductsLaunchedSemiannual` (integer): New products launched (180 days)
- `successfulLaunchedSemiannual` (integer): Successful launches (180 days)
- `returnRateAnnual` (number, 0-1): Annual return rate

#### Advertising
- `acos` (number, 0-1): Advertising Cost of Sales
- `cpc` (object): CPC metrics
  - `low` (number): Low CPC value
  - `medium` (number): Median CPC value
  - `high` (number): High CPC value

#### Visual
- `referenceAsinImageUrl` (string): Representative product image URL

## Example Requests

### Basic Search
```json
{
  "keyword": "wireless earbuds",
  "countryCode": "US"
}
```

### Low Competition Search
```json
{
  "keyword": "yoga mat",
  "countryCode": "US",
  "brandCountMax": 30,
  "top5BrandsClickShareMax": 0.3,
  "sortField": "demand",
  "sortType": "desc"
}
```

### Price Range Search
```json
{
  "keyword": "kitchen knife",
  "countryCode": "DE",
  "avgPriceMin": 20,
  "avgPriceMax": 50,
  "returnRateT360Max": 0.1,
  "pageSize": 100
}
```

### High Volume, Low Competition
```json
{
  "keyword": "desk lamp",
  "countryCode": "JP",
  "unitsSoldT7Min": 1000,
  "productCountMax": 100,
  "top5ProductsClickShareMax": 0.4,
  "sortField": "unitsSoldT7",
  "sortType": "desc"
}
```

## Response Example

```json
{
  "total": 145,
  "data": [
    {
      "nicheId": "123456",
      "nicheTitle": "bluetooth wireless charger cable",
      "translationZh": "蓝牙无线充电线",
      "demand": 78,
      "avgPrice": 23.9,
      "minimumPrice": 9.99,
      "maximumPrice": 39.99,
      "productCount": 320,
      "brandCount": 44,
      "unitsSoldWeekly": 5400,
      "unitsSoldQuarterly": 18000,
      "searchVolumeWeekly": 12000,
      "searchVolumeQuarterly": 36000,
      "searchVolumeGrowthWeekly": 0.05,
      "searchVolumeGrowthQuarterly": 0.14,
      "clickCountWeekly": 8600,
      "clickCountQuarterly": 24000,
      "clickToSaleConversionWeekly": 0.08,
      "searchConversionRateWeekly": 0.09,
      "searchConversionRateQuarterly": 0.12,
      "clickConversionRateQuarterly": 0.1,
      "top5BrandsClickShare": 0.28,
      "top5ProductsClickShare": 0.22,
      "profitMarginGt50PctSkuRatio": 0.31,
      "returnRateAnnual": 0.07,
      "acos": 0.23,
      "breakEvenRatio": 0.41,
      "launchRateSemiannual": 0.3,
      "newProductsLaunchedSemiannual": 40,
      "successfulLaunchedSemiannual": 12,
      "avgBrandAgeNow": 2.2,
      "avgBrandAgeQuarterly": 2.5,
      "cpc": {
        "low": 0.8,
        "medium": 1.4,
        "high": 2.3
      },
      "referenceAsinImageUrl": "https://example.com/image.jpg",
      "categorieList": []
    }
  ],
  "columns": [],
  "costToken": 123,
  "type": "table",
  "title": "Niche Market Information"
}
```

## Error Responses

### Authentication Error
```json
{
  "error": "Unauthorized",
  "message": "Invalid or missing API key"
}
```

### Validation Error
```json
{
  "error": "Validation Failed",
  "message": "countryCode must be one of: US, JP, DE"
}
```

### Rate Limit Error
```json
{
  "error": "Rate Limit Exceeded",
  "message": "Too many requests, please try again later"
}
```

## Best Practices

### Query Optimization
1. Start with broad searches (keyword + country only)
2. Analyze top results to understand market patterns
3. Apply 2-3 relevant filters to narrow down
4. Use pagination for comprehensive market coverage

### Performance Tips
- Larger `pageSize` (50-100) reduces API calls
- Cache results for repeated analysis
- Use specific filters to reduce processing time
- Background processing recommended for complex queries

### Data Interpretation
- Values in 0-1 range represent percentages (multiply by 100)
- Weekly (T7) data shows recent trends
- Quarterly (T90) data shows stable patterns
- Compare both timeframes for trend analysis

### Common Patterns

**Find Emerging Opportunities**
```json
{
  "searchVolumeGrowthT7Min": 0.1,
  "productCountMax": 100,
  "launchRateT180Min": 0.2,
  "sortField": "demand"
}
```

**Avoid Saturated Markets**
```json
{
  "top5BrandsClickShareMax": 0.3,
  "top5ProductsClickShareMax": 0.3,
  "returnRateT360Max": 0.1
}
```

**Target Profitable Niches**
```json
{
  "profitRate50Min": 0.3,
  "acosMax": 0.25,
  "searchConversionRateT7Min": 0.08
}
```

## Limitations

- Maximum keyword length: 1000 characters
- Supported countries: US, JP, DE only
- Page size range: 10-100 results
- Background processing typical: 1-5 minutes
- API rate limits apply based on subscription tier

## Troubleshooting

**No Results Returned**
- Verify keyword spelling and relevance
- Relax filter constraints
- Try alternative keywords or synonyms
- Check country code validity

**Slow Response Times**
- Use background processing for large queries
- Reduce `pageSize` if needed
- Check API status and rate limits

**Unexpected Values**
- Verify decimal vs percentage interpretation (0-1 range)
- Check currency for price fields (local market currency)
- Confirm time period (T7 = weekly, T90 = quarterly, etc.)
