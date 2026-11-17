# Migration execution and checklist

## Pre-migration analysis

Before starting the migration, the following analysis must be completed and a **migration analysis report** must be output:

1. **Inventory Count**
   - Number of pages and number of functional modules
   - Dependent jQuery plugins and alternatives (such as DataTables → TanStack Table)
   - Existing API calling methods and whether there is unified encapsulation
   - Are there any server-side templates (JSP/Thymeleaf/EJS, etc.) that need to be retained, partially replaced, or changed to pure front-end rendering?
   - Is the target stack React/Vue/Next/Nuxt, modern MPA, or just partial TypeScript/build/test modernization?

2. **Dependencies**
   - JS/CSS modules shared between pages
- Business logic reused across pages
   - Interface contract with the backend (whether it needs to be adjusted)

3. **Migration Priority**
   - Sort by business value, complexity, coupling degree
   - Prioritize migrating independent modules and low-coupling pages
   - Identify reusable utility functions, constants, and type definitions

## Phased migration process

### Phase 0: Preparation

- Build or identify target project skeleton: React/Vue/Next/Nuxt, modern MPA, or progressive TypeScript/build entry within existing projects
- Configure ESLint, Prettier, and test framework
- Establish `services/request.ts` unified request layer, compatible with existing API
- Gradually migrate `utils` and `constants` in legacy projects and add types

### Phase 1: Base Layer

- Migrate and type API calls (`$.ajax` → `axios`/`fetch`)
- Migration tool functions (date, formatting, verification, etc.)
- Migrate constants, enumerations, and type definitions
- Establish target navigation/page entry skeleton; unmigrated pages can continue to use old routing, redirection, iframe or micro-front-end embedding

### Phase 2: Migration by module/page

- Migrate one complete feature or page at a time
- From simple to complex: static page → list page → form page → complex interactive page
- Extract reusable components during migration, following the directory structure of the target React or Vue project
- Supplementary unit testing and E2E critical path for each completed module

### Phase 3: Closing

- Remove or freeze old code entries according to the migration strategy; if MPA is retained, the old entries will be converged and the modernization boundary will be completed
- Configure 404, error boundaries, and global error handling
- Performance optimization (lazy loading, code splitting, caching strategy)
- Document updates and deployment process adjustments

## Refactoring implementation requirements

The following implementation constraints need to be followed when migrating to ensure consistent vision and interaction, and the code is simpler and easier to maintain.

### Pictures and Icons

- Directly use the image resource path of the original project without rehosting or replacing it.
- SVG images (`<img src="*.svg" />` or CSS `background-image`) can be used; when icon components or accessible interactions require inline SVG, the target project icon specifications should be followed and the reasons should be explained.
- If the original project uses iconfont or IcoMoon icons, priority should be given to continuing to use them during reconstruction to keep the icon system consistent; visual consistency, packaging, and maintenance costs need to be evaluated before replacing with other icon schemes.
- For icons, priority is given to using existing icon files in the original project (iconfont / IcoMoon / existing SVG). If necessary, SVG files can be introduced as independent resources

### Internationalization (i18n)

- User-visible copy in the new stack code (React/Vue, etc.) must follow the project i18n, and do not hardcode Chinese/English copy in the new code
- **Do not add** user-visible hard-coded copy in legacy HTML/JS, unless it is purely static and the warehouse does not yet have an available i18n access point; before changing the copy, check whether locales already has an entry, and synchronize the main language files
- Keys are organized by page/module/semantics, and existing keys are reused; mapping transition is only done when the old key is an external contract. For details, see **Internationalization (i18n)** in the project rules ("Legacy Code and Migration Scenarios" in `templates/shared/rules/fec-i18n.md`)

### Style

- The layout style aligns with the visual effects of the original project, but **only refers to the original project effects and does not copy its CSS**
- Prioritize the use of **flex elastic layout** to avoid `float`, complex `position`, and redundant nesting
- Avoid unreasonable writing methods: such as `!important` abuse, excessively deep selectors, and repeated definitions
- Prioritize to avoid inline styles (`style={{ ... }}` / `style="..."`) in components; when it is necessary to use runtime dynamic values, third-party component APIs or CSS variable bridging, they should be kept local and interpretable and put into the target project style system first.

### Target

- **Visual and interactive**: consistent with the original project, no perceived difference by users
- **Code Quality**: more concise, easier to maintain, and in line with the target framework specifications
- **Business functions**: consistent with the original project, **no missing functions**; behaviors before and after migration are equivalent

### Verification layering

- If it involves the migration of pages, components, routing, forms, pop-ups, navigation or key user processes, first establish a list of behaviors before and after refactoring, and then use Playwright or an equivalent real browser verification method to compare and verify the critical paths.
- For visually sensitive pages, supplement screenshot comparison or manual screenshot acceptance; dynamic content, animation, fonts and environmental differences need to be clearly blocked, stabilized or explained.
- For pure logic, type, build or UI-less migrations, Playwright is not forced and a validation layer closer to risk should be chosen: type-check, unit test, component test, build or lint.
- The verification goal is not to be completely consistent at the pixel level, but to confirm that there are no missing business functions, key interactions are equivalent, there are no unexpected deviations in the main visual layout, and the code is clearer and maintainable than the old implementation.

## Migration Checklist

After each migration unit is completed, confirm:

- [ ] A behavioral list before and after refactoring has been established, covering public APIs, routing, forms, permissions, error status, cache, hidden points and key interactions
- [ ] The business logic is consistent with the old implementation, no functions are missing, and the functions are completely equivalent.
- [ ] Migration involving UI, interaction or critical processes has completed critical path comparison using Playwright or equivalent real browser verification
- [ ] For visually sensitive pages, screenshot comparison or manual screenshot acceptance has been completed, and the method of handling differences in dynamic content, animation, fonts and environment has been explained.
- [ ] Pure logic, type, build or no UI migrations have selected a validation layer that is closer to the risk and do not force the application of Playwright
- [ ] Type definition is complete, no `any` abuse
- [ ] API calls use a unified request layer, with complete error handling
- [ ] Form verification, loading, empty state, and error state have been implemented
- [ ] Accessibility: The form has a label and can be interacted with via the keyboard.
- [ ] No XSS risk (user input is escaped or secure API is used)
- [ ] Critical path has test coverage
- [ ] Comply with the project specifications of the target stack (React / Vue / Next / Nuxt / MPA modernization, etc.)
- [ ] Pictures use original project resources; icon systems give priority to the original project or target project specifications, exceptions have been explained
- [ ] The style refers to the original project effect but does not copy the CSS. The target project style system is used first. The inline style exception has been explained.
- [ ] The visual and interaction are consistent with the original project, and the code is simpler and easier to maintain.
- [ ] The new code path copy has been i18n; the legacy layer has not been expanded and hardcoded; locales retrieval and multi-language synchronization have been completed (see i18n rule migration supplementary list)
