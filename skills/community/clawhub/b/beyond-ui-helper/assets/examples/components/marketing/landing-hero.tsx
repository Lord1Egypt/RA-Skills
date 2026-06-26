import { Button, Badge, Card, CardContent, CardHeader, CardTitle } from '@beyondcorp/beyond-ui';
import '@beyondcorp/beyond-ui/dist/styles.css';
import { ArrowRight, Sparkle, ShieldCheck } from 'lucide-react';

export function LandingHeroSection() {
  return (
    <section className="relative overflow-hidden rounded-3xl bg-gradient-to-br from-primary-50 via-white to-secondary-50 p-10 shadow-lg">
      <div className="flex flex-col gap-8 md:flex-row md:items-center md:justify-between">
        <div className="space-y-6 md:max-w-lg">
          <Badge variant="info" className="gap-2 text-primary-600">
            <ShieldCheck className="h-4 w-4" />
            Trusted by 2,000+ teams
          </Badge>
          <h1 className="text-4xl font-bold text-secondary-900 md:text-5xl">
            Ship production-grade frontends without the design debt.
          </h1>
          <p className="text-lg text-secondary-600">
            Beyond UI bundles fully typed components, dashboard layouts, and theming tokens so your team can launch polished experiences in days.
          </p>
          <div className="flex flex-col gap-3 sm:flex-row">
            <Button variant="primary" size="lg" className="gap-1">
              Start building
              <ArrowRight className="h-5 w-5" />
            </Button>
            <Button variant="outline" size="lg">
              View Storybook
            </Button>
          </div>
        </div>

        <Card className="max-w-sm border border-primary-100 bg-white/70 backdrop-blur">
          <CardHeader>
            <CardTitle className="flex items-center gap-2 text-secondary-900">
              <Sparkle className="h-4 w-4 text-primary-600" />
              Why Beyond UI
            </CardTitle>
          </CardHeader>
          <CardContent className="space-y-3 text-sm text-secondary-600">
            <p>✓ 35+ components with consistent variants and accessibility baked in.</p>
            <p>✓ Works with or without Tailwind thanks to semantic CSS tokens.</p>
            <p>✓ Hooks, layouts, and Storybook docs to accelerate onboarding.</p>
          </CardContent>
        </Card>
      </div>
    </section>
  );
}
