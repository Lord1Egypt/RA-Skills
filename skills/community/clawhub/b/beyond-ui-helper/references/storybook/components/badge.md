# Badge

## Usage
```tsx
import { Badge } from '@beyondcorp/beyond-ui';
import '@beyondcorp/beyond-ui/dist/styles.css';

export function StatusBadges() {
  return (
    <div className="flex gap-2">
      <Badge>Default</Badge>
      <Badge variant="success">Success</Badge>
      <Badge variant="danger">Alert</Badge>
      <Badge variant="outline">Draft</Badge>
    </div>
  );
}
```

## Props
| Prop | Type | Description |
|------|------|-------------|
| variant | 'default' | 'secondary' | 'success' | 'danger' | 'warning' | 'outline' | Color/style variant (default: default) |
| className | string | Utility classes to adjust spacing and appearance |

## Notes
- Badges are inline-flex with rounded styling; place near labels or counters.
- Combine with icons or numbers to represent statuses, counts, or tags.

Story source: stories/Badge.stories.tsx
