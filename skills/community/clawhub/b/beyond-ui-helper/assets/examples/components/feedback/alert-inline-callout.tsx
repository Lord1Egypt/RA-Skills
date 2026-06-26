import { Alert, AlertTitle, AlertDescription, Button } from '@beyondcorp/beyond-ui';
import '@beyondcorp/beyond-ui/dist/styles.css';
import { ShieldAlert } from 'lucide-react';

export function BillingAlert() {
  return (
    <Alert variant="warning" className="max-w-xl border border-warning-300 bg-warning-50">
      <ShieldAlert className="h-5 w-5 text-warning-600" />
      <AlertTitle>Payment required</AlertTitle>
      <AlertDescription>
        Your card ending in 4242 failed twice. Update billing to avoid service interruption.
      </AlertDescription>
      <div className="mt-4 flex items-center gap-2">
        <Button size="sm" variant="primary">Update payment</Button>
        <Button size="sm" variant="ghost">Skip for now</Button>
      </div>
    </Alert>
  );
}
