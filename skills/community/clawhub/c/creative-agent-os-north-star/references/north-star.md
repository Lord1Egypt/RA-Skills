# North Star

The target is a lightweight creative agent OS with these properties:

1. multi-user
2. ordinary-user oriented
3. lightweight
4. cloud sandbox based
5. built-in coding-agent capability
6. local filesystem memory
7. easy to add vertical domain agents
8. multimodal support beyond code and text
9. skill support
10. CLI surface for bridges into heavier agent systems

## Priority references

1. Nanobot
2. OpenClaw
3. Open Inspect / background-agents

## Simplified architecture rule

- runtime: learn from Nanobot
- cloud execution: learn from Open Inspect
- system shape: learn from OpenClaw
- coding engine: adapter, not hard-coded

## Drift signals

- too much local-only state
- coding engine assumptions leaking into product architecture
- adding a new app/agent requires deep framework surgery
- product is useful only to developers
- text-only assumptions block image/video workflows
- skills are bolted on instead of native

## Preferred corrections

- move engine specifics behind adapters
- keep orchestration thin
- define stable product primitives first
- add domain agents as first-class extensions
- keep deployment cloud-first unless a local exception is justified
