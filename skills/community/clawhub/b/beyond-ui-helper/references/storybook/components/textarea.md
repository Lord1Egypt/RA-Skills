# Textarea

## Usage
```tsx
import { Textarea } from '@beyondcorp/beyond-ui';
import '@beyondcorp/beyond-ui/dist/styles.css';

export function CommentBox() {
  const [value, setValue] = useState('');
  const maxLength = 240;

  return (
    <div className="space-y-2 w-full max-w-md">
      <Textarea
        value={value}
        onChange={(event) => setValue(event.target.value)}
        placeholder="Write a comment..."
        maxLength={maxLength}
      />
      <div className="text-xs text-gray-400 text-right">{value.length}/{maxLength}</div>
    </div>
  );
}
```

## Props
| Prop | Type | Description |
|------|------|-------------|
| variant | 'default' | 'success' | 'error' | Visual state (default: default) |
| className | string | Additional Tailwind classes |

## Notes
- Inherits all native `<textarea>` props (rows, maxLength, onChange, etc.).
- Apply variants for validation states in forms (success/error).

Story source: stories/Textarea.stories.tsx
