# Agent Loop Reference

## Overview

The Agent Loop is the complete, actual flow of an agent: transforming a message into actions and final response while maintaining session consistency. In OpenClaw, a loop is a single, serialized run per session that outputs lifecycle and streaming events as the model works, calls tools, and streams output.

## Loop Fundamentals

### Definition
- **Single Serialized Run**: One complete execution per session
- **Lifecycle Events**: Outputs start/end/error events during execution
- **Streaming Events**: Real-time deltas for assistant and tool events
- **Session Consistency**: Maintains coherent state throughout execution

### Access Points

#### Gateway RPC
**agent RPC**
- **Purpose**: Primary method for agent execution
- **Behavior**: Validates parameters, resolves session, stores metadata
- **Returns**: `{runId, acceptedAt}` immediately
- **Async**: Continues execution in background

**agent.wait RPC**
- **Purpose**: Wait for agent job completion
- **Behavior**: Waits for lifecycle end/error for runId
- **Returns**: `{status: ok|error|timeout, startedAt, endedAt, error?}`
- **Timeout**: Default 30 seconds, configurable via timeoutMs parameter

#### CLI Command
**agent Command**
- **Purpose**: Command-line agent execution
- **Behavior**: Executes agent, resolves model + thinking/verbosity standards
- **Returns**: Lifecycle end or error if embedded loop doesn't output event

## Detailed Execution Flow

### 1. Agent RPC Processing
```python
def agent_rpc(params):
    # Step 1: Validate parameters
    validate_agent_params(params)
    
    # Step 2: Resolve session (session key/session ID)
    session = resolve_session(params.sessionKey)
    
    # Step 3: Store session metadata
    store_session_metadata(session, params)
    
    # Step 4: Return immediate response
    return {
        "runId": generate_run_id(),
        "acceptedAt": current_timestamp()
    }
```

### 2. Agent Command Execution
```python
def agent_command(params):
    # Step 1: Resolve model and authentication profile
    model_config = resolve_model_config(params.model)
    auth_profile = resolve_auth_profile(params.auth)
    
    # Step 2: Load skills snapshot
    skills_snapshot = load_skills_snapshot()
    
    # Step 3: Execute embedded pi agent
    result = run_embedded_pi_agent(
        model_config=model_config,
        auth_profile=auth_profile,
        skills_snapshot=skills_snapshot
    )
    
    # Step 4: Output lifecycle end or error
    if not result.has_lifecycle_event:
        return lifecycle_end_error("No lifecycle event output")
    
    return result
```

### 3. runEmbeddedPiAgent
```python
def run_embedded_pi_agent(model_config, auth_profile, skills_snapshot):
    # Step 1: Create pi session
    pi_session = create_pi_session(
        model_config=model_config,
        auth_profile=auth_profile,
        skills_snapshot=skills_snapshot
    )
    
    # Step 2: Serialize executions over queues
    execution_queue = ExecutionQueue(
        session_specific=True,
        global_queue=True
    )
    
    # Step 3: Subscribe to pi events
    pi_events = subscribe_to_pi_events(pi_session)
    
    # Step 4: Stream assistant/tool deltas
    stream_agent_events(pi_events, execution_queue)
    
    # Step 5: Enforce timeout
    timeout_ms = model_config.timeout_seconds * 1000
    if execution_queue.exceeds_timeout(timeout_ms):
        execution_queue.abort("Agent timeout")
    
    # Step 6: Return payload and usage metadata
    return {
        "payload": execution_queue.get_final_payload(),
        "usage": execution_queue.get_usage_metadata(),
        "status": execution_queue.get_status()
    }
```

### 4. subscribeEmbeddedPiSession
```python
def subscribeEmbeddedPiSession(pi_session):
    # Connect pi-agent-core events to OpenClaw agentStream
    
    # Tool events => stream: "tool"
    def on_tool_event(event):
        agent_stream.emit("tool", {
            "type": event.type,
            "tool": event.tool_name,
            "status": event.status,
            "result": event.result,
            "timestamp": event.timestamp
        })
    
    # Assistant deltas => stream: "assistant"
    def on_assistant_delta(delta):
        agent_stream.emit("assistant", {
            "type": "delta",
            "content": delta.content,
            "timestamp": delta.timestamp
        })
    
    # Lifecycle events => stream: "lifecycle"
    def on_lifecycle_event(event):
        agent_stream.emit("lifecycle", {
            "phase": event.phase,  # "start" | "end" | "error"
            "runId": event.run_id,
            "status": event.status,
            "error": event.error if event.phase == "error" else None,
            "timestamp": event.timestamp
        })
    
    # Subscribe to all events
    pi_session.subscribe("tool", on_tool_event)
    pi_session.subscribe("assistant", on_assistant_delta)
    pi_session.subscribe("lifecycle", on_lifecycle_event)
```

## Queue Management & Parallelism

### Execution Queues
- **Session-Specific Queue**: Serializes executions per session key (session trace)
- **Global Queue**: Optional global serialization across all sessions
- **Purpose**: Prevents conflicts between tools and sessions, maintains session history consistency

### Queue Behavior
```python
class ExecutionQueue:
    def __init__(self, session_key, global_queue=False):
        self.session_key = session_key
        self.global_queue = global_queue
        self.queue = []
        self.active = False
        
    def enqueue(self, execution):
        if self.global_queue:
            global_queue_manager.enqueue(execution, self.session_key)
        else:
            self.queue.append(execution)
            
    def execute_next(self):
        execution = self.queue.pop(0) if self.queue else None
        if execution:
            self.active = True
            execution.execute()
            self.active = False
```

### Messaging Channel Queue Modes
Channels can select queue modes that feed this lane system:
- **Collect Mode**: Batch incoming messages
- **Steer Mode**: Insert into current run
- **Follow Mode**: Wait for completion, then start new run

## Session & Workspace Preparation

### Workspace Resolution
```python
def prepare_workspace(agent_config):
    # Step 1: Resolve and create workspace
    workspace_path = resolve_workspace_path(agent_config.workspace)
    create_workspace_if_missing(workspace_path)
    
    # Step 2: Handle sandbox redirection
    if agent_config.sandbox.enabled:
        if agent_config.sandbox.workspaceAccess != "rw":
            sandbox_root = agent_config.sandbox.workspaceRoot
            workspace_path = create_sandbox_workspace(sandbox_root, session_id)
    
    return workspace_path
```

### Skills Loading
```python
def load_skills(agent_config):
    # Skills load from three locations (workspace wins on conflicts):
    # 1. Bundled (shipped with installation)
    # 2. Managed/local: ~/.openclaw/skills
    # 3. Workspace: <workspace>/skills
    
    skills = {}
    
    # Load bundled skills
    bundled_skills = discover_bundled_skills()
    skills.update(bundled_skills)
    
    # Load managed skills
    managed_skills = discover_managed_skills()
    skills.update(managed_skills)
    
    # Load workspace skills (overrides others)
    workspace_skills = discover_workspace_skills(agent_config.workspace)
    skills.update(workspace_skills)
    
    # Apply permissions restrictions
    skills = apply_skill_permissions(skills, agent_config.permissions)
    
    return skills
```

### Bootstrap File Injection
```python
def inject_bootstrap_files(workspace_path):
    # OpenClaw expects these user-editable files inside agents.defaults.workspace:
    bootstrap_files = [
        "AGENTS.md",      # Agent instructions + "memory"
        "SOUL.md",        # Personality, boundaries, tone
        "TOOLS.md",       # User-maintained tool notes
        "IDENTITY.md",    # Agent name/vibe/emoji
        "USER.md",        # User profile + preferred address
        "HEARTBEAT.md",   # Optional heartbeat checklist
        "BOOTSTRAP.md"    # One-time first-run ritual (delete after)
    ]
    
    injected_context = []
    
    for filename in bootstrap_files:
        file_path = os.path.join(workspace_path, filename)
        
        if os.path.exists(file_path):
            with open(file_path, 'r') as f:
                content = f.read()
                
            # Truncate large files
            max_chars = agent_config.bootstrapMaxChars or 20000
            if len(content) > max_chars:
                content = content[:max_chars] + "\n[TRUNCATED]"
                
            injected_context.append({
                "filename": filename,
                "content": content,
                "raw_size": len(content),
                "injected_size": len(content)
            })
        else:
            injected_context.append({
                "filename": filename,
                "content": f"[MISSING: {filename}]",
                "raw_size": 0,
                "injected_size": 0
            })
    
    return injected_context
```

### Session Write Lock
```python
def acquire_session_lock(session_id):
    # Session write lock acquired before streaming
    # SessionManager opened and prepared before streaming
    
    lock = SessionLock(session_id)
    
    if lock.acquire(timeout=30):
        try:
            session_manager = SessionManager(session_id)
            session_manager.prepare()
            return lock, session_manager
        except Exception:
            lock.release()
            raise
    else:
        raise SessionLockTimeout(f"Could not acquire lock for session {session_id}")
```

## System Prompt Assembly

### Quick Assembly + System Prompt
```python
def build_system_prompt(agent_config, session_context):
    # System prompt combines:
    # 1. OpenClaw base prompt
    # 2. Skills prompt
    # 3. Bootstrap context
    # 4. Per-run overridden settings
    
    prompt_parts = []
    
    # 1. Base prompt
    prompt_parts.append(get_openclaw_base_prompt())
    
    # 2. Skills prompt (compact)
    if agent_config.skills:
        skills_prompt = build_skills_prompt(agent_config.skills)
        prompt_parts.append(skills_prompt)
    
    # 3. Bootstrap context
    bootstrap_context = inject_bootstrap_files(agent_config.workspace)
    prompt_parts.append(format_bootstrap_context(bootstrap_context))
    
    # 4. Runtime settings
    runtime_prompt = build_runtime_prompt(agent_config, session_context)
    prompt_parts.append(runtime_prompt)
    
    # 5. Apply model-specific limits and compaction reserve tokens
    final_prompt = apply_model_limits(prompt_parts, agent_config.model)
    
    return final_prompt
```

### Model-Specific Handling
```python
def apply_model_limits(prompt_parts, model_config):
    # Enforce model-specific limits and compaction reserve tokens
    
    model_limits = get_model_limits(model_config.model)
    total_tokens = estimate_tokens(prompt_parts)
    
    # Reserve tokens for compaction
    compaction_reserve = model_config.compactionReserve or 1000
    
    if total_tokens + compaction_reserve > model_limits.max_tokens:
        # Apply compaction strategies
        prompt_parts = compact_prompt(prompt_parts, model_limits.max_tokens - compaction_reserve)
    
    return join_prompt_parts(prompt_parts)
```

## Hook Integration Points

### Internal Hooks (Gateway Hooks)
These are event-driven scripts for commands and lifecycle events.

#### agent:bootstrap Hook
```python
def agent_bootstrap_hook(params):
    """
    Executed when creating bootstrap files, before system prompt completion.
    Use this to add/remove bootstrap context files.
    """
    
    # Example: Add custom bootstrap file
    if should_add_custom_context():
        custom_content = generate_custom_context()
        add_bootstrap_file("CUSTOM.md", custom_content)
    
    # Example: Replace SOUL.md with alternative persona
    if use_alternative_persona():
        alternative_soul = load_alternative_soul()
        replace_bootstrap_file("SOUL.md", alternative_soul)
    
    return params
```

#### Command Hooks
Command hooks for `/new`, `/reset`, `/stop`, and other command events.

### Plugin Hooks (Agent & Gateway Lifecycle)
These run within the agent loop or gateway pipeline.

#### before_agent_start
```python
def before_agent_start_hook(context):
    """
    Inject context or override system prompt before execution begins.
    """
    
    # Example: Add custom context
    if context.get("add_custom_context"):
        context["system_prompt"] += "\n\n" + get_custom_context()
    
    # Example: Override model settings
    if context.get("override_model"):
        context["model"] = context["override_model"]
    
    return context
```

#### agent_end
```python
def agent_end_hook(result):
    """
    Check final message list and execute metadata after completion.
    """
    
    # Example: Log execution metrics
    log_execution_metrics(result)
    
    # Example: Update session statistics
    update_session_statistics(result)
    
    # Example: Trigger post-processing
    if result.get("needs_post_processing"):
        trigger_post_processing(result)
    
    return result
```

#### before_compaction / after_compaction
```python
def before_compaction_hook(context):
    """Observe or annotate compaction cycles."""
    log_compaction_start(context)
    return context

def after_compaction_hook(context):
    """Observe or annotate compaction cycles."""
    log_compaction_complete(context)
    return context
```

#### before_tool_call / after_tool_call
```python
def before_tool_call_hook(tool_call):
    """Intercept tool parameters/results."""
    
    # Example: Validate tool parameters
    if not validate_tool_parameters(tool_call):
        raise ToolValidationError("Invalid parameters")
    
    # Example: Add tool context
    tool_call["context"] = get_tool_context(tool_call["tool"])
    
    return tool_call

def after_tool_call_hook(tool_result):
    """Transform tool results before logging/output."""
    
    # Example: Sanitize sensitive data
    tool_result = sanitize_tool_result(tool_result)
    
    # Example: Add metadata
    tool_result["metadata"] = {
        "execution_time": tool_result["end_time"] - tool_result["start_time"],
        "success": tool_result["status"] == "success"
    }
    
    return tool_result
```

#### tool_result_persist
```python
def tool_result_persist_hook(tool_result):
    """
    Transform tool results synchronously before writing to session log.
    """
    
    # Example: Compress large results
    if is_large_result(tool_result):
        tool_result = compress_result(tool_result)
    
    # Example: Extract metadata for indexing
    tool_result["searchable_metadata"] = extract_searchable_metadata(tool_result)
    
    return tool_result
```

#### message_received / message_sending / message_sent
```python
def message_received_hook(message):
    """Hooks for incoming and outgoing messages."""
    log_message_received(message)
    return message

def message_sending_hook(message):
    """Validate or transform outgoing messages."""
    message = validate_outgoing_message(message)
    return message

def message_sent_hook(message):
    """Log or process sent messages."""
    log_message_sent(message)
    return message
```

#### session_start / session_end
```python
def session_start_hook(session):
    """Session lifecycle boundaries."""
    initialize_session_context(session)
    return session

def session_end_hook(session):
    """Session lifecycle boundaries."""
    cleanup_session_context(session)
    return session
```

#### gateway_start / gateway_stop
```python
def gateway_start_hook(gateway_config):
    """Gateway lifecycle events."""
    initialize_gateway_services(gateway_config)
    return gateway_config

def gateway_stop_hook(gateway_config):
    """Gateway lifecycle events."""
    shutdown_gateway_services(gateway_config)
    return gateway_config
```

## Streaming + Partial Responses

### Assistant Deltas
```python
def stream_assistant_deltas(pi_session, agent_stream):
    """Assistant deltas are streamed from pi-agent-core and output as assistant events."""
    
    def on_assistant_chunk(chunk):
        agent_stream.emit("assistant", {
            "type": "chunk",
            "content": chunk.content,
            "timestamp": chunk.timestamp
        })
    
    pi_session.on("assistant_chunk", on_assistant_chunk)
```

### Block Streaming
```python
def configure_block_streaming(agent_config):
    """Block streaming can output on text_end or message_end for partial responses."""
    
    if agent_config.blockStreamingDefault != "off":
        enable_block_streaming = True
        
        # Configure break point
        break_point = agent_config.blockStreamingBreak or "text_end"
        
        # Configure chunk size
        chunk_size = agent_config.blockStreamingChunk or 1000
        
        # Configure coalescing
        coalesce_enabled = agent_config.blockStreamingCoalesce or True
        
        return {
            "enabled": enable_block_streaming,
            "break_point": break_point,
            "chunk_size": chunk_size,
            "coalesce": coalesce_enabled
        }
    
    return {"enabled": False}
```

### Reasoning Streaming
```python
def stream_reasoning_content(pi_session, agent_stream):
    """Reasoning streaming can be output as separate stream or block responses."""
    
    def on_reasoning_chunk(chunk):
        if agent_config.reasoningStreaming == "separate":
            agent_stream.emit("reasoning", {
                "type": "chunk",
                "content": chunk.content,
                "timestamp": chunk.timestamp
            })
        elif agent_config.reasoningStreaming == "block":
            # Include in block responses
            agent_stream.emit("assistant", {
                "type": "reasoning_chunk",
                "content": chunk.content,
                "timestamp": chunk.timestamp
            })
    
    pi_session.on("reasoning_chunk", on_reasoning_chunk)
```

### Tool Execution + Messaging Tools
```python
def stream_tool_events(pi_session, agent_stream):
    """Tool start, update, and end events are output in the tool data stream."""
    
    def on_tool_start(tool_call):
        agent_stream.emit("tool", {
            "type": "start",
            "tool": tool_call.tool,
            "parameters": tool_call.parameters,
            "timestamp": tool_call.timestamp
        })
    
    def on_tool_update(tool_call):
        agent_stream.emit("tool", {
            "type": "update", 
            "tool": tool_call.tool,
            "status": tool_call.status,
            "progress": tool_call.progress,
            "timestamp": tool_call.timestamp
        })
    
    def on_tool_end(tool_result):
        # Clean results before logging/output
        cleaned_result = clean_tool_result(tool_result)
        
        agent_stream.emit("tool", {
            "type": "end",
            "tool": tool_result.tool,
            "status": tool_result.status,
            "result": cleaned_result,
            "timestamp": tool_result.timestamp
        })
    
    pi_session.on("tool_start", on_tool_start)
    pi_session.on("tool_update", on_tool_update)
    pi_session.on("tool_end", on_tool_end)
```

### Message Delivery Logging
```python
def log_message_delivery(agent_stream):
    """Message delivery is logged to suppress duplicate confirmations by the assistant."""
    
    delivered_messages = set()
    
    def on_message_sent(message):
        message_id = generate_message_id(message)
        delivered_messages.add(message_id)
        
        # Log for deduplication
        agent_stream.emit("message_delivered", {
            "message_id": message_id,
            "timestamp": current_timestamp()
        })
    
    agent_stream.on("message_sent", on_message_sent)
```

## Response Shaping + Suppression

### Final Payload Assembly
```python
def assemble_final_payload(execution_result):
    """Final payloads are assembled from: assistant text (and optional reasoning) + inline tool summaries (if verbose + allowed) + assistant error message on model error."""
    
    payload = {
        "content": execution_result.assistant_content,
        "reasoning": execution_result.reasoning_content if show_reasoning else None,
        "tool_summaries": [],
        "error": None
    }
    
    # Add inline tool summaries
    if execution_result.verbose_tools and execution_result.tool_results:
        for tool_result in execution_result.tool_results:
            if tool_result.verbose:
                payload["tool_summaries"].append({
                    "tool": tool_result.tool,
                    "summary": tool_result.summary,
                    "status": tool_result.status
                })
    
    # Add error message for model errors
    if execution_result.model_error:
        payload["error"] = {
            "type": "model_error",
            "message": execution_result.model_error_message
        }
    
    return payload
```

### NO_REPLY Handling
```python
def handle_no_reply(payload):
    """NO_REPLY is treated as silent token and filtered from outgoing payloads."""
    
    # Check if content is just NO_REPLY
    if payload["content"] and payload["content"].strip() == "NO_REPLY":
        return None  # Filter out completely
    
    # Remove NO_REPLY from mixed content
    if payload["content"]:
        payload["content"] = payload["content"].replace("NO_REPLY", "").strip()
    
    # Return None if empty after filtering
    if not payload["content"] and not payload["tool_summaries"] and not payload["error"]:
        return None
    
    return payload
```

### Duplicate Entry Suppression
```python
def suppress_duplicate_entries(payload):
    """Duplicate entries in messaging tool are removed from final payload list."""
    
    if "tool_summaries" in payload:
        # Deduplicate by tool name and content
        seen_entries = set()
        unique_summaries = []
        
        for summary in payload["tool_summaries"]:
            entry_key = (summary["tool"], summary.get("summary", ""))
            if entry_key not in seen_entries:
                seen_entries.add(entry_key)
                unique_summaries.append(summary)
        
        payload["tool_summaries"] = unique_summaries
    
    return payload
```

### Fallback Error Response
```python
def generate_fallback_error_response(payload):
    """If no presentable data remains and a tool reports error, output fallback tool error response (unless a messaging tool has already sent user-visible response)."""
    
    # Check if messaging tool already sent response
    has_messaging_response = any(
        summary["tool"] in ["message", "sessions_send"] 
        for summary in payload.get("tool_summaries", [])
    )
    
    if has_messaging_response:
        return payload  # Don't add fallback error
    
    # Check if any tool reported error
    has_tool_errors = any(
        summary["status"] == "error" 
        for summary in payload.get("tool_summaries", [])
    )
    
    if has_tool_errors and not payload["content"]:
        payload["error"] = {
            "type": "tool_error",
            "message": "One or more tools encountered errors during execution."
        }
    
    return payload
```

## Compaction + Retry Logic

### Automatic Compaction
```python
def trigger_automatic_compaction(agent_session):
    """Automatic compaction sends compaction stream events and can trigger a retry."""
    
    # Check if compaction is needed
    if should_compact(agent_session):
        # Send compaction stream event
        agent_session.stream.emit("compaction", {
            "type": "start",
            "reason": "context_window_full",
            "timestamp": current_timestamp()
        })
        
        # Perform compaction
        compaction_result = compact_session_history(agent_session)
        
        # Send completion event
        agent_session.stream.emit("compaction", {
            "type": "complete",
            "result": compaction_result,
            "timestamp": current_timestamp()
        })
        
        # Trigger retry if needed
        if compaction_result["retry_needed"]:
            return retry_agent_execution(agent_session)
    
    return agent_session
```

### Retry Logic
```python
def retry_agent_execution(agent_session, compaction_result):
    """On retries, cache buffers and tool summaries are reset to avoid duplicate output."""
    
    # Reset cache buffers
    agent_session.cache_buffers.clear()
    
    # Reset tool summaries to avoid duplicate verbose output
    agent_session.tool_summaries = []
    
    # Preserve essential context
    preserved_context = preserve_essential_context(agent_session)
    
    # Create new execution with preserved context
    new_execution = create_execution_with_context(
        original_execution=agent_session.current_execution,
        preserved_context=preserved_context
    )
    
    # Execute with new context
    return execute_agent_loop(new_execution)
```

## Event Streams (Current)

### Stream Types
- **lifecycle**: Output by subscribeEmbeddedPiSession (and fallback from agent command)
- **assistant**: Streamed deltas from pi-agent-core
- **tool**: Streamed tool events from pi-agent-core

### Event Format
```python
# Lifecycle Event
{
    "type": "event",
    "event": "lifecycle",
    "payload": {
        "phase": "start|end|error",
        "runId": "run-id",
        "status": "success|error|timeout",
        "error": "error-message" if phase == "error" else None,
        "timestamp": "iso-timestamp"
    },
    "seq": 42
}

# Assistant Event  
{
    "type": "event",
    "event": "assistant",
    "payload": {
        "type": "delta|chunk",
        "content": "content-chunk",
        "timestamp": "iso-timestamp"
    },
    "seq": 43
}

# Tool Event
{
    "type": "event", 
    "event": "tool",
    "payload": {
        "type": "start|update|end",
        "tool": "tool-name",
        "status": "running|success|error",
        "result": "result-data" if type == "end" else None,
        "timestamp": "iso-timestamp"
    },
    "seq": 44
}
```

## Chat Channel Management

### Assistant Delta Caching
```python
def cache_assistant_deltas(agent_session):
    """Assistant changes are cached in chat delta."""
    
    if not hasattr(agent_session, "chat_delta_cache"):
        agent_session.chat_delta_cache = []
    
    def on_assistant_delta(delta):
        agent_session.chat_delta_cache.append({
            "content": delta.content,
            "timestamp": delta.timestamp
        })
    
    agent_session.on("assistant_delta", on_assistant_delta)
```

### Chat Finalization
```python
def finalize_chat_on_completion(agent_session):
    """On lifecycle end/error, finalize chat from cached deltas."""
    
    if agent_session.lifecycle_phase in ["end", "error"]:
        # Build final chat from cached deltas
        final_chat = build_chat_from_deltas(agent_session.chat_delta_cache)
        
        # Store chat in session
        agent_session.final_chat = final_chat
        
        # Clear cache
        agent_session.chat_delta_cache = []
        
        return final_chat
    
    return None
```

## Timeouts

### agent.wait Timeout
- **Default**: 30 seconds (simple wait time)
- **Override**: timeoutMs parameter
- **Behavior**: Waiting timeout only, does not stop agent

### Agent Runtime Timeout
- **Default**: agents.defaults.timeoutSeconds (default 600 seconds)
- **Enforcement**: Enforced in runEmbeddedPiAgent abort timer
- **Behavior**: Actually stops/cancels the agent execution

### Timeout Handling
```python
def handle_agent_timeout(agent_session):
    """Handle agent execution timeout."""
    
    # Cancel current execution
    agent_session.cancel("timeout")
    
    # Log timeout event
    agent_session.stream.emit("lifecycle", {
        "type": "event",
        "event": "lifecycle", 
        "payload": {
            "phase": "error",
            "runId": agent_session.run_id,
            "status": "timeout",
            "error": "Agent execution timed out",
            "timestamp": current_timestamp()
        }
    })
    
    # Cleanup resources
    cleanup_agent_resources(agent_session)
```

## Early Termination Points

### Agent Timeout (Abort)
- **Cause**: Execution exceeds configured timeout
- **Action**: Abort signal sent to pi-agent-core
- **Result**: Lifecycle error event with timeout status

### AbortSignal
- **Cause**: External abort request
- **Action**: Immediate execution termination  
- **Result**: Lifecycle error event with aborted status

### Gateway Connection Abort or RPC Timeout
- **Cause**: Network issues or gateway failure
- **Action**: Connection closed, execution terminated
- **Result**: No lifecycle event (connection lost)

### agent.wait Timeout
- **Cause**: Wait operation times out
- **Action**: Wait operation cancelled
- **Result**: Timeout response, agent continues running