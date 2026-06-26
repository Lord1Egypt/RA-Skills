import { Card, CardHeader, CardTitle, CardContent, Button, Input, Checkbox } from '@beyondcorp/beyond-ui';
import '@beyondcorp/beyond-ui/dist/styles.css';

export function AuthLoginPanel() {
  return (
    <Card className="w-full max-w-md">
      <CardHeader>
        <CardTitle className="text-2xl">Sign in</CardTitle>
      </CardHeader>
      <CardContent className="space-y-5">
        <div className="space-y-2">
          <label className="text-sm font-medium text-secondary-700">Email</label>
          <Input type="email" placeholder="you@example.com" autoComplete="email" />
        </div>

        <div className="space-y-2">
          <label className="flex items-center justify-between text-sm font-medium text-secondary-700">
            Password
            <a href="/reset" className="text-primary-600 text-xs">Forgot?</a>
          </label>
          <Input type="password" placeholder="••••••••" autoComplete="current-password" />
        </div>

        <div className="flex items-center justify-between">
          <label className="flex items-center gap-2 text-sm text-secondary-600">
            <Checkbox />
            Remember me
          </label>
        </div>

        <Button type="submit" variant="primary" className="w-full">
          Continue
        </Button>

        <div className="flex items-center gap-2 text-xs text-secondary-500">
          <span className="h-px flex-1 bg-secondary-200" />
          or continue with
          <span className="h-px flex-1 bg-secondary-200" />
        </div>

        <Button variant="outline" type="button" className="w-full">
          Continue with Google
        </Button>
      </CardContent>
    </Card>
  );
}
