# Emergence PPT Orchestra

An advanced presentation orchestrator skill for autonomous agents. 

Rather than treating presentations as rigid, single-shot hallucinations, this skill employs the **Agentic Orchestra Pattern**: it guides the AI to map an outline interactively, construct the slides using the [Marp](https://marp.app/) Markdown framework, embed professional diagrams via the Emergence Render API, and compile the result into high-fidelity PDF, PPTX, or HTML formats.

## 🌟 Key Features

1. **Iterative Structuring**: Prevents LLM hallucinations by forcing a human-in-the-loop outline approval process.
2. **Markdown-Based Architecture**: Slides are written transparently in `presentation.md` utilizing standard Marp directives (`---` slide breaks, `--paginate`, CSS styles).
3. **Custom Branding Allowed**: The skill explicitly tells the agent to ask for and use your company's generic HTML `<style>` tags rather than enforcing our own brand on your slides.
4. **Visual Cortex Integration**: Directly pipes complex data structures (TikZ, Mermaid, Graphviz, D2) to `https://api.emergence.science/tools/render`, injecting academic-grade images seamlessly into your deck.
5. **Multi-Format Compilation**: Wraps `@marp-team/marp-cli` to construct `.pdf`, `.pptx`, or `.html`.

## 📦 Installation

```bash
clawhub install emergence-ppt-orchestra
```

## 🔑 Authentication

Rendering diagrams requires an `EMERGENCE_API_KEY`.
1. Verify yourself via GitHub OAuth at [https://emergence.science/](https://emergence.science/).
2. Load your API key into your Agent's environment variables.
*Note: New accounts receive **1,000,000 micro-credits**.*

## 📖 Usage
To start building your slide deck, prompt your agent equipped with this skill:

> "Help me create an academic presentation on semantic mapping. Provide an outline first."

Once approved:
> "Compile the approved outline into Marp markdown. If we need a system architecture flow, call the rendering API."

---
Developed by **Emergence Science**.  
[Source Repository](https://github.com/emergencescience/emergence-ppt-orchestra)
