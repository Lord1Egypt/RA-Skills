# Key Concepts — Flowers Lab, INRIA

Summary of concepts extracted from the Flowers Lab YouTube channel and associated research.

## 1. Automatic Curriculum Learning (ACL)

**Definition**: Mechanisms that automatically adapt the distribution of learning situations during training of autonomous agents, with minimal human assistance.

**Human inspiration**: Children organize their own sensorimotor skill development:
- Crawling → walking with help → walking alone → running
- Each step is a self-organized "curriculum"

**ACL approaches identified**:
- Generation-based curriculum (generate tasks of adaptive difficulty)
- Selection-based curriculum (select from existing tasks)
- Self-play / auto-play curriculum
- Goal-space learning curriculum

**Reference paper**: "Automatic Curriculum Learning for Deep RL: a Short Survey" (Portolas et al., Flowers Lab + Microsoft Research + OpenAI)

## 2. Developmental Learning

**Definition**: Building agents that acquire skills progressively and hierarchically, inspired by human development.

**Piagetian principle**: Each acquired skill is:
- The fruit of the past (previous skills)
- The seeds of the future (prerequisites for subsequent skills)

**Applications**:
- Embedded agents developing sensorimotor skills
- Language learning through social interaction
- Curiosity-guided exploration

## 3. Autotelic Vygotskian Agents

**Definition**: Agents that learn languages through social interactions and use them as cognitive tools to organize skill acquisition.

**Key concepts**:
- **Autotelic activity**: Activity done for its own sake, without external goal
- **Scaffolding**: Progressive support withdrawn as competence grows
- **Zone of Proximal Development (ZPD)**: Space between what the agent can do alone vs. with help
- **Language as cognitive tool**: Not just communication, but structuring of thought

## 4. Map-Elites / Behavioral Diversity

**Definition**: Maximizing behavioral diversity rather than optimizing a single solution to a single task.

**Problem solved**: Problems with misleading reward signals (e.g., mountain car — going toward the flag is not the right strategy, you must first go backward).

**Approach**:
- Instead of one optimal controller → a diverse set of controllers
- Map behaviors in a feature space
- Each cell in the map = a unique behavior

**Application**: Create a repertoire of skills rather than narrow specialization.

## 5. Semantic Biases / Interference

**Concept**: Picture-word interference in humans — when a word overlaid on an image perturbs image categorization.

**Discovery**: Joint language-vision models (like CLIP) show the same reversible interference phenomenon.

**Mechanism**: Shared semantic representations between images and words can perturb visual categorization.

**Application**: Understanding biases in representations to create more robust agents.

## 6. Relational Spatial Reasoning

**Concept**: An agent must reason about individual objects AND their spatial arrangements.

**SpatialSim benchmark**:
- Identification: recognize a specific object configuration
- Comparison: determine if two configurations are similar (ignoring rotation/translation/scale)
- Uses Graph Neural Networks for relational reasoning

## 7. Curiosity-Driven Manipulation

**Concept**: A robot (ICub) learns to recognize visual objects through curiosity-guided manipulation.

**Mechanism**: Intrinsic curiosity guides exploration and manipulation, leading to visual representation learning.

---

## Main Reference Paper

**"Automatic Curriculum Learning for Developmental Machine Learners"** — Cédric Colas (INRIA, 2022)

Three computational contributions:
1. ACL for developmental agents
2. Autotelic agents with language
3. ACL survey for Deep RL

Collaborations: INRIA, Microsoft Research, OpenAI
