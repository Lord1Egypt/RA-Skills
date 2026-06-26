# SignupForm

## Usage
```tsx
import { SignupForm } from '@beyondcorp/beyond-ui';
import { AuthProvider } from '@beyondcorp/beyond-ui/contexts/AuthContext';
import '@beyondcorp/beyond-ui/dist/styles.css';

export function SignupScreen() {
  return (
    <AuthProvider>
      <div className="min-h-screen flex items-center justify-center bg-gray-50 p-6">
        <SignupForm
          onSuccess={() => console.log('Account created!')}
          onLoginClick={() => console.log('Back to login')}
        />
      </div>
    </AuthProvider>
  );
}
```

## Props
| Prop | Type | Description |
|------|------|-------------|
| onSuccess | () => void | Invoked after successful registration |
| onLoginClick | () => void | Callback for "Already have an account" link |
| className | string | Extra Tailwind classes for the outer wrapper |

## Notes
- Requires `AuthProvider`; leverages `useAuth` for async signup, loading, and error states.
- Real-time validation via `react-hook-form` + Zod; password strength badge uses `calculatePasswordStrength` helper.
- Includes terms checkbox & marketing opt-in copy—adapt copy or remove sections to match your flow.

Story source: stories/SignupForm.stories.tsx
