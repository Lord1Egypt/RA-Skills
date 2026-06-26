#!/bin/bash
# Fullstack Feature Template Spawn Prompt
# Use for: Frontend + Backend + Tests coordination

cat << 'SPAWNPROMPT'
I need to build a full-stack feature: ${TASK_DESCRIPTION}

Target: ${TARGET_DIR}

Spawn 3 teammates using Sonnet (tactical implementation):

1. **Frontend Developer**
   - Name: frontend-dev
   - Focus: UI components, API integration, user experience
   - Output: frontend-implementation.md
   - Tasks:
     * Create/modif y UI components for the feature
     * Implement API client and data fetching
     * Add loading states, error handling, validation
     * Ensure responsive design and accessibility
     * Document component usage and props

2. **Backend Developer**
   - Name: backend-dev
   - Focus: API endpoints, business logic, data models
   - Output: backend-implementation.md
   - Tasks:
     * Design and implement API endpoints
     * Implement business logic and validation
     * Update data models/schemas as needed
     * Add error handling and logging
     * Document API contracts (request/response formats)

3. **Test Engineer**
   - Name: test-engineer
   - Focus: Unit tests, integration tests, test coverage
   - Output: test-implementation.md
   - Tasks:
     * Write unit tests for backend logic
     * Write integration tests for API endpoints
     * Add frontend component tests
     * Ensure critical paths have E2E tests
     * Verify test coverage meets requirements

Coordination rules:
- Use delegate mode: I coordinate, teammates implement
- Define clear API contracts before implementation
- Frontend and backend work in parallel (mock API initially)
- Test engineer writes tests alongside implementation
- Daily sync: Review progress and resolve blocking issues

After all teammates finish:
1. Review all implementation files
2. Verify API contracts match between frontend and backend
3. Run all tests and ensure they pass
4. Create integration-summary.md with:
   - Feature overview and architecture
   - API documentation
   - Test coverage report
   - Known limitations or follow-up work
5. Report completion with summary
SPAWNPROMPT
