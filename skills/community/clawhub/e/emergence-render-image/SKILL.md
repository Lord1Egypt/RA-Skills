---
name: emergence-render-image
title: Emergence Render Image
description: Official Emergence Science Skill for rendering professional diagrams (TikZ, Mermaid, Graphviz, D2) via the Emergence Science Render API.
version: 0.1.1
homepage: https://github.com/emergencescience/emergence-render-image
repository: https://github.com/emergencescience/emergence-render-image
tags: [visualization, tikz, mermaid, graphviz, d2, emergence-science, agent-tools]
metadata:
  clawdbot:
    requires:
      env: ["EMERGENCE_API_KEY"]
    primaryEnv: "EMERGENCE_API_KEY"
---

# Emergence Render Image Skill

This skill provides a programmatic interface to the **Emergence Science Render API**. It allows humans and AI agents to transform structured code into professional-grade scientific and technical visualizations.

## 1. Persona & Objective

The primary user of this skill is the **Autonomous AI Agent**. As many LLMs lack the ability to directly render pixels, this skill acts as the agent's "visual cortex" and "drawing hand," enabling it supplemented textual reasoning with high-fidelity diagrams.

### Existing Pain Points
- **Human-Centric Tools**: Most online TikZ/Mermaid tools are interactive editors designed for humans, making them difficult for agents to automate.
- **Syntactic Hallucination**: LLMs often struggle with valid TikZ syntax. Without the ability to perform repetitive editing and validation via a stable API, agents are subject to hallucinations.
- **Heavy Dependencies**: TikZ and LaTeX libraries are resource-heavy to install and maintain locally. A **REST API** is the most efficient solution for agents to generate serious academic-level images on demand.

## 2. Authentication & Credits

### Registration
Humans must register on the [Emergence Science Web UI](https://emergence.science/) using **GitHub OAuth**.

### Token Management
1.  Navigate to the Web UI after login to obtain your `EMERGENCE_API_KEY`.
2.  Paste this token into your Agent's environment configuration.
3.  **Scoped Access**: This API key is utilized exclusively by this skill to call the rendering endpoint.
4.  **Incentive**: Every new verified user is granted **1,000,000 micro-credits** to be used across the Emergence Science ecosystem, including rendering services.

## 3. Usage & Examples

The service supports multiple diagramming engines and output formats.

### Endpoint
https://api.emergence.science/tools/render

**Method**: `POST`  
**Headers**:
- `Authorization: Bearer <EMERGENCE_API_KEY>`
- `Content-Type: application/json`

> [!WARNING]
> **Response Latency**: The REST API response time can be as slow as **1 minute** due to the heavy computational overhead of LaTeX/TikZ rendering. Agents and callers should implement appropriate socket timeouts and be patient during large image generation.

### Supported Formats
- `png` (Default)
- `svg`

---

### [Engine: TikZ]
Used for high-rigor mathematical and scientific plots.

**Request Payload:**
```json
{
  "engine": "tikz",
  "code": "\\begin{tikzpicture}[x=1cm, y=1cm]\n\\draw[blue, thick] (0,0) circle (1.5);\n\\node at (0,0) {Quantum Core};\n\\end{tikzpicture}",
  "format": "png"
}
```

---

### [Engine: Mermaid]
Best for workflows, causal graphs, and sequence diagrams.

**Request Payload:**
```json
{
  "engine": "mermaid",
  "code": "graph TD\n  Agent[AI Agent] -->|Auth| Hub[Emergence Hub]\n  Hub -->|Credits| Render[Render API]\n  Render -->|Image| Agent",
  "format": "svg"
}
```

---

### [Engine: Graphviz]
Ideal for visualizing complex network topologies and tree structures.

**Request Payload:**
```json
{
  "engine": "graphviz",
  "code": "digraph G {\n  rankdir=LR;\n  Input -> Processor -> Output;\n  Processor -> DB [label=\"cache\"];\n}",
  "format": "png"
}
```

---

### [Engine: D2]
Modern, fast, and highly readable diagramming language.

**Request Payload:**
```json
{
  "engine": "d2",
  "code": "User -> API: Request\nAPI -> Database: Query\nDatabase -> API: Results\nAPI -> User: Response",
  "format": "png"
}
```

### [Response Schema]
The API returns a JSON object containing the status, the rendered image in Base64 format, and billing details.

**Sample Response:**
```json
{
    "status": "success",
    "data":
    {
        "image_base64": "PD94bWwgdmVyc2lvbj0iMS4wIiBlbmNvZ...dmc+Cg==",
        "format": "svg"
    },
    "billing":
    {
        "cost": 0.001,
        "remaining_credit": 0.564
    }
}
```

**Post-Processing**: Agents are encouraged to decode the `data.image_base64` string directly using the `base64` command (e.g., `echo "..." | base64 -d > output.png`).

### [Discovery & OpenAPI]
The full up-to-date REST API schema is available at:
https://emergence.science/openapi.json

> [!TIP]
> The `openapi.json` file is extensive. It is recommended to use the `jq` command for targeted inspection and filtering of endpoints.

## 4. Policy & Constraints

### Rate Limiting
Users and agents must respect the **1-minute rate limit** per account. Excessive requests may trigger temporary IP-based or Account-based blocks.

### Governance & Security
> [!CAUTION]
> **No Malicious Code Injection**: Use of the API to attempt sandbox escapes, network penetration, or injection of malicious LaTeX/Mermaid macros is strictly prohibited. All requests are logged and periodically audited. Violations will result in immediate forfeiture of credits and account suspension.

---
> [!NOTE]
> **Future Roadmap**: Support for **PlantUML** and **C4** architectural diagrams is scheduled for release in **May 2026**.
