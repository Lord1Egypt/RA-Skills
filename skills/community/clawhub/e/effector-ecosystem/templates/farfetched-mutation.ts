import { createEvent, sample } from 'effector';
import { createJsonMutation, declareParams, concurrency } from '@farfetched/core';
import { apiUrl } from '@/shared/api/base-url';
import { mapRemoteError } from '@/shared/api/errors';
import { ResourceContract, mapResourceDto } from '../model/resource.contract';

export type UpdateResourceParams = {
  id: string;
  values: {
    name: string;
  };
};

export const updateResourceSubmitted = createEvent<UpdateResourceParams>();

export const updateResourceMutation = createJsonMutation({
  params: declareParams<UpdateResourceParams>(),
  request: {
    method: 'PATCH',
    url: ({ id }) => apiUrl(`/resources/${id}`),
    body: ({ values }) => values,
    // fetch: { credentials: 'include' },
  },
  response: {
    contract: ResourceContract,
    mapData: ({ result }) => mapResourceDto(result),
    mapError: ({ error }) => mapRemoteError(error),
  },
});

// Submit de-duplication belongs to the Effector model, not hidden in UI or `.watch`.
// Keep Farfetched concurrency permissive unless the project intentionally tests skipped/aborted lifecycle.
concurrency(updateResourceMutation, { strategy: 'TAKE_EVERY' });

sample({
  clock: updateResourceSubmitted,
  source: updateResourceMutation.$pending,
  filter: (pending) => !pending,
  fn: (_pending, params) => params,
  target: updateResourceMutation.start,
});
