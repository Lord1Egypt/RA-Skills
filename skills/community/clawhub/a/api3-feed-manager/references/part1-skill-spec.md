# Part 1 Skill Spec: Api3 Feed Activation Skill

## Skill name (working)
`api3-feed-manager`

## Purpose
Enable OpenClaw agents to discover, activate, fund, and maintain Api3 data feeds permissionlessly for downstream applications.

## User stories

### Story 1
As an agent building an app that needs a price feed,
I want to discover the correct Api3 feed on a target chain,
so I can use it without human oracle coordination.

### Story 2
As an agent deploying a lending market,
I want to ensure the required Api3 feed is active and funded for ~3 months,
so my market can operate continuously.

### Story 3
As an agent maintaining deployed systems,
I want to check runway and top up feed funding before expiration,
so dependent systems do not silently degrade.

## Inputs

### Required core inputs
- `chain`
- `asset` or `pair`
- `useCase`

### Optional inputs
- `quoteAsset`
- `runwayDays` (default 90)
- `minimumRunwayDays`
- `walletReference`
- `execute` (boolean, default false for discovery/check flows)
- `allowTopUp` (boolean)

## Outputs
- `feedFound`
- `feedName`
- `feedAddressOrId`
- `chain`
- `active`
- `funded`
- `runwayEstimateDays`
- `requiredFundingAsset`
- `estimatedFundingAmount`
- `actionsTaken`
- `transactions`
- `nextMaintenanceRecommendation`
- `warnings`

## Commands / modes

### discover-feed
Return the best matching feed and its state.

### ensure-feed-active
Ensure feed is active and funded for target runway.

### check-feed-runway
Inspect runway and return top-up recommendation.

### top-up-feed
Extend funding for an existing feed.

### maintain-feed
Check one or more feeds and top up if allowed.

## Safety requirements
- Never claim a feed is active without a concrete check.
- Never claim coequal feeds are interchangeable without evidence.
- Distinguish:
  - feed exists but unfunded
  - feed missing
  - feed exists on another chain only
  - feed exists but requires manual wallet capability not currently available
- Log exact blockers instead of vague failure text.

## MVP build plan

### MVP scope
- single-feed discovery
- single-feed status inspection
- single-feed ensure/top-up flow
- maintenance recommendation output

### Not required in MVP
- batch optimization across many feeds
- advanced treasury strategy
- multi-wallet policy orchestration
- automatic cron creation

## Dependencies to confirm
- exact Api3 Market/API access path
- exact contract or API method to read feed funding/runway
- exact activation/funding execution flow
- exact token/payment route for feed funding on supported chains

## Acceptance criteria
- Given an asset/pair and chain, the skill can identify whether a usable Api3 feed exists.
- Given a feed and wallet capability, the skill can determine whether it is sufficiently funded.
- Given insufficient runway and execution rights, the skill can top up or produce exact execution instructions.
- The skill can report back the resulting active/funded state and next maintenance recommendation.
