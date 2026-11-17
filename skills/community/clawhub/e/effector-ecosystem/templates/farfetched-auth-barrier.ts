// Example placement for strict FSD: entities/session/api/session-refresh-barrier.ts or app/api/apply-auth-barriers.ts
import {
  applyBarrier,
  createBarrier,
  createJsonMutation,
  isHttpErrorCode,
} from '@farfetched/core';
import { apiUrl } from '@/shared/api/base-url';
import { mapRemoteError } from '@/shared/api/errors';
import { SessionContract } from '@/entities/session';
import { userQuery } from '@/entities/user';
import { updateProfileMutation } from '@/features/profile-update';

export const refreshSessionMutation = createJsonMutation({
  request: {
    method: 'POST',
    url: apiUrl('/auth/refresh'),
    fetch: { credentials: 'include' },
  },
  response: {
    contract: SessionContract,
    mapError: ({ error }) => mapRemoteError(error),
  },
});

export const authBarrier = createBarrier({
  activateOn: {
    failure: isHttpErrorCode(401),
  },
  perform: [refreshSessionMutation],
});

applyBarrier([userQuery, updateProfileMutation], { barrier: authBarrier });
