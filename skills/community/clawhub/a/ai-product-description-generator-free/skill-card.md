## Description: <br>
Generate product descriptions using free AI backends: Ollama locally or HuggingFace Inference API online. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[loutai0307-prog](https://clawhub.ai/user/loutai0307-prog) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and ecommerce teams use this skill to generate ready-to-use product copy from a product name and feature list without paid API keys. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Product names and feature details may be sent to HuggingFace-hosted infrastructure when the HuggingFace backend is selected. <br>
Mitigation: Use the default Ollama backend for private or unreleased products, and use HuggingFace only when sharing those inputs with hosted infrastructure is acceptable. <br>
Risk: Runtime environments may contain unrelated secrets alongside the optional HuggingFace token. <br>
Mitigation: Run the skill with only the environment variables it needs, such as HF_TOKEN when using HuggingFace, and avoid exposing unrelated credentials. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/loutai0307-prog/ai-product-description-generator-free) <br>
- [BytesAgain homepage](https://bytesagain.com) <br>
- [BytesAgain feedback](https://bytesagain.com/feedback/) <br>
- [Ollama](https://ollama.ai) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown-style product copy with a title, short description, and feature bullets, plus command-line status text.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports professional, casual, and SEO styles; local Ollama is the default backend and HuggingFace is optional.] <br>

## Skill Version(s): <br>
2.0.1 (source: server release and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
