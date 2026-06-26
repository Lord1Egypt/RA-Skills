# Toast

## Usage
```tsx
import { Toast, showToast } from '@beyondcorp/beyond-ui';
import '@beyondcorp/beyond-ui/dist/styles.css';

export function DemoToast() {
  return (
    <div className="space-y-2">
      <button
        className="bg-primary-600 text-white px-3 py-2 rounded"
        onClick={() => showToast.success('Saved successfully!')}
      >
        Notify
      </button>
      <Toast />
    </div>
  );
}
```

## Props
| Prop | Type | Description |
|------|------|-------------|
| (Toast component) | – | Place `<Toast />` once near root to render notifications |
| showToast.* | functions | `showToast.success/info/warning/error` display toasts |

## Notes
- `showToast` helpers wrap react-hot-toast; customize duration or icons via options.
- Include `<Toast />` once per app to mount the toaster container.

Story source: stories/Toast.stories.tsx
