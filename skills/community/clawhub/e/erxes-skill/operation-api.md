---
title: operation_api – SaaS Workflow Reference
description: User-facing workflows and exact GraphQL operations for erxes operation_api
---

# operation_api – SaaS Workflow Reference

Use this file when the user wants to operate operation-side work records through natural language. Focus on projects, tasks, triage, teams, statuses, cycles, milestones, notes, activities, and templates.

Assume OpenClaw is operating as the erxes owner by default. Backend permission names exist, but they should not be treated as a normal blocker for owner-run workflows.

## Safety Rules

- Read, list, search, filter, group, and summarize can run directly.
- If the user asks to group by status, assignee, team, or priority, fetch the matching list first and group the returned records in the response.
- For create or update, ask only for missing required fields.
- For remove, delete, end-cycle, or remove-member actions, identify the exact record first and ask for explicit confirmation.
- Never expose raw tokens or session payloads.

## Backend Permission Names

- Tasks: `taskRead`, `taskCreate`, `taskUpdate`, `taskRemove`, `taskAssign`
- Triage: `triageRead`, `triageCreate`, `triageUpdate`, `triageConvert`
- Projects: `projectRead`, `projectCreate`, `projectUpdate`, `projectRemove`
- Milestones: `milestoneRead`, `milestoneCreate`, `milestoneUpdate`, `milestoneRemove`
- Cycles: `cycleRead`, `cycleCreate`, `cycleUpdate`, `cycleRemove`, `cycleEnd`
- Teams: `teamRead`, `teamCreate`, `teamUpdate`, `teamRemove`, `teamMemberManage`
- Notes: `noteRead`, `noteCreate`, `noteUpdate`, `noteRemove`
- Statuses: `statusRead`, `statusCreate`, `statusUpdate`, `statusRemove`

These names are useful only as backend reference. In normal OpenClaw usage, proceed as owner and only surface an access issue if the API actually rejects the call.

## Natural Language Examples

- "Show me active projects"
- "Summarize project progress"
- "Find tasks with no assignee"
- "Group tasks by status"
- "Create a task for this team"
- "Create a triage item"
- "Convert this triage item to a task"
- "Show active cycles for this team"
- "Summarize milestone progress"
- "Add a note to this task"

## Workflows

### Projects

- What the user can ask:
- List projects, filter them, inspect one project, or summarize project progress.
- Create, update, or remove a project.
- What OpenClaw needs:
- Project `_id` for detail, progress, update, or remove.
- `name` and `teamIds` to create.
- Optional `leadId`, `memberIds`, `status`, `priority`, `tagIds`, `startDate`, `targetDate`, `convertedFromId`.
- GraphQL:
- `getProject(_id: String!): Project`
- `getProjects(filter: IProjectFilter): ProjectListResponse`
- `getProjectProgress(_id: String!): JSON`
- `getProjectProgressByMember(_id: String!): JSON`
- `getProjectProgressByTeam(_id: String!): JSON`
- `getProjectProgressChart(_id: String!): JSON`
- `getConvertedProject(convertedFromId: String): Project`
- `cpGetProjects: [Project]`
- `createProject(name: String!, leadId: String, memberIds: [String], icon: String, description: String, status: Int, priority: Int, teamIds: [String!]!, tagIds: [String], startDate: Date, targetDate: Date, convertedFromId: String): Project`
- `updateProject(_id: String!, name: String, leadId: String, memberIds: [String], icon: String, description: String, status: Int, priority: Int, teamIds: [String], tagIds: [String], startDate: Date, targetDate: Date): Project`
- `removeProject(_id: String!): JSON`
- Required fields:
- Create requires `name` and `teamIds`.
- Optional filters:
- `_id`, `_ids`, `name`, `description`, `status`, `priority`, `teamIds`, `tagIds`, `leadId`, `memberIds`, `memberId`, `startDate`, `targetDate`, `userId`, `active`, `taskId`, plus cursor pagination.
- Safe confirmation rules:
- Read, list, and progress queries can run directly.
- Remove must always ask for confirmation first.

### Tasks

- What the user can ask:
- List tasks, find overdue tasks, find tasks with no assignee, group tasks by status, or inspect one task.
- Create, update, or remove a task.
- What OpenClaw needs:
- Task `_id` for detail, update, or remove.
- For create, confirm `name`, `teamId`, and `status`.
- Optional `description`, `priority`, `labelIds`, `tagIds`, `startDate`, `targetDate`, `assigneeId`, `cycleId`, `projectId`, `estimatePoint`, `milestoneId`.
- GraphQL:
- `getTask(_id: String!): Task`
- `getTasks(filter: ITaskFilter): TaskListResponse`
- `createTask(name: String!, description: String, teamId: String!, status: String, priority: Int, labelIds: [String], tagIds: [String], startDate: Date, targetDate: Date, assigneeId: String, cycleId: String, projectId: String, estimatePoint: Int, milestoneId: String): Task`
- `updateTask(_id: String!, name: String, description: String, teamId: String, status: String, priority: Int, labelIds: [String], tagIds: [String], assigneeId: String, startDate: Date, targetDate: Date, cycleId: String, projectId: String, estimatePoint: Int, milestoneId: String): Task`
- `removeTask(_id: String!): Task`
- Required fields:
- Create requires `name`, `teamId`, and `status`.
- Optional filters:
- `name`, `status`, `statusType`, `priority`
- `assigneeId`, including `no-assignee`
- `projectId`, including `no-project`
- `teamId`, `createdBy`, `cycleId`, `cycleFilter`
- `milestoneId`, `estimatePoint`, `labelIds`, `tagIds`
- `projectStatus`, `projectPriority`, `projectLeadId`, `projectMilestoneName`
- `startDate`, `targetDate`, `createdDate`, `updatedDate`, `completedDate`
- Safe confirmation rules:
- Grouping happens after `getTasks`.
- Remove must always ask for confirmation first.

### Triage

- What the user can ask:
- List triage items for a team.
- Create or update a triage item.
- Convert a triage item to a task.
- What OpenClaw needs:
- Triage `_id` for detail, update, cancel, or convert.
- For create, confirm `name` and `teamId`.
- Optional `description`, `priority`, and `status`.
- GraphQL:
- `operationGetTriage(_id: String!): Triage`
- `operationGetTriageList(filter: ITriageFilter): TriageListResponse`
- `operationAddTriage(input: ITriageAddInput!): Triage`
- `operationUpdateTriage(_id: String!, input: ITriageUpdateInput!): Triage`
- `operationCancelTriage(_id: String!): Triage`
- `operationConvertTriageToTask(_id: String!, status: Int, reason: String): Task`
- Required fields:
- Create requires `name` and `teamId`.
- Optional filters:
- `_id`, `teamId`, `createdBy`, `createdAt`, `updatedAt`, `name`, `description`, `priority`, plus cursor pagination.
- Safe confirmation rules:
- Convert and cancel must ask for confirmation first.
- If the user wants the created task in a specific workflow lane, fetch team status choices first.

### Teams And Team Members

- What the user can ask:
- List teams, inspect one team, or show team members.
- Create, update, or remove a team.
- Add or remove members.
- What OpenClaw needs:
- Team `_id` for detail, update, remove, add members, or remove members.
- `name` and `icon` to create a team.
- Member IDs to add or remove members.
- GraphQL:
- `getTeam(_id: String!): Team`
- `getTeams(name: String, userId: String, teamIds: [String], projectId: String, isTriageEnabled: Boolean, teamId: String): [Team]`
- `getTeamMembers(teamId: String, teamIds: [String]): [TeamMember]`
- `getTeamEstimateChoises(teamId: String): JSON`
- `teamAdd(name: String!, description: String, icon: String!, memberIds: [String]): Team`
- `teamUpdate(_id: String!, name: String, description: String, icon: String, memberIds: [String], estimateType: Int, cycleEnabled: Boolean, triageEnabled: Boolean): Team`
- `teamRemove(_id: String!): Team`
- `teamAddMembers(_id: String!, memberIds: [String]): [TeamMember]`
- `teamRemoveMember(teamId: String!, memberId: String!): TeamMember`
- `teamUpdateMember(_id: String!): TeamMember`
- Optional filters:
- `name`, `userId`, `teamIds`, `projectId`, `isTriageEnabled`, `teamId`
- Safe confirmation rules:
- Team removal and member removal must always ask for confirmation first.
- If the user names a member without an ID, search or list likely matches first.

### Statuses

- What the user can ask:
- Show available statuses for a team.
- Show statuses for a specific type.
- Create, update, or delete a status.
- What OpenClaw needs:
- Status `_id` for detail, update, or delete.
- For create, confirm `name`, `teamId`, `color`, `type`, and `order`.
- GraphQL:
- `getStatus(_id: String!): Status`
- `getStatusesChoicesByTeam(teamId: String!): JSON`
- `getStatusesByType(type: Int!, teamId: String!): [Status]`
- `addStatus(name: String!, teamId: String!, description: String, color: String, order: Int, type: Int): Status`
- `updateStatus(_id: String!, name: String, description: String, color: String, order: Int, type: Int): Status`
- `deleteStatus(_id: String!): JSON`
- Required fields:
- Create requires `name`, `teamId`, `color`, `type`, and `order`.
- Safe confirmation rules:
- Fetch choices first when the user uses a human status name instead of an ID.
- Delete must always ask for confirmation first.

### Cycles

- What the user can ask:
- Show cycles for a team.
- Show active or upcoming cycles.
- Summarize cycle progress.
- Create, update, remove, or end a cycle.
- What OpenClaw needs:
- Cycle `_id` for detail, progress, update, remove, or end.
- `teamId`, `name`, `startDate`, and `endDate` for a meaningful create flow.
- GraphQL:
- `getCycle(_id: String): Cycle`
- `getCycles(teamId: String, page: Int, perPage: Int, after: String, before: String): CycleListResponse`
- `getCyclesActive(teamId: String, taskId: String, page: Int, perPage: Int, after: String, before: String): CycleListResponse`
- `getCycleProgress(_id: String!, assigneeId: String): JSON`
- `getCycleProgressChart(_id: String!, assigneeId: String): JSON`
- `getCycleProgressByMember(_id: String!, assigneeId: String): JSON`
- `getCycleProgressByProject(_id: String!, assigneeId: String): JSON`
- `createCycle(input: CycleInput): Cycle`
- `updateCycle(input: CycleInput): Cycle`
- `removeCycle(_id: String): JSON`
- `endCycle(_id: String): JSON`
- Safe confirmation rules:
- Remove and end-cycle must always ask for confirmation first.

### Milestones, Activities, Notes, Templates

- What the user can ask:
- List milestones for a project.
- Summarize milestone progress.
- Show activity history for a task or record.
- Add, update, or delete a note.
- List or manage templates for a team.
- What OpenClaw needs:
- Project `_id` for milestone list or progress.
- Milestone `_id` for update or remove.
- `contentId` for activity or notes.
- `teamId` for templates.
- GraphQL:
- `getMilestone(_id: String!): Milestone`
- `milestones(projectId: String!, searchValue: String, page: Int, perPage: Int, after: String, before: String): MilestoneListResponse`
- `milestoneProgress(projectId: String!): [MilestoneProgress]`
- `createMilestone(name: String!, description: String, targetDate: Date, projectId: String!): Milestone`
- `updateMilestone(_id: String!, name: String!, description: String, targetDate: Date, projectId: String!): Milestone`
- `removeMilestone(_id: String!): Milestone`
- `getOperationActivities(contentId: String!, page: Int, perPage: Int, after: String, before: String): OperationActivityListResponse`
- `getNote(_id: String!): Note`
- `createNote(content: String, contentId: String, mentions: [String]): Note`
- `updateNote(_id: String!, content: String, contentId: String, mentions: [String]): Note`
- `deleteNote(_id: String!): JSON`
- `operationTemplates(teamId: String): [OperationTemplate]`
- `operationTemplateDetail(_id: String): OperationTemplate`
- `operationTemplateAdd(name: String!, defaults: JSON!, teamId: String!): OperationTemplate`
- `operationTemplateEdit(_id: String!, name: String, defaults: JSON): OperationTemplate`
- `operationTemplateRemove(_id: String!): JSON`
- Required fields:
- Milestone create requires `name` and `projectId`.
- Template create requires `name`, `defaults`, and `teamId`.
- Safe confirmation rules:
- Remove milestone, delete note, and remove template must always ask for confirmation first.
- If the live API rejects note removal, report the rejection directly instead of assuming ownership limits in advance.

## Needs Verification

- `operationCancelTriage(_id: String!)` exists in the schema, but no resolver implementation was found. Runtime behavior needs verification.
- `teamUpdateMember(_id: String!)` is exposed in the schema without a `role` argument, but the resolver expects a role value. Live member role updates need verification.
- Template queries and mutations do not call `checkPermission`, and no template permission definitions were found in the permission metadata. This is a backend detail only; owner-mode access should still be assumed unless the live API says otherwise.
