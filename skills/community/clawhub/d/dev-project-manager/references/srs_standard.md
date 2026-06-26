# SRS Standard — Software Requirements Specification

## Purpose

The SRS is the formal agreement between the client and the development team on what will be built. It is a client-facing document — written in accessible, non-technical language while being precise enough for engineering to implement against. Think of it as "what the software will do and how the user will experience it" — not "how the software will be built internally."

## Document Conventions

- **Version numbering**: Start at 1.0 for first client-ready draft. Minor revisions (typo fixes, clarifications) increment the decimal: 1.1, 1.2. Major scope changes increment the whole number: 2.0, 3.0.
- **Requirement IDs**: Every requirement gets a unique, never-reused ID. Functional requirements use `FR-XXX`, non-functional use `NFR-XXX`, interface requirements use `IR-XXX`.
- **Priority tags**: Every requirement is tagged `[Must-Have]`, `[Should-Have]`, `[Nice-to-Have]`, or `[Out-of-Scope]`.
- **Language**: Use "The system shall..." for mandatory requirements, "The system should..." for recommended, and "The system may..." for optional.

## SRS Template

```
SOFTWARE REQUIREMENTS SPECIFICATION
[Project Name]

Version: [X.X]
Date: [YYYY-MM-DD]
Prepared by: [PM Agent Name/ID]
Client: [Client Name/Organization]
Status: [Draft | In Review | Approved | Amended]

═══════════════════════════════════════════════════

TABLE OF CONTENTS
1. Introduction
2. Overall Description
3. System Features & Functional Requirements
4. Interface Requirements
5. Non-Functional Requirements
6. Cost & Effort Analysis
7. Assumptions & Dependencies
8. Out of Scope
9. Open Questions
10. Acceptance Criteria Summary
11. Change Log
12. Sign-Off

═══════════════════════════════════════════════════

1. INTRODUCTION

1.1 Purpose
   Describe what this document covers and its intended audience.
   Example: "This document defines the software requirements for
   the redesign of the Acme Corp customer portal's reporting
   module. It is intended for review and approval by the Acme
   Corp product team and will serve as the basis for engineering
   implementation."

1.2 Scope
   High-level description of what the project will deliver and
   what business goals it supports. Keep it to 2-3 paragraphs.

1.3 Definitions & Acronyms
   Define any terms that may be ambiguous. Include business terms
   the client uses that have specific meaning in this project.

1.4 References
   Link to related documents: existing documentation, mockups,
   previous SRS versions, relevant third-party specs.

═══════════════════════════════════════════════════

2. OVERALL DESCRIPTION

2.1 Product Perspective
   How does this software/feature fit into the larger ecosystem?
   Is it a standalone system, an update to an existing one, or a
   new module within a larger platform? For existing software,
   describe the current state and what is changing.

2.2 User Classes and Characteristics
   Who uses this software? Describe each user type:
   - Role/title
   - What they use the software for
   - Technical comfort level
   - Frequency of use

2.3 Operating Environment
   Where does the software run? (Web browser, mobile, desktop,
   specific OS requirements, integrations with other systems)

2.4 Constraints
   Business rules, regulatory requirements, technology
   constraints, timeline constraints that shape the solution.

═══════════════════════════════════════════════════

3. SYSTEM FEATURES & FUNCTIONAL REQUIREMENTS

   Organize by feature area. Each feature gets a subsection.

   3.X [Feature Name]

   3.X.1 Description
         What this feature does in plain language. Include the
         business value — why does this feature matter?

   3.X.2 Current State (for existing software changes)
         How this area works today. What the user currently sees
         and can do. Be specific enough that the client can
         confirm "yes, that's how it works now."

   3.X.3 Proposed Changes
         What will be different. Describe from the user's
         perspective: what they'll see, what they'll be able to
         do, how the workflow changes.

   3.X.4 Requirements

         FR-XXX: [Requirement title] [Must-Have]
         The system shall [specific behavior].
         Acceptance Criteria:
         - Given [context], when [action], then [expected result]
         - Given [context], when [action], then [expected result]

         FR-XXX: [Requirement title] [Should-Have]
         The system should [specific behavior].
         Acceptance Criteria:
         - Given [context], when [action], then [expected result]

   3.X.5 Interface Changes (if applicable)
         Description of visual/UI changes. Reference mockups
         if provided. Describe in terms of what the user sees
         and interacts with, not implementation details.

═══════════════════════════════════════════════════

4. INTERFACE REQUIREMENTS

4.1 User Interface Requirements
   General UI standards, accessibility requirements, responsive
   design expectations, branding guidelines.

4.2 External Interface Requirements
   Integrations with other systems, APIs, data feeds, third-
   party services that the software must interact with.

4.3 Data Migration Requirements (if applicable)
   What existing data needs to be preserved, transformed, or
   migrated as part of this project.

═══════════════════════════════════════════════════

5. NON-FUNCTIONAL REQUIREMENTS

   NFR-XXX: [Performance] [Must-Have]
   Example: "Page load times shall not exceed 2 seconds under
   normal load conditions."

   NFR-XXX: [Security] [Must-Have]
   Example: "All user data shall be encrypted in transit and
   at rest."

   NFR-XXX: [Availability] [Should-Have]
   Example: "The system should maintain 99.9% uptime."

   Common categories to address:
   - Performance / response times
   - Security & data protection
   - Scalability
   - Availability / uptime
   - Browser / device compatibility
   - Accessibility (WCAG compliance level)
   - Data retention / backup

═══════════════════════════════════════════════════

6. COST & EFFORT ANALYSIS

6.1 Effort Summary Table

   | Req ID | Feature | Complexity | Human Hours | Human Cost | AI Hours | AI Cost | AI Success % | Savings |
   |--------|---------|------------|-------------|------------|----------|---------|-------------|---------|
   | FR-001 | ...     | Low        | 8h          | $XXX       | 0.5h     | $X.XX   | 97%         | $XXX    |
   | FR-002 | ...     | Medium     | 24h         | $XXX       | 2h       | $X.XX   | 90%         | $XXX    |
   | FR-003 | ...     | High       | 80h         | $XXX       | 8h       | $X.XX   | 75%         | $XXX    |

6.2 Complexity Definitions
   - Trivial: Cosmetic changes, copy updates, config changes
   - Low: Single-component changes, straightforward logic
   - Medium: Multi-component changes, moderate logic, some
     integration work
   - High: Cross-cutting changes, complex business logic, data
     model changes, new integrations
   - Very High: Architectural changes, new subsystems, complex
     migration, novel technical challenges

6.3 Human Cost Basis
   Provide the standard bill rates used for comparison:
   - Senior Developer: $[X]/hr
   - Frontend Developer: $[X]/hr
   - Backend Developer: $[X]/hr
   - QA Engineer: $[X]/hr
   - DevOps/Infrastructure: $[X]/hr

6.4 AI Cost Basis
   Calculated using estimated token consumption per task
   complexity. See the estimation reference for the formula.

6.5 Total Project Summary
   - Total human effort estimate: [X] hours / $[X]
   - Total AI effort estimate: [X] hours / $[X]
   - Estimated client savings: $[X] ([X]%)
   - Weighted average AI success probability: [X]%

6.6 Risk-Adjusted Estimates
   For tasks with AI success probability below 85%, include
   a fallback estimate that accounts for potential rework or
   human intervention.

═══════════════════════════════════════════════════

7. ASSUMPTIONS & DEPENDENCIES

   List anything the project relies on that isn't guaranteed:
   - Client will provide [X] by [date]
   - Existing API [X] will remain stable
   - Third-party service [X] will be available
   - Client has [X] environment/access available for testing

═══════════════════════════════════════════════════

8. OUT OF SCOPE

   Explicitly list things that were discussed but are NOT
   included in this project. This prevents scope disputes later.
   For each item, note why it's excluded and whether it's
   planned for a future phase.

═══════════════════════════════════════════════════

9. OPEN QUESTIONS

   Any unresolved items that need client or stakeholder input
   before implementation can proceed. Each question should note
   who needs to answer it and what the impact of not answering
   it would be.

   | # | Question | Owner | Impact if Unresolved | Status |
   |---|----------|-------|---------------------|--------|

═══════════════════════════════════════════════════

10. ACCEPTANCE CRITERIA SUMMARY

   A consolidated list of all acceptance criteria across all
   requirements. This section serves as the testing checklist
   that will be used to verify the implementation.

   | Req ID | Acceptance Criterion | Status |
   |--------|---------------------|--------|
   | FR-001 | Given X, when Y, then Z | Pending |

═══════════════════════════════════════════════════

11. CHANGE LOG

   | Version | Date | Author | Changes |
   |---------|------|--------|---------|
   | 1.0     | ...  | ...    | Initial draft |

═══════════════════════════════════════════════════

12. SIGN-OFF

   By signing below, the client confirms that this SRS
   accurately represents the agreed-upon requirements and
   approves engineering to proceed with implementation.

   Client Representative: ________________________
   Name: [Name]
   Title: [Title]
   Date: [YYYY-MM-DD]
   SRS Version Approved: [X.X]

   Project Manager: ________________________
   Name: [PM Agent ID]
   Date: [YYYY-MM-DD]

   Notes:
   [Any conditions or caveats on the approval]
```

## SRS Writing Guidelines

### Language Rules

1. **No technical jargon without explanation.** If you must use a technical term, define it in section 1.3 and use the plain-language equivalent in the requirement itself.
   - Bad: "The system shall expose a RESTful endpoint that returns paginated JSON payloads."
   - Good: "The system shall provide a way for external systems to retrieve report data in batches, supporting standard web integration formats."

2. **Be specific and testable.** Every "shall" statement needs to be verifiable.
   - Bad: "The system shall be fast."
   - Good: "The system shall display search results within 2 seconds of the user submitting a query."

3. **One requirement per ID.** Don't bundle multiple behaviors into a single requirement.
   - Bad: "FR-010: The system shall allow users to upload files, and those files shall be scanned for viruses, and the user shall receive email confirmation."
   - Good: Three separate requirements — FR-010 (upload), FR-011 (virus scan), FR-012 (email confirmation).

4. **Describe behavior, not implementation.** The SRS says what the system does, not how it's built.
   - Bad: "The system shall store user preferences in a Redis cache with a 24-hour TTL."
   - Good: "The system shall remember user preferences between sessions for at least 24 hours."

5. **Use consistent verb forms.** "The system shall" for Must-Have, "The system should" for Should-Have, "The system may" for Nice-to-Have.

### Acceptance Criteria Format

Use Given-When-Then format for all acceptance criteria:

```
Given [a precondition or context],
When [the user performs an action],
Then [the expected observable result].
```

**Example:**
```
FR-015: Dashboard Date Filter [Must-Have]
The system shall allow users to filter the dashboard by date range.

Acceptance Criteria:
- Given the user is on the dashboard page,
  When they select a start date and end date from the date picker,
  Then the dashboard shall refresh to show only data from the
  selected range within 2 seconds.

- Given the user has set a date filter,
  When they click "Clear Filter,"
  Then the dashboard shall return to showing the default
  date range (last 30 days).

- Given the user selects an end date that is before the start date,
  When they attempt to apply the filter,
  Then the system shall display a validation message and
  not apply the filter.
```

### Section Completeness Checklist

Before presenting an SRS to the client, verify:

- [ ] Every section has content (no "TBD" placeholders in Must-Have items)
- [ ] Every functional requirement has at least one acceptance criterion
- [ ] Every requirement has a unique ID and priority tag
- [ ] The effort/cost table covers all requirements
- [ ] Out-of-scope section is populated (even if it's just "Nothing was explicitly excluded")
- [ ] Change log reflects current version
- [ ] Open questions are documented with owners
- [ ] No orphan references (no mention of a requirement ID that doesn't exist)
