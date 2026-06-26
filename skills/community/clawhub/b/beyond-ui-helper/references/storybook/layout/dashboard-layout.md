# DashboardLayout

## Usage
```tsx
import { DashboardLayout } from '@beyondcorp/beyond-ui';
import '@beyondcorp/beyond-ui/dist/styles.css';
import { StatsCard } from '@beyondcorp/beyond-ui';
import { Card, CardHeader, CardTitle, CardContent } from '@beyondcorp/beyond-ui';
import { Home, BarChart3 } from 'lucide-react';

const menuItems = [
  { id: 'dashboard', label: 'Dashboard', icon: <Home className="h-5 w-5" /> },
  { id: 'analytics', label: 'Analytics', icon: <BarChart3 className="h-5 w-5" />, badge: 'New' },
];

export function AnalyticsShell() {
  const [active, setActive] = useState('analytics');
  return (
    <DashboardLayout
      sidebarMenuItems={menuItems}
      activeSidebarItem={active}
      onSidebarItemClick={setActive}
      breadcrumbs={[{ label: 'Home', href: '#' }, { label: 'Analytics' }]}
    >
      <div className="grid gap-6 md:grid-cols-2">
        <StatsCard title="Revenue" value="$18,500" trend={{ direction: 'up', value: '+2.1%' }} />
        <StatsCard title="Users" value="1,230" trend={{ direction: 'up', value: '+1.5%' }} />
      </div>
      <Card className="mt-6">
        <CardHeader>
          <CardTitle>Daily Active Users</CardTitle>
        </CardHeader>
        <CardContent className="h-32 flex items-center justify-center text-gray-400">
          [Chart Placeholder]
        </CardContent>
      </Card>
    </DashboardLayout>
  );
}
```

## Props
| Prop | Type | Description |
|------|------|-------------|
| sidebarMenuItems | MenuItem[] | Items rendered in the sidebar |
| activeSidebarItem | string | ID of the active sidebar entry |
| onSidebarItemClick | (id: string) => void | Callback when a menu item is clicked |
| breadcrumbs | BreadcrumbItem[] | Data passed to DashboardHeader |
| showSearch | boolean | Displays header search control |
| onSearchChange | (value: string) => void | Search input handler |
| dashboardHeaderProps | DashboardHeaderProps | Additional header customization |
| sidebarTitle / sidebarTitleLetter | string | Branding text shown in the sidebar header |

## Notes
- Sidebar collapse is controlled internally via the hamburger icon.
- Content scrolls independently of sidebar/header; wrap sections with padding for spacing.
- Combine with StatsCard, Table, and Card components for dashboards.

Story source: stories/DashboardLayout.stories.tsx
