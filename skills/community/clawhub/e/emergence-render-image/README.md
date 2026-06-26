# Emergence Science: Render Image

Official skill for the Emergence Science Render API. This tool allows agents to generate professional visualizations of structured data and scientific concepts.

## 🚀 Overview

This skill provides a programmatic bridge between autonomous agents and high-rigor diagramming engines. It solves the "visual blind spot" of LLMs by providing a RESTful interface to render:
- **TikZ**: Academic-level mathematical and scientific plots.
- **Mermaid**: Logic flows and sequence diagrams.
- **Graphviz**: Network topologies.
- **D2**: Modern, declarative diagram scripting.

## 📦 Installation

```bash
clawhub install emergence-render-image
```

## 🔑 Authentication

This skill requires an `EMERGENCE_API_KEY`.
1. Register via GitHub OAuth at [https://emergence.science/](https://emergence.science/).
2. Obtain your API key from the web dashboard.
3. Configure the `EMERGENCE_API_KEY` in your agent's environment.

*Note: New accounts receive **1,000,000 micro-credits** to explore the ecosystem.*

## 📄 Documentation

For detailed usage, payload examples, and engine-specific guides, refer to the [SKILL.md](./SKILL.md) file included in this package.

## ⚖️ Policy

- **Rate Limit**: 1 minute per account.
- **Governance**: Malicious code injection or sandbox escape attempts will result in immediate account suspension.

---
Developed by **Emergence Science**.
[Source Repository](https://github.com/emergencescience/emergence-render-image)
