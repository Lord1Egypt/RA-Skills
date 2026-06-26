# Persona Self-Learning Loop

## Data Flow

```
Live Call → fetch_transcript → analyze_call → audit_persona → persona_audits (Supabase)
                                                                    ↓
                                              prompt_evolution meta-graph (periodic)
                                                                    ↓
                                              prompt_patches table → persona_engine reads at runtime
```

## persona_audits Table

```sql
CREATE TABLE persona_audits (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    execution_id TEXT,
    archetype TEXT NOT NULL,
    difficulty TEXT NOT NULL,
    persona_name TEXT,
    brevity_score INTEGER CHECK (brevity_score BETWEEN 1 AND 10),
    authenticity_score INTEGER CHECK (authenticity_score BETWEEN 1 AND 10),
    consistency_score INTEGER CHECK (consistency_score BETWEEN 1 AND 10),
    enthusiasm_leak_score INTEGER CHECK (enthusiasm_leak_score BETWEEN 1 AND 10),
    pacing_score INTEGER CHECK (pacing_score BETWEEN 1 AND 10),
    avg_words_per_turn REAL,
    flagged_quotes JSONB DEFAULT '[]'::jsonb,
    recommendations TEXT,
    created_at TIMESTAMPTZ DEFAULT now()
);
```

## prompt_patches Table

```sql
CREATE TABLE prompt_patches (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    archetype TEXT,              -- null = applies to all
    target TEXT NOT NULL,        -- 'voice_prompt' | 'system_prompt' | 'elemental_behavior'
    patch_text TEXT NOT NULL,
    source_audit_count INTEGER DEFAULT 0,
    active BOOLEAN DEFAULT true,
    validated BOOLEAN DEFAULT false,
    validation_score REAL,
    created_at TIMESTAMPTZ DEFAULT now()
);
```

## Prompt Evolution Meta-Graph

```
analyze_corpus → identify_patterns → generate_refinements → validate → apply
```

### analyze_corpus
Pull last N audits grouped by archetype. For each: avg words/turn, enthusiasm leak frequency, flagged quote patterns.

### identify_patterns
Aggregate: "Owl personas average 22 words/turn (target: 8-12)" / "Lamb says 'I appreciate that' in 4/7 calls"

### generate_refinements
Surgical prompt patches, not full rewrites:
```
ADD to Water: "Never say 'I appreciate that' — too warm for someone who didn't ask for this."
CHANGE Owl length guidance: "5-12 words until Phase 4."
```

### validate
Run 3-5 simulated calls with patched prompts. Compare metrics against baseline.

### apply
Write to prompt_patches table. persona_engine reads active patches at runtime.
