# PasswordResetForm

## Usage
```tsx
import { PasswordResetForm } from '@beyondcorp/beyond-ui';
import '@beyondcorp/beyond-ui/dist/styles.css';

export function ForgotPasswordPage() {
  return (
    <div className="min-h-screen flex items-center justify-center bg-surface-50">
      <div className="bg-white shadow-lg rounded-xl p-8 w-full max-w-sm">
        <h1 className="text-xl font-semibold mb-2">Reset your password</h1>
        <p className="text-sm text-gray-500 mb-6">
          Enter the email linked to your account and we’ll send reset instructions.
        </p>
        <PasswordResetForm
          onReset={async (email) => {
            await requestPasswordReset(email);
          }}
          successMessage="If that email is registered, you'll receive a reset link shortly."
        />
      </div>
    </div>
  );
}
```

## Props
| Prop | Type | Description |
|------|------|-------------|
| onReset | (email: string) => Promise<void>\|void | Called with email when the form submits |
| isLoading | boolean | Locks inputs/button when true |
| successMessage | string | Optional override for success alert copy |
| errorMessage | string | Optional override for error alert copy |
| className | string | Extends wrapper classes |

## Notes
- Uses `react-hook-form` + Zod for validation; invalid email surfaces inline errors.
- Status banners swap between success/error states; set `isLoading` when wiring real API calls.
- Pair with LoginForm/SignupForm screens to complete auth recovery flows.

Story source: stories/PasswordResetForm.stories.tsx
