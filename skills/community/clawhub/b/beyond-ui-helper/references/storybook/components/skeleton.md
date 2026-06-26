# Skeleton

## Usage
```tsx
import { Skeleton } from '@beyondcorp/beyond-ui';
import '@beyondcorp/beyond-ui/dist/styles.css';

export function LoadingCard() {
  return (
    <div className="space-y-4 max-w-md w-full border rounded-lg shadow p-4 bg-white">
      <div className="flex items-center gap-4">
        <Skeleton className="h-10 w-10 rounded-full" />
        <div className="flex-1 space-y-1">
          <Skeleton className="h-4 w-3/4" />
          <Skeleton className="h-3 w-1/2" />
        </div>
      </div>
      <Skeleton className="h-4 w-full" />
      <Skeleton className="h-6 w-2/3" />
      <div className="flex gap-2">
        <Skeleton className="h-8 w-20 rounded" />
        <Skeleton className="h-8 w-20 rounded" />
      </div>
    </div>
  );
}
```

## Props
| Prop | Type | Description |
|------|------|-------------|
| className | string | Tailwind utility classes defining size, shape, color |

## Notes
- Use multiple skeletons to approximate the layout of the eventual content.
- Combine rounded classes (`rounded`, `rounded-full`) to mimic avatars or buttons.

Story source: stories/Skeleton.stories.tsx
