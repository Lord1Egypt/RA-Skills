import { combine, createEvent, createStore, sample } from 'effector';

export const pageOpened = createEvent();
export const valueChanged = createEvent<string>();
export const submitted = createEvent();

export const $value = createStore('')
  .on(valueChanged, (_, value) => value);

export const $canSubmit = $value.map((value) => value.trim().length > 0);
export const $submitDisabled = $canSubmit.map((canSubmit) => !canSubmit);

sample({
  clock: submitted,
  source: $value,
  filter: $canSubmit,
  // target: mutation.start,
});

export const $vm = combine({
  value: $value,
  canSubmit: $canSubmit,
  submitDisabled: $submitDisabled,
});

// Public UI binding shape: use as `const { value, onSubmit } = useUnit($$model)`.
export const $$model = {
  value: $value,
  canSubmit: $canSubmit,
  submitDisabled: $submitDisabled,
  onValueChange: valueChanged,
  onSubmit: submitted,
};
