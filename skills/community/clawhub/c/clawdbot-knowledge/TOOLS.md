# TOOLS.md - Local Notes (Updated 2026-02-08 22:04 UTC)

Skills provide *how* tools work. This file is for *your* specifics — the stuff that's unique to your setup.

## What Goes Here

Things like:
- Camera names and locations
- SSH hosts and aliases
- Preferred voices for TTS
- Speaker/room names
- Device nicknames
- Anything environment-specific

## Tools Extracted from 20 SKILLs

### 🧠 MEMORY TOOLS

**A. ChromaDB Memory**
- `chromadb_search(text, limit, collection_id)` - Semantic search over memory
- `memory_recall(query, limit, autoRecall)` - Automatic context recall
- `memory_store(text, category, importance, minScore)` - Store new memories
- `autoRecallResults` - Config: max recall per turn (default 3)
- `minScore` - Config: minimum similarity (default 0.5)

**B. Elite Longterm Memory (6-Layer Architecture)**
- `SESSION-STATE.md` - Hot ram layer (survives compaction)
- `memory_store(text, category, importance)` - Store decision/learning
- `wal_store(record)` - Write-Ahead Log protocol
- `memory_recall(query, limit)` - Query semantic memory
- `super_memory_api_store()` - Cloud backup (optional)

**Layers:**
1. Hot RAM - SESSION-STATE.md
2. Warm Store - LanceDB Vectors
3. Cold Store - Git-Notes Knowledge Graph
4. Curated Memory - MEMORY.md (human-readable)
5. Cloud Backup - SuperMemory API

### 🤖 MULTI-AGENT TOOLS

**C. SuperAgent (8 Agents)**
- `Watcher Mode` - System health monitoring, error detection
- `Assistant Mode` - General questions, information retrieval
- `Analyzer Mode` - Complex task decomposition, risk assessment
- `Planner Mode` - Detailed execution plans
- `Fixer Mode` - Error diagnosis, recovery
- `Architect Mode` - System architecture, scalability
- `Coder Mode` - Code generation, implementation
- `Researcher Mode` - Trend analysis, feasibility studies

**D. Autonomous Worker Agent**
- `create_worker(name, role, capabilities)` - Create specialized worker
- `create_task(name, description, priority, metadata)` - Define structured tasks
- `assign_task(task, worker)` - Intelligent task distribution
- `execute_task(task)` - Autonomous execution
- `coordinate_workers(agents, task)` - Multi-agent coordination
- `monitor_agents()` - Real-time performance monitoring

**E. Sub-Agent Manager**
- `create_sub_agent(config)` - Dynamically create sub-agents
- `coordinate_agents(agents, task)` - Multi-agent orchestration
- `monitor_agents()` - Performance measurement
- `integrate_agents(agent)` - Into Super-Skill ecosystem
- `agent_allocator()` - Dynamic resource allocation

**F. MCP Orchestral (27-28 Super-Agents)**
- `deep_master_agent_integration()` - JSON modules + Flowise
- `mcp_server_integration()` - File organization + MongoDB
- `flowise_orchestration()` - Workflow orchestration
- `coordinate_agents(workflows)` - Multi-agent coordination
- `mongodb_integration()` - Database management
- `multi_agent_orchestrator()` - Central coordination

### 🧠 NEURAL & AI TOOLS

**G. Deepsynaptica**
- `NeuralProcessor.load_model(path)` - Load neural network models
- `NeuralProcessor.analyze_synaptic_connections(network)` - Architecture analysis
- `DeepAllIntegration.real_agent_neural_processing(input, params)` - Real-time processing
- `Meta-block neural logic` - Conditional neural pathways
- `Weight optimization` - Synaptic-level processing

**H. Axiomata (Axiomatic Intelligence)**
- `AxiomataSystem.process_input(text)` - Axiomatic processing
- `AxiomataSystem.calculate_i_evo(logic, ethos)` - Integrity score calculation
- `I_Evo = (Logic + Ethos) / (Ego + 10^-9)` - Core formula
- `paradox_detection()` - Detect logical contradictions
- `omega_trigger()` - Handle high logical entropy

**I. SuperSkill (RUI+ARS+MIRAS+AIXI+DeepSynaptica)**
- `RUI-ARS-Integration()` - Resilient universal intelligence
- `MIRAS-Holonomic-Processing()` - Multi-dimensional holonomic logic
- `AIXI-Universal()()` - Universal intelligence with expected cumulative return
- `Teleological_Attractor()` - Goal-oriented decision making
- `Phase_Omega()` - Absolute phase processing

**J. CellCog (Any-to-Any AI)**
- `create_chat(prompt, notify_session_key, task_label)` - Fire-and-forget
- `prompt = "Analyze multiple files together"` - Multi-file analysis
- `request = "Create PDF + HTML + Video + PPTX outputs"` - Multiple outputs
- Supports: PDF, Excel, Images, Audio, Video, Code files

### 🧰 DEVELOPMENT TOOLS

**K. Codex Helper**
- `complete_code(prefix, language)` - Intelligent code completion
- `fix_syntax_errors(code)` - Syntax error detection & fixing
- `suggest_improvements(code)` - Code quality suggestions
- `explain_code(code, line_range)` - Code explanation
- `refactor(code, operation)` - Refactoring support
- Languages: Python, JavaScript/TypeScript, Java, Go, Rust, C/C++

**L. Dash Cog (CellCog-based)**
- `create_dashboard(type, data, options)` - Analytics dashboards
- `create_kpi_tracker(metrics)` - KPI monitoring
- `create_chart(type, data, options)` - Interactive charts
- `create_data_explorer(dataset)` - Dataset exploration
- `create_calculator()` - Interactive calculators
- `create_quiz()` - Quiz applications

### 🖥️ INFRASTRUCTURE TOOLS

**M. MCP Management (MCPorter)**
- `mcporter list` - List all MCP servers
- `mcporter call server.tool key=value` - Call MCP tools
- `mcporter auth server [--reset]` - OAuth authentication
- `mcporter daemon start/stop/status` - MCP daemon management
- `mcporter generate-cli --server <name>` - Generate CLI tool
- `mcporter emit-ts <server> --mode client` - Generate TypeScript types

**N. OpenClaw Sandbox**
- `openclaw sandbox list [--browser]` - List container status
- `openclaw sandbox recreate --all` - Recreate all containers
- `openclaw sandbox recreate --session <name>` - Recreate specific session
- `openclaw sandbox explain --session <name>` - Show effective policy

**O. Model Switcher**
- `list models` - List all available models (OpenRouter + Ollama)
- `set main model <model>` - Change main model
- `show config` - Show current configuration
- `test model <model>` - Test model response time
- Models: Qwen3 Coder 30B, Mistral 7B, GPT-OSS 20B, DeepSeek R1 8B

### 🗣️ VOICE TOOLS

**P. SpeakMCP (Voice Powered AI)**
- `Voice Input` - Speech recognition (WebRTC/Native)
- `LLM Processing` - Multi-LLM support (OpenAI, Groq, Gemini)
- `MCP Client` - Tool discovery & execution
- `Cross-platform` - macOS, Windows, Linux
- `Shortcut driven` - Keyboard shortcut control

### 🔄 SYSTEM TOOLS

**Q. ClawD Architecture Tools**
- `agent RPC` - Agent execution API
- `agent.wait` - Wait for agent completion
- Gateway WebSocket API - Typed WS API
- `bootstrap` injection - System prompt composition
- `workspace management` - Single workspace directory
- `tool execution` - File tools + context

**R. FATONI Meta-Intelligence Tools**
- `Pattern Recognition Engine` - 97%+ accuracy
- `Manipulation Detection Framework` - 5-level detection
- `Meta-Intelligence Engine` - Meta-meta analysis
- `Real-time Dashboard` - Live analytics
- `Optimization Engine` - Continuous improvement

## Your Specific Tools

### Chat Systems
- (Check: Signal, Telegram, Slack, Discord, WebChat are handled by Gateway)

### SSH Access
- Check: Which hosts do you have access to?

### TTS Voices
- Preferred voice: (From AGENTS.md: ask Toni)

### Device Names
- (Fill in your specific environment setup)

## How to Use These Tools

**For Memory:**
```python
from chromadb_memory import ChromaDBMemory
memory = ChromaDBMemory()
memory.store("User prefers dark mode", category="preference", importance=0.9)
results = memory.recall("preferences", limit=5)
```

**For Multi-Agent:**
```python
from autonomous_worker import AutonomousWorkerAgent
agent = AutonomousWorkerAgent("production-agent")
worker = agent.create_worker(name="QA", capabilities=["test", "validate"])
task = agent.create_task("Test authentication", priority=10)
agent.execute_task(task)
```

**For Code:**
```python
from codex_helper import CodexHelper
helper = CodexHelper()
completions = helper.complete_code("def calculate_", language="python")
fixes = helper.fix_syntax_errors("code_with_errors")
```

**For MCP:**
```bash
mcporter call mcp-server.tool parameter=value
mcporter list
mcporter auth mcp-server
```

## Tool Categories Summary

1. **Memory (3 tools)** - ChromaDB, Elite Longterm, Auto-recall
2. **Multi-Agent (6 tools)** - SuperAgent, Autonomous Worker, Sub-Agent, MCP Orchestral
3. **Neural/AI (5 tools)** - Deepsynaptica, Axiomata, SuperSkill, CellCog
4. **Development (2 tools)** - Codex Helper, Dash Cog
5. **Infrastructure (3 tools)** - MCP Manager, OpenClaw Sandbox, Model Switcher
6. **Voice (1 tool)** - SpeakMCP
7. **System (2 tools)** - ClawD Architecture, FATONI

**Total: 22 Tool Categories / 50+ Individual Tools**

---

*Last Updated: 2026-02-21 11:43 UTC*  
*Mode: Fully Autonomous Learning*  
*🎯 Status: Enhanced ClawdBot 2.0.0 Ultimate MCP - Tools Integrated*  
*🚀 Ready to Use!*

---

## Dashboard Access

**Tokenized URL
