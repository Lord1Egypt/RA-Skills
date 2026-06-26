Use the $kai-business-blueprint skill to create a business capability blueprint from these retail notes.

Output requirements:
- Save all generated artifacts under {artifact_dir}.
- Create `solution.blueprint.json`.
- Export SVG and HTML viewer artifacts.
- Use the `retail` industry template.
- Do not invent missing numbers or systems.

Source notes:
- Stores use POS for checkout, CRM for membership, OMS for fulfillment, and WMS for inventory.
- Current pain: store associates cannot see online order status during returns.
- Target capability: unified order lookup across channels.
- Required flow: customer return request -> associate lookup -> OMS validation -> refund approval -> WMS restock update.
- Actors: customer, store associate, finance approver, warehouse operator.
