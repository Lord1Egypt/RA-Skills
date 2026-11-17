# Blazor Design Conventions

Blazor sits between a traditional server-rendered app and a modern SPA. The design must work for both WebAssembly and Server modes, and it should lean on the component model for consistency.

## Component Boundaries

- Each `.razor` file is a component. Separate layout (`MainLayout.razor`), pages (`Pages/`), and shared UI (`Shared/`).
- Use parameters (`[Parameter]`) for variants and content. Keep markup and C# codebehind focused.
- MudBlazor, Fluent UI, and Radzen are common component libraries. Treat them as starting points, not final designs.

## Styling Strategy

- Use `site.css` for global tokens and utilities.
- Scoped CSS via `.razor.css` for component-specific rules.
- CSS custom properties in `:root` for the design token layer so they are reachable from all components.

## Responsive Patterns

- Use CSS Grid and Flexbox; Blazor does not ship a layout utility by default.
- MudBlazor provides `MudHidden` and `MudBreakpointProvider` for breakpoint-aware rendering.
- Avoid JavaScript-based layout. Keep layout in CSS so the pre-rendered state is not broken.

## Common Traps

- Heavy page-level components with inline C# and markup.
- Default MudBlazor/Fluent UI palettes used without brand tokens.
- Forgetting that Blazor Server latency means loading states matter more.
