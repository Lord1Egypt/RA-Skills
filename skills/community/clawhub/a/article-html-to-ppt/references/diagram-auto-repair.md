# Diagram Auto Repair

Stage 5 does not automatically change business relationships. It emits repair advice that a model or human must confirm.

## Main Path Missing

Suggested repair:

- find primary entry nodes;
- follow `sequence`, `request`, `data_flow`, `trigger`, `validation`, or `produce` edges;
- propose one main path;
- require confirmation before writing it back.

## All Edges Primary

Suggested repair:

- keep edges on the main path as `primary`;
- mark feedback, monitoring, and influence edges as `secondary` or `supporting`;
- convert weak relationships into annotations.

## Unknown Node

Suggested repair:

- correct the edge source/target id if it is a typo;
- otherwise add the missing node with a label, role, type, priority, shape, and status;
- do not invent hidden nodes silently.

## Connector Web Risk

Suggested repair:

- define one main path;
- group nodes into lanes/layers/zones;
- lift repeated node-level edges to group-level semantics;
- move weak influence/monitoring edges to annotations;
- split into overview + detail slides.

## Type Mismatch

Suggested repair:

- `swimlane` when role handoff dominates;
- `layered_architecture` when layers and responsibility dominate;
- `flywheel` when feedback loop dominates;
- `zoned_ecosystem` when multi-party zones dominate;
- `capability_landscape` when coverage/grouping matters more than flow.

## Node Overload

Suggested repair:

- cluster nodes by group;
- keep first-level nodes on the main slide;
- move detail nodes to appendix or next slide;
- preserve the original relation set in notes or source artifacts.
