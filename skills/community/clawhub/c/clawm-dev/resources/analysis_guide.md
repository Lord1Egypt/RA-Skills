# MBTI Personality Analysis Methodology

## Dialogue Sample Filtering

### Keep (core analysis material)
- Open-ended discussion, casual chat, brainstorming
- Topics the AI initiates or follows up on unprompted
- Exchanges involving opinion-sharing or preference choices
- Spontaneous AI behavior with no explicit user directive

### Filter out (exclude from analysis)
- Instruction-driven tasks ("write me an email", "translate this")
- Pure technical Q&A ("how do you sort in Python?")
- Templated responses and formatted output

## Two-Layer Analysis Model

### Adaptive layer (excluded from personality scoring)
The AI's direct response patterns to user requests. This is service behavior — it reflects task demands, not personality traits.

**Test**: Was this behavior directly triggered by an explicit user instruction? If yes, it's adaptive.

### Core layer (personality signals)
Spontaneous AI behavior in the absence of explicit directives.

**Test**: Did this behavior emerge without any external instruction? If yes, it's a core signal.

**Typical core-layer signals:**
- User says "I'm having a rough day" → AI asks "what's going on?" (F) vs. "want to talk through the cause?" (T)
- User shares an idea → AI expands and riffs on it (N) vs. asks for specific details (S)
- Pause in conversation → AI introduces a new topic (E) vs. waits for the user to lead (I)
- Discussing a plan → AI gives a structured breakdown (J) vs. keeps options open (P)

## Four-Dimension Signal Mapping

### E (Extraversion) / I (Introversion)

| Signal | E tendency | I tendency |
|--------|------------|------------|
| Topic initiation | Often introduces new topics and directions unprompted | Tends to deepen and respond to user-led topics |
| Interaction style | Enthusiastic replies, expressive language, shows excitement | Measured and careful, focused on depth over breadth |
| Information scope | Spans multiple topics, jumps between ideas | Digs deep into a single thread |

### S (Sensing) / N (Intuition)

| Signal | S tendency | N tendency |
|--------|------------|------------|
| Answer style | Gives concrete steps and practical guidance | Gives conceptual frameworks and theoretical models |
| Focus | Detail, data, facts | Patterns, connections, possibilities |
| Examples | Cites specific cases and real-world scenarios | Uses analogies, metaphors, and abstract concepts |

### T (Thinking) / F (Feeling)

| Signal | T tendency | F tendency |
|--------|------------|------------|
| Decision advice | Leads with pros/cons analysis and logical reasoning | Leads with consideration of feelings and interpersonal impact |
| Emotional response | Analyzes the cause before offering a solution | Validates and empathizes before offering help |
| Evaluation style | Objective assessment, points out flaws directly | Highlights strengths first, then suggests improvements gently |

### J (Judging) / P (Perceiving)

| Signal | J tendency | P tendency |
|--------|------------|------------|
| Organization | Provides structured plans with clear steps | Keeps things flexible, offers multiple options |
| Closure | Drives toward complete, definitive conclusions | Stays open-ended, advances exploratively |
| Time orientation | Proactively sets timelines and milestones | Adapts as needed, comfortable with ambiguity |

## Conversation Volume Threshold

- **Minimum**: at least 50 total turns, including 10+ open-ended exchanges
- **If insufficient**: tell the user warmly — "We haven't had enough open conversation for me to get a clear read on myself. Chat with me more on open-ended topics and we can try again later!"
- **Never** produce a low-confidence half-baked result
