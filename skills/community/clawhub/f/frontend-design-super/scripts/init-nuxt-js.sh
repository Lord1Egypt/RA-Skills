#!/bin/bash
# Initialize a Nuxt 3 + JavaScript + Tailwind + @nuxt/ui project
# Usage: bash scripts/init-nuxt-js.sh <project-name>

set -e

PROJECT_NAME="${1:-my-site}"

# Check Node version
NODE_VERSION=$(node -v 2>/dev/null | cut -d'v' -f2 | cut -d'.' -f1)
if [ -z "$NODE_VERSION" ] || [ "$NODE_VERSION" -lt 18 ]; then
  echo "❌ Error: Node.js 18+ is required. Current: $(node -v 2>/dev/null || echo 'not installed')"
  exit 1
fi

echo "🚀 Creating Nuxt 3 project (JavaScript): $PROJECT_NAME"

# Create Nuxt 3 project
npx nuxi@latest init "$PROJECT_NAME"
cd "$PROJECT_NAME"

# Create .nvmrc for Node version
echo "18" > .nvmrc

echo "📦 Installing dependencies..."

# Install Tailwind CSS module for Nuxt
npm install @nuxtjs/tailwindcss

# Install @nuxt/ui (Nuxt's shadcn/ui equivalent)
npm install @nuxt/ui

# Install animation library (@vueuse/motion works with Nuxt)
npm install @vueuse/core @vueuse/motion

echo "⚙️ Configuring Nuxt..."

# Update nuxt.config.js with all modules (JavaScript version)
cat > nuxt.config.js << 'EOF'
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
  },

  app: {
    head: {
      link: [
        {
          rel: 'preconnect',
          href: 'https://fonts.googleapis.com'
        },
        {
          rel: 'preconnect',
          href: 'https://fonts.gstatic.com',
          crossorigin: ''
        },
        {
          rel: 'stylesheet',
          href: 'https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700&family=Space+Grotesk:wght@500;600;700&display=swap'
        }
      ]
    }
  }
})
EOF

# Create Tailwind config with custom theme (JavaScript version)
cat > tailwind.config.js << 'EOF'
/** @type {import('tailwindcss').Config} */
export default {
  content: [
    './components/**/*.{js,vue}',
    './layouts/**/*.vue',
    './pages/**/*.vue',
    './plugins/**/*.{js}',
    './app.vue',
    './error.vue'
  ],
  darkMode: 'class',
  theme: {
    extend: {
      colors: {
        border: 'hsl(var(--border))',
        input: 'hsl(var(--input))',
        ring: 'hsl(var(--ring))',
        background: 'hsl(var(--background))',
        foreground: 'hsl(var(--foreground))',
        primary: {
          DEFAULT: 'hsl(var(--primary))',
          foreground: 'hsl(var(--primary-foreground))'
        },
        secondary: {
          DEFAULT: 'hsl(var(--secondary))',
          foreground: 'hsl(var(--secondary-foreground))'
        },
        destructive: {
          DEFAULT: 'hsl(var(--destructive))',
          foreground: 'hsl(var(--destructive-foreground))'
        },
        muted: {
          DEFAULT: 'hsl(var(--muted))',
          foreground: 'hsl(var(--muted-foreground))'
        },
        accent: {
          DEFAULT: 'hsl(var(--accent))',
          foreground: 'hsl(var(--accent-foreground))'
        },
        popover: {
          DEFAULT: 'hsl(var(--popover))',
          foreground: 'hsl(var(--popover-foreground))'
        },
        card: {
          DEFAULT: 'hsl(var(--card))',
          foreground: 'hsl(var(--card-foreground))'
        }
      },
      borderRadius: {
        lg: 'var(--radius)',
        md: 'calc(var(--radius) - 2px)',
        sm: 'calc(var(--radius) - 4px)'
      },
      fontFamily: {
        sans: ['var(--font-sans)', 'system-ui', 'sans-serif'],
        display: ['var(--font-display)', 'system-ui', 'sans-serif']
      },
      keyframes: {
        'accordion-down': {
          from: { height: '0' },
          to: { height: 'var(--radix-accordion-content-height)' }
        },
        'accordion-up': {
          from: { height: 'var(--radix-accordion-content-height)' },
          to: { height: '0' }
        },
        'fade-in': {
          from: { opacity: '0' },
          to: { opacity: '1' }
        },
        'slide-up': {
          from: {
            opacity: '0',
            transform: 'translateY(20px)'
          },
          to: {
            opacity: '1',
            transform: 'translateY(0)'
          }
        }
      },
      animation: {
        'accordion-down': 'accordion-down 0.2s ease-out',
        'accordion-up': 'accordion-up 0.2s ease-out',
        'fade-in': 'fade-in 0.5s ease-out',
        'slide-up': 'slide-up 0.5s ease-out'
      }
    }
  },
  plugins: []
}
EOF

# Create global CSS with design system variables (same as TypeScript version)
mkdir -p assets/css
cat > assets/css/main.css << 'EOF'
@tailwind base;
@tailwind components;
@tailwind utilities;

@layer base {
  :root {
    --background: 0 0% 100%;
    --foreground: 222.2 84% 4.9%;
    --card: 0 0% 100%;
    --card-foreground: 222.2 84% 4.9%;
    --popover: 0 0% 100%;
    --popover-foreground: 222.2 84% 4.9%;
    --primary: 222.2 47.4% 11.2%;
    --primary-foreground: 210 40% 98%;
    --secondary: 210 40% 96.1%;
    --secondary-foreground: 222.2 47.4% 11.2%;
    --muted: 210 40% 96.1%;
    --muted-foreground: 215.4 16.3% 46.9%;
    --accent: 210 40% 96.1%;
    --accent-foreground: 222.2 47.4% 11.2%;
    --destructive: 0 84.2% 60.2%;
    --destructive-foreground: 210 40% 98%;
    --border: 214.3 31.8% 91.4%;
    --input: 214.3 31.8% 91.4%;
    --ring: 222.2 84% 4.9%;
    --radius: 0.5rem;
    
    /* Custom font families */
    --font-sans: 'Plus Jakarta Sans', system-ui, sans-serif;
    --font-display: 'Space Grotesk', system-ui, sans-serif;
  }

  .dark {
    --background: 222.2 84% 4.9%;
    --foreground: 210 40% 98%;
    --card: 222.2 84% 4.9%;
    --card-foreground: 210 40% 98%;
    --popover: 222.2 84% 4.9%;
    --popover-foreground: 210 40% 98%;
    --primary: 210 40% 98%;
    --primary-foreground: 222.2 47.4% 11.2%;
    --secondary: 217.2 32.6% 17.5%;
    --secondary-foreground: 210 40% 98%;
    --muted: 217.2 32.6% 17.5%;
    --muted-foreground: 215 20.2% 65.1%;
    --accent: 217.2 32.6% 17.5%;
    --accent-foreground: 210 40% 98%;
    --destructive: 0 62.8% 30.6%;
    --destructive-foreground: 210 40% 98%;
    --border: 217.2 32.6% 17.5%;
    --input: 217.2 32.6% 17.5%;
    --ring: 212.7 26.8% 83.9%;
  }
}

@layer base {
  * {
    @apply border-border;
  }

  body {
    @apply bg-background text-foreground;
    font-family: var(--font-sans);
  }
  
  h1, h2, h3, h4, h5, h6 {
    font-family: var(--font-display);
  }
}

/* Staggered animations */
.stagger-1 { animation-delay: 0.1s; }
.stagger-2 { animation-delay: 0.2s; }
.stagger-3 { animation-delay: 0.3s; }
.stagger-4 { animation-delay: 0.4s; }
.stagger-5 { animation-delay: 0.5s; }

/* Grain texture overlay */
.grain::before {
  content: '';
  position: fixed;
  inset: 0;
  background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 400 400' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noiseFilter'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noiseFilter)'/%3E%3C/svg%3E");
  opacity: 0.03;
  pointer-events: none;
  z-index: 1000;
}
EOF

# Create site configuration (JavaScript version)
mkdir -p config
cat > config/site.js << 'EOF'
export const siteConfig = {
  name: 'My Site',
  tagline: 'Build something amazing',
  description: 'A modern website built with Nuxt 3, Tailwind, and @nuxt/ui',
  url: 'https://mysite.com',

  nav: {
    links: [
      { label: 'Features', href: '#features' },
      { label: 'Pricing', href: '#pricing' },
      { label: 'FAQ', href: '#faq' }
    ],
    cta: { label: 'Get Started', href: '/signup' }
  },

  hero: {
    badge: 'Now in beta',
    title: 'Your words,\nsupercharged',
    subtitle: 'Write 10x faster with AI that understands your style',
    cta: { text: 'Get Started', href: '/signup' },
    secondaryCta: { text: 'Watch Demo', href: '#demo' }
  },

  features: [
    {
      icon: 'Zap',
      title: 'Lightning Fast',
      description: 'Blazing fast performance with optimized builds and smart caching'
    },
    {
      icon: 'Shield',
      title: 'Secure by Default',
      description: 'Enterprise-grade security with end-to-end encryption'
    },
    {
      icon: 'Globe',
      title: 'Global Scale',
      description: 'Deploy worldwide with automatic edge scaling'
    }
  ],

  pricing: [
    {
      name: 'Free',
      price: 0,
      features: ['Basic features', 'Community support', '1 project']
    },
    {
      name: 'Pro',
      price: 19,
      popular: true,
      features: ['Advanced features', 'Priority support', 'Unlimited projects', 'API access']
    },
    {
      name: 'Enterprise',
      price: 49,
      features: ['Custom solutions', 'Dedicated support', 'SLA guarantee', 'Custom integrations']
    }
  ],

  faq: [
    {
      q: 'How does it work?',
      a: 'Simply describe what you want to build and our AI will generate production-ready code.'
    },
    {
      q: 'What frameworks are supported?',
      a: 'We support React, Vue 3, and Nuxt 3 with consistent design patterns across all frameworks.'
    },
    {
      q: 'Can I customize the output?',
      a: 'Yes! All generated code is fully customizable and follows best practices.'
    }
  ]
}
EOF

# Create composables directory with motion composable (JavaScript version)
mkdir -p composables
cat > composables/useMotion.js << 'EOF'
import { useMotion } from '@vueuse/motion'

export function usePageTransition() {
  return {
    fadeIn: {
      initial: { opacity: 0 },
      enter: { opacity: 1 }
    },
    slideUp: {
      initial: { opacity: 0, y: 20 },
      enter: { opacity: 1, y: 0 }
    },
    staggerChildren: {
      initial: {},
      enter: {
        transition: {
          staggerChildren: 0.1
        }
      }
    }
  }
}
EOF

# Create a basic page with animations (JavaScript version)
mkdir -p pages
cat > pages/index.vue << 'EOF'
<script setup>
import { siteConfig } from '~/config/site'

useHead({
  title: siteConfig.name,
  meta: [
    { name: 'description', content: siteConfig.description }
  ]
})
</script>

<template>
  <div class="min-h-screen flex flex-col items-center justify-center p-24">
    <h1 class="text-5xl font-bold mb-4 animate-slide-up font-display">
      {{ siteConfig.name }}
    </h1>
    <p class="text-xl text-muted-foreground mb-8 animate-slide-up stagger-1">
      {{ siteConfig.tagline }}
    </p>
    <UButton size="xl" class="animate-slide-up stagger-2">
      Get Started
    </UButton>
  </div>
</template>
EOF

# Create app.vue with global layout structure (JavaScript version)
cat > app.vue << 'EOF'
<script setup>
const colorMode = useColorMode()
</script>

<template>
  <div :class="{ 'dark': colorMode.preference === 'dark' }" class="grain">
    <NuxtLoadingIndicator />
    <NuxtLayout>
      <NuxtPage />
    </NuxtLayout>

    <!-- Motion plugin will be auto-imported by Nuxt -->
    <UNotifications />
  </div>
</template>
EOF

# Create layouts/default.vue (JavaScript version)
mkdir -p layouts
cat > layouts/default.vue << 'EOF'
<script setup>
import { siteConfig } from '~/config/site'
</script>

<template>
  <div class="min-h-screen bg-background text-foreground">
    <header class="sticky top-0 z-50 w-full border-b border-border/40 bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60">
      <div class="container mx-auto px-4 py-4">
        <nav class="flex items-center justify-between">
          <a href="/" class="text-2xl font-bold font-display">{{ siteConfig.name }}</a>

          <div class="hidden md:flex items-center gap-6">
            <a
              v-for="link in siteConfig.nav.links"
              :key="link.label"
              :href="link.href"
              class="text-sm text-muted-foreground hover:text-foreground transition-colors"
            >
              {{ link.label }}
            </a>
          </div>

          <UButton :label="siteConfig.nav.cta.label" :to="siteConfig.nav.cta.href" />
        </nav>
      </div>
    </header>

    <main>
      <slot />
    </main>
  </div>
</template>
EOF

# Update package.json with scripts
npm pkg set scripts.dev="nuxt dev"
npm pkg set scripts.build="nuxt build"
npm pkg set scripts.generate="nuxt generate"

echo ""
echo "✅ Nuxt 3 project created successfully!"
echo ""
echo "Installed:"
echo "  ✓ Nuxt 3 with JavaScript"
echo "  ✓ Tailwind CSS v3"
echo "  ✓ @nuxt/ui (shadcn/ui for Nuxt)"
echo "  ✓ @vueuse/motion for animations"
echo "  ✓ Site config pattern"
echo "  ✓ Auto-imports configured"
echo ""
echo "Next steps:"
echo "  cd $PROJECT_NAME"
echo "  npm run dev"
echo ""
echo "Available @nuxt/ui components:"
echo "  UButton, UCard, UBadge, UAccordion, UModal, UNavigationMenu,"
echo "  UTabs, USheet, USeparator, UAvatar, UAlert, and more..."
echo ""
echo "Build for static deployment:"
echo "  npm run generate"
echo ""
echo "Deploy to Vercel/Netlify:"
echo "  npx nuxi deploy"
echo ""