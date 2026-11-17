# Goal recipes

## Revise a goal

```sh
candor goals get GOAL_ID --reason "Read the goal before changing it"
candor goals history GOAL_ID --reason "See earlier versions and why they changed"
candor goals update --file GOAL.json --reason "Move the date the person agreed to"
```

Every operation takes the `goal_key` wherever it takes a goal id. An update
saves a new version; say what changed so the person can correct it. Progress
facts never retarget a goal on their own: a slipping goal is a conversation,
not an automatic new date.

## Record progress by hand

Only for a `recorded` measure, or progress the records cannot show (cash at
home, an account Candor does not see):

```sh
candor goals progress record GOAL_ID --amount 'USD 250.00' --kind contribution --reason "Record the deposit the person made at their credit union"
```

Check it is not already counted, cite where it came from, and re-read the
goal.

## Archive

```sh
candor goals archive GOAL_ID --reason "The person dropped this goal"
```

Archiving keeps history. Save a note saying why, so it is not suggested again.

## Several goals

When goals compete for the same money, show the collision with figures and
let the person rank them; record `priority` as they say it. Parts of one
ambition use `parent_goal_id` and show under it on the dashboard.

## Goal check-in

"Am I on track?" Read `progress` for each goal: what moved since last time
(`goal.moved` in the opening), the required versus planned pace, and the
projected completion date. Lead with the one that needs attention. Show
`candor visual goals --reason "Show the person their goals"` when they want the picture.
