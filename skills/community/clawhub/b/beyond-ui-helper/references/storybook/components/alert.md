# Alert

## Usage
```tsx
import { Alert, AlertTitle, AlertDescription } from '@beyondcorp/beyond-ui';
import '@beyondcorp/beyond-ui/dist/styles.css';

export function FormErrorAlert() {
  return (
    <Alert variant="danger" className="max-w-md">
      <AlertTitle>Submission failed</AlertTitle>
      <AlertDescription>
        Please fix the highlighted fields and try again.
      </AlertDescription>
    </Alert>
  );
}
```

## Props
| Prop | Type | Description |
|------|------|-------------|
| variant | 'default' | 'success' | 'warning' | 'danger' | 'info' | Semantic color scheme for the container |
| className | string | Utility classes added to the root alert wrapper |

## Notes
- Alert provides `AlertTitle` and `AlertDescription` helpers for consistent spacing.
- Content is flexible—insert buttons, links, or lists inside the description block.

Story source: stories/Alert.stories.tsx