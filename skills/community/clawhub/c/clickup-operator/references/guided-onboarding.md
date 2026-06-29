# ClickUp Operator Guided Onboarding

This is the intended experience for a new user.

The user should be able to install the skill and then tell the agent to run it.
From there, the agent should guide the setup instead of expecting the user to manually figure out the whole integration.

## Product goal

The experience should feel like:

1. install the skill
2. tell the agent to set up ClickUp Operator
3. the agent walks through technical connection
4. the agent learns the user's ClickUp structure
5. the agent confirms routing defaults
6. the agent runs a tiny smoke test
7. the skill is ready for normal use

## The agent's onboarding responsibilities

The agent should actively guide four setup layers:

### 1. Connection layer

The agent helps the user:

- connect the official ClickUp MCP endpoint
- complete ClickUp auth / token retrieval
- store or reference the token in the correct local environment path
- verify the MCP connection is live

### 2. Discovery layer

The agent learns:

- default workspace
- default space
- general to-do destination
- ideas destination
- default assignee rules
- project-routing pattern
- status vocabulary

### 3. Language-mapping layer

The agent learns what the user's natural phrases mean, for example:

- "my to-do list"
- "my task list"
- "ideas"
- "website project"
- "that client"

### 4. Validation layer

The agent runs a safe smoke test using clearly labeled test items and confirms the behavior matches expectations.

## Best agent behavior during onboarding

- ask short targeted questions, not a giant questionnaire dump
- prefer using the real ClickUp hierarchy to make questions concrete
- do not impose a new structure if the user already has one
- summarize discovered defaults back to the user before finalizing
- save the discovered setup into config only after the user confirms it

## Required outputs of onboarding

By the end of guided onboarding, the agent should have:

- a working ClickUp MCP connection
- the required workspace/list/member IDs
- the user's routing defaults
- the user's language mapping
- a config file or config snapshot
- a smoke test result

## Setup conversation shape

Good flow:

1. verify or establish ClickUp MCP access
2. inspect live hierarchy
3. ask where general tasks go
4. ask where ideas go
5. ask about project routing
6. ask about default assignee and due-date behavior
7. restate discovered rules
8. run smoke test

Bad flow:

- asking the user to fill in raw IDs with no guidance
- forcing a generic structure on top of an existing system
- skipping the language-mapping step
- declaring setup complete before validation
