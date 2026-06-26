import * as React from 'react';
import {
  Modal,
  ModalHeader,
  ModalTitle,
  ModalDescription,
  ModalContent,
  ModalFooter,
  Button,
} from '@beyondcorp/beyond-ui';
import '@beyondcorp/beyond-ui/dist/styles.css';

export function DeleteModalExample() {
  const [open, setOpen] = React.useState(false);

  return (
    <div>
      <Button variant="danger" onClick={() => setOpen(true)}>
        Delete project
      </Button>
      <Modal open={open} onOpenChange={setOpen} size="sm">
        <ModalHeader>
          <ModalTitle>Delete project?</ModalTitle>
          <ModalDescription>
            Removing this project will delete dashboards, automations, and history. This action cannot be undone.
          </ModalDescription>
        </ModalHeader>
        <ModalContent className="space-y-3">
          <p className="text-sm text-secondary-600">
            Make sure you exported any necessary reports before deletion. Members will lose access immediately.
          </p>
        </ModalContent>
        <ModalFooter className="flex justify-end gap-3">
          <Button variant="ghost" onClick={() => setOpen(false)}>
            Cancel
          </Button>
          <Button variant="danger" onClick={() => setOpen(false)}>
            Confirm delete
          </Button>
        </ModalFooter>
      </Modal>
    </div>
  );
}
