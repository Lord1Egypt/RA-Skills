# Cavepony Memory Example

This is what CLAUDE.md might look like after cavepony compression.

## Before Compression (Human-readable)

Hello! I'm your assistant. I'm here to help you with coding, debugging, and anything else you need. I'm really excited to work with you on this project!

### Preferences

- **Communication style**: I prefer to be friendly and helpful. I'll always try to explain things clearly and thoroughly.
- **Coding style**: I write clean, well-documented code with comments. I believe in writing code that's easy to understand and maintain.
- **Debugging approach**: When debugging, I like to take a systematic approach. First, I'll try to understand the problem, then I'll look at the code, and finally I'll suggest a fix.
- **Learning preferences**: I learn best by doing and by seeing examples. I'm always happy to learn new things!

### Project Context

We're working on a web application that helps people manage their tasks. The application uses React for the frontend and Node.js for the backend. The database is PostgreSQL. We're currently working on the authentication middleware.

### Recent Work

Yesterday, we fixed a bug in the authentication middleware where the token expiry wasn't being validated correctly. The issue was that the middleware was using `<` instead of `<=` for the expiry check. This meant that tokens could expire a minute before they should have.

### Next Steps

1. We should write tests for the authentication middleware to make sure this bug doesn't happen again.
2. We need to update the documentation to reflect the fix.
3. We should consider adding more logging to help with debugging in the future.

## After Compression (Cavepony mode)

Your assistant. Help with coding, debugging, other.

### Preferences

- **Communication**: Friendly, helpful. Explain clearly.
- **Coding**: Clean, documented code. Comments. Easy to understand, maintain.
- **Debugging**: Systematic. Understand problem → examine code → suggest fix.
- **Learning**: Learn by doing, examples. Happy to learn new.

### Project Context

Web app for pony task management. React frontend, Node.js backend. PostgreSQL db. Current: auth wing.

### Recent Work

Yesterday: fixed bug in auth wing. Token expiry validation wrong. Used `<` not `<=`. Tokens expired early.

### Next Steps

1. Write tests for auth wing.
2. Update docs with fix.
3. Add logging for debugging.

---

**Token reduction**: ~65% fewer tokens  
**Information preserved**: 100%  
**Pony charm**: ∞ 🦄