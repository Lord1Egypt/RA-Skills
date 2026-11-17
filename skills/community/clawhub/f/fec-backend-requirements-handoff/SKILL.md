---
name: fec-backend-requirements-handoff
description: Use when frontend work needs to communicate data, action, state, permission, validation, or business-rule needs to backend teams without dictating endpoint design, field names, database shape, or implementation details; Chinese triggers include front-end and back-end requirements handover, back-end requirements, API requirements clarification, data requirements description.
---

# Handover of front-end and back-end requirements

## Purpose

Organize the data, actions, status, and questions required for front-end pages and interactions into discussion-ready requirements for the back-end.

## Procedure

1. Clarify the functional context
- Describe what the page, process, or component is, what type of user it is intended for, and the success status of the user completing the task.
   - If there are existing designs, routes, user stories, or permission roles, use them as sources of truth first.

2. Describe front-end display requirements
   - List information to be displayed by screen or component, relationships between information, sorting/filtering/pagination requirements and visibility rules.
   - Use business language to describe "what needs to be displayed" and do not specify endpoints, field names, DTOs, database tables or response nested structures in advance.

3. Describe user actions and results
   - List the actions the user can perform, expected results, success feedback, failure feedback and whether optimistic updates are needed.
   - Mark behaviors that affect the UI such as idempotence, undo, confirm, dangerous operations, batch operations, or long task progress.

4. Complete status and business rules
   - Override the status of loading, empty, error, partial, permission denied, expired, conflict, offline and retrying.
   - Document permissions, lifecycle, amounts/timezones/enumerations, validations, editable conditions, and boundary rules that affect the UI.

5. Output discussion document
   - By default, it is written to `docs/backend-requirements/<feature-name>.md`; if the warehouse already has a requirements document directory, the existing location will be used.
   - Documentation includes Context, Screens/Components, Data Needs, User Actions, UI States, Business Rules, Uncertainties, Questions for Backend and Decision Log.
   - If the user only needs chat replies, they can directly output Markdown with the same structure without creating a file.

## Constraints

- Does not specify URLs, HTTP methods, field names, database schema, cache implementation, or service splitting for the backend.
- Don't write front-end guesses into facts; uncertain business rules must go into Uncertainties or Questions.
- Errors, empty states, permissions and partial data are not ignored; these states determine the quality of interface collaboration.
- Do not expose internal error stacks, database fields, or sensitive implementation details to the UI.
- Does not duplicate the API integration process: This skill describes the requirements, client boundaries, type sources and error mapping implementation should be handled in subsequent implementation phases.

## Expected Output

Produce a back-end requirements handover description from a front-end perspective, clearly describing what data and behaviors the UI requires, which rules still need to be confirmed, and subsequent issues that need to be decided jointly by the front-end and back-end.
