# Card

## Usage
```tsx
import { Card, CardHeader, CardTitle, CardContent, CardFooter } from '@beyondcorp/beyond-ui';
import '@beyondcorp/beyond-ui/dist/styles.css';

export function MetricsCard() {
  return (
    <Card className="max-w-sm">
      <CardHeader>
        <CardTitle>Monthly revenue</CardTitle>
      </CardHeader>
      <CardContent>
        <p className="text-3xl font-semibold">$84,500</p>
        <p className="text-sm text-secondary-500">+12.4% vs last month</p>
      </CardContent>
      <CardFooter className="text-xs text-secondary-400">Updated 5 minutes ago</CardFooter>
    </Card>
  );
}
```

## Props
| Prop | Type | Description |
|------|------|-------------|
| className | string | Utility classes to adjust borders, spacing, etc. |

## Notes
- Combine Card subcomponents (`CardHeader`, `CardContent`, `CardFooter`) for consistent structure.
- Pair with `CardDescription` to render supporting text under titles.

Story source: stories/Card.stories.tsx