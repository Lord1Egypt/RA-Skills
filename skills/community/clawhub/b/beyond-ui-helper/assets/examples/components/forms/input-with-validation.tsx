import * as React from 'react';
import { Input, Textarea, Checkbox, RadioGroup, Select, Switch, Button } from '@beyondcorp/beyond-ui';
import '@beyondcorp/beyond-ui/dist/styles.css';

const roleOptions = [
  { label: 'Designer', value: 'designer' },
  { label: 'Engineer', value: 'engineer' },
  { label: 'Product Manager', value: 'pm' },
];

const planOptions = [
  { label: 'Starter', value: 'starter' },
  { label: 'Growth', value: 'growth' },
  { label: 'Enterprise', value: 'enterprise' },
];

export function ProfileFormExample() {
  const [name, setName] = React.useState('');
  const [email, setEmail] = React.useState('');
  const [about, setAbout] = React.useState('');
  const [role, setRole] = React.useState('');
  const [plan, setPlan] = React.useState('growth');
  const [newsletter, setNewsletter] = React.useState(true);
  const [error, setError] = React.useState('');

  const handleSubmit = (event: React.FormEvent) => {
    event.preventDefault();
    if (!email.includes('@')) {
      setError('Enter a valid email address.');
      return;
    }
    setError('');
    // submit...
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-6 rounded-xl border border-secondary-100 bg-white p-6 shadow-sm">
      <div className="space-y-2">
        <label className="text-sm font-medium text-secondary-700">Full name</label>
        <Input placeholder="Jane Developer" value={name} onChange={(e) => setName(e.target.value)} />
      </div>

      <div className="space-y-2">
        <label className="text-sm font-medium text-secondary-700">Email</label>
        <Input
          placeholder="jane@example.com"
          value={email}
          variant={error ? 'error' : 'default'}
          onChange={(e) => setEmail(e.target.value)}
        />
        {error ? <p className="text-xs text-danger-600">{error}</p> : null}
      </div>

      <div className="space-y-2">
        <label className="text-sm font-medium text-secondary-700">About</label>
        <Textarea
          placeholder="Tell us about your work..."
          value={about}
          rows={4}
          onChange={(event) => setAbout(event.target.value)}
        />
      </div>

      <div className="space-y-2">
        <label className="text-sm font-medium text-secondary-700">Role</label>
        <Select
          value={role}
          onChange={(event) => setRole(event.target.value)}
          options={[{ label: 'Select role...', value: '' }, ...roleOptions]}
        />
      </div>

      <div className="space-y-3">
        <span className="text-sm font-medium text-secondary-700">Pricing plan</span>
        <RadioGroup
          name="pricing"
          value={plan}
          onChange={(event) => setPlan(event.target.value)}
          options={planOptions}
        />
      </div>

      <div className="flex items-start gap-3 rounded-lg border border-secondary-100 bg-secondary-50 p-4">
        <Checkbox checked={newsletter} onChange={(event) => setNewsletter(event.target.checked)} />
        <div>
          <p className="text-sm font-medium text-secondary-800">Weekly newsletter</p>
          <p className="text-sm text-secondary-500">
            Receive product updates, templates, and best practices straight to your inbox.
          </p>
        </div>
      </div>

      <div className="flex items-center justify-between">
        <Switch
          checked={newsletter}
          onCheckedChange={(checked) => setNewsletter(Boolean(checked))}
          aria-label="Toggle newsletter subscription"
        />
        <Button type="submit" variant="primary">
          Save profile
        </Button>
      </div>
    </form>
  );
}
