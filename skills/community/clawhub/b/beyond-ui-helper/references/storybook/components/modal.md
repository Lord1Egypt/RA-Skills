# Modal

## Usage
```tsx
import { Modal, ModalHeader, ModalTitle, ModalContent, ModalFooter } from '@beyondcorp/beyond-ui';
import { Button } from '@beyondcorp/beyond-ui';
import '@beyondcorp/beyond-ui/dist/styles.css';

export function ExampleModal() {
  const [open, setOpen] = useState(false);

  return (
    <div>
      <Button onClick={() => setOpen(true)}>Open modal</Button>
      <Modal open={open} onOpenChange={setOpen} size="md">
        <ModalHeader>
          <ModalTitle>Edit profile</ModalTitle>
        </ModalHeader>
        <ModalContent className="space-y-3">
          <Input label="Name" placeholder="Ada Lovelace" />
          <Textarea label="Bio" placeholder="Add a short bio" />
        </ModalContent>
        <ModalFooter>
          <Button variant="ghost" onClick={() => setOpen(false)}>Cancel</Button>
          <Button variant="primary">Save changes</Button>
        </ModalFooter>
      </Modal>
    </div>
  );
}
```

## Props
| Prop | Type | Description |
|------|------|-------------|
| open | boolean | Controls whether the modal is visible |
| onOpenChange | (open: boolean) => void | Fired when the modal toggles open/closed |
| size | 'sm' | 'md' | 'lg' | 'xl' | 'full' | Sets maximum width (default: md) |
| className | string | Utility classes for the modal container |

## Notes
- When `open` is false the modal renders null; wrap in state to control visibility.
- The backdrop closes the modal when clicked; disable by handling `onOpenChange` accordingly.
- Include `ModalHeader`, `ModalContent`, and `ModalFooter` for consistent structure.

Story source: stories/Modal.stories.tsx
