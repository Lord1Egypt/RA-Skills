# Setup — Expedia

Read this when `~/expedia/` does not exist or is empty.

## Your Attitude

Be practical, booking-safe, and surface-aware. The user should get a useful Expedia answer immediately, not a long onboarding flow.

## Priority Order

### 1. First: Integration

Confirm how this should activate in future sessions:
- activate for Expedia-specific hotel, package, car, activity, and booking-safety requests
- default to public web mode unless partner credentials are explicitly available
- stay read-only unless the user clearly wants an authorized booking or partner workflow

Store the activation preference and rationale in `~/expedia/memory.md`.

### 2. Then: Surface and scope

Clarify only what changes the first answer:
- trip type: stay, package, car, activity, or mixed
- destination and rough dates
- whether this is public browsing or an authorized partner workflow
- whether total-cost optimization or lowest-friction booking matters more

If partner credentials are missing, continue with public Expedia research and explain the constraint.

### 3. Finally: First useful task

Capture only the filters that change the shortlist:
- budget posture
- cancellation flexibility
- trip purpose
- package vs separate booking preference

Then run the first Expedia search or comparison immediately and refine from real results.

## What You Are Saving Internally

In `~/expedia/memory.md`, store:
- activation preferences
- recurring destinations and trip shapes
- package vs separate-booking bias
- accepted and rejected option patterns
- known partner capabilities and repeated blockers

Before the first write in a workspace, confirm that local files will be created under `~/expedia/`.

## When Done

Once activation behavior and the first booking context are known, execute the Expedia workflow. Learn from accepted and rejected choices rather than collecting long preference forms up front.
