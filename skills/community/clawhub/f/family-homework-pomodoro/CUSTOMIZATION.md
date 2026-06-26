# Customization Guide

This document explains how to adapt `family-homework-pomodoro` for a private
deployment, paid support engagement, or a team-specific workflow.

The public skill remains the reference version. Keep that version generic and
public-safe, and use this guide when you want a custom variant.

## What can be customized

The following parts are safe to adapt for a private implementation:

- reminder cadence
- parent confirmation flow
- child-facing message tone
- night check timing
- reward approval wording
- multi-child variants
- local workflow metadata
- packaging and installation steps

## What should stay generic

Even in a custom deployment, avoid adding:

- real names
- school names
- group IDs or account IDs
- private schedules tied to identity
- health or other sensitive personal data

## Suggested customization inputs

If someone wants a tailored version, the minimum useful inputs are:

- intended deployment location
- number of children or roles involved
- desired reminder cadence
- preferred approval flow
- whether the skill should be read-only, prompt-only, or tool-assisted
- any packaging requirements for the target platform

## Recommended process

1. start from the public skill as the reference
2. list the fields that should change
3. confirm the fields that must remain public-safe
4. update the README and skill metadata together
5. test the result in a private workspace before publishing

## Example customization directions

- change the default rhythm from `25/5` to another study/break cycle
- split reminders by subject or assignment type
- add a private parent-only approval note
- add deployment-specific packaging or import instructions
- add platform-specific metadata for a private skill registry

## Support positioning

If this skill is used in a paid or sponsored context, the customization work is
best positioned as:

- setup assistance
- documentation cleanup
- workflow adaptation
- packaging for a private environment

The public skill itself should remain free to inspect and reuse.
