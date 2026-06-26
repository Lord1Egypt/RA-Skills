import { useState } from 'react';
import { Spinner, Button } from '@beyondcorp/beyond-ui';
import '@beyondcorp/beyond-ui/dist/styles.css';

export function LoadingOverlay() {
  const [loading, setLoading] = useState(false);

  const simulateRefresh = () => {
    setLoading(true);
    setTimeout(() => setLoading(false), 1800);
  };

  return (
    <div className="relative flex h-48 w-full items-center justify-center rounded-lg border border-secondary-100 bg-white">
      {loading ? (
        <div className="absolute inset-0 flex flex-col items-center justify-center gap-3 bg-white/80">
          <Spinner size="lg" />
          <span className="text-sm text-secondary-600">Syncing customer records…</span>
        </div>
      ) : (
        <p className="text-sm text-secondary-500">Click refresh to sync latest CRM data.</p>
      )}

      <Button
        variant="primary"
        size="sm"
        className="absolute bottom-4 right-4"
        onClick={simulateRefresh}
      >
        Refresh data
      </Button>
    </div>
  );
}
