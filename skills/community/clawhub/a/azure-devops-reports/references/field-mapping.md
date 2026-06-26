# Field Mapping

Normalize Azure DevOps work items to these fields when possible:

- `id` ← `System.Id`
- `title` ← `System.Title`
- `state` ← `System.State`
- `type` ← `System.WorkItemType`
- `assignedTo` ← `System.AssignedTo.displayName` or string value
- `assignedToEmail` ← `System.AssignedTo.uniqueName` when available
- `project` ← `System.TeamProject`
- `iterationPath` ← `System.IterationPath`
- `areaPath` ← `System.AreaPath`
- `priority` ← `Microsoft.VSTS.Common.Priority`
- `createdDate` ← `System.CreatedDate`
- `changedDate` ← `System.ChangedDate`
- `closedDate` ← `Microsoft.VSTS.Common.ClosedDate`
- `originalEstimate` ← `Microsoft.VSTS.Scheduling.OriginalEstimate`
- `remainingWork` ← `Microsoft.VSTS.Scheduling.RemainingWork`
- `storyPoints` ← `Microsoft.VSTS.Scheduling.StoryPoints`

Preferred default field list for reporting:

- `System.Id`
- `System.Title`
- `System.State`
- `System.WorkItemType`
- `System.AssignedTo`
- `System.TeamProject`
- `System.IterationPath`
- `System.AreaPath`
- `System.CreatedDate`
- `System.ChangedDate`
- `Microsoft.VSTS.Common.ClosedDate`
- `Microsoft.VSTS.Common.Priority`
- `Microsoft.VSTS.Scheduling.OriginalEstimate`
- `Microsoft.VSTS.Scheduling.RemainingWork`
- `Microsoft.VSTS.Scheduling.StoryPoints`
