> This is a sub-module of the `gcp-fullstack` skill. See the main [SKILL.md](../SKILL.md) for the Planning Protocol and overview.

## Service Selection: Auth Decision Tree

| Condition | Recommended Service | Why |
|---|---|---|
| Standard consumer app, social logins, email/password | **Firebase Auth** | Free tier generous, easy SDK, battle-tested |
| Enterprise SSO (SAML, OIDC), multi-tenancy, SLA | **Identity Platform** | Superset of Firebase Auth, tenant isolation, blocking functions |
| Machine-to-machine, service accounts | **Cloud IAM + Workload Identity** | No user auth needed, service-level access |

Firebase Auth and Identity Platform share the same API surface. Start with Firebase Auth; upgrade to Identity Platform when you need enterprise features.

---

## Part 8: Authentication

### Firebase Auth (default)

Use the same patterns as the `firebase-auth-setup` skill. Key files:

- `src/lib/firebase/client.ts` — client SDK initialization
- `src/lib/firebase/admin.ts` — admin SDK initialization
- `src/hooks/use-auth.ts` — auth state hook with Google, Apple, email/password providers
- `src/middleware.ts` — server-side token verification

### Identity Platform (enterprise upgrade)

Identity Platform uses the same Firebase Auth SDK but adds:

```bash
# Enable Identity Platform (replaces Firebase Auth)
gcloud services enable identitytoolkit.googleapis.com

# Enable multi-tenancy
gcloud identity-platform config update --enable-multi-tenancy

# Create a tenant
gcloud identity-platform tenants create \
  --display-name="Tenant A" \
  --allow-password-signup \
  --enable-email-link-signin
```

Client-side code is identical to Firebase Auth. Server-side adds tenant awareness:

```typescript
// Verify token with tenant context
import { adminAuth } from "@/lib/firebase/admin";

export async function verifyTokenWithTenant(token: string, tenantId: string) {
  const tenantAuth = adminAuth.tenantManager().authForTenant(tenantId);
  try {
    const decoded = await tenantAuth.verifyIdToken(token);
    return { uid: decoded.uid, email: decoded.email, tenantId: decoded.firebase.tenant };
  } catch {
    return null;
  }
}
```
