import {
  DashboardLayout,
  Navbar,
  Sidebar,
  Button,
  Badge,
  Card,
  CardHeader,
  CardTitle,
  CardContent,
  StatsCard,
  DataTable,
  Tabs,
  TabsList,
  TabsTrigger,
  TabsContent,
  Toast,
  showToast,
} from '@beyondcorp/beyond-ui';
import '@beyondcorp/beyond-ui/dist/styles.css';
import { useState } from 'react';
import { Home, Users, BarChart3, Layers, Settings } from 'lucide-react';

type MetricRow = {
  feature: string;
  status: 'released' | 'in-progress' | 'blocked';
  owner: string;
  eta: string;
};

const roadmap: MetricRow[] = [
  { feature: 'Usage-based billing', status: 'released', owner: 'Priya N.', eta: 'Now' },
  { feature: 'Teams access control', status: 'in-progress', owner: 'Caleb W.', eta: 'Apr 22' },
  { feature: 'Realtime alerts', status: 'blocked', owner: 'Diego M.', eta: 'TBD' },
];

const roadmapColumns = [
  {
    key: 'feature',
    title: 'Feature',
    dataIndex: 'feature' as const,
  },
  {
    key: 'status',
    title: 'Status',
    dataIndex: 'status' as const,
    render: (status: MetricRow['status']) => (
      <Badge variant={status === 'released' ? 'success' : status === 'blocked' ? 'danger' : 'warning'}>
        {status}
      </Badge>
    ),
  },
  {
    key: 'owner',
    title: 'Owner',
    dataIndex: 'owner' as const,
  },
  {
    key: 'eta',
    title: 'ETA',
    dataIndex: 'eta' as const,
  },
];

const menuItems = [
  { id: 'overview', label: 'Overview', icon: <Home className="h-4 w-4" /> },
  { id: 'customers', label: 'Customers', icon: <Users className="h-4 w-4" /> },
  { id: 'analytics', label: 'Analytics', icon: <BarChart3 className="h-4 w-4" /> },
  { id: 'platform', label: 'Platform', icon: <Layers className="h-4 w-4" />, badge: 'New' },
  { id: 'settings', label: 'Settings', icon: <Settings className="h-4 w-4" /> },
];

export function ProductDashboardPage() {
  const [active, setActive] = useState('overview');
  const [tab, setTab] = useState('usage');

  return (
    <DashboardLayout
      sidebarMenuItems={menuItems}
      activeSidebarItem={active}
      onSidebarItemClick={setActive}
      sidebarTitle="Beyond UI"
      dashboardHeaderProps={{
        title: 'Product performance',
        description: 'Monitor adoption, churn, and roadmap momentum.',
        actions: (
          <div className="flex items-center gap-3">
            <Button variant="ghost" size="sm">
              Export CSV
            </Button>
            <Button variant="primary" size="sm" onClick={() => showToast.success('Report shared')}>
              Share report
            </Button>
          </div>
        ),
      }}
    >
      <Toast />

      <Navbar className="mb-6 border-b border-secondary-100 bg-white">
        <div className="flex flex-1 items-center justify-end gap-3">
          <Button variant="ghost" size="sm">
            Feedback
          </Button>
          <Button variant="primary" size="sm">
            Create view
          </Button>
        </div>
      </Navbar>

      <div className="grid gap-4 md:grid-cols-3">
        <StatsCard title="Active workspaces" value="1,024" trendValue="8%" trendLabel="vs last 30 days" />
        <StatsCard title="Deployment frequency" value="35 / week" trendValue="+12%" trendLabel="CI pipeline" />
        <StatsCard title="Availability" value="99.98%" trendValue="0.01%" trendLabel="last 90 days" />
      </div>

      <Card className="mt-6">
        <CardHeader>
          <CardTitle>Usage insights</CardTitle>
        </CardHeader>
        <CardContent>
          <Tabs value={tab} onValueChange={setTab} className="w-full">
            <TabsList className="w-full justify-start">
              <TabsTrigger value="usage">Usage</TabsTrigger>
              <TabsTrigger value="retention">Retention</TabsTrigger>
              <TabsTrigger value="roadmap">Roadmap</TabsTrigger>
            </TabsList>
            <TabsContent value="usage" className="pt-6 text-sm text-secondary-600">
              Daily active seats grew to 4,012 (+14% MoM). API requests peaked Tuesday and Thursday.
            </TabsContent>
            <TabsContent value="retention" className="pt-6 text-sm text-secondary-600">
              Net retention 118%. Expansion driven by Enterprise tier upgrades.
            </TabsContent>
            <TabsContent value="roadmap" className="pt-6">
              <DataTable<MetricRow>
                columns={roadmapColumns}
                dataSource={roadmap}
                rowKey="feature"
                pagination={{ current: 1, total: roadmap.length, pageSize: 3 }}
              />
            </TabsContent>
          </Tabs>
        </CardContent>
      </Card>
    </DashboardLayout>
  );
}
