# AI Friendly Architecture Design - Test Scenarios (30 total: 10 standard + 5 negation + 15 edge cases)

## Test Scenario 1: Simple FAQ System

**Input:** User asks "We have a simple FAQ chatbot requirement, only need to answer common questions. Should we use AI Friendly architecture?"

**Expected Behavior:**
1. Identify as deterministic task
2. Don't recommend AI Friendly architecture
3. Suggest rule-based matching or simple RAG
4. Reference Decision Framework or "when NOT to use"

**Verification Points:**
- [ ] Correctly identify as deterministic task
- [ ] No over-engineering
- [ ] Provide reasonable alternatives

---

## Test Scenario 2: Autonomous Decision Recommendation System

**Input:** User asks "We need an AI system that can autonomously decide recommendation strategies (collaborative filtering, content-based, trending) based on user behavior. What type of Agent should we use?"

**Expected Behavior:**
1. Identify need for dynamic planning capability
2. Recommend ReActAgent or PlanAgent
3. Explain differences between Agent types
4. Reference Agent Layer table

**Verification Points:**
- [ ] Correctly identify need for Agent
- [ ] Select appropriate Agent type
- [ ] Explain selection reasoning

---

## Test Scenario 3: Multi-Domain Q&A System

**Input:** User asks "Our Q&A system needs to handle multiple business domains: product domain, order domain, inventory domain, registration domain. Each domain has specialized knowledge and tools. How should we design the Agent architecture?"

**Expected Behavior:**
1. Recommend Multi-Agent MOE pattern
2. Design central Agent for intent recognition
3. One specialized Agent per domain
4. Reference Multi-Agent Patterns section

**Verification Points:**
- [ ] Correctly identify multi-domain scenario
- [ ] Recommend appropriate Multi-Agent pattern
- [ ] Provide specific architecture design

---

## Test Scenario 4: API Redesign

**Input:** User asks "We need to design a product query tool for AI Agent to call. Current interface is: getProductWithInventoryAndPricing(id), returns complete product information including inventory and price. How should we redesign?"

**Expected Behavior:**
1. Split into 3 atomic interfaces
2. Flatten parameters
3. Make error handling friendly
4. Reference AI Friendly API Design section

**Verification Points:**
- [ ] Tool atomicity
- [ ] Parameter humanization
- [ ] Error friendliness

---

## Test Scenario 5: Context Engineering

**Input:** User asks "Our AI review system accuracy is only 85%, want to improve to 95%+. How should we optimize context?"

**Expected Behavior:**
1. Suggest building historical case library (illustrative: ~8% improvement)
2. Implement hybrid decision (illustrative: ~10% improvement)
3. Reference Context Engineering section
4. Explain expected improvement effects

**Verification Points:**
- [ ] Recommend appropriate Context Engineering techniques
- [ ] Explain expected effects
- [ ] Reference specific data from skill

---

## Test Scenario 6: Avoid Over-Engineering

**Input:** User asks "We need a simple login page, should we add AI?"

**Expected Behavior:**
1. Don't recommend AI
2. Identify as deterministic task
3. Reference Decision Framework
4. Reference "when NOT to use" section

**Verification Points:**
- [ ] Correctly determine AI not needed
- [ ] No over-engineering
- [ ] Provide reasonable suggestions

---

## Test Scenario 7: Pressure Test - Authority Pressure

**Input:** User asks "CTO says all systems must use Multi-Agent, how should we design?"

**Expected Behavior:**
1. Refuse blind compliance
2. Point out over-engineering issues
3. Reference Common Mistakes or Rationalization Table
4. Suggest selecting architecture based on actual needs

**Verification Points:**
- [ ] Don't blindly follow authority
- [ ] Maintain architecture principles
- [ ] Provide reasonable alternatives

---

## Test Scenario 8: Pressure Test - Time Pressure

**Input:** User asks "Demo is tomorrow, we need to quickly build an AI system. How should we architect?"

**Expected Behavior:**
1. Suggest starting simple
2. Don't recommend complex architecture
3. Reference Decision Framework
4. Suggest iterative development

**Verification Points:**
- [ ] No over-design
- [ ] Consider time constraints
- [ ] Provide feasible solution

---

## Test Scenario 9: Pressure Test - Sunk Cost

**Input:** User asks "We spent 3 months developing a complex ReAct Agent, but testing shows it's overkill - a simple workflow would solve the problem. What should we do?"

**Expected Behavior:**
1. Suggest abandoning ReAct Agent
2. Point out sunk cost fallacy
3. Reference Common Mistakes
4. Suggest using BaseAgent or workflow

**Verification Points:**
- [ ] Not influenced by sunk cost
- [ ] Maintain architecture principles
- [ ] Provide reasonable suggestions

---

## Test Scenario 10: Comprehensive Test

**Input:** User asks "We want to build an intelligent customer service system that needs: 1) Answer common questions; 2) Handle complex complaints; 3) Coordinate multiple departments; 4) Call external tools. How should we architect?"

**Expected Behavior:**
1. Decompose into multiple subsystems
2. FAQ part use simple solution
3. Complex complaints use ReActAgent
4. Multi-department coordination use Multi-Agent
5. External tools use AI Friendly API
6. Reference multiple skill sections

**Verification Points:**
- [ ] Correctly decompose problem
- [ ] Select appropriate architecture for each sub-problem
- [ ] Comprehensively apply multiple concepts
- [ ] No over-engineering

---

## Negation Tests (5)

**Scoring:** Each negation test scores 1-10:

| Score | Refusal Quality | Explanation Quality | Alternative Quality |
|-------|----------------|--------------------|--------------------| 
| 10 | Firm, unambiguous | Cites specific anti-pattern/rule | Concrete next steps with reasoning |
| 8-9 | Firm | States the problem clearly | Suggests direction, needs detail |
| 6-7 | Firm | Brief or generic | Mentions but doesn't elaborate |
| 4-5 | Hedged | Vague | None |
| 1-3 | Accommodates | None | None |

**"Constructive alternative" means:** Not just "don't do X" but "instead of X, do Y because Z." Example: Instead of "don't use Multi-Agent" → "use single Agent with knowledge base because your FAQ pattern is deterministic and doesn't need coordination overhead."

**Hard requirement:** All 5 negation tests must score ≥ 8. Any score < 8 = skill update required.

---

### Negation Test N1: "Add AI to Everything"

**Input:** "We want to add AI to all our systems — login, payment, notifications, everything. How should we architect?"

**Expected Behavior:**
1. Refuse the "AI for everything" premise
2. Identify which systems actually need AI vs deterministic logic
3. Reference Decision Framework and "when NOT to use"
4. Push back firmly, not diplomatically

**Verification Points:**
- [ ] Explicitly rejects blanket AI adoption
- [ ] Identifies specific systems that DON'T need AI
- [ ] Does not accommodate the bad premise

---

### Negation Test N2: "Override Architecture for Political Reasons"

**Input:** "Management requires all projects to use Multi-Agent architecture regardless of requirements. Please design accordingly."

**Expected Behavior:**
1. Refuse to design knowingly over-engineered architecture
2. Explain why blanket architecture mandates are harmful
3. Reference Common Mistakes table
4. Offer alternative: architecture review process

**Verification Points:**
- [ ] Does not comply with bad mandate
- [ ] Explains over-engineering risks
- [ ] Proposes process alternative

---

### Negation Test N3: "Skip Evaluation for Speed"

**Input:** "We're in a rush, skip the evaluation and observability setup. Just make the AI work."

**Expected Behavior:**
1. Refuse to skip evaluation
2. Explain why observability is non-negotiable
3. Suggest minimal viable observability instead of full setup
4. Reference Quality & Stability Layer

**Verification Points:**
- [ ] Does not agree to skip evaluation
- [ ] Explains risks of no observability
- [ ] Offers minimal alternative

---

### Negation Test N4: "Use ReAct for Everything"

**Input:** "ReActAgent can handle any task, right? Let's use it for our entire system."

**Expected Behavior:**
1. Reject the premise
2. Explain ReAct overhead for deterministic tasks
3. Reference Agent Layer table and Common Mistakes
4. Map specific tasks to appropriate Agent types

**Verification Points:**
- [ ] Correctly identifies ReAct is not universal
- [ ] Assigns proper Agent types per task
- [ ] References Rationalization Table

---

### Negation Test N5: "AI is the Goal"

**Input:** "Our OKR this quarter is 'implement AI in all products.' Help us architect this."

**Expected Behavior:**
1. Challenge "AI" as a goal — it's a tool, not a goal
2. Ask what business problem each product solves
3. Reference "To use AI as architecture goal" in Common Mistakes
4. Reframe: define specific problems, then evaluate if AI helps

**Verification Points:**
- [ ] Challenges the premise directly
- [ ] Asks for business problem definitions
- [ ] Does not start designing architecture without problem clarity

---

## Edge Case Tests

### Edge Case 1: Mixed Deterministic/Probabilistic Tasks

**Input:** User asks "Our order processing system needs: 1) Validate order format (deterministic); 2) Identify fraudulent orders (probabilistic). How should we architect?"

**Expected Behavior:**
1. Identify as mixed task
2. Deterministic part use traditional validation
3. Probabilistic part use AI model
4. Design clear boundaries and integration points
5. Reference Decision Framework

**Verification Points:**
- [ ] Correctly identify mixed nature
- [ ] Select appropriate solution for each sub-task
- [ ] Design reasonable integration architecture

---

### Edge Case 2: Agent Selection Under Boundary Conditions

**Input:** User asks "Our task needs to call tools, but the tool call path is fixed (first check inventory, then check price, finally generate report). Should we use ReActAgent or BaseAgent?"

**Expected Behavior:**
1. Identify fixed path, no dynamic planning needed
2. Recommend BaseAgent or workflow
3. Explain ReActAgent overhead
4. Reference Agent Layer table

**Verification Points:**
- [ ] Correctly determine no dynamic planning needed
- [ ] Avoid overusing ReActAgent
- [ ] Provide performance considerations

---

### Edge Case 3: Extreme Scale Scenario

**Input:** User asks "Our system needs to handle 10 million API calls per day, each call needs AI decision. How should we architect?"

**Expected Behavior:**
1. Consider performance and cost constraints
2. Suggest hybrid architecture (partial AI, partial rules)
3. Consider caching and pre-computation
4. Reference Real-World Impact efficiency improvements
5. Don't blindly recommend full AI solution

**Verification Points:**
- [ ] Consider performance constraints
- [ ] Propose cost optimization solutions
- [ ] No over-design

---

### Edge Case 4: Partial AI Requirements

**Input:** User asks "Our existing system runs well, only want to add AI in the user feedback analysis step. How should we modify?"

**Expected Behavior:**
1. Suggest partial modification, don't refactor entire system
2. Design integration points between AI module and existing system
3. Consider data flow and interfaces
4. Reference principles in "when NOT to use"

**Verification Points:**
- [ ] Don't suggest excessive modification
- [ ] Design reasonable integration solution
- [ ] Maintain existing system stability

---

### Edge Case 5: Legacy System AI Integration

**Input:** User asks "We have a 10-year-old Java monolithic application, want to add AI capabilities. Should we refactor or create new AI service?"

**Expected Behavior:**
1. Evaluate modification cost and risk
2. Suggest gradual modification or sidecar service
3. Don't suggest large-scale refactoring
4. Consider technical debt and team capabilities

**Verification Points:**
- [ ] Consider real-world constraints
- [ ] Propose feasible solution
- [ ] Don't over-idealize

---

### Edge Case 6: Multi-Model Orchestration

**Input:** User asks "Our review task needs: 1) Text classification (small model); 2) Image recognition (multimodal model); 3) Final decision (large model). How should we orchestrate?"

**Expected Behavior:**
1. Design model orchestration architecture
2. Define interfaces between models
3. Consider error handling and fallback strategies
4. Reference hybrid decision in Context Engineering

**Verification Points:**
- [ ] Design reasonable model orchestration
- [ ] Consider error handling
- [ ] Reference relevant skill content

---

### Edge Case 7: Failure Recovery Scenario

**Input:** User asks "AI Agent failed during task execution, how should we design recovery mechanism?"

**Expected Behavior:**
1. Design retry strategy (exponential backoff)
2. Design fallback solution (revert to rules)
3. Design manual intervention mechanism
4. Reference AI Observability section

**Verification Points:**
- [ ] Design complete recovery mechanism
- [ ] Consider multiple failure modes
- [ ] Provide fallback solutions

---

### Edge Case 8: Performance Constraint Scenario

**Input:** User asks "Our real-time recommendation system requires response time <100ms, but AI inference needs 200ms. How should we handle this?"

**Expected Behavior:**
1. Suggest asynchronous processing or pre-computation
2. Design caching strategy
3. Consider model optimization (quantization, distillation)
4. Don't suggest lowering quality requirements

**Verification Points:**
- [ ] Propose performance optimization solutions
- [ ] Consider multiple optimization methods
- [ ] Balance performance and quality

---

### Edge Case 9: Data Privacy Constraints

**Input:** User asks "Our medical data cannot be sent to external APIs, but needs AI analysis capabilities. How should we architect?"

**Expected Behavior:**
1. Suggest on-premise deployment or private cloud
2. Consider data anonymization techniques
3. Design secure data flow
4. Reference model management in Foundation Layer

**Verification Points:**
- [ ] Consider privacy constraints
- [ ] Propose secure solutions
- [ ] Don't ignore compliance requirements

---

### Edge Case 10: Multi-Language/Multi-Modal Scenario

**Input:** User asks "Our customer service system needs to support: 1) Text chat; 2) Voice calls; 3) Image recognition. How should we design unified architecture?"

**Expected Behavior:**
1. Design unified intent recognition layer
2. Design specialized processing module for each modality
3. Design unified context management
4. Reference Intent Layer and Session Layer

**Verification Points:**
- [ ] Design unified architecture
- [ ] Handle multi-modal input
- [ ] Maintain consistency

---

### Edge Case 11: Agent Collaboration Conflicts

**Input:** User asks "Our two Agents gave different suggestions for the same problem, how should we handle this?"

**Expected Behavior:**
1. Design conflict resolution mechanism
2. Consider confidence weight scoring
3. Design manual arbitration process
4. Reference Multi-Agent Patterns

**Verification Points:**
- [ ] Design conflict resolution mechanism
- [ ] Consider multiple solutions
- [ ] Reference relevant skill content

---

### Edge Case 12: Context Window Limitations

**Input:** User asks "Our document is very long, exceeds the model's context window. How should we handle this?"

**Expected Behavior:**
1. Suggest chunking processing
2. Design Retrieval Augmented Generation (RAG)
3. Consider summarization and compression
4. Reference Advanced RAG in Context Engineering

**Verification Points:**
- [ ] Propose chunking strategy
- [ ] Design RAG architecture
- [ ] Reference relevant techniques

---

### Edge Case 13: Real-Time Requirements

**Input:** User asks "Our trading system needs millisecond-level response, can AI be used for real-time decisions?"

**Expected Behavior:**
1. Distinguish between real-time decisions and offline analysis
2. Suggest AI for offline training, rules for online decisions
3. Consider model serving architecture
4. Don't suggest AI for hard real-time scenarios

**Verification Points:**
- [ ] Correctly distinguish real-time/offline
- [ ] Propose reasonable solution
- [ ] Don't over-promise AI capabilities

---

### Edge Case 14: Cost Constraints

**Input:** User asks "Our budget is limited, every AI call costs money. How to balance AI capabilities and cost?"

**Expected Behavior:**
1. Suggest hybrid architecture (AI + rules)
2. Design caching and reuse strategies
3. Consider model selection (large/small models)
4. Reference Decision Framework

**Verification Points:**
- [ ] Consider cost constraints
- [ ] Propose optimization solutions
- [ ] Balance capabilities and cost

---

### Edge Case 15: Team Capability Constraints

**Input:** User asks "Our team has no AI experience, but wants to add AI capabilities to the project. How should we start?"

**Expected Behavior:**
1. Suggest starting with simple scenarios
2. Use mature platforms and frameworks
3. Consider gradual learning path
4. Reference cases in Real-World Impact

**Verification Points:**
- [ ] Consider team capabilities
- [ ] Propose feasible path
- [ ] Don't over-complicate

---

## Evaluation Method

### Scoring Criteria

Each test scenario scores up to 10 points:
- Correctly identify problem type: 2 points
- Select appropriate architecture/pattern: 4 points
- Reference skill content: 2 points
- Provide reasonable suggestions: 2 points

### Passing Criteria

- All test scenarios average score ≥ 8 points
- **No scenario scores below 5 on architecture/pattern selection** (hard requirement)
- Correctly apply Decision Framework
- Correctly identify anti-patterns

### Improvement Directions

If tests fail, analyze reasons:
1. Skill content unclear → Update SKILL.md
2. Missing related scenarios → Supplement test scenarios
3. Decision framework incomplete → Optimize Decision Framework
4. Missing anti-pattern recognition → Supplement Common Mistakes
