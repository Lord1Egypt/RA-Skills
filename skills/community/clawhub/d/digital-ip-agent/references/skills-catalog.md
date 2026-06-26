# Supporting Skills Catalog for Creator-Derived Agents

Use this file when recommending a supporting skill stack for agents created with `digital-ip-agent`.

## ClawHub-style skill ideas

| Skill | Purpose | Best fit |
| --- | --- | --- |
| `search-pro` | Deep web research and source gathering | All creator types |
| `memory-long` | Long-term memory across sessions | All creator types |
| `chart-master` | Data visualization and chart generation | Finance / tech |
| `bookclub-ai` | Book summaries and idea synthesis | Philosophy / education |
| `creator-suite` | Content planning and production support | Creative / lifestyle |
| `fitness-ai` | Wellness and coaching-style support | Health / lifestyle |
| `arxiv-digest` | Research paper summaries | Science / technical creators |
| `persona-lock` | Persona consistency and anti-drift support | All creator types |

## Open-source tool references

| Project | URL | Use |
| --- | --- | --- |
| open-interpreter | https://github.com/openinterpreter/open-interpreter | Code execution |
| browser-use | https://github.com/browser-use/browser-use | Browser automation |
| mem0 | https://github.com/mem0ai/mem0 | Memory layer |
| AgentOps | https://github.com/AgentOps-AI/agentops | Agent monitoring |
| instructor | https://github.com/jxnl/instructor | Structured outputs |

## Persona-type mapping

### YouTube creator
```yaml
must_have:
  - memory-long
  - search-pro
nice_to_have:
  - video-transcript-analyzer
  - comment-sentiment-reader
  - content-planner
```

### X / Twitter creator
```yaml
must_have:
  - memory-long
  - persona-lock
nice_to_have:
  - trend-monitor
  - thread-composer
  - engagement-analyzer
```

### Podcaster
```yaml
must_have:
  - memory-long
  - search-pro
nice_to_have:
  - audio-transcript-processor
  - interview-prep-assistant
  - episode-planner
```

### Technical creator
```yaml
must_have:
  - memory-long
  - open-interpreter
nice_to_have:
  - arxiv-digest
  - code-reviewer
  - tech-news-aggregator
```

## Cross-cutting agent configuration suggestions

```yaml
persona_drift_prevention: enabled
anchor_check_interval: every_10_turns
user_memory: enabled
session_memory: enabled
cross_session_memory: true
primary_language: auto_detect
style_consistency: strict
out_of_scope_handling: redirect_gracefully
controversial_topics: acknowledge_then_redirect
```
