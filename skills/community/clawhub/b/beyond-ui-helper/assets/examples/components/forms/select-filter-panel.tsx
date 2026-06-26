import * as React from 'react';
import { Select, Checkbox, Button, Badge } from '@beyondcorp/beyond-ui';
import '@beyondcorp/beyond-ui/dist/styles.css';

const statusOptions = [
  { label: 'All status', value: '' },
  { label: 'Active', value: 'active' },
  { label: 'Trial', value: 'trial' },
  { label: 'Churned', value: 'churned' },
];

const planOptions = [
  { label: 'Starter', value: 'starter' },
  { label: 'Growth', value: 'growth' },
  { label: 'Enterprise', value: 'enterprise' },
];

export function FiltersPanel() {
  const [status, setStatus] = React.useState('');
  const [plan, setPlan] = React.useState('growth');
  const [includePaused, setIncludePaused] = React.useState(false);
  const [tags, setTags] = React.useState(['priority', 'upsell']);

  return (
    <aside className="space-y-5 rounded-xl border border-secondary-100 bg-white p-6 shadow-sm">
      <header>
        <h2 className="text-base font-semibold text-secondary-900">Customers filters</h2>
        <p className="text-sm text-secondary-500">Narrow the dataset by status, plan, or tags.</p>
      </header>

      <div className="space-y-2">
        <label className="text-sm font-medium text-secondary-700">Status</label>
        <Select
          value={status}
          onChange={(event) => setStatus(event.target.value)}
          options={statusOptions}
        />
      </div>

      <div className="space-y-2">
        <label className="text-sm font-medium text-secondary-700">Plan</label>
        <Select
          value={plan}
          onChange={(event) => setPlan(event.target.value)}
          options={planOptions}
        />
      </div>

      <div className="flex items-start gap-3 rounded-lg bg-secondary-50 p-4">
        <Checkbox
          checked={includePaused}
          onChange={(event) => setIncludePaused(event.target.checked)}
        />
        <div>
          <p className="text-sm font-medium text-secondary-800">Include paused accounts</p>
          <p className="text-sm text-secondary-500">Show customers on temporary hold.</p>
        </div>
      </div>

      <div className="space-y-3">
        <label className="text-sm font-medium text-secondary-700">Active tags</label>
        <div className="flex flex-wrap gap-2">
          {tags.map((tag) => (
            <Badge key={tag} variant="info" className="capitalize">
              {tag}
            </Badge>
          ))}
        </div>
      </div>

      <footer className="flex items-center justify-between">
        <Button variant="ghost" onClick={() => {
          setStatus('');
          setPlan('growth');
          setIncludePaused(false);
          setTags([]);
        }}>
          Reset
        </Button>
        <Button variant="primary">Apply filters</Button>
      </footer>
    </aside>
  );
}
