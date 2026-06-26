---
name: auto-glossary
description: Automatically add technical jargon to the user's tech glossary GitHub repository when encountered during coding sessions. Use when technical terms, coding concepts, or developer jargon comes up that the user (E-man) might need to understand. The skill watches for unfamiliar terminology during coding tasks and adds it to the glossary with analogy-based explanations following the established format.
---

# Auto-Glossary Skill

This skill automatically manages technical terminology for E-man by adding new terms to his tech glossary when encountered during coding work.

## When to Use This Skill

Trigger this skill when:
1. A technical term appears in code, error messages, or discussions that might be unfamiliar
2. Explaining a coding concept that hasn't been glossary-ified yet
3. Encountering jargon during debugging, reviews, or implementation
4. The user asks "what does X mean?" or shows confusion about terminology

## Term Identification

Watch for these categories during coding sessions:
- **Programming concepts** (async/await, closure, currying, memoization)
- **TypeScript/JavaScript terms** (generics, union types, type guards, inference)
- **Git/GitHub terms** (rebase, cherry-pick, stash, squash)
- **Framework terms** (hydration, SSR, CSR, middleware, route handlers)
- **Database terms** (migration, indexing, normalization, transaction)
- **Architecture terms** (monolith, microservices, serverless, edge)
- **Testing terms** (mocking, stubbing, TDD, integration test)
- **DevOps terms** (CI/CD, containerization, orchestration, deployment)
- **Security terms** (authentication, authorization, encryption, hashing)
- **Performance terms** (lazy loading, caching, memoization, tree-shaking)

## Glossary Entry Format

Every term must follow this exact format:

```markdown
### Term Name
- **Simple definition**: One sentence explanation in plain English
- **Analogy**: A relatable real-world comparison that makes the concept click
- **When you'll use it**: Practical context for when this matters
- **Related terms**: 2-5 related concepts (comma separated)
- **Example**: A concrete code or scenario example
```

### Format Rules

1. **Simple definition**: Must be jargon-free. If you need to explain the definition, it's too complex.
2. **Analogy**: Should be from everyday life (cooking, driving, organizing, etc.). The user loves these.
3. **When you'll use it**: Be specific about the trigger moment - "When you see X error" or "Before deploying to production"
4. **Related terms**: Only include terms that are actually in the glossary or should be added soon
5. **Example**: Use real code from the current project when possible, or realistic pseudo-code

## Workflow

When a new term is identified:

1. **Check if term exists**: Read `project/tech-glossary/glossary.md` to verify it's not already there
2. **Categorize**: Determine which section (Git & Version Control, Development Tools, Web Development, etc.)
3. **Write the entry**: Follow the format above strictly
4. **Update count**: Increment "Terms covered" at the bottom
5. **Commit and push**: 
   ```bash
   cd project/tech-glossary
   git add glossary.md
   git commit -m "Add '<Term>' to glossary: <one-line description>"
   git push
   ```

## Categories (for organizing entries)

Use these existing sections or create new ones:
- Git & Version Control
- Artificial Intelligence
- Development Tools & Configuration
- Web Development
- Programming Concepts
- Databases
- Testing
- DevOps & Deployment
- Security
- Performance & Optimization

## Examples of Good Entries

### Refactor (from existing glossary)
```markdown
### Refactor
- **Simple definition**: Improving the *internal* structure of code without changing its *external* behavior. It's about making code cleaner, faster, or easier to read
- **Analogy**: Like rewriting a paragraph to be clearer using better words, but the meaning of the paragraph stays exactly the same. Or rearranging your kitchen so it's easier to cook, but you're still making the same meal
- **When you'll use it**: When your code works, but it's getting messy or hard to understand as you add new features
- **Related terms**: Technical Debt, Best Practices, Optimization
- **Example**: You have a long, confusing function that calculates a budget. You refactor it by breaking it into three smaller, clearly-named functions. The math doesn't change, but it's now much easier for a human to read
```

### Type Guard (hypothetical new entry)
```markdown
### Type Guard
- **Simple definition**: A check that tells TypeScript "I know what type this is" so it can give you better autocomplete and catch errors
- **Analogy**: Like showing your ID at a bar. The bouncer doesn't know you're over 21 just by looking, but once you show ID, they treat you differently. TypeScript doesn't know a variable is a string until you prove it
- **When you'll use it**: When TypeScript complains that "property doesn't exist" on a variable that could be multiple types
- **Related terms**: TypeScript, Type Inference, Union Types
- **Example**: 
  ```typescript
  function process(value: string | number) {
    if (typeof value === "string") {
      // TypeScript now knows this is a string
      return value.toUpperCase();
    }
    // TypeScript knows this is a number
    return value.toFixed(2);
  }
  ```
```

## Reference: Full Glossary Structure

See [references/glossary-format.md](references/glossary-format.md) for the complete format guide and examples.

## Don't Overdo It

- **Skip obvious terms**: Don't add "Variable" or "Function" - these are too basic
- **Skip one-off mentions**: If a term comes up once and never again, maybe skip it
- **Prioritize recurring confusion**: If the user asks about something twice, definitely add it
- **Batch related terms**: If 3 related terms come up, add them all at once in one commit

## After Adding a Term

Let the user know: "Added 'X' to your tech glossary with an analogy. You can check it anytime at github.com/EmanxChan/tech-glossary"