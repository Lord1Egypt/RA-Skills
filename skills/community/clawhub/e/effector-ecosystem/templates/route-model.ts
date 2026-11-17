import { createRoute, chainRoute } from 'atomic-router';
import { startChain, freshChain } from '@farfetched/atomic-router';
import { pageQuery } from '../api/page.query';

export const pageRoute = createRoute<{ id: string }>();

export const pageOpened = pageRoute.opened;
export const pageClosed = pageRoute.closed;

// Use this when pageQuery params match the route-open payload expected by @farfetched/atomic-router.
export const pageLoadedRoute = chainRoute({
  route: pageRoute,
  ...startChain(pageQuery),
});

// Use freshChain instead when cache/stale policy should decide whether to refetch.
export const pageFreshRoute = chainRoute({
  route: pageRoute,
  ...freshChain(pageQuery),
});

// If query params differ from route params, map in the page model instead of React:
// sample({
//   clock: pageRoute.opened,
//   fn: ({ params }) => ({ id: params.id }),
//   target: pageQuery.start,
// });
