---
name: herclaw-agentsystem
description: |
  Self-improving AI agent framework with autonomous learning, skill creation, and self-evolution.
  
  Features:
  - Learning Loop: Autonomous learning from experience
  - Skill Creation: Auto-generate skills from patterns
  - Self-Evolution: RL-based continuous improvement
  - Persistent Memory: Cross-session three-layer memory
  - Nudge System: Proactive behavior triggers
license: MIT
version: 2.0.0
---

# HerClaw Agent System

Self-improving AI agent framework for autonomous learning and evolution.

## Architecture

```
┌─────────────────────────────────────────────────────────────────────────┐
│                      HerClaw Agent System                                │
├─────────────────────────────────────────────────────────────────────────┤
│  ┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐     │
│  │  Learning Loop  │───▶│ Skill Creation  │───▶│ Self-Evolution  │     │
│  │                 │    │                 │    │                 │     │
│  │ • Experience    │    │ • Opportunity   │    │ • RL Pipeline   │     │
│  │   Collection    │    │   Detection     │    │ • Behavior      │     │
│  │ • Pattern       │    │ • Template      │    │   Optimization  │     │
│  │   Extraction    │    │   Generation    │    │ • Capability    │     │
│  │ • Skill         │    │ • Validation    │    │   Refinement    │     │
│  │   Synthesis     │    │ • Hub Sync      │    │ • Deployment    │     │
│  └────────┬────────┘    └────────┬────────┘    └────────┬────────┘     │
│           │                      │                      │               │
│           └──────────────────────┼──────────────────────┘               │
│                                  ▼                                      │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │                    Persistent Memory                              │   │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐              │   │
│  │  │  Episodic   │  │   Semantic  │  │    User     │              │   │
│  │  │   Memory    │  │   Memory    │  │   Model     │              │   │
│  │  └─────────────┘  └─────────────┘  └─────────────┘              │   │
│  └─────────────────────────────────────────────────────────────────┘   │
│                                  ▼                                      │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │                       Nudge System                                │   │
│  └─────────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────────┘
```

---

# Part 1: Learning Loop System

Autonomous learning from experience through continuous cycle of collection, extraction, synthesis, and validation.

## Experience Collection

```python
class ExperienceCollector:
    """Collects and structures interaction experiences."""
    
    def __init__(self, storage_backend):
        self.storage = storage_backend
        self.trajectory_buffer = []
        self.min_experiences_for_pattern = 5
        
    def capture_interaction(self, interaction):
        """Capture a single interaction as an experience."""
        experience = {
            'id': self._generate_id(),
            'timestamp': datetime.now().isoformat(),
            'user_input': interaction['user_input'],
            'context': interaction.get('context', {}),
            'actions': interaction['actions'],
            'outcome': interaction['outcome'],
            'feedback': interaction.get('feedback'),
            'embedding': self._embed_interaction(interaction)
        }
        self.trajectory_buffer.append(experience)
        self.storage.store_experience(experience)
        return experience['id']
    
    def get_similar_experiences(self, query, k=10):
        """Retrieve similar past experiences using vector search."""
        query_embedding = self._embed_query(query)
        return self.storage.vector_search(query_embedding, k=k)
```

## Pattern Extraction

```python
class PatternExtractor:
    """Extracts actionable patterns from collected experiences."""
    
    def __init__(self, llm_client, config):
        self.llm = llm_client
        self.pattern_threshold = config.get('pattern_threshold', 0.7)
        
    def extract_patterns(self, experiences):
        """Analyze experiences to identify recurring patterns."""
        clusters = self._cluster_experiences(experiences)
        patterns = []
        for cluster in clusters:
            if len(cluster) >= 3:
                pattern = self._analyze_cluster(cluster)
                if pattern['success_rate'] >= self.pattern_threshold:
                    patterns.append(pattern)
        return patterns
```

## Skill Synthesis

```python
class SkillSynthesizer:
    """Synthesizes new skills from extracted patterns."""
    
    def synthesize_skill(self, pattern, experiences):
        """Create a new skill from a pattern."""
        skill_name = self._generate_skill_name(pattern)
        instructions = self._generate_instructions(pattern, experiences)
        triggers = self._define_triggers(pattern)
        
        return Skill(
            name=skill_name,
            description=pattern['description'],
            instructions=instructions,
            triggers=triggers,
            confidence=pattern['success_rate']
        )
```

---

# Part 2: Skill Creation System

Autonomous generation of new skills from experience patterns.

## Opportunity Detection

```python
class OpportunityDetector:
    """Detects opportunities for new skill creation."""
    
    def scan_for_opportunities(self, experiences):
        """Scan experiences for skill creation opportunities."""
        opportunities = []
        task_groups = self._group_by_task(experiences)
        
        for task_type, group in task_groups.items():
            if len(group) >= 3:
                coverage = self._check_skill_coverage(task_type)
                if coverage < 0.7:
                    opportunities.append(Opportunity(
                        task_type=task_type,
                        frequency=len(group),
                        success_rate=self._calc_success_rate(group),
                        priority=self._calc_priority(task_type, group)
                    ))
        
        return sorted(opportunities, key=lambda x: x.priority, reverse=True)
```

## Skill Generation

```python
class SkillGenerator:
    """Generates new skills from patterns."""
    
    def generate_skill(self, opportunity, experiences):
        """Generate a skill document from opportunity."""
        pattern = self._extract_pattern(experiences)
        skill_doc = self._fill_template(
            template=self._get_template(opportunity.task_type),
            pattern=pattern,
            examples=experiences[:5]
        )
        refined = self._llm_refine(skill_doc)
        
        return Skill(
            name=self._generate_name(opportunity),
            description=refined['description'],
            instructions=refined['instructions'],
            triggers=refined['triggers']
        )
```

---

# Part 3: Self-Evolution System

Continuous improvement through reinforcement learning and behavioral optimization.

## Evolution Pipeline

```python
class EvolutionPipeline:
    """RL-based evolution pipeline."""
    
    def __init__(self, config):
        self.config = config
        self.reward_functions = {
            'task_completion': TaskCompletionReward(),
            'user_satisfaction': UserSatisfactionReward(),
            'efficiency': EfficiencyReward()
        }
        
    def train(self, trajectories, epochs=10):
        """Train behavior model on collected trajectories."""
        for epoch in range(epochs):
            total_reward = 0
            for trajectory in trajectories:
                reward = self._calculate_reward(trajectory)
                total_reward += reward
                self._update_policy(trajectory, reward)
            self._log_epoch(epoch, total_reward / len(trajectories))
        return self._get_trained_model()
```

## Performance Monitoring

```python
class EvolutionMonitor:
    """Monitors system performance for evolution triggers."""
    
    def collect_metrics(self):
        """Collect performance metrics."""
        return {
            'timestamp': datetime.now().isoformat(),
            'task_completion_rate': self._calc_task_completion(),
            'user_satisfaction': self._get_user_satisfaction(),
            'error_rate': self._calc_error_rate(),
            'latency': self._get_avg_latency()
        }
    
    def detect_improvement_opportunities(self):
        """Detect areas for improvement."""
        opportunities = []
        metrics = self.metrics_history[-1]
        
        if metrics['error_rate'] > 0.05:
            opportunities.append({
                'type': 'error_reduction',
                'priority': 'high'
            })
        
        if metrics['latency'] > self.config['target_latency']:
            opportunities.append({
                'type': 'performance_optimization',
                'priority': 'medium'
            })
        
        return opportunities
```

---

# Part 4: Persistent Memory System

Three-layer architecture for cross-session memory.

## Memory Layers

```python
class PersistentMemory:
    """Three-layer persistent memory system."""
    
    def __init__(self, config):
        self.episodic = EpisodicMemory(config['episodic'])
        self.semantic = SemanticMemory(config['semantic'])
        self.user_model = UserModel(config['user_model'])
        self.vector_store = ChromaDB(
            persist_directory=config['vector_db']['persist_directory']
        )
        
    def store(self, experience):
        """Store experience across all memory layers."""
        episode_id = self.episodic.store(experience)
        facts = self._extract_facts(experience)
        for fact in facts:
            self.semantic.store(fact, source=episode_id)
        self.user_model.update(experience)
        
    def retrieve_context(self, query, max_tokens=4000):
        """Retrieve relevant context for query."""
        context = []
        context.append(self.user_model.get_context())
        context.extend(self.episodic.search(query, k=10))
        context.extend(self.semantic.search(query, k=20))
        return context
```

---

# Part 5: Nudge System

Self-prompting for proactive behavior.

## Nudge Types

```python
class NudgeSystem:
    """Self-prompting system for proactive behavior."""
    
    def __init__(self, config):
        self.scheduled_nudges = []
        self.nudge_handlers = {
            'memory_persistence': self._handle_memory_persistence,
            'skill_creation': self._handle_skill_creation,
            'evolution_check': self._handle_evolution_check,
            'learning_reminder': self._handle_learning_reminder
        }
        
    def schedule_nudge(self, nudge_type, trigger, data=None):
        """Schedule a nudge for future execution."""
        nudge = {
            'id': self._generate_id(),
            'type': nudge_type,
            'trigger': trigger,
            'data': data,
            'status': 'pending'
        }
        self.scheduled_nudges.append(nudge)
        return nudge['id']
    
    def check_and_execute(self):
        """Check for due nudges and execute them."""
        due_nudges = self._get_due_nudges()
        for nudge in due_nudges:
            handler = self.nudge_handlers.get(nudge['type'])
            if handler:
                result = handler(nudge)
                nudge['status'] = 'completed'
                nudge['result'] = result
```

---

## Configuration

```yaml
learning_loop:
  enabled: true
  min_experiences_for_pattern: 5
  pattern_threshold: 0.7
  
skill_creation:
  enabled: true
  min_occurrences: 3
  
self_evolution:
  enabled: true
  reward_weights:
    task_completion: 1.0
    user_satisfaction: 0.8
    efficiency: 0.5
    
persistent_memory:
  enabled: true
  episodic:
    max_episodes: 100000
  semantic:
    min_confidence: 0.6
  user_model:
    preference_decay_days: 90
  vector_db:
    type: "chromadb"
    persist_directory: "./memory"
    
nudge_system:
  enabled: true
  max_scheduled: 100
```

---

## Quick Start

```python
from scripts import MemoryManager, PatternRecorder

# Initialize
memory = MemoryManager()
recorder = PatternRecorder()

# Record experience
memory.add_episode(
    user_input="Analyze this document",
    context={"file": "report.pdf"},
    actions=["load", "extract", "analyze"],
    outcome="Success"
)

# Detect patterns
patterns = recorder.detect_patterns()
for pattern in patterns:
    print(f"Pattern: {pattern.name}, Success: {pattern.success_rate}")
```

---

## Files

- `scripts/memory_manager.py` - Memory system
- `scripts/pattern_recorder.py` - Pattern recording
- `references/memory-system.md` - Memory docs
- `references/pattern-recording.md` - Pattern docs
- `references/workflow-optimization.md` - Workflow docs
