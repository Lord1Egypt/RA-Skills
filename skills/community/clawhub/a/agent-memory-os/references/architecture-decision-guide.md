# Architecture Decision Guide

Use this guide when the user is unsure whether they need a full memory system.

## Start simple if
- work is mostly one-off chat
- there are no long-lived projects
- durable lessons are not yet important
- maintenance overhead would exceed the value

## Upgrade to a memory system if
- the agent repeatedly loses context
- multiple projects are active at once
- the user wants reusable lessons, not just logs
- project-local state keeps polluting long-term memory
- people want something sharable or standardizable

## Use the full global / project / bridge model when
- long-term memory and active work must stay separate
- multiple projects need independent working brains
- reusable knowledge should flow upward over time
- validation and maintenance matter, not just storage

## Rule of thumb
If the pain is "my agent forgets once in a while," do not overbuild.
If the pain is "my agent becomes chaotic as work scales," this skill is likely a strong fit.
