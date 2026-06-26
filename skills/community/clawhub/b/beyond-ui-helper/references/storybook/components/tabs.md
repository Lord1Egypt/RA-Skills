# Tabs

## Usage
```tsx
import { Tabs, TabsList, TabsTrigger, TabsContent } from '@beyondcorp/beyond-ui';
import '@beyondcorp/beyond-ui/dist/styles.css';

export function SettingsTabs() {
  const [value, setValue] = useState('profile');

  return (
    <Tabs value={value} onValueChange={setValue} className="w-full max-w-lg">
      <TabsList>
        <TabsTrigger value="profile">Profile</TabsTrigger>
        <TabsTrigger value="billing">Billing</TabsTrigger>
        <TabsTrigger value="team">Team</TabsTrigger>
      </TabsList>
      <TabsContent value="profile">Profile content here</TabsContent>
      <TabsContent value="billing">Billing content here</TabsContent>
      <TabsContent value="team">Team content here</TabsContent>
    </Tabs>
  );
}
```

## Props
| Prop | Type | Description |
|------|------|-------------|
| value | string | Current active tab value |
| defaultValue | string | Initial active tab (uncontrolled) |
| onValueChange | (value: string) => void | Callback when tab changes |

### TabsTrigger
| Prop | Type | Description |
|------|------|-------------|
| value | string | Identifier linking trigger to content |
| disabled | boolean | Prevents activation of the trigger |

## Notes
- Compose TabsList + TabsTrigger in a flex container for horizontal tab bars.
- Use TabsContent to render content sections with matching `value`.

Story source: stories/Tabs.stories.tsx
