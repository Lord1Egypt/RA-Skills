# Scope and limitations

Fly Coworker is a connectome-based novelty task picker. Task labels never enter its neural circuit; it does not understand or evaluate your work.

- DesktopFly’s 1,045-neuron MaleCNS circuit contains 17,224 measured connection rows. Modeled motor activity drives browser-local movement.
- FlyGym/NeuroMechFly anatomy supplies the body. Gait and movement are animated, not MuJoCo physics.
- Measured MaleCNS anatomy provides 114 neuropil regions and 166 active circuit-neuron skeletons for visualization. Gray regions do not add simulated neurons.
- LIF physiology, artificial neural inputs, task-sector mapping and outward movement bias are modeled. Selection is not claimed to be uniformly random.
- The fly is not a full Eon/Flyhard brain and no cognition, learning or biological fidelity is claimed.

## Interaction

Provide 2–64 distinct tasks, 1–300 characters each. Vetoing excludes the selected task and starts a fresh flight. Accepting submits only the chosen task to the owning OpenClaw conversation with its existing permissions. A durable one-time claim prevents duplicate handoffs. A run receipt proves dispatch, not successful task completion.

The dashboard plugin is the supported workflow. The optional standalone development viewer only saves a local result; it does not dispatch work. No calendar, email, social account or task-system import is included.

macOS/Chrome is verified; Linux, Windows and authenticated HTTPS deployment are unverified. Native Mac WebKit over loopback HTTP has a known plugin-cookie issue; use Chrome without weakening authentication.
