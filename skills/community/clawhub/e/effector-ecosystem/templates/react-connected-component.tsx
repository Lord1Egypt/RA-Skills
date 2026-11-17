import { useUnit } from 'effector-react';
import { $$form } from '../model/form.model';

export function ConnectedForm() {
  const {
    name,
    email,
    errors,
    submitDisabled,
    onNameChange,
    onEmailChange,
    onSubmit,
  } = useUnit($$form);

  return (
    <form
      onSubmit={(event) => {
        event.preventDefault();
        onSubmit();
      }}
    >
      <input
        value={name}
        aria-invalid={Boolean(errors.name)}
        onChange={(event) => onNameChange(event.currentTarget.value)}
      />

      <input
        value={email}
        aria-invalid={Boolean(errors.email)}
        onChange={(event) => onEmailChange(event.currentTarget.value)}
      />

      <button type="submit" disabled={submitDisabled}>
        Save
      </button>
    </form>
  );
}
