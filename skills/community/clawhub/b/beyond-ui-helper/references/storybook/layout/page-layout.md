# PageLayout

## Usage (Blog layout example)
```tsx
import {
  PageLayout,
  PageHeader,
  PageHero,
  PageContent,
  PageSidebar,
  PageFooter,
  PageLayoutContent,
} from '@beyondcorp/beyond-ui';
import '@beyondcorp/beyond-ui/dist/styles.css';
import { Badge } from '@beyondcorp/beyond-ui';
import { Avatar, AvatarImage, AvatarFallback } from '@beyondcorp/beyond-ui';

export function BlogLayout() {
  return (
    <PageLayout variant="blog" maxWidth="full">
      <PageHeader>
        <div className="max-w-6xl mx-auto px-4 py-6 flex items-center justify-between">
          <span className="text-2xl font-bold">Beyond Blog</span>
          <nav className="flex items-center gap-4 text-sm text-gray-600">
            <a href="#">Articles</a>
            <a href="#">Resources</a>
            <a href="#">About</a>
            <Badge variant="primary">Subscribe</Badge>
          </nav>
        </div>
      </PageHeader>

      <PageHero fullHeight={false} className="bg-primary-50">
        <div className="max-w-4xl mx-auto px-4 py-16 text-center space-y-4">
          <Badge variant="info">Case Study</Badge>
          <h1 className="text-4xl font-bold text-gray-900">Scaling UI Systems Across Teams</h1>
          <p className="text-lg text-gray-600">
            Explore how Beyond-UI enables product teams to build accessible, theme-aware layouts rapidly.
          </p>
        </div>
      </PageHero>

      <PageLayoutContent layout="sidebar" spacing="lg" className="max-w-6xl mx-auto px-4">
        <PageContent maxWidth="full" className="space-y-8">
          <article className="prose prose-gray">
            <p>
              Beyond-UI ships composable primitives so your marketing site, docs, or product pages stay consistent.
              Use PageLayout to orchestrate headers, heroes, content, and footers without reinventing structure.
            </p>
            <p>
              Publish case studies, release notes, or deep dives while staying on brand via Tailwind tokens.
            </p>
          </article>

          <section className="border-t border-gray-100 pt-8">
            <h2 className="text-xl font-semibold mb-4">Latest posts</h2>
            <div className="grid md:grid-cols-2 gap-6">
              <Card>
                <CardHeader>
                  <CardTitle>Design systems that scale</CardTitle>
                </CardHeader>
                <CardContent>
                  <p className="text-sm text-gray-600">How we use semantic tokens to drive multi-brand sites.</p>
                </CardContent>
              </Card>
              <Card>
                <CardHeader>
                  <CardTitle>Accessibility playbook</CardTitle>
                </CardHeader>
                <CardContent>
                  <p className="text-sm text-gray-600">Color contrast, keyboard nav, and live regions with Beyond-UI.</p>
                </CardContent>
              </Card>
            </div>
          </section>
        </PageContent>

        <PageSidebar position="right" width="md" className="space-y-6">
          <Card>
            <CardHeader>
              <CardTitle>About the author</CardTitle>
            </CardHeader>
            <CardContent className="flex items-center gap-3">
              <Avatar>
                <AvatarImage src="" alt="Mark Kiprotich" />
                <AvatarFallback>MK</AvatarFallback>
              </Avatar>
              <div>
                <p className="text-sm font-medium">Mark Kiprotich</p>
                <p className="text-xs text-gray-500">Product Engineer @ Beyond</p>
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle>Newsletter</CardTitle>
            </CardHeader>
            <CardContent>
              <p className="text-sm text-gray-600 mb-3">Stay informed on component releases and migration guides.</p>
              <form className="space-y-3">
                <Input type="email" placeholder="you@example.com" />
                <Button type="submit" className="w-full">Subscribe</Button>
              </form>
            </CardContent>
          </Card>
        </PageSidebar>
      </PageLayoutContent>

      <PageFooter variant="simple">
        <div className="max-w-6xl mx-auto px-4 py-8 text-sm text-gray-500 flex justify-between">
          <span>&copy; {new Date().getFullYear()} Beyond-UI. All rights reserved.</span>
          <a href="#" className="hover:text-gray-700">Privacy</a>
        </div>
      </PageFooter>
    </PageLayout>
  );
}
```

## Props
| Prop | Type | Description |
|------|------|-------------|
| variant | 'default' · 'centered' · 'sidebar' · 'landing' · 'product' · 'blog' | Determines layout scaffolding |
| maxWidth | 'sm' · 'md' · 'lg' · 'xl' · '2xl' · 'full' | Outer container width |
| contentLayout | 'default' · 'centered' · 'sidebar' · 'fullWidth' | Configures PageLayoutContent arrangement |
| contentSpacing | 'none' · 'sm' · 'md' · 'lg' · 'xl' | Gap between stacked sections |
| children | ReactNode | Compose header, hero, content, sidebar, footer regions |

## Notes
- Wrap inner sections with `PageLayoutContent` to toggle centered vs. sidebar splits.
- Pair with `PageHero` for marketing/landing hero treatments; `variant="blog"` adds balanced spacing.
- Combine with `useBreakpoint` for responsive tweaks and `useDarkMode` to honor theme toggle stories.

Story source: stories/PageLayout.stories.tsx
