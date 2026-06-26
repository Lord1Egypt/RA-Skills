import {
  PageLayout,
  PageHeader,
  PageHero,
  PageLayoutContent,
  PageFooter,
  Button,
  Card,
  CardHeader,
  CardTitle,
  CardContent,
  Badge,
} from '@beyondcorp/beyond-ui';
import '@beyondcorp/beyond-ui/dist/styles.css';
import { ArrowRight, Sparkles, Shield, Zap, Globe } from 'lucide-react';

export function LandingShell() {
  return (
    <PageLayout variant="landing" maxWidth="full">
      <PageHeader sticky transparent>
        <div className="mx-auto flex h-16 max-w-6xl items-center justify-between px-4">
          <div className="flex items-center gap-2 text-primary-600">
            <Sparkles className="h-5 w-5" />
            <span className="text-lg font-semibold">Beyond UI</span>
          </div>
          <nav className="hidden items-center gap-6 text-sm font-medium text-secondary-600 md:flex">
            <a href="#features" className="hover:text-primary-600">Features</a>
            <a href="#templates" className="hover:text-primary-600">Templates</a>
            <a href="#pricing" className="hover:text-primary-600">Pricing</a>
          </nav>
          <Button variant="primary" size="sm" className="hidden md:flex">
            Get started
          </Button>
        </div>
      </PageHeader>

      <PageHero fullHeight>
        <div className="mx-auto flex max-w-3xl flex-col items-center gap-6 text-center">
          <Badge variant="info" className="gap-2">
            <Shield className="h-4 w-4" />
            Trusted by 2,400 teams
          </Badge>
          <h1 className="text-4xl font-bold tracking-tight text-secondary-900 sm:text-5xl">
            Build polished frontends in days, not weeks.
          </h1>
          <p className="text-lg text-secondary-500">
            Beyond UI is a themeable React component system with layouts, forms, dashboards, and marketing
            templates ready for production.
          </p>
          <div className="flex flex-col gap-3 sm:flex-row">
            <Button variant="primary" size="lg" className="gap-2">
              Explore components
              <ArrowRight className="h-5 w-5" />
            </Button>
            <Button variant="outline" size="lg">
              View Storybook
            </Button>
          </div>
        </div>
      </PageHero>

      <PageLayoutContent id="features" layout="centered" spacing="xl">
        <div className="grid gap-6 md:grid-cols-3">
          {[
            {
              title: 'Production ready',
              description: 'Type safe components, Storybook docs, and tests ready to ship.',
              icon: <Shield className="h-6 w-6 text-primary-600" />,
            },
            {
              title: 'Themeable tokens',
              description: 'Override semantic colors and spaces to match your brand instantly.',
              icon: <Zap className="h-6 w-6 text-primary-600" />,
            },
            {
              title: 'Full templates',
              description: 'Landing pages, dashboards, and portals assembled from modular blocks.',
              icon: <Globe className="h-6 w-6 text-primary-600" />,
            },
          ].map((feature) => (
            <Card key={feature.title}>
              <CardHeader className="flex flex-col gap-4">
                <div className="flex h-12 w-12 items-center justify-center rounded-full bg-primary-50 text-primary-600">
                  {feature.icon}
                </div>
                <CardTitle className="text-lg text-secondary-900">{feature.title}</CardTitle>
              </CardHeader>
              <CardContent className="text-sm text-secondary-500">
                {feature.description}
              </CardContent>
            </Card>
          ))}
        </div>
      </PageLayoutContent>

      <PageFooter variant="detailed">
        <div className="mx-auto flex max-w-6xl flex-col gap-6 px-4 py-10">
          <div className="flex flex-col gap-3 text-white md:flex-row md:items-center md:justify-between">
            <div className="flex items-center gap-2 text-primary-100">
              <Sparkles className="h-5 w-5" />
              <span className="text-lg font-semibold">Beyond UI</span>
            </div>
            <Button variant="secondary" className="bg-white text-secondary-900">
              Request a demo
            </Button>
          </div>
          <p className="text-sm text-primary-100">
            MIT licensed. Built by Beyond Corp. Follow the roadmap to learn what’s next.
          </p>
        </div>
      </PageFooter>
    </PageLayout>
  );
}
