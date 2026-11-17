# Connector Routing and Diagram Topology Gate

## Route selection

| Relationship | Default route | Layout rule |
|---|---|---|
| Same-row primary sequence | straight | Short, same-axis, no obstacle |
| Cross-row process or hierarchy | orthogonal | Use reserved horizontal/vertical channels |
| Many-to-one / one-to-many | orthogonal bus | One trunk plus short branches |
| Feedback, retry, recovery | curved | Run outside the main path |
| Weak influence / optional relation | curved or dashed | Keep away from primary labels |

## Topology before geometry

1. Identify one dominant main path.
2. Partition branches into non-overlapping zones.
3. Choose node ports before placing connectors.
4. Reserve connector channels between rows, columns, and layers.
5. Replace radial hub webs with a router/bus pattern.
6. Put return paths on the outside edge, not through the main flow.
7. Split the diagram if any relationship remains ambiguous after routing.

## Hard failures

- A connector crosses an unrelated node or text region.
- Two primary connectors cross.
- An arrow starts or ends in empty space without an intentional gate/bus.
- Layer spacing leaves no dedicated connector channel.
- A straight diagonal is used where an orthogonal or curved route is needed to preserve reading order.
- A route is assembled from multiple line objects plus a detached arrowhead.

## Verification

For every complex diagram page:

1. Render the page immediately after construction.
2. Inspect at readable scale, not only in a whole-deck contact sheet.
3. Confirm source, destination, direction, route type, and main path.
4. Confirm the connector does not cross text, nodes, or another primary connector.
5. Confirm OOXML endpoint binding and an arrow end on the connector object when native editability is claimed.
