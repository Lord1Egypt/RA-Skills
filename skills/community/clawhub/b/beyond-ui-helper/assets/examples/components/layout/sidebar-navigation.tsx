import { Sidebar, Button, Badge } from '@beyondcorp/beyond-ui';
import '@beyondcorp/beyond-ui/dist/styles.css';
import { Home, BarChart3, Users, Settings, Compass, LifeBuoy } from 'lucide-react';

const menu = [
  {
    id: 'home',
    label: 'Home',
    icon: <Home className="h-4 w-4" />,
  },
  {
    id: 'analytics',
    label: 'Analytics',
    icon: <BarChart3 className="h-4 w-4" />,
    badge: 'New',
    children: [
      { id: 'dashboards', label: 'Dashboards' },
      { id: 'experiments', label: 'Experiments' },
    ],
  },
  {
    id: 'customers',
    label: 'Customers',
    icon: <Users className="h-4 w-4" />,
  },
  {
    id: 'segmentation',
    label: 'Segmentation',
    icon: <Compass className="h-4 w-4" />,
  },
];

const footerActions = (
  <div className="flex flex-col gap-2">
    <Button variant="secondary" size="sm">
      Invite teammate
    </Button>
    <Button variant="ghost" size="sm" className="justify-start">
      <LifeBuoy className="mr-2 h-4 w-4" />
      Support
    </Button>
  </div>
);

export function AppSidebar() {
  return (
    <Sidebar
      title="Beyond Corp"
      menuItems={menu}
      activeItem="home"
      className="h-full border-r border-secondary-100"
      headerClassName="text-primary-600"
      footer={
        <div className="rounded-lg border border-secondary-100 bg-secondary-50 p-3">
          <div className="flex items-center justify-between">
            <p className="text-xs font-semibold text-secondary-700">Workspace plan</p>
            <Badge variant="info">Pro</Badge>
          </div>
          <p className="mt-2 text-xs text-secondary-500">
            Upgrade to unlock advanced analytics, SSO, and priority support.
          </p>
          <div className="mt-4">{footerActions}</div>
        </div>
      }
      sidebarFooterClassName="p-4"
    />
  );
}
