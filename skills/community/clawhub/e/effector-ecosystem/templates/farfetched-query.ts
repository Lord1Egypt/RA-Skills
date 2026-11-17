import { createJsonQuery, declareParams, concurrency } from '@farfetched/core';
import { apiUrl } from '@/shared/api/base-url';
import { mapRemoteError } from '@/shared/api/errors';
import { ResourceContract, mapResourceDto } from '../model/resource.contract';

export type ResourceQueryParams = {
  id: string;
};

export const resourceQuery = createJsonQuery({
  params: declareParams<ResourceQueryParams>(),
  request: {
    method: 'GET',
    url: ({ id }) => apiUrl(`/resources/${id}`),
    // query: ({ id }) => ({ expand: 'owner' }),
    // fetch: { credentials: 'include' }, // cookie/session APIs; do not use deprecated top-level credentials
  },
  response: {
    contract: ResourceContract,
    mapData: ({ result }) => mapResourceDto(result),
    mapError: ({ error }) => mapRemoteError(error),
  },
});

// Use the operator; do not put concurrency into createJsonQuery config.
concurrency(resourceQuery, { strategy: 'TAKE_LATEST' });
