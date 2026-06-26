# LoginForm

## Usage
```tsx
import { LoginForm } from '@beyondcorp/beyond-ui';
import { AuthProvider } from '@beyondcorp/beyond-ui/contexts/AuthContext';
import '@beyondcorp/beyond-ui/dist/styles.css';

export function LoginScreen() {
  return (
    <AuthProvider>
      <div className="min-h-screen flex items-center justify-center bg-gray-50">
        <LoginForm
          onSuccess={() => console.log('Logged in')}
          onForgotPassword={() => console.log('Reset flow')}
          onSignupClick={() => console.log('Go to signup')}
        />
      </div>
    </AuthProvider>
  );
}
```

## Props
| Prop | Type | Description |
|------|------|-------------|
| onSuccess | () => void | Fired after successful login (AuthProvider resolves) |
| onForgotPassword | () => void | Callback for "Forgot password?" link |
| onSignupClick | () => void | Handles "Create account" link |
| className | string | Tailwind classes to extend outer wrapper |

## Notes
- Wrap in `AuthProvider` to supply `useAuth` context—handles `login`, loading/error states.
- Uses `react-hook-form` + Zod; invalid fields display inline errors, spinner shows during submission.
- Includes demo credentials section; swap copy or hide if you supply real authentication.

Story source: stories/LoginForm.stories.tsx
