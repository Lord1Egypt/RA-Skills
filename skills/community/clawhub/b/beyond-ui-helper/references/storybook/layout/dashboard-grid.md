# DashboardGrid

## Usage
```tsx
import { DashboardGrid } from '@beyondcorp/beyond-ui';
import { StatsCard } from '@beyondcorp/beyond-ui';
import { Card, CardHeader, CardTitle, CardContent } from '@beyondcorp/beyond-ui';
import { BarChart3 } from 'lucide-react';
import '@beyondcorp/beyond-ui/dist/styles.css';

export function WidgetGrid() {
  return (
    <DashboardGrid>
      <StatsCard
        title="Revenue"
        value="$18,500"
        trend={{ direction: 'up', value: '+2.1%', label: 'vs last week' }}
        icon={<BarChart3 className="h-6 w-6 text-primary-600" />}
      />
      <Card>
        <CardHeader>
          <CardTitle>Daily Activity</CardTitle>
        </CardHeader>
        <CardContent className="h-24 flex items-center justify-center text-gray-400">
          [Chart Placeholder]
        </CardContent>
      </Card>
      <Card>
        <CardHeader>
          <CardTitle>Notifications</CardTitle>
        </CardHeader>
        <CardContent>
          Add latest alerts, tasks, or messages here.
        </CardContent>
      </Card>
    </DashboardGrid>
  );
}
```

## Props
| Prop | Type | Description |
|------|------|-------------|
| children | ReactNode | Grid items rendered inside the dashboard grid |
| className | string | Tailwind utility classes applied to the grid container |

## Notes
- Uses CSS grid under the hood; drop any React node into each slot.
- Combine with StatsCard, Card, charts, or tables to fill analytics dashboards.

Story source: stories/DashboardGrid.stories.tsx
