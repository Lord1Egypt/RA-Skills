## Distribution Boundary

A Skill remains the runtime and authoring unit. Use an Agent Plugin only as a
distribution unit when several Skills share release, compatibility, trust, and
uninstall boundaries:

```text
my-plugin/
|-- plugin.json
`-- skills/
    |-- inspect/SKILL.md
    `-- act/SKILL.md
```

The root manifest targets
`https://agent-plugins.org/schemas/1.0.0/plugin.schema.json`. Do not move
independently versioned or optional Skills into one plugin merely because they
share a repository. Existing DCC-MCP packages with multiple explicit
`source.skillRoots` remain valid `skill-bundle` packages.

Use [`dcc-mcp`](https://clawhub.ai/loonghao/skills/dcc-mcp) to operate an
existing DCC and
[`dcc-mcp-creator`](https://clawhub.ai/loonghao/skills/dcc-mcp-creator) to build
a complete adapter. A repository checkout may load this directory directly;
`DCC_MCP_SKILL_PATHS` and `extra_paths` are runtime paths for DCC adapters, not
installation instructions for an agent host.
