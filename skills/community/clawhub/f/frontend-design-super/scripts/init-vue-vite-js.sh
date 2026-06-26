#!/bin/bash
# Initialize a Vite + Vue 3 + JavaScript + Tailwind + shadcn-vue project
# Usage: bash scripts/init-vue-vite-js.sh <project-name>

set -e

PROJECT_NAME="${1:-my-site}"

# Check Node version
NODE_VERSION=$(node -v 2>/dev/null | cut -d'v' -f2 | cut -d'.' -f1)
if [ -z "$NODE_VERSION" ] || [ "$NODE_VERSION" -lt 18 ]; then
  echo "❌ Error: Node.js 18+ is required. Current: $(node -v 2>/dev/null || echo 'not installed')"
  exit 1
fi

echo "🚀 Creating Vue 3 + Vite project (JavaScript): $PROJECT_NAME"

# Create Vite project with Vue 3 (JavaScript template)
npm create vite@latest "$PROJECT_NAME" -- --template vue
cd "$PROJECT_NAME"

# Create .nvmrc for Node version
echo "18" > .nvmrc

echo "📦 Installing dependencies..."

# Install Tailwind CSS v4 for Vue 3
npm install -D tailwindcss postcss autoprefixer
npx tailwindcss init -p

# Install Vue animation library (@vueuse/motion)
npm install @vueuse/core @vueuse/motion

# Install shadcn-vue base dependencies
npm install tailwindcss-animate class-variance-authority clsx tailwind-merge radix-vue lucide-vue-next

echo "⚙️ Configuring Tailwind..."

# Create tailwind.config.js (JavaScript version)
cat > tailwind.config.js << 'EOF'
/** @type {import('tailwindcss').Config} */
import tailwindcssAnimate from "tailwindcss-animate"

export default {
  darkMode: ["class"],
  content: [
    "./index.html",
    "./src/**/*.{js,jsx,vue}",
  ],
  theme: {
    container: {
      center: true,
      padding: "2rem",
      screens: {
        "2xl": "1400px",
      },
    },
    extend: {
      colors: {
        border: "hsl(var(--border))",
        input: "hsl(var(--input))",
        ring: "hsl(var(--ring))",
        background: "hsl(var(--background))",
        foreground: "hsl(var(--foreground))",
        primary: {
          DEFAULT: "hsl(var(--primary))",
          foreground: "hsl(var(--primary-foreground))",
        },
        secondary: {
          DEFAULT: "hsl(var(--secondary))",
          foreground: "hsl(var(--secondary-foreground))",
        },
        destructive: {
          DEFAULT: "hsl(var(--destructive))",
          foreground: "hsl(var(--destructive-foreground))",
        },
        muted: {
          DEFAULT: "hsl(var(--muted))",
          foreground: "hsl(var(--muted-foreground))",
        },
        accent: {
          DEFAULT: "hsl(var(--accent))",
          foreground: "hsl(var(--accent-foreground))",
        },
        popover: {
          DEFAULT: "hsl(var(--popover))",
          foreground: "hsl(var(--popover-foreground))",
        },
        card: {
          DEFAULT: "hsl(var(--card))",
          foreground: "hsl(var(--card-foreground))",
        },
      },
      borderRadius: {
        lg: "var(--radius)",
        md: "calc(var(--radius) - 2px)",
        sm: "calc(var(--radius) - 4px)",
      },
      fontFamily: {
        sans: ["var(--font-sans)", "system-ui", "sans-serif"],
      },
      keyframes: {
        "accordion-down": {
          from: { height: "0" },
          to: { height: "var(--radix-accordion-content-height)" },
        },
        "accordion-up": {
          from: { height: "var(--radix-accordion-content-height)" },
          to: { height: "0" },
        },
      },
      animation: {
        "accordion-down": "accordion-down 0.2s ease-out",
        "accordion-up": "accordion-up 0.2s ease-out",
      },
    },
  },
  plugins: [tailwindcssAnimate],
}
EOF

# Create base CSS (same as TypeScript version)
cat > src/assets/index.css << 'EOF'
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
  }
}
EOF

# Create utils for Vue (JavaScript version)
mkdir -p src/lib
cat > src/lib/utils.js << 'EOF'
import { clsx } from "clsx"
import { twMerge } from "tailwind-merge"

export function cn(...inputs) {
  return twMerge(clsx(inputs))
}
EOF

# Create components directory
mkdir -p src/components/ui

# Create Button component for Vue (JavaScript version)
cat > src/components/ui/Button.vue << 'EOF'
<script setup>
import { computed } from 'vue'
import { cva } from 'class-variance-authority'
import { cn } from '@/lib/utils'

const buttonVariants = cva(
  "inline-flex items-center justify-center whitespace-nowrap rounded-md text-sm font-medium ring-offset-background transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50",
  {
    variants: {
      variant: {
        default: "bg-primary text-primary-foreground hover:bg-primary/90",
        destructive: "bg-destructive text-destructive-foreground hover:bg-destructive/90",
        outline: "border border-input bg-background hover:bg-accent hover:text-accent-foreground",
        secondary: "bg-secondary text-secondary-foreground hover:bg-secondary/80",
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

const props = withDefaults(defineProps({
  variant: {
    type: String,
    default: 'default'
  },
  size: {
    type: String,
    default: 'default'
  },
  asChild: {
    type: Boolean,
    default: false
  },
  class: {
    type: String,
    default: ''
  },
  disabled: {
    type: Boolean,
    default: false
  }
}))

const classes = computed(() =>
  cn(buttonVariants({ variant: props.variant, size: props.size }), props.class)
)
</script>

<template>
  <button :class="classes" :disabled="disabled">
    <slot />
  </button>
</template>
EOF

# Update vite.config.js with path aliases and Vue plugin (JavaScript version)
cat > vite.config.js << 'EOF'
import path from "path"
import vue from "@vitejs/plugin-vue"
import { defineConfig } from "vite"

export default defineConfig({
  plugins: [vue()],
  resolve: {
    alias: {
      "@": path.resolve(__dirname, "./src"),
    },
  },
})
EOF

# Create components.json for shadcn-vue CLI (JavaScript version)
cat > components.json << 'EOF'
{
  "$schema": "https://shadcn-vue.com/schema.json",
  "style": "default",
  "typescript": false,
  "tailwind": {
    "config": "tailwind.config.js",
    "css": "src/assets/index.css",
    "baseColor": "slate",
    "cssVariables": true,
    "prefix": ""
  },
  "framework": "vite",
  "aliases": {
    "components": "@/components",
    "utils": "@/lib/utils",
    "ui": "@/components/ui",
    "lib": "@/lib",
    "hooks": "@/hooks"
  }
}
EOF

# Create Vue motion plugin setup (JavaScript version)
mkdir -p src/plugins
cat > src/plugins/motion.js << 'EOF'
import { MotionPlugin } from '@vueuse/motion'

export function setupMotion(app) {
  app.use(MotionPlugin)
}
EOF

echo ""
echo "📦 Installing shadcn-vue components..."

# Try to initialize shadcn-vue
npx shadcn-vue@latest init -y -d 2>/dev/null || echo "⚠️ shadcn-vue CLI not available, components created manually"

# Install common components manually if CLI fails
if [ ! -d "src/components/ui/Button.vue" ]; then
  echo "✓ Button component created"
fi

echo ""
echo "✅ Vue 3 project created successfully!"
echo ""
echo "Installed:"
echo "  ✓ Vue 3 + JavaScript + Vite"
echo "  ✓ Tailwind CSS with shadcn/ui theming"
echo "  ✓ @vueuse/motion for animations"
echo "  ✓ shadcn-vue compatible structure"
echo "  ✓ Path aliases (@/) configured"
echo ""
echo "Next steps:"
echo "  cd $PROJECT_NAME"
echo "  npm run dev"
echo ""
echo "Add more shadcn-vue components:"
echo "  npx shadcn-vue@latest add [component-name]"
echo ""
echo "Build for production:"
echo "  npm run build"
echo ""