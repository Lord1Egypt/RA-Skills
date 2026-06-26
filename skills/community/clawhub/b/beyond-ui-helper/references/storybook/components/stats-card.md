# StatsCard

## Usage
```tsx
import { StatsCard } from '@beyondcorp/beyond-ui';
import '@beyondcorp/beyond-ui/dist/styles.css';
import { BarChart3 } from 'lucide-react';

export function MetricsGrid() {
  return (
    <div className="grid gap-4 md:grid-cols-2">
      <StatsCard
        title="Total Users"
        value="2,543"
        trend={{ direction: 'up', value: '+12%', label: 'from last month' }}
        icon={<BarChart3 className="h-6 w-6 text-primary-600" />}
      />
      <StatsCard
        variant="gradient"
        color="success"
        title="Monthly Revenue"
        value="$45,231"
        trend={{ direction: 'up', value: '+8.2%', label: 'from last month' }}
        icon={<BarChart3 className="h-6 w-6" />}
      />
    </div>
  );
}
```

## Props
| Prop | Type | Description |
|------|------|-------------|
| title | string | Label displayed above the metric |
| value | string | number | Main metric value |
| trend | { direction: 'up' | 'down' | 'neutral'; value: string | number; label?: string } | Trend metadata (icon + text) |
| icon | ReactNode | Optional icon rendered in the corner |
| variant | 'default' | 'gradient' | Background style (default: default) |
| color | 'primary' | 'secondary' | 'success' | 'warning' | 'danger' | Color palette used when variant="gradient" |

## Notes
- Trend icons adjust color based on direction; neutral uses a minus icon.
- Gradient variant applies a background gradient with white text—great for highlight cards.

Story source: stories/StatsCard.stories.tsx
