# Button

## Usage
```tsx
import { Button } from '@beyondcorp/beyond-ui';
import '@beyondcorp/beyond-ui/dist/styles.css';

export function ToolbarActions() {
  return (
    <div className="flex items-center gap-2">
      <Button variant="primary">Save</Button>
      <Button variant="secondary">Cancel</Button>
      <Button variant="danger">Delete</Button>
      <Button variant="ghost">More</Button>
    </div>
  );
}
```

## Props
| Prop | Type | Description |
|------|------|-------------|
| variant | 'primary' · 'secondary' · 'danger' · 'success' · 'warning' · 'outline' · 'ghost' · 'link' | Visual style (defaults to primary) |
| size | 'sm' · 'md' · 'lg' · 'xl' | Control height and padding |
| asChild | boolean | Render as `<Slot />` to wrap another element |
| className | string | Tailwind utilities appended to the button |

## Notes
- Based on `class-variance-authority`—extend palettes by overriding Tailwind semantic tokens.
- `asChild` lets you transform any element (e.g. `<Link>`) into a styled button while preserving semantics.
- Disabled buttons automatically reduce opacity and block pointer events.

Story source: stories/Button.stories.tsx
