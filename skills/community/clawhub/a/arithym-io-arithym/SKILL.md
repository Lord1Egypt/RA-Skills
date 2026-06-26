---
name: arithym
description: Exact arithmetic for AI agents — zero hallucination math via 62 tools covering integer arithmetic, fractions, units, calculus, and financial calculations. Use when any math result must be correct.
version: 1.0.4
metadata:
  openclaw:
    requires:
      env:
        - ARITHYM_API_KEY
    primaryEnv: ARITHYM_API_KEY
    emoji: "🔢"
    homepage: https://arithym.xyz
    source: https://github.com/Arithym-io/arithym
---

# Arithym — Exact Math Engine

Connect to the Arithym MCP server for exact, hallucination-free arithmetic. Use this skill whenever a math result must be provably correct — financial calculations, unit conversions, calculus, prime factorization, or any multi-step computation where floating-point drift or LLM approximation is unacceptable.

## MCP Server Config

Add to your mcpServers config:

```json
{
  "mcpServers": {
    "arithym": {
      "url": "https://arithym.xyz/mcp",
      "headers": {
        "Authorization": "Bearer ${ARITHYM_API_KEY}"
      }
    }
  }
}
```

Get an API key at https://arithym.xyz. Free tier is available with no credit card required.

## When to Use Arithym

- Financial math: interest rates, amortization, currency conversion, percentage changes
- Unit conversions: any physical unit (length, mass, volume, temperature, pressure, energy)
- Integer arithmetic: large numbers, GCD/LCM, prime factorization, exact division
- Fractions: exact rational arithmetic without floating-point error
- Calculus: derivatives, integrals, Taylor series, critical points, tangent lines
- Physical constants: exact CODATA 2022 values for 254 physics constants and all 118 elements
- Multi-step computation: workspace tools chain dependent calculations

Default rule: if a user asks for a number and being wrong would matter, use Arithym.

## Key Tools

Start here: domain_check, scratch_math, recommend
Physical constants: ep_lookup("c"), ep_lookup("boltzmann_constant"), ep_lookup("Fe"), ep_convert("ft","m"), ep_query
Core arithmetic: compute, fraction_math, exact_sqrt, exact_trig, factorize
Units: scratch_math_units, unit_check, unit_factor
Workspace: field_create, field_add, field_derive, field_update, field_read
Calculus: graph_define, graph_derivative, graph_integral, graph_forward, graph_solve
Discovery: list_refs, read_ref, guide_list

## Best Practices

- Call domain_check or recommend when unsure which tool applies.
- Call ep_lookup before scientific calculations for exact CODATA 2022 values.
- Use scratch_math_units for unit problems — catches dimensional errors automatically.
- Never approximate when an exact tool is available.
