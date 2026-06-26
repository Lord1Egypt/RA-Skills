---
title: block_api – SaaS Workflow Reference
description: User-facing workflows and exact GraphQL operations for erxes block_api
---

# block_api – SaaS Workflow Reference

Use this file when the user wants to operate block-side business records through natural language. Focus on business workflows, not source code.

Assume OpenClaw is operating as the erxes owner by default.

## Safety Rules

- Read, list, search, filter, group, and summarize can run directly.
- If the user asks to group by status, type, project, or similar, fetch the matching list first and group the returned records in the response.
- For create or update, ask only for missing required fields.
- For delete, remove, publish, unpublish, transfer, or convert actions, identify the record first and ask for explicit confirmation.
- Never expose raw tokens or session payloads.

## Natural Language Examples

- "Show me all projects that are on sale"
- "Create a new project called Central Residence"
- "Show me all blocks grouped by status"
- "Add a new block to this project"
- "List the floors in this building"
- "Create units for floors 3 to 10"
- "Find opportunities related to this customer"
- "Move this opportunity to another status"
- "Create a payment plan for this project"

## Workflows

### Projects

- What the user can ask:
- List projects, search by name, filter by publish state, project status, type, city, district, or date ranges.
- Create a new project.
- Update project general information.
- Publish or unpublish a project.
- Remove a project.
- What OpenClaw needs:
- Project `_id` for detail, update, publish, unpublish, or remove.
- `name` to create a project.
- Optional filters `searchValue`, `dateFilters`, `types`, `status`, `isPublished`, `locations`.
- GraphQL:
- `blockGetProject(_id: String!): BlockProject`
- `blockGetProjects(filters: BlockProjectFilterInput): [BlockProject]`
- `blockCreateProject(name: String!): BlockProject`
- `blockUpdateProjectGeneralInfo(_id: String!, input: BlockProjectGeneralInput!): BlockProject`
- `blockPublishProject(_id: String!, isPublished: Boolean!): BlockProject`
- `blockRemoveProject(_id: String!): BlockProject`
- Required fields:
- Create requires `name`.
- Update requires the target `_id` and a `BlockProjectGeneralInput` object.
- Optional filters:
- `searchValue`, `dateFilters`, `types`, `status`, `isPublished`, `locations`
- Safe confirmation rules:
- Read and list can run directly.
- Publish, unpublish, and remove must always ask for confirmation first.

### Buildings / Blocks

- What the user can ask:
- Show all blocks in a project.
- Group blocks by status.
- Create, duplicate, update, or delete a block.
- What OpenClaw needs:
- Project `_id` to list blocks.
- Building `_id` to inspect, duplicate, update, or delete.
- For create, confirm `project`, `name`, and `types`.
- GraphQL:
- `blockGetBuildings(project: String!): [BlockBuilding]`
- `blockGetBuilding(_id: String!): BlockBuilding`
- `blockCreateBuilding(input: BlockBuildingInput!): BlockBuilding`
- `blockDupplicateBuilding(buildingId: String!): BlockBuilding`
- `blockUpdateBuilding(_id: String!, input: BlockBuildingInput!): BlockBuilding`
- `blockDeleteBuilding(_id: String!): BlockBuilding`
- Required fields:
- The underlying model requires `name`, `types`, and `project`.
- Optional fields:
- `description`, `coverImage`, `status`, `startDate`, `endDate`
- Safe confirmation rules:
- Grouping happens after `blockGetBuildings`.
- Delete must ask for confirmation.
- Warn that delete fails when the building still has zonings.

### Floor Zonings

- What the user can ask:
- List floors or zoning rows for a building.
- Add a zoning for a floor.
- Duplicate or update a zoning.
- Delete a zoning.
- What OpenClaw needs:
- Building `_id` to list zonings.
- Zoning `_id` to inspect, update, duplicate, or delete.
- For create, at minimum confirm `building` and `floor`.
- GraphQL:
- `blockGetBuildingZonings(building: String!): [BlockBuildingZoning]`
- `blockGetBuildingZoning(_id: String!): BlockBuildingZoning`
- `blockCreateBuildingZoning(input: BlockBuildingZoningInput!): BlockBuildingZoning`
- `blockDupplicateBuildingZoning(_id: String!): BlockBuildingZoning`
- `blockUpdateBuildingZoning(_id: String!, input: BlockBuildingZoningInput!): BlockBuildingZoning`
- `blockDeleteBuildingZoning(_id: String!): BlockBuildingZoning`
- Optional fields:
- `usageTypes`, `areaType`, `tenureTypes`, `priceList`, `size`, `useProjectPrice`
- Safe confirmation rules:
- Delete must ask for confirmation.
- Warn that delete fails when the zoning still has units.

### Units

- What the user can ask:
- Show units for one zoning or many zonings.
- Create a single unit.
- Create units in bulk for a building and floor range.
- Update a unit.
- Remove one or many units.
- Transfer a unit to an agency.
- What OpenClaw needs:
- Unit `_id` for detail, update, remove, or transfer.
- `zoning` or `zonings` to list units.
- For bulk creation, `buildingId`, `units`, and `zoneRange`.
- For transfer, `unitId`, `agencySubdomain`, and `agencyId`.
- GraphQL:
- `blockGetUnit(_id: String!): BlockUnit`
- `blockGetUnits(zoning: String, zonings: [String]): [BlockUnit]`
- `blockGetAgencies: [BlockAgencyBasic]`
- `blockCreateUnit(input: BlockUnitInput!): BlockUnit`
- `blockCreateUnits(input: BlockUnitsInput!): [BlockUnit]`
- `blockUpdateUnit(_id: String!, input: BlockUnitInput!): BlockUnit`
- `blockRemoveUnit(_id: String!): BlockUnit`
- `blockRemoveUnits(_ids: [String]): JSON`
- `blockTransferUnit(input: BlockTransferUnitInput!): BlockUnit`
- Required fields:
- A safe single-unit create flow should confirm `zoning`, `number`, and `type`.
- Optional fields:
- `status`, `agencyEntityId`, `useProjectPrice`
- Safe confirmation rules:
- Remove, bulk remove, and transfer must ask for confirmation.
- Warn that updates can fail if the unit already has a signed contract.

### Opportunities And Statuses

- What the user can ask:
- Show all opportunities for a project.
- Search opportunities by number, customer, description, or assignee.
- Group opportunities by status.
- Create, update, or delete an opportunity.
- Convert an opportunity to a contract.
- Create, update, reorder, or remove opportunity statuses.
- What OpenClaw needs:
- Project `_id` to list opportunities or statuses.
- Opportunity `_id` for detail, update, delete, or convert.
- For create or update, confirm `description`, `customerId`, and `status`.
- GraphQL:
- `blockGetOppty(_id: String!): BlockOppty`
- `blockGetOpptys(projectId: String!, filter: IOpptyFilter): BlockOpptyListResponse`
- `blockGetOpptyUnitRows(_id: String!): [BlockOpptyUnitRow]`
- `blockCreateOppty(input: IBlockOpptyInput!): BlockOppty`
- `blockUpdateOppty(_id: String!, input: IBlockOpptyInput!): BlockOppty`
- `blockDeleteOppty(_id: String!): BlockOppty`
- `blockOpptyConvertToContract(_id: String!, unit: String!, paymentPlan: BlockProjectPaymentPlanInput!): String`
- `getBlockOpptyStatus(_id: String!): BlockOpptyStatus`
- `getBlockOpptyStatuses(projectId: String!): [BlockOpptyStatus]`
- `getBlockOpptyStatusTypes: JSON`
- `createBlockOpptyStatus(input: BlockOpptyStatusInput!): BlockOpptyStatus`
- `updateBlockOpptyStatus(_id: String!, input: BlockOpptyStatusInput!): BlockOpptyStatus`
- `updateBlockOpptyStatusOrder(_id: String!, order: Int!): BlockOpptyStatus`
- `removeBlockOpptyStatus(_id: String!): BlockOpptyStatus`
- Required fields:
- The underlying opportunity model requires `description`, `customerId`, and `status`.
- Optional filters:
- `searchValue`, `number`, `description`, `customerId`, `unitType`, `tenureType`, `unit`, `assignedUserId`, `status`, `priority`, `startDate`, `targetDate`, `dateFilters`, `customerSource`, `labelId`, `tagId`
- Safe confirmation rules:
- Grouping happens after `blockGetOpptys`.
- Create and update should fetch status choices first when the status is ambiguous.
- Delete, status removal, and convert-to-contract must ask for confirmation.

### Supporting Records

- Payment plans:
- `blockGetProjectPaymentPlans(project: String!): [BlockProjectPaymentPlan]`
- `blockCreateProjectPaymentPlan(input: BlockProjectPaymentPlanInput!): BlockProjectPaymentPlan`
- `blockUpdateProjectPaymentPlan(_id: String!, input: BlockProjectPaymentPlanInput!): BlockProjectPaymentPlan`
- `blockRemoveProjectPaymentPlan(_id: String!): BlockProjectPaymentPlan`
- Project members:
- `blockGetProjectMembers(project: String!): [BlockProjectMember]`
- `blockAddProjectMembers(project: String!, memberIds: [String!]!): [BlockProjectMember]`
- `blockUpdateProjectMember(_id: String!, role: BlockProjectMemberRole): BlockProjectMember`
- `blockDeleteProjectMember(_id: String!): BlockProjectMember`
- Unit types:
- `blockGetUnitTypes(project: String): [UnitType]`
- `blockGetUnitType(_id: String!): UnitType`
- `blockCreateUnitType(input: UnitTypeInput!): UnitType`
- `blockUpdateUnitType(_id: String!, input: UnitTypeInput!): UnitType`
- `blockRemoveUnitType(_id: String!): UnitType`
- Unit leads:
- `blockGetUnitLeads(unit: ID!): [BlockUnitLead]`
- `blockAddUnitLead(input: BlockUnitLeadInput!): BlockUnitLead`
- `blockRemoveUnitLead(input: BlockUnitLeadInput!): BlockUnitLead`
- Documents:
- `blockGetDocument(_id: String!): BlockDocument`
- `blockGetDocuments(itemType: String!, itemId: String!): [BlockDocument]`
- `blockCreateDocument(input: BlockDocumentInput!): BlockDocument`
- `blockUpdateDocument(_id: String!, input: BlockDocumentInput!): BlockDocument`
- `blockDeleteDocument(_id: String!): BlockDocument`
- Attachments:
- `blockGetAttachment(_id: String!): BlockAttachment`
- `blockGetAttachments(itemType: String!, itemId: String!): [BlockAttachment]`
- `blockCreateAttachment(input: BlockAttachmentInput!): BlockAttachment`
- `blockUpdateAttachment(_id: String!, input: BlockAttachmentInput!): BlockAttachment`
- `blockDeleteAttachment(_id: String!): BlockAttachment`
- Contracts:
- `blockGetContract(_id: String!): BlockContract`
- `blockGetContracts(unit: String): [BlockContract]`
- `blockCreateContract(input: BlockContractInput!): BlockContract`
- `blockUpdateContract(_id: String!, input: BlockContractInput!): BlockContract`
- `blockUpdateContractStatus(_id: String!, status: BlockContractStatus!): BlockContract`
- Offers:
- `blockGetOffer(_id: String!): BlockOffer`
- `blockGetOffers(unit: String): [BlockOffer]`
- `blockCreateOffer(input: BlockOfferInput!): BlockOffer`
- `blockUpdateOffer(_id: String!, input: BlockOfferInput!): BlockOffer`
- `blockSendOfferEmail(_id: String!): String`
- Invoices:
- `blockGetInvoice(_id: String!): BlockInvoice`
- `blockGetInvoices(itemId: String!): [BlockInvoice]`
- `blockPayInvoice(_id: String!, paidDate: Date): String`
- Notes:
- `blockGetNote(_id: String!): BlockNote`
- `blockCreateNote(content: String, contentId: String, mentions: [String], contentType: EnumBlockNoteContentType): BlockNote`
- `blockUpdateNote(_id: String!, content: String, contentId: String, mentions: [String]): BlockNote`
- `blockDeleteNote(_id: String!): JSON`
- Developer profile:
- `getDeveloperInfo: Developer`
- `updateDeveloperInfo(input: DeveloperInput): Developer`
- `updateDeveloperVerificationStatus: Developer`

## Needs Verification

- No block-specific permission matrix was found for GraphQL workflows. This does not block owner-mode use, but non-owner access scope behavior still needs verification.
- `blockDupplicateBuildingZoning` is exposed with `_id` in the schema, but the resolver reads `zoningId`. The live argument shape needs verification.
- `blockOpptyConvertToContract` currently returns `"success"` in the resolver without visible conversion logic. The real business effect needs verification.
