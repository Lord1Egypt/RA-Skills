import {
  Card,
  CardHeader,
  CardTitle,
  CardContent,
  CardDescription,
  Badge,
  Button,
  Avatar,
  AvatarImage,
  AvatarFallback,
  Tabs,
  TabsList,
  TabsTrigger,
  TabsContent,
  DataTable,
  Sidebar,
  Navbar,
  DashboardLayout,
} from '@beyondcorp/beyond-ui';
import '@beyondcorp/beyond-ui/dist/styles.css';
import { Shield, Users, LogOut, Settings, Activity, Clock } from 'lucide-react';

type Session = {
  id: number;
  location: string;
  device: string;
  seen: string;
};

const sessions: Session[] = [
  { id: 1, location: 'Nairobi, Kenya', device: 'Chrome · MacBook Pro', seen: 'Active now' },
  { id: 2, location: 'Amsterdam, NL', device: 'Safari · iPhone 15', seen: '2 hours ago' },
  { id: 3, location: 'Austin, USA', device: 'Edge · Windows', seen: 'Yesterday' },
];

const sessionColumns = [
  { key: 'location', title: 'Location', dataIndex: 'location' as const },
  { key: 'device', title: 'Device', dataIndex: 'device' as const },
  {
    key: 'seen',
    title: 'Last seen',
    dataIndex: 'seen' as const,
    render: (value: string) => (
      <div className="flex items-center gap-2 text-sm text-secondary-600">
        <Clock className="h-4 w-4 text-secondary-400" />
        {value}
      </div>
    ),
  },
];

const sidebarMenu = [
  { id: 'profile', label: 'Profile', icon: <Users className="h-4 w-4" /> },
  { id: 'security', label: 'Security', icon: <Shield className="h-4 w-4" />, badge: 'Active' },
  { id: 'sessions', label: 'Sessions', icon: <Activity className="h-4 w-4" /> },
  { id: 'settings', label: 'Settings', icon: <Settings className="h-4 w-4" /> },
];

export function AuthDashboardPage() {
  return (
    <DashboardLayout
      sidebarMenuItems={sidebarMenu}
      activeSidebarItem="security"
      sidebarTitle="Account"
      dashboardHeaderProps={{
        title: 'Account security',
        description: 'Manage password rules, multi-factor authentication, and active sessions.',
        actions: <Button variant="ghost" size="sm" icon={<LogOut className="h-4 w-4" />}>Sign out</Button>,
      }}
    >
      <Navbar className="border-b border-secondary-100 bg-white">
        <div className="flex flex-1 items-center justify-end gap-3">
          <Button variant="ghost" size="sm">
            Support
          </Button>
          <Button variant="primary" size="sm">
            Upgrade plan
          </Button>
        </div>
      </Navbar>

      <div className="grid gap-6 lg:grid-cols-3">
        <Card className="lg:col-span-2">
          <CardHeader className="flex flex-row items-center justify-between">
            <div>
              <CardTitle>Multi-factor authentication</CardTitle>
              <CardDescription>Keep your account secured with a second factor.</CardDescription>
            </div>
            <Badge variant="success">Enabled</Badge>
          </CardHeader>
          <CardContent className="space-y-4">
            <p className="text-sm text-secondary-600">
              Authenticator apps generate a one-time code to confirm it’s you. Recommended for all admins.
            </p>
            <Button variant="ghost" size="sm">
              Regenerate backup codes
            </Button>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>Account owner</CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            <Avatar size="md">
              <AvatarImage src="https://i.pravatar.cc/64?img=9" />
              <AvatarFallback>A</AvatarFallback>
            </Avatar>
            <div className="text-sm text-secondary-600">
              Avery Howard
              <br />avery@beyondcorp.com
            </div>
            <Button variant="ghost" size="sm">
              Transfer ownership
            </Button>
          </CardContent>
        </Card>
      </div>

      <Card>
        <CardHeader>
          <CardTitle>Active sessions</CardTitle>
          <CardDescription>Monitor and terminate logins from unfamiliar devices.</CardDescription>
        </CardHeader>
        <CardContent>
          <Tabs value="sessions" className="w-full">
            <TabsList className="w-full justify-start">
              <TabsTrigger value="sessions">Sessions</TabsTrigger>
              <TabsTrigger value="api">API access</TabsTrigger>
            </TabsList>
            <TabsContent value="sessions" className="pt-4">
              <DataTable
                dataSource={sessions}
                columns={sessionColumns}
                rowKey="id"
                pagination={{ current: 1, total: sessions.length, pageSize: sessions.length }}
              />
            </TabsContent>
            <TabsContent value="api" className="pt-4 text-sm text-secondary-500">
              Rotate API tokens regularly. Set expiration reminders to avoid downtime.
            </TabsContent>
          </Tabs>
        </CardContent>
      </Card>
    </DashboardLayout>
  );
}
