# Navbar

## Usage
```tsx
import { Navbar, NavItem } from '@beyondcorp/beyond-ui';
import '@beyondcorp/beyond-ui/dist/styles.css';

export function AppShellNavbar() {
  return (
    <Navbar
      logo={<span className="text-lg font-semibold">Beyond UI</span>}
      variant="default"
      size="md"
    >
      <NavItem href="#">Dashboard</NavItem>
      <NavItem href="#">Projects</NavItem>
      <NavItem href="#">Team</NavItem>
    </Navbar>
  );
}
```

## Props
| Prop | Type | Description |
|------|------|-------------|
| variant | 'default' | 'dark' | 'transparent' | Background + border style (default: default) |
| size | 'sm' | 'md' | 'lg' | Padding scales (default: md) |
| logo | ReactNode | Element rendered left-aligned before navigation items |
| className | string | Utility classes for the nav container |

## Notes
- Children (NavItem elements) render inline on desktop and collapse under a mobile toggle on smaller screens.
- Pair with badges, buttons, or avatar components in the right-aligned actions area.

Story source: stories/Navbar.stories.tsx
