import { Button, Toast, showToast } from '@beyondcorp/beyond-ui';
import '@beyondcorp/beyond-ui/dist/styles.css';

export function ToastExamples() {
  return (
    <div className="space-y-4">
      <Toast />
      <div className="flex flex-wrap gap-3">
        <Button
          variant="primary"
          onClick={() => showToast.success('Deployed to production in 2m 14s')}
        >
          Success toast
        </Button>
        <Button
          variant="secondary"
          onClick={() => showToast.info('Analytics will refresh in the next hour')}
        >
          Info toast
        </Button>
        <Button
          variant="danger"
          onClick={() => showToast.error('Build failed: missing environment variables')}
        >
          Error toast
        </Button>
      </div>
    </div>
  );
}
