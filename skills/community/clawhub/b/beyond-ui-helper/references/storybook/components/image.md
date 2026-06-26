# Image

## Usage
```tsx
import { Image } from '@beyondcorp/beyond-ui';
import '@beyondcorp/beyond-ui/dist/styles.css';

export function HeroImage() {
  return (
    <div className="w-80 h-48">
      <Image
        src="https://images.unsplash.com/photo-1506744038136-46273834b3fb?w=800"
        alt="Greenhouse"
        className="rounded-lg shadow"
        style={{ width: '100%', height: '100%' }}
      />
    </div>
  );
}
```

## Props
| Prop | Type | Description |
|------|------|-------------|
| src | string | Image source URL (required) |
| alt | string | Accessible alt text |
| className | string | Tailwind utility classes applied to the <img> |
| skeletonClassName | string | Tailwind classes for the loading placeholder |

## Notes
- Displays a skeleton loader until the image is ready; customize via `skeletonClassName`.
- Maintains the container dimensions you provide; wrap in a sized div for layout control.
- Falls back to a solid background on load failure.

Story source: stories/Image.stories.tsx
