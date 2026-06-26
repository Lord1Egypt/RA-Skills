# NightModeSwitch

## Usage
```tsx
import { NightModeSwitch } from '@beyondcorp/beyond-ui';
import '@beyondcorp/beyond-ui/dist/styles.css';

export function ThemeToggle() {
  return (
    <NightModeSwitch
      variant="ghost"
      size="md"
      iconStyle="filled"
      ariaLabel="Toggle dark mode"
    />
  );
}
```

## Props
| Prop | Type | Description |
|------|------|-------------|
| variant | 'primary' | 'secondary' | 'ghost' | Button styling variants (default: ghost) |
| size | 'sm' | 'md' | 'lg' | Control button dimensions (default: md) |
| iconStyle | 'filled' | 'outline' | Icon look for sun/moon glyphs (default: filled) |
| ariaLabel | string | Accessible label for the switch |

## Notes
- Tied to the `useDarkMode` hook; adding the switch toggles document theme classes.
- Pass `className` to place it in toolbars or navbars without extra wrappers.

Story source: stories/NightModeSwitch.stories.tsx
