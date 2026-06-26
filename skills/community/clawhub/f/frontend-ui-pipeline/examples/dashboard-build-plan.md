# Example: SaaS Dashboard Build Plan

## Prompt

"I have a dashboard concept for operations managers. They need KPIs, task status, filters, and detail views. Turn this into a React and Tailwind build plan."

## Recommended Route

- Scenario: SaaS dashboard
- Stage: Build Plan
- Optional companion: `frontend-design` for implementation output

## Example Output Shape

### Build Summary
- **Build scope:** Multi-screen dashboard module
- **Implementation target:** React + Tailwind
- **Priority level:** MVP

### Screens
- Overview dashboard
- Task list with filters
- Task detail panel
- Settings or configuration screen

### Shared Components
- Sidebar navigation
- KPI cards
- Filter toolbar
- Data table
- Detail drawer
- Status badges
- Empty, loading, and error states

### Responsive Rules
- Desktop: sidebar + main content + optional detail drawer
- Tablet: collapsible sidebar and stacked summary modules
- Mobile: list-first flow with detail screens instead of drawers

### Accessibility Requirements
- Keyboard-accessible filters and table actions
- Visible focus states
- Clear labels for status and actions

### DESIGN.md Note
- Create or update `DESIGN.md` after implementation starts.
- Record dashboard density, navigation, state rules, and responsive behavior.
