---
name: fec-route-protection
description: Use when implementing or reviewing frontend route protection, auth guards, RBAC, permission routes, login state handling, redirects, middleware, React Router, Next.js, Vue Router, or Nuxt route middleware; Chinese triggers include route protection, permission routing, login state.
---

#Route protection

## Purpose

Establish clear authentication, authorization and redirection boundaries for front-end applications to avoid unauthorized access and flickering rendering.

## When to Use

- The page needs to be logged in to access, or different roles can see different routes.
- Requires implementing route guards for React Router, Next.js, Nuxt or Vue Router.
- Login expiration, insufficient permissions, and organization/tenant switching need to be handled uniformly.
- Not used to replace server-side authorization; front-end routing protection can only improve the experience and cannot be used as the only security boundary.

## Procedure

### 1. Define authentication and authorization status

```ts
export type AuthStatus = "loading" | "anonymous" | "authenticated";

export interface CurrentUser {
  id: string;
  roles: string[];
  permissions: string[];
}

export function canAccess(user: CurrentUser, required: string[]) {
  return required.every((permission) => user.permissions.includes(permission));
}
```

### 2. React Router uses layout guards

```tsx
import { Navigate, Outlet, useLocation } from "react-router-dom";

interface ProtectedRouteProps {
  requiredPermissions?: string[];
}

export function ProtectedRoute({ requiredPermissions = [] }: ProtectedRouteProps) {
  const location = useLocation();
  const { status, user } = useAuth();

  if (status === "loading") return <RouteLoading />;
  if (status === "anonymous") {
    return <Navigate to="/login" replace state={{ from: location }} />;
  }
  if (requiredPermissions.length > 0 && !canAccess(user, requiredPermissions)) {
    return <Navigate to="/403" replace />;
  }

  return <Outlet />;
}
```

```tsx
const router = createBrowserRouter([
  {
    element: <ProtectedRoute requiredPermissions={["orders:read"]} />,
    children: [{ path: "/orders", element: <OrdersPage /> }],
  },
]);
```

### 3. Next.js prioritizes processing at the server boundary

```ts
// middleware.ts
import { NextResponse, type NextRequest } from "next/server";

export function middleware(request: NextRequest) {
  const token = request.cookies.get("session")?.value;
  const isPrivateRoute = request.nextUrl.pathname.startsWith("/dashboard");

  if (isPrivateRoute && !token) {
    const loginUrl = new URL("/login", request.url);
    loginUrl.searchParams.set("redirect", request.nextUrl.pathname);
    return NextResponse.redirect(loginUrl);
  }

  return NextResponse.next();
}

export const config = {
  matcher: ["/dashboard/:path*"],
};
```

For App Router pages that require fine-grained permissions, re-verify permissions in the server component or server action, regardless of client status.

### 4. Vue Router / Nuxt uses navigation guards

```ts
router.beforeEach(async (to) => {
  const auth = useAuthStore();
  if (auth.status === "unknown") await auth.fetchCurrentUser();

  if (to.meta.requiresAuth && !auth.user) {
    return { path: "/login", query: { redirect: to.fullPath } };
  }

  const required = to.meta.permissions as string[] | undefined;
  if (required?.length && !auth.canAccess(required)) {
    return { path: "/403" };
  }
});
```

### 5. Unify failure and jump experience

- `401`: Clean up expired sessions, jump to the login page and keep `redirect`.
- `403`: Enter the unauthorized page, do not try again.
- `loading`: Render a stable skeleton screen to avoid displaying private content first and then jumping.
- Successful login: only jump to the same origin and allowed path to prevent open redirect.
- RBAC: The permission matrix is returned from the trusted session or backend; the frontend is only used for routing experience and UI tailoring, and cannot replace interface authorization.
- Session refresh: Uniformly clean up status after 401 refresh failure; avoid multiple concurrent requests from triggering jumps or refresh storms.

## Constraints

- Front-end routing protection is not a security boundary; API, SSR loader, and server actions must undergo repeated authorization verification.
- Do not use `useEffect` to jump to the private page after the component is rendered, otherwise sensitive content will flicker.
- The redirect parameter must be restricted to within-site paths and URL input cannot be trusted directly.
- Permission information should come from a trusted session or backend response, don't rely solely on role fields in localStorage.
- Multi-tenant applications must incorporate the tenant/org context into permission determinations.
- Menu hiding is not considered authorization completion; users must authenticate when accessing the URL directly, refreshing the page, tampering with localStorage, and replacing tenants.

## Expected Output

Produce a set of routing guard implementations, covering loading, not logged in, insufficient permissions, bounce after login and session expiration. During verification, directly access the private URL, refresh the page, switch roles, and tamper with redirect parameters to confirm that the behavior is stable and the API still has server authorization.
