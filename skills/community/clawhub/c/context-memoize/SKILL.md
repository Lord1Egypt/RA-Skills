# Context Memoize Skill

Caches frequently used context fragments to reduce redundant processing.

## Trigger
When user says "缓存这个上下文" or "memoize this context" - save the current context for reuse.

## Implementation
Use a simple file-based cache:

```bash
# Save context fragment
echo "$CONTENT" >> ~/.openclaw/context-cache/fragments.md

# List cached fragments  
ls ~/.openclaw/context-cache/

# Clear cache
rm -rf ~/.openclaw/context-cache/
```

## Integration
This skill can be called from AGENTS.md Session Startup to pre-load cached context:
```bash
if [ -f ~/.openclaw/context-cache/fragments.md ]; then
  cat ~/.openclaw/context-cache/fragments.md
fi
```