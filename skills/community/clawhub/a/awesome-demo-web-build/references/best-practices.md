# Tech Stack Best Practices

> Sourced from official Next.js 15 docs, React Hook Form API docs, and shadcn/ui community patterns.

---

## Next.js 15 (App Router)

**Source:** https://nextjs.org/blog/next-15

### Server vs Client Components

From https://nextjs.org/docs/app/getting-started/server-and-client-components:

- **Default to Server Components** — no JS bundle cost, direct DB access
- Add `'use client'` only when needed: useState, useEffect, browser APIs, event listeners
- Push client boundaries as low/far as possible in the component tree
- Server Components can import Client Components; not vice versa (but can pass as props/children)

```tsx
// Server Component (default) — fetch data directly
async function Page({ params }: { params: Promise<{ id: string }> }) {
  const { id } = await params
  const item = await db.items.findUnique({ where: { id } })
  return <ItemDetail item={item} />
}

// Client Component — only when interactivity needed
'use client'
import { useState } from 'react'
export function LikeButton({ initialLikes }: { initialLikes: number }) {
  const [likes, setLikes] = useState(initialLikes)
  return <button onClick={() => setLikes(l => l + 1)}>{likes} Likes</button>
}
```

### Data Fetching

**Next.js 15 Breaking Change:** `GET` Route Handlers and client navigations are **no longer cached by default**.

```tsx
// Static — cached until manually invalidated (default)
const data = await fetch('https://...', { cache: 'force-cache' })

// Dynamic — refetched every request
const data = await fetch('https://...', { cache: 'no-store' })

// ISR — revalidate every N seconds
const data = await fetch('https://...', { next: { revalidate: 60 } })
```

### Async Request APIs (Next.js 15 Breaking)

`headers`, `cookies`, `params`, `searchParams` are now **async** in layout/page/route:

```tsx
// Next.js 15 — params is now a Promise
export default async function Page({
  params,
}: {
  params: Promise<{ id: string }>
}) {
  const { id } = await params
  // ...
}

// Access cookies/headers asynchronously
import { cookies, headers } from 'next/headers'
export async function Layout() {
  const cookieStore = await cookies()
  const headersList = await headers()
}
```

### Route Handlers

```ts
// app/api/items/route.ts
export async function GET(request: Request) {
  const { searchParams } = new URL(request.url)
  const limit = Number(searchParams.get('limit') ?? '10')

  const items = await db.items.findMany({ take: limit })
  return Response.json({ items })
}

export async function POST(request: Request) {
  const body = await request.json()
  const item = await db.items.create({ data: body })
  return Response.json({ item }, { status: 201 })
}
```

### Special Files

| File | Purpose |
|------|---------|
| `layout.tsx` | Shared UI, persists across navigations |
| `page.tsx` | Route segment, creates unique URL |
| `not-found.tsx` | 404 UI for route segment |
| `error.tsx` | Error boundary for route segment |
| `loading.tsx` | Suspense fallback during navigation |
| `route.ts` | API endpoint (don't cache GET by default in Next.js 15) |
| `template.tsx` | Remounts on navigation (vs layout persists) |

### Streaming with Suspense

```tsx
import { Suspense } from 'react'

export default function FeedPage() {
  return (
    <div>
      <h1>Feed</h1>
      <Suspense fallback={<FeedSkeleton />}>
        <FeedItems />
      </Suspense>
    </div>
  )
}

async function FeedItems() {
  const items = await fetchItems() // Streaming data
  return items.map(item => <FeedItem key={item.id} item={item} />)
}
```

### Server Actions

```tsx
// app/actions.ts
'use server'
export async function createItem(formData: FormData) {
  const name = formData.get('name')
  await db.items.create({ data: { name: name as string } })
  revalidatePath('/items')
}

// Client usage
<form action={createItem}>
  <input name="name" />
  <button type="submit">Create</button>
</form>
```

---

## Tailwind CSS

### Class Organization (Recommended)

```tsx
// Structure → Style → States
<button className="
  inline-flex items-center justify-center  // display & layout
  gap-2                               // child spacing
  px-4 py-2                           // padding
  text-sm font-medium                  // typography
  bg-primary text-white                // colors
  rounded-md                           // radius
  hover:bg-primary/90                  // interactive states
  disabled:opacity-50                  // conditional
  transition-colors                    // animation
">
```

### Design Token Usage

Always use CSS variables from the fetched DESIGN.md:

```tsx
// Use CSS variables, not hardcoded values
className="bg-background text-foreground border-border"

// Map to Tailwind
<div className="bg-[var(--background)] text-[var(--foreground)]" />
```

### Responsive Patterns

```tsx
// Mobile-first
className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3"

// Text responsive
className="text-sm md:text-base lg:text-lg"

// Spacing responsive
className="p-4 md:p-6 lg:p-8"
```

### Dark Mode

```tsx
// Use 'dark' class strategy (default in shadcn)
className="bg-white dark:bg-slate-950"

// Or use CSS variables for theme tokens
className="bg-[var(--card)] text-[var(--card-foreground)]"
```

---

## shadcn/ui

**Source:** https://ui.shadcn.com, https://www.rupeshpoudel.com.np/blog/shadcn-best-practices

### Component Composition

```tsx
// Start with base components, compose for your domain
import { Button } from '@/components/ui/button'
import { LogIn } from 'lucide-react'

// Create semantic components for your app
export function LoginButton({ isLoading, ...props }: LoginButtonProps) {
  return (
    <Button disabled={isLoading} {...props}>
      <LogIn className="h-4 w-4" />
      Sign in
    </Button>
  )
}
```

### Slot Pattern (Radix)

```tsx
// For polymorphic or extensible components
import { Slot } from '@radix-ui/react-slot'
import { type ButtonProps, buttonVariants } from '@/components/ui/button'

function IconButton({ asChild, ...props }: ButtonProps) {
  const Comp = asChild ? Slot : 'button'
  return <Comp {...props} />
}

// Usage — Slot passes props to the child
<IconButton asChild>
  <Link href="/settings">
    <Settings className="h-4 w-4" />
  </Link>
</IconButton>
```

### CSS Variables (Tailwind Config)

```js
// tailwind.config.ts — extend with design tokens
module.exports = {
  theme: {
    extend: {
      colors: {
        border: 'var(--border)',
        input: 'var(--input)',
        ring: 'var(--ring)',
        background: 'var(--background)',
        foreground: 'var(--foreground)',
        primary: {
          DEFAULT: 'var(--primary)',
          foreground: 'var(--primary-foreground)',
        },
      },
      borderRadius: {
        lg: 'var(--radius)',
        md: 'calc(var(--radius) - 2px)',
        sm: 'calc(var(--radius) - 4px)',
      },
    },
  },
}
```

### Utility: cn()

```tsx
// lib/utils.ts — merge Tailwind classes
import { type ClassValue, clsx } from 'clsx'
import { twMerge } from 'tailwind-merge'

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs))
}

// Usage — deduplicates conflicting Tailwind classes
<div className={cn('p-4', 'p-6', 'bg-white')} />
// → 'p-6 bg-white'
```

---

## React Hook Form + Zod

**Source:** https://react-hook-form.com/docs/useform

### Basic Pattern

```tsx
import { useForm } from 'react-hook-form'
import { zodResolver } from '@hookform/resolvers/zod'
import { z } from 'zod'

const schema = z.object({
  name: z.string().min(2),
  email: z.string().email(),
})

export function ContactForm() {
  const form = useForm<z.infer<typeof schema>>({
    resolver: zodResolver(schema),
    defaultValues: { name: '', email: '' },
  })

  return (
    <form onSubmit={form.handleSubmit(console.log)}>
      <input {...form.register('name')} />
      {form.formState.errors.name && (
        <span>{form.formState.errors.name.message}</span>
      )}
      <input {...form.register('email')} />
      <button type="submit">Submit</button>
    </form>
  )
}
```

### Controlled with Controller

For UI components that don't expose `ref`:

```tsx
import { Controller, useForm } from 'react-hook-form'

<Controller
  name="country"
  control={form.control}
  render={({ field }) => (
    <Select onValueChange={field.onChange} value={field.value}>
      <SelectTrigger>
        <SelectValue placeholder="Select country" />
      </SelectTrigger>
      <SelectContent>
        <SelectItem value="us">United States</SelectItem>
      </SelectContent>
    </Select>
  )}
/>
```

---

## Zustand

**Source:** https://docs.pmnd.rs/zustand

### Store Structure

```ts
import { create } from 'zustand'

interface ChatStore {
  messages: Message[]
  isLoading: boolean
  sendMessage: (text: string) => Promise<void>
  clearMessages: () => void
}

export const useChatStore = create<ChatStore>((set) => ({
  messages: [],
  isLoading: false,
  sendMessage: async (text) => {
    set({ isLoading: true })
    const msg = { id: crypto.randomUUID(), role: 'user', content: text }
    set((s) => ({ messages: [...s.messages, msg] }))
    const reply = await api.chat(text)
    set((s) => ({
      messages: [...s.messages, { id: crypto.randomUUID(), role: 'assistant', content: reply }],
      isLoading: false,
    }))
  },
  clearMessages: () => set({ messages: [] }),
}))
```

### Selectors & Derived State

```ts
// Inline selector — only re-renders on messages change
const messages = useChatStore((s) => s.messages)

// Selector for derived value
const messageCount = useChatStore((s) => s.messages.length)

// Stable reference with useShallow
import { useShallow } from 'zustand/react/shallow'
const { messages, isLoading } = useChatStore(
  useShallow((s) => ({ messages: s.messages, isLoading: s.isLoading }))
)
```

### Persistence

```ts
import { create } from 'zustand'
import { persist } from 'zustand/middleware'

const usePrefsStore = create(
  persist(
    (set) => ({
      theme: 'dark',
      setTheme: (theme) => set({ theme }),
    }),
    { name: 'preferences' }
  )
)
```

---

## TypeScript

### Strict Mode

```json
{
  "compilerOptions": {
    "strict": true,
    "noUncheckedIndexedAccess": true,
    "noImplicitReturns": true,
    "noFallthroughCasesInSwitch": true
  }
}
```

### Discriminated Unions for State

```ts
// Instead of optional fields, use discriminated unions
type AsyncState<T> =
  | { status: 'idle' }
  | { status: 'loading' }
  | { status: 'success'; data: T }
  | { status: 'error'; error: string }

// narrows correctly in switch/if
function render(state: AsyncState<User>) {
  if (state.status === 'loading') return <Spinner />
  if (state.status === 'error') return <Error message={state.error} />
  if (state.status === 'success') return <Profile user={state.data} />
}
```

### Import Organization

```ts
// 1. React
import { useState, useEffect } from 'react'
// 2. Next.js
import Link from 'next/link'
import Image from 'next/image'
// 3. External
import { z } from 'zod'
// 4. Internal (@/)
import { Button } from '@/components/ui/button'
import { cn } from '@/lib/utils'
// 5. Types (adjacent)
import type { Item } from '@/types'
```

---

## Performance Patterns

### Dynamic Imports

```tsx
import dynamic from 'next/dynamic'

const HeavyChart = dynamic(
  () => import('@/components/chart'),
  {
    ssr: false,
    loading: () => <Skeleton className="h-[300px] w-full" />
  }
)
```

### Font Optimization

```tsx
import { Inter } from 'next/font/google'

const inter = Inter({
  subsets: ['latin'],
  variable: '--font-inter',
  display: 'swap',
})

export default function Layout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en" className={inter.variable}>
      <body>{children}</body>
    </html>
  )
}
```

### Image Optimization

```tsx
import Image from 'next/image'

<Image
  src="/hero.jpg"
  alt="Hero"
  width={1200}
  height={600}
  priority          // preload above-fold images
  className="object-cover"
/>
```

---

## File Structure (Recommended)

```
/app
  /(auth)
    /login/page.tsx
    /register/page.tsx
  /(dashboard)
    /layout.tsx       # Sidebar + header
    /page.tsx         # Dashboard home
    /settings/page.tsx
  /api
    /items/route.ts
  layout.tsx          # Root layout (fonts, providers)
  page.tsx            # Landing/home

/components
  /ui                 # shadcn/ui base components
  /features           # Feature-specific (e.g., chat/, dashboard/)
    /chat
      chat-input.tsx
      chat-message.tsx
    /dashboard
      stats-card.tsx

/lib
  utils.ts            # cn(), formatDate(), etc.
  db.ts               # Prisma/DB client
  auth.ts             # Auth utilities

/hooks
  use-chat.ts
  use-debounce.ts

/types
  index.ts            # Shared types (re-export from features)
```
