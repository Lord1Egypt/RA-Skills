import {
  DashboardLayout,
  Sidebar,
  Navbar,
  Card,
  CardHeader,
  CardTitle,
  CardContent,
  Tabs,
  TabsList,
  TabsTrigger,
  TabsContent,
  Button,
  Toast,
  showToast,
  Badge,
} from '@beyondcorp/beyond-ui';
import '@beyondcorp/beyond-ui/dist/styles.css';
import { useState } from 'react';
import { Home, Users, BarChart3, Settings, Bell } from 'lucide-react';

const sidebarMenu = [
  { id: 'overview', label: 'Overview', icon: <Home className="h-4 w-4" /> },
  { id: 'customers', label: 'Customers', icon: <Users className="h-4 w-4" /> },
  { id: 'analytics', label: 'Analytics', icon: <BarChart3 className="h-4 w-4" />, badge: 'New' },
  { id: 'settings', label: 'Settings', icon: <Settings className="h-4 w-4" /> },
];

export function ShowcaseDashboard() {
  const [active, setActive] = useState('overview');
  const [tab, setTab] = useState('q1');

  return (
    <DashboardLayout
      sidebarMenuItems={sidebarMenu}
      activeSidebarItem={active}
      onSidebarItemClick={setActive}
      sidebarTitle="Beyond Dashboard"
      dashboardHeaderProps={{
        title: 'Revenue Insights',
        actions: (
          <div className="flex items-center gap-3">
            <Badge variant="info">Live</Badge>
            <Button
              variant="primary"
              onClick={() => showToast.success('Shared with Finance')}
            >
              Share report
            </Button>
          </div>
        ),
      }}
    >
      <Toast />
      <Navbar className="border-b border-secondary-100 bg-white">
        <div className="flex flex-1 items-center justify-end gap-3">
          <Button variant="ghost" size="sm" aria-label="Notifications">
            <Bell className="h-4 w-4" />
          </Button>
          <Button variant="primary" size="sm">
            New dashboard
          </Button>
        </div>
      </Navbar>

      <div className="grid gap-4 md:grid-cols-2">
        <Card>
          <CardHeader>
            <CardTitle>Quarterly breakdown</CardTitle>
          </CardHeader>
          <CardContent>
            <Tabs value={tab} onValueChange={setTab} className="w-full">
              <TabsList className="grid grid-cols-3">
                <TabsTrigger value="q1">Q1</TabsTrigger>
                <TabsTrigger value="q2">Q2</TabsTrigger>
                <TabsTrigger value="q3">Q3</TabsTrigger>
              </TabsList>
              <TabsContent value="q1" className="pt-6">
                <p className="text-sm text-secondary-500">
                  Q1 growth was driven by enterprise upgrades and LATAM expansion.
                </p>
              </TabsContent>
              <TabsContent value="q2" className="pt-6">
                <p className="text-sm text-secondary-500">
                  Q2 pipeline under review—marketing spend reduced churn by 8%.
                </p>
              </TabsContent>
              <TabsContent value="q3" className="pt-6">
                <p className="text-sm text-secondary-500">
                  Q3 projections trending 14% above baseline due to pricing changes.
                </p>
              </TabsContent>
            </Tabs>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>Highlights</CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="rounded-lg border border-secondary-200 bg-secondary-50 p-4">
              <p className="text-sm font-semibold text-secondary-800">ARR</p>
              <p className="text-2xl font-bold text-secondary-900">$1.8M</p>
              <p className="text-xs text-success-600">+12.4% vs last quarter</p>
            </div>
            <div className="rounded-lg border border-secondary-200 bg-secondary-50 p-4">
              <p className="text-sm font-semibold text-secondary-800">Net retention</p>
              <p className="text-2xl font-bold text-secondary-900">115%</p>
              <p className="text-xs text-success-600">+5 pts MoM</p>
            </div>
          </CardContent>
        </Card>
      </div>
    </DashboardLayout>
  );
}
