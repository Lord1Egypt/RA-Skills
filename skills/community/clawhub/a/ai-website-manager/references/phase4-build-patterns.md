# Phase 4: Build Patterns & Code Conventions

Common patterns for building site sections, connecting Sanity, and structuring components.
Use these as starting templates — adapt to the user's design references.

## Table of Contents
1. [Section Building Order](#section-building-order)
2. [Sanity Schema Patterns](#sanity-schema-patterns)
3. [Component Templates](#component-templates)
4. [Animation Patterns](#animation-patterns)
5. [Image Handling](#image-handling)
6. [RTL Support](#rtl-support)

---

## Section Building Order

Build in this order — it keeps the user motivated (they see progress fast):

1. **Layout** (Navbar + Footer) — frame the site
2. **Hero Section** — the first thing visitors see; makes the biggest impression
3. **About / Bio Section** — who is this person/company
4. **Work / Portfolio / Services** — the main content
5. **Contact Section** — call to action
6. Additional pages as needed

After each section:
- Commit to GitHub
- Push to Vercel
- Show the user the live URL

---

## Sanity Schema Patterns

### Site Settings Schema (global config)
```ts
// src/sanity/schemas/siteSettings.ts
import { defineField, defineType } from 'sanity'

export default defineType({
  name: 'siteSettings',
  title: 'Site Settings',
  type: 'document',
  fields: [
    defineField({ name: 'siteName', title: 'Site Name', type: 'string' }),
    defineField({ name: 'tagline', title: 'Tagline', type: 'string' }),
    defineField({ name: 'email', title: 'Contact Email', type: 'string' }),
    defineField({ name: 'logo', title: 'Logo', type: 'image' }),
  ],
})
```

### Hero Section Schema
```ts
// src/sanity/schemas/hero.ts
export default defineType({
  name: 'hero',
  title: 'Hero Section',
  type: 'document',
  fields: [
    defineField({ name: 'headline', title: 'Main Headline', type: 'string' }),
    defineField({ name: 'subheadline', title: 'Sub-headline', type: 'text' }),
    defineField({ name: 'ctaLabel', title: 'Button Text', type: 'string' }),
    defineField({ name: 'ctaLink', title: 'Button Link', type: 'string' }),
    defineField({ name: 'image', title: 'Hero Image', type: 'image', options: { hotspot: true } }),
  ],
})
```

### Portfolio / Case Study Schema
```ts
// src/sanity/schemas/project.ts
export default defineType({
  name: 'project',
  title: 'Project',
  type: 'document',
  fields: [
    defineField({ name: 'title', title: 'Project Title', type: 'string' }),
    defineField({ name: 'slug', title: 'Slug', type: 'slug', options: { source: 'title' } }),
    defineField({ name: 'description', title: 'Description', type: 'text' }),
    defineField({ name: 'image', title: 'Cover Image', type: 'image', options: { hotspot: true } }),
    defineField({ name: 'tags', title: 'Tags', type: 'array', of: [{ type: 'string' }] }),
    defineField({ name: 'url', title: 'Live URL', type: 'url' }),
    defineField({ name: 'publishedAt', title: 'Published At', type: 'datetime' }),
    defineField({ name: 'order', title: 'Display Order', type: 'number' }),
  ],
  orderings: [{ title: 'Display Order', name: 'orderAsc', by: [{ field: 'order', direction: 'asc' }] }],
})
```

### Sanity Client Setup
```ts
// src/sanity/lib/client.ts
import { createClient } from 'next-sanity'

export const client = createClient({
  projectId: process.env.NEXT_PUBLIC_SANITY_PROJECT_ID!,
  dataset: process.env.NEXT_PUBLIC_SANITY_DATASET || 'production',
  apiVersion: '2024-01-01',
  useCdn: false,
})
```

### Fetching Data
```ts
// src/sanity/lib/queries.ts
import { client } from './client'
import imageUrlBuilder from '@sanity/image-url'

const builder = imageUrlBuilder(client)

export function urlFor(source: any) {
  return builder.image(source)
}

export async function getHero() {
  return client.fetch(`*[_type == "hero"][0]`)
}

export async function getProjects() {
  return client.fetch(`*[_type == "project"] | order(order asc)`)
}
```

---

## Component Templates

### Hero Section Component
```tsx
// src/components/HeroSection.tsx
'use client'
import { motion } from 'framer-motion'

interface HeroProps {
  headline: string
  subheadline: string
  ctaLabel: string
  ctaLink: string
}

export default function HeroSection({ headline, subheadline, ctaLabel, ctaLink }: HeroProps) {
  return (
    <section className="min-h-screen flex items-center justify-center bg-[#0a0a0a] px-6">
      <div className="max-w-4xl mx-auto text-center">
        <motion.h1
          className="text-5xl md:text-7xl font-bold text-white mb-6 leading-tight"
          initial={{ opacity: 0, y: 30 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6 }}
        >
          {headline}
        </motion.h1>
        <motion.p
          className="text-xl text-gray-400 mb-10 max-w-2xl mx-auto"
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 0.2 }}
        >
          {subheadline}
        </motion.p>
        <motion.a
          href={ctaLink}
          className="inline-block bg-[#DD9933] text-white px-8 py-4 rounded-full text-lg font-semibold hover:opacity-90 transition-opacity"
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 0.4 }}
        >
          {ctaLabel}
        </motion.a>
      </div>
    </section>
  )
}
```

### Navbar Component
```tsx
// src/components/Navbar.tsx
'use client'
import { useState } from 'react'
import Link from 'next/link'

const navLinks = [
  { label: 'About', href: '#about' },
  { label: 'Work', href: '#work' },
  { label: 'Contact', href: '#contact' },
]

export default function Navbar({ siteName }: { siteName: string }) {
  const [isOpen, setIsOpen] = useState(false)

  return (
    <nav className="fixed top-0 left-0 right-0 z-50 bg-[#0a0a0a]/80 backdrop-blur-md border-b border-white/10">
      <div className="max-w-6xl mx-auto px-6 h-16 flex items-center justify-between">
        <Link href="/" className="text-white font-bold text-xl">{siteName}</Link>
        <div className="hidden md:flex items-center gap-8">
          {navLinks.map(link => (
            <Link key={link.href} href={link.href} className="text-gray-300 hover:text-white transition-colors">
              {link.label}
            </Link>
          ))}
        </div>
      </div>
    </nav>
  )
}
```

### Page Layout (fetches from Sanity)
```tsx
// src/app/page.tsx
import { getHero, getProjects } from '@/sanity/lib/queries'
import HeroSection from '@/components/HeroSection'

export default async function HomePage() {
  const [hero, projects] = await Promise.all([getHero(), getProjects()])

  return (
    <main>
      <HeroSection
        headline={hero?.headline ?? 'Welcome'}
        subheadline={hero?.subheadline ?? ''}
        ctaLabel={hero?.ctaLabel ?? 'Get in touch'}
        ctaLink={hero?.ctaLink ?? '#contact'}
      />
      {/* Add more sections here */}
    </main>
  )
}
```

---

## Animation Patterns

Use Framer Motion for all animations. Keep them subtle — they should enhance, not distract.

### Fade In on Scroll
```tsx
import { motion } from 'framer-motion'
import { useInView } from 'framer-motion'
import { useRef } from 'react'

function AnimatedSection({ children }: { children: React.ReactNode }) {
  const ref = useRef(null)
  const isInView = useInView(ref, { once: true, margin: '-100px' })

  return (
    <motion.div
      ref={ref}
      initial={{ opacity: 0, y: 40 }}
      animate={isInView ? { opacity: 1, y: 0 } : {}}
      transition={{ duration: 0.6, ease: 'easeOut' }}
    >
      {children}
    </motion.div>
  )
}
```

### Stagger Children (for grids/lists)
```tsx
const container = {
  hidden: { opacity: 0 },
  show: {
    opacity: 1,
    transition: { staggerChildren: 0.1 }
  }
}

const item = {
  hidden: { opacity: 0, y: 20 },
  show: { opacity: 1, y: 0 }
}

// Usage:
<motion.div variants={container} initial="hidden" animate="show">
  {projects.map(p => (
    <motion.div key={p._id} variants={item}>
      <ProjectCard project={p} />
    </motion.div>
  ))}
</motion.div>
```

---

## Image Handling

### From Sanity
```tsx
import { urlFor } from '@/sanity/lib/queries'
import Image from 'next/image'

// In component:
<Image
  src={urlFor(project.image).width(800).url()}
  alt={project.title}
  width={800}
  height={600}
  className="w-full h-full object-cover"
/>
```

### From Public Folder
```tsx
import Image from 'next/image'
import logo from '../../public/logo.png'

<Image src={logo} alt="Logo" width={120} height={40} />
```

### next.config.ts — Allow Sanity Images
```ts
const nextConfig = {
  images: {
    remotePatterns: [
      {
        protocol: 'https',
        hostname: 'cdn.sanity.io',
      },
    ],
  },
}

export default nextConfig
```

---

## RTL Support

### Global RTL
```tsx
// src/app/layout.tsx
<html lang="he" dir="rtl">
  <body className="font-[Heebo]">
```

### Loading Hebrew Font
```tsx
// src/app/layout.tsx
import { Heebo } from 'next/font/google'

const heebo = Heebo({
  subsets: ['hebrew', 'latin'],
  weight: ['400', '500', '700', '900'],
  variable: '--font-heebo',
})

<html lang="he" dir="rtl" className={heebo.variable}>
```

### Bilingual Layout Trick
For sections that need to flip alignment:
```tsx
// For RTL sections
<div className="text-right" dir="rtl">

// For LTR sections inside RTL page
<div className="text-left" dir="ltr">
```

### Common RTL Gotchas
- Flexbox `flex-row` becomes reversed in RTL — use `flex-row-reverse` if needed to fix visual order
- `ml-4` (margin-left) becomes visually right in RTL — prefer `mx-4` or logical properties
- Icons that point directions (arrows) may need to be flipped: `transform scale-x-[-1]`
- Code blocks and URLs should always be `dir="ltr"` even on RTL pages
