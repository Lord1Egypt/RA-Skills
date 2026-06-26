import * as React from 'react';
import { RadioGroup, Switch, Button } from '@beyondcorp/beyond-ui';
import '@beyondcorp/beyond-ui/dist/styles.css';

const notificationOptions = [
  { label: 'All activity', value: 'all' },
  { label: 'Mentions only', value: 'mentions' },
  { label: 'Direct messages', value: 'dm' },
  { label: 'None', value: 'none' },
];

export function NotificationPreferencesCard() {
  const [frequency, setFrequency] = React.useState('mentions');
  const [digest, setDigest] = React.useState(true);

  return (
    <section className="space-y-6 rounded-2xl border border-secondary-100 bg-white p-6 shadow">
      <header className="space-y-1">
        <h2 className="text-lg font-semibold text-secondary-900">Notification settings</h2>
        <p className="text-sm text-secondary-500">
          Choose when we notify you about new updates and conversations.
        </p>
      </header>

      <div className="space-y-4">
        <p className="text-sm font-medium text-secondary-700">Delivery frequency</p>
        <RadioGroup
          name="notification-frequency"
          value={frequency}
          onChange={(event) => setFrequency(event.target.value)}
          options={notificationOptions}
        />
      </div>

      <div className="flex items-center justify-between rounded-xl bg-secondary-50 p-4">
        <div>
          <p className="text-sm font-semibold text-secondary-800">Weekly summary</p>
          <p className="text-xs text-secondary-500">
            Receive a single digest with highlights from the week.
          </p>
        </div>
        <Switch
          checked={digest}
          onCheckedChange={(checked) => setDigest(Boolean(checked))}
        />
      </div>

      <footer className="flex items-center justify-end gap-3">
        <Button variant="ghost">Cancel</Button>
        <Button variant="primary">Save preferences</Button>
      </footer>
    </section>
  );
}
