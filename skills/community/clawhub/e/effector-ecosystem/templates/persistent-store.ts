import { createEvent, createStore } from 'effector';
import { persist } from 'effector-storage/local';
import { or, val } from '@withease/contracts';

export const appStarted = createEvent();
export const themeChanged = createEvent<'light' | 'dark'>();

export const $theme = createStore<'light' | 'dark'>('light')
  .on(themeChanged, (_, theme) => theme);

persist({
  store: $theme,
  key: 'theme',
  contract: or(val('light'), val('dark')),
  pickup: appStarted,
});

export const $$theme = {
  theme: $theme,
  themeChanged,
};
