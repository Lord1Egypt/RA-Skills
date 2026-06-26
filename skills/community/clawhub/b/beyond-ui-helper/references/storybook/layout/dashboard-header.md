# DashboardHeader

## Usage
```tsx
import { DashboardHeader } from '@beyondcorp/beyond-ui';
import { Button } from '@beyondcorp/beyond-ui';
import '@beyondcorp/beyond-ui/dist/styles.css';

export function ReportsHeader() {
  return (
    <DashboardHeader
      breadcrumbs={[{ label: 'Home', href: '#' }, { label: 'Reports' }]}
      title="Reports Overview"
      description="Track, measure, and export key analytics."
      actions={<Button variant="primary" size="sm">Add Widget</Button>}
      showSearch
      searchPlaceholder="Search reports..."
    />
  );
}
```

## Props
| Prop | Type | Description |
|------|------|-------------|
| breadcrumbs | { label: string; href?: string }[] | Breadcrumb trail items |
| showSearch | boolean | Whether to render the search input |
| searchPlaceholder | string | Placeholder text for search input |
| onSearchChange | (value: string) => void | Search change callback |
| actions | ReactNode | Right-aligned action slot (buttons etc.) |
| title | string | Optional header title |
| description | string | Optional supporting description |
| showMenuButton | ResponsiveShow | Toggle visibility of menu button |

## Notes
- Automatically adapts to sidebar collapse; width adjusts as layout shifts.
- Use with DashboardLayout for full-page shells; breadcrumbs collapse responsively.

Story source: stories/DashboardHeader.stories.tsx
