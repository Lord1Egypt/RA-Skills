# Effective Java Item Map

This is a compact, paraphrased map of Effective Java, 3rd edition. Use it for item-level navigation and learning summaries; do not treat it as a substitute for the book.

## Object Creation and Destruction

1. Prefer static factories when naming, caching, subtyping, or instance control makes construction clearer.
2. Use builders when constructors would require many optional or interdependent parameters.
3. Enforce singleton properties carefully; enum singletons are often simplest.
4. Prevent instantiation of utility classes with a private constructor.
5. Prefer dependency injection to hard-coded resources.
6. Avoid unnecessary objects, especially in hot paths.
7. Remove obsolete references that prevent garbage collection.
8. Avoid finalizers and cleaners for normal cleanup.
9. Use try-with-resources for deterministic resource release.

## Methods Common to All Objects

10. Override `equals` only when logical equality is needed and can satisfy the full contract.
11. Always override `hashCode` when overriding `equals`.
12. Implement `toString` for useful diagnostics and logging.
13. Prefer copying alternatives to `clone`; if cloning, respect its tricky contract.
14. Implement `Comparable` only with a consistent, documented total ordering.

## Classes and Interfaces

15. Minimize accessibility of every type and member.
16. Use accessors instead of public mutable fields.
17. Minimize mutability; immutable objects are simpler and safer.
18. Favor composition and forwarding over inheritance for reuse.
19. Design and document inheritance deliberately, or prohibit it.
20. Prefer interfaces to abstract classes for type definitions.
21. Design interfaces carefully because default methods can create compatibility traps.
22. Do not use interfaces only to export constants.
23. Prefer class hierarchies to tagged classes with mode fields.
24. Prefer static member classes over nonstatic ones when no enclosing instance is needed.
25. Keep one top-level class per source file.

## Generics

26. Do not use raw types in new code.
27. Eliminate unchecked warnings; suppress only tightly and with justification.
28. Prefer lists to arrays when generics are involved.
29. Favor generic types over casts at use sites.
30. Favor generic methods for reusable type-safe operations.
31. Use bounded wildcards to make APIs flexible.
32. Combine generics and varargs carefully; avoid heap pollution.
33. Use type tokens for type-safe heterogeneous containers.

## Enums and Annotations

34. Use enums instead of integer constants for fixed sets.
35. Do not rely on enum ordinals for data or persistence.
36. Use `EnumSet` instead of bit fields.
37. Use `EnumMap` instead of ordinal indexing.
38. Model extensible enum-like behavior with interfaces when needed.
39. Prefer annotations to naming patterns.
40. Consistently use `@Override`.
41. Use marker interfaces when type relationships matter at compile time.

## Lambdas and Streams

42. Prefer lambdas to anonymous classes for small function objects.
43. Prefer method references when they are clearer than lambdas.
44. Use standard functional interfaces before inventing new ones.
45. Use streams judiciously; clarity beats novelty.
46. Keep stream functions side-effect-free.
47. Return collections or arrays rather than streams when callers need normal collection behavior.
48. Use parallel streams only with evidence that they are correct and faster.

## Methods

49. Check parameters for validity and fail early.
50. Make defensive copies when accepting or returning mutable objects across trust boundaries.
51. Design method signatures carefully: names, parameters, overloads, and return types are API.
52. Use overloading carefully; avoid surprising compile-time dispatch.
53. Use varargs judiciously and avoid ambiguous or unsafe calls.
54. Return empty collections or arrays, not `null`.
55. Return `Optional` judiciously for absent results.
56. Write documentation comments for exposed APIs.

## General Programming

57. Minimize the scope of local variables.
58. Prefer enhanced `for` loops when indexes or iterators are not needed.
59. Know and use the standard libraries.
60. Use `BigDecimal`, `int`, or `long` for exact monetary calculations; avoid float or double for exact answers.
61. Prefer primitives to boxed primitives unless nullability or generics require boxing.
62. Avoid strings for data that has a better type.
63. Beware repeated string concatenation in performance-sensitive loops.
64. Refer to objects by interfaces when suitable.
65. Prefer interfaces to reflection for normal application logic.
66. Use native methods only when justified.
67. Optimize only after measurement identifies a real problem.
68. Follow generally accepted naming conventions.

## Exceptions

69. Use exceptions only for exceptional conditions.
70. Use checked exceptions for recoverable conditions and runtime exceptions for programming errors.
71. Avoid unnecessary checked exceptions that make APIs painful.
72. Prefer standard exceptions when they fit.
73. Translate lower-level exceptions while preserving the cause.
74. Document every exception thrown by exposed APIs.
75. Include failure-capture information in detail messages.
76. Strive for failure atomicity.
77. Do not ignore exceptions.

## Concurrency

78. Synchronize access to shared mutable data.
79. Avoid excessive synchronization and avoid alien method calls inside locks.
80. Prefer executors, tasks, and streams to raw threads.
81. Prefer concurrency utilities to `wait` and `notify`.
82. Document thread-safety guarantees.
83. Use lazy initialization only when it is necessary and safely implemented.
84. Do not depend on the thread scheduler for correctness.

## Serialization

85. Prefer alternatives to Java serialization.
86. Implement `Serializable` very cautiously because it creates long-lived API and security obligations.
87. Consider a custom serialized form when the default form exposes internals or wastes space.
88. Write `readObject` defensively.
89. Prefer enum types for instance control when compatible with the design.
90. Consider serialization proxies for classes with invariants.

## Fast Mapping by Task

- New value object: items 2, 10-14, 17, 49-50, 56.
- Public API review: items 1-2, 15-22, 31, 49-56, 70-75, 82.
- Collection-heavy utility: items 26-33, 45-48, 54-55, 57-59.
- Concurrent service: items 5, 17, 78-84.
- Enum modeling: items 34-38.
- Legacy serialization: items 85-90.
- Performance pass: items 6, 45-48, 59-61, 63, 67, 78-81.
