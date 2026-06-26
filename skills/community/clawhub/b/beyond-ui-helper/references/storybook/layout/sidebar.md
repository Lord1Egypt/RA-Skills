# Sidebar

## Usage
```tsx
import { Sidebar } from '@beyondcorp/beyond-ui';
import { Home, BarChart3, Users, Settings } from 'lucide-react';
import '@beyondcorp/beyond-ui/dist/styles.css';

const menuItems = [
  { id: 'dashboard', label: 'Dashboard', icon: <Home className="h-5 w-5" /> },
  { id: 'analytics', label: 'Analytics', icon: <BarChart3 className="h-5 w-5" />, badge: 'New' },
  {
    id: 'users',
    label: 'Users',
    icon: <Users className="h-5 w-5" />,
    children: [
      { id: 'all-users', label: 'All Users', href: '#' },
      { id: 'roles', label: 'Roles', icon: <Settings className="h-4 w-4" />, href: '#' },
    ],
  },
];

export function AdminSidebar() {
  const [active, setActive] = useState('dashboard');

  return (
    <Sidebar
      menuItems={menuItems}
      activeItem={active}
      onItemClick={setActive}
      title="Admin Panel"
      titleLetter="A"
      collapsed={false}
    />
  );
}
```

## Props
| Prop | Type | Description |
|------|------|-------------|
| menuItems | MenuItem[] | Top-level items rendered in the sidebar |
| activeItem | string | Track the current active entry |
| onItemClick | (id: string) => void | Callback when menu item is selected |
| collapsed | boolean | Controls collapsed state (width toggles between 4rem/18rem) |
| title | string | Header title text |
| titleLetter | string | Letter displayed in header badge |
| headerClassName | string | Extra classes for header area |
| profileButtonProps / logoutButtonProps | Profile and logout button overrides |
| profileSectionProps | Sidebar profile section content |

## Notes
- Perfect companion for `DashboardLayout`; the layout manages collapse toggles automatically.
- Nested children render secondary navigation groups with icons/badges.
- Inline style widths (4rem/18rem) match DashboardLayout defaults—keep them aligned when customizing.

Story source: stories/Sidebar.stories.tsx
