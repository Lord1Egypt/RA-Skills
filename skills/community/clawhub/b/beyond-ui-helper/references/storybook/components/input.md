# Input

## Usage
```tsx
import { Input } from '@beyondcorp/beyond-ui';
import '@beyondcorp/beyond-ui/dist/styles.css';

export function EmailField() {
  return (
    <Input
      type="email"
      placeholder="you@example.com"
      variant="success"
      inputSize="md"
    />
  );
}
```

## Props
| Prop | Type | Description |
|------|------|-------------|
| variant | 'default' | 'success' | 'error' | Visual feedback state |
| inputSize | 'sm' | 'md' | 'lg' | Controls height and padding |

## Notes
- Fully controlled/uncontrolled; use with React Hook Form the same as a native input.
- For icon adornments, wrap the input and render icons absolutely as in storybook examples.

Story source: stories/Input.stories.tsx