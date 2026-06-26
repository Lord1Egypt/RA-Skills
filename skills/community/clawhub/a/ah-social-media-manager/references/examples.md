# Social Media Manager — Code Examples

## Example 1

```typescript
// Social media metrics
interface SocialAnalytics {
  platform: Platform;
  period: DateRange;
  metrics: {
    reach: number;
    impressions: number;
    engagement: number;
    engagementRate: number;
    followers: {
      gained: number;
      lost: number;
      net: number;
    };
    topPosts: Post[];
    bestTimes: TimeSlot[];
    audienceGrowth: number; // percentage
  };
}

// ROI calculation
function calculateSocialROI(
  spend: number,
  conversions: number,
  avgOrderValue: number
): ROIMetrics {
  const revenue = conversions * avgOrderValue;
  const roi = ((revenue - spend) / spend) * 100;
  const costPerConversion = spend / conversions;

  return { roi, revenue, costPerConversion };
}

// Competitive analysis
interface CompetitorAnalysis {
  competitor: string;
  platforms: Platform[];
  postingFrequency: number;
  avgEngagement: number;
  topContentTypes: string[];
  hashtagStrategy: string[];
  growthRate: number;
}
```
