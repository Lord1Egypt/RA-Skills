# Cross-Framework Integration Guide

Complete guide for integrating and using the Frontend Design Ultimate skill across React, Vue 3, and Nuxt 3 frameworks.

## Table of Contents

1. [Quick Start Comparison](#quick-start-comparison)
2. [Framework Setup Details](#framework-setup-details)
3. [Component Patterns](#component-patterns)
4. [State Management](#state-management)
5. [Routing Integration](#routing-integration)
6. [Animation Implementation](#animation-implementation)
7. [Performance Optimization](#performance-optimization)
8. [Common Patterns by Framework](#common-patterns-by-framework)
9. [Migration Examples](#migration-examples)

---

## Quick Start Comparison

### Initialize Projects

```bash
# React + Vite (Static SPA)
bash scripts/init-vite.sh my-react-app
cd my-react-app
npm run dev

# React + Next.js (SSR/SSG)
bash scripts/init-nextjs.sh my-next-app
cd my-next-app
npm run dev

# Vue 3 + Vite (Static SPA)
bash scripts/init-vue-vite.sh my-vue-app
cd my-vue-app
npm run dev

# Nuxt 3 (Full-stack/SSR/SSG)
bash scripts/init-nuxt.sh my-nuxt-app
cd my-nuxt-app
npm run dev
```

### Build & Deploy

| Framework | Dev Server | Build | Output | Deploy |
|-----------|-----------|-------|--------|--------|
| React + Vite | `npm run dev` | `npm run build` | `dist/` | Any static host |
| React + Next.js | `npm run dev` | `npm run build` | `.next/` | Vercel, Node.js |
| Vue 3 + Vite | `npm run dev` | `npm run build` | `dist/` | Any static host |
| Nuxt 3 | `npm run dev` | `npm run generate` | `.output/public/` | Vercel, Netlify, Node.js |

---

## Framework Setup Details

### React + Vite Configuration

**Key Files**:
- `vite.config.ts` - Build configuration with path aliases
- `tsconfig.json` - TypeScript configuration
- `tailwind.config.ts` - Tailwind with shadcn/ui theme
- `src/index.css` - Global CSS with CSS variables

**Dependencies**:
```json
{
  "dependencies": {
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "framer-motion": "^10.16.0",
    "lucide-react": "^0.263.0",
    "@radix-ui/react-slot": "^1.0.2",
    "class-variance-authority": "^0.7.0",
    "clsx": "^2.0.0",
    "tailwind-merge": "^1.14.0"
  },
  "devDependencies": {
    "typescript": "^5.0.0",
    "vite": "^4.4.0",
    "@vitejs/plugin-react": "^4.0.0",
    "tailwindcss": "^3.3.0"
  }
}
```

**Path Aliases**:
```typescript
// vite.config.ts
resolve: {
  alias: {
    "@": path.resolve(__dirname, "./src"),
  },
}

// tsconfig.json
"paths": {
  "@/*": ["./src/*"]
}
```

### React + Next.js Configuration

**Additional Features**:
- App Router (`app/` directory structure)
- Server Components (default) vs Client Components (`'use client'`)
- Image optimization via `next/image`
- Built-in routing, API routes, middleware

**Next.js-Specific Config**:
```typescript
// next.config.js
module.exports = {
  images: {
    domains: ['images.unsplash.com'],
  },
}
```

**Server vs Client Components**:
```tsx
// app/page.tsx (Server Component by default)
import { Hero } from '@/components/hero' // Client component

export default function Home() {
  return (
    <main>
      <Hero />
      {/* Server-rendered content */}
    </main>
  )
}
```

```tsx
// components/hero.tsx (Client Component)
'use client'
import { motion } from 'framer-motion'

export function Hero() {
  return <motion.div>{/* Animated content */}</motion.div>
}
```

### Vue 3 + Vite Configuration

**Key Files**:
- `vite.config.ts` - Vue plugin and path aliases
- `tsconfig.json` - TypeScript with Vue support
- `tailwind.config.ts` - Tailwind theme
- `src/assets/index.css` - Global styles
- `src/plugins/motion.ts` - Motion plugin setup

**Dependencies**:
```json
{
  "dependencies": {
    "vue": "^3.3.0",
    "@vueuse/core": "^10.5.0",
    "@vueuse/motion": "^2.2.0",
    "radix-vue": "^1.4.0",
    "lucide-vue-next": "^0.263.0",
    "class-variance-authority": "^0.7.0",
    "clsx": "^2.0.0",
    "tailwind-merge": "^1.14.0"
  },
  "devDependencies": {
    "typescript": "^5.0.0",
    "vite": "^4.4.0",
    "@vitejs/plugin-vue": "^4.3.0",
    "tailwindcss": "^3.3.0"
  }
}
```

**Vue Plugin Setup**:
```typescript
// src/main.ts
import { createApp } from 'vue'
import App from './App.vue'
import { setupMotion } from './plugins/motion'

const app = createApp(App)
setupMotion(app)
app.mount('#app')
```

### Nuxt 3 Configuration

**Key Features**:
- Auto-imports (components, composables, utils)
- File-based routing (`pages/`)
- Multiple rendering modes (SSR, SSG, SPA, hybrid)
- Built-in modules system

**nuxt.config.ts**:
```typescript
export default defineNuxtConfig({
  compatibilityDate: '2024-01-01',

  modules: [
    '@nuxtjs/tailwindcss',
    '@nuxt/ui'
  ],

  ui: {
    theme: {
      colors: {
        primary: 'green',
        neutral: 'slate'
      }
    }
  }
})
```

**Auto-Imports Available**:
- `ref`, `reactive`, `computed`, `watch`, etc. (Vue Composition API)
- `useRouter`, `useRoute`, `useHead`, `useSeoMeta`, etc. (Nuxt composables)
- All components in `components/` directory
- All utilities in `utils/` or `lib/` directory

---

## Component Patterns

### Button Component (All Frameworks)

**React**:
```tsx
// src/components/ui/button.tsx
import * as React from "react"
import { Slot } from "@radix-ui/react-slot"
import { cva, type VariantProps } from "class-variance-authority"
import { cn } from "@/lib/utils"

const buttonVariants = cva(
  "inline-flex items-center justify-center rounded-md text-sm font-medium...",
  {
    variants: {
      variant: {
        default: "bg-primary text-primary-foreground hover:bg-primary/90",
        destructive: "bg-destructive text-destructive-foreground...",
        outline: "border border-input bg-background hover:bg-accent...",
        secondary: "bg-secondary text-secondary-foreground...",
        ghost: "hover:bg-accent hover:text-accent-foreground",
        link: "text-primary underline-offset-4 hover:underline",
      },
      size: {
        default: "h-10 px-4 py-2",
        sm: "h-9 rounded-md px-3",
        lg: "h-11 rounded-md px-8",
        icon: "h-10 w-10",
      },
    },
    defaultVariants: {
      variant: "default",
      size: "default",
    },
  }
)

export interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement>,
  VariantProps<typeof buttonVariants> {
  asChild?: boolean
}

const Button = React.forwardRef<HTMLButtonElement, ButtonProps>(
  ({ className, variant, size, asChild = false, ...props }, ref) => {
    const Comp = asChild ? Slot : "button"
    return (
      <Comp
        className={cn(buttonVariants({ variant, size, className }))}
        ref={ref}
        {...props}
      />
    )
  }
)
Button.displayName = "Button"

export { Button, buttonVariants }
```

**Vue 3**:
```vue
<!-- src/components/ui/Button.vue -->
<script setup lang="ts">
import { computed } from 'vue'
import { cva, type VariantProps } from 'class-variance-authority'
import { cn } from '@/lib/utils'

const buttonVariants = cva(
  "inline-flex items-center justify-center rounded-md text-sm font-medium...",
  {
    variants: {
      variant: {
        default: "bg-primary text-primary-foreground hover:bg-primary/90",
        destructive: "bg-destructive text-destructive-foreground...",
        outline: "border border-input bg-background hover:bg-accent...",
        secondary: "bg-secondary text-secondary-foreground...",
        ghost: "hover:bg-accent hover:text-accent-foreground",
        link: "text-primary underline-offset-4 hover:underline",
      },
      size: {
        default: "h-10 px-4 py-2",
        sm: "h-9 rounded-md px-3",
        lg: "h-11 rounded-md px-8",
        icon: "h-10 w-10",
      },
    },
    defaultVariants: {
      variant: 'default',
      size: 'default',
    },
  }
)

type ButtonVariants = VariantProps<typeof buttonVariants>

interface Props {
  variant?: NonNullable<ButtonVariants['variant']>
  size?: NonNullable<ButtonVariants['size']>
  class?: string
  disabled?: boolean
}

const props = withDefaults(defineProps<Props>(), {
  variant: 'default',
  size: 'default',
  disabled: false,
})

const classes = computed(() =>
  cn(buttonVariants({ variant: props.variant, size: props.size }), props.class)
)
</script>

<template>
  <button :class="classes" :disabled="disabled">
    <slot />
  </button>
</template>
```

**Nuxt 3** (using @nuxt/ui):
```vue
<!-- Using UButton directly - no custom component needed -->
<template>
  <UButton 
    color="primary" 
    variant="solid" 
    size="xl"
    :to="'/signup'"
  >
    Get Started
  </UButton>
</template>
```

---

## State Management

### Local Component State

**React**:
```tsx
const [isOpen, setIsOpen] = useState(false)
const [count, setCount] = useState(0)

const toggle = () => setIsOpen(prev => !prev)
const increment = () => setCount(prev => prev + 1)
```

**Vue 3**:
```ts
const isOpen = ref(false)
const count = ref(0)

const toggle = () => (isOpen.value = !isOpen.value)
const increment = () => count.value++
```

**Nuxt 3** (same as Vue 3):
```ts
const isOpen = ref(false)
const count = ref(0)

const toggle = () => (isOpen.value = !isOpen.value)
const increment = () => count.value++
```

### Reactive Objects

**React**:
```tsx
const [form, setForm] = useState({
  name: '',
  email: '',
})

const updateField = (field: string, value: string) => {
  setForm(prev => ({ ...prev, [field]: value }))
}
```

**Vue 3 / Nuxt 3**:
```ts
const form = reactive({
  name: '',
  email: '',
})

const updateField = (field: string, value: string) => {
  form[field] = value
}
```

### Computed Values

**React**:
```tsx
const fullName = useMemo(() => `${firstName} ${lastName}`, [firstName, lastName])
```

**Vue 3 / Nuxt 3**:
```ts
const fullName = computed(() => `${firstName.value} ${lastName.value}`)
```

---

## Routing Integration

### React (React Router)

```tsx
import { Link, useLocation } from 'react-router-dom'

function Navigation() {
  const location = useLocation()
  
  return (
    <nav>
      <Link to="/" className={location.pathname === '/' ? 'active' : ''}>
        Home
      </Link>
      <Link to="/about">About</Link>
    </nav>
  )
}
```

### Vue 3 (Vue Router)

```vue
<script setup lang="ts">
import { useRoute, useRouter } from 'vue-router'

const route = useRoute()
const router = useRouter()

const isActive = (path: string) => route.path === path
</script>

<template>
  <nav>
    <router-link to="/" :class="{ active: isActive('/') }">Home</router-link>
    <router-link to="/about">About</router-link>
  </nav>
</template>
```

### Nuxt 3 (File-based Routing)

```vue
<script setup lang="ts">
const route = useRoute()
const router = useRouter()

const isActive = (path: string) => route.path === path
</script>

<template>
  <nav>
    <NuxtLink to="/" :class="{ active: isActive('/') }">Home</NuxtLink>
    <NuxtLink to="/about">About</NuxtLink>
  </nav>
</template>
```

**Nuxt Pages Structure**:
```
pages/
├── index.vue          # /
├── about.vue          # /about
├── blog/
│   ├── index.vue      # /blog
│   └── [slug].vue     # /blog/:slug
└── admin/
    └── layout.vue     # Layout for /admin/*
```

---

## Animation Implementation

### Page Load Animation

**React (Framer Motion)**:
```tsx
<motion.section
  initial={{ opacity: 0, y: 20 }}
  animate={{ opacity: 1, y: 0 }}
  transition={{ duration: 0.5, delay: 0.2 }}
>
  <h1>Welcome</h1>
</motion.section>
```

**Vue 3 (@vueuse/motion)**:
```vue
<section
  v-motion
  :initial="{ opacity: 0, y: 20 }"
  :enter="{ opacity: 1, y: 0 }"
  :duration="500"
  :delay="200"
>
  <h1>Welcome</h1>
</section>
```

**Nuxt 3 (@vueuse/motion)**:
```vue
<section
  v-motion
  :initial="{ opacity: 0, y: 20 }"
  :visible-once="{ opacity: 1, y: 0 }"
  :duration="500"
  :delay="200"
>
  <h1>Welcome</h1>
</section>
```

### Staggered Children Animation

**React**:
```tsx
<motion.ul
  initial="hidden"
  animate="show"
  variants={{
    hidden: {},
    show: {
      transition: {
        staggerChildren: 0.1
      }
    }
  }}
>
  <motion.li variants={{ hidden: { opacity: 0 }, show: { opacity: 1 } }}>
    Item 1
  </motion.li>
  <motion.li variants={{ hidden: { opacity: 0 }, show: { opacity: 1 } }}>
    Item 2
  </motion.li>
</motion.ul>
```

**Vue 3 / Nuxt 3**:
```vue
<ul
  v-motion
  :initial="{ opacity: 0 }"
  :visible-once="{ opacity: 1 }"
  :transition="{ stagger: 100 }"
>
  <li v-for="(item, index) in items" :key="index" v-motion>
    {{ item }}
  </li>
</ul>
```

### Hover Effects

**React**:
```tsx
<motion.button
  whileHover={{ scale: 1.05 }}
  whileTap={{ scale: 0.95 }}
>
  Click me
</motion.button>
```

**Vue 3 / Nuxt 3**:
```vue
<button
  v-motion
  :hovered="{ scale: 1.05 }"
  :tapped="{ scale: 0.95 }"
  @mouseenter="handleMouseEnter"
  @mouseleave="handleMouseLeave"
>
  Click me
</button>
```

---

## Performance Optimization

### Code Splitting

**React**:
```tsx
import { lazy, Suspense } from 'react'

const HeavyComponent = lazy(() => './HeavyComponent')

function App() {
  return (
    <Suspense fallback={<div>Loading...</div>}>
      <HeavyComponent />
    </Suspense>
  )
}
```

**Vue 3**:
```vue
<script setup lang="ts">
import { defineAsyncComponent } from 'vue'

const HeavyComponent = defineAsyncComponent(() =>
  import('./HeavyComponent.vue')
)
</script>

<template>
  <Suspense>
    <template #fallback><div>Loading...</div></template>
    <HeavyComponent />
  </Suspense>
</template>
```

**Nuxt 3** (Automatic):
```vue
<!-- Nuxt auto-splits components in pages/ -->
<!-- Use lazy hydration for heavy components -->
<ClientOnly>
  <HeavyComponent />
</ClientOnly>
```

### Image Optimization

**React**: Manual optimization or third-party libraries

**Next.js**:
```tsx
import Image from 'next/image'

<Image
  src="/hero.jpg"
  alt="Hero image"
  width={1200}
  height={600}
  priority
/>
```

**Nuxt 3**:
```vue
<NuxtImg
  src="/hero.jpg"
  alt="Hero image"
  width="1200"
  height="600"
  priority
/>
```

### Lazy Loading Routes

**React Router**:
```tsx
const About = lazy(() => import('./pages/About'))
```

**Vue Router**:
```ts
{
  path: '/about',
  component: () => import('./pages/About.vue')
}
```

**Nuxt 3**: Automatic route-based code splitting

---

## Common Patterns by Framework

### Hero Section Pattern

**React**:
```tsx
// components/Hero.tsx
'use client'
import { motion } from 'framer-motion'
import { Button } from '@/components/ui/button'
import { siteConfig } from '@/config/site'

export function Hero() {
  return (
    <section className="relative min-h-screen flex items-center justify-center overflow-hidden">
      {/* Background effects */}
      <div className="absolute inset-0 gradient-mesh grain" />
      
      <motion.div
        initial={{ opacity: 0, y: 30 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.8 }}
        className="relative z-10 text-center max-w-4xl mx-auto px-4"
      >
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.2 }}
          className="mb-4"
        >
          <Badge variant="secondary">{siteConfig.hero.badge}</Badge>
        </motion.div>
        
        <motion.h1
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.3 }}
          className="text-5xl md:text-7xl font-bold mb-6 whitespace-pre-line"
        >
          {siteConfig.hero.title}
        </motion.h1>
        
        <motion.p
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.4 }}
          className="text-xl text-muted-foreground mb-8 max-w-2xl mx-auto"
        >
          {siteConfig.hero.subtitle}
        </motion.p>
        
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.5 }}
          className="flex gap-4 justify-center"
        >
          <Button size="lg">{siteConfig.hero.cta.text}</Button>
          <Button variant="outline" size="lg">
            {siteConfig.hero.secondaryCta.text}
          </Button>
        </motion.div>
      </motion.div>
    </section>
  )
}
```

**Vue 3**:
```vue
<!-- components/Hero.vue -->
<script setup lang="ts">
import { siteConfig } from '@/config/site'
</script>

<template>
  <section class="relative min-h-screen flex items-center justify-center overflow-hidden">
    <!-- Background effects -->
    <div class="absolute inset-0 gradient-mesh grain" />
    
    <div
      v-motion
      :initial="{ opacity: 0, y: 30 }"
      :enter="{ opacity: 1, y: 0 }"
      :duration="800"
      class="relative z-10 text-center max-w-4xl mx-auto px-4"
    >
      <div
        v-motion
        :initial="{ opacity: 0 }"
        :enter="{ opacity: 1 }"
        :delay="200"
        class="mb-4"
      >
        <Badge variant="secondary">{{ siteConfig.hero.badge }}</Badge>
      </div>
      
      <h1
        v-motion
        :initial="{ opacity: 0, y: 20 }"
        :enter="{ opacity: 1, y: 0 }"
        :delay="300"
        class="text-5xl md:text-7xl font-bold mb-6 whitespace-pre-line"
      >
        {{ siteConfig.hero.title }}
      </h1>
      
      <p
        v-motion
        :initial="{ opacity: 0 }"
        :enter="{ opacity: 1 }"
        :delay="400"
        class="text-xl text-muted-foreground mb-8 max-w-2xl mx-auto"
      >
        {{ siteConfig.hero.subtitle }}
      </p>
      
      <div
        v-motion
        :initial="{ opacity: 0, y: 20 }"
        :enter="{ opacity: 1, y: 0 }"
        :delay="500"
        class="flex gap-4 justify-center"
      >
        <Button size="lg">{{ siteConfig.hero.cta.text }}</Button>
        <Button variant="outline" size="lg">
          {{ siteConfig.hero.secondaryCta.text }}
        </Button>
      </div>
    </div>
  </section>
</template>
```

**Nuxt 3**:
```vue
<!-- components/Hero.vue (auto-imported) -->
<script setup lang="ts">
import { siteConfig } from '~/config/site'

useHead({
  title: `${siteConfig.name} - ${siteConfig.tagline}`
})
</script>

<template>
  <section class="relative min-h-screen flex items-center justify-center overflow-hidden">
    <!-- Background effects -->
    <div class="absolute inset-0 gradient-mesh grain" />
    
    <div
      v-motion
      :initial="{ opacity: 0, y: 30 }"
      :visible-once="{ opacity: 1, y: 0 }"
      :duration="800"
      class="relative z-10 text-center max-w-4xl mx-auto px-4"
    >
      <div
        v-motion
        :initial="{ opacity: 0 }"
        :visible-once="{ opacity: 1 }"
        :delay="200"
        class="mb-4"
      >
        <UBadge variant="subtle">{{ siteConfig.hero.badge }}</UBadge>
      </div>
      
      <h1
        v-motion
        :initial="{ opacity: 0, y: 20 }"
        :visible-once="{ opacity: 1, y: 0 }"
        :delay="300"
        class="text-5xl md:text-7xl font-bold mb-6 whitespace-pre-line font-display"
      >
        {{ siteConfig.hero.title }}
      </h1>
      
      <p
        v-motion
        :initial="{ opacity: 0 }"
        :visible-once="{ opacity: 1 }"
        :delay="400"
        class="text-xl text-muted-foreground mb-8 max-w-2xl mx-auto"
      >
        {{ siteConfig.hero.subtitle }}
      </p>
      
      <div
        v-motion
        :initial="{ opacity: 0, y: 20 }"
        :visible-once="{ opacity: 1, y: 0 }"
        :delay="500"
        class="flex gap-4 justify-center"
      >
        <UButton size="xl" :to="siteConfig.hero.cta.href">
          {{ siteConfig.hero.cta.text }}
        </UButton>
        <UButton variant="outline" size="xl" :to="siteConfig.hero.secondaryCta.href">
          {{ siteConfig.hero.secondaryCta.text }}
        </UButton>
      </div>
    </div>
  </section>
</template>
```

### Feature Grid Pattern

**React**:
```tsx
// components/FeatureGrid.tsx
import { motion } from 'framer-motion'
import { Card, CardHeader, CardTitle, CardDescription } from '@/components/ui/card'

interface FeatureGridProps {
  features: Array<{
    icon: LucideIcon
    title: string
    description: string
  }>
}

export function FeatureGrid({ features }: FeatureGridProps) {
  return (
    <section className="py-24 px-4">
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8 max-w-6xl mx-auto">
        {features.map((feature, index) => (
          <motion.div
            key={feature.title}
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ delay: index * 0.1 }}
          >
            <Card className="h-full hover:shadow-lg transition-shadow">
              <CardHeader>
                <feature.icon className="w-8 h-8 mb-2 text-primary" />
                <CardTitle>{feature.title}</CardTitle>
                <CardDescription>{feature.description}</CardDescription>
              </CardHeader>
            </Card>
          </motion.div>
        ))}
      </div>
    </section>
  )
}
```

**Vue 3**:
```vue
<!-- components/FeatureGrid.vue -->
<script setup lang="ts">
interface Feature {
  icon: any
  title: string
  description: string
}

defineProps<{
  features: Feature[]
}>()
</script>

<template>
  <section class="py-24 px-4">
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8 max-w-6xl mx-auto">
      <div
        v-for="(feature, index) in features"
        :key="feature.title"
        v-motion
        :initial="{ opacity: 0, y: 20 }"
        :visible-once="{ opacity: 1, y: 0 }"
        :delay="index * 100"
      >
        <Card class="h-full hover:shadow-lg transition-shadow">
          <CardHeader>
            <component :is="feature.icon" class="w-8 h-8 mb-2 text-primary" />
            <CardTitle>{{ feature.title }}</CardTitle>
            <CardDescription>{{ feature.description }}</CardDescription>
          </CardHeader>
        </Card>
      </div>
    </div>
  </section>
</template>
```

**Nuxt 3**:
```vue
<!-- components/FeatureGrid.vue -->
<script setup lang="ts">
interface Feature {
  icon: string
  title: string
  description: string
}

defineProps<{
  features: Feature[]
}>()
</script>

<template>
  <section class="py-24 px-4">
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8 max-w-6xl mx-auto">
      <div
        v-for="(feature, index) in features"
        :key="feature.title"
        v-motion
        :initial="{ opacity: 0, y: 20 }"
        :visible-once="{ opacity: 1, y: 0 }"
        :delay="index * 100"
      >
        <UCard class="h-full hover:shadow-lg transition-shadow">
          <UIcon :name="feature.icon" class="w-8 h-8 mb-2 text-primary" />
          <h3 class="text-lg font-semibold mb-2">{{ feature.title }}</h3>
          <p class="text-muted-foreground">{{ feature.description }}</p>
        </UCard>
      </div>
    </div>
  </section>
</template>
```

---

## Migration Examples

### Converting a React Component to Vue 3

**Before (React)**:
```tsx
import { useState } from 'react'
import { motion } from 'framer-motion'

interface AccordionItemProps {
  title: string
  children: React.ReactNode
}

export function AccordionItem({ title, children }: AccordionItemProps) {
  const [isOpen, setIsOpen] = useState(false)

  return (
    <motion.div
      initial={false}
      animate={{ height: isOpen ? 'auto' : 0 }}
      className="overflow-hidden"
    >
      <button
        onClick={() => setIsOpen(!isOpen)}
        className="flex items-center justify-between w-full p-4 text-left"
      >
        <span>{title}</span>
        <ChevronDown className={`transform transition-transform ${isOpen ? 'rotate-180' : ''}`} />
      </button>
      {isOpen && <div className="p-4 pt-0">{children}</div>}
    </motion.div>
  )
}
```

**After (Vue 3)**:
```vue
<!-- AccordionItem.vue -->
<script setup lang="ts">
defineProps<{
  title: string
}>()

const isOpen = ref(false)

const toggle = () => {
  isOpen.value = !isOpen.value
}
</script>

<template>
  <div
    v-motion
    :initial="{ height: 0 }"
    :animate="{ height: isOpen ? 'auto' : 0 }"
    class="overflow-hidden"
  >
    <button
      @click="toggle"
      class="flex items-center justify-between w-full p-4 text-left"
    >
      <span>{{ title }}</span>
      <UIcon name="i-lucide-chevron-down" :class="['transform transition-transform', { 'rotate-180': isOpen }]" />
    </button>
    <div v-if="isOpen" class="p-4 pt-0">
      <slot />
    </div>
  </div>
</template>
```

### Converting Vue 3 to Nuxt 3

**Changes Required**:
1. Move file from `src/components/` to `components/`
2. Remove imports for auto-imported functions (ref, computed, etc.)
3. Change `@/` imports to `~/`
4. Replace `vue-router` usage with `<NuxtLink>` and `useRoute()`/`useRouter()`
5. Add SEO metadata with `useHead()` or `useSeoMeta()`
6. Use `@nuxt/image` for images instead of standard `<img>`

**Example**:
```vue
<!-- Before (Vue 3): src/components/Hero.vue -->
<script setup lang="ts">
import { ref } from 'vue'
import { useRoute } from 'vue-router'
import { siteConfig } from '@/config/site'

const route = useRoute()
</script>

<!-- After (Nuxt 3): components/Hero.vue -->
<script setup lang="ts">
// No need to import ref, useRoute - auto-imported!
import { siteConfig } from '~/config/site'

const route = useRoute()

useHead({
  title: `${siteConfig.name} - ${route.meta.title || 'Home'}`
})
</script>
```

---

## Best Practices

### Cross-Framework Do's ✅

✅ **Use composition patterns** that translate easily between frameworks  
✅ **Keep business logic separate** from framework-specific code  
✅ **Use TypeScript interfaces** shared across all implementations  
✅ **Implement consistent design tokens** (CSS variables)  
✅ **Follow mobile-first responsive design** universally  
✅ **Optimize performance** with lazy loading and code splitting  
✅ **Maintain accessibility standards** (WCAG AA) regardless of framework  

### Cross-Framework Don'ts ❌

❌ Don't mix framework-specific syntax in shared logic  
❌ Don't ignore framework conventions (e.g., using JSX patterns in Vue)  
❌ Don't skip framework-specific optimizations (e.g., Next.js image optimization)  
❌ Don't assume identical APIs exist across all libraries  
❌ Don't forget to test on all target frameworks before shipping  

---

## Troubleshooting

### Common Issues

**Issue**: Animations not working in Vue/Nuxt  
**Solution**: Ensure `@vueuse/motion` is properly installed and plugin is initialized

**Issue**: Path aliases not resolving  
**Solution**: Check `vite.config.ts` or `nuxt.config.ts` for correct alias configuration

**Issue**: Styles not applying consistently  
**Solution**: Verify Tailwind CSS is configured identically across all frameworks

**Issue**: Build errors after adding new dependencies  
**Solution**: Clear node_modules and reinstall: `rm -rf node_modules package-lock.json && npm install`

---

*This guide ensures consistent implementation quality across all supported frameworks while respecting each framework's idioms and best practices.*
