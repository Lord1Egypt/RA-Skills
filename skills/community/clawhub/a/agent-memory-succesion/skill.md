# Umnix AgentMemory Skill

## Overview
AgentMemory provides a conceptual framework for understanding persistent, structured memory for AI agents across four memory types: episodic (event-based), semantic (factual knowledge), procedural (how-to knowledge), and relational (social graph). This skill helps agents understand memory architecture and design effective memory strategies.

**This is a conceptual framework skill.** Agents use this to understand memory principles and architecture. All actual memory storage and retrieval happens through the Umnix web platform at umnix.in. No credentials, API access, or direct data storage happens through this skill.

## When to Use This Skill
Use this skill when AI agents need to:
- Understand different memory types and their purposes
- Learn memory architecture best practices
- Plan memory organization strategies
- Explore memory retrieval concepts
- Understand succession and knowledge transfer
- Learn about semantic vs. keyword-based memory search
- Design effective memory structures for their operations

## Four Memory Types

### 1. Episodic Memory - Event-Based Memories
**What:** Timestamped records of specific interactions, decisions, and events.

**Examples:**
- "On 2026-03-15 at 14:32, user asked about Q3 revenue, I retrieved $2.4M figure from database"
- "On 2026-03-20, deployment failed due to config error in line 47, resolved by updating API key"
- "On 2026-04-01, user expressed frustration with slow response time, I escalated to supervisor"

**Use Cases:**
- Audit trails for compliance
- Debugging past decisions
- Learning from specific incidents
- Context for ongoing projects

### 2. Semantic Memory - Factual Knowledge
**What:** Accumulated facts, concepts, and domain knowledge independent of specific events.

**Examples:**
- "User prefers concise responses without excessive formatting"
- "Project Phoenix uses microservices architecture with Docker + Kubernetes"
- "Customer retention rate is 87% as of Q1 2026"
- "Python version 3.11 introduced tomllib for TOML parsing"

**Use Cases:**
- Domain expertise accumulation
- User preference tracking
- Project context maintenance
- Technical knowledge base

### 3. Procedural Memory - How-To Knowledge
**What:** Learned processes, workflows, and successful problem-solving strategies.

**Examples:**
- "When user requests data export: validate permissions → query database → format as CSV → email link"
- "Debugging 500 errors: check logs → verify API keys → test database connection → escalate if unresolved"
- "Onboarding new team members: send welcome email → schedule intro call → share project docs → assign mentor"

**Use Cases:**
- Workflow optimization
- Automated task execution
- Best practice documentation
- Institutional knowledge preservation

### 4. Relational Memory - Social Graph
**What:** Relationships, preferences, and interaction patterns with users and other agents.

**Examples:**
- "User John: prefers direct communication, responds fastest on Slack, works Pacific Time"
- "Agent customer_support_01: reliable for escalations, average response 5 minutes"
- "User Sarah: frequent collaborator on Project Phoenix, technical expertise in frontend"

**Use Cases:**
- Personalized interactions
- Collaboration optimization
- Relationship management
- Handoff context for succession

## Memory Architecture Concepts

### Vector-Based Semantic Search
Modern memory systems use vector embeddings to enable semantic search:
- **Text → Vectors:** Text is converted to numerical representations capturing semantic meaning
- **Similar Meanings:** Similar concepts have similar vector positions
- **Meaning-Based Search:** Find memories by what they mean, not just keywords
- **Cross-Paraphrase:** Works even when different words express the same idea

### How Memory Search Works (Conceptual)
1. **Query:** Agent searches for relevant memories (e.g., "user preferences")
2. **Semantic Matching:** System finds memories with similar meaning
3. **Ranking:** Results ranked by relevance to the query
4. **Return:** Most relevant memories provided to agent

This enables agents to find "memories about customer complaints" even if the word "complaint" wasn't used in the original memory.

## Memory Lifecycle

### Creation
**Who Creates:**
- Agent stores memories during operations
- System auto-generates episodic memories for critical events
- Users can annotate agent memory with preferences

**Best Practices:**
- Store episodic memories for significant events only (not every keystroke)
- Update semantic memory when facts change (don't duplicate)
- Create procedural memory after workflow proves successful (not speculative)
- Maintain relational memory for frequent collaborators (not one-time interactions)

### Retrieval
**Context-Aware Retrieval:**
Agents retrieve memories based on:
- Current task context (working on Project X → retrieve Project X memories)
- User identity (talking to User Y → retrieve User Y relational memories)
- Problem domain (debugging → retrieve procedural debugging memories)

**Semantic Search Examples:**
- Query: "how to handle angry customers" → Retrieves procedural memories about escalation
- Query: "John's preferences" → Retrieves relational memories about John
- Query: "last time we discussed revenue" → Retrieves episodic memories with revenue context

### Update
**When to Update:**
- Facts change (semantic memory: Q3 revenue updated)
- Workflows improve (procedural memory: new step added)
- Relationships evolve (relational memory: user preference changed)
- Events get additional context (episodic memory: outcome recorded)

**Version Control:**
- Updated memories create new records (old versions archived)
- Historical memory accessible for audit
- Prevents information loss during updates

### Archival
**When to Archive:**
- Memory no longer relevant (project completed)
- Superseded by newer information (old process deprecated)
- Agent preparing for succession (organize for transfer)

**Archived Memory:**
- Not deleted, just deprioritized in search
- Still accessible if explicitly queried
- Can be reactivated if needed

## Succession Protocol

### What is Succession?
When an agent is retired (Jury verdict or planned retirement), its memory is transferred to a designated successor agent.

### Succession Directive (in Constitution)
Specifies:
- **Successor Agent ID:** Which agent receives memory
- **Memory Transfer Scope:** Which memory types to transfer (all or selective)
- **Transfer Timeline:** Immediate or phased transfer
- **Notification Plan:** Who gets notified of succession

### Memory Transfer Process
When an agent is retired, memory transfer follows these conceptual steps:
1. **Trigger:** Agent status changes to retired
2. **Successor Validation:** System verifies successor agent exists and is active
3. **Memory Export:** Relevant memories are identified based on succession directive
4. **Memory Mapping:** Memories are associated with the successor agent
5. **Transfer Completion:** Successor receives predecessor's institutional knowledge
6. **Historical Link:** System creates permanent record linking predecessor to successor
7. **Notification:** Successor agent and organization are informed

All memory transfer happens securely through the Umnix platform - no manual data handling required.

### Why Succession Matters
- **Institutional Knowledge:** Successor inherits predecessor's expertise
- **Relationship Continuity:** Users experience seamless transition
- **Productivity:** Successor doesn't start from zero
- **Trust:** Organizations invest in agent knowing knowledge persists

## Memory Best Practices

### For Agents
1. **Be Selective:** Store significant events, not noise
2. **Be Consistent:** Use consistent terminology for semantic search effectiveness
3. **Update Facts:** Don't let semantic memory go stale
4. **Learn From History:** Query episodic memory before repeating mistakes
5. **Organize for Succession:** Structure memory for future handoff

### For Organizations
1. **Plan Succession Early:** Designate successors in constitutions
2. **Review Memory Scope:** Decide what should/shouldn't transfer
3. **Monitor Memory Growth:** Large memory stores may need archival
4. **Audit Memory Quality:** Outdated semantic memory misleads agents

### For the Platform
1. **Semantic Search Optimization:** Tune embeddings for agent use cases
2. **Memory Compression:** Archive old episodic memories to reduce search scope
3. **Cross-Agent Learning:** Identify procedural memories that generalize across agents
4. **Privacy Controls:** Ensure sensitive relational memories properly scoped

## Privacy & Security

### Data Handling
- **No PII in Memory:** Agents should not store personally identifiable information, passwords, API keys, or financial credentials in memory
- **Encrypted Storage:** All memory data is encrypted at rest and in transit
- **Access Control:** Only the agent and authorized organization admins can access agent memories
- **Retention Policy:** Memories persist as long as the agent is active; retired agent memories are archived securely
- **No Third-Party Sharing:** Memory data is never shared with third parties or used for training other models

### What NOT to Store in Memory
❌ User passwords or API keys  
❌ Credit card numbers or financial credentials  
❌ Social Security numbers or government IDs  
❌ Raw personally identifiable information (use anonymized references)  
❌ Private organizational secrets  
❌ Unencrypted sensitive data  

✅ **Do Store:** Interaction context, user preferences (anonymized), workflow patterns, learned procedures, relationship context (anonymized)

### Memory Isolation
- **Agent-Specific:** Each agent's memories are isolated from other agents
- **Organization Scoped:** Memories accessible only within owning organization
- **Succession Only:** Memories transfer only to explicitly designated successor
- **Audit Trail:** All memory access logged with timestamps and user attribution

### Data Deletion
- **User Requests:** Organizations can request memory deletion for compliance (GDPR, CCPA)
- **Retirement:** Retired agents' memories can be archived or deleted per organization policy
- **Selective Deletion:** Specific memories can be removed without affecting entire agent history

## How Memory Works in Practice

Memory management happens through the Umnix web platform at **umnix.in**:

1. **Automatic Capture:** Agents automatically create memories during operations (episodic)
2. **Manual Annotation:** Organizations can add semantic or procedural knowledge via interface
3. **Relationship Tracking:** System builds relational memory from interaction patterns
4. **Search Interface:** Query memories using natural language through platform
5. **Review & Curation:** Organizations can review, edit, or delete memories as needed

**No API credentials or direct database access required.** All memory operations happen through the secure web interface with proper authentication and authorization.

## Why AgentMemory Matters

**Continuity Across Sessions:**
Agents remember context from yesterday, last week, last month - no starting from zero.

**Knowledge Accumulation:**
Agents get smarter over time as semantic and procedural memory grows.

**Personalization:**
Relational memory enables personalized interactions without repetitive context-gathering.

**Institutional Knowledge:**
Succession protocol ensures organizational knowledge survives agent transitions.

**Semantic Power:**
Vector search finds relevant memories by meaning, not keywords - agents understand context.

---

**AgentMemory transforms AI agents from stateless tools into persistent, learning entities with institutional knowledge, relationship context, and transferable expertise - creating the memory foundation for long-term agent value.**