# Claude Code Rules for [Project Name]

## Project Context
- **Type**: [e.g., TypeScript library, Python data pipeline, React app]
- **Key files**: [list main entry points]
- **Testing framework**: [Jest, pytest, etc.]
- **Deployment target**: [Vercel, AWS, etc.]

## Hard Rules (Never Violate)
1. **Never force-push** to main branch
2. **Always run tests** before committing changes
3. **No direct database modifications** without review
4. **Follow ESLint/Prettier** configuration strictly
5. **Update documentation** when adding new features

## Code Style Preferences
- **Indentation**: 2 spaces
- **Quotes**: Single quotes for JS, double for JSX
- **Imports**: Grouped (external → internal → relative)
- **Naming**: camelCase for variables, PascalCase for components

## Workflow Preferences
- Create feature branches: `feature/description`
- Write commit messages in present tense
- Squash merge PRs
- Run full test suite before opening PR

## Tool Configuration
- Use `npm run lint` before committing
- Use `npm run build` to verify compilation
- Use `npm test -- --coverage` for test coverage

## Memory Integration
- Check `memory.md` for learned patterns
- Review `mistakes.md` before starting complex tasks
- Update `memory.md` with new discoveries