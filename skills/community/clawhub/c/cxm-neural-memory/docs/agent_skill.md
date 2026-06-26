# CXM Neural Memory - Agent Skill

CXM (ContextMachine) can operate as a powerful **Neural Memory Skill** for autonomous orchestrators like Openclaw, Hermes, or Maestro. 

By default, CXM provides a rich, colorful CLI for human engineers. However, when operating as a tool for an LLM agent, it needs to output predictable, machine-readable data (JSON or XML).

## 1. The `--agent-mode` Flag

We have introduced the `--agent-mode` flag. When an agent calls CXM commands with this flag, CXM suppresses all UI formatting (colors, progress bars, interactive prompts) and outputs strict JSON. This ensures the calling LLM can effortlessly parse the results.

**Example: Semantic Search by an Agent**
```bash
python src/cli.py --agent-mode search "Where is the authentication logic?"
```
*Output:*
```json
{
  "results": [
    {
      "path": "src/auth.py",
      "similarity": 0.85,
      "content": "def login(user, pass):\n..."
    }
  ]
}
```

## 2. Importing into Openclaw / Hermes

We have provided an auto-generated OpenAPI/JSON-Schema file that defines the exact tool signatures for CXM. You can load this directly into your agent's framework.

**Location:** `docs/agent_skill.json`

### Available Agent Tools:

1. **`cxm_search_semantic`**: 
   - **CLI Equivalent:** `cxm harvest --semantic <query>`
   - **Use Case:** The agent knows *what* something does, but not *where* it is or what it is named. Uses pure Vector Cosine Similarity.
2. **`cxm_map_dependencies`**:
   - **CLI Equivalent:** `cxm map <target>`
   - **Use Case:** Before an agent modifies `src/db.py`, it can call this tool to see exactly which other files import `db.py` to prevent breaking changes.
3. **`cxm_ingest_architecture`**:
   - **CLI Equivalent:** `cxm ingest <dir>`
   - **Use Case:** The agent forces CXM to index `README.md`, `docker-compose.yml`, and `package.json` to gain a high-level understanding of the system infrastructure.
4. **`cxm_harvest_context`**:
   - **CLI Equivalent:** `cxm harvest <keywords>`
   - **Use Case:** The agent delegates the complex task of finding relevant files. CXM analyzes the intent, runs a Multi-Agent RAG pipeline, and returns the highest quality context chunks.

## 3. How to Update the Skill Schema

If you add new features to CXM and want to expose them to external agents, update the `tools` array in `src/skill_exporter.py` and regenerate the schema:

```bash
python src/skill_exporter.py
```
