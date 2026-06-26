# Checkbox

## Usage
```tsx
import { Checkbox } from '@beyondcorp/beyond-ui';
import '@beyondcorp/beyond-ui/dist/styles.css';

export function TermsCheckbox() {
  const [checked, setChecked] = useState(false);
  return (
    <label className="inline-flex items-center gap-2">
      <Checkbox checked={checked} onChange={(event) => setChecked(event.target.checked)} />
      <span className="text-sm">I agree to the terms and conditions</span>
    </label>
  );
}
```

## Props
| Prop | Type | Description |
|------|------|-------------|
| size | 'sm' | 'md' | 'lg' | Adjusts checkbox dimensions |
| checked | boolean | Controlled checked state |
| defaultChecked | boolean | Initial checked state for uncontrolled usage |

## Notes
- When `checked` is true the checkmark is rendered automatically.
- For complex layouts wrap the checkbox in a flex container so the label lines up vertically.

Story source: stories/Checkbox.stories.tsx