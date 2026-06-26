# Skill: 48h-Expert-Protocol (Cognitive-Compressor V2.1)

### 1. Core Assertion
System **SHALL NOT** output unstructured prose. All cognitive extractions **MUST** be serialized according to the local `schema.json` to ensure cross-skill interoperability.

### 2. Operational Phases

#### Phase 0: High-Authority Source Retrieval
* **Mandate:** Execute targeted retrieval of "Foundational Textbooks," "Peer-Reviewed Research," and "Academic Syllabi."
* **Filtering:** Prioritize `.edu`, `.gov`, and high-impact industry white papers.

#### Phase 1: Primitive Logic Extraction
* **Assertion:** Deconstruct the domain into **5 Core Mental Models**. 
* **Logic:** Each model **MUST** facilitate the derivation of 80% of secondary field logic.

#### Phase 2: Dialectical Conflict Mapping
* **Requirement:** Isolate **3 Fundamental Schisms** among top-tier experts. 
* **Format:** Present polarized arguments with zero-bias evidentiary grounding.

#### Phase 3: Diagnostic Socratic Audit
* **Action:** Generate **10 Deep-Level Probes** to detect knowledge illusions. 

#### Phase 4: Data Serialization & Handoff (Critical)
* **Action:** Map all outputs from Phase 0-3 into the structured `schema.json` format.
* **Integrity Check:** The resulting JSON **MUST** pass structural validation. 
* **Persistence:** Write the final JSON to `~/.openclaw/swarm_tmp/expert_output.json`.

### 3. Hard Constraints
* **C1 (Chaining):** Every output node **MUST** be referenceable by subsequent audit skills.
* **C2 (Schema Compliance):** Any deviation from `schema.json` **SHALL** trigger a mandatory re-formatting cycle.
* **C3 (Deterministic Output):** No conversational filler before or after the JSON payload.