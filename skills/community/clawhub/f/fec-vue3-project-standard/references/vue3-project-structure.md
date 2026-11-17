# Vue 3 project structure and component standards

## Project structure

The following is the industry's best practice structure for medium and large Vue 3 projects, tailored according to the actual situation of the project:

```
src/
├── app/ # Application entry and global configuration
│ ├── App.vue # Root component
│ ├── main.ts # Application startup entrance
│ └── router.ts # Routing instance and configuration
│
├── pages/ # Page components (one-to-one correspondence with routing)
│   ├── Dashboard/
│   │   ├── DashboardPage.vue
│ │ ├── components/ # Page private components
│ │ └── composables/ # Page private composables
│   ├── UserList/
│   └── Settings/
│
├── layouts/ # Layout component
│ ├── MainLayout.vue # Main layout (sidebar + top bar + content area)
│ ├── AuthLayout.vue # Login/registration page layout
│ └── BlankLayout.vue # Blank layout (error page, etc.)
│
├── features/ # Function modules (divided by business areas)
│   ├── auth/
│ │ ├── components/ # Module components
│ │ ├── composables/ # module composables
│ │ ├── api.ts # Module API call
│ │ ├── types.ts # Module type definition
│ │ ├── constants.ts # Module constants
│ │ └── index.ts # Module publicly exported
│   └── order/
│
├── components/ # Globally shared UI components
│   ├── AppButton/
│   │   ├── AppButton.vue
│   │   └── __tests__/
│   ├── AppModal/
│   ├── AppForm/
│   └── AppErrorBoundary/
│
├── composables/ # Global shared composables
│   ├── useAuth.ts
│   ├── useDebounce.ts
│   └── useMediaQuery.ts
│
├── services/ # API base layer
│ ├── request.ts # Axios/fetch instance and interceptor
│ └── endpoints/ # API endpoint definition (such as split by field)
│
├── stores/ # Pinia status management
│   ├── authStore.ts
│   └── uiStore.ts
│
├── locales/ # International language pack
│ ├── zh-CN.json # Simplified Chinese
│ ├── en-US.json # English
│ └── index.ts # i18n instance initialization (vue-i18n)
│
├── assets/ # Static resources
│ ├── images/ # Pictures (PNG, JPG, WebP)
│ ├── icons/ # SVG icon
│ └── fonts/ # Custom fonts
│
├── config/ # Application configuration
│ ├── env.ts # Typed encapsulation of environment variables
│ └── features.ts # Feature Flags Management
│
├── types/ # Global shared types
│ ├── api.ts # API response/request common type
│ ├── models.ts #Business entity type
│ └── global.d.ts # Global type extension (component type, module declaration, etc.)
│
├── utils/ # Pure utility function
│ ├── format.ts # Date, number, currency formatting
│ ├── validators.ts # Form validation rules
│ └── storage.ts # LocalStorage / SessionStorage package
│
├── directives/ # Custom directives
│ ├── vPermission.ts # Permission command
│ └── vClickOutside.ts # Click outside to close
│
├── plugins/ # Vue plug-in registration
│ ├── i18n.ts # vue-i18n plug-in configuration
│ └── index.ts # Plug-in unified registration entrance
│
├── styles/ # Global styles and themes
│ ├── global.css # Global basic style (reset/normalize)
│ ├── variables.css # CSS variables (color, spacing, font size)
│ ├── breakpoints.ts # Responsive breakpoint constants
│ └── themes/ # theme definition
│ ├── light.css # Light theme variable
│ ├── dark.css # Dark theme variable
│ └── index.ts # theme switching logic
│
└── constants/ # Global constants
    ├── routes.ts #Routing path constants
    └── config.ts #Business constants (paging size, timeout, etc.)
```

### Key Principles

- `pages/` does route mapping and layout combination without putting business logic
- `layouts/` defines the page skeleton (sidebar, top bar, breadcrumbs), referenced by the `component` of the routing configuration
- `features/` is divided by business areas, self-contained within the module (components + composables + api + types)
- `components/` only contains common components without business coupling and can be reused across projects
- `composables/` only places common logic (anti-shake, media query, etc.), and business composables are placed in the corresponding feature
- `locales/` stores language pack JSON files, use `$t('key')` in the template instead of hard-coded copy
- `assets/` stores static resources, SVG is preferred for icons, and WebP/AVIF is preferred for images.
- `config/` encapsulates environment variables and Feature Flags, prohibiting direct reading of `import.meta.env` in components
- `styles/themes/` implements theme switching through CSS variables. Variables are referenced in components instead of hard-coded colors.
- Each module controls the public API through `index.ts` to avoid deep path imports

## Component design specifications

- Use `<script setup lang="ts">`
- Explicitly use `defineProps` / `defineEmits` with accompanying types
- Reusable logic is first extracted to composables
- Keep the template readable and avoid too deep nesting of conditions
- Prefer using computed properties instead of repeatedly maintaining state
- Avoid building large single components; **single file size** see `templates/shared/rules/fec-vue.md` "**component file size**" (approximately 300 lines or less, more than 500 lines or too complex to separate sub-components and Composables)
- Prioritize the use of strongly typed props, emits and exposed methods
- Follow the file and directory naming conventions of the warehouse
- Prioritize reuse of existing UI components and tokens

### Component layering

```
Pages → Route mapping, layout combination
  └── Container components (Containers) → Data acquisition, status orchestration
       └── Business components (Features) → Domain logic display
            └── Universal Component (UI) → Pure display, no business coupling
```

## Comment specifications

- **Prefer using Chinese**: When explaining "why this is done", business constraints, boundary conditions, and non-obvious trade-offs, give priority to writing comments in Chinese to make it easier for the team and business parties to read.
- **Exception when consistent with the code language**: When connecting third-party protocol field names, HTTP headers, and English terms in specifications, English proper nouns can be retained in the comments, and Chinese and English descriptions can be given when necessary.
- **Less but more precise**: Can express clear logic through clear naming and types without writing nonsense comments; complex branches, temporary compatibility, and performance trade-offs must be clearly stated.
- **Public API**: Composable or module external contracts can use JSDoc (`@param` / `@returns` / `@example`). The instructions can be in Chinese, unless the warehouse requires English.

## TypeScript Specification

Common TypeScript project rules are taken care of by `fec-typescript-project-standard`, including `tsconfig`, strictness, DTO / view model boundaries, `unknown` narrowing, public API types, declared artifacts, and type tests.

The Vue specification only supplements SFC, Props / Emits, exposed methods, Provide / Inject and composable reactive types; complex type modeling or cross-framework type contracts are first offloaded to `fec-typescript-project-standard`.

### Vue 3 project supplementary conventions

```vue
<script setup lang="ts">
interface Props {
  title: string;
  items: Item[];
  loading?: boolean;
}

interface Emits {
  (e: "select", item: Item): void;
  (e: "delete", id: string): void;
}

const props = withDefaults(defineProps<Props>(), {
  loading: false,
});

const emit = defineEmits<Emits>();
</script>
```

- Props and Emits are defined using the TypeScript interface
- Use `withDefaults` to set default values
- `defineExpose` exposed methods must have type constraints

