import { createEffect, createEvent, sample } from 'effector';

export type AppStartParams = {
  initialUrl?: string;
  locale?: string;
};

export const appStarted = createEvent<AppStartParams>();
export const appDestroyed = createEvent();

export const storagePickupStarted = createEvent<AppStartParams>();
export const i18nStarted = createEvent<AppStartParams>();
export const initialRouteResolved = createEvent<string | undefined>();

const browserIntegrationsStartedFx = createEffect<AppStartParams, void>();
const routerStartedFx = createEffect<AppStartParams, string | undefined>();

sample({ clock: appStarted, target: storagePickupStarted });
sample({ clock: appStarted, target: i18nStarted });
sample({ clock: appStarted, target: browserIntegrationsStartedFx });
sample({ clock: appStarted, target: routerStartedFx });
sample({ clock: routerStartedFx.doneData, target: initialRouteResolved });

// Runtime/test usage:
// const scope = fork();
// await allSettled(appStarted, { scope, params: { initialUrl: location.href } });

// Review rule: do not add a free-floating `startRouter(scope)` / `startAppClock(scope)`
// sequence for ordinary startup. Add router/history/clock installation as effects
// sampled from `appStarted`; use external helpers only for documented host adapter wiring.

// Audit note for protected-route apps:
// if the router can open a protected URL before session/storage restore finishes,
// do not start `routerStartedFx` in parallel with the restore query. Either sample
// router startup from `sessionRestoreFinished`, or model auth as `unknown` and let
// protected route chains wait for a known session state.
