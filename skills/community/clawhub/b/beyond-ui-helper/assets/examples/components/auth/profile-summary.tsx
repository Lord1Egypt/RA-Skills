import { Card, CardHeader, CardTitle, CardDescription, CardContent, Button, Badge } from '@beyondcorp/beyond-ui';
import '@beyondcorp/beyond-ui/dist/styles.css';
import { Edit3, Shield, Settings2 } from 'lucide-react';

export function ProfileSummaryCard() {
  return (
    <Card className="border border-secondary-100">
      <CardHeader className="flex flex-row items-center justify-between">
        <div>
          <CardTitle className="text-lg">Account overview</CardTitle>
          <CardDescription>Manage plan, security, and billing contacts.</CardDescription>
        </div>
        <Button variant="ghost" size="sm" icon={<Edit3 className="h-4 w-4" />}
        >
          Edit profile
        </Button>
      </CardHeader>
      <CardContent className="space-y-4 text-sm text-secondary-600">
        <div className="flex items-center justify-between">
          <span className="font-medium text-secondary-700">Plan</span>
          <Badge variant="info">Pro annual</Badge>
        </div>
        <div className="flex items-center justify-between">
          <span className="font-medium text-secondary-700">MFA status</span>
          <span className="flex items-center gap-2 text-success-600">
            <Shield className="h-4 w-4" />
            Enabled
          </span>
        </div>
        <div className="flex items-center justify-between">
          <span className="font-medium text-secondary-700">Billing contact</span>
          <span>finance@beyondcorp.com</span>
        </div>
        <div className="flex items-center justify-between">
          <span className="font-medium text-secondary-700">Support tier</span>
          <span className="flex items-center gap-2">
            <Settings2 className="h-4 w-4 text-primary-600" />
            Priority (SLA 4h)
          </span>
        </div>
      </CardContent>
    </Card>
  );
}
