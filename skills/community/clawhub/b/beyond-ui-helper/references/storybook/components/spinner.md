# Spinner

## Usage
```tsx
import { Spinner, Button } from '@beyondcorp/beyond-ui';
import '@beyondcorp/beyond-ui/dist/styles.css';

export function LoadingButton() {
  return (
    <Button variant="primary" disabled>
      <Spinner className="mr-2 h-4 w-4" /> Processing
    </Button>
  );
}
```

## Props
| Prop | Type | Description |
|------|------|-------------|
| className | string | Utility classes for size/color tweaks |

## Notes
- Combine with buttons, overlays, or status text to indicate loading states.
- Spinner inherits current text color—wrap in a container to change color.

Story source: stories/Spinner.stories.tsx
