# Glossary Format Reference

This document provides the complete format specification for glossary entries.

## Entry Template

```markdown
### Term Name
- **Simple definition**: [One sentence, jargon-free]
- **Analogy**: [Everyday comparison that makes it click]
- **When you'll use it**: [Specific context/scenario]
- **Related terms**: [2-5 comma-separated related terms]
- **Example**: [Concrete code or scenario example]
```

## Field Guidelines

### Simple Definition
- Must be understandable to a non-technical person
- Avoid nested technical terms (or briefly define them inline)
- Focus on WHAT it does, not HOW it works
- Keep to one sentence if possible, two max

**Good**: "A function that remembers its surroundings even after those surroundings have finished executing"
**Bad**: "A closure is a record storing a function together with an environment mapping associates each free variable of the function with the value or storage location to which the name was bound when the closure was created"

### Analogy
- Use everyday activities: cooking, driving, organizing, sports, shopping
- The analogy should map cleanly to the concept
- Include a "just like" or "similar to" comparison
- Make it vivid and specific

**Good**: "Like a restaurant kitchen where the chef has mise en place (everything prepped and ready). The ingredients are "closed over" and available when the chef starts cooking, even if the prep station has been cleaned up"
**Bad**: "Like a box that holds things"

### When You'll Use It
- Be specific about the trigger moment
- Include the problem it solves
- Mention error messages or symptoms that indicate this is relevant

**Good**: "When you need a function to 'remember' data from where it was created, even when called from somewhere else. You'll see this in callbacks, event handlers, and factory functions"
**Bad**: "When programming"

### Related Terms
- Only include terms actually in the glossary or commonly understood
- Link related concepts that build on each other
- Keep to 2-5 terms max

**Good**: "First-Class Functions, Callback, Scope, Lexical Environment"
**Bad**: "Programming, Computer Science, JavaScript, Code"

### Example
- Use real code when possible
- Show the problem AND the solution
- Keep it concise but complete
- Use TypeScript/JavaScript since that's what the user works with

## Section Headers

Organize terms into these sections (create new ones as needed):

```markdown
## Git & Version Control
[Git-specific terms]

## Artificial Intelligence
[AI/ML terms]

## Development Tools & Configuration
[IDEs, configs, CLIs]

## Web Development
[Frontend/backend web concepts]

## Programming Concepts
[Language-agnostic concepts]

## Databases
[SQL, NoSQL, data concepts]

## Testing
[Testing methodologies and tools]

## DevOps & Deployment
[Infrastructure, CI/CD, hosting]

## Security
[Auth, encryption, vulnerabilities]

## Performance & Optimization
[Speed, memory, efficiency]
```

## Complete Example Entry

```markdown
### Closure
- **Simple definition**: A function that "remembers" the variables from where it was created, even when called from somewhere else
- **Analogy**: Like packing a lunchbox before leaving home. Even though you're now at work (a different environment), you still have access to the sandwich you packed. The lunchbox "closed over" the food from your kitchen
- **When you'll use it**: When you need to create functions that maintain access to private data. Common in callbacks, event handlers, and factory functions. You'll know you need it when a function needs to "remember" something from when it was defined
- **Related terms**: Scope, First-Class Functions, Callback, Factory Pattern
- **Example**:
  ```typescript
  function createCounter() {
    let count = 0;  // This variable is "closed over"
    return function() {
      count++;      // Inner function remembers count
      return count;
    };
  }

  const counter = createCounter();
  console.log(counter()); // 1
  console.log(counter()); // 2 - remembers the previous count!
  ```
```

## Footer Format

Always include at the bottom:

```markdown
---

## How to Use This Glossary

- **When learning**: Look up terms you've forgotten
- **When I add terms**: I'll automatically update this file and commit the changes
- **Seeing history**: Run `git log` in this folder to see every time we've updated the glossary
- **Viewing old versions**: Git keeps every version, so you can always go back to see how your understanding has grown

---

**Terms covered**: [NUMBER]
```

Update the number when adding new terms.