import { createStore, useStore } from '@/lib/store';

/**
 * The signed-in user (demo role). In production, single sign-on / a portal cookie provides the employee id and the backend looks up
 * organization, role and data scope in the user–organization table; the prototype simulates this with the demo role switcher in the top bar.
 * The example is purchase request approval; rewrite RoleKey / USERS per project.
 */
export type RoleKey = 'applicant' | 'approver' | 'finance' | 'admin';

export interface DemoUser {
  role: RoleKey;
  empNo: string;
  name: string;
  orgCode: string;
  orgName: string;
}

export const USERS: Record<RoleKey, DemoUser> = {
  applicant: { role: 'applicant', empNo: 'E1001', name: '周敏', orgCode: 'D01', orgName: '市场部' },
  approver: { role: 'approver', empNo: 'E1002', name: '林可', orgCode: 'D01', orgName: '市场部' },
  finance: { role: 'finance', empNo: 'E2001', name: '陈立衡', orgCode: 'F01', orgName: '财务部' },
  admin: { role: 'admin', empNo: 'E9001', name: '吴佳', orgCode: 'IT', orgName: '信息部' },
};

interface SessionState {
  role: RoleKey;
}

export const sessionStore = createStore<SessionState>('session', () => ({ role: 'applicant' }));

/** Fall back to the default role if an older version saved a removed role */
if (!(sessionStore.get().role in USERS)) sessionStore.set({ role: 'applicant' });

export function useRole(): RoleKey {
  return useStore(sessionStore, (s) => s.role);
}

export function useUser(): DemoUser {
  return USERS[useRole()];
}

export function setRole(role: RoleKey) {
  sessionStore.set({ role });
}
