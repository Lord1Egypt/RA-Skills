# React project structure and component boundaries

## Project structure (recommended reference)

The following is the industry's best practice structure for medium and large React projects, tailored according to the actual situation of the project:

```text
src/
├── app/ # Application entry and global configuration
│ ├── App.tsx # Root component (Provider combination)
│ ├── routes.tsx # Routing configuration
│ └── providers.tsx # Global Provider assembly
│
├── pages/ # Page components (one-to-one correspondence with routing)
│   ├── Dashboard/
│   │   ├── DashboardPage.tsx
│ │ ├── components/ # Page private components
│ │ └── hooks/ # Page private hooks
│   ├── UserList/
│   └── Settings/
│
├── layouts/ # Layout component
│ ├── MainLayout.tsx # Main layout (sidebar + top bar + content area)
│ ├── AuthLayout.tsx # Login/registration page layout
│ └── BlankLayout.tsx # Blank layout (error page, etc.)
│
├── features/ # Function modules (divided by business areas)
│   ├── auth/
│ │ ├── components/ # Module components
│ │ ├── hooks/ # module hooks
│ │ ├── api.ts # Module API call
│ │ ├── types.ts # Module type definition
│ │ ├── constants.ts # Module constants
│ │ └── index.ts # Module publicly exported
│   └── order/
│
├── components/ # Globally shared UI components
│   ├── Button/
│   │   ├── Button.tsx
│   │   ├── Button.styles.css
│   │   └── __tests__/
│   ├── Modal/
│   ├── Form/
│ └── ErrorBoundary/ # Thin wrapper (function component) for react-error-boundary etc.
│
├── hooks/ # Global shared hooks
│   ├── useAuth.ts
│   ├── useDebounce.ts
│   └── useMediaQuery.ts
│
├── services/ # API base layer
│ ├── request.ts # Axios/fetch instance and interceptor
│ └── endpoints/ # API endpoint definition (such as split by field)
│
├── stores/ # Global status management
│   ├── authStore.ts
│   └── uiStore.ts
│
├── locales/ # International language pack
│ ├── zh-CN.json # Simplified Chinese
│ ├── en-US.json # English
│ └── index.ts # i18n instance initialization (i18next / react-intl)
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
│ └── global.d.ts # Global type extension (picture module declaration, etc.)
│
├── utils/ # Pure utility function
│ ├── format.ts # Date, number, currency formatting
│ ├── validators.ts # Form validation rules
│ └── storage.ts # LocalStorage / SessionStorage package
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

- `pages/` does route mapping and page arrangement, and does not carry large pieces of reusable business logic.
- `layouts/` is responsible for the page skeleton and layout container, referenced by the routing configuration
- `features/` is divided according to business areas, and the module should be as self-contained as possible
- `components/` only contains common components that are reused across pages and modules
- `hooks/` only puts global general hooks; business hooks are put back to the corresponding feature or page first
- `locales/` stores language pack JSON files, use `t('key')` in the component instead of hard-coded copy
- `assets/` stores static resources, SVG is preferred for icons, and WebP/AVIF is preferred for images.
- `services/` is responsible for requesting infrastructure and does not stack business details
- `config/` uniformly encapsulates environment variables and feature switches, prohibiting direct reading of `import.meta.env` in components
- `styles/` and theme variables are managed uniformly to avoid colors and sizes being scattered in business code
- Each module controls the public API through `index.ts` to avoid deep path imports

---

## Component and module layering

Recommended layering:

```text
Page components (Pages) → route mapping, layout combination, page arrangement
  └── Container/orchestration layer → data acquisition, status organization, event orchestration
       └── Business components → Domain logic display
            └── Common components → No business coupling, reusable across modules
```

### When to put it in `pages/`

Suitable for:

- Routing entry component
- Page level layout combination
- Page private lightweight orchestration logic

Not suitable for:

- A lot of domain logic
- Complex business blocks that can be reused on multiple pages
- API/hooks/types that are strongly bound to a certain business domain

### When to put it in `features/`

Suitable for:

- Components, hooks, apis, and types of a certain business domain
- Logic that can be shared by multiple pages but has business semantics
- Self-contained implementation of a complete business unit

### When to put it in `components/`

Suitable for:

- Common UI such as buttons, pop-up windows, form items, table shells, empty states, error states, etc.
- Components that have nothing to do with specific business and can be reused across modules

---

## Component design specifications

- Use **Functional Components**, Hooks and TypeScript; **Do not** add new class components (Error Boundary uses libraries such as `react-error-boundary`, see below)
- **Single file size** and splitting principles can be found in `templates/shared/rules/fec-react.md` "**Component file size**" (approximately 300 lines is preferred, if it exceeds 500 lines or is too complex, sub-components, Hooks, utils, and types will be split)
- Keep components with single responsibilities and composable
- Extract reusable logic into hooks
- Prioritize the use of controlled component APIs in appropriate scenarios
- props are clearly defined and typed
- Prioritize reuse of existing design system components
- Maintain accessibility with keyboard interaction
- Avoid deep JSX nesting and duplicate branches
- Do not store additional state for deducible values

---


## Component directory suggestions

When the component complexity is low, only one file can be kept.  
When a component contains styles, subcomponents, hooks, and tests, it is recommended to use the following structure:

```text
ComponentName/
├── ComponentName.tsx
├── ComponentName.types.ts
├── ComponentName.styles.css
├── hooks/
│   └── useComponentLogic.ts
├── components/
│   └── SubComponent.tsx
└── __tests__/
    └── ComponentName.spec.tsx
```

Description:

- Split `ComponentName.types.ts` when the type is complex
- Split `hooks/` when there is local logic reuse
- When the subcomponent is only used inside the current component, it is placed in the current directory `components/`
- Whether the test should be placed nearby should follow the existing protocols of the warehouse

---

