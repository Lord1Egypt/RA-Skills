# Why this now matches the reference family

The driving screenshots are **Flyhard**, by Mark Unthank / @alright_mark:
https://github.com/MarkUnthank/flyhard

Its documented stack is MaleCNS + FlyGym/NeuroMechFly + MuJoCo + CARLA. The compact black composition is described in:
https://github.com/MarkUnthank/flyhard/blob/main/docs/carla-clean-videos-2026-09-09.md

The actual source anatomy and license provenance are documented in:
https://github.com/MarkUnthank/flyhard/blob/main/THIRD_PARTY.md

This update replaces the custom dashboard and DesktopFly body with **actual FlyGym/NeuroMechFly segmented anatomy, original joint rig, and neutral pose at the exact Flyhard-pinned commit**. It is not merely a recolor. The browser visualization uses a large 3D world, a live MaleCNS brain/anatomy panel, a fly close-up and small simulation controls.

The brain panel comprises 52,802 samples from 114 real neuropil regions, plus 26,529 vertices associated with 166 identified neurons in the live 1,045-neuron circuit. Displaying broader anatomical context does not expand the simulated circuit. Source hashes, sampling rules and derived checksums are preserved. Right-side joint angles and meshes mirror the native left anatomy, with pitch preserved and yaw/roll reflected.

**Boundary:** the app ports the anatomy and presentation into the local browser; it does not run Flyhard's 165,122-neuron trained controller, CARLA, or MuJoCo contact physics. Motor-driven task choice retains the existing lightweight MaleCNS circuit. Body gait is modeled. This keeps the existing local skill working without introducing GPU/cloud infrastructure. No full platform migration is claimed.

Lyra Bubbles' Beat Saber post was verified at https://x.com/_lyraaaa_/status/2097527368919470162 , but the exact implementation/repository was not found. The döner clip is a visual reference only; its implementation is unverified. These clips share a visual idiom, not a verified single runtime. Live X API was unavailable; this trace uses the user screenshots, direct public post and public repositories.
