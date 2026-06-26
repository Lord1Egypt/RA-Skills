# Switch

## Usage
```tsx
import { Switch } from '@beyondcorp/beyond-ui';
import '@beyondcorp/beyond-ui/dist/styles.css';

export function NotificationToggle() {
  const [enabled, setEnabled] = useState(true);

  return (
    <label className="flex items-center gap-2">
      <Switch checked={enabled} onCheckedChange={setEnabled} />
      <span className="text-sm">Enable notifications</span>
    </label>
  );
}
```

## Props
| Prop | Type | Description |
|------|------|-------------|
| checked | boolean | Controlled checked state |
| defaultChecked | boolean | Initial state for uncontrolled usage |
| onCheckedChange | (checked: boolean) => void | Callback fired when toggled |
| size | 'sm' | 'md' | 'lg' | Control track/thumb size (default: md) |

## Notes
- Switch is rendered as a button with `role="switch"`; supply an accessible label externally.
- Combine with labels, helper text, or tooltips to explain the toggled setting.

Story source: stories/Switch.stories.tsx
