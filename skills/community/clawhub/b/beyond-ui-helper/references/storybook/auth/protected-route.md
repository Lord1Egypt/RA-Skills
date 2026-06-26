# ProtectedRoute

## Usage
```tsx
import { ProtectedRoute } from '@beyondcorp/beyond-ui';
import { AuthProvider } from '@beyondcorp/beyond-ui/contexts/AuthContext';
import '@beyondcorp/beyond-ui/dist/styles.css';
import { DashboardShell } from './DashboardShell';
import { UnauthorizedScreen } from './UnauthorizedScreen';

export function AppRoutes() {
  return (
    <AuthProvider>
      <Router>
        <Routes>
          <Route path="/login" element={<LoginPage />} />
          <Route
            path="/admin"
            element={
              <ProtectedRoute requiredRole="admin" fallback={<UnauthorizedScreen />}>
                <DashboardShell />
              </ProtectedRoute>
            }
          />
        </Routes>
      </Router>
    </AuthProvider>
  );
}
```

## Props
| Prop | Type | Description |
|------|------|-------------|
| requiredRole | string | Optional role to enforce (matched against `user.role`) |
| fallback | ReactNode | Rendered when user lacks required role |
| redirectTo | string | Route to redirect unauthenticated users (default `/login`) |
| children | ReactNode | Protected content |

## Notes
- Relies on `useAuth` context for `user`, `isAuthenticated`, and `isLoading`—wrap your app with `AuthProvider`.
- Shows a loading spinner while auth state hydrates; redirect preserves `location.state.from` for post-login navigation.
- Exported helpers `useRequireRole` and `withRoleProtection` provide hook/HOC alternatives for role checks.

Story source: stories/ProtectedRoute.stories.tsx
