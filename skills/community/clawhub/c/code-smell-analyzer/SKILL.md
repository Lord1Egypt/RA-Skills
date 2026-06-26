---
name: 'code-smell-analyzer'
description: 'Analyzes code for improvements including code smells, design patterns, and best practices. Invoke when user asks for code analysis, code review, or suggestions to improve code quality.'
version: '1.0.0'
---

# Code Smell Analyzer

Analyzes code files for potential improvements including code smells, design patterns, and best practices. Provides suggestions for enhancing readability, maintainability, and performance while preserving functionality.

## When to Use

Invoke this skill when:

- User asks for code analysis or code review
- User wants suggestions to improve code quality
- User mentions "code smells", "refactoring", or "best practices"
- User wants to optimize code structure without changing functionality

## Analysis Framework

### 1. Code Smells

Identify any code smells such as:

- **Long Methods**: Methods exceeding 20-30 lines should be broken down
- **Large Classes**: Classes with too many responsibilities
- **Duplicate Code**: Repeated code blocks that should be extracted
- **Complex Conditionals**: Deeply nested if/else statements
- **Magic Numbers**: Hard-coded values without explanation
- **Dead Code**: Unused variables, methods, or imports
- **Long Parameter Lists**: Methods with more than 3-4 parameters
- **Feature Envy**: Methods that use another class more than their own

### 2. Design Patterns

Suggest appropriate design patterns that could improve the code structure:

- **Creational**: Factory, Builder, Singleton, Prototype
- **Structural**: Adapter, Decorator, Facade, Composite
- **Behavioral**: Strategy, Observer, Command, State, Template Method

### 3. Best Practices

Check adherence to language-specific best practices:

- **Naming Conventions**: Clear, descriptive names for variables, functions, classes
- **DRY Principle**: Don't Repeat Yourself
- **SOLID Principles**: Single Responsibility, Open/Closed, Liskov Substitution, Interface Segregation, Dependency Inversion
- **Error Handling**: Proper exception handling and error messages
- **Documentation**: Adequate comments and documentation
- **Testing**: Testability of the code

### 4. Readability

Evaluate code clarity:

- **Naming**: Are names self-documenting?
- **Structure**: Is the code well-organized?
- **Comments**: Are complex sections explained?
- **Formatting**: Is indentation and spacing consistent?
- **Abstraction Level**: Is the code at the right level of abstraction?

### 5. Maintainability

Assess how easy the code would be to modify and extend:

- **Coupling**: Are components loosely coupled?
- **Cohesion**: Are related functionalities grouped together?
- **Modularity**: Can parts be changed independently?
- **Configuration**: Are hard-coded values externalized?
- **Logging**: Is there adequate logging for debugging?

### 6. Performance

Identify potential performance optimizations:

- **Algorithm Complexity**: O(n) vs O(n^2) considerations
- **Memory Usage**: Unnecessary object creation, memory leaks
- **I/O Operations**: Database queries, file operations, network calls
- **Caching**: Opportunities for caching repeated computations
- **Lazy Loading**: Defer expensive operations until needed

## Output Format

For each suggestion, provide:

### Issue Description

Clear explanation of the issue or improvement opportunity.

### Current Code

```language
// Show the problematic code
```

### Suggested Improvement

```language
// Show the improved code
```

### Rationale

Explain why the change would be beneficial.

### Priority

- **High**: Critical issues affecting functionality, security, or major performance
- **Medium**: Important improvements for maintainability and readability
- **Low**: Minor enhancements or nice-to-have improvements

## Example Analysis

### Issue: Long Method with Multiple Responsibilities

**Priority: High**

**Current Code:**

```javascript
function processOrder(order) {
    // Validate order
    if (!order.items || order.items.length === 0) {
        throw new Error('Order has no items');
    }
    if (!order.customer) {
        throw new Error('Customer is required');
    }

    // Calculate totals
    let subtotal = 0;
    for (const item of order.items) {
        subtotal += item.price * item.quantity;
    }
    const tax = subtotal * 0.1;
    const total = subtotal + tax;

    // Apply discount
    if (order.discountCode) {
        total = total * 0.9;
    }

    // Save to database
    db.orders.insert({
        ...order,
        subtotal,
        tax,
        total,
        createdAt: new Date(),
    });

    // Send confirmation email
    emailService.send(order.customer.email, 'Order Confirmed', total);

    return {orderId: order.id, total};
}
```

**Suggested Improvement:**

```javascript
function processOrder(order) {
    validateOrder(order);
    const pricing = calculatePricing(order);
    saveOrder(order, pricing);
    sendConfirmation(order, pricing.total);
    return {orderId: order.id, total: pricing.total};
}

function validateOrder(order) {
    if (!order.items?.length) throw new Error('Order has no items');
    if (!order.customer) throw new Error('Customer is required');
}

function calculatePricing(order) {
    const subtotal = order.items.reduce((sum, item) => sum + item.price * item.quantity, 0);
    const tax = subtotal * 0.1;
    let total = subtotal + tax;

    if (order.discountCode) {
        total *= 0.9;
    }

    return {subtotal, tax, total};
}

function saveOrder(order, pricing) {
    db.orders.insert({
        ...order,
        ...pricing,
        createdAt: new Date(),
    });
}

function sendConfirmation(order, total) {
    emailService.send(order.customer.email, 'Order Confirmed', total);
}
```

**Rationale:**

- Single Responsibility: Each function has one clear purpose
- Testability: Each function can be tested independently
- Readability: Main function reads like a high-level overview
- Maintainability: Changes to pricing logic don't affect validation

## Language-Specific Considerations

### JavaScript/TypeScript

- Use `const`/`let` instead of `var`
- Prefer arrow functions for callbacks
- Use optional chaining (`?.`) and nullish coalescing (`??`)
- Avoid `any` type in TypeScript

### Python

- Follow PEP 8 style guide
- Use list comprehensions appropriately
- Leverage context managers (`with` statements)
- Type hints for better documentation

### Java

- Use streams for collection operations
- Prefer composition over inheritance
- Use Optional instead of null
- Follow Java naming conventions

### WeChat Mini Program

- Use Service layer for all HTTP requests
- Avoid storing redundant data in Page data
- Use `wx:key` for list rendering
- Follow the project's AGENTS.md guidelines

## Notes

- Always preserve existing functionality
- Consider the project's existing conventions
- Prioritize changes by impact and effort
- Provide actionable, specific suggestions
- Consider backward compatibility
