import { Button, NightModeSwitch } from '@beyondcorp/beyond-ui';
import '@beyondcorp/beyond-ui/dist/styles.css';
import { useState } from 'react';
import { LayoutDashboard, Grid, Users } from 'lucide-react';

export function ThemeableToolbar() {
  const [view, setView] = useState<'dashboard' | 'grid' | 'team'>('dashboard');

  return (
    <div className="flex items-center justify-between rounded-xl border border-secondary-100 bg-white p-4 shadow-sm">
      <div className="flex items-center gap-2">
        <Button
          size="sm"
          variant={view === 'dashboard' ? 'primary' : 'ghost'}
          onClick={() => setView('dashboard')}
          icon={<LayoutDashboard className="h-4 w-4" />}
        >
          Dashboard
        </Button>
        <Button
          size="sm"
          variant={view === 'grid' ? 'primary' : 'ghost'}
          onClick={() => setView('grid')}
          icon={<Grid className="h-4 w-4" />}
        >
          Kanban
        </Button>
        <Button
          size="sm"
          variant={view === 'team' ? 'primary' : 'ghost'}
          onClick={() => setView('team')}
          icon={<Users className="h-4 w-4" />}
        >
          Team
        </Button>
      </div>
      <NightModeSwitch ariaLabel="Toggle dark mode" variant="ghost" />
    </div>
  );
}
