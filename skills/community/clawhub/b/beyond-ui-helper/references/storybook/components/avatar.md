# Avatar

## Usage
```tsx
import { Avatar, AvatarImage, AvatarFallback } from '@beyondcorp/beyond-ui';
import '@beyondcorp/beyond-ui/dist/styles.css';

export function ProfileAvatar() {
  return (
    <Avatar size="lg">
      <AvatarImage src="https://randomuser.me/api/portraits/women/44.jpg" />
      <AvatarFallback>JS</AvatarFallback>
    </Avatar>
  );
}
```

## Props
| Prop | Type | Description |
|------|------|-------------|
| size | 'sm' | 'md' | 'lg' | 'xl' | Control avatar diameter (default: md) |

## Notes
- AvatarFallback renders initials or placeholders when AvatarImage fails.
- Compose Avatar inside flex layouts for group or profile blocks.

Story source: stories/Avatar.stories.tsx